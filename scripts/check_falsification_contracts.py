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


def workflow_steps(path: Path) -> list[tuple[str, dict[str, object], dict[str, object]]]:
    """Return real steps nested under real workflow jobs."""
    document = yaml.safe_load(path.read_text(encoding="utf-8-sig"))
    if not isinstance(document, dict):
        raise ValueError(f"{path}: workflow must be a mapping")
    jobs = document.get("jobs")
    if not isinstance(jobs, dict):
        raise ValueError(f"{path}: workflow must define a jobs mapping")
    found: list[tuple[str, dict[str, object], dict[str, object]]] = []
    for job_id, raw_job in jobs.items():
        if not isinstance(raw_job, dict):
            continue
        steps = raw_job.get("steps")
        if not isinstance(steps, list):
            continue
        for raw_step in steps:
            if isinstance(raw_step, dict):
                found.append((str(job_id), raw_job, raw_step))
    return found


def command_invokes_runner(command: str, relative_path: Path) -> bool:
    """Recognize a direct Python invocation, not a textual mention such as echo."""
    candidate = re.escape(relative_path.as_posix())
    python = r"(?:python(?:3(?:\.\d+)*)?(?:\.exe)?|py(?:\.exe)?(?:\s+-3)?)"
    option = r"(?:\s+-[A-Za-z0-9]+)*"
    invocation = re.compile(
        rf"^\s*{python}{option}\s+[\"']?{candidate}[\"']?(?:\s|$)",
        re.IGNORECASE,
    )
    return any(invocation.search(line.replace("\\", "/")) for line in command.splitlines())


def step_gates_runner(
    job: dict[str, object], step: dict[str, object], relative_path: Path
) -> bool:
    command = step.get("run")
    if not isinstance(command, str) or not command_invokes_runner(command, relative_path):
        return False
    return job.get("continue-on-error") is not True and step.get("continue-on-error") is not True


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
    steps: list[tuple[str, dict[str, object], dict[str, object]]] = []
    if workflow_path is not None:
        if workflow_path.is_file():
            try:
                steps = workflow_steps(workflow_path)
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
            if not any(step_gates_runner(job, step, runner) for _, job, step in steps):
                errors.append(f"{contract.id}: runner is not executed by workflow: {runner}")
    if workflow_path is not None and steps:
        runners = {owners[contract.id].relative_to(root) for contract in contracts}
        executed_runners = {
            runner for runner in runners if any(step_gates_runner(job, step, runner) for _, job, step in steps)
        }
        executed_contracts = sum(
            any(step_gates_runner(job, step, owners[item.id].relative_to(root)) for _, job, step in steps)
            for item in contracts
        )
        print(
            "FALSIFICATION_EXECUTION "
            f"runners={len(executed_runners)}/{len(runners)} contracts={executed_contracts}/{len(contracts)}"
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
