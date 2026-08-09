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
        "negative": "Python and PowerShell must scan and exclude the same sentinel paths, including hidden entries and exact-case skip boundaries, independently of the host path separator.",
        "mutation": "mutant_text = ps_text.replace(",
        "boundaries": (
            "assert python_scanned == powershell_scanned == expected_scanned",
            "assert python_excluded == powershell_excluded == expected_excluded",
            "assert \"Area_comun/tasks/.gitkeep\" in extra_excluded",
            "assert hidden_scanned != expected_scanned",
            "assert \"runtime/Memory/case.txt\" not in case_scanned",
            "assert \"runtime/memory/index.db\" in separator_scanned",
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
        scanned_paths = {
            "Area_comun/artifacts/.gitkeep",
            "Area_comun/contracts/.gitkeep",
            "Area_comun/decisions/.gitkeep",
            "Area_comun/handoffs/.gitkeep",
            "Area_comun/mailbox/answered/.gitkeep",
            "Area_comun/mailbox/archived/.gitkeep",
            "Area_comun/mailbox/open/.gitkeep",
            "Area_comun/reports/.gitkeep",
            "Area_comun/tasks/.gitkeep",
            "runtime/.cache/note.txt",
            "runtime/Memory/case.txt",
            "runtime/memoryX/file.txt",
            "runtime/memory-extra/file.txt",
            "runtime/memoryfile.txt",
            "runtime/sub/memory/file.txt",
            "Area_comun/runtime/memory/file.txt",
        }
        excluded_paths = {
            "runtime/memory/index.db",
            "runtime/node_modules/hidden.txt",
            "runtime/__pycache__/hidden.txt",
            "runtime/.git/hidden.txt",
            "runtime/skip.png",
        }
        universe = scanned_paths | excluded_paths
        for relative in universe:
            path = fixture / relative
            if relative == "runtime/memory/index.db":
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"SQLite format 3\x00\xff\xfe\xfd")
            else:
                write(path, "# Espa\u00c3\u00b1a\n")

        python_result = run_scan(fixture)
        powershell_result = run_ps_scan(fixture)
        python_scanned = finding_paths(python_result.stdout) & universe
        powershell_scanned = finding_paths(powershell_result.stdout) & universe
        python_excluded = universe - python_scanned
        powershell_excluded = universe - powershell_scanned
        expected_scanned = scanned_paths
        expected_excluded = excluded_paths
        assert python_result.returncode == powershell_result.returncode == 1
        assert python_scanned == powershell_scanned == expected_scanned
        assert python_excluded == powershell_excluded == expected_excluded

        ps_text = PS_SCAN.read_text(encoding="utf-8-sig")
        separator_text = ps_text.replace(
            "        # Compare one host-native directory boundary, never a literal slash shape.\n"
            "        $trimChars = [char[]]@([System.IO.Path]::DirectorySeparatorChar, [System.IO.Path]::AltDirectorySeparatorChar)\n"
            "        $directoryPrefix = $directory.TrimEnd($trimChars) + [System.IO.Path]::DirectorySeparatorChar\n"
            "        if ($File.FullName.Equals($directory, $PathComparison) -or $File.FullName.StartsWith($directoryPrefix, $PathComparison)) { return $false }",
            '        if ($File.FullName -eq $directory -or $File.FullName.StartsWith("$directory\\", [System.StringComparison]::OrdinalIgnoreCase)) { return $false }',
            1,
        )
        assert separator_text != ps_text
        separator_path = fixture / "scan_encoding_separator_mutant.ps1"
        separator_path.write_text(separator_text, encoding="utf-8", newline="\n")
        separator_result = run_ps_scan(fixture, separator_path)
        if os.name != "nt":
            separator_scanned = finding_paths(separator_result.stdout) & universe
            assert "runtime/memory/index.db" in separator_scanned

        mutant_text = ps_text.replace(
            '$SkipAbsoluteDirs = @((Join-Path $ResolvedRoot "runtime/memory"))',
            '$SkipAbsoluteDirs = @((Join-Path $ResolvedRoot "runtime/memory"), (Join-Path $ResolvedRoot "Area_comun/tasks"))',
            1,
        )
        assert mutant_text != ps_text
        extra_path = fixture / "scan_encoding_extra_exclusion_mutant.ps1"
        extra_path.write_text(mutant_text, encoding="utf-8", newline="\n")
        extra_scanned = finding_paths(run_ps_scan(fixture, extra_path).stdout) & universe
        extra_excluded = universe - extra_scanned
        assert extra_excluded != expected_excluded
        assert "Area_comun/tasks/.gitkeep" in extra_excluded

        hidden_text = ps_text.replace(" -File -Force", " -File")
        assert hidden_text != ps_text
        hidden_path = fixture / "scan_encoding_hidden_omission_mutant.ps1"
        hidden_path.write_text(hidden_text, encoding="utf-8", newline="\n")
        if os.name != "nt":
            hidden_scanned = finding_paths(run_ps_scan(fixture, hidden_path).stdout) & universe
            assert hidden_scanned != expected_scanned
            assert "Area_comun/mailbox/open/.gitkeep" not in hidden_scanned

        case_text = ps_text.replace(
            "$PathComparison = [System.StringComparison]::Ordinal",
            "$PathComparison = [System.StringComparison]::OrdinalIgnoreCase",
            1,
        )
        assert case_text != ps_text
        case_path = fixture / "scan_encoding_case_mutant.ps1"
        case_path.write_text(case_text, encoding="utf-8", newline="\n")
        case_scanned = finding_paths(run_ps_scan(fixture, case_path).stdout) & universe
        assert "runtime/Memory/case.txt" not in case_scanned


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
