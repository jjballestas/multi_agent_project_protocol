#!/usr/bin/env python3
"""Real-commit regression and mutation controls for the commit-msg trailer gate."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(args: list[str], cwd: Path, ok: bool) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    assert (result.returncode == 0) is ok, (args, result.returncode, result.stdout, result.stderr)
    return result


def fixture() -> Path:
    root = Path(tempfile.mkdtemp(prefix="commit-msg-gate-"))
    run(["git", "init"], root, True)
    run(["git", "config", "user.name", "Gate Test"], root, True)
    run(["git", "config", "user.email", "gate@example.invalid"], root, True)
    run(["git", "config", "core.hooksPath", ".githooks"], root, True)
    for rel in ("scripts/check_commit_trailers.py", ".githooks/commit-msg"):
        target = root / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / rel, target)
    state = root / "Area_comun/state"
    state.mkdir(parents=True)
    (state / "TASK_INDEX.json").write_text('{"tasks":[{"id":"TASK-0279"}]}\n', encoding="utf-8")
    (state / "TASK_INDEX_ARCHIVE.json").write_text('{"tasks":[{"id":"TASK-0200"}]}\n', encoding="utf-8")
    return root


def attempt(repo: Path, subject: str, trailers: str, accepted: bool) -> None:
    target = repo / "scripts/work.py"
    target.write_text(target.read_text(encoding="utf-8") + "x=1\n" if target.exists() else "x=1\n", encoding="utf-8")
    run(["git", "add", "."], repo, True)
    before = run(["git", "rev-list", "--count", "HEAD"], repo, True).stdout.strip() if (repo / ".git/refs/heads/master").exists() else "0"
    result = run(["git", "commit", "-m", subject, "-m", trailers], repo, accepted)
    if not accepted:
        after = run(["git", "rev-list", "--count", "HEAD"], repo, True).stdout.strip() if before != "0" else "0"
        assert after == before and "commit trailer gate:" in result.stderr


def main() -> int:
    cases = [
        ("valid", "feat: valid", "Task-Id: TASK-0279", True),
        ("archived", "feat: archived", "Task-Id: TASK-0200", True),
        ("blank-line mutation", "feat: blank", "Task-Id: TASK-0279\n\nCo-Authored-By: Gate <gate@example.invalid>", False),
        ("long Ops-Reason mutation", "chore: ops", "Task-Id: none\nOps-Reason: " + "x" * 121, False),
        ("missing Task-Id mutation", "feat: missing", "Ops-Reason: bounded", False),
        ("fix without Fixes-Task mutation", "fix: broken", "Task-Id: TASK-0279", False),
        ("unknown task mutation", "feat: unknown", "Task-Id: TASK-9999", False),
    ]
    for name, subject, trailers, accepted in cases:
        repo = fixture()
        try:
            attempt(repo, subject, trailers, accepted)
        finally:
            shutil.rmtree(repo, ignore_errors=True)
    print(f"OK: commit-msg trailer gate passed {len(cases)} real-commit cases with explicit mutation controls.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
