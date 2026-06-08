#!/usr/bin/env python3
"""Golden cases for submit_intent protocol write-path."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from runtime.protocol_replay import protocol_state_drift, write_genesis_reference  # noqa: E402
from runtime.submit_intent import IntentError, submit_intent  # noqa: E402


TASK_ID = "TASK-9300"
CLAIM_ID = f"CLAIM-{TASK_ID}-codex"
TIMESTAMP = "2026-06-07T00:00:00Z"
COMMIT = "abc123intentfixture"
RUNTIME_TIER_REQUIRED_PATHS = [
    "runtime/turn_schema.json",
    "scripts/validate_collaboration_state.py",
    "scripts/validate_collaboration_state.ps1",
    "scripts/scan_encoding.py",
    "scripts/scan_encoding.ps1",
    "scripts/scan_domain_neutrality.py",
    "scripts/scan_domain_neutrality.ps1",
    "scripts/measure_context_cost.py",
    "scripts/prune_state.py",
    "scripts/prune_state.ps1",
    ".github/workflows/validate.yml",
]


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=4, ensure_ascii=True, sort_keys=True) + "\n", encoding="ascii", newline="\n")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="ascii", newline="\n")


def run(command: list[str], cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=check)


def protocol_config(*, enforce: bool = False, authoritative: bool = False) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "adoption_tier": "runtime",
        "agent_roles": {
            "architect": "Claude",
            "implementer": "Codex",
            "human_owner": "operador humano",
        },
        "event_auth": {"enabled": False},
        "event_state": {
            "enabled": True,
            "materialize": True,
            "enforce": enforce,
            "authoritative": authoritative,
        },
        "domain_neutrality": {"enabled": True, "denylist": [], "scan_globs": [], "exempt_globs": []},
        "state_invariants": [{"path": "status", "equals": "active"}],
    }


def task(status: str = "ready") -> dict[str, Any]:
    return {
        "id": TASK_ID,
        "owner": "Codex",
        "status": status,
        "type": "implementation",
        "priority": "normal",
        "phase": "P2",
        "title": "Intent fixture",
        "file": f"Area_comun/tasks/{TASK_ID}.md",
        "depends_on": [],
        "relates_to": [],
        "relevant_files": [],
        "deliverables": [],
        "blocked_by_questions": [],
        "updated_at": "2026-06-07",
    }


def claim(*, status: str = "active", owner: str = "Codex", scope: list[str] | None = None) -> dict[str, Any]:
    return {
        "claim_id": CLAIM_ID if owner == "Codex" else f"CLAIM-{TASK_ID}-claude",
        "task_id": TASK_ID,
        "owner": owner,
        "status": status,
        "scope": scope
        or [
            f"Area_comun/tasks/{TASK_ID}.md",
            f"Area_comun/state/TASK_INDEX.json#{TASK_ID}",
            f"Area_comun/state/PROJECT_STATE.json#active_tasks/{TASK_ID}",
            "Area_comun/state/CLAIMS.json",
            "Area_comun/state/PROJECT_STATE.json",
        ],
        "started_at": "2026-06-07",
        "updated_at": "2026-06-07",
        "expires_at": "2026-06-08",
        "notes": "intent fixture",
    }


def hot_docs(status: str = "ready", *, claims: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    task_payload = task(status)
    return {
        "task_index": {"schema_version": "1.0", "tasks": [task_payload]},
        "project_state": {
            "status": "active",
            "decisions": ["DECISION-0001"],
            "active_tasks": [{"id": TASK_ID, "owner": "Codex", "status": status, "title": "Intent fixture"}],
        },
        "claims": {"schema_version": "1.0", "claims": claims if claims is not None else [claim()]},
    }


def write_hot_state(root: Path, docs: dict[str, Any], *, task_status: str = "ready") -> None:
    write_json(root / "Area_comun/state/TASK_INDEX.json", docs["task_index"])
    write_json(root / "Area_comun/state/PROJECT_STATE.json", docs["project_state"])
    write_json(root / "Area_comun/state/CLAIMS.json", docs["claims"])
    write_json(root / "Area_comun/state/CLAIMS_ARCHIVE.json", {"schema_version": "1.0", "claims": []})
    write_json(root / "Area_comun/state/TASK_INDEX_ARCHIVE.json", {"schema_version": "1.0", "tasks": []})
    write(root / "Area_comun/tasks" / f"{TASK_ID}.md", f"---\nid: {TASK_ID}\nstatus: {task_status}\n---\n\n# Fixture\n")
    write(root / "Area_comun/reports/HUMAN_REPORT_TEMPLATE.md", "# Human report\n")
    for folder in ("open", "answered", "archived"):
        write(root / "Area_comun/mailbox" / folder / ".gitkeep", "\n")


def build_fixture(
    root: Path,
    *,
    status: str = "ready",
    claims: list[dict[str, Any]] | None = None,
    genesis: bool = True,
    enforce: bool = False,
    authoritative: bool = False,
) -> None:
    write_json(root / "protocol.config.json", protocol_config(enforce=enforce, authoritative=authoritative))
    write_hot_state(root, hot_docs(status, claims=claims), task_status=status)
    for relative in RUNTIME_TIER_REQUIRED_PATHS:
        source = ROOT / relative
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    if genesis:
        write_genesis_reference(root, actor_id="Codex", timestamp=TIMESTAMP, commit=COMMIT)


def state_bytes(root: Path) -> dict[str, bytes]:
    return {
        path.relative_to(root).as_posix(): path.read_bytes()
        for path in sorted(root.rglob("*"))
        if path.is_file()
    }


def task_status_intent(from_status: str = "ready", to_status: str = "in_progress") -> dict[str, Any]:
    return {
        "task_status": {
            "task_id": TASK_ID,
            "from": from_status,
            "to": to_status,
            "idempotency_key": "intent-fixture:task-status",
        }
    }


def case_task_status_materializes_json_and_task_file() -> None:
    with tempfile.TemporaryDirectory(prefix="intent-task-status-") as temp:
        root = Path(temp)
        build_fixture(root, status="ready")
        result = submit_intent(root, "Codex", task_status_intent(), timestamp=TIMESTAMP, commit=COMMIT)
        assert result["event"]["type"] == "intent.applied"
        index = read_json(root / "Area_comun/state/TASK_INDEX.json")
        project = read_json(root / "Area_comun/state/PROJECT_STATE.json")
        task_file = (root / f"Area_comun/tasks/{TASK_ID}.md").read_text(encoding="utf-8-sig")
        assert index["tasks"][0]["status"] == "in_progress"
        assert project["active_tasks"][0]["status"] == "in_progress"
        assert "status: in_progress" in task_file
        assert protocol_state_drift(root)["has_drift"] is False


def case_claim_release_materializes_claims() -> None:
    with tempfile.TemporaryDirectory(prefix="intent-claim-release-") as temp:
        root = Path(temp)
        build_fixture(root, status="in_progress")
        result = submit_intent(
            root,
            "Codex",
            {"claim": {"op": "release", "claim_id": CLAIM_ID, "idempotency_key": "intent-fixture:claim-release"}},
            timestamp=TIMESTAMP,
            commit=COMMIT,
        )
        assert result["event"]["type"] == "intent.applied"
        claims = read_json(root / "Area_comun/state/CLAIMS.json")["claims"]
        assert claims[0]["status"] == "released", claims
        assert protocol_state_drift(root)["has_drift"] is False


def case_decision_materializes_project_state() -> None:
    with tempfile.TemporaryDirectory(prefix="intent-decision-") as temp:
        root = Path(temp)
        build_fixture(root, claims=[claim(owner="Claude")])
        result = submit_intent(
            root,
            "Claude",
            {"decision": {"decision_id": "DECISION-0099", "idempotency_key": "intent-fixture:decision"}},
            timestamp=TIMESTAMP,
            commit=COMMIT,
        )
        assert result["event"]["type"] == "intent.applied"
        decisions = read_json(root / "Area_comun/state/PROJECT_STATE.json")["decisions"]
        assert decisions == ["DECISION-0001", "DECISION-0099"], decisions
        assert protocol_state_drift(root)["has_drift"] is False


def case_project_narrative_materializes_project_state() -> None:
    with tempfile.TemporaryDirectory(prefix="intent-project-narrative-") as temp:
        root = Path(temp)
        build_fixture(root, claims=[claim(owner="Claude", scope=["Area_comun/state/PROJECT_STATE.json"])])
        result = submit_intent(
            root,
            "Claude",
            {
                "project_narrative": {
                    "append": {"next_actions": ["Revisar ventana enforce"]},
                    "idempotency_key": "intent-fixture:project-narrative",
                }
            },
            timestamp=TIMESTAMP,
            commit=COMMIT,
        )
        assert result["event"]["type"] == "intent.applied"
        project = read_json(root / "Area_comun/state/PROJECT_STATE.json")
        assert project["next_actions"] == ["Revisar ventana enforce"], project
        assert protocol_state_drift(root)["has_drift"] is False


def case_protocol_prune_removes_terminal_hot_entries() -> None:
    with tempfile.TemporaryDirectory(prefix="intent-protocol-prune-") as temp:
        root = Path(temp)
        build_fixture(
            root,
            status="done",
            claims=[
                claim(status="released"),
                claim(owner="Claude", scope=[
                    "Area_comun/state/TASK_INDEX.json",
                    "Area_comun/state/PROJECT_STATE.json",
                    "Area_comun/state/CLAIMS.json",
                ]),
            ],
        )
        result = submit_intent(
            root,
            "Claude",
            {
                "protocol_prune": {
                    "task_ids": [TASK_ID],
                    "active_task_ids": [TASK_ID],
                    "claim_ids": [CLAIM_ID],
                    "idempotency_key": "intent-fixture:protocol-prune",
                }
            },
            timestamp=TIMESTAMP,
            commit=COMMIT,
        )
        assert result["event"]["type"] == "intent.applied"
        assert read_json(root / "Area_comun/state/TASK_INDEX.json")["tasks"] == []
        assert read_json(root / "Area_comun/state/PROJECT_STATE.json")["active_tasks"] == []
        claims = read_json(root / "Area_comun/state/CLAIMS.json")["claims"]
        assert [item["claim_id"] for item in claims] == [f"CLAIM-{TASK_ID}-claude"], claims
        assert protocol_state_drift(root)["has_drift"] is False


def case_invalid_scope_rejected_without_changes() -> None:
    with tempfile.TemporaryDirectory(prefix="intent-invalid-scope-") as temp:
        root = Path(temp)
        build_fixture(root, claims=[claim(scope=[f"Area_comun/tasks/{TASK_ID}.md"])])
        before = state_bytes(root)
        try:
            submit_intent(root, "Codex", task_status_intent(), timestamp=TIMESTAMP, commit=COMMIT)
        except IntentError as exc:
            assert "outside active claim scope" in str(exc)
        else:
            raise AssertionError("invalid scope intent was accepted")
        assert state_bytes(root) == before


def case_materialization_failure_rolls_back_event_and_hot_state() -> None:
    with tempfile.TemporaryDirectory(prefix="intent-atomic-") as temp:
        root = Path(temp)
        build_fixture(root, status="ready")
        before = state_bytes(root)
        try:
            submit_intent(root, "Codex", task_status_intent(), timestamp=TIMESTAMP, commit=COMMIT, fail_after_writes=1)
        except IntentError:
            pass
        else:
            raise AssertionError("simulated materialization failure did not fail")
        assert state_bytes(root) == before


def case_idempotent_retry_does_not_duplicate() -> None:
    with tempfile.TemporaryDirectory(prefix="intent-idempotent-") as temp:
        root = Path(temp)
        build_fixture(root, status="ready")
        first = submit_intent(root, "Codex", task_status_intent(), timestamp=TIMESTAMP, commit=COMMIT)
        second = submit_intent(root, "Codex", task_status_intent(), timestamp=TIMESTAMP, commit=COMMIT)
        events = [
            json.loads(line)
            for line in (root / "runtime/state/events.jsonl").read_text(encoding="utf-8-sig").splitlines()
            if line.strip()
        ]
        intent_events = [event for event in events if event.get("type") == "intent.applied"]
        assert len(intent_events) == 1, events
        assert first["event"]["seq"] == second["event"]["seq"]
        assert second.get("deduped") is True
        assert protocol_state_drift(root)["has_drift"] is False


def build_and_apply_for_determinism() -> dict[str, bytes]:
    root = Path(tempfile.mkdtemp(prefix="intent-deterministic-"))
    try:
        build_fixture(root, status="ready")
        submit_intent(root, "Codex", task_status_intent(), timestamp=TIMESTAMP, commit=COMMIT)
        return {
            "events": (root / "runtime/state/events.jsonl").read_bytes(),
            "snapshot": (root / "runtime/state/snapshot.json").read_bytes(),
            "task_index": (root / "Area_comun/state/TASK_INDEX.json").read_bytes(),
            "project_state": (root / "Area_comun/state/PROJECT_STATE.json").read_bytes(),
            "claims": (root / "Area_comun/state/CLAIMS.json").read_bytes(),
        }
    finally:
        shutil.rmtree(root, ignore_errors=True)


def case_deterministic_bytes_for_same_inputs() -> None:
    assert build_and_apply_for_determinism() == build_and_apply_for_determinism()


def case_enforce_on_sequence_passes_and_manual_edit_fails() -> None:
    with tempfile.TemporaryDirectory(prefix="intent-enforce-") as temp:
        root = Path(temp)
        build_fixture(root, status="ready", enforce=True, authoritative=True)
        submit_intent(root, "Codex", task_status_intent(), timestamp=TIMESTAMP, commit=COMMIT)
        ok = run([sys.executable, str(ROOT / "scripts/validate_collaboration_state.py"), "--root", str(root)])
        assert "OK" in ok.stdout, ok.stdout
        project = read_json(root / "Area_comun/state/PROJECT_STATE.json")
        project["active_tasks"][0]["title"] = "Manual divergence"
        write_json(root / "Area_comun/state/PROJECT_STATE.json", project)
        failed = run([sys.executable, str(ROOT / "scripts/validate_collaboration_state.py"), "--root", str(root)], check=False)
        assert failed.returncode != 0, failed.stdout
        assert "Runtime protocol state drift detected" in failed.stdout, failed.stdout


def case_powershell_wrapper_parity_if_available() -> None:
    shell = shutil.which("pwsh") or shutil.which("powershell")
    if not shell:
        return
    with tempfile.TemporaryDirectory(prefix="intent-wrapper-") as temp:
        root = Path(temp)
        build_fixture(root, status="ready")
        intent_path = root / "intent.json"
        write_json(intent_path, task_status_intent())
        result = run(
            [
                shell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(ROOT / "runtime/submit_intent.ps1"),
                "-Root",
                str(root),
                "-ActorId",
                "Codex",
                "-Timestamp",
                TIMESTAMP,
                "-Commit",
                COMMIT,
                "-Intent",
                str(intent_path),
            ]
        )
        payload = json.loads(result.stdout)
        assert payload["applied"] is True, result.stdout
        assert protocol_state_drift(root)["has_drift"] is False


def main() -> int:
    cases = [
        case_task_status_materializes_json_and_task_file,
        case_claim_release_materializes_claims,
        case_decision_materializes_project_state,
        case_project_narrative_materializes_project_state,
        case_protocol_prune_removes_terminal_hot_entries,
        case_invalid_scope_rejected_without_changes,
        case_materialization_failure_rolls_back_event_and_hot_state,
        case_idempotent_retry_does_not_duplicate,
        case_deterministic_bytes_for_same_inputs,
        case_enforce_on_sequence_passes_and_manual_edit_fails,
        case_powershell_wrapper_parity_if_available,
    ]
    failures = []
    for case in cases:
        try:
            case()
        except Exception as exc:  # noqa: BLE001 - compact golden failure reporting
            failures.append({"case": case.__name__, "error": str(exc)})
    if failures:
        print(json.dumps({"status": "FAILED", "failures": failures}, indent=2))
        return 1
    print(f"OK: {len(cases)} intent flow golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
