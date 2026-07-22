#!/usr/bin/env python3
"""Bounded commit-msg gate for governed commit trailers."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

GOVERNED = ("Area_comun/", "runtime/", "scripts/", "protocol.config.json")
TRAILER = re.compile(r"^[A-Za-z][A-Za-z0-9-]*: .+$")
TASK = re.compile(r"^Task-Id: (TASK-\d{4}|none)$")
FIXES = re.compile(r"^Fixes-Task: TASK-\d{4}$")
OPS = re.compile(r"^Ops-Reason: .{1,120}$")
FIX_SUBJECT = re.compile(r"^(fix|revert|hotfix)(\(|:|!)")


def load_task_ids(path: Path) -> set[str]:
    if not path.exists():
        return set()
    data = json.loads(path.read_text(encoding="utf-8"))
    return {str(row.get("id")) for row in data.get("tasks", []) if isinstance(row, dict) and row.get("id")}


def final_trailers(message: str) -> dict[str, list[str]]:
    lines = message.rstrip("\n").splitlines()
    start = len(lines) - 1
    while start > 0 and lines[start - 1].strip():
        start -= 1
    block = lines[start:]
    if not block or not all(TRAILER.fullmatch(line) for line in block):
        return {}
    found: dict[str, list[str]] = {}
    for line in block:
        key = line.split(":", 1)[0]
        if key in {"Task-Id", "Fixes-Task", "Ops-Reason"}:
            found.setdefault(key, []).append(line)
    return found


def staged_governed(root: Path) -> bool:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMRTD"],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        check=True,
    )
    return any(path == "protocol.config.json" or path.startswith(GOVERNED[:3]) for path in result.stdout.splitlines())


def validate(root: Path, message: str) -> list[str]:
    if not staged_governed(root):
        return []
    lines = message.rstrip("\n").splitlines()
    subject = lines[0] if lines else ""
    trailers = final_trailers(message)
    task_lines = trailers.get("Task-Id", [])
    if len(task_lines) != 1 or not TASK.fullmatch(task_lines[0]):
        return ["missing exact final trailer; write `Task-Id: TASK-XXXX` or `Task-Id: none` in one final trailer block without blank lines"]
    known = load_task_ids(root / "Area_comun/state/TASK_INDEX.json") | load_task_ids(root / "Area_comun/state/TASK_INDEX_ARCHIVE.json")
    task_id = task_lines[0].split(": ", 1)[1]
    errors: list[str] = []
    if task_id != "none" and task_id not in known:
        errors.append(f"unknown Task-Id {task_id}; use an id from TASK_INDEX or TASK_INDEX_ARCHIVE")
    if task_id == "none":
        ops = trailers.get("Ops-Reason", [])
        if len(ops) != 1 or not OPS.fullmatch(ops[0]):
            errors.append("Task-Id: none requires exactly one `Ops-Reason: <1-120 characters>` in the same final block")
    if FIX_SUBJECT.match(subject):
        fixes = trailers.get("Fixes-Task", [])
        if len(fixes) != 1 or not FIXES.fullmatch(fixes[0]):
            errors.append("fix/revert/hotfix subject requires exactly one `Fixes-Task: TASK-XXXX` in the final block")
        elif fixes[0].split(": ", 1)[1] not in known:
            errors.append(f"unknown {fixes[0]}; use an id from TASK_INDEX or TASK_INDEX_ARCHIVE")
    return errors


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: check_commit_trailers.py <commit-message-file>", file=sys.stderr)
        return 2
    root = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], text=True).strip())
    errors = validate(root, Path(sys.argv[1]).read_text(encoding="utf-8"))
    if errors:
        for error in errors:
            print(f"commit trailer gate: {error}", file=sys.stderr)
        print("Emergency disarm: git config --unset core.hooksPath (rearm: git config core.hooksPath .githooks)", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
