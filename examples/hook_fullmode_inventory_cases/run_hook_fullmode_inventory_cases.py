#!/usr/bin/env python3
"""Exercise TASK-0287 through the real pre-commit hook entrypoint."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run(args: list[str], cwd: Path, *, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=cwd, env=env, text=True, capture_output=True, check=False)


def require(result: subprocess.CompletedProcess[str], expected: int, label: str) -> None:
    if result.returncode != expected:
        raise AssertionError(
            f"{label}: expected exit {expected}, got {result.returncode}\n"
            f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}"
        )


def hook(root: Path) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["HOOK_FULL"] = "1"
    env["HOOK_SNAPSHOT_MODE"] = "partial"
    return run(["sh", ".githooks/pre-commit"], root, env=env)


def main() -> int:
    source = Path(__file__).resolve().parents[2]
    with tempfile.TemporaryDirectory(prefix="protocol-hook-fullmode-") as tmp:
        root = Path(tmp) / "repo"
        require(
            run(["git", "clone", "--quiet", "--no-hardlinks", str(source), str(root)], source),
            0,
            "sandbox clone",
        )
        for relative in (".githooks/pre-commit", ".github/workflows/validate.yml"):
            shutil.copy2(source / relative, root / relative)
        require(run(["git", "add", ".githooks/pre-commit", ".github/workflows/validate.yml"], root), 0, "stage fix")

        positive = hook(root)
        require(positive, 0, "clean governed tree in full partial-snapshot mode")

        task_index = root / "Area_comun" / "state" / "TASK_INDEX.json"
        task_index.write_text("{\n", encoding="ascii")
        require(run(["git", "add", "Area_comun/state/TASK_INDEX.json"], root), 0, "stage broken governed state")
        negative = hook(root)
        if negative.returncode == 0:
            raise AssertionError("genuinely broken governed state was accepted")
        combined = f"{negative.stdout}\n{negative.stderr}"
        if "collaboration state in staged snapshot is invalid" not in combined:
            raise AssertionError(
                "broken state was rejected for the wrong reason; validator boundary not evidenced\n"
                f"stdout:\n{negative.stdout}\nstderr:\n{negative.stderr}"
            )

    print(
        "OK: real hook accepts the clean full-mode partial snapshot with indexed "
        "deliverables and rejects genuinely broken staged governed state."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
