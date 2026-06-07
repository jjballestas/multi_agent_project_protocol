#!/usr/bin/env python3
"""Create a new instance of the multi-agent project protocol.

The script uses only the Python standard library and treats ``*.template.*`` files
as the source of canonical instance files.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import date
from pathlib import Path


PLACEHOLDER_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")

CANONICAL_TEMPLATE_FILES = {
    "AGENTS.template.md": "AGENTS.md",
    "protocol.config.template.json": "protocol.config.json",
    "Area_comun/README.template.md": "Area_comun/README.md",
    "Area_comun/state/PROJECT_STATE.template.json": "Area_comun/state/PROJECT_STATE.json",
    "Area_comun/state/TASK_INDEX.template.json": "Area_comun/state/TASK_INDEX.json",
    "Area_comun/state/CLAIMS.template.json": "Area_comun/state/CLAIMS.json",
}

GATE_SCRIPT_FILES = [
    "validate_collaboration_state.py",
    "validate_collaboration_state.ps1",
    "scan_encoding.py",
    "scan_encoding.ps1",
    "scan_domain_neutrality.py",
    "scan_domain_neutrality.ps1",
    "measure_context_cost.py",
    "prune_state.py",
    "prune_state.ps1",
]

COPIED_DIRS = [
    "Area_comun/protocol",
    "Area_comun/mailbox/open",
    "Area_comun/mailbox/answered",
    "Area_comun/mailbox/archived",
    "Area_comun/tasks",
    "Area_comun/handoffs",
    "Area_comun/reports",
    "Area_comun/artifacts",
    "Area_comun/contracts",
    "Area_comun/decisions",
]

RUNTIME_TIER_WORKFLOW = """name: Validate protocol instance

on:
  push:
  pull_request:

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.x"

      - name: Compile distributed Python modules
        run: python -m compileall runtime scripts

      - name: Validate protocol state
        run: python scripts/validate_collaboration_state.py --root .

      - name: Validate protocol state with PowerShell
        shell: pwsh
        run: ./scripts/validate_collaboration_state.ps1 -Root .

      - name: Scan encoding
        run: python scripts/scan_encoding.py --root .

      - name: Scan encoding with PowerShell
        shell: pwsh
        run: ./scripts/scan_encoding.ps1 -Root .

      - name: Check systematic state pruning
        run: python scripts/prune_state.py --root . --check

      - name: Scan domain neutrality
        run: python scripts/scan_domain_neutrality.py --root .

      - name: Scan domain neutrality with PowerShell
        shell: pwsh
        run: ./scripts/scan_domain_neutrality.ps1 -Root .
"""


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Instantiate a project from the multi-agent protocol templates."
    )
    parser.add_argument("--source-template", required=True, help="Path to the protocol template root")
    parser.add_argument("--target", required=True, help="Directory where the new instance is created")
    parser.add_argument("--project-name", required=True)
    parser.add_argument("--project-goal", required=True)
    parser.add_argument("--project-description", required=True)
    parser.add_argument("--architect", required=True)
    parser.add_argument("--implementer", required=True)
    parser.add_argument("--human-owner", required=True)
    parser.add_argument("--phase-id", required=True)
    parser.add_argument("--phase-name", required=True)
    parser.add_argument("--phase-goal", required=True)
    parser.add_argument("--protocol-version", default=None)
    parser.add_argument("--in-scope", default="Project-specific work declared by the instance.")
    parser.add_argument("--out-of-scope", default="Work not explicitly approved for this instance.")
    parser.add_argument(
        "--domain-critical-boundaries",
        default="No secrets committed. Project-specific critical boundaries must be recorded here.",
    )
    parser.add_argument(
        "--stack-decisions",
        default="No stack-specific decisions declared yet. Record decisions in Area_comun/decisions/.",
    )
    parser.add_argument(
        "--quality-gates",
        default="Run the collaboration state validator before handoff or review.",
    )
    parser.add_argument(
        "--human-approval-points",
        default="Critical boundary changes and release decisions require human owner approval.",
    )
    parser.add_argument("--phase-exit-criteria", default="Initial protocol instance is valid.")
    parser.add_argument("--repo-map", default="Complete this section with the instance repository map.")
    parser.add_argument("--project-code-or-docs", default="project_code_or_docs/")
    parser.add_argument("--maintainer", default=None)
    parser.add_argument("--updated-by", default=None)
    parser.add_argument(
        "--force",
        action="store_true",
        help="Allow writing into an existing non-empty target directory.",
    )
    parser.add_argument(
        "--tier",
        choices=("coordination", "runtime"),
        default="coordination",
        help="Adoption tier for the generated instance. Default: coordination.",
    )
    return parser.parse_args()


def read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception:
        return {}


def discover_protocol_version(source: Path) -> str:
    config = read_json(source / "protocol.config.json")
    if isinstance(config.get("protocol_version"), str):
        return config["protocol_version"]
    state = read_json(source / "Area_comun" / "state" / "PROJECT_STATE.json")
    if isinstance(state.get("version"), str):
        return state["version"]
    return "0.1.0"


def ensure_target(target: Path, force: bool) -> None:
    if target.exists():
        if not target.is_dir():
            raise ValueError(f"Target exists and is not a directory: {target}")
        if any(target.iterdir()) and not force:
            raise ValueError(f"Target directory is not empty: {target}. Use --force to overwrite.")
        if force:
            for child in target.iterdir():
                if child.is_dir():
                    shutil.rmtree(child)
                else:
                    child.unlink()
    target.mkdir(parents=True, exist_ok=True)


def copy_support_dirs(source: Path, target: Path) -> None:
    for relative in COPIED_DIRS:
        source_dir = source / relative
        target_dir = target / relative
        target_dir.mkdir(parents=True, exist_ok=True)
        if not source_dir.exists():
            continue

        if relative in {
            "Area_comun/mailbox/open",
            "Area_comun/mailbox/answered",
            "Area_comun/mailbox/archived",
            "Area_comun/tasks",
            "Area_comun/handoffs",
            "Area_comun/artifacts",
            "Area_comun/contracts",
            "Area_comun/decisions",
        }:
            copy_gitkeep(source_dir, target_dir)
            continue

        if relative == "Area_comun/reports":
            copy_gitkeep(source_dir, target_dir)
            template = source_dir / "HUMAN_REPORT_TEMPLATE.md"
            if template.exists():
                shutil.copy2(template, target_dir / template.name)
            continue

        for item in source_dir.iterdir():
            destination = target_dir / item.name
            if item.is_dir():
                if destination.exists():
                    shutil.rmtree(destination)
                shutil.copytree(item, destination)
            elif not item.name.endswith(".template.json") and not item.name.endswith(".template.md"):
                shutil.copy2(item, destination)
            elif relative not in ("Area_comun/state",):
                shutil.copy2(item, destination)


def copy_gitkeep(source_dir: Path, target_dir: Path) -> None:
    gitkeep = source_dir / ".gitkeep"
    if gitkeep.exists():
        shutil.copy2(gitkeep, target_dir / ".gitkeep")
    else:
        (target_dir / ".gitkeep").write_text("\n", encoding="utf-8")


def copy_runtime_dir(source: Path, target: Path) -> None:
    source_dir = source / "runtime"
    if not source_dir.exists():
        raise FileNotFoundError(f"Missing runtime directory: {source_dir}")
    target_dir = target / "runtime"
    if target_dir.exists():
        shutil.rmtree(target_dir)

    def ignore_artifacts(current: str, names: list[str]) -> set[str]:
        current_path = Path(current)
        ignored: set[str] = set()
        for name in names:
            candidate = current_path / name
            try:
                relative_parts = candidate.relative_to(source_dir).parts
            except ValueError:
                continue
            if "__pycache__" in relative_parts:
                ignored.add(name)
            elif len(relative_parts) == 1 and relative_parts[0] in {"state", "runs"}:
                ignored.add(name)
        return ignored

    shutil.copytree(source_dir, target_dir, ignore=ignore_artifacts)


def copy_gate_scripts(source: Path, target: Path) -> None:
    target_scripts = target / "scripts"
    target_scripts.mkdir(parents=True, exist_ok=True)
    for filename in GATE_SCRIPT_FILES:
        source_file = source / "scripts" / filename
        if not source_file.exists():
            raise FileNotFoundError(f"Missing gate script: {source_file}")
        shutil.copy2(source_file, target_scripts / filename)


def write_runtime_ci_workflow(target: Path) -> None:
    workflow_path = target / ".github" / "workflows" / "validate.yml"
    workflow_path.parent.mkdir(parents=True, exist_ok=True)
    workflow_path.write_text(RUNTIME_TIER_WORKFLOW, encoding="utf-8")


def copy_runtime_tier_files(source: Path, target: Path) -> None:
    copy_runtime_dir(source, target)
    copy_gate_scripts(source, target)
    write_runtime_ci_workflow(target)


def render_text(text: str, replacements: dict[str, str], source_path: Path) -> str:
    missing = sorted({match.group(1) for match in PLACEHOLDER_RE.finditer(text)} - replacements.keys())
    if missing:
        raise ValueError(f"Missing replacements for {source_path}: {', '.join(missing)}")

    def replace(match: re.Match[str]) -> str:
        return replacements[match.group(1)]

    return PLACEHOLDER_RE.sub(replace, text)


def render_templates(source: Path, target: Path, replacements: dict[str, str]) -> None:
    for source_relative, target_relative in CANONICAL_TEMPLATE_FILES.items():
        source_path = source / source_relative
        if not source_path.exists():
            raise FileNotFoundError(f"Missing template file: {source_path}")
        rendered = render_text(source_path.read_text(encoding="utf-8-sig"), replacements, source_path)
        target_path = target / target_relative
        target_path.parent.mkdir(parents=True, exist_ok=True)
        target_path.write_text(rendered, encoding="utf-8")


def render_remaining_files(target: Path, replacements: dict[str, str]) -> None:
    for path in target.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            continue
        if "{{" not in text:
            continue
        rendered = render_text(text, replacements, path)
        path.write_text(rendered, encoding="utf-8")


def find_unresolved_placeholders(target: Path) -> list[str]:
    unresolved: list[str] = []
    for path in target.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            continue
        if PLACEHOLDER_RE.search(text):
            unresolved.append(str(path.relative_to(target)))
    return unresolved


def build_replacements(args: argparse.Namespace, source: Path) -> dict[str, str]:
    today = date.today().isoformat()
    protocol_version = args.protocol_version or discover_protocol_version(source)
    maintainer = args.maintainer or f"{args.architect} + {args.human_owner}"
    updated_by = args.updated_by or args.architect
    agent_roles = (
        f"- `{args.architect}`: Architect / orchestrator.\n"
        f"- `{args.implementer}`: Implementation specialist.\n"
        f"- `{args.human_owner}`: Human owner."
    )
    return {
        "PROJECT_NAME": args.project_name,
        "ADOPTION_TIER": args.tier,
        "PROJECT_GOAL": args.project_goal,
        "PROJECT_DESCRIPTION": args.project_description,
        "PHASE_ID": args.phase_id,
        "PHASE_NAME": args.phase_name,
        "PHASE_GOAL": args.phase_goal,
        "AGENT_ARCHITECT": args.architect,
        "AGENT_IMPLEMENTER": args.implementer,
        "HUMAN_OWNER": args.human_owner,
        "PROTOCOL_VERSION": protocol_version,
        "LAST_UPDATED": today,
        "CREATED_AT": today,
        "UPDATED_AT": today,
        "UPDATED_BY": updated_by,
        "MAINTAINER": maintainer,
        "IN_SCOPE": args.in_scope,
        "OUT_OF_SCOPE": args.out_of_scope,
        "AGENT_ROLES": agent_roles,
        "DOMAIN_CRITICAL_BOUNDARIES": args.domain_critical_boundaries,
        "STACK_DECISIONS": args.stack_decisions,
        "QUALITY_GATES": args.quality_gates,
        "HUMAN_APPROVAL_POINTS": args.human_approval_points,
        "PHASE_EXIT_CRITERIA": args.phase_exit_criteria,
        "REPO_MAP": args.repo_map,
        "PROJECT_CODE_OR_DOCS": args.project_code_or_docs,
    }


def create_personal_areas(target: Path, args: argparse.Namespace) -> None:
    """DECISION-0016: each registered participant gets a personal area personal/<id>/.

    Created with a .gitkeep so the directory persists in git when empty. <id> matches the
    participant identifier used in the agent registry / agents block.
    """
    participants = [args.architect, args.implementer, args.human_owner]
    seen: set[str] = set()
    for participant in participants:
        pid = str(participant).strip()
        if not pid or pid in seen:
            continue
        seen.add(pid)
        area = target / "personal" / pid
        area.mkdir(parents=True, exist_ok=True)
        keep = area / ".gitkeep"
        if not keep.exists():
            keep.write_text("\n", encoding="utf-8")


def main() -> int:
    args = parse_args()
    source = Path(args.source_template).resolve()
    target = Path(args.target).resolve()

    if not source.exists():
        print(f"ERROR: source template does not exist: {source}", file=sys.stderr)
        return 1

    try:
        ensure_target(target, args.force)
        replacements = build_replacements(args, source)
        copy_support_dirs(source, target)
        render_templates(source, target, replacements)
        render_remaining_files(target, replacements)
        create_personal_areas(target, args)
        if args.tier == "runtime":
            copy_runtime_tier_files(source, target)
        unresolved = find_unresolved_placeholders(target)
        if unresolved:
            raise ValueError(
                "Unresolved placeholders remain in generated instance: " + ", ".join(unresolved)
            )
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    print(f"OK: created protocol instance at {target}")
    print(f"Protocol version: {replacements['PROTOCOL_VERSION']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
