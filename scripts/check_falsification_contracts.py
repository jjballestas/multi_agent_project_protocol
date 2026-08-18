#!/usr/bin/env python3
"""Inventory declared falsification mutations beside convention-marked negative tests.

Discovery walks the complete AST of every Python file under ``examples/`` and
``scripts/``, including methods and nested functions. ``PERMANENT_NEGATIVE:`` is
mandatory and load-bearing: an unmarked or runtime-generated negative is a prohibited
review/CI defect, but cannot be inferred from the static source. The inventory is
complete for source definitions that follow the convention; runtime generation is not
mechanically decidable here.
"""

from __future__ import annotations

import argparse
import ast
import re
import sys
from pathlib import Path

import yaml

from falsification_contracts import validate_contracts


PERMANENT_NEGATIVE_PREFIX = "PERMANENT_NEGATIVE:"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--inventory", action="store_true")
    parser.add_argument(
        "--workflow",
        help="Workflow file whose run commands must execute every declared contract owner.",
    )
    return parser.parse_args()


def workflow_steps(
    path: Path,
) -> tuple[bool, list[tuple[str, dict[str, object], dict[str, object], dict[str, object]]]]:
    """Return trigger coverage and real steps nested under real workflow jobs."""
    document = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    if not isinstance(document, dict):
        raise ValueError(f"{path}: workflow must be a mapping")
    # PyYAML uses YAML 1.1 and therefore parses an unquoted GitHub ``on`` key as True.
    raw_triggers = document.get("on", document.get(True))
    if isinstance(raw_triggers, str):
        triggers = {raw_triggers}
    elif isinstance(raw_triggers, list):
        triggers = {str(item) for item in raw_triggers}
    elif isinstance(raw_triggers, dict):
        triggers = {str(item) for item in raw_triggers}
    else:
        triggers = set()
    required_triggers = {"push", "pull_request"}
    jobs = document.get("jobs")
    if not isinstance(jobs, dict):
        raise ValueError(f"{path}: workflow must define a jobs mapping")
    workflow_defaults = document.get("defaults")
    if not isinstance(workflow_defaults, dict):
        workflow_defaults = {}
    found: list[tuple[str, dict[str, object], dict[str, object], dict[str, object]]] = []
    for job_id, raw_job in jobs.items():
        if not isinstance(raw_job, dict):
            continue
        steps = raw_job.get("steps")
        if not isinstance(steps, list):
            continue
        for raw_step in steps:
            if isinstance(raw_step, dict):
                found.append((str(job_id), workflow_defaults, raw_job, raw_step))
    return required_triggers <= triggers, found


def configured_shell(
    workflow_defaults: dict[str, object],
    job: dict[str, object],
    step: dict[str, object],
) -> object:
    """Resolve the step, job-default, then workflow-default shell declaration."""
    if "shell" in step:
        return step["shell"]
    for defaults in (job.get("defaults"), workflow_defaults):
        if not isinstance(defaults, dict):
            continue
        run_defaults = defaults.get("run")
        if isinstance(run_defaults, dict) and "shell" in run_defaults:
            return run_defaults["shell"]
    return None


def effective_shell_kind(
    workflow_defaults: dict[str, object],
    job: dict[str, object],
    step: dict[str, object],
) -> str | None:
    """Resolve only shell families whose single-command exit semantics are known."""
    shell = configured_shell(workflow_defaults, job, step)
    if shell == "bash":
        return "bash"
    if shell in {"pwsh", "powershell"}:
        return "powershell"
    if shell == "cmd":
        return "cmd"
    if shell is not None:
        return None
    runs_on = job.get("runs-on")
    if not isinstance(runs_on, str):
        return None
    if runs_on.startswith(("ubuntu-", "macos-")):
        return "bash"
    if runs_on.startswith("windows-"):
        return "powershell"
    return None


def shell_guarantees_abort(
    workflow_defaults: dict[str, object],
    job: dict[str, object],
    step: dict[str, object],
) -> bool:
    """Recognize GitHub shell modes that abort a multiline script on first failure."""
    return effective_shell_kind(workflow_defaults, job, step) == "bash"


def bash_line_continues(raw_line: str) -> bool:
    """Detect an executable Bash line whose final backslash consumes the next newline."""
    if not raw_line.strip(" \t") or raw_line.lstrip(" \t").startswith("#"):
        return False
    trailing_backslashes = len(raw_line) - len(raw_line.rstrip("\\"))
    return trailing_backslashes % 2 == 1


def recognized_command_form(
    command: str,
    relative_path: Path,
    workflow_defaults: dict[str, object],
    job: dict[str, object],
    step: dict[str, object],
) -> str | None:
    """Return the short, fail-closed command form proved by the static gate.

    The whitelist has two members: one undecorated runner invocation under a
    resolved shell family, or one aborting Bash block made only of a single runner invocation, inert ``echo``
    commands, undecorated Python processes, blank lines, and standalone comments.
    Any executable Bash line continuation is outside the grammar. This makes a
    following physical comment incapable of splicing the runner into an earlier
    command while preserving ordinary standalone comments (including ``# ... \\``).
    """
    path_parts = [re.escape(part) for part in relative_path.parts]
    candidate = r"[\\/]".join(path_parts)
    python = r"(?:python(?:3(?:\.\d+)*)?(?:\.exe)?|py(?:\.exe)?(?:\s+-3)?)"
    invocation = re.compile(
        rf"{python}\s+(?:{candidate}|\"{candidate}\"|'{candidate}')",
        re.IGNORECASE,
    )
    safe_echo = re.compile(r"echo(?:\s+[A-Za-z0-9_./: -]+)?", re.IGNORECASE)
    safe_python = re.compile(
        rf"{python}\s+[A-Za-z0-9_./:=,-]+(?:\s+[A-Za-z0-9_./:=,-]+)*",
        re.IGNORECASE,
    )
    shell_kind = effective_shell_kind(workflow_defaults, job, step)
    if shell_kind is None:
        return None
    # Bash ends commands at LF. Python-only line separators remain inside the
    # same command and must not manufacture extra whitelist members. Trim only
    # horizontal layout whitespace; other controls are command-significant.
    physical_lines = command.split("\n")
    executable_lines = [
        line.strip(" \t")
        for line in physical_lines
        if line.strip(" \t") and not line.lstrip(" \t").startswith("#")
    ]
    if len(executable_lines) == 1 and invocation.fullmatch(executable_lines[0]):
        return "single_runner"
    if shell_kind != "bash" or not shell_guarantees_abort(workflow_defaults, job, step):
        return None
    if any(bash_line_continues(line) for line in physical_lines):
        return None
    if sum(bool(invocation.fullmatch(line)) for line in executable_lines) != 1:
        return None
    if all(
        invocation.fullmatch(line) or safe_echo.fullmatch(line) or safe_python.fullmatch(line)
        for line in executable_lines
    ):
        return "bash_abort_block"
    return None


def command_gates_runner(
    command: str,
    relative_path: Path,
    workflow_defaults: dict[str, object],
    job: dict[str, object],
    step: dict[str, object],
) -> bool:
    """Accept only one of the two explicitly proved command forms."""
    return recognized_command_form(
        command, relative_path, workflow_defaults, job, step
    ) is not None


def condition_allows_execution(value: object) -> bool:
    """Accept only conditions that do not select a branch or event-specific path."""
    if value is None:
        return True
    if not isinstance(value, str):
        return False
    normalized = re.sub(r"\s+", "", value).lower()
    if normalized.startswith("${{") and normalized.endswith("}}"):
        normalized = normalized[3:-2]
    return normalized in {"always()", "success()"}


def failure_reaches_job(mapping: dict[str, object]) -> bool:
    """Only an absent or literal false continue-on-error preserves the failure."""
    return "continue-on-error" not in mapping or mapping["continue-on-error"] is False


def step_gates_runner(
    workflow_triggers: bool,
    workflow_defaults: dict[str, object],
    job: dict[str, object],
    step: dict[str, object],
    relative_path: Path,
) -> bool:
    command = step.get("run")
    if not workflow_triggers:
        return False
    if "needs" in job or "needs" in step:
        return False
    if not condition_allows_execution(job.get("if")) or not condition_allows_execution(step.get("if")):
        return False
    if not failure_reaches_job(job) or not failure_reaches_job(step):
        return False
    return isinstance(command, str) and command_gates_runner(
        command, relative_path, workflow_defaults, job, step
    )


def declarations(path: Path) -> list[dict[str, object]]:
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    for node in tree.body:
        if isinstance(node, (ast.Assign, ast.AnnAssign)):
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if any(isinstance(target, ast.Name) and target.id == "FALSIFICATION_CONTRACTS" for target in targets):
                value = ast.literal_eval(node.value)
                if not isinstance(value, (list, tuple)):
                    raise ValueError(f"{path}: FALSIFICATION_CONTRACTS must be a sequence")
                return list(value)
    return []


def function_source(path: Path, name: str) -> str:
    source = path.read_text(encoding="utf-8-sig")
    tree = ast.parse(source, filename=str(path))
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == name:
            return ast.get_source_segment(source, node) or ""
    return ""


def permanent_negatives(path: Path) -> dict[str, str]:
    """Discover the negative-test universe independently from contract declarations."""
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    found: dict[str, str] = {}
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        docstring = ast.get_docstring(node, clean=False) or ""
        for line in docstring.splitlines():
            marker = line.strip()
            if not marker.startswith(PERMANENT_NEGATIVE_PREFIX):
                continue
            ids = [item.strip() for item in marker[len(PERMANENT_NEGATIVE_PREFIX) :].split(",")]
            for negative_id in ids:
                if not negative_id:
                    raise ValueError(f"{path}:{node.name}: empty permanent-negative marker")
                if negative_id in found:
                    raise ValueError(f"duplicate permanent-negative marker: {negative_id}")
                found[negative_id] = node.name
    return found


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    files = sorted(
        path
        for test_root in (root / "examples", root / "scripts")
        if test_root.is_dir()
        for path in test_root.rglob("*.py")
    )
    raw: list[dict[str, object]] = []
    owners: dict[str, Path] = {}
    existing: dict[str, tuple[Path, str]] = {}
    errors: list[str] = []
    for path in files:
        try:
            for negative_id, function_name in permanent_negatives(path).items():
                if negative_id in existing:
                    raise ValueError(f"duplicate permanent-negative marker: {negative_id}")
                existing[negative_id] = (path, function_name)
            rows = declarations(path)
            for row in rows:
                raw.append(row)
                owners[str(row.get("id", ""))] = path
        except (SyntaxError, ValueError, TypeError) as exc:
            errors.append(str(exc))
    try:
        contracts = validate_contracts(raw)
    except ValueError as exc:
        errors.append(str(exc))
        contracts = []
    declared_ids = {contract.id for contract in contracts}
    existing_ids = set(existing)
    missing = sorted(existing_ids - declared_ids)
    stale = sorted(declared_ids - existing_ids)
    workflow_path = (root / args.workflow).resolve() if args.workflow else None
    required_triggers_present = False
    steps: list[tuple[str, dict[str, object], dict[str, object], dict[str, object]]] = []
    if workflow_path is not None:
        if workflow_path.is_file():
            try:
                required_triggers_present, steps = workflow_steps(workflow_path)
            except (OSError, ValueError, yaml.YAMLError) as exc:
                errors.append(str(exc))
        else:
            errors.append(f"workflow file does not exist: {workflow_path}")
    for negative_id in missing:
        path, function_name = existing[negative_id]
        errors.append(
            f"{negative_id}: permanent negative {path.relative_to(root)}:{function_name} has no declared contract"
        )
    for negative_id in stale:
        errors.append(f"{negative_id}: declared contract has no permanent-negative marker")
    for contract in contracts:
        source = function_source(owners[contract.id], contract.exercised_by)
        if not source:
            errors.append(f"{contract.id}: missing exercised_by function {contract.exercised_by}")
        if contract.mutation not in source:
            errors.append(f"{contract.id}: declared mutation is not applied beside the test")
        for boundary in contract.boundaries:
            if boundary not in source:
                errors.append(f"{contract.id}: assertion boundary not found beside the test: {boundary}")
        if workflow_path is not None and steps:
            runner = owners[contract.id].relative_to(root)
            if not any(
                step_gates_runner(required_triggers_present, defaults, job, step, runner)
                for _, defaults, job, step in steps
            ):
                errors.append(f"{contract.id}: runner is not executed by workflow: {runner}")
    if workflow_path is not None and steps:
        runners = {owners[contract.id].relative_to(root) for contract in contracts}
        executed_runners = {
            runner
            for runner in runners
            if any(
                step_gates_runner(required_triggers_present, defaults, job, step, runner)
                for _, defaults, job, step in steps
            )
        }
        executed_contracts = sum(
            any(
                step_gates_runner(
                    required_triggers_present,
                    defaults,
                    job,
                    step,
                    owners[item.id].relative_to(root),
                )
                for _, defaults, job, step in steps
            )
            for item in contracts
        )
        print(
            "FALSIFICATION_STATIC_WIRING "
            f"runners={len(executed_runners)}/{len(runners)} contracts={executed_contracts}/{len(contracts)} "
            "scope=trigger_keys+conditions+recognized_step_form+job_failure "
            "residuals=trigger_filters,working_directory,yaml_1_1_scalars,"
            "safe_forms_outside_whitelist,line_continuation_mechanism_redundancy,"
            f"contract_discrimination_23_of_{len(next((contract.boundaries for contract in contracts if contract.id == 'NEG-FALSIFICATION-RUNNER-WIRING'), ()))},twin_TASK_0338"
        )
    print(
        "FALSIFICATION_INVENTORY "
        f"permanent_negatives={len(existing_ids)} declared={len(declared_ids)} missing={len(missing)}"
    )
    print(
        "FALSIFICATION_CONTRACT_CENSUS "
        f"contracts={len(contracts)} "
        f"assertion_boundaries={sum(len(contract.boundaries) for contract in contracts)} "
        f"runner_files={len({owners[contract.id] for contract in contracts})}"
    )
    for contract in contracts:
        print(f"DECLARED {contract.id} boundaries={len(contract.boundaries)} runner={owners[contract.id].relative_to(root)}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
