#!/usr/bin/env python3
"""Host-local periodic entrypoint for scratch-discipline anomaly delivery."""

from __future__ import annotations

from pathlib import Path
import subprocess
import sys


ROOT = Path(__file__).resolve().parents[1]
SCANNER = ROOT / "scripts" / "scan_scratch_discipline.py"


def main(argv: list[str] | None = None) -> int:
    scanner_args = list(sys.argv[1:] if argv is None else argv)
    if scanner_args[:1] == ["--"]:
        scanner_args = scanner_args[1:]
    result = subprocess.run(
        [sys.executable, str(SCANNER), *scanner_args, "--check"],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        check=False,
    )
    if result.stdout:
        print(result.stdout, end="")
    if result.stderr:
        print(result.stderr, end="", file=sys.stderr)
    if result.returncode == 1:
        print(
            "ACTION REQUIRED: deliver these host-local findings to the responsible "
            "owner as a DECISION-0018 anomaly.",
            file=sys.stderr,
        )
    return result.returncode


if __name__ == "__main__":
    raise SystemExit(main())
