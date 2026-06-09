#!/usr/bin/env python3
"""Apply validated runtime turn reports to protocol files."""

from __future__ import annotations

import json
import re
import shutil
import tempfile
from copy import deepcopy
from pathlib import Path
from typing import Any

try:
    from .eventlog import (
        EventLogError,
        EventWriter,
        STATE_DIR,
        assert_snapshot_matches,
        observability_enabled,
        read_protocol_config,
        runtime_state_has_content,
    )
    from .gate import run_gate
    from .protocol_replay import (
        ProtocolMaterializationError,
        ProtocolStateDriftError,
        event_state_config_error,
        enforce_protocol_state_drift,
        materialize_from_event_log_if_enabled,
    )
    from .review_qa import (
        checks_with_signatures,
        has_consecutive_failure,
        max_qa_cycles,
        qa_attempts_after_failure,
        review_qa_span,
        task_author,
    )
    from .turn_validate import derive_transition_scopes, validate_turn
    from .vcs import VcsError, commit_turn, discard_worktree_changes
except ImportError:  # pragma: no cover - direct script execution
    from eventlog import (
        EventLogError,
        EventWriter,
        STATE_DIR,
        assert_snapshot_matches,
        observability_enabled,
        read_protocol_config,
        runtime_state_has_content,
    )
    from gate import run_gate
    from protocol_replay import (
        ProtocolMaterializationError,
        ProtocolStateDriftError,
        event_state_config_error,
        enforce_protocol_state_drift,
        materialize_from_event_log_if_enabled,
    )
    from review_qa import checks_with_signatures, has_consecutive_failure, max_qa_cycles, qa_attempts_after_failure, review_qa_span, task_author
    from turn_validate import derive_transition_scopes, validate_turn
    from vcs import VcsError, commit_turn, discard_worktree_changes


class ApplyError(RuntimeError):
    pass


RuntimeStateBackup = tuple[Path, Path | None]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=4, ensure_ascii=False), encoding="utf-8")


def assert_event_state_config_valid(root: Path) -> None:
    error = event_state_config_error(read_protocol_config(root))
    if error:
        raise ApplyError(f"invalid event_state config: {error}")


def snapshot_runtime_state(root: Path) -> RuntimeStateBackup:
    temp_root = Path(tempfile.mkdtemp(prefix="runtime-state-backup-"))
    state_dir = root / STATE_DIR
    backup_dir = temp_root / "state"
    if state_dir.exists():
        shutil.copytree(state_dir, backup_dir)
        return temp_root, backup_dir
    return temp_root, None


def restore_runtime_state(root: Path, backup: RuntimeStateBackup) -> None:
    temp_root, backup_dir = backup
    state_dir = root / STATE_DIR
    if state_dir.exists():
        shutil.rmtree(state_dir)
    if backup_dir is not None and backup_dir.exists():
        shutil.copytree(backup_dir, state_dir)
    shutil.rmtree(temp_root, ignore_errors=True)


def cleanup_runtime_state_backup(backup: RuntimeStateBackup) -> None:
    shutil.rmtree(backup[0], ignore_errors=True)


def runtime_state_commit_paths(root: Path) -> list[str]:
    if not runtime_state_has_content(root):
        return []
    return [STATE_DIR.as_posix()]


def active_claim_for_report(root: Path, report: dict[str, Any]) -> dict[str, Any] | None:
    claims_doc = read_json(root / "Area_comun" / "state" / "CLAIMS.json")
    for claim in claims_doc.get("claims") or []:
        if (
            isinstance(claim, dict)
            and claim.get("status") == "active"
            and claim.get("task_id") == report.get("task_id")
            and claim.get("owner") == report.get("agent")
        ):
            return dict(claim)
    return None


def report_attempt_id(report: dict[str, Any]) -> str:
    return str(report.get("attempt_id") or report.get("turn_id") or "attempt-unknown")


def report_transition_name(report: dict[str, Any]) -> str:
    transition = (report.get("transitions") or {}).get("task_status")
    if isinstance(transition, dict):
        return f"{transition.get('from')}->{transition.get('to')}"
    return str(report.get("outcome") or "no_transition")


def review_qa_observability(root: Path, report: dict[str, Any], writer: EventWriter) -> dict[str, Any] | None:
    if not observability_enabled(read_protocol_config(root)):
        return None
    transitions = report.get("transitions") or {}
    payload = transitions.get("review_qa")
    transition = transitions.get("task_status")
    if not isinstance(payload, dict) or not isinstance(transition, dict):
        return None
    event = str(payload.get("event") or "")
    if not event:
        return None
    attempt_id = str(payload.get("attempt_id") or report_attempt_id(report))
    return {
        "event": event,
        "span": review_qa_span(
            task_id=str(report.get("task_id") or ""),
            event=event,
            from_status=str(transition.get("from") or ""),
            to_status=str(transition.get("to") or ""),
            actor=str(report.get("agent") or ""),
            run_id=str(report.get("turn_id") or "run-unknown"),
            attempt_id=attempt_id,
            seq=writer.next_seq(),
        ),
    }


def emit_runtime_eventlog(root: Path, report: dict[str, Any], claim: dict[str, Any] | None) -> list[dict[str, Any]]:
    task_id = str(report.get("task_id") or "")
    actor = str(report.get("agent") or "")
    if not task_id or task_id == "none" or not actor:
        return []

    attempt_id = report_attempt_id(report)
    writer = EventWriter(root)
    claim_event = writer.acquire_claim(
        task_id=task_id,
        owner=actor,
        lease_until=str((claim or {}).get("expires_at") or ""),
        idempotency_key=f"{actor}:{task_id}:claim:{attempt_id}:0",
        claim_id=str((claim or {}).get("claim_id") or ""),
    )
    intent_payload = {
        "turn_id": report.get("turn_id"),
        "outcome": report.get("outcome"),
        "claim_id": (claim or {}).get("claim_id"),
        "changed_paths": list(report.get("changed_paths") or []),
        "transitions": deepcopy(report.get("transitions") or {}),
    }
    task_payload = task_payload_after_apply(root, task_id)
    if task_payload:
        intent_payload["task"] = task_payload
    review_qa = review_qa_observability(root, report, writer)
    if review_qa:
        intent_payload["review_qa"] = review_qa
    intent_event = writer.apply_intent(
        task_id=task_id,
        actor_id=actor,
        transition=report_transition_name(report),
        attempt_id=attempt_id,
        fencing_token=int(claim_event["fencing_token"]),
        payload=intent_payload,
    )
    writer.write_snapshot()
    return [claim_event, intent_event]


def task_payload_after_apply(root: Path, task_id: str) -> dict[str, Any] | None:
    index_path = root / "Area_comun" / "state" / "TASK_INDEX.json"
    if not index_path.exists():
        return None
    index = read_json(index_path)
    for task in index.get("tasks") or []:
        if isinstance(task, dict) and task.get("id") == task_id:
            return deepcopy(task)
    return None


def assert_runtime_snapshot_if_active(root: Path) -> None:
    if runtime_state_has_content(root):
        assert_snapshot_matches(root)


def materialization_commit_paths(result: dict[str, Any] | None) -> list[str]:
    if not isinstance(result, dict) or result.get("materialized") is not True:
        return []
    return [str(path) for path in result.get("paths") or [] if str(path).strip()]


def transition_commit_paths(report: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    for path in derive_transition_scopes(report):
        clean = str(path or "").split("#", 1)[0].strip()
        if clean and clean not in paths:
            paths.append(clean)
    return paths


def with_terminal_claim_release(report: dict[str, Any], claim: dict[str, Any] | None) -> dict[str, Any]:
    if not claim or not str(claim.get("claim_id") or "").strip():
        return report

    transitions = deepcopy(report.get("transitions") or {})
    claims = transitions.get("claims")
    if claims is None:
        claims = []
    if not isinstance(claims, list):
        return report

    claim_id = str(claim["claim_id"])
    if any(isinstance(item, dict) and item.get("claim_id") == claim_id for item in claims):
        return report

    task_transition = transitions.get("task_status")
    to_status = str((task_transition or {}).get("to") or "") if isinstance(task_transition, dict) else ""
    should_release = to_status in {"in_review", "done", "blocked"} or report.get("outcome") == "blocked"
    if not should_release:
        return report

    updated = deepcopy(report)
    updated_transitions = dict(transitions)
    updated_claims = [deepcopy(item) for item in claims]
    updated_claims.append({"op": "release", "claim_id": claim_id})
    updated_transitions["claims"] = updated_claims
    updated["transitions"] = updated_transitions
    return updated


def set_task_file_status(path: Path, status: str) -> None:
    text = path.read_text(encoding="utf-8-sig")
    updated = re.sub(r"(?m)^status:\s*\S+\s*$", f"status: {status}", text, count=1)
    if updated == text:
        raise ApplyError(f"Task file has no status field: {path}")
    path.write_text(updated, encoding="utf-8")


def set_task_status(root: Path, task_id: str, status: str) -> None:
    index_path = root / "Area_comun" / "state" / "TASK_INDEX.json"
    index = read_json(index_path)
    task_file: str | None = None
    found = False
    for task in index.get("tasks") or []:
        if task.get("id") == task_id:
            task["status"] = status
            task_file = task.get("file")
            found = True
            break
    if not found:
        raise ApplyError(f"Task not found in hot TASK_INDEX: {task_id}")
    write_json(index_path, index)
    if task_file:
        set_task_file_status(root / task_file, status)

    project_path = root / "Area_comun" / "state" / "PROJECT_STATE.json"
    project = read_json(project_path)
    for task in project.get("active_tasks") or []:
        if task.get("id") == task_id:
            task["status"] = status
            break
    write_json(project_path, project)


def increment_int(task: dict[str, Any], key: str, amount: int = 1) -> int:
    try:
        value = int(task.get(key) or 0)
    except (TypeError, ValueError):
        value = 0
    value += amount
    task[key] = value
    return value


def ensure_original_author(root: Path, task_id: str) -> None:
    index_path = root / "Area_comun" / "state" / "TASK_INDEX.json"
    index = read_json(index_path)
    changed = False
    for task in index.get("tasks") or []:
        if task.get("id") != task_id:
            continue
        if not str(task.get("original_author") or "").strip():
            original_author = str(task.get("owner") or "").strip()
            if original_author:
                task["original_author"] = original_author
                changed = True
        break
    if changed:
        write_json(index_path, index)


def apply_review_qa_transition(root: Path, report: dict[str, Any]) -> None:
    transitions = report.get("transitions") or {}
    payload = transitions.get("review_qa")
    if not isinstance(payload, dict):
        return

    index_path = root / "Area_comun" / "state" / "TASK_INDEX.json"
    index = read_json(index_path)
    task: dict[str, Any] | None = None
    for item in index.get("tasks") or []:
        if item.get("id") == report.get("task_id"):
            task = item
            break
    if task is None:
        raise ApplyError(f"Task not found in hot TASK_INDEX: {report.get('task_id')}")

    event = str(payload.get("event") or "")
    transition = transitions.get("task_status") or {}
    from_status = str(transition.get("from") or "")
    to_status = str(transition.get("to") or "")
    attempt_id = str(payload.get("attempt_id") or report.get("attempt_id") or "attempt-unknown")
    actor = str(report.get("agent") or "")

    if event in {"reject_review", "approve_review"}:
        increment_int(task, "review_attempts")
    if event == "fail_qa":
        task["qa_attempts"] = qa_attempts_after_failure(task)

    if event in {"reject_review", "fail_qa"}:
        checks = checks_with_signatures([item for item in payload.get("checks_failed") or [] if isinstance(item, dict)])
        defects = task.setdefault("defect_log", [])
        if not isinstance(defects, list):
            defects = []
            task["defect_log"] = defects
        loop_cut = event == "fail_qa" and has_consecutive_failure(task, checks)
        cycle_limit = max_qa_cycles(read_json(root / "protocol.config.json"))
        escalation_reason = None
        if event == "fail_qa" and loop_cut:
            escalation_reason = "loop_cut"
        elif event == "fail_qa" and int(task.get("qa_attempts") or 0) > cycle_limit:
            escalation_reason = "max_qa_cycles"
        defect = {
            "event": event,
            "attempt_id": attempt_id,
            "actor": actor,
            "from": from_status,
            "to": to_status,
            "checks_failed": checks,
        }
        if escalation_reason:
            defect["escalation_reason"] = escalation_reason
            task["quality_escalation_reason"] = escalation_reason
        defects.append(defect)

    if event == "pass_qa":
        task["qa_evidence"] = list(payload.get("evidence") or [])
        task["qa_passed_by"] = actor
    elif event == "approve_review":
        task["review_approved_by"] = actor
    elif event == "assign_fix":
        increment_int(task, "attempt")
        assignee = str(payload.get("assignee") or task_author(task, payload) or task.get("owner") or "")
        if assignee:
            task["assigned_to"] = assignee

    write_json(index_path, index)


def apply_claim_transitions(root: Path, transitions: list[dict[str, Any]]) -> None:
    claims_path = root / "Area_comun" / "state" / "CLAIMS.json"
    claims_doc = read_json(claims_path)
    claims = claims_doc.setdefault("claims", [])
    for transition in transitions:
        op = transition.get("op")
        claim_id = transition.get("claim_id")
        if op == "acquire":
            task_id = str(transition.get("task_id") or "none")
            if task_id != "none":
                ensure_original_author(root, task_id)
            if any(claim.get("claim_id") == claim_id for claim in claims):
                raise ApplyError(f"Claim already exists: {claim_id}")
            claims.append(
                {
                    "claim_id": claim_id,
                    "task_id": task_id,
                    "owner": transition.get("owner", "Codex"),
                    "status": "active",
                    "scope": transition.get("scope") or [],
                    "started_at": transition.get("started_at", "2026-06-05"),
                    "updated_at": transition.get("updated_at", "2026-06-05"),
                    "expires_at": transition.get("expires_at", "2026-06-06"),
                    "notes": transition.get("notes", "acquired by runtime"),
                }
            )
        elif op == "release":
            for claim in claims:
                if claim.get("claim_id") == claim_id:
                    claim["status"] = "released"
                    break
            else:
                raise ApplyError(f"Claim not found for release: {claim_id}")
    write_json(claims_path, claims_doc)


def apply_mailbox_transitions(root: Path, transitions: list[dict[str, Any]]) -> None:
    mailbox_root = root / "Area_comun" / "mailbox"
    for transition in transitions:
        message_id = transition.get("message_id")
        if not message_id:
            continue
        if transition.get("op") == "send":
            target = mailbox_root / "open" / f"{message_id}.md"
            target.write_text(
                f"---\nmessage_id: {message_id}\nstatus: open\n---\n\n# {message_id}\n",
                encoding="utf-8",
            )
        elif transition.get("op") in {"answer", "archive"}:
            source = mailbox_root / "open" / f"{message_id}.md"
            folder = "answered" if transition.get("op") == "answer" else "archived"
            target = mailbox_root / folder / f"{message_id}.md"
            if source.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(source), str(target))


def apply_turn(report: dict[str, Any], root: Path) -> dict[str, Any]:
    root = root.resolve()
    assert_event_state_config_valid(root)
    errors = validate_turn(report, root)
    if errors:
        raise ApplyError("; ".join(errors))
    transitions = report.get("transitions") or {}
    task_transition = transitions.get("task_status")
    if isinstance(task_transition, dict):
        ensure_original_author(root, str(report["task_id"]))
        set_task_status(root, str(report["task_id"]), str(task_transition["to"]))
    apply_review_qa_transition(root, report)
    apply_claim_transitions(root, transitions.get("claims") or [])
    apply_mailbox_transitions(root, transitions.get("mailbox") or [])
    return {"applied": True}


def block_task(root: Path, task_id: str) -> None:
    set_task_status(root, task_id, "blocked")


def apply_gate_and_commit(report: dict[str, Any], root: Path, allow_policy: bool = False) -> dict[str, Any]:
    root = root.resolve()
    assert_event_state_config_valid(root)
    runtime_backup = snapshot_runtime_state(root)
    materialization: dict[str, Any] | None = None
    protocol_drift_gate: dict[str, Any] | None = None
    try:
        try:
            assert_runtime_snapshot_if_active(root)
        except EventLogError as exc:
            restore_runtime_state(root, runtime_backup)
            block_task(root, str(report["task_id"]))
            return {"green": False, "reverted": True, "blocked": True, "gate": None, "error": str(exc)}
        try:
            protocol_drift_gate = enforce_protocol_state_drift(root)
        except ProtocolStateDriftError as exc:
            restore_runtime_state(root, runtime_backup)
            block_task(root, str(report["task_id"]))
            return {"green": False, "reverted": True, "blocked": True, "gate": None, "error": str(exc)}
        claim = active_claim_for_report(root, report)
        report_for_apply = with_terminal_claim_release(report, claim)
        apply_turn(report_for_apply, root)
        eventlog_events = emit_runtime_eventlog(root, report_for_apply, claim)
        try:
            materialization = materialize_from_event_log_if_enabled(root)
        except ProtocolMaterializationError as exc:
            discard_worktree_changes(root)
            restore_runtime_state(root, runtime_backup)
            block_task(root, str(report["task_id"]))
            return {"green": False, "reverted": True, "blocked": True, "gate": None, "error": str(exc)}
        try:
            protocol_drift_gate = enforce_protocol_state_drift(root)
        except ProtocolStateDriftError as exc:
            discard_worktree_changes(root)
            restore_runtime_state(root, runtime_backup)
            block_task(root, str(report["task_id"]))
            return {"green": False, "reverted": True, "blocked": True, "gate": None, "error": str(exc)}
        gate = run_gate(root)
        if gate["green"]:
            try:
                assert_runtime_snapshot_if_active(root)
            except EventLogError as exc:
                discard_worktree_changes(root)
                restore_runtime_state(root, runtime_backup)
                block_task(root, str(report["task_id"]))
                return {"green": False, "reverted": True, "blocked": True, "gate": gate, "error": str(exc)}
            paths = [
                *(report_for_apply.get("changed_paths") or []),
                *transition_commit_paths(report_for_apply),
                *runtime_state_commit_paths(root),
                *materialization_commit_paths(materialization),
            ]
            try:
                commit = commit_turn(root, report_for_apply["commit_message"], paths, allow_policy=allow_policy)
                cleanup_runtime_state_backup(runtime_backup)
                return {
                    "green": True,
                    "commit": commit,
                    "gate": gate,
                    "eventlog_events": eventlog_events,
                    "protocol_materialization": materialization,
                    "protocol_drift_gate": protocol_drift_gate,
                }
            except VcsError as exc:
                discard_worktree_changes(root)
                restore_runtime_state(root, runtime_backup)
                block_task(root, str(report["task_id"]))
                return {"green": False, "reverted": True, "blocked": True, "gate": gate, "error": str(exc)}
        discard_worktree_changes(root)
        restore_runtime_state(root, runtime_backup)
        block_task(root, str(report["task_id"]))
        return {"green": False, "reverted": True, "blocked": True, "gate": gate}
    except Exception:
        discard_worktree_changes(root)
        restore_runtime_state(root, runtime_backup)
        raise
