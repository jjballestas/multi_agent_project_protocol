#!/usr/bin/env python3
"""Shared context loaders for the protocol runtime."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


PRIORITY_RANK = {"critical": 4, "high": 3, "normal": 2, "low": 1}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def merge_by_array_field(hot: dict[str, Any], archive: dict[str, Any] | None, field: str) -> dict[str, Any]:
    merged = dict(hot)
    merged[field] = list(hot.get(field) or []) + list((archive or {}).get(field) or [])
    return merged


def parse_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    metadata: dict[str, Any] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        match = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*):\s*(.*?)\s*$", line)
        if not match:
            continue
        key, value = match.groups()
        metadata[key] = parse_scalar(value)
    return metadata


def parse_scalar(value: str) -> Any:
    value = value.strip()
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [part.strip().strip("\"'") for part in inner.split(",")]
    return value.strip("\"'")


def load_state(root: Path) -> dict[str, Any]:
    root = root.resolve()
    mailbox_open = []
    open_dir = root / "Area_comun" / "mailbox" / "open"
    if open_dir.exists():
        for path in sorted(open_dir.glob("MSG-*.md")):
            metadata = parse_frontmatter(path)
            metadata["_path"] = path.relative_to(root).as_posix()
            mailbox_open.append(metadata)

    state_dir = root / "Area_comun" / "state"
    task_index = read_json(state_dir / "TASK_INDEX.json")
    claims = read_json(state_dir / "CLAIMS.json")
    task_archive_path = state_dir / "TASK_INDEX_ARCHIVE.json"
    claims_archive_path = state_dir / "CLAIMS_ARCHIVE.json"
    if task_archive_path.exists():
        task_index = merge_by_array_field(task_index, read_json(task_archive_path), "tasks")
    if claims_archive_path.exists():
        claims = merge_by_array_field(claims, read_json(claims_archive_path), "claims")

    return {
        "root": root,
        "project": read_json(state_dir / "PROJECT_STATE.json"),
        "task_index": task_index,
        "claims": claims,
        "mailbox_open": mailbox_open,
    }


def tasks_by_id(state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    tasks = state.get("task_index", {}).get("tasks") or []
    return {task.get("id"): task for task in tasks if isinstance(task, dict) and task.get("id")}


def active_claims(state: dict[str, Any]) -> list[dict[str, Any]]:
    claims = state.get("claims", {}).get("claims") or []
    return [claim for claim in claims if isinstance(claim, dict) and claim.get("status") == "active"]


def is_claim_scope_covering(scope_entry: str, path: str) -> bool:
    scope = scope_entry.replace("\\", "/").strip()
    candidate = path.replace("\\", "/").strip()
    if scope.endswith("/"):
        return candidate.startswith(scope)
    return candidate == scope


def path_is_claimed_by_other(path: str, owner: str, state: dict[str, Any]) -> bool:
    for claim in active_claims(state):
        if claim.get("owner") == owner:
            continue
        for scope in claim.get("scope") or []:
            if is_claim_scope_covering(str(scope), path):
                return True
    return False


def task_is_claimed_by_other(task: dict[str, Any], state: dict[str, Any]) -> bool:
    owner = str(task.get("owner") or "")
    task_id = task.get("id")
    task_file = task.get("file") or task.get("task_file")
    for claim in active_claims(state):
        if claim.get("owner") == owner:
            continue
        if claim.get("task_id") == task_id:
            return True
        for path in [task_file, *list(task.get("relevant_files") or [])]:
            if path and path_is_claimed_by_other(str(path), owner, state):
                return True
    return False


def priority_value(task: dict[str, Any]) -> int:
    return PRIORITY_RANK.get(str(task.get("priority") or "normal"), 2)
