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


def hook(root: Path, *, report_inventory: bool = False) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["HOOK_FULL"] = "1"
    env["HOOK_SNAPSHOT_MODE"] = "partial"
    if report_inventory:
        env["HOOK_INVENTORY_REPORT"] = "1"
    return run(["sh", ".githooks/pre-commit"], root, env=env)


def clone_with_fix(source: Path, destination: Path) -> None:
    require(
        run(["git", "clone", "--quiet", "--no-hardlinks", str(source), str(destination)], source),
        0,
        "sandbox clone",
    )
    for relative in (".githooks/pre-commit", ".github/workflows/validate.yml"):
        shutil.copy2(source / relative, destination / relative)
    require(
        run(["git", "add", ".githooks/pre-commit", ".github/workflows/validate.yml"], destination),
        0,
        "stage fix",
    )


def main() -> int:
    source = Path(__file__).resolve().parents[2]
    with tempfile.TemporaryDirectory(prefix="protocol-hook-fullmode-") as tmp:
        root = Path(tmp) / "positive"
        clone_with_fix(source, root)

        positive = hook(root, report_inventory=True)
        require(positive, 0, "clean governed tree in full partial-snapshot mode")
        inventory_line = next(
            (line for line in positive.stdout.splitlines() if line.startswith("bounded personal deliverables: ")),
            "",
        )
        if not inventory_line:
            raise AssertionError(f"bounded inventory measurement missing\nstdout:\n{positive.stdout}")
        selected, tracked = (
            int(value)
            for value in inventory_line.removeprefix("bounded personal deliverables: ")
            .removesuffix(" tracked paths")
            .split(" of ")
        )
        if selected != 1 or tracked <= selected:
            raise AssertionError(
                f"personal inventory was not measurably bounded: selected={selected}, tracked={tracked}"
            )

        broken_root = Path(tmp) / "broken"
        clone_with_fix(source, broken_root)
        task_index = broken_root / "Area_comun" / "state" / "TASK_INDEX.json"
        task_index.write_text("{\n", encoding="ascii")
        require(
            run(["git", "add", "Area_comun/state/TASK_INDEX.json"], broken_root),
            0,
            "stage broken governed state",
        )
        negative = hook(broken_root)
        if negative.returncode == 0:
            raise AssertionError("genuinely broken governed state was accepted")
        combined = f"{negative.stdout}\n{negative.stderr}"
        if "collaboration state in staged snapshot is invalid" not in combined:
            raise AssertionError(
                "broken state was rejected for the wrong reason; validator boundary not evidenced\n"
                f"stdout:\n{negative.stdout}\nstderr:\n{negative.stderr}"
            )

        masking_root = Path(tmp) / "masking"
        clone_with_fix(source, masking_root)
        require(
            run(["git", "rm", "--cached", "personal/Codex/STARTUP_PROMPT.md"], masking_root),
            0,
            "stage indexed personal deliverable deletion",
        )
        masking = hook(masking_root)
        if masking.returncode == 0:
            raise AssertionError("staged deletion of an indexed personal deliverable was accepted")

    print(
        "OK: real hook accepts the clean full-mode partial snapshot with indexed "
        "deliverables, bounds personal materialization, and rejects broken state "
        "plus an indexed-deliverable masking probe."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
