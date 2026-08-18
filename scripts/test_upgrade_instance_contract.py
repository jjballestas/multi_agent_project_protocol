#!/usr/bin/env python3
"""Executable TASK-0394 contract for upgrade reporting and instancing parity."""
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRATCH = Path("D:/Aegis_Scratch/multi_agent_project_protocol/task0394-contract")


def run_upgrade(master: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(master / "scripts/upgrade_instance.py"),
            "--master",
            str(master),
            "--instance",
            str(ROOT / "examples/minimal_instance"),
        ],
        text=True,
        capture_output=True,
        check=False,
    )


def run_upgrade_ps(master: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            "pwsh",
            "-NoProfile",
            "-File",
            str(master / "scripts/upgrade_instance.ps1"),
            "-Master",
            str(master),
            "-Instance",
            str(ROOT / "examples/minimal_instance"),
            "-Report",
            str(SCRATCH.parent / "task0394-ps-report.md"),
        ],
        text=True,
        capture_output=True,
        check=False,
    )


def run_default_instance(master: Path, target: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(master / "scripts/new_instance.py"),
            "--source-template",
            str(master),
            "--target",
            str(target),
            "--project-name",
            "task0394-contract",
            "--project-goal",
            "Exercise default-tier scaffold delivery.",
            "--project-description",
            "Disposable neutral contract fixture.",
            "--architect",
            "Architect",
            "--implementer",
            "Maker",
            "--analyst",
            "Checker",
            "--human-owner",
            "Owner",
            "--phase-id",
            "P0",
            "--phase-name",
            "Contract",
            "--phase-goal",
            "Verify scaffold co-delivery.",
            "--scratch-root",
            str(SCRATCH.parent / "task0394-instance-scratch"),
        ],
        text=True,
        capture_output=True,
        check=False,
    )


def main() -> int:
    if SCRATCH.exists():
        shutil.rmtree(SCRATCH)
    SCRATCH.parent.mkdir(parents=True, exist_ok=True)
    shutil.copytree(ROOT, SCRATCH, ignore=shutil.ignore_patterns(".git", ".protocol-tmp", "personal"))
    try:
        baseline = run_upgrade(SCRATCH)
        assert baseline.returncode == 0, baseline.stderr
        baseline_ps = run_upgrade_ps(SCRATCH)
        assert baseline_ps.returncode == 0, baseline_ps.stderr

        seeded = SCRATCH / "tools/gatekeeper"
        seeded.parent.mkdir(parents=True)
        seeded.write_text("# generic reusable tool\n", encoding="utf-8")
        negative = run_upgrade(SCRATCH)
        assert negative.returncode == 1, negative.stdout + negative.stderr
        assert "tools/gatekeeper" in negative.stderr
        negative_ps = run_upgrade_ps(SCRATCH)
        assert negative_ps.returncode == 1, negative_ps.stdout + negative_ps.stderr
        assert "tools/gatekeeper" in negative_ps.stderr
        seeded.unlink()

        upgrade_py = SCRATCH / "scripts/upgrade_instance.py"
        py_text = upgrade_py.read_text(encoding="utf-8")
        py_mutant = py_text.replace('    ".githooks",\n', "", 1)
        assert py_mutant != py_text
        upgrade_py.write_text(py_mutant, encoding="utf-8")
        missing_hooks = run_upgrade(SCRATCH)
        assert missing_hooks.returncode == 1, missing_hooks.stdout + missing_hooks.stderr
        assert ".githooks/pre-commit" in missing_hooks.stderr

        upgrade_ps = SCRATCH / "scripts/upgrade_instance.ps1"
        ps_text = upgrade_ps.read_text(encoding="utf-8")
        ps_mutant = ps_text.replace(
            '$AdoptableRecursiveRoots = @("scripts", "skills", ".githooks", "runtime")',
            '$AdoptableRecursiveRoots = @("scripts", "skills", "runtime")',
            1,
        )
        assert ps_mutant != ps_text
        upgrade_ps.write_text(ps_mutant, encoding="utf-8")
        missing_hooks_ps = run_upgrade_ps(SCRATCH)
        assert missing_hooks_ps.returncode == 1, missing_hooks_ps.stdout + missing_hooks_ps.stderr
        assert ".githooks/pre-commit" in missing_hooks_ps.stderr

        generated = SCRATCH.parent / "task0394-generated"
        if generated.exists():
            shutil.rmtree(generated)
        scaffold = run_default_instance(SCRATCH, generated)
        assert scaffold.returncode == 0, scaffold.stdout + scaffold.stderr
        guide = generated / "skills/session-watchdogs.skill.md"
        proof = generated / "scripts/harness/test_session_watchdog_filter.py"
        assert guide.is_file(), guide
        assert proof.is_file(), proof
        return 0
    finally:
        if SCRATCH.exists():
            shutil.rmtree(SCRATCH)
        generated = SCRATCH.parent / "task0394-generated"
        if generated.exists():
            shutil.rmtree(generated)


if __name__ == "__main__":
    raise SystemExit(main())
