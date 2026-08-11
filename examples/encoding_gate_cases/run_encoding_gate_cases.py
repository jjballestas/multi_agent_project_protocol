#!/usr/bin/env python3
"""Golden cases for scripts/scan_encoding.py."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCAN = ROOT / "scripts" / "scan_encoding.py"
PS_SCAN = ROOT / "scripts" / "scan_encoding.ps1"
POWERSHELL = shutil.which("pwsh")
sys.path.insert(0, str(ROOT / "scripts"))
import scan_encoding as python_scan  # noqa: E402

FALSIFICATION_CONTRACTS = (
    {
        "id": "NEG-ENCODING-SKIP-PATH-SEPARATOR",
        "negative": "Python and PowerShell must derive identical scanned and excluded sets from effective runtime policy, independent of coordinate, order, formatting, hidden-enumeration channel, dot-only basenames, case semantics, and host path separators.",
        "mutation": "mutant_text = insert_after_policy_build(",
        "boundaries": (
            "assert python_scanned == powershell_scanned == expected_scanned",
            "assert python_excluded == powershell_excluded == expected_excluded",
            "assert \"Area_comun/tasks/.gitkeep\" in extra_excluded",
            "assert relative_case_paths - case_scanned",
            "assert relative_exact_paths <= separator_scanned",
            "assert dot_suffix_paths <= expected_scanned",
            "assert directory_case_paths <= expected_scanned",
            "assert suffix_case_paths <= expected_excluded",
            "assert skip_dir_case_scanned != expected_scanned",
            "assert ascii_hidden_scanned != expected_scanned",
            "assert state_hidden_scanned != expected_scanned",
            "assert mojibake_hidden_scanned != expected_scanned",
            "assert (control_path in policy_scanned) is expected_control_scanned",
            "assert (policy_mutant[\"skip_dirs\"] == ps_skip_dirs) is expected_policy_equal",
            "assert policy_declares_excluded",
            "assert affected_paths <= late_scanned",
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


def powershell_policy(root: Path, script: Path = PS_SCAN) -> dict[str, set[str]]:
    if not POWERSHELL:
        raise RuntimeError("PowerShell is required for encoding scanner policy parity")
    result = subprocess.run(
        [POWERSHELL, "-NoProfile", "-File", str(script), "-Root", str(root), "-DumpPolicy"],
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise AssertionError(f"PowerShell policy dump failed: {result.stderr}")
    payload = json.loads(result.stdout)
    return {
        "skip_dirs": set(payload["skip_dirs"]),
        "skip_relative_dirs": {value.replace("\\", "/") for value in payload["skip_relative_dirs"]},
        "skip_suffixes": set(payload["skip_suffixes"]),
    }


def case_variant(value: str) -> str | None:
    variant = value.swapcase()
    if variant == value:
        return None
    return variant


def relative_case_variant(value: str) -> str | None:
    parts = value.rstrip("/").split("/")
    for index in range(len(parts) - 1, -1, -1):
        variant = case_variant(parts[index])
        if variant is not None:
            parts[index] = variant
            return "/".join(parts)
    return None


def mutate_function(text: str, function_name: str, old: str, new: str) -> str:
    start = text.index(f"function {function_name} {{")
    next_function = text.find("\nfunction ", start + 1)
    end = len(text) if next_function < 0 else next_function
    body = text[start:end]
    mutated_body = body.replace(old, new, 1)
    if mutated_body == body:
        raise AssertionError(f"mutation anchor missing in {function_name}: {old}")
    return text[:start] + mutated_body + text[end:]


def insert_after_policy_build(text: str, statement: str) -> str:
    match = re.search(r"(?m)^\$ScanPolicy[ \t]*=[ \t]*New-ScanPolicy[ \t]*(?:#.*)?$", text)
    if not match:
        raise AssertionError("effective policy construction point is missing")
    return text[: match.end()] + "\n" + statement + text[match.end() :]


def insert_before_policy_dump(text: str, statement: str) -> str:
    match = re.search(r"(?m)^if \(\$DumpPolicy\) \{$", text)
    if not match:
        raise AssertionError("post-consumption policy dump point is missing")
    return text[: match.start()] + statement + "\n\n" + text[match.start() :]


def fresh_directory_coordinate(*policies: set[str]) -> str:
    occupied = set().union(*policies)
    index = 0
    while True:
        candidate = f"contract-control-{index}"
        if candidate not in occupied:
            return candidate
        index += 1


def fresh_suffix_coordinate(*policies: set[str]) -> str:
    occupied = set().union(*policies)
    index = 0
    while True:
        candidate = f".contract{index}"
        if candidate not in occupied:
            return candidate
        index += 1


def has_case_sensitive_filesystem(root: Path) -> bool:
    lower = root / "case-probe"
    upper = root / "CASE-PROBE"
    lower.write_text("probe\n", encoding="ascii")
    return not upper.exists()


def assert_case(name: str, expected: int, **fixture_kwargs: str) -> None:
    with task_temp(f"encoding-{name}-") as temp:
        fixture = Path(temp)
        build_fixture(fixture, **fixture_kwargs)
        result = run_scan(fixture)
        if result.returncode != expected:
            print(result.stdout)
            print(result.stderr)
            raise AssertionError(f"{name}: expected exit {expected}, got {result.returncode}")


def assert_cross_platform_skip_parity() -> bool:
    """PERMANENT_NEGATIVE: NEG-ENCODING-SKIP-PATH-SEPARATOR"""
    if not POWERSHELL:
        print("UNMEASURED: PowerShell 7 parity requires pwsh; CI measures the POSIX boundary.")
        return False
    with task_temp("encoding-skip-parity-") as temp:
        fixture = Path(temp)
        if not has_case_sensitive_filesystem(fixture):
            print("UNMEASURED: skip parity requires a case-sensitive filesystem; CI measures it on POSIX.")
            return False
        build_fixture(fixture)
        ps_text = PS_SCAN.read_text(encoding="utf-8-sig")
        ps_policy = powershell_policy(fixture)
        ps_skip_dirs = ps_policy["skip_dirs"]
        ps_skip_relative_dirs = ps_policy["skip_relative_dirs"]
        ps_skip_suffixes = ps_policy["skip_suffixes"]
        declared_skip_dirs = set(python_scan.SKIP_DIRS) | ps_skip_dirs
        declared_skip_relative_dirs = set(python_scan.SKIP_RELATIVE_DIRS) | ps_skip_relative_dirs
        declared_skip_suffixes = set(python_scan.SKIP_SUFFIXES) | ps_skip_suffixes
        assert set(python_scan.SKIP_DIRS) == ps_skip_dirs
        assert set(python_scan.SKIP_RELATIVE_DIRS) == ps_policy["skip_relative_dirs"]
        assert set(python_scan.SKIP_SUFFIXES) == ps_skip_suffixes

        scanned_paths = {
            "Area_comun/artifacts/.gitkeep",
            "Area_comun/contracts/.gitkeep",
            "Area_comun/decisions/.gitkeep",
            "Area_comun/handoffs/.gitkeep",
            "Area_comun/mailbox/answered/.gitkeep",
            "Area_comun/mailbox/archived/.gitkeep",
            "Area_comun/mailbox/open/.gitkeep",
            "Area_comun/mailbox/open/.hidden.md",
            "Area_comun/state/.hidden.json",
            "Area_comun/tasks/.hidden.md",
            "Area_comun/reports/.gitkeep",
            "Area_comun/tasks/.gitkeep",
            "runtime/.cache/note.txt",
        }
        excluded_paths: set[str] = set()
        relative_exact_paths = {
            f"{item.rstrip('/')}/contract-{index}.db"
            for index, item in enumerate(sorted(declared_skip_relative_dirs))
        }
        relative_near_paths = {
            coordinate
            for item in declared_skip_relative_dirs
            for coordinate in (
                f"{item.rstrip('/')}X/file.txt",
                f"{item.rstrip('/')}-extra/file.txt",
                f"{item.rstrip('/')}file.txt",
            )
        }
        relative_case_paths = {
            f"{variant}/case.txt"
            for item in declared_skip_relative_dirs
            if (variant := relative_case_variant(item)) is not None
        }
        relative_nested_paths = {
            coordinate
            for item in declared_skip_relative_dirs
            for coordinate in (
                f"Area_comun/{item.rstrip('/')}/file.txt",
                f"runtime/sub/{item.rstrip('/').split('/')[-1]}/file.txt",
            )
        }
        directory_exact_paths = {f"runtime/{item}/exact.txt" for item in declared_skip_dirs}
        directory_case_paths = {
            f"runtime/{variant}/case.txt"
            for item in declared_skip_dirs
            if (variant := case_variant(item)) is not None
        }
        suffix_exact_paths = {
            f"runtime/suffixes/exact-{index}{suffix}"
            for index, suffix in enumerate(sorted(declared_skip_suffixes))
        }
        suffix_case_paths = {
            f"runtime/suffixes/case-{index}{variant}"
            for index, suffix in enumerate(sorted(declared_skip_suffixes))
            if (variant := case_variant(suffix)) is not None
        }
        dot_suffix_paths = {
            f"Area_comun/mailbox/open/{suffix}" for suffix in declared_skip_suffixes
        }
        excluded_paths |= relative_exact_paths | directory_exact_paths | suffix_exact_paths | suffix_case_paths
        scanned_paths |= relative_near_paths | relative_case_paths | relative_nested_paths | directory_case_paths | dot_suffix_paths
        universe = scanned_paths | excluded_paths
        for relative in universe:
            path = fixture / relative
            if relative in relative_exact_paths:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(b"SQLite format 3\x00\xff\xfe\xfd")
            elif relative.startswith("Area_comun/mailbox/") or relative.startswith("Area_comun/state/"):
                write(path, "# se\u00f1al\n")
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
        assert dot_suffix_paths <= expected_scanned
        assert directory_case_paths <= expected_scanned
        assert suffix_case_paths <= expected_excluded
        assert python_result.returncode == powershell_result.returncode == 1
        assert python_scanned == powershell_scanned == expected_scanned, {
            "python_missing": sorted(expected_scanned - python_scanned),
            "python_extra": sorted(python_scanned - expected_scanned),
            "powershell_missing": sorted(expected_scanned - powershell_scanned),
            "powershell_extra": sorted(powershell_scanned - expected_scanned),
        }
        assert python_excluded == powershell_excluded == expected_excluded

        control_dir = fresh_directory_coordinate(
            declared_skip_dirs,
            {Path(item).name for item in declared_skip_relative_dirs},
        )
        control_path = f"runtime/{control_dir}/a.txt"
        live_append = f'$ScanPolicy.SkipDirs += "{control_dir}"'
        live_replace = (
            f'$ScanPolicy.SkipDirs = @($ScanPolicy.SkipDirs) + @("{control_dir}")'
        )
        policy_mutants = (
            ("A4_plus_equals", insert_after_policy_build(ps_text, live_append), False, False),
            ("A7_later_assignment", insert_after_policy_build(ps_text, live_replace), False, False),
            ("A5_multiline", insert_after_policy_build(ps_text, "# equivalent multiline format\n"), True, True),
            ("A8_trailing_comment", insert_after_policy_build(ps_text, "# same effective policy"), True, True),
        )
        write(fixture / control_path, "# Espa\u00c3\u00b1a\n")
        assert control_path in finding_paths(run_scan(fixture).stdout)
        for name, mutant, expected_control_scanned, expected_policy_equal in policy_mutants:
            mutant_path = fixture / f"scan_encoding_{name}_mutant.ps1"
            mutant_path.write_text(mutant, encoding="utf-8", newline="\n")
            policy_mutant = powershell_policy(fixture, mutant_path)
            policy_scanned = finding_paths(run_ps_scan(fixture, mutant_path).stdout)
            assert (control_path in policy_scanned) is expected_control_scanned
            assert (policy_mutant["skip_dirs"] == ps_skip_dirs) is expected_policy_equal
            verdict = "ACCEPTED_EQUIVALENT" if expected_policy_equal else "CAUGHT_DIVERGENCE"
            print(f"POLICY_MUTATION {name} {verdict}")

        late_suffix = fresh_suffix_coordinate(declared_skip_suffixes)
        late_absolute_dir = fresh_directory_coordinate(
            declared_skip_dirs,
            {Path(item).name for item in declared_skip_relative_dirs},
            {control_dir},
        )
        late_dir_path = f"runtime/{control_dir}/late.txt"
        late_suffix_path = f"runtime/late-suffix/file{late_suffix}"
        late_absolute_path = f"runtime/{late_absolute_dir}/late.txt"
        late_probe_paths = {late_dir_path, late_suffix_path, late_absolute_path}
        for relative in late_probe_paths:
            write(fixture / relative, "# Espa\u00c3\u00b1a\n")
        late_mutants = (
            ("G9a", f'$ScanPolicy.SkipDirs += "{control_dir}"', {late_dir_path}),
            ("G9b", f'$ScanPolicy.SkipSuffixes += "{late_suffix}"', {late_suffix_path}),
            (
                "G9c",
                f'$ScanPolicy.SkipAbsoluteDirs += (Join-Path $ResolvedRoot "runtime/{late_absolute_dir}")',
                {late_absolute_path},
            ),
            (
                "G9d",
                "\n".join(
                    (
                        f'$ScanPolicy.SkipDirs += "{control_dir}"',
                        f'$ScanPolicy.SkipSuffixes += "{late_suffix}"',
                        f'$ScanPolicy.SkipAbsoluteDirs += (Join-Path $ResolvedRoot "runtime/{late_absolute_dir}")',
                    )
                ),
                late_probe_paths,
            ),
        )
        for name, statement, affected_paths in late_mutants:
            late_text = insert_before_policy_dump(ps_text, statement)
            late_path = fixture / f"scan_encoding_{name}_late_policy_mutant.ps1"
            late_path.write_text(late_text, encoding="utf-8", newline="\n")
            late_policy = powershell_policy(fixture, late_path)
            late_scanned = finding_paths(run_ps_scan(fixture, late_path).stdout)
            policy_declares_excluded = (
                control_dir in late_policy["skip_dirs"]
                or late_suffix in late_policy["skip_suffixes"]
                or f"runtime/{late_absolute_dir}" in late_policy["skip_relative_dirs"]
            )
            assert policy_declares_excluded
            assert affected_paths <= late_scanned
            print(f"LATE_POLICY_MUTATION {name} CAUGHT_DIVERGENCE")

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
            assert relative_exact_paths <= separator_scanned

        mutant_text = insert_after_policy_build(
            ps_text,
            '$ScanPolicy.SkipAbsoluteDirs += (Join-Path $ResolvedRoot "Area_comun/tasks")',
        )
        assert mutant_text != ps_text
        extra_path = fixture / "scan_encoding_extra_exclusion_mutant.ps1"
        extra_path.write_text(mutant_text, encoding="utf-8", newline="\n")
        extra_scanned = finding_paths(run_ps_scan(fixture, extra_path).stdout) & universe
        extra_excluded = universe - extra_scanned
        assert extra_excluded != expected_excluded
        assert "Area_comun/tasks/.gitkeep" in extra_excluded

        ascii_hidden_text = mutate_function(ps_text, "Scan-AsciiPath", " -File -Force", " -File")
        ascii_hidden_path = fixture / "scan_encoding_ascii_hidden_omission_mutant.ps1"
        ascii_hidden_path.write_text(ascii_hidden_text, encoding="utf-8", newline="\n")
        if os.name != "nt":
            ascii_hidden_scanned = finding_paths(run_ps_scan(fixture, ascii_hidden_path).stdout) & universe
            assert ascii_hidden_scanned != expected_scanned
            assert "Area_comun/mailbox/open/.hidden.md" not in ascii_hidden_scanned

        state_hidden_text = mutate_function(ps_text, "Scan-AsciiStateJson", " -File -Force", " -File")
        state_hidden_path = fixture / "scan_encoding_state_hidden_omission_mutant.ps1"
        state_hidden_path.write_text(state_hidden_text, encoding="utf-8", newline="\n")
        if os.name != "nt":
            state_hidden_scanned = finding_paths(run_ps_scan(fixture, state_hidden_path).stdout) & universe
            assert state_hidden_scanned != expected_scanned
            assert "Area_comun/state/.hidden.json" not in state_hidden_scanned

        mojibake_hidden_text = mutate_function(ps_text, "Scan-MojibakeRoot", " -File -Force", " -File")
        mojibake_hidden_path = fixture / "scan_encoding_mojibake_hidden_omission_mutant.ps1"
        mojibake_hidden_path.write_text(mojibake_hidden_text, encoding="utf-8", newline="\n")
        if os.name != "nt":
            mojibake_hidden_scanned = finding_paths(run_ps_scan(fixture, mojibake_hidden_path).stdout) & universe
            assert mojibake_hidden_scanned != expected_scanned
            assert "Area_comun/tasks/.hidden.md" not in mojibake_hidden_scanned

        case_text = ps_text.replace(
            "$PathComparison = [System.StringComparison]::Ordinal",
            "$PathComparison = [System.StringComparison]::OrdinalIgnoreCase",
            1,
        )
        assert case_text != ps_text
        case_path = fixture / "scan_encoding_case_mutant.ps1"
        case_path.write_text(case_text, encoding="utf-8", newline="\n")
        case_scanned = finding_paths(run_ps_scan(fixture, case_path).stdout) & universe
        assert relative_case_paths - case_scanned

        skip_dir_case_text = ps_text.replace("$ScanPolicy.SkipDirs -ccontains $part", "$ScanPolicy.SkipDirs -contains $part", 1)
        assert skip_dir_case_text != ps_text
        skip_dir_case_path = fixture / "scan_encoding_skip_dir_case_mutant.ps1"
        skip_dir_case_path.write_text(skip_dir_case_text, encoding="utf-8", newline="\n")
        skip_dir_case_scanned = finding_paths(run_ps_scan(fixture, skip_dir_case_path).stdout) & universe
        assert skip_dir_case_scanned != expected_scanned
        assert directory_case_paths - skip_dir_case_scanned
        return True


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

    parity_measured = assert_cross_platform_skip_parity()

    if parity_measured:
        print("OK: encoding gate cases passed (3 py cases + measured PowerShell parity and separator mutation).")
    else:
        print("OK: encoding gate cases passed (3 py cases; PowerShell parity UNMEASURED).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
