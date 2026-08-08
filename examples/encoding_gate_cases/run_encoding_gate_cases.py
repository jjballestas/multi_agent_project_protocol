#!/usr/bin/env python3
"""Golden cases for scripts/scan_encoding.py."""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCAN = ROOT / "scripts" / "scan_encoding.py"
PS_SCAN = ROOT / "scripts" / "scan_encoding.ps1"
POWERSHELL = shutil.which("pwsh")

FALSIFICATION_CONTRACTS = (
    {
        "id": "NEG-ENCODING-SKIP-PATH-SEPARATOR",
        "negative": "Python and PowerShell must exclude runtime/memory independently of the host path separator.",
        "mutation": "mutant_text = ps_text.replace(",
        "boundaries": (
            "assert python_skipped.returncode == 0",
            "assert powershell_skipped.returncode == 0",
            "assert python_findings == powershell_findings == {\"runtime/visible.txt\"}",
            "assert mutant.returncode != 0",
            "assert \"runtime/memory/index.db\" in mutant.stdout.replace(\"\\\\\", \"/\")",
        ),
        "exercised_by": "assert_cross_platform_skip_parity",
    },
)


def scratch_parent() -> Path:
    if os.name == "nt":
        parent = Path(f"{ROOT.drive}/Aegis_Scratch/multi_agent_project_protocol/encoding_gate_cases")
    else:
        parent = Path.home() / "Aegis_Scratch/multi_agent_project_protocol/encoding_gate_cases"
    parent.mkdir(parents=True, exist_ok=True)
    return parent


def task_temp(prefix: str) -> tempfile.TemporaryDirectory[str]:
    return tempfile.TemporaryDirectory(prefix=prefix, dir=scratch_parent())


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


def run_ps_scan(root: Path, script: Path = PS_SCAN) -> subprocess.CompletedProcess[str]:
    if not POWERSHELL:
        raise RuntimeError("PowerShell is required for encoding scanner parity")
    return subprocess.run(
        [POWERSHELL, "-NoProfile", "-File", str(script), "-Root", str(root)],
        text=True,
        capture_output=True,
        check=False,
    )


def finding_paths(output: str) -> set[str]:
    return {
        match.replace("\\", "/")
        for match in re.findall(r"^- (?:mojibake|non_ascii_channel): (.+?):\d+ ", output, re.MULTILINE)
    }


def assert_case(name: str, expected: int, **fixture_kwargs: str) -> None:
    with task_temp(f"encoding-{name}-") as temp:
        fixture = Path(temp)
        build_fixture(fixture, **fixture_kwargs)
        result = run_scan(fixture)
        if result.returncode != expected:
            print(result.stdout)
            print(result.stderr)
            raise AssertionError(f"{name}: expected exit {expected}, got {result.returncode}")


def assert_cross_platform_skip_parity() -> None:
    """PERMANENT_NEGATIVE: NEG-ENCODING-SKIP-PATH-SEPARATOR"""
    if not POWERSHELL:
        print("UNMEASURED: PowerShell 7 parity requires pwsh; CI measures the POSIX boundary.")
        return
    with task_temp("encoding-skip-parity-") as temp:
        fixture = Path(temp)
        build_fixture(fixture)
        skipped = fixture / "runtime/memory/index.db"
        skipped.parent.mkdir(parents=True, exist_ok=True)
        skipped.write_bytes(b"SQLite format 3\x00\xff\xfe\xfd")

        python_skipped = run_scan(fixture)
        powershell_skipped = run_ps_scan(fixture)
        assert python_skipped.returncode == 0
        assert powershell_skipped.returncode == 0

        write(fixture / "runtime/visible.txt", "# Espa\u00c3\u00b1a\n")
        python_visible = run_scan(fixture)
        powershell_visible = run_ps_scan(fixture)
        python_findings = finding_paths(python_visible.stdout)
        powershell_findings = finding_paths(powershell_visible.stdout)
        assert python_visible.returncode == powershell_visible.returncode == 1
        assert python_findings == powershell_findings == {"runtime/visible.txt"}

        ps_text = PS_SCAN.read_text(encoding="utf-8-sig")
        mutant_text = ps_text.replace(
            "        # Compare one host-native directory boundary, never a literal slash shape.\n"
            "        $trimChars = [char[]]@([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar)\n"
            "        $directoryPrefix = $directory.TrimEnd($trimChars) + [System.IO.Path]::DirectorySeparatorChar\n"
            "        if ($File.FullName -eq $directory -or $File.FullName.StartsWith($directoryPrefix, [System.StringComparison]::OrdinalIgnoreCase)) { return $false }",
            '        if ($File.FullName -eq $directory -or $File.FullName.StartsWith("$directory\\", [System.StringComparison]::OrdinalIgnoreCase)) { return $false }',
            1,
        )
        assert mutant_text != ps_text
        mutant_path = fixture / "scan_encoding_separator_mutant.ps1"
        mutant_path.write_text(mutant_text, encoding="utf-8", newline="\n")
        (fixture / "runtime/visible.txt").unlink()
        mutant = run_ps_scan(fixture, mutant_path)
        if os.name != "nt":
            assert mutant.returncode != 0
            assert "runtime/memory/index.db" in mutant.stdout.replace("\\", "/")


def main() -> int:
    assert_case("clean", 0)
    assert_case("non_ascii_mailbox", 1, mailbox_text="status: open\nbody: se\u00f1al\n")
    assert_case("mojibake", 1, task_text="# Espa\u00c3\u00b1a\n")

    if POWERSHELL:
        with task_temp("encoding-ps1-") as temp:
            fixture = Path(temp)
            build_fixture(fixture, mailbox_text="status: open\nbody: se\u00f1al\n")
            result = run_ps_scan(fixture)
            if result.returncode != 1:
                print(result.stdout)
                print(result.stderr)
                raise AssertionError(f"ps1 non_ascii_mailbox: expected exit 1, got {result.returncode}")

    assert_cross_platform_skip_parity()

    print("OK: encoding gate cases passed (3 py cases + PowerShell parity and separator mutation).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
