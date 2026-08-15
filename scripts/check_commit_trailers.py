#!/usr/bin/env python3
"""Bounded commit-msg gate for governed commit trailers."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

GOVERNED = ("Area_comun/", "runtime/", "scripts/", ".githooks/", "protocol.config.json")
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


def instance_context() -> tuple[Path, Path, str]:
    instance_root = Path(__file__).resolve().parents[1]
    repo_root = Path(subprocess.check_output(["git", "rev-parse", "--show-toplevel"], cwd=instance_root, text=True).strip())
    relative = instance_root.relative_to(repo_root).as_posix()
    return repo_root, instance_root, f"{relative}/" if relative != "." else ""


def staged_paths(root: Path) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--cached", "--name-only", "--diff-filter=ACMRTD"],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        check=True,
    )
    return result.stdout.splitlines()


def instance_paths(paths: list[str], prefix: str) -> list[str]:
    return [path[len(prefix):] for path in paths if path.startswith(prefix)] if prefix else paths


def staged_product(root: Path, prefix: str) -> bool:
    return bool(staged_product_paths(root, prefix))


def staged_governed(root: Path, prefix: str) -> bool:
    paths = instance_paths(staged_paths(root), prefix)
    return any(path == "protocol.config.json" or path.startswith(GOVERNED[:-1]) for path in paths)


def staged_product_paths(root: Path, prefix: str) -> list[str]:
    paths = instance_paths(staged_paths(root), prefix)
    return [
        path
        for path in paths
        if path == "protocol.config.json"
        or path.startswith(("scripts/", ".githooks/"))
        or (path.startswith("runtime/") and not path.startswith("runtime/state/"))
    ]


def commit_actor(root: Path) -> str:
    return subprocess.check_output(["git", "config", "user.name"], cwd=root, text=True).strip()


def has_active_claim(instance_root: Path, task_id: str | None, actor: str, product_paths: list[str]) -> bool:
    return claim_state(instance_root, task_id, actor, product_paths) == "owned"


def claim_state(instance_root: Path, task_id: str | None, actor: str, product_paths: list[str]) -> str:
    path = instance_root / "Area_comun/state/CLAIMS.json"
    if not path.exists():
        return "missing"
    rows = json.loads(path.read_text(encoding="utf-8")).get("claims", [])
    covered_by_other = False
    for row in rows:
        if not isinstance(row, dict) or row.get("status") != "active":
            continue
        if task_id is not None and row.get("task_id") != task_id:
            continue
        scope = {str(item).split("#", 1)[0] for item in row.get("scope", [])}
        if all(path in scope for path in product_paths):
            if row.get("owner") == actor:
                return "owned"
            covered_by_other = True
    return "other" if covered_by_other else "missing"


def validate(root: Path, instance_root: Path, prefix: str, message: str) -> list[str]:
    if not staged_governed(root, prefix):
        return []
    lines = message.rstrip("\n").splitlines()
    subject = lines[0] if lines else ""
    trailers = final_trailers(message)
    task_lines = trailers.get("Task-Id", [])
    if len(task_lines) != 1 or not TASK.fullmatch(task_lines[0]):
        return ["missing exact final trailer; write `Task-Id: TASK-XXXX` or `Task-Id: none` in one final trailer block without blank lines"]
    known = load_task_ids(instance_root / "Area_comun/state/TASK_INDEX.json") | load_task_ids(instance_root / "Area_comun/state/TASK_INDEX_ARCHIVE.json")
    task_id = task_lines[0].split(": ", 1)[1]
    errors: list[str] = []
    if task_id != "none" and task_id not in known:
        errors.append(f"unknown Task-Id {task_id}; use an id from TASK_INDEX or TASK_INDEX_ARCHIVE")
    if task_id != "none" and task_id in known and staged_product(root, prefix):
        actor = commit_actor(root)
        state = claim_state(instance_root, task_id, actor, staged_product_paths(root, prefix))
        if state == "other":
            errors.append(f"product commit rejected: Task-Id {task_id} is covered by an active claim owned by another actor, not commit actor {actor}")
        elif state == "missing":
            errors.append(f"product commit rejected: Task-Id {task_id} has no active claim covering every staged product path for commit actor {actor}")
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
    if len(sys.argv) not in (2, 3):
        print("usage: check_commit_trailers.py <commit-message-file> | --pre-commit", file=sys.stderr)
        return 2
    root, instance_root, prefix = instance_context()
    if sys.argv[1] == "--pre-commit":
        if not staged_product(root, prefix):
            return 0
        actor = commit_actor(root)
        state = claim_state(instance_root, None, actor, staged_product_paths(root, prefix))
        if state == "owned":
            return 0
        cause = "active claim is owned by another actor" if state == "other" else "no active claim covers every staged product path"
        print(f"pre-commit claim gate: product commit rejected: {cause} for commit actor {actor}", file=sys.stderr)
        return 1
    errors = validate(root, instance_root, prefix, Path(sys.argv[1]).read_text(encoding="utf-8"))
    if errors:
        for error in errors:
            print(f"commit trailer gate: {error}", file=sys.stderr)
        print("Emergency disarm: git config --unset core.hooksPath (rearm: git config core.hooksPath .githooks)", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
