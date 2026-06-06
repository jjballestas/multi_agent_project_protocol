#!/usr/bin/env python3
"""Golden cases for scripts/scan_encoding.py."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCAN = ROOT / "scripts" / "scan_encoding.py"


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_fixture(root: Path, *, mailbox_text: str = "status: open\n", task_text: str = "# Clean\n") -> None:
    write(root / "Area_comun" / "mailbox" / "open" / "MSG-clean.md", mailbox_text)
    write(root / "Area_comun" / "mailbox" / "answered" / ".gitkeep", "\n")
    write(root / "Area_comun" / "mailbox" / "archived" / ".gitkeep", "\n")
    write(root / "Area_comun" / "state" / "PROJECT_STATE.json", '{"project":"fixture"}\n')
    write(root / "Area_comun" / "tasks" / "TASK-clean.md", task_text)


def run_scan(root: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python", str(SCAN), "--root", str(root)],
        text=True,
        capture_output=True,
        check=False,
    )


def assert_case(name: str, expected: int, **fixture_kwargs: str) -> None:
    with tempfile.TemporaryDirectory(prefix=f"encoding-{name}-") as temp:
        fixture = Path(temp)
        build_fixture(fixture, **fixture_kwargs)
        result = run_scan(fixture)
        if result.returncode != expected:
            print(result.stdout)
            print(result.stderr)
            raise AssertionError(f"{name}: expected exit {expected}, got {result.returncode}")


def main() -> int:
    assert_case("clean", 0)
    assert_case("non_ascii_mailbox", 1, mailbox_text="status: open\nbody: se\u00f1al\n")
    assert_case("mojibake", 1, task_text="# Espa\u00c3\u00b1a\n")

    ps1 = ROOT / "scripts" / "scan_encoding.ps1"
    if shutil.which("pwsh"):
        with tempfile.TemporaryDirectory(prefix="encoding-ps1-") as temp:
            fixture = Path(temp)
            build_fixture(fixture, mailbox_text="status: open\nbody: se\u00f1al\n")
            result = subprocess.run(
                ["pwsh", "-NoProfile", "-File", str(ps1), "-Root", str(fixture)],
                text=True,
                capture_output=True,
                check=False,
            )
            if result.returncode != 1:
                print(result.stdout)
                print(result.stderr)
                raise AssertionError(f"ps1 non_ascii_mailbox: expected exit 1, got {result.returncode}")

    print("OK: encoding gate cases passed (3 py cases + ps1 parity if available).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
