#!/usr/bin/env python3
"""Inventory and mutation contracts for PowerShell entry points run by CI."""

from __future__ import annotations

import re
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "validate.yml"

CI_POWERSHELL_ENTRY_POINTS = {
    "examples/compact_comms_validation_cases/run_compact_comms_cases.ps1",
    "examples/llm_turn_wrapper_cases/run_llm_turn_wrapper_cases.ps1",
    "examples/neutrality_scan_cases/run_neutrality_scan_cases.ps1",
    "examples/sdd_validation_cases/run_sdd_cases.ps1",
    "scripts/scan_domain_neutrality.ps1",
    "scripts/scan_encoding.ps1",
    "scripts/validate_collaboration_state.ps1",
}

HOST_DIMENSIONS = {
    "separators": CI_POWERSHELL_ENTRY_POINTS,
    "absolute_vs_relative": CI_POWERSHELL_ENTRY_POINTS,
    "line_splitting": CI_POWERSHELL_ENTRY_POINTS,
    "filesystem_case": CI_POWERSHELL_ENTRY_POINTS,
    "line_endings": CI_POWERSHELL_ENTRY_POINTS,
}

FALSIFICATION_CONTRACTS = (
    {
        "id": "NEG-POWERSHELL-HOST-ASSUMPTION-CLASS",
        "negative": "All CI PowerShell entry points stay inventoried and the four known host-dependent forms stay absent or explicitly bounded.",
        "mutation": "mutants = {",
        "boundaries": (
            'assert classify_known_forms(mutants["line_reader"]) == {"line_reader"}',
            'assert classify_known_forms(mutants["bash_boundary"]) == {"bash_boundary"}',
            'assert classify_known_forms(mutants["literal_separator"]) == {"literal_separator"}',
            'assert classify_known_forms(mutants["relative_uri"]) == {"relative_uri"}',
        ),
        "exercised_by": "case_known_form_mutations",
    },
    {
        "id": "NEG-POWERSHELL-LINUX-JOB-WIRING",
        "negative": "A dedicated Linux job executes the affected PowerShell twins and the permanent host contract with job-failure power.",
        "mutation": 'mutant_workflow = workflow_text.replace("runs-on: ubuntu-latest", "runs-on: windows-latest", 1)',
        "boundaries": (
            "assert linux_job_is_failure_gating(workflow_text)",
            "assert not linux_job_is_failure_gating(mutant_workflow)",
        ),
        "exercised_by": "case_linux_job_wiring",
    },
    {
        "id": "NEG-POWERSHELL-EXPECTED-NEGATIVE-EXIT-LEAK",
        "negative": "A PowerShell parity runner must not leak LASTEXITCODE from its final expected-negative child process.",
        "mutation": 'mutant_runner = runner_text.replace("\\nexit 0\\n", "\\n", 1)',
        "boundaries": (
            "assert runner_has_explicit_success_exit(runner_text)",
            "assert not runner_has_explicit_success_exit(mutant_runner)",
        ),
        "exercised_by": "case_expected_negative_exit",
    },
)


def workflow_powershell_paths(workflow_text: str) -> set[str]:
    return {
        match.replace("\\", "/")
        for match in re.findall(r"(?:\./)?([A-Za-z0-9_./-]+\.ps1)\b", workflow_text)
    }


def classify_known_forms(text: str) -> set[str]:
    forms: set[str] = set()
    if "TASK0345_UNBOUNDED_GET_CONTENT_LINE_READER" in text:
        forms.add("line_reader")
    if "command.splitlines()" in text:
        forms.add("bash_boundary")
    if 'StartsWith("$directory\\")' in text:
        forms.add("literal_separator")
    if ".MakeRelativeUri(" in text:
        forms.add("relative_uri")
    return forms


def linux_job_is_failure_gating(workflow_text: str) -> bool:
    document = yaml.safe_load(workflow_text)
    jobs = document.get("jobs", {}) if isinstance(document, dict) else {}
    job = jobs.get("powershell-linux-parity", {}) if isinstance(jobs, dict) else {}
    if job.get("runs-on") != "ubuntu-latest" or job.get("continue-on-error") is True:
        return False
    required = {
        "./scripts/scan_encoding.ps1 -Root .",
        "./scripts/scan_domain_neutrality.ps1 -Root .",
        "./examples/neutrality_scan_cases/run_neutrality_scan_cases.ps1",
        "python examples/neutrality_scan_cases/run_powershell_host_cases.py",
    }
    steps = job.get("steps", []) if isinstance(job, dict) else []
    commands = {step.get("run") for step in steps if isinstance(step, dict)}
    return required <= commands and all(
        step.get("continue-on-error") is not True
        for step in steps
        if isinstance(step, dict) and step.get("run") in required
    )


def runner_has_explicit_success_exit(source: str) -> bool:
    return source.rstrip().endswith("exit 0")


def case_inventory() -> None:
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert workflow_powershell_paths(workflow_text) == CI_POWERSHELL_ENTRY_POINTS
    assert set(HOST_DIMENSIONS) == {
        "separators",
        "absolute_vs_relative",
        "line_splitting",
        "filesystem_case",
        "line_endings",
    }
    assert all(paths == CI_POWERSHELL_ENTRY_POINTS for paths in HOST_DIMENSIONS.values())

    neutrality = (ROOT / "scripts" / "scan_domain_neutrality.ps1").read_text(encoding="utf-8-sig")
    encoding = (ROOT / "scripts" / "scan_encoding.ps1").read_text(encoding="utf-8-sig")
    bash_reader = (ROOT / "scripts" / "check_falsification_contracts.py").read_text(encoding="utf-8-sig")
    assert ".MakeRelativeUri(" not in neutrality
    assert 'StartsWith("$directory\\")' not in encoding
    assert bash_reader.count('command.split("\\n")') == 1
    # TASK-0338 owns the one remaining scanner line-reader mismatch. This
    # contract freezes its footprint so TASK-0345 does not absorb that work.
    assert neutrality.count("$lines = @(Get-Content -Path $file.Path -Encoding UTF8)") == 1


def case_known_form_mutations() -> None:
    """PERMANENT_NEGATIVE: NEG-POWERSHELL-HOST-ASSUMPTION-CLASS"""
    neutrality = (ROOT / "scripts" / "scan_domain_neutrality.ps1").read_text(encoding="utf-8-sig")
    encoding = (ROOT / "scripts" / "scan_encoding.ps1").read_text(encoding="utf-8-sig")
    bash_reader = (ROOT / "scripts" / "check_falsification_contracts.py").read_text(encoding="utf-8-sig")
    mutants = {
        "line_reader": neutrality.replace(
            "$lines = @(Get-Content -Path $file.Path -Encoding UTF8)",
            "$lines = @(Get-Content -Path $file.Path -Encoding UTF8) # TASK0345_UNBOUNDED_GET_CONTENT_LINE_READER",
            1,
        ),
        "bash_boundary": bash_reader.replace('command.split("\\n")', "command.splitlines()", 1),
        "literal_separator": encoding.replace(
            "StartsWith($directoryPrefix, $PathComparison)",
            'StartsWith("$directory\\")',
            1,
        ),
        "relative_uri": neutrality.replace(
            "$relativePath = $resolvedFullPath.Substring($rootPrefix.Length)",
            "$relativePath = $rootUri.MakeRelativeUri($fileUri).ToString()",
            1,
        ),
    }
    assert classify_known_forms(mutants["line_reader"]) == {"line_reader"}
    assert classify_known_forms(mutants["bash_boundary"]) == {"bash_boundary"}
    assert classify_known_forms(mutants["literal_separator"]) == {"literal_separator"}
    assert classify_known_forms(mutants["relative_uri"]) == {"relative_uri"}
    assert classify_known_forms(neutrality) == set()
    assert classify_known_forms(encoding) == set()
    assert classify_known_forms(bash_reader) == set()


def case_linux_job_wiring() -> None:
    """PERMANENT_NEGATIVE: NEG-POWERSHELL-LINUX-JOB-WIRING"""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    assert linux_job_is_failure_gating(workflow_text)
    mutant_workflow = workflow_text.replace("runs-on: ubuntu-latest", "runs-on: windows-latest", 1)
    assert mutant_workflow != workflow_text
    assert not linux_job_is_failure_gating(mutant_workflow)


def case_expected_negative_exit() -> None:
    """PERMANENT_NEGATIVE: NEG-POWERSHELL-EXPECTED-NEGATIVE-EXIT-LEAK"""
    runner_path = ROOT / "examples" / "neutrality_scan_cases" / "run_neutrality_scan_cases.ps1"
    runner_text = runner_path.read_text(encoding="utf-8-sig")
    assert runner_has_explicit_success_exit(runner_text)
    mutant_runner = runner_text.replace("\nexit 0\n", "\n", 1)
    assert mutant_runner != runner_text
    assert not runner_has_explicit_success_exit(mutant_runner)


def main() -> int:
    case_inventory()
    case_known_form_mutations()
    case_linux_job_wiring()
    case_expected_negative_exit()
    print("OK: 7 CI PowerShell entry points x 5 host dimensions; 5 host mutations; Linux job wiring.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
