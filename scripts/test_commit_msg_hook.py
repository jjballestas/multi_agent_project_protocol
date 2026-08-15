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
    (state / "TASK_INDEX.json").write_text('{"tasks":[{"id":"TASK-0278"},{"id":"TASK-0279"}]}\n', encoding="utf-8")
    (state / "TASK_INDEX_ARCHIVE.json").write_text('{"tasks":[{"id":"TASK-0200"}]}\n', encoding="utf-8")
    (state / "CLAIMS.json").write_text(
        '{"claims":[{"claim_id":"C1","task_id":"TASK-0279","owner":"Gate Test","status":"active","scope":["scripts/work.py","scripts/check_commit_trailers.py",".githooks/commit-msg"]},'
        '{"claim_id":"C2","task_id":"TASK-0200","owner":"Gate Test","status":"active","scope":["scripts/work.py","scripts/check_commit_trailers.py",".githooks/commit-msg"]}]}\n', encoding="utf-8"
    )
    return root


def attempt(repo: Path, subject: str, trailers: str, accepted: bool) -> subprocess.CompletedProcess[str]:
    target = repo / "scripts/work.py"
    target.write_text(target.read_text(encoding="utf-8") + "x=1\n" if target.exists() else "x=1\n", encoding="utf-8")
    run(["git", "add", "."], repo, True)
    before = run(["git", "rev-list", "--count", "HEAD"], repo, True).stdout.strip() if (repo / ".git/refs/heads/master").exists() else "0"
    result = run(["git", "commit", "-m", subject, "-m", trailers], repo, accepted)
    if not accepted:
        after = run(["git", "rev-list", "--count", "HEAD"], repo, True).stdout.strip() if before != "0" else "0"
        assert after == before and "commit trailer gate:" in result.stderr
        if "claim" in result.stderr:
            print(f"COMMIT_MSG_REJECTION exit={result.returncode}: {result.stderr.strip().splitlines()[0]}")
    return result


def main() -> int:
    cases = [
        ("valid", "feat: valid", "Task-Id: TASK-0279", True),
        ("archived", "feat: archived", "Task-Id: TASK-0200", True),
        ("blank-line mutation", "feat: blank", "Task-Id: TASK-0279\n\nCo-Authored-By: Gate <gate@example.invalid>", False),
        ("long Ops-Reason mutation", "chore: ops", "Task-Id: none\nOps-Reason: " + "x" * 121, False),
        ("missing Task-Id mutation", "feat: missing", "Ops-Reason: bounded", False),
        ("fix without Fixes-Task mutation", "fix: broken", "Task-Id: TASK-0279", False),
        ("unknown task mutation", "feat: unknown", "Task-Id: TASK-9999", False),
        ("missing claim rejection", "feat: unclaimed", "Task-Id: TASK-0278", False),
        ("coordination exemption", "chore: coordinate", "Task-Id: none\nOps-Reason: bounded coordination", True),
    ]
    for name, subject, trailers, accepted in cases:
        repo = fixture()
        try:
            attempt(repo, subject, trailers, accepted)
        finally:
            shutil.rmtree(repo, ignore_errors=True)
    repo = fixture()
    try:
        claims = repo / "Area_comun/state/CLAIMS.json"
        claims.write_text(
            '{"claims":[{"claim_id":"C1","task_id":"TASK-0279","owner":"Other","status":"active","scope":["scripts/work.py","scripts/check_commit_trailers.py",".githooks/commit-msg"]}]}\n',
            encoding="utf-8",
        )
        result = attempt(repo, "feat: other actor", "Task-Id: TASK-0279", False)
        assert "owned by another actor" in result.stderr
    finally:
        shutil.rmtree(repo, ignore_errors=True)

    repo = fixture()
    try:
        nested = repo / "Aegis"
        nested.mkdir()
        for name in ("scripts", ".githooks", "Area_comun"):
            shutil.move(str(repo / name), str(nested / name))
        run(["git", "config", "core.hooksPath", "Aegis/.githooks"], repo, True)
        run(["git", "add", "Aegis"], repo, True)
        run(["git", "commit", "--no-verify", "-qm", "fixture"], repo, True)
        target = nested / "scripts/work.py"
        target.write_text("x=1\n", encoding="utf-8")
        run(["git", "add", "Aegis/scripts/work.py"], repo, True)
        message = repo / "message.txt"
        message.write_text("feat: prefixed\n\nTask-Id: TASK-0279\n", encoding="utf-8")
        verdict = run(["python", "Aegis/scripts/check_commit_trailers.py", str(message)], repo, True)
        assert verdict.returncode == 0
        hook_verdict = run(["sh", "Aegis/.githooks/commit-msg", str(message)], repo, True)
        assert hook_verdict.returncode == 0
    finally:
        shutil.rmtree(repo, ignore_errors=True)
    print(f"OK: commit-msg trailer gate passed {len(cases) + 2} cases including empty/non-empty instance prefixes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
