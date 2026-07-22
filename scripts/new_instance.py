#!/usr/bin/env python3
"""Create a new instance of the multi-agent project protocol.

The script uses only the Python standard library and treats ``*.template.*`` files
as the source of canonical instance files.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import date
from pathlib import Path
from typing import Any


PLACEHOLDER_RE = re.compile(r"\{\{([A-Z0-9_]+)\}\}")

# Encapsulated instance layout (model 2.A): for the attested tier the governance
# instance (methodology "Aegis") lives in a constant subfolder of the product repo,
# so a product keeps a single git and its root stays product-only. The folder name
# is constant across products (new_instance.py / CI / harness always target it) while
# the instance identity (agent_registry / config) carries the product-specific name.
GOVERNANCE_DIR_DEFAULT = "Aegis"

GOVERNANCE_CLAUDE_MD = """# CLAUDE.md - Governance layer (Aegis)

> This folder is the **governance / methodology layer** ("Aegis") for the product in the
> parent repository. It is intentionally isolated from the product's own `.claude` and
> `CLAUDE.md`: Claude Code roots at the working directory, so launch governance sessions
> with the working directory set to THIS folder to load only the governance configuration
> (settings, hooks, skills). Product-dev sessions run from the repo root and never load
> this folder's config.
>
> The source of truth for the governance contract is AGENTS.md in this folder.

@AGENTS.md
"""

# Neutral, read-only governance starter permissions. The one-time Claude Code "trust"
# dialog per folder still applies before these take effect; the instance customizes.
GOVERNANCE_CLAUDE_SETTINGS = {
    "permissions": {
        "allow": [
            "Bash(python scripts/validate_collaboration_state.py:*)",
            "Bash(python scripts/scan_encoding.py:*)",
            "Bash(python scripts/scan_domain_neutrality.py:*)",
        ],
        "deny": [],
    }
}

CANONICAL_TEMPLATE_FILES = {
    "AGENTS.template.md": "AGENTS.md",
    "protocol.config.template.json": "protocol.config.json",
    "Area_comun/README.template.md": "Area_comun/README.md",
    "Area_comun/state/PROJECT_STATE.template.json": "Area_comun/state/PROJECT_STATE.json",
    "Area_comun/state/TASK_INDEX.template.json": "Area_comun/state/TASK_INDEX.json",
    "Area_comun/state/CLAIMS.template.json": "Area_comun/state/CLAIMS.json",
}

# Operational layer shipped with instances (DECISION-0096): the generic peer runner +
# neutral role prompts, and the methodology skills masters for the governance .claude.
# Runtime tokens inside these files use @@...@@ (never {{...}}: reserved by the renderer).
HARNESS_SOURCE_DIR = "scripts/harness"
CLAUDE_SKILLS_SOURCE_DIR = "scripts/instance_assets/claude-skills"

GATE_SCRIPT_FILES = [
    "check_commit_trailers.py",
    "validate_collaboration_state.py",
    "validate_collaboration_state.ps1",
    "scan_encoding.py",
    "scan_encoding.ps1",
    "scan_domain_neutrality.py",
    "scan_domain_neutrality.ps1",
    "measure_context_cost.py",
    "prune_state.py",
    "prune_state.ps1",
    "generate_human_guide.py",
    "keygen_agent.py",
]

COPIED_DIRS = [
    ".githooks",
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
    "skills",
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

      - name: Verify pinned pre-commit hook
        shell: bash
        run: |
          test -f .githooks/pre-commit
          echo "739d9eadf7c8c2b692cc8a87a4938729ba1ad9ff6063b14f2846ba01a210704e  .githooks/pre-commit" | sha256sum --check --strict

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
        shell: bash
        run: |
          if ! python scripts/prune_state.py --root . --check; then
            echo "ERROR: protocol state pruning is overdue. Run the coordinated Architect checkpoint and commit its governed result before integration." >&2
            exit 1
          fi

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
    parser.add_argument("--analyst", required=True, help="Independent analyst/checker participant.")
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
        choices=("coordination", "runtime", "attested"),
        default="coordination",
        help="Adoption tier for the generated instance. Default: coordination.",
    )
    parser.add_argument(
        "--roster",
        default=None,
        help=(
            "JSON file for attested tier. Shape: "
            "{\"agents\":[{\"id\":\"agent-a\",\"role\":\"architect\",\"tier\":\"signer\","
            "\"llm_preset\":\"default\"}]}"
        ),
    )
    parser.add_argument(
        "--scratch-root",
        default=None,
        help=(
            "Single scratch root the instance declares at birth for ALL its temporary work "
            "(validation clones, staging, independent crons). Must live OUTSIDE the instance "
            "tree, under the per-disk umbrella (default: <target drive>/Aegis_Scratch/"
            "<project_name>/ on Windows, ~/Aegis_Scratch/<project_name>/ elsewhere). "
            "Ad-hoc work dirs at the disk root are forbidden by policy."
        ),
    )
    parser.add_argument(
        "--governance-dir",
        default=GOVERNANCE_DIR_DEFAULT,
        help=(
            "For the attested tier, encapsulate the governance instance in this constant "
            "subfolder of the product repo (default: Aegis) so the product keeps a single "
            "git with a product-only root. Pass '.' to keep the legacy root layout."
        ),
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


def copy_peer_harness(source: Path, target: Path) -> None:
    """Ship the operational layer: the generic peer runner + neutral role prompts.

    Instances must be born OPERATIONAL, not only validatable: without the harness every
    adopter had to hand-copy the hub's per-peer cron scripts (instancing gap, DECISION-0096).
    Runtime state (.protocol-tmp/) is intentionally NOT shipped -- the runner creates it on
    first run.
    """
    source_dir = source / HARNESS_SOURCE_DIR
    if not source_dir.exists():
        raise FileNotFoundError(f"Missing harness directory: {source_dir}")
    target_dir = target / HARNESS_SOURCE_DIR
    if target_dir.exists():
        shutil.rmtree(target_dir)
    shutil.copytree(source_dir, target_dir)


def write_runtime_ci_workflow(target: Path, working_dir: str | None = None) -> None:
    workflow = RUNTIME_TIER_WORKFLOW
    if working_dir:
        # Encapsulated instance: the governance gates live in the subfolder; run all
        # steps from there. The CI file itself must stay at the repo root (.github/).
        anchor = "    runs-on: ubuntu-latest\n"
        defaults_block = (
            anchor
            + f'    # Governance (methodology "Aegis") is encapsulated in {working_dir}/.\n'
            + "    defaults:\n      run:\n"
            + f"        working-directory: {working_dir}\n"
        )
        workflow = workflow.replace(anchor, defaults_block, 1)
    workflow_path = target / ".github" / "workflows" / "validate.yml"
    workflow_path.parent.mkdir(parents=True, exist_ok=True)
    workflow_path.write_text(workflow, encoding="utf-8")


def copy_runtime_tier_files(source: Path, repo_root: Path, gov: Path, *, working_dir: str | None = None) -> None:
    copy_runtime_dir(source, gov)
    copy_gate_scripts(source, gov)
    copy_peer_harness(source, gov)
    write_runtime_ci_workflow(repo_root, working_dir)


def write_root_gitattributes(target: Path, governance_dir: str) -> None:
    """Scope LF byte-stability to the encapsulated governance subtree at the repo root."""
    block = [
        "",
        "# --- governance protocol (LF byte-stable, platform-independent) ---",
        f'# The governance instance (methodology "Aegis") is encapsulated in {governance_dir}/.',
        f"{governance_dir}/protocol.config.json text eol=lf",
        f"{governance_dir}/event-state.runtime.json text eol=lf",
        f"{governance_dir}/AGENTS.md text eol=lf",
        f"{governance_dir}/Area_comun/** text eol=lf",
        f"{governance_dir}/runtime/** text eol=lf",
        f"{governance_dir}/scripts/** text eol=lf",
        f"{governance_dir}/skills/** text eol=lf",
        "",
    ]
    path = target / ".gitattributes"
    prefix = ""
    if path.exists():
        existing = path.read_text(encoding="utf-8-sig").rstrip()
        if existing:
            prefix = existing + "\n"
    path.write_text(prefix + "\n".join(block).lstrip("\n"), encoding="utf-8")


def reset_commit_trailers(gov: Path) -> None:
    """A fresh instance must not inherit the hub's LIVE commit-trailer gate state (its
    enabled flag + hub-specific start_commit + rationale). Reset to a neutral disabled
    gate so the instance is born validatable; it activates its own gate once its harness
    emits trailers (mirrors the "COMMIT_TRAILERS off baseline" practice for real instances)."""
    path = gov / "Area_comun" / "protocol" / "COMMIT_TRAILERS.json"
    if not path.exists():
        return
    path.write_text(
        json.dumps(
            {
                "enabled": False,
                "start_commit": "",
                "enforcement": "post_start_governed_commits_require_task_id_trailer",
                "rationale": "Disabled at instantiation; activate after the instance harness emits trailers.",
            },
            indent=2,
            ensure_ascii=True,
        )
        + "\n",
        encoding="utf-8",
    )


def scaffold_governance_claude(source: Path, gov: Path) -> None:
    """Governance-scoped .claude (settings + methodology skills) + CLAUDE.md.

    Claude Code roots at the working directory: a governance session launched with cwd
    set to gov loads only gov/.claude and gov/CLAUDE.md; a product-dev session at the
    repo root never loads them (they are below its root). Bidirectional isolation.

    Ships the neutralized methodology skills masters (DECISION-0096, closing the
    DECISION-0061 wiring gap) so the instance coordinator inherits the operational
    procedures (monitor/watchdogs, cron lifecycle, mailbox hygiene, state checkpoint)
    without hand-copying them from the hub.
    """
    claude_dir = gov / ".claude"
    claude_dir.mkdir(parents=True, exist_ok=True)
    (claude_dir / "settings.json").write_text(
        json.dumps(GOVERNANCE_CLAUDE_SETTINGS, indent=2, ensure_ascii=True) + "\n",
        encoding="utf-8",
    )
    (gov / "CLAUDE.md").write_text(GOVERNANCE_CLAUDE_MD, encoding="utf-8")
    skills_source = source / CLAUDE_SKILLS_SOURCE_DIR
    if not skills_source.exists():
        raise FileNotFoundError(f"Missing claude skills masters: {skills_source}")
    skills_target = claude_dir / "skills"
    for skill_dir in sorted(p for p in skills_source.iterdir() if p.is_dir()):
        destination = skills_target / skill_dir.name
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(skill_dir, destination)


def ensure_protocol_secrets_gitignored(target: Path) -> None:
    gitignore = target / ".gitignore"
    lines = []
    if gitignore.exists():
        lines = gitignore.read_text(encoding="utf-8-sig").splitlines()
    required = ["protocol-secrets/", ".protocol-secrets/", "Aegis_Scratch/", ".protocol-tmp/"]
    changed = False
    for item in required:
        if item not in lines:
            lines.append(item)
            changed = True
    if changed or not gitignore.exists():
        gitignore.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def load_roster(args: argparse.Namespace) -> list[dict[str, str]]:
    if args.roster:
        payload = read_json(Path(args.roster))
        agents = payload.get("agents") if isinstance(payload, dict) else None
    else:
        agents = [
            {"id": args.architect, "role": "architect", "tier": "signer", "llm_preset": "architect"},
            {"id": args.implementer, "role": "implementer", "tier": "signer", "llm_preset": "implementer"},
            {"id": args.analyst, "role": "analyst", "tier": "signer", "llm_preset": "analyst"},
            {"id": args.human_owner, "role": "human_owner", "tier": "worker", "llm_preset": "human"},
        ]
    if not isinstance(agents, list) or not agents:
        raise ValueError("attested tier roster requires a non-empty agents list")
    normalized: list[dict[str, str]] = []
    seen: set[str] = set()
    for item in agents:
        if not isinstance(item, dict):
            raise ValueError("each roster agent must be an object")
        agent_id = str(item.get("id") or "").strip()
        role = str(item.get("role") or "worker").strip()
        tier = str(item.get("tier") or "").strip().lower()
        llm_preset = str(item.get("llm_preset") or "").strip()
        if not agent_id:
            raise ValueError("each roster agent requires id")
        if tier not in {"signer", "worker"}:
            raise ValueError(f"roster agent {agent_id} tier must be signer or worker")
        if not llm_preset:
            raise ValueError(f"roster agent {agent_id} requires llm_preset")
        if agent_id in seen:
            raise ValueError(f"duplicate roster agent id: {agent_id}")
        seen.add(agent_id)
        normalized.append({"id": agent_id, "role": role, "tier": tier, "llm_preset": llm_preset})
    return normalized


def read_instance_config(target: Path) -> dict[str, Any]:
    config = read_json(target / "protocol.config.json")
    if not isinstance(config, dict):
        raise ValueError("generated protocol.config.json is not an object")
    return config


def write_instance_config(target: Path, config: dict[str, Any]) -> None:
    (target / "protocol.config.json").write_text(
        json.dumps(config, indent=2, ensure_ascii=True, sort_keys=False) + "\n",
        encoding="utf-8",
    )


def signer_keyid(agent_id: str) -> str:
    return f"{slug_for_config(agent_id)}:v1"


def slug_for_config(value: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "-" for ch in value.strip())
    cleaned = "-".join(part for part in cleaned.split("-") if part)
    if not cleaned:
        raise ValueError("agent id must contain at least one alphanumeric character")
    return cleaned


def run_keygen(target: Path, source: Path, agent_id: str) -> dict[str, Any]:
    keyid = signer_keyid(agent_id)
    cmd = [
        sys.executable,
        str(target / "scripts" / "keygen_agent.py"),
        "--root",
        str(target),
        "--agent-id",
        agent_id,
        "--keyid",
        keyid,
        "--output",
        "-",
    ]
    result = subprocess.run(cmd, cwd=str(target), text=True, capture_output=True, check=False)
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or f"keygen failed for {agent_id}")
    try:
        return json.loads(result.stdout)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"keygen returned invalid JSON for {agent_id}") from exc


def write_attested_override(target: Path, signers: dict[str, dict[str, Any]], *, actor_auth_enforce: bool) -> None:
    keyids = {agent_id: info["keyid"] for agent_id, info in sorted(signers.items())}
    private_key_files = {agent_id: info["private_key_file"] for agent_id, info in sorted(signers.items())}
    event_auth_keys = {agent_id: info["event_auth"] for agent_id, info in sorted(signers.items())}
    override = {
        "event_state": {
            "actor_auth_enforce": actor_auth_enforce,
            "actor_auth_config": {
                "secret_root": "protocol-secrets",
                "keyids": keyids,
                "private_key_files": private_key_files,
            },
            "event_auth": {"keys": event_auth_keys},
        }
    }
    (target / "event-state.runtime.json").write_text(
        json.dumps(override, indent=2, ensure_ascii=True, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def apply_attested_config(target: Path, roster: list[dict[str, str]], signers: dict[str, dict[str, Any]]) -> None:
    config = read_instance_config(target)
    runtime = config.setdefault("runtime", {})
    runtime["enabled"] = True
    presets = runtime.setdefault("llm_cli_presets", {})
    for agent in roster:
        preset = agent["llm_preset"]
        presets.setdefault(preset, {"command": preset})

    # Keep the generated instance validator-compatible without changing the hub validator:
    # attested is a ceremony on top of the existing runtime tier.
    config["adoption_tier"] = "runtime"
    config["agent_registry"] = {
        "enabled": True,
        "routing_policy": "weighted_least_loaded_deterministic",
        "agents": [
            {
                "id": agent["id"],
                "role": agent["role"],
                "tier": agent["tier"],
                "llm_preset": agent["llm_preset"],
                "adapter": "human" if agent["role"] == "human_owner" else "llm",
                "enabled": True,
                "capabilities": ["human_owner"] if agent["role"] == "human_owner" else (
                    ["orchestrator", "reviewer"] if agent["role"] == "architect" else ["implementer"]
                ),
            }
            for agent in roster
        ],
    }
    event_auth = config.setdefault("event_auth", {})
    event_auth.update({"enabled": True, "method": "hmac-sha256", "issuer": "local-runtime", "audience": "runtime-event-log"})
    secret_dirs = event_auth.setdefault("secret_dirs", [])
    if "protocol-secrets" not in secret_dirs:
        secret_dirs.append("protocol-secrets")
    event_state = config.setdefault("event_state", {})
    event_state.update(
        {
            "enabled": True,
            "materialize": True,
            "enforce": False,
            "authoritative": False,
            "chain_enabled": True,
            "agent_signatures_enabled": True,
            "signature_backend": "local-ed25519",
        }
    )
    signature_config = event_state.setdefault("signature_config", {})
    signature_config["backend"] = "local-ed25519"
    signature_config["public_keys"] = {info["keyid"]: info["public_key"] for info in signers.values()}
    config["attested_instancing"] = {
        "enabled": True,
        "provenance_metadata": {
            "author_agent": "real worker or signer id responsible for the produced work",
            "model": "runtime LLM/model preset used for the produced work",
            "submitted_by": "signer id that attests and submits the ledger event",
        },
        "roster": roster,
    }
    write_instance_config(target, config)


def create_roster_personal_areas(target: Path, roster: list[dict[str, str]]) -> None:
    for agent in roster:
        area = target / "personal" / agent["id"]
        area.mkdir(parents=True, exist_ok=True)
        (area / ".gitkeep").write_text("\n", encoding="utf-8")
        (area / "LLM_PRESET.md").write_text(
            f"# LLM preset\n\n- agent_id: {agent['id']}\n- llm_preset: {agent['llm_preset']}\n",
            encoding="utf-8",
        )


def run_regenesis_for_attested_instance(target: Path, signer_id: str) -> None:
    # Sign the genesis boundary, then return the final override to off-by-default.
    result = subprocess.run(
        [
            sys.executable,
            str(target / "runtime" / "regenesis.py"),
            "--root",
            str(target),
            "--actor-id",
            signer_id,
            "--timestamp",
            "1970-01-01T00:00:00Z",
            "--commit",
            "attested-instance-genesis",
            "--idempotency-key",
            "attested-instance:genesis",
            "--output",
            "-",
        ],
        cwd=str(target),
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "attested instance regenesis failed")


def configure_attested_instance(
    source: Path, repo_root: Path, gov: Path, args: argparse.Namespace, *, working_dir: str | None = None
) -> None:
    copy_runtime_tier_files(source, repo_root, gov, working_dir=working_dir)
    ensure_protocol_secrets_gitignored(repo_root)
    roster = load_roster(args)
    signer_ids = [agent["id"] for agent in roster if agent["tier"] == "signer"]
    if not signer_ids:
        raise ValueError("attested tier requires at least one signer")
    signers = {agent_id: run_keygen(gov, source, agent_id) for agent_id in signer_ids}
    apply_attested_config(gov, roster, signers)
    create_roster_personal_areas(gov, roster)
    write_attested_override(gov, signers, actor_auth_enforce=True)
    run_regenesis_for_attested_instance(gov, signer_ids[0])
    write_attested_override(gov, signers, actor_auth_enforce=False)


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


def resolve_scratch_root(args: argparse.Namespace) -> str:
    """Scratch-root policy (DECISION-0098): one scratch root per project, declared at birth,
    outside the tree. Default umbrella: <drive of target>/Aegis_Scratch/<project_name>/ on
    Windows, ~/Aegis_Scratch/<project_name>/ elsewhere. Forward slashes for cross-platform
    configs. A user-provided value is validated at birth (born validatable): it must be
    absolute (host-independent shapes: X:/, / or \\, ~) and must not point inside the target.
    """
    if args.scratch_root:
        value = str(args.scratch_root).replace("\\", "/")
        if not (re.match(r"^[A-Za-z]:/", value) or value.startswith(("/", "~"))):
            raise ValueError(
                f"--scratch-root must be an absolute path outside the instance tree, got: {value}"
            )
        try:
            target_abs = Path(args.target).resolve()
            Path(value).expanduser().resolve().relative_to(target_abs)
        except (ValueError, RuntimeError, OSError):
            return value
        raise ValueError(
            f"--scratch-root must live OUTSIDE the instance tree, got: {value} inside {args.target}"
        )
    project = args.project_name
    if os.name == "nt":
        drive = Path(args.target).resolve().drive or "C:"
        return f"{drive}/Aegis_Scratch/{project}/"
    return f"~/Aegis_Scratch/{project}/"


def build_replacements(args: argparse.Namespace, source: Path) -> dict[str, str]:
    today = date.today().isoformat()
    protocol_version = args.protocol_version or discover_protocol_version(source)
    maintainer = args.maintainer or f"{args.architect} + {args.human_owner}"
    updated_by = args.updated_by or args.architect
    agent_roles = (
        f"- `{args.architect}`: Architect / orchestrator.\n"
        f"- `{args.implementer}`: Implementation specialist.\n"
        f"- `{args.analyst}`: Independent analyst / checker.\n"
        f"- `{args.human_owner}`: Human owner."
    )
    return {
        "PROJECT_NAME": args.project_name,
        "ADOPTION_TIER": args.tier,
        "SCRATCH_ROOT": resolve_scratch_root(args),
        "PROJECT_GOAL": args.project_goal,
        "PROJECT_DESCRIPTION": args.project_description,
        "PHASE_ID": args.phase_id,
        "PHASE_NAME": args.phase_name,
        "PHASE_GOAL": args.phase_goal,
        "AGENT_ARCHITECT": args.architect,
        "AGENT_IMPLEMENTER": args.implementer,
        "AGENT_ANALYST": args.analyst,
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
    participants = [args.architect, args.implementer, args.analyst, args.human_owner]
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
        # Encapsulation (model 2.A) applies to the attested tier: governance content goes
        # into target/<governance_dir>/ so the product keeps one git with a product-only
        # root. Other tiers keep the legacy root layout (gov == target).
        governance_dir = (args.governance_dir or "").strip()
        encapsulate = args.tier == "attested" and governance_dir not in ("", ".")
        gov = (target / governance_dir) if encapsulate else target
        if encapsulate:
            gov.mkdir(parents=True, exist_ok=True)
        replacements = build_replacements(args, source)
        copy_support_dirs(source, gov)
        reset_commit_trailers(gov)
        render_templates(source, gov, replacements)
        render_remaining_files(gov, replacements)
        create_personal_areas(gov, args)
        # Every tier ships the local hook, so every tier also needs its gate scripts.
        copy_gate_scripts(source, gov)
        # The Python validator imports the neutral runtime replay/event modules even
        # when event state is disabled, so coordination instances need the library.
        copy_runtime_dir(source, gov)
        ensure_protocol_secrets_gitignored(target)
        if args.tier == "runtime":
            copy_runtime_tier_files(source, target, gov)
        elif args.tier == "attested":
            configure_attested_instance(
                source, target, gov, args, working_dir=(governance_dir if encapsulate else None)
            )
        if encapsulate:
            write_root_gitattributes(target, governance_dir)
            scaffold_governance_claude(source, gov)
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
    print("Enable the validation hook in this clone: git config core.hooksPath .githooks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
