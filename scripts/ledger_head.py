#!/usr/bin/env python3
"""Read complete event-log records and their governed materialization paths."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any


def _events(root: Path) -> tuple[list[dict[str, Any]], bool]:
    path = root / "runtime/state/events.jsonl"
    if not path.exists():
        return ([], False)
    lines = path.read_bytes().splitlines(keepends=True)
    events: list[dict[str, Any]] = []
    torn_tail = False
    for index, raw_line in enumerate(lines):
        stripped = raw_line.rstrip(b"\r\n")
        if not stripped.strip():
            continue
        try:
            events.append(json.loads(stripped.decode("utf-8-sig")))
        except (UnicodeDecodeError, json.JSONDecodeError):
            if index == len(lines) - 1 and not raw_line.endswith((b"\n", b"\r")):
                torn_tail = True
                break
            raise
    return (events, torn_tail)


def event_log_head(root: Path) -> tuple[int, str, bool]:
    events, torn_tail = _events(root)
    if not events:
        return (0, hashlib.sha256(b"").hexdigest(), torn_tail)
    complete_lines = [line.rstrip(b"\r\n") for line in (root / "runtime/state/events.jsonl").read_bytes().splitlines(keepends=True)]
    valid_lines = complete_lines[:-1] if torn_tail else complete_lines
    last = next(line for line in reversed(valid_lines) if line.strip())
    return (int(events[-1]["seq"]), hashlib.sha256(last).hexdigest(), torn_tail)


def event_managed_paths_after(root: Path, after_seq: int) -> list[str]:
    events, _ = _events(root)
    paths = {
        "runtime/state/events.jsonl",
        "runtime/state/snapshot.json",
        "Area_comun/state/CLAIMS.json",
        "Area_comun/state/CLAIMS.slim.json",
        "Area_comun/state/PROJECT_STATE.json",
        "Area_comun/state/PROJECT_STATE.slim.json",
        "Area_comun/state/TASK_INDEX.json",
        "Area_comun/state/TASK_INDEX.slim.json",
    }
    task_files: dict[str, str] = {}
    task_index = root / "Area_comun/state/TASK_INDEX.json"
    if task_index.exists():
        payload = json.loads(task_index.read_text(encoding="utf-8-sig"))
        task_files = {row["id"]: row["file"] for row in payload.get("tasks", []) if row.get("id") and row.get("file")}
    for event in events:
        if int(event.get("seq", 0)) <= after_seq:
            continue
        payload = event.get("payload", {})
        task_id = payload.get("task_id")
        if task_id in task_files:
            paths.add(task_files[task_id])
        archive = payload.get("transitions", {}).get("mailbox_archive", {})
        message_id = archive.get("message_id") or payload.get("message_id")
        if message_id:
            paths.add(f"Area_comun/mailbox/open/{message_id}.md")
            paths.add(f"Area_comun/mailbox/archived/{message_id}.md")
    return sorted(paths)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--paths-after", type=int)
    args = parser.parse_args()
    root = Path(args.root).resolve()
    if args.paths_after is not None:
        print(json.dumps(event_managed_paths_after(root, args.paths_after), sort_keys=True))
        return 0
    seq, digest, torn_tail = event_log_head(root)
    print(json.dumps({"seq": seq, "hash": digest, "torn_tail": torn_tail}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
