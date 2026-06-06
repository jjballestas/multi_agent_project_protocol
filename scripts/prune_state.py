#!/usr/bin/env python3
"""Prune hot protocol state into archives when measured thresholds are exceeded."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from measure_context_cost import measure
except ImportError:  # pragma: no cover
    from .measure_context_cost import measure


DEFAULT_CONFIG = {
    "enabled": True,
    "cold_start_tokens_hard": 20000,
    "done_ratio_hard": 85,
    "released_ratio_hard": 90,
    "recent_done_tasks": 2,
    "recent_released_claims": 4,
    "mailbox_keep_recent": 8,
}


@dataclass(frozen=True)
class Assessment:
    due: bool
    reasons: list[str]
    before_tokens: int


def read_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=4, ensure_ascii=True) + "\n", encoding="utf-8")


def maintenance_config(root: Path) -> dict[str, Any]:
    config = read_json(root / "protocol.config.json")
    maintenance = dict(DEFAULT_CONFIG)
    maintenance.update(config.get("maintenance") or {})
    return maintenance


def assess(root: Path) -> Assessment:
    cfg = maintenance_config(root)
    measured = measure(root)
    cold_tokens = int(measured["cold_start"]["total_tokens"])
    task_weight = measured["dead_weight"]["tasks"]
    claim_weight = measured["dead_weight"]["claims"]
    done_ratio = float(task_weight["done_percent"])
    released_ratio = float(claim_weight["released_percent"])
    done_count = int(task_weight["done"])
    released_count = int(claim_weight["released"])
    reasons: list[str] = []
    if cfg.get("enabled") is False:
        return Assessment(False, ["maintenance disabled"], cold_tokens)
    if cold_tokens >= int(cfg["cold_start_tokens_hard"]):
        reasons.append(f"cold_start_tokens {cold_tokens} >= {cfg['cold_start_tokens_hard']}")
    if done_count > int(cfg["recent_done_tasks"]) and done_ratio >= float(cfg["done_ratio_hard"]):
        reasons.append(f"done_ratio {done_ratio} >= {cfg['done_ratio_hard']}")
    if released_count > int(cfg["recent_released_claims"]) and released_ratio >= float(cfg["released_ratio_hard"]):
        reasons.append(f"released_ratio {released_ratio} >= {cfg['released_ratio_hard']}")
    return Assessment(bool(reasons), reasons, cold_tokens)


def archive_entries(
    hot_doc: dict[str, Any],
    archive_doc: dict[str, Any],
    field: str,
    id_field: str,
    terminal_status: str,
    keep_recent: int,
) -> tuple[int, dict[str, Any], dict[str, Any]]:
    hot_entries = [entry for entry in hot_doc.get(field, []) if isinstance(entry, dict)]
    terminal = [entry for entry in hot_entries if str(entry.get("status", "")).lower() == terminal_status]
    keep_ids = {str(entry.get(id_field)) for entry in terminal[-keep_recent:]} if keep_recent > 0 else set()
    to_archive = [entry for entry in terminal if str(entry.get(id_field)) not in keep_ids]
    archive_ids = {str(entry.get(id_field)) for entry in archive_doc.get(field, []) if isinstance(entry, dict)}

    hot_doc[field] = [
        entry
        for entry in hot_entries
        if str(entry.get("status", "")).lower() != terminal_status or str(entry.get(id_field)) in keep_ids
    ]
    for entry in to_archive:
        if str(entry.get(id_field)) not in archive_ids:
            archive_doc.setdefault(field, []).append(entry)
            archive_ids.add(str(entry.get(id_field)))
    return len(to_archive), hot_doc, archive_doc


def prune_project_state(root: Path, keep_recent: int) -> int:
    path = root / "Area_comun/state/PROJECT_STATE.json"
    state = read_json(path)
    tasks = [task for task in state.get("active_tasks", []) if isinstance(task, dict)]
    done = [task for task in tasks if str(task.get("status", "")).lower() == "done"]
    keep_ids = {str(task.get("id")) for task in done[-keep_recent:]} if keep_recent > 0 else set()
    kept = [
        task
        for task in tasks
        if str(task.get("status", "")).lower() != "done" or str(task.get("id")) in keep_ids
    ]
    removed = len(tasks) - len(kept)
    state["active_tasks"] = kept
    state["updated_by"] = "Codex"
    write_json(path, state)
    return removed


def prune_mailbox(root: Path, keep_recent: int) -> int:
    mailbox = root / "Area_comun/mailbox"
    answered = mailbox / "answered"
    archived = mailbox / "archived"
    archived.mkdir(parents=True, exist_ok=True)
    messages = sorted(answered.glob("MSG-*.md"), key=lambda path: path.name)
    move = messages[:-keep_recent] if keep_recent > 0 else messages
    for path in move:
        target = archived / path.name
        if not target.exists():
            shutil.move(str(path), str(target))
    return len(move)


def apply_prune(root: Path) -> dict[str, Any]:
    cfg = maintenance_config(root)
    state_dir = root / "Area_comun/state"
    task_hot_path = state_dir / "TASK_INDEX.json"
    task_archive_path = state_dir / "TASK_INDEX_ARCHIVE.json"
    claims_hot_path = state_dir / "CLAIMS.json"
    claims_archive_path = state_dir / "CLAIMS_ARCHIVE.json"

    before = measure(root)["cold_start"]["total_tokens"]

    tasks_moved, task_hot, task_archive = archive_entries(
        read_json(task_hot_path),
        read_json(task_archive_path),
        "tasks",
        "id",
        "done",
        int(cfg["recent_done_tasks"]),
    )
    claims_moved, claims_hot, claims_archive = archive_entries(
        read_json(claims_hot_path),
        read_json(claims_archive_path),
        "claims",
        "claim_id",
        "released",
        int(cfg["recent_released_claims"]),
    )
    task_hot["updated_by"] = "Codex"
    claims_hot["updated_by"] = "Codex"
    task_archive["updated_by"] = "Codex"
    claims_archive["updated_by"] = "Codex"
    write_json(task_hot_path, task_hot)
    write_json(task_archive_path, task_archive)
    write_json(claims_hot_path, claims_hot)
    write_json(claims_archive_path, claims_archive)
    project_removed = prune_project_state(root, int(cfg["recent_done_tasks"]))
    mailbox_moved = prune_mailbox(root, int(cfg["mailbox_keep_recent"]))

    after = measure(root)["cold_start"]["total_tokens"]
    return {
        "tasks_archived": tasks_moved,
        "claims_archived": claims_moved,
        "project_state_done_removed": project_removed,
        "mailbox_archived": mailbox_moved,
        "before_tokens": before,
        "after_tokens": after,
        "recovered_tokens": before - after,
    }


def run_check(root: Path) -> int:
    assessment = assess(root)
    if not assessment.due:
        print(f"OK: prune not due (cold_start_tokens={assessment.before_tokens}).")
        return 0
    print("PRUNE DUE:")
    for reason in assessment.reasons:
        print(f"- {reason}")
    print("Run: python scripts/prune_state.py --root . --apply")
    return 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check or apply systematic protocol state pruning.")
    parser.add_argument("--root", default=".", help="Repository or instance root.")
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true", help="Read-only threshold check.")
    mode.add_argument("--apply", action="store_true", help="Archive terminal hot state entries.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    if args.check:
        return run_check(root)
    result = apply_prune(root)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
