#!/usr/bin/env python3
"""Derived CI PowerShell inventory and host-assumption mutation contracts."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
WORKFLOW = ROOT / ".github" / "workflows" / "validate.yml"

# TASK-0338 owns this real, host-sensitive line-reader coordinate. The exception
# is structural (not a frozen source line) and bounded to one occurrence.
BOUNDED_LINE_READERS = {
    "scripts/scan_domain_neutrality.ps1": 1,
}

FALSIFICATION_CONTRACTS = (
    {
        "id": "NEG-POWERSHELL-HOST-ASSUMPTION-CLASS",
        "negative": "Every PowerShell surface derived from CI rejects known host-dependent path forms at every entry point and bounds the real line-reader residual.",
        "mutation": "for route, source in sources.items():",
        "boundaries": (
            "assert scan_powershell_surface(surface) == {}",
            "assert set(mutation_failures) == set(sources)",
            'assert classify_bash_boundary(bash_mutant) == {"bash_line_model"}',
            'assert scan_inline_powershell(mutant_surface.inline_commands[-1]) == {"relative_uri"}',
        ),
        "exercised_by": "case_host_surface_mutations",
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
        "negative": "The PowerShell parity runner reaches an unconditional success exit before any top-level exit can leak a child LASTEXITCODE.",
        "mutation": 'mutant_runner = insert_before_final_exit(runner_text, "exit $LASTEXITCODE")',
        "boundaries": (
            "assert runner_reaches_success_exit(runner_text)",
            "assert not runner_reaches_success_exit(mutant_runner)",
        ),
        "exercised_by": "case_expected_negative_exit",
    },
)


@dataclass(frozen=True)
class PowerShellSurface:
    paths: frozenset[str]
    inline_commands: tuple[str, ...]


def _effective_shell(workflow: dict, job: dict, step: dict) -> str | None:
    shell = step.get("shell")
    if shell is None:
        for owner in (job, workflow):
            defaults = owner.get("defaults", {})
            if isinstance(defaults, dict):
                run_defaults = defaults.get("run", {})
                if isinstance(run_defaults, dict) and "shell" in run_defaults:
                    shell = run_defaults["shell"]
                    break
    if isinstance(shell, str):
        return shell.split()[0].lower()
    runner = job.get("runs-on")
    if isinstance(runner, str) and runner.startswith("windows-"):
        return "powershell"
    return None


def workflow_powershell_surface(workflow_text: str) -> PowerShellSurface:
    """Derive files and inline commands from steps actually evaluated as PowerShell."""
    document = yaml.safe_load(workflow_text)
    if not isinstance(document, dict) or not isinstance(document.get("jobs"), dict):
        raise AssertionError("workflow must contain jobs")
    paths: set[str] = set()
    inline: list[str] = []
    path_pattern = re.compile(r"(?:^|\s)(?:\./)?([A-Za-z0-9_./-]+\.ps1)(?=\s|$)", re.I)
    for job in document["jobs"].values():
        if not isinstance(job, dict):
            continue
        for step in job.get("steps", []):
            if not isinstance(step, dict) or _effective_shell(document, job, step) not in {
                "pwsh",
                "powershell",
            }:
                continue
            command = step.get("run")
            if not isinstance(command, str):
                continue
            matches = {match.replace("\\", "/") for match in path_pattern.findall(command)}
            paths.update(matches)
            executable = [
                line.strip()
                for line in command.splitlines()
                if line.strip() and not line.lstrip().startswith("#")
            ]
            if not matches or len(executable) != 1:
                inline.append(command)
    return PowerShellSurface(frozenset(paths), tuple(inline))


def workflow_with_job(workflow_text: str, name: str, job: dict) -> str:
    """Return a workflow variant with one additional job."""
    document = yaml.safe_load(workflow_text)
    assert isinstance(document, dict) and isinstance(document.get("jobs"), dict)
    assert name not in document["jobs"]
    document["jobs"][name] = job
    return yaml.safe_dump(document, sort_keys=False)


def powershell_sources(surface: PowerShellSurface) -> dict[str, str]:
    sources: dict[str, str] = {}
    for route in sorted(surface.paths):
        path = ROOT / route
        assert path.is_file(), f"workflow PowerShell route does not exist: {route}"
        sources[route] = path.read_text(encoding="utf-8-sig")
    return sources


def _code_lines(source: str) -> str:
    """Drop full-line comments while preserving quoted path operands."""
    return "\n".join(
        line for line in source.splitlines() if not line.lstrip().startswith("#")
    )


def _line_reader_count(source: str) -> int:
    code = _code_lines(source)
    return len(
        re.findall(
            r"\$lines\s*=\s*@\(\s*Get-Content\b(?=[^\r\n)]*-Path\s+\$file\.Path\b)(?![^\r\n)]*\s-Raw\b)[^\r\n)]*\)",
            code,
            re.I,
        )
    )


def scan_powershell_source(route: str, source: str) -> set[str]:
    """Recognize semantic host forms, independent of source order and spacing."""
    code = _code_lines(source)
    violations: set[str] = set()
    if re.search(r"\.\s*MakeRelativeUri\s*\(", code, re.I):
        violations.add("relative_uri")
    # A literal host separator used as the boundary operand of StartsWith is
    # unsafe. This models the call shape rather than one frozen source string.
    literal_prefix = re.search(
        r"\.\s*StartsWith\s*\(\s*\"\s*\$[A-Za-z_][A-Za-z0-9_.]*\\\"\s*(?:,|\))",
        code,
        re.I,
    )
    literal_root_suffix = re.search(
        r"\.\s*TrimEnd\s*\([^\r\n)]*\)\s*\+\s*[\"']\\[\"']",
        code,
        re.I,
    )
    if literal_prefix or literal_root_suffix:
        violations.add("literal_path_boundary")
    if re.search(
        r"(?im)^\s*\$(?:Path)?Comparison\s*=\s*\[System\.StringComparison\]::OrdinalIgnoreCase\s*$",
        code,
    ):
        violations.add("fixed_case_path_comparison")
    readers = _line_reader_count(source)
    if readers > BOUNDED_LINE_READERS.get(route, 0):
        violations.add("unbounded_line_reader")
    return violations


def scan_inline_powershell(command: str) -> set[str]:
    return scan_powershell_source("<workflow-inline>", command)


def scan_powershell_surface(surface: PowerShellSurface) -> dict[str, set[str]]:
    violations = {
        route: found
        for route, source in powershell_sources(surface).items()
        if (found := scan_powershell_source(route, source))
    }
    for number, command in enumerate(surface.inline_commands, 1):
        found = scan_inline_powershell(command)
        if found:
            violations[f"<workflow-inline:{number}>"] = found
    return violations


def classify_bash_boundary(source: str) -> set[str]:
    return {"bash_line_model"} if re.search(r"command\s*\.\s*splitlines\s*\(\s*\)", source) else set()


def insert_before_final_exit(source: str, statement: str) -> str:
    matches = list(re.finditer(r"(?im)^(\s*)exit\s+0\s*(?:#.*)?$", source))
    assert matches, "runner has no success exit"
    match = matches[-1]
    return source[: match.start()] + statement + "\n" + source[match.start() :]


def runner_reaches_success_exit(source: str) -> bool:
    """Reject a top-level exit before the runner's unconditional ``exit 0``."""
    depth = 0
    for raw_line in source.splitlines():
        line = raw_line.split("#", 1)[0].strip()
        if not line:
            continue
        leading_closes = len(line) - len(line.lstrip("}"))
        depth = max(0, depth - leading_closes)
        body = line[leading_closes:].strip()
        match = re.fullmatch(r"exit(?:\s+(.+?))?", body, re.I)
        if match and depth == 0:
            return (match.group(1) or "").strip() == "0"
        depth += body.count("{") - body.count("}")
        depth = max(0, depth)
    return False


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


def case_inventory() -> None:
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    surface = workflow_powershell_surface(workflow_text)
    assert set(BOUNDED_LINE_READERS) <= set(surface.paths)
    assert scan_powershell_surface(surface) == {}

    safe_workflow = workflow_with_job(
        workflow_text,
        "inventory-safe-growth",
        {
            "runs-on": "ubuntu-latest",
            "steps": [
                {"shell": "pwsh", "run": "Write-Output 'inventory safe growth'"}
            ],
        },
    )
    safe_surface = workflow_powershell_surface(safe_workflow)
    assert safe_surface.paths == surface.paths
    assert safe_surface.inline_commands[:-1] == surface.inline_commands
    assert scan_inline_powershell(safe_surface.inline_commands[-1]) == set()
    assert scan_powershell_surface(safe_surface) == {}

    unsafe_workflow = workflow_with_job(
        workflow_text,
        "inventory-unbounded-inline",
        {
            "runs-on": "ubuntu-latest",
            "steps": [
                {"shell": "pwsh", "run": "$rootUri.MakeRelativeUri($fileUri)"}
            ],
        },
    )
    unsafe_surface = workflow_powershell_surface(unsafe_workflow)
    assert unsafe_surface.paths == surface.paths
    assert unsafe_surface.inline_commands[:-1] == surface.inline_commands
    assert scan_powershell_surface(unsafe_surface) == {
        f"<workflow-inline:{len(unsafe_surface.inline_commands)}>": {"relative_uri"}
    }


def case_host_surface_mutations() -> None:
    """PERMANENT_NEGATIVE: NEG-POWERSHELL-HOST-ASSUMPTION-CLASS"""
    workflow_text = WORKFLOW.read_text(encoding="utf-8")
    surface = workflow_powershell_surface(workflow_text)
    sources = powershell_sources(surface)
    assert scan_powershell_surface(surface) == {}

    mutation_failures: dict[str, set[str]] = {}
    forms = (
        '$probe = $rootUri . MakeRelativeUri ( $fileUri )',
        '$probe = $candidate.StartsWith( "$directory\\" )',
        '$lines = @( Get-Content -Encoding UTF8 -Path $file.Path )',
        "$PathComparison = [System.StringComparison]::OrdinalIgnoreCase",
    )
    for route, source in sources.items():
        killed: set[str] = set()
        for index, form in enumerate(forms):
            injected = source + ("\n\n" if index % 2 else "\n") + form + "\n"
            found = scan_powershell_source(route, injected)
            assert found, f"host mutant {index} escaped at {route}"
            killed.add(str(index))
        mutation_failures[route] = killed
    assert set(mutation_failures) == set(sources)
    assert all(len(killed) == len(forms) for killed in mutation_failures.values())

    # The TASK-0336 Bash boundary remains owned there, but its real production
    # reader and production mutant stay accredited without a synthetic marker.
    bash_path = ROOT / "scripts" / "check_falsification_contracts.py"
    bash_source = bash_path.read_text(encoding="utf-8-sig")
    bash_mutant = bash_source.replace('command.split("\\n")', "command.splitlines()", 1)
    assert bash_mutant != bash_source
    assert classify_bash_boundary(bash_source) == set()
    assert classify_bash_boundary(bash_mutant) == {"bash_line_model"}

    # Inline PowerShell is in scope mechanically even though the current
    # workflow has none: a new inline host form must not evade file discovery.
    inline_mutant = workflow_with_job(
        workflow_text,
        "inline-powershell-host-mutant",
        {
            "runs-on": "ubuntu-latest",
            "steps": [
                {"shell": "pwsh", "run": "$rootUri.MakeRelativeUri($fileUri)"}
            ],
        },
    )
    mutant_surface = workflow_powershell_surface(inline_mutant)
    assert len(mutant_surface.inline_commands) == len(surface.inline_commands) + 1
    assert mutant_surface.inline_commands[:-1] == surface.inline_commands
    assert scan_inline_powershell(mutant_surface.inline_commands[-1]) == {"relative_uri"}


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
    assert runner_reaches_success_exit(runner_text)
    mutant_runner = insert_before_final_exit(runner_text, "exit $LASTEXITCODE")
    assert mutant_runner != runner_text
    assert not runner_reaches_success_exit(mutant_runner)


def main() -> int:
    case_inventory()
    case_host_surface_mutations()
    case_linux_job_wiring()
    case_expected_negative_exit()
    surface = workflow_powershell_surface(WORKFLOW.read_text(encoding="utf-8"))
    print(
        f"OK: {len(surface.paths)} workflow-derived CI PowerShell entry points; "
        "28 all-coordinate production mutants; inline PowerShell and exit reachability covered."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
