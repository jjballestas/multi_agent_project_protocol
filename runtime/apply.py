#!/usr/bin/env python3
"""Apply validated runtime turn reports to protocol files."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any

try:
    from .gate import run_gate
    from .turn_validate import validate_turn
    from .vcs import VcsError, commit_turn, discard_worktree_changes
except ImportError:  # pragma: no cover - direct script execution
    from gate import run_gate
    from turn_validate import validate_turn
    from vcs import VcsError, commit_turn, discard_worktree_changes


class ApplyError(RuntimeError):
    pass


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=4, ensure_ascii=False), encoding="utf-8")


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


def apply_claim_transitions(root: Path, transitions: list[dict[str, Any]]) -> None:
    claims_path = root / "Area_comun" / "state" / "CLAIMS.json"
    claims_doc = read_json(claims_path)
    claims = claims_doc.setdefault("claims", [])
    for transition in transitions:
        op = transition.get("op")
        claim_id = transition.get("claim_id")
        if op == "acquire":
            if any(claim.get("claim_id") == claim_id for claim in claims):
                raise ApplyError(f"Claim already exists: {claim_id}")
            claims.append(
                {
                    "claim_id": claim_id,
                    "task_id": transition.get("task_id", "none"),
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
    errors = validate_turn(report, root)
    if errors:
        raise ApplyError("; ".join(errors))
    transitions = report.get("transitions") or {}
    task_transition = transitions.get("task_status")
    if isinstance(task_transition, dict):
        set_task_status(root, str(report["task_id"]), str(task_transition["to"]))
    apply_claim_transitions(root, transitions.get("claims") or [])
    apply_mailbox_transitions(root, transitions.get("mailbox") or [])
    return {"applied": True}


def block_task(root: Path, task_id: str) -> None:
    set_task_status(root, task_id, "blocked")


def apply_gate_and_commit(report: dict[str, Any], root: Path, allow_policy: bool = False) -> dict[str, Any]:
    root = root.resolve()
    apply_turn(report, root)
    gate = run_gate(root)
    if gate["green"]:
        try:
            commit = commit_turn(root, report["commit_message"], report.get("changed_paths") or [], allow_policy=allow_policy)
            return {"green": True, "commit": commit, "gate": gate}
        except VcsError as exc:
            discard_worktree_changes(root)
            block_task(root, str(report["task_id"]))
            return {"green": False, "reverted": True, "blocked": True, "gate": gate, "error": str(exc)}
    discard_worktree_changes(root)
    block_task(root, str(report["task_id"]))
    return {"green": False, "reverted": True, "blocked": True, "gate": gate}
