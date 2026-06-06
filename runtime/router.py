#!/usr/bin/env python3
"""Deterministic work router for the protocol runtime."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

try:
    from .context import (
        active_claims,
        default_agent_registry,
        enabled_agents,
        load_state,
        priority_value,
        task_is_claimed_by_other,
        tasks_by_id,
    )
except ImportError:  # pragma: no cover - direct script execution
    from context import active_claims, default_agent_registry, enabled_agents, load_state, priority_value, task_is_claimed_by_other, tasks_by_id


REVIEW_TRANSITIONS = {"review", "qa"}


def select_next(state: dict[str, Any]) -> dict[str, Any] | None:
    tasks = tasks_by_id(state)

    human_gate = select_human_gate(state, tasks)
    if human_gate:
        return human_gate

    mailbox = select_mailbox_response(state)
    if mailbox:
        return mailbox

    review = select_review(tasks, state)
    if review:
        return review

    qa = select_qa(tasks, state)
    if qa:
        return qa

    ready = select_ready_task(state, tasks)
    if ready:
        return ready

    return None


def select_human_gate(state: dict[str, Any], tasks: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    for task_id in sorted(tasks):
        task = tasks[task_id]
        text = json.dumps(task, ensure_ascii=False).upper()
        if task.get("status") == "blocked" and ("DECISION_REQUIRED" in text or "HUMAN_REQUIRED" in text):
            return {
                "action": "escalate",
                "task_id": task_id,
                "owner": "operador humano",
                "reason": "blocked task requires human or decision gate",
            }

    for message in state.get("mailbox_open") or []:
        text = json.dumps(message, ensure_ascii=False).lower()
        if "human_required" in text:
            return {
                "action": "escalate",
                "task_id": message.get("task_id") or "none",
                "owner": "operador humano",
                "reason": f"mailbox human gate: {message.get('message_id')}",
            }
    return None


def select_mailbox_response(state: dict[str, Any]) -> dict[str, Any] | None:
    candidates = []
    for message in state.get("mailbox_open") or []:
        if message.get("requires_response") is True and message.get("response_owner") not in (None, "", "none"):
            candidates.append(message)
    if not candidates:
        return None
    message = sorted(candidates, key=lambda item: str(item.get("message_id") or item.get("_path") or ""))[0]
    return {
        "action": "answer_mailbox",
        "task_id": message.get("task_id") or "none",
        "owner": message.get("response_owner"),
        "reason": f"pending mailbox response: {message.get('message_id')}",
    }


def select_review(tasks: dict[str, dict[str, Any]], state: dict[str, Any] | None = None) -> dict[str, Any] | None:
    candidates = [task for task in tasks.values() if task.get("status") == "in_review"]
    if not candidates:
        return None
    task = sorted(candidates, key=lambda item: str(item.get("id")))[0]
    return select_agent(task, "review", state or {}, action="review")


def select_qa(tasks: dict[str, dict[str, Any]], state: dict[str, Any]) -> dict[str, Any] | None:
    candidates = [task for task in tasks.values() if task.get("status") == "qa_pending"]
    if not candidates:
        return None
    task = sorted(candidates, key=lambda item: str(item.get("id")))[0]
    return select_agent(task, "qa", state, action="qa")


def select_ready_task(state: dict[str, Any], tasks: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    candidates = []
    for task in tasks.values():
        if task.get("status") != "ready":
            continue
        dependencies = task.get("depends_on") or []
        if any(tasks.get(dep, {}).get("status") != "done" for dep in dependencies):
            continue
        if task_is_claimed_by_other(task, state):
            continue
        candidates.append(task)
    if not candidates:
        return None
    task = sorted(candidates, key=lambda item: (-priority_value(item), str(item.get("id"))))[0]
    if configured_required_capability(task):
        return select_agent(task, "execute", state, action="execute")
    return {
        "action": "execute",
        "task_id": task.get("id"),
        "owner": task.get("owner"),
        "reason": f"ready task selected by priority {task.get('priority', 'normal')}",
    }


def configured_required_capability(task: dict[str, Any]) -> str | None:
    value = task.get("required_capability")
    if value is None:
        return None
    value = str(value).strip()
    if not value or value.lower() in {"none", "null"}:
        return None
    return value


def required_capability(task: dict[str, Any], transition: str) -> str | None:
    configured = configured_required_capability(task)
    if configured:
        return configured
    if transition == "review":
        return "reviewer"
    if transition == "qa":
        return "qa"
    return None


def task_author(task: dict[str, Any]) -> str:
    return str(task.get("author") or task.get("created_by") or task.get("owner") or "")


def routing_registry(state: dict[str, Any]) -> dict[str, Any]:
    registry = state.get("agent_registry")
    if isinstance(registry, dict):
        return registry
    return default_agent_registry()


def routing_epoch(state: dict[str, Any]) -> str:
    config = state.get("config") or {}
    for source in (state, config, config.get("runtime") or {}):
        value = source.get("routing_epoch") if isinstance(source, dict) else None
        if value not in (None, ""):
            return str(value)
    return "0"


def routing_weights(state: dict[str, Any]) -> dict[str, float]:
    config = state.get("config") or {}
    raw = config.get("routing_weights")
    if not isinstance(raw, dict):
        raw = (config.get("runtime") or {}).get("routing_weights")
    if not isinstance(raw, dict):
        return {}
    weights: dict[str, float] = {}
    for key, value in raw.items():
        try:
            weights[str(key)] = float(value)
        except (TypeError, ValueError):
            continue
    return weights


def active_claim_count(agent_id: str, state: dict[str, Any]) -> int:
    return sum(1 for claim in active_claims(state) if claim.get("owner") == agent_id)


def assigned_agent(task: dict[str, Any], keys: tuple[str, ...]) -> str:
    for key in keys:
        value = task.get(key)
        if value not in (None, ""):
            return str(value)
    return ""


def pending_review_count(agent_id: str, state: dict[str, Any]) -> int:
    tasks = tasks_by_id(state).values()
    keys = ("reviewer", "review_owner", "assigned_reviewer")
    return sum(1 for task in tasks if task.get("status") == "in_review" and assigned_agent(task, keys) == agent_id)


def pending_qa_count(agent_id: str, state: dict[str, Any]) -> int:
    tasks = tasks_by_id(state).values()
    keys = ("qa", "qa_owner", "assigned_qa")
    return sum(1 for task in tasks if task.get("status") == "qa_pending" and assigned_agent(task, keys) == agent_id)


def open_fix_cycle_count(agent_id: str, state: dict[str, Any]) -> int:
    tasks = tasks_by_id(state).values()
    keys = ("owner", "assignee", "assigned_to")
    fix_statuses = {"changes_requested", "qa_failed"}
    return sum(1 for task in tasks if task.get("status") in fix_statuses and assigned_agent(task, keys) == agent_id)


def cooldown_penalty(agent: dict[str, Any], state: dict[str, Any]) -> float:
    agent_id = str(agent.get("id") or "")
    cooldowns = state.get("routing_cooldowns") or {}
    value = cooldowns.get(agent_id) if isinstance(cooldowns, dict) else None
    if value is None:
        value = agent.get("cooldown_penalty")
    try:
        return float(value or 0)
    except (TypeError, ValueError):
        return 0.0


def capability_affinity(agent: dict[str, Any], required: str) -> float:
    affinity = agent.get("capability_affinity")
    if isinstance(affinity, dict):
        try:
            return float(affinity.get(required) or 0)
        except (TypeError, ValueError):
            return 0.0
    return 1.0 if required in {str(item) for item in agent.get("capabilities") or []} else 0.0


def load_metrics(agent: dict[str, Any], required: str, state: dict[str, Any]) -> dict[str, float]:
    agent_id = str(agent.get("id") or "")
    return {
        "active_claims": float(active_claim_count(agent_id, state)),
        "pending_reviews": float(pending_review_count(agent_id, state)),
        "pending_qa": float(pending_qa_count(agent_id, state)),
        "open_fix_cycles": float(open_fix_cycle_count(agent_id, state)),
        "cooldown_penalty": cooldown_penalty(agent, state),
        "capability_affinity": capability_affinity(agent, required),
    }


def load_score(metrics: dict[str, float], weights: dict[str, float]) -> float:
    total = 0.0
    for key, value in metrics.items():
        weighted = value * weights.get(key, 0.0)
        total = total - weighted if key == "capability_affinity" else total + weighted
    return total


def stable_hash(task_id: str, transition: str, agent_id: str, epoch: str) -> int:
    payload = f"{task_id}|{transition}|{agent_id}|{epoch}"
    return int(hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16], 16)


def max_active_claims(agent: dict[str, Any]) -> int | None:
    value = agent.get("max_active_claims")
    if value in (None, ""):
        return None
    try:
        limit = int(value)
    except (TypeError, ValueError):
        return None
    return limit if limit >= 0 else None


def explain_filter(agent: dict[str, Any], reason: str, **extra: Any) -> dict[str, Any]:
    payload = {"agent": str(agent.get("id") or ""), "reason": reason}
    payload.update(extra)
    return payload


def candidate_evaluation(task: dict[str, Any], transition: str, state: dict[str, Any]) -> dict[str, Any]:
    registry = routing_registry(state)
    required = required_capability(task, transition)
    weights = routing_weights(state)
    epoch = routing_epoch(state)
    author = task_author(task)
    task_id = str(task.get("id") or "")
    candidates: list[dict[str, Any]] = []
    filtered: list[dict[str, Any]] = []
    capability_candidates: list[str] = []

    for agent in registry.get("agents") or []:
        if not isinstance(agent, dict):
            continue
        agent_id = str(agent.get("id") or "")
        capabilities = {str(item) for item in agent.get("capabilities") or []}
        if agent.get("enabled") is not True:
            filtered.append(explain_filter(agent, "disabled"))
            continue
        if required and required not in capabilities:
            filtered.append(explain_filter(agent, "missing_capability", required_capability=required))
            continue
        capability_candidates.append(agent_id)
        if transition in REVIEW_TRANSITIONS and agent_id == author:
            filtered.append(explain_filter(agent, "author_excluded", author=author))
            continue
        active_count = active_claim_count(agent_id, state)
        limit = max_active_claims(agent)
        if limit is not None and active_count >= limit:
            filtered.append(explain_filter(agent, "max_active_claims", active_claims=active_count, max_active_claims=limit))
            continue
        metrics = load_metrics(agent, required or "", state)
        score = load_score(metrics, weights)
        tie_break = stable_hash(task_id, transition, agent_id, epoch)
        candidates.append(
            {
                "agent": agent_id,
                "metrics": metrics,
                "score": [score, tie_break, agent_id],
                "load_score": score,
                "stable_hash": tie_break,
            }
        )

    return {
        "policy": (registry.get("routing_policy") or "weighted_least_loaded_deterministic"),
        "transition": transition,
        "required_capability": required,
        "routing_epoch": epoch,
        "author": author if transition in REVIEW_TRANSITIONS else None,
        "weights": weights,
        "candidate_agents": capability_candidates,
        "candidates": candidates,
        "filtered": filtered,
    }


def routing_decision(explanation: dict[str, Any], selected: str | None = None) -> dict[str, Any]:
    payload = dict(explanation)
    payload["selected"] = selected
    return {
        "policy": explanation.get("policy"),
        "transition": explanation.get("transition"),
        "required_capability": explanation.get("required_capability"),
        "explanation": payload,
    }


def escalation_owner(state: dict[str, Any], author: str) -> str:
    registry = routing_registry(state)
    preferred: list[str] = []
    fallback: list[str] = []
    for agent in enabled_agents(registry):
        agent_id = str(agent.get("id") or "")
        capabilities = {str(item) for item in agent.get("capabilities") or []}
        if not ({"orchestrator", "architect"} & capabilities):
            continue
        fallback.append(agent_id)
        if agent_id != author:
            preferred.append(agent_id)
    if preferred:
        return sorted(preferred)[0]
    if fallback:
        return sorted(fallback)[0]
    return "Claude"


def select_agent(task: dict[str, Any], transition: str, state: dict[str, Any], *, action: str | None = None) -> dict[str, Any]:
    selected_action = action or transition
    required = required_capability(task, transition)
    if not required:
        return {
            "action": selected_action,
            "task_id": task.get("id"),
            "owner": task.get("owner"),
            "reason": "task has no required_capability; using declared owner",
        }

    explanation = candidate_evaluation(task, transition, state)
    candidates = sorted(explanation["candidates"], key=lambda item: (item["load_score"], item["stable_hash"], item["agent"]))
    if not candidates:
        reason = f"no eligible {required} agent for {transition}"
        if transition in REVIEW_TRANSITIONS:
            reason += "; review/qa author exclusion is enforced"
        return {
            "action": "escalate",
            "task_id": task.get("id"),
            "owner": escalation_owner(state, task_author(task)),
            "reason": reason,
            "routing_decision": routing_decision(explanation),
        }

    selected = candidates[0]
    owner = selected["agent"]
    return {
        "action": selected_action,
        "task_id": task.get("id"),
        "owner": owner,
        "reason": (
            f"{selected_action} selected by required_capability={required}, "
            f"load_score={selected['load_score']}"
        ),
        "routing_decision": routing_decision(explanation, owner),
    }


def assignment_weight(agent_id: str, weights: dict[str, Any]) -> float:
    try:
        value = float(weights.get(agent_id, 1.0))
    except (TypeError, ValueError):
        value = 1.0
    return value if value > 0 else 0.0


def evaluate_fairness(
    assignments: list[dict[str, Any]],
    *,
    minimum_sample: int = 30,
    max_fairness_ratio: float = 2.0,
    max_weighted_share_delta: float = 0.20,
) -> dict[str, Any]:
    counts: dict[str, int] = {}
    expected: dict[str, float] = {}
    eligible_seen: dict[str, int] = {}
    denominator_zero = False

    for assignment in assignments:
        selected = str(assignment.get("selected") or assignment.get("owner") or "")
        eligible = assignment.get("eligible_agents") or assignment.get("eligible") or []
        eligible = [str(agent) for agent in eligible if str(agent)]
        weights = assignment.get("weights") if isinstance(assignment.get("weights"), dict) else {}
        if selected:
            counts[selected] = counts.get(selected, 0) + 1
        total_weight = sum(assignment_weight(agent, weights) for agent in eligible)
        if total_weight <= 0:
            denominator_zero = True
            continue
        for agent in eligible:
            counts.setdefault(agent, 0)
            eligible_seen[agent] = eligible_seen.get(agent, 0) + 1
            expected[agent] = expected.get(agent, 0.0) + assignment_weight(agent, weights) / total_weight

    total_expected = sum(expected.values())
    if total_expected <= 0:
        return {
            "ok": True,
            "reason": "no eligible assignments",
            "assignments": len(assignments),
            "counts": counts,
            "expected": expected,
            "denominator_zero": True,
        }

    eligible_agents = sorted(expected)
    min_count = min(counts.get(agent, 0) for agent in eligible_agents)
    max_count = max(counts.get(agent, 0) for agent in eligible_agents)
    fairness_ratio = None if min_count == 0 else max_count / min_count
    observed_total = sum(counts.get(agent, 0) for agent in eligible_agents)
    weighted_deltas: dict[str, float] = {}
    for agent in eligible_agents:
        observed_share = (counts.get(agent, 0) / observed_total) if observed_total else 0.0
        expected_share = expected[agent] / total_expected
        weighted_deltas[agent] = abs(observed_share - expected_share)

    starvation = [
        agent
        for agent in eligible_agents
        if eligible_seen.get(agent, 0) >= minimum_sample and counts.get(agent, 0) == 0
    ]
    max_delta = max(weighted_deltas.values()) if weighted_deltas else 0.0
    ratio_ok = fairness_ratio is None or fairness_ratio <= max_fairness_ratio
    ok = not starvation and ratio_ok and max_delta <= max_weighted_share_delta
    return {
        "ok": ok,
        "assignments": len(assignments),
        "counts": counts,
        "expected": expected,
        "eligible_seen": eligible_seen,
        "fairness_ratio": fairness_ratio,
        "weighted_share_delta": weighted_deltas,
        "max_weighted_share_delta": max_delta,
        "starvation": starvation,
        "denominator_zero": denominator_zero,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Select the next runtime action.")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    result = select_next(load_state(Path(args.root)))
    print(json.dumps(result, indent=2, ensure_ascii=False) if result else "null")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
