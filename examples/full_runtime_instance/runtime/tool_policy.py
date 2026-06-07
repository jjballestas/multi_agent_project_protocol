#!/usr/bin/env python3
"""Tool allowlist and action gate helpers for runtime turn validation."""

from __future__ import annotations

import re
from typing import Any


ACTION_TYPES = {"read", "local_write", "local_exec", "contract_change", "external", "sensitive"}
TOOL_DENIED_EVENT = "security.tool_denied"

_ACTION_ALIASES = {
    "read": "read",
    "leer": "read",
    "write": "local_write",
    "local_write": "local_write",
    "edit": "local_write",
    "patch": "local_write",
    "exec": "local_exec",
    "execute": "local_exec",
    "local_exec": "local_exec",
    "run": "local_exec",
    "contract": "contract_change",
    "contract_change": "contract_change",
    "schema": "contract_change",
    "api": "contract_change",
    "migration": "contract_change",
    "external": "external",
    "network": "external",
    "deploy": "external",
    "release": "external",
    "sensitive": "sensitive",
    "secret": "sensitive",
    "credential": "sensitive",
    "delete": "sensitive",
    "destructive": "sensitive",
}

_KEYWORD_PATTERNS: list[tuple[str, re.Pattern[str]]] = [
    ("sensitive", re.compile(r"\b(secret|credential|production|delete|destructive|sensitive)\b", re.I)),
    ("external", re.compile(r"\b(push|release|deploy|network|external|publish)\b", re.I)),
    ("contract_change", re.compile(r"\b(schema|api|contract|migration|breaking|public interface)\b", re.I)),
    ("local_exec", re.compile(r"\b(exec|execute|run|command|script|shell|test)\b", re.I)),
    ("local_write", re.compile(r"\b(write|edit|patch|create|modify|move)\b", re.I)),
]


def _as_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, (list, tuple, set)):
        return [str(item).strip() for item in value if str(item).strip()]
    text = str(value).strip()
    return [text] if text else []


def _normalize_action(value: Any) -> str | None:
    text = str(value or "").strip().lower().replace("-", "_")
    return _ACTION_ALIASES.get(text)


def _action_text(action: Any) -> str:
    if isinstance(action, str):
        return action
    if not isinstance(action, dict):
        return ""
    pieces: list[str] = []
    for key in ("type", "action_type", "kind", "name", "summary", "description", "tool"):
        value = action.get(key)
        if isinstance(value, (str, int, float)):
            pieces.append(str(value))
    return " ".join(pieces)


def classify_action(action: Any) -> str:
    """Classify an action into the generic gate taxonomy.

    Explicit action types win. Ambiguous declared actions are treated as sensitive
    so callers fail closed instead of silently bypassing policy.
    """

    if isinstance(action, dict):
        for key in ("type", "action_type", "kind"):
            normalized = _normalize_action(action.get(key))
            if normalized:
                return normalized
    else:
        normalized = _normalize_action(action)
        if normalized:
            return normalized

    text = _action_text(action)
    for action_type, pattern in _KEYWORD_PATTERNS:
        if pattern.search(text):
            return action_type
    return "sensitive"


def gate_for_action(action_type: str) -> dict[str, Any]:
    """Return the gate contract for a generic action type."""

    normalized = _normalize_action(action_type) or "sensitive"
    if normalized == "read":
        return {"gate": "automatic_log", "human_required": False, "diff_required": False}
    if normalized == "local_write":
        return {"gate": "sandbox_diff", "human_required": False, "diff_required": True}
    if normalized == "local_exec":
        return {"gate": "sandbox_command_allowlist", "human_required": False, "command_allowlist_required": True}
    if normalized == "contract_change":
        return {
            "gate": "decision_review_qa",
            "human_required": False,
            "decision_required": True,
            "review_required": True,
            "qa_required": True,
        }
    return {"gate": "human_approval", "human_required": True}


def _split_scope(scope: str) -> tuple[str, str | None]:
    normalized = scope.replace("\\", "/").strip()
    path, separator, selector = normalized.partition("#")
    return path, selector if separator else None


def _scope_covers(policy_scope: str, requested_scope: str) -> bool:
    policy = policy_scope.replace("\\", "/").strip()
    requested = requested_scope.replace("\\", "/").strip()
    if policy == "*":
        return True
    policy_path, policy_selector = _split_scope(policy)
    requested_path, requested_selector = _split_scope(requested)
    if policy_path == requested_path:
        return policy_selector is None or policy_selector == requested_selector
    return requested_path.startswith(policy_path.rstrip("/") + "/") if policy_path.endswith("/") else False


def _tool_name(tool: Any) -> str:
    if isinstance(tool, str):
        return tool.strip()
    if isinstance(tool, dict):
        return str(tool.get("name") or tool.get("tool") or "").strip()
    return ""


def _tool_scopes(tool: Any, task_scope: Any) -> list[str]:
    if isinstance(tool, dict):
        for key in ("scope", "scopes", "paths"):
            scopes = _as_list(tool.get(key))
            if scopes:
                return scopes
    scopes = _as_list(task_scope)
    return scopes if scopes else ["*"]


def _agent_by_id(registry: dict[str, Any], agent_id: str) -> dict[str, Any] | None:
    for item in registry.get("agents") or []:
        if isinstance(item, dict) and str(item.get("id") or "") == agent_id:
            return item
    return None


def _policy_refs(agent_id: str, agent: dict[str, Any], tool_policy: dict[str, Any]) -> list[str]:
    refs: list[str] = []
    refs.extend(_as_list(agent.get("tool_policy_ref")))
    agent_policies = tool_policy.get("agent_policies")
    if isinstance(agent_policies, dict):
        refs.extend(_as_list(agent_policies.get(agent_id)))
    refs.extend(_as_list(tool_policy.get("default_policy_ref")))
    return list(dict.fromkeys(refs))


def _rules_for_refs(refs: list[str], tool_policy: dict[str, Any]) -> list[dict[str, Any]]:
    rules: list[dict[str, Any]] = []
    for key in ("allow", "rules"):
        for item in tool_policy.get(key) or []:
            if isinstance(item, dict):
                rules.append(item)
    policies = tool_policy.get("policies")
    if isinstance(policies, dict):
        for ref in refs:
            policy = policies.get(ref)
            if isinstance(policy, dict):
                for item in policy.get("allow") or []:
                    if isinstance(item, dict):
                        rules.append(item)
            elif isinstance(policy, list):
                for item in policy:
                    if isinstance(item, dict):
                        rules.append(item)
    return rules


def _rule_tools(rule: dict[str, Any]) -> list[str]:
    return _as_list(rule.get("tool")) + _as_list(rule.get("tools"))


def _rule_actions(rule: dict[str, Any]) -> set[str]:
    return {item for item in (_normalize_action(value) for value in _as_list(rule.get("actions"))) if item}


def _tool_action(tool: Any) -> str | None:
    if not isinstance(tool, dict):
        return None
    for key in ("action_type", "type", "kind"):
        normalized = _normalize_action(tool.get(key))
        if normalized:
            return normalized
    return None


def _rule_matches(rule: dict[str, Any], *, agent_id: str, agent: dict[str, Any], tool: Any, task_scope: Any) -> bool:
    name = _tool_name(tool)
    allowed_tools = _rule_tools(rule)
    if not name or not allowed_tools or name not in set(allowed_tools):
        return False

    allowed_agents = set(_as_list(rule.get("agents")) + _as_list(rule.get("agent")))
    if allowed_agents and agent_id not in allowed_agents:
        return False

    required_capabilities = set(_as_list(rule.get("capabilities")) + _as_list(rule.get("capability")))
    agent_capabilities = {str(item) for item in agent.get("capabilities") or []}
    if not required_capabilities or not (required_capabilities & agent_capabilities):
        return False

    allowed_actions = _rule_actions(rule)
    action_type = _tool_action(tool)
    if action_type and allowed_actions and action_type not in allowed_actions:
        return False

    allowed_scopes = _as_list(rule.get("scope")) + _as_list(rule.get("scopes"))
    if not allowed_scopes:
        return False
    return all(any(_scope_covers(allowed, requested) for allowed in allowed_scopes) for requested in _tool_scopes(tool, task_scope))


def is_tool_allowed(agent: str, tool: Any, task_scope: Any, registry: dict[str, Any], config: dict[str, Any]) -> bool:
    """Return whether an agent can use a declared tool for the requested scope.

    If no tool_policy is declared, the legacy runtime behavior is preserved.
    Once tool_policy is enabled, rules are deny-by-default.
    """

    tool_policy = config.get("tool_policy")
    if not isinstance(tool_policy, dict) or tool_policy.get("enabled") is False:
        return True

    agent_id = str(agent or "").strip()
    agent_info = _agent_by_id(registry, agent_id)
    if not agent_info or agent_info.get("enabled") is not True:
        return False

    refs = _policy_refs(agent_id, agent_info, tool_policy)
    rules = _rules_for_refs(refs, tool_policy)
    return any(_rule_matches(rule, agent_id=agent_id, agent=agent_info, tool=tool, task_scope=task_scope) for rule in rules)
