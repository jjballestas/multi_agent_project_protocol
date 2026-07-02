#!/usr/bin/env python3
"""Regression tests for commit trailer validation."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

from validate_collaboration_state import Validation, validate_commit_trailers


def run(args: list[str], cwd: Path) -> str:
    completed = subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return completed.stdout


def commit(repo: Path, subject: str, body: str = "") -> str:
    message = subject if not body else f"{subject}\n\n{body}"
    run(["git", "add", "."], repo)
    run(["git", "commit", "-m", message], repo)
    return run(["git", "rev-parse", "HEAD"], repo).strip()


def write(repo: Path, relpath: str, text: str) -> None:
    path = repo / relpath
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def make_repo() -> tuple[Path, str]:
    root = Path(tempfile.mkdtemp(prefix="trailer-cases-"))
    run(["git", "init"], root)
    run(["git", "config", "user.email", "actor@example.invalid"], root)
    run(["git", "config", "user.name", "Trailer Test"], root)
    write(root, "README.md", "fixture\n")
    base = commit(root, "chore: base")
    return root, base


def validate(repo: Path, start_commit: str) -> list[str]:
    result = Validation()
    index = {"tasks": [{"id": "TASK-0240"}, {"id": "TASK-0241"}]}
    config = {"commit_trailers": {"enabled": True, "start_commit": start_commit}}
    validate_commit_trailers(repo, index, config, result)
    return result.errors


def case(name: str, build, expect_error: str | None) -> None:
    repo, start_commit = make_repo()
    try:
        build(repo)
        errors = validate(repo, start_commit)
        if expect_error is None:
            assert not errors, f"{name}: expected pass, got {errors}"
        else:
            assert any(expect_error in error for error in errors), f"{name}: expected {expect_error!r}, got {errors}"
    finally:
        shutil.rmtree(repo, ignore_errors=True)


def main() -> int:
    case(
        "N1 governed commit without Task-Id",
        lambda repo: (write(repo, "scripts/tool.py", "print('x')\n"), commit(repo, "feat: governed"))[-1],
        "without exact Task-Id",
    )
    case(
        "N2 fix without Fixes-Task",
        lambda repo: (write(repo, "runtime/x.py", "x=1\n"), commit(repo, "fix: runtime", "Task-Id: TASK-0240"))[-1],
        "without exact Fixes-Task",
    )
    case(
        "N3 Fixes-Task unknown",
        lambda repo: (
            write(repo, "scripts/tool.py", "print('x')\n"),
            commit(repo, "fix: governed", "Task-Id: TASK-0240\nFixes-Task: TASK-9999"),
        )[-1],
        "unknown Fixes-Task TASK-9999",
    )
    case(
        "N4 none without Ops-Reason",
        lambda repo: (write(repo, "Area_comun/x.md", "x\n"), commit(repo, "chore: ops", "Task-Id: none"))[-1],
        "without Ops-Reason",
    )
    case(
        "N5 Task-Id outside final trailer block",
        lambda repo: (
            write(repo, "scripts/tool.py", "print('x')\n"),
            commit(repo, "feat: governed", "Task-Id: TASK-0240\n\nextra paragraph after trailer-looking line"),
        )[-1],
        "without exact Task-Id",
    )
    case(
        "P1 governed commit with Task-Id",
        lambda repo: (write(repo, "scripts/tool.py", "print('x')\n"), commit(repo, "feat: governed", "Task-Id: TASK-0240"))[-1],
        None,
    )
    case(
        "P2 fix with both trailers",
        lambda repo: (
            write(repo, "runtime/x.py", "x=1\n"),
            commit(repo, "fix: runtime", "Task-Id: TASK-0240\nFixes-Task: TASK-0241"),
        )[-1],
        None,
    )
    repo, start_commit = make_repo()
    try:
        write(repo, "scripts/pre.py", "print('pre')\n")
        start_commit = commit(repo, "feat: pre-start")
        write(repo, "scripts/post.py", "print('post')\n")
        commit(repo, "feat: post-start", "Task-Id: TASK-0240")
        errors = validate(repo, start_commit)
        assert not errors, f"P3 pre-start commit exempt: expected pass, got {errors}"
    finally:
        shutil.rmtree(repo, ignore_errors=True)
    case(
        "P4 personal path exempt",
        lambda repo: (write(repo, "personal/worker/note.md", "x\n"), commit(repo, "feat: personal"))[-1],
        None,
    )
    print("OK: trailer validation tests passed (9 cases).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
