#!/usr/bin/env python3
"""Runtime gate wrapper around existing project validators."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path
from typing import Any


def run_command(command: list[str], cwd: Path) -> dict[str, Any]:
    completed = subprocess.run(command, cwd=cwd, text=True, capture_output=True)
    return {
        "command": command,
        "returncode": completed.returncode,
        "stdout": completed.stdout,
        "stderr": completed.stderr,
    }


def run_gate(root: Path, tools_root: Path | None = None) -> dict[str, Any]:
    root = root.resolve()
    tools_root = (tools_root or Path(__file__).resolve().parents[1]).resolve()
    checks = [
        run_command([sys.executable, str(tools_root / "scripts" / "validate_collaboration_state.py"), "--root", str(root)], tools_root),
        run_command([sys.executable, str(tools_root / "scripts" / "scan_domain_neutrality.py"), "--root", str(root)], tools_root),
    ]
    return {
        "green": all(check["returncode"] == 0 for check in checks),
        "checks": checks,
    }
