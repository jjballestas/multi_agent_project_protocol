#!/usr/bin/env python3
"""Permanent regression checks for the staged-snapshot pre-commit guard."""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run(args: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, text=True, capture_output=True, check=False)


def require(result: subprocess.CompletedProcess[str], expected: int, label: str) -> None:
    if result.returncode != expected:
        raise AssertionError(
            f"{label}: expected exit {expected}, got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )


def require_rejected(result: subprocess.CompletedProcess[str], label: str) -> None:
    if result.returncode == 0:
        raise AssertionError(
            f"{label}: expected a non-zero exit\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )


def main() -> int:
    source = Path(__file__).resolve().parents[1]
    with tempfile.TemporaryDirectory(prefix="protocol-precommit-") as tmp:
        root = Path(tmp) / "repo"
        (root / ".githooks").mkdir(parents=True)
        (root / "scripts").mkdir()
        (root / "runtime").mkdir()
        (root / "Area_comun" / "state").mkdir(parents=True)
        shutil.copy2(source / ".githooks" / "pre-commit", root / ".githooks" / "pre-commit")
        (root / "scripts" / "prune_state.py").write_text("raise SystemExit(0)\n", encoding="utf-8")
        (root / "scripts" / "validate_collaboration_state.py").write_text("raise SystemExit(1)\n", encoding="utf-8")
        (root / "scripts" / "generate_human_guide.py").write_text("raise SystemExit(0)\n", encoding="utf-8")
        (root / "runtime" / "protocol_replay.py").write_text("# judgment dependency\n", encoding="utf-8")
        state = root / "Area_comun" / "state" / "TASK_INDEX.json"
        state.write_text("{}\n", encoding="utf-8")
        require(run(["git", "init", "-q"], root), 0, "git init")
        require(run(["git", "config", "user.email", "hook@example.invalid"], root), 0, "git email")
        require(run(["git", "config", "user.name", "Hook Test"], root), 0, "git name")
        require(run(["git", "add", "."], root), 0, "initial add")
        require(run(["git", "commit", "--no-verify", "-qm", "fixture"], root), 0, "fixture commit")

        state.write_text('{"broken": true}\n', encoding="utf-8")
        require(run(["git", "add", str(state.relative_to(root))], root), 0, "stage governed state")
        negative = run(["sh", ".githooks/pre-commit"], root)
        if negative.returncode == 0 or "collaboration state in staged snapshot is invalid" not in negative.stderr:
            raise AssertionError(
                "invalid staged collaboration state was not rejected\n"
                f"stdout:\n{negative.stdout}\nstderr:\n{negative.stderr}"
            )

        validator = root / "scripts" / "validate_collaboration_state.py"
        validator.write_text("raise SystemExit(0)\n", encoding="utf-8")
        bypass = run(["sh", ".githooks/pre-commit"], root)
        if bypass.returncode == 0 or "validation-code routes" not in bypass.stderr:
            raise AssertionError(
                "unstaged validator bypass was not rejected\n"
                f"stdout:\n{bypass.stdout}\nstderr:\n{bypass.stderr}"
            )

        require(run(["git", "restore", "scripts/validate_collaboration_state.py"], root), 0, "restore validator")
        require(run(["git", "restore", "--staged", str(state.relative_to(root))], root), 0, "unstage state")
        require(run(["git", "restore", str(state.relative_to(root))], root), 0, "restore state")
        require(run(["sh", ".githooks/pre-commit"], root), 0, "bounded unrelated snapshot")

        deletion_routes = (
            "scripts/validate_collaboration_state.py",
            "runtime/protocol_replay.py",
            "Area_comun/state/TASK_INDEX.json",
            ".githooks/pre-commit",
        )
        for route in deletion_routes:
            require(run(["git", "rm", "--", route], root), 0, f"stage deletion {route}")
            deletion = run(["sh", ".githooks/pre-commit"], root)
            require_rejected(deletion, f"staged deletion {route}")
            require(run(["git", "restore", "--staged", "--", route], root), 0, f"unstage deletion {route}")
            require(run(["git", "restore", "--", route], root), 0, f"restore deletion {route}")
    print("OK: pre-commit staged-snapshot bypass regression and bounded mode.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
