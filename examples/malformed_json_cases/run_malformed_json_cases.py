#!/usr/bin/env python3
"""Exercise graceful malformed-JSON failures through the real entrypoints."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def run(args: list[str], cwd: Path, *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False, env=env)


def require_graceful_failure(result: subprocess.CompletedProcess[str], path: str, label: str) -> None:
    output = result.stdout + result.stderr
    if result.returncode == 0:
        raise AssertionError(f"{label}: expected non-zero exit")
    if path not in output:
        raise AssertionError(f"{label}: output did not name {path}\n{output}")
    if "Traceback (most recent call last)" in output:
        raise AssertionError(f"{label}: leaked a Python traceback\n{output}")


def copy_tracked_tree(destination: Path) -> None:
    cloned = run(["git", "clone", "--quiet", "--no-hardlinks", str(ROOT), str(destination)], ROOT)
    if cloned.returncode != 0:
        raise AssertionError(cloned.stderr)
    for relative in (
        "scripts/validate_collaboration_state.py",
        "scripts/prune_state.py",
        "examples/malformed_json_cases/run_malformed_json_cases.py",
    ):
        source = ROOT / relative
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="protocol-malformed-json-") as tmp:
        fixture = Path(tmp) / "repo"
        copy_tracked_tree(fixture)
        for args, label in (
            (["git", "config", "user.email", "fixture@example.invalid"], "git email"),
            (["git", "config", "user.name", "Fixture"], "git name"),
            (["git", "config", "core.hooksPath", ".githooks"], "hook path"),
            (
                [
                    "git",
                    "add",
                    "scripts/validate_collaboration_state.py",
                    "scripts/prune_state.py",
                    "examples/malformed_json_cases/run_malformed_json_cases.py",
                ],
                "overlay add",
            ),
        ):
            result = run(args, fixture)
            if result.returncode != 0:
                raise AssertionError(f"{label} failed\n{result.stdout}\n{result.stderr}")
        overlay = run(["git", "diff", "--cached", "--quiet"], fixture)
        if overlay.returncode == 1:
            result = run(
                [
                    "git",
                    "commit",
                    "--no-verify",
                    "-qm",
                    "test(TASK-0288): malformed JSON fixture overlay",
                    "-m",
                    "Task-Id: TASK-0288",
                ],
                fixture,
            )
            if result.returncode != 0:
                raise AssertionError(f"overlay commit failed\n{result.stdout}\n{result.stderr}")
        elif overlay.returncode != 0:
            raise AssertionError(f"overlay diff failed\n{overlay.stdout}\n{overlay.stderr}")
        task_index = fixture / "Area_comun/state/TASK_INDEX.json"
        original = task_index.read_text(encoding="utf-8-sig")

        clean = run([sys.executable, "scripts/validate_collaboration_state.py", "--root", "."], fixture)
        if clean.returncode != 0:
            raise AssertionError(f"clean validator failed\n{clean.stdout}\n{clean.stderr}")

        task_index.write_text("{", encoding="utf-8")
        malformed_validate = run(
            [sys.executable, "scripts/validate_collaboration_state.py", "--root", "."], fixture
        )
        require_graceful_failure(
            malformed_validate, "TASK_INDEX.json", "malformed validator"
        )
        malformed_prune = run(
            [sys.executable, "scripts/prune_state.py", "--root", ".", "--check"], fixture
        )
        require_graceful_failure(malformed_prune, "TASK_INDEX.json", "malformed prune")

        task_index.write_text('{"schema_version":"1.0","tasks":[]}\n', encoding="utf-8")
        semantic = run(
            [sys.executable, "scripts/validate_collaboration_state.py", "--root", "."], fixture
        )
        if semantic.returncode == 0:
            raise AssertionError("valid JSON with broken governed semantics was accepted")

        task_index.write_text(original, encoding="utf-8")
        task_index.write_text("{", encoding="utf-8")
        staged = run(["git", "add", "Area_comun/state/TASK_INDEX.json"], fixture)
        if staged.returncode != 0:
            raise AssertionError(staged.stderr)
        env = os.environ.copy()
        env["HOOK_FULL"] = "1"
        hook = run(["sh", ".githooks/pre-commit"], fixture, env=env)
        require_graceful_failure(hook, "TASK_INDEX.json", "full hook malformed state")
        if "collaboration state in staged snapshot is invalid" not in hook.stderr:
            raise AssertionError(f"full hook did not reject at validator boundary\n{hook.stderr}")

    print("OK: clean, malformed validate/prune, semantic rejection, and full-hook C5 cases.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
