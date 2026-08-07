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


def workflow_commands(path: Path) -> str:
    """Return only executable ``run`` fields from a GitHub Actions workflow."""
    lines = path.read_text(encoding="utf-8-sig").splitlines()
    commands: list[str] = []
    index = 0
    while index < len(lines):
        match = re.match(r"^(\s*)(?:-\s+)?run:\s*(.*)$", lines[index])
        if not match:
            index += 1
            continue
        indent = len(match.group(1))
        value = match.group(2).strip()
        if value in {"|", ">", "|-", ">-", "|+", ">+"}:
            index += 1
            while index < len(lines):
                line = lines[index]
                if line.strip() and len(line) - len(line.lstrip()) <= indent:
                    break
                commands.append(line.strip())
                index += 1
            continue
        commands.append(value.strip("'\""))
        index += 1
    return "\n".join(commands).replace("\\", "/")


def command_executes(commands: str, relative_path: Path) -> bool:
    candidate = relative_path.as_posix()
    return re.search(rf"(?<![\w./-]){re.escape(candidate)}(?![\w./-])", commands) is not None


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
    commands = ""
    if workflow_path is not None:
        if workflow_path.is_file():
            commands = workflow_commands(workflow_path)
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
        if workflow_path is not None and commands:
            runner = owners[contract.id].relative_to(root)
            if not command_executes(commands, runner):
                errors.append(f"{contract.id}: runner is not executed by workflow: {runner}")
    if workflow_path is not None and commands:
        runners = {owners[contract.id].relative_to(root) for contract in contracts}
        executed_runners = {runner for runner in runners if command_executes(commands, runner)}
        executed_contracts = sum(command_executes(commands, owners[item.id].relative_to(root)) for item in contracts)
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
