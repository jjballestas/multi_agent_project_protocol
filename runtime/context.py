#!/usr/bin/env python3
"""Shared context loaders for the protocol runtime."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


PRIORITY_RANK = {"critical": 4, "high": 3, "normal": 2, "low": 1}

DEFAULT_AGENT_ROLES = {
    "architect": "architect",
    "implementer": "implementer",
    "human_owner": "human_owner",
}

ROLE_CAPABILITIES = {
    "architect": ["architect", "reviewer", "orchestrator", "qa"],
    "implementer": ["implementer", "test_engineer"],
    "human_owner": ["human_owner"],
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_json_if_exists(path: Path) -> dict[str, Any] | None:
    if not path.exists():
        return None
    return read_json(path)


def merge_by_array_field(hot: dict[str, Any], archive: dict[str, Any] | None, field: str) -> dict[str, Any]:
    merged = dict(hot)
    merged[field] = list(hot.get(field) or []) + list((archive or {}).get(field) or [])
    return merged


def parse_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    metadata: dict[str, Any] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            break
        match = re.match(r"^\s*([A-Za-z_][A-Za-z0-9_]*):\s*(.*?)\s*$", line)
        if not match:
            continue
        key, value = match.groups()
        metadata[key] = parse_scalar(value)
    return metadata


def parse_scalar(value: str) -> Any:
    value = value.strip()
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [part.strip().strip("\"'") for part in inner.split(",")]
    return value.strip("\"'")


def load_state(root: Path) -> dict[str, Any]:
    root = root.resolve()
    mailbox_open = []
    open_dir = root / "Area_comun" / "mailbox" / "open"
    if open_dir.exists():
        for path in sorted(open_dir.glob("MSG-*.md")):
            metadata = parse_frontmatter(path)
            metadata["_path"] = path.relative_to(root).as_posix()
            mailbox_open.append(metadata)

    state_dir = root / "Area_comun" / "state"
    config = read_json_if_exists(root / "protocol.config.json") or {}
    task_index = read_json(state_dir / "TASK_INDEX.json")
    claims = read_json(state_dir / "CLAIMS.json")
    task_archive_path = state_dir / "TASK_INDEX_ARCHIVE.json"
    claims_archive_path = state_dir / "CLAIMS_ARCHIVE.json"
    if task_archive_path.exists():
        task_index = merge_by_array_field(task_index, read_json(task_archive_path), "tasks")
    if claims_archive_path.exists():
        claims = merge_by_array_field(claims, read_json(claims_archive_path), "claims")

    return {
        "root": root,
        "config": config,
        "agent_registry": load_agent_registry(root),
        "project": read_json(state_dir / "PROJECT_STATE.json"),
        "task_index": task_index,
        "claims": claims,
        "mailbox_open": mailbox_open,
    }


def normalize_agent(agent: dict[str, Any]) -> dict[str, Any]:
    return {
        "id": str(agent.get("id") or ""),
        "role": agent.get("role"),
        "tier": agent.get("tier"),
        "capabilities": sorted({str(cap) for cap in agent.get("capabilities") or [] if str(cap)}),
        "adapter": agent.get("adapter", "llm"),
        "enabled": agent.get("enabled") is not False,
        "max_active_claims": agent.get("max_active_claims"),
        "trust_boundary": agent.get("trust_boundary"),
        "tool_policy_ref": agent.get("tool_policy_ref"),
        "auth": agent.get("auth") or {},
    }


def registry_from_roles(agent_roles: dict[str, Any]) -> dict[str, Any]:
    agents_by_id: dict[str, dict[str, Any]] = {}
    for role, default_agent in DEFAULT_AGENT_ROLES.items():
        agent_id = str(agent_roles.get(role) or default_agent)
        agent = agents_by_id.setdefault(
            agent_id,
            {
                "id": agent_id,
                "capabilities": [],
                "adapter": "human" if role == "human_owner" else "llm",
                "enabled": True,
            },
        )
        agent["capabilities"].extend(ROLE_CAPABILITIES[role])
        if role == "human_owner":
            agent["adapter"] = "human"
    return {
        "enabled": True,
        "routing_policy": "legacy_roles",
        "agents": [normalize_agent(agent) for agent in agents_by_id.values()],
        "source": "agent_roles",
    }


def default_agent_registry() -> dict[str, Any]:
    registry = registry_from_roles(DEFAULT_AGENT_ROLES)
    registry["source"] = "default"
    return registry


def load_agent_registry(root: Path) -> dict[str, Any]:
    config = read_json_if_exists(root.resolve() / "protocol.config.json") or {}
    explicit = config.get("agent_registry")
    if isinstance(explicit, dict) and explicit.get("enabled") is not False and isinstance(explicit.get("agents"), list):
        return {
            "enabled": True,
            "routing_policy": explicit.get("routing_policy", "weighted_least_loaded_deterministic"),
            "agents": [normalize_agent(agent) for agent in explicit.get("agents") or [] if isinstance(agent, dict)],
            "source": "agent_registry",
        }
    if isinstance(config.get("agent_roles"), dict):
        return registry_from_roles(config["agent_roles"])
    return default_agent_registry()


def enabled_agents(registry: dict[str, Any]) -> list[dict[str, Any]]:
    return [agent for agent in registry.get("agents") or [] if isinstance(agent, dict) and agent.get("enabled") is True]


def agents_with_capability(registry: dict[str, Any], capability: str) -> list[dict[str, Any]]:
    return [
        agent
        for agent in enabled_agents(registry)
        if capability in {str(item) for item in agent.get("capabilities") or []}
    ]


def has_capability(registry: dict[str, Any], agent_id: str, capability: str) -> bool:
    return any(agent.get("id") == agent_id for agent in agents_with_capability(registry, capability))


def tasks_by_id(state: dict[str, Any]) -> dict[str, dict[str, Any]]:
    tasks = state.get("task_index", {}).get("tasks") or []
    return {task.get("id"): task for task in tasks if isinstance(task, dict) and task.get("id")}


def active_claims(state: dict[str, Any]) -> list[dict[str, Any]]:
    claims = state.get("claims", {}).get("claims") or []
    return [claim for claim in claims if isinstance(claim, dict) and claim.get("status") == "active"]


def is_claim_scope_covering(scope_entry: str, path: str) -> bool:
    scope = scope_entry.replace("\\", "/").strip()
    candidate = path.replace("\\", "/").strip()
    if scope.endswith("/"):
        return candidate.startswith(scope)
    return candidate == scope


def path_is_claimed_by_other(path: str, owner: str, state: dict[str, Any]) -> bool:
    for claim in active_claims(state):
        if claim.get("owner") == owner:
            continue
        for scope in claim.get("scope") or []:
            if is_claim_scope_covering(str(scope), path):
                return True
    return False


def task_is_claimed_by_other(task: dict[str, Any], state: dict[str, Any]) -> bool:
    owner = str(task.get("owner") or "")
    task_id = task.get("id")
    task_file = task.get("file") or task.get("task_file")
    for claim in active_claims(state):
        if claim.get("owner") == owner:
            continue
        if claim.get("task_id") == task_id:
            return True
        for path in [task_file, *list(task.get("relevant_files") or [])]:
            if path and path_is_claimed_by_other(str(path), owner, state):
                return True
    return False


def priority_value(task: dict[str, Any]) -> int:
    return PRIORITY_RANK.get(str(task.get("priority") or "normal"), 2)
