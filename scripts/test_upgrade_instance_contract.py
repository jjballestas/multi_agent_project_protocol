#!/usr/bin/env python3
"""Executable TASK-0394 contract for upgrade reporting and instancing parity."""
from __future__ import annotations

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRATCH = Path("D:/Aegis_Scratch/multi_agent_project_protocol/task0394-contract")


def load_new_instance():
    spec = importlib.util.spec_from_file_location("new_instance", ROOT / "scripts/new_instance.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_upgrade(master: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [
            sys.executable,
            str(ROOT / "scripts/upgrade_instance.py"),
            "--master",
            str(master),
            "--instance",
            str(ROOT / "examples/minimal_instance"),
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

        seeded = SCRATCH / "tools/exportable.py"
        seeded.parent.mkdir(parents=True)
        seeded.write_text("# generic reusable tool\n", encoding="utf-8")
        negative = run_upgrade(SCRATCH)
        assert negative.returncode == 1, negative.stdout + negative.stderr
        assert "tools/exportable.py" in negative.stderr

        module = load_new_instance()
        generated = SCRATCH.parent / "task0394-generated"
        if generated.exists():
            shutil.rmtree(generated)
        generated.mkdir()
        module.copy_peer_harness(ROOT, generated)
        proof = generated / "scripts/harness/test_session_watchdog_filter.py"
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
