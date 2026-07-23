#!/usr/bin/env python3
"""Exercise TASK-0287 through the real pre-commit hook entrypoint."""

from __future__ import annotations

import json
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

        nonreviewed_root = Path(tmp) / "nonreviewed"
        clone_with_fix(source, nonreviewed_root)
        task_index = nonreviewed_root / "Area_comun" / "state" / "TASK_INDEX.json"
        task_data = json.loads(task_index.read_text(encoding="utf-8"))
        nonreviewed_task = next(task for task in task_data["tasks"] if task["id"] == "TASK-0291")
        if nonreviewed_task["status"] in {
            "in_review",
            "review_approved",
            "qa_pending",
            "architect_review",
            "done",
        }:
            raise AssertionError("non-reviewed probe fixture unexpectedly has a reviewed status")
        nonreviewed_task["deliverables"] = ["personal/Codex/absent-nonreviewed-probe.md"]
        task_index.write_text(
            json.dumps(task_data, ensure_ascii=True, indent=4) + "\n",
            encoding="ascii",
        )
        config_path = nonreviewed_root / "protocol.config.json"
        config_data = json.loads(config_path.read_text(encoding="utf-8"))
        for key in (
            "enabled",
            "materialize",
            "enforce",
            "authoritative",
            "chain_enabled",
            "agent_signatures_enabled",
            "anchor_enabled",
        ):
            config_data["event_state"][key] = False
        config_path.write_text(
            json.dumps(config_data, ensure_ascii=True, indent=2) + "\n",
            encoding="ascii",
        )
        require(
            run(
                ["git", "add", "Area_comun/state/TASK_INDEX.json", "protocol.config.json"],
                nonreviewed_root,
            ),
            0,
            "stage non-reviewed missing deliverable probe",
        )
        require(
            hook(nonreviewed_root),
            0,
            "non-reviewed task with absent personal deliverable",
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
        combined = f"{masking.stdout}\n{masking.stderr}"
        if (
            "deliverable missing" not in combined
            or "collaboration state in staged snapshot is invalid" not in combined
        ):
            raise AssertionError(
                "reviewed-task masking probe was rejected outside the validator boundary\n"
                f"stdout:\n{masking.stdout}\nstderr:\n{masking.stderr}"
            )

    print(
        "OK: real hook accepts the clean full-mode partial snapshot with indexed "
        "deliverables, tolerates absent non-reviewed deliverables, bounds personal "
        "materialization, and rejects broken state plus a reviewed-task masking "
        "probe at the validator boundary."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
