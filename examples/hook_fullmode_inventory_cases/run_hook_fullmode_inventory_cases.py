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
        require(
            run(["git", "config", "user.name", "Codex"], nonreviewed_root),
            0,
            "configure synthetic commit actor",
        )
        shutil.copy2(
            source / "scripts" / "check_commit_trailers.py",
            nonreviewed_root / "scripts" / "check_commit_trailers.py",
        )
        task_index = nonreviewed_root / "Area_comun" / "state" / "TASK_INDEX.json"
        task_data = json.loads(task_index.read_text(encoding="utf-8"))
        existing_task_ids = {task["id"] for task in task_data["tasks"]}
        synthetic_task_id = next(
            f"TASK-{number:04d}"
            for number in range(9999, 8999, -1)
            if f"TASK-{number:04d}" not in existing_task_ids
        )
        synthetic_task_file = (
            f"Area_comun/tasks/{synthetic_task_id}-nonreviewed-hook-probe.md"
        )
        task_data["tasks"].append(
            {
                "file": synthetic_task_file,
                "id": synthetic_task_id,
                "owner": "Codex",
                "phase": "P2",
                "priority": "low",
                "status": "ready",
                "title": "Synthetic non-reviewed hook probe",
                "type": "infra",
                "deliverables": ["personal/Codex/absent-nonreviewed-probe.md"],
            }
        )
        task_index.write_text(
            json.dumps(task_data, ensure_ascii=True, indent=4) + "\n",
            encoding="ascii",
        )
        synthetic_task_path = nonreviewed_root / synthetic_task_file
        synthetic_task_path.write_text(
            "---\n"
            f"task_id: {synthetic_task_id}\n"
            "title: Synthetic non-reviewed hook probe\n"
            "type: infra\n"
            "status: ready\n"
            "owner: Codex\n"
            "phase: P2\n"
            "priority: low\n"
            f"file: {synthetic_task_file}\n"
            "intake:\n"
            "  type: infra\n"
            "  goal: Exercise absent non-reviewed deliverable handling.\n"
            "  acceptance:\n"
            "    - The synthetic ready task is accepted without its personal deliverable.\n"
            "  verification_cmd:\n"
            "    - HOOK_FULL=1 sh .githooks/pre-commit\n"
            "  scope_routes:\n"
            "    - examples/\n"
            "  out_of_scope:\n"
            "    - Production task state.\n"
            "  risk: low\n"
            "  estimate: S\n"
            "---\n\n"
            "# Synthetic non-reviewed hook probe\n",
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
        actor = run(
            ["git", "config", "user.name"], nonreviewed_root
        ).stdout.strip()
        claims_path = nonreviewed_root / "Area_comun" / "state" / "CLAIMS.json"
        claims_data = json.loads(claims_path.read_text(encoding="utf-8"))
        claims_data["claims"].append(
            {
                "claim_id": "CLAIM-20990101-HookProbe-PRODUCT",
                "task_id": synthetic_task_id,
                "owner": actor,
                "status": "active",
                "scope": ["protocol.config.json", "scripts/check_commit_trailers.py"],
                "started_at": "2099-01-01T00:00:00Z",
                "updated_at": "2099-01-01T00:00:00Z",
                "expires_at": "2099-01-01T01:00:00Z",
            }
        )
        claims_path.write_text(
            json.dumps(claims_data, ensure_ascii=True, indent=4) + "\n",
            encoding="ascii",
        )
        require(
            run(
                [
                    "git",
                    "add",
                    "Area_comun/state/TASK_INDEX.json",
                    "Area_comun/state/CLAIMS.json",
                    synthetic_task_file,
                    "protocol.config.json",
                    "scripts/check_commit_trailers.py",
                ],
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
