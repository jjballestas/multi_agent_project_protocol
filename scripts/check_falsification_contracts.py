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


def shell_guarantees_abort(
    workflow_defaults: dict[str, object],
    job: dict[str, object],
    step: dict[str, object],
) -> bool:
    """Recognize GitHub shell modes that abort a multiline script on first failure."""
    shell = configured_shell(workflow_defaults, job, step)
    if shell == "bash":
        return True
    runs_on = job.get("runs-on")
    return shell is None and isinstance(runs_on, str) and runs_on.startswith(("ubuntu-", "macos-"))


def bash_block_preserves_abort(
    lines: list[str], invocation: re.Pattern[str], safe_python: re.Pattern[str]
) -> bool:
    """Accept only block lines that cannot change or intercept bash failure handling."""
    direct_invocations = [line for line in lines if invocation.fullmatch(line)]
    if len(direct_invocations) != 1:
        return False
    safe_echo = re.compile(r"echo(?:\s+[A-Za-z0-9_./: -]+)?", re.IGNORECASE)
    return all(
        invocation.fullmatch(line) or safe_echo.fullmatch(line) or safe_python.fullmatch(line)
        for line in lines
    )


def command_gates_runner(
    command: str,
    relative_path: Path,
    workflow_defaults: dict[str, object],
    job: dict[str, object],
    step: dict[str, object],
) -> bool:
    """Require one undecorated invocation, with a narrow safe multiline exception."""
    candidate = re.escape(relative_path.as_posix())
    python = r"(?:python(?:3(?:\.\d+)*)?(?:\.exe)?|py(?:\.exe)?(?:\s+-3)?)"
    invocation = re.compile(
        rf"{python}\s+(?:{candidate}|\"{candidate}\"|'{candidate}')",
        re.IGNORECASE,
    )
    safe_python = re.compile(
        rf"{python}\s+[A-Za-z0-9_./:=,-]+(?:\s+[A-Za-z0-9_./:=,-]+)*",
        re.IGNORECASE,
    )
    lines = [
        line.strip().replace("\\", "/")
        for line in command.splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    direct_invocations = [line for line in lines if invocation.fullmatch(line)]
    if len(lines) == 1:
        return len(direct_invocations) == 1
    # GitHub's bash shell starts with ``-eo pipefail``.  The multiline exception is
    # deliberately narrower than nominal shell selection: every other executable line
    # must be an inert echo or an undecorated Python process, so the block cannot change
    # parent-shell options, disable errexit, or intercept ERR.
    return shell_guarantees_abort(workflow_defaults, job, step) and bash_block_preserves_abort(
        lines, invocation, safe_python
    )


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
            "scope=trigger_keys+conditions+direct_invocation+shell_failure+job_failure "
            "residuals=trigger_filters,working_directory,yaml_1_1_scalars"
        )
    print(
        "FALSIFICATION_INVENTORY "
        f"permanent_negatives={len(existing_ids)} declared={len(declared_ids)} missing={len(missing)}"
    )
    for contract in contracts:
        print(f"DECLARED {contract.id} boundaries={len(contract.boundaries)} runner={owners[contract.id].relative_to(root)}")
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
