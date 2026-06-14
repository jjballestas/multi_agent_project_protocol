#!/usr/bin/env python3
"""Post-hoc metrics for runtime JSONL logs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def read_entries(run_log_path: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    if not run_log_path.exists():
        return entries
    for line in run_log_path.read_text(encoding="utf-8-sig").splitlines():
        if line.strip():
            entries.append(json.loads(line))
    return entries


def summarize(run_log_path: Path) -> dict[str, Any]:
    entries = read_entries(run_log_path)
    turns_total = len(entries)
    turns_per_task: dict[str, int] = {}
    cost_per_task: dict[str, int] = {}
    green_count = 0
    gate_count = 0
    reverts = 0
    collisions_avoided = 0
    cost_total = 0

    for entry in entries:
        task_id = str(entry.get("task_id") or "none")
        turns_per_task[task_id] = turns_per_task.get(task_id, 0) + 1
        if entry.get("gate_green") is not None:
            gate_count += 1
            if entry.get("gate_green") is True:
                green_count += 1
        if entry.get("reverted") is True:
            reverts += 1
        collision_value = entry.get("collision_avoided") or 0
        collisions_avoided += int(collision_value) if isinstance(collision_value, int) else int(bool(collision_value))
        cost = entry.get("cost")
        if isinstance(cost, dict):
            tokens = cost.get("tokens")
        else:
            tokens = cost
        if isinstance(tokens, int):
            cost_total += tokens
            cost_per_task[task_id] = cost_per_task.get(task_id, 0) + tokens

    gates_green_pct = 100.0 if gate_count == 0 else round((green_count / gate_count) * 100, 2)
    return {
        "run_id": entries[0].get("run_id") if entries else None,
        "turns_total": turns_total,
        "turns_per_task": turns_per_task,
        "gates_green_pct": gates_green_pct,
        "reverts": reverts,
        "collisions_avoided": collisions_avoided,
        "cost_total": cost_total,
        "cost_per_task": cost_per_task,
        "duration_ms_total": sum(entry.get("duration_ms") or 0 for entry in entries),
    }


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    entries: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        value = json.loads(line)
        if isinstance(value, dict):
            entries.append(value)
    return entries


def sorted_counts(counts: dict[str, int]) -> dict[str, int]:
    return {key: counts[key] for key in sorted(counts)}


def increment(counts: dict[str, int], key: Any, amount: int = 1) -> None:
    text = str(key or "none")
    counts[text] = counts.get(text, 0) + amount


def transition_target(transition: Any) -> str:
    if isinstance(transition, dict):
        return str(transition.get("to") or "")
    if isinstance(transition, str) and "->" in transition:
        return transition.rsplit("->", 1)[1]
    return ""


def review_qa_event(payload: dict[str, Any]) -> str:
    review_qa = payload.get("review_qa")
    if isinstance(review_qa, dict) and review_qa.get("event"):
        return str(review_qa["event"])
    transition = str(payload.get("transition") or "")
    return {
        "qa_pending->qa_failed": "fail_qa",
        "qa_pending->architect_review": "fail_qa",
        "qa_pending->done": "pass_qa",
    }.get(transition, "")


def routing_decision_from_unit(unit: dict[str, Any]) -> dict[str, Any] | None:
    decision = unit.get("routing_decision")
    return decision if isinstance(decision, dict) else None


def assignment_from_decision(task_id: str, owner: Any, decision: dict[str, Any]) -> dict[str, Any]:
    explanation = decision.get("explanation") if isinstance(decision.get("explanation"), dict) else {}
    candidates = [
        str(candidate.get("agent"))
        for candidate in explanation.get("candidates") or []
        if isinstance(candidate, dict) and str(candidate.get("agent") or "")
    ]
    eligible = candidates or [str(agent) for agent in explanation.get("candidate_agents") or [] if str(agent)]
    selected = str(explanation.get("selected") or owner or "")
    return {
        "task_id": task_id,
        "selected": selected,
        "eligible": sorted(set(eligible or ([selected] if selected else []))),
        "weights": explanation.get("weights") if isinstance(explanation.get("weights"), dict) else {},
        "filtered": [item for item in explanation.get("filtered") or [] if isinstance(item, dict)],
    }


def assignment_weight(agent_id: str, weights: dict[str, Any]) -> float:
    try:
        value = float(weights.get(agent_id, 1.0))
    except (TypeError, ValueError):
        value = 1.0
    return value if value > 0 else 0.0


def fairness_summary(assignments: list[dict[str, Any]]) -> dict[str, Any]:
    counts: dict[str, int] = {}
    expected: dict[str, float] = {}
    denominator_zero = False

    for assignment in assignments:
        selected = str(assignment.get("selected") or "")
        eligible = [str(agent) for agent in assignment.get("eligible") or [] if str(agent)]
        weights = assignment.get("weights") if isinstance(assignment.get("weights"), dict) else {}
        if selected:
            increment(counts, selected)
        total_weight = sum(assignment_weight(agent, weights) for agent in eligible)
        if total_weight <= 0:
            denominator_zero = True
            continue
        for agent in eligible:
            counts.setdefault(agent, 0)
            expected[agent] = expected.get(agent, 0.0) + assignment_weight(agent, weights) / total_weight

    if not expected:
        return {
            "assignments": len(assignments),
            "counts": sorted_counts(counts),
            "expected": {},
            "fairness_ratio": None,
            "max_weighted_share_delta": 0.0,
            "denominator_zero": denominator_zero or bool(assignments),
        }

    agents = sorted(expected)
    min_count = min(counts.get(agent, 0) for agent in agents)
    max_count = max(counts.get(agent, 0) for agent in agents)
    observed_total = sum(counts.get(agent, 0) for agent in agents)
    expected_total = sum(expected.values())
    weighted_delta: dict[str, float] = {}
    for agent in agents:
        observed_share = (counts.get(agent, 0) / observed_total) if observed_total else 0.0
        expected_share = expected[agent] / expected_total if expected_total else 0.0
        weighted_delta[agent] = round(abs(observed_share - expected_share), 6)
    return {
        "assignments": len(assignments),
        "counts": sorted_counts(counts),
        "expected": {agent: round(expected[agent], 6) for agent in agents},
        "fairness_ratio": None if min_count == 0 else round(max_count / min_count, 6),
        "weighted_share_delta": weighted_delta,
        "max_weighted_share_delta": max(weighted_delta.values()) if weighted_delta else 0.0,
        "denominator_zero": denominator_zero,
    }


def summarize_cost_attribution(event_log_path: Path) -> dict[str, Any]:
    """Read `cost.attributed` events from the event log and impute tokens per dimension.

    Three dimensions (DECISION-0033): `by_handoff` keeps every handoff separate (NO cross-aggregation),
    `by_decision` sums per decision_id, `by_agent` sums per actor. Deterministic: handoffs sorted by
    `(seq, subject_hash)`, maps sorted by key. Reads the protocol plane only (metric + subject hash).
    """
    handoffs: list[dict[str, Any]] = []
    by_decision: dict[str, int] = {}
    by_agent: dict[str, int] = {}
    total = 0
    attributions = 0

    for event in read_jsonl(event_log_path):
        if event.get("type") != "cost.attributed":
            continue
        attributions += 1
        payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
        dimension = str(payload.get("dimension") or "")
        actor = str(event.get("actor") or payload.get("actor") or "none")
        try:
            cost = int(payload.get("cost_tokens") or 0)
        except (TypeError, ValueError):
            cost = 0
        total += cost
        by_agent[actor] = by_agent.get(actor, 0) + cost
        if dimension == "handoff":
            handoffs.append(
                {
                    "seq": event.get("seq"),
                    "subject_seq": payload.get("subject_seq"),
                    "subject_hash": payload.get("subject_hash"),
                    "actor": actor,
                    "task_id": payload.get("task_id"),
                    "cost_tokens": cost,
                }
            )
        elif dimension == "decision":
            decision_id = str(payload.get("decision_id") or payload.get("subject_hash") or "none")
            by_decision[decision_id] = by_decision.get(decision_id, 0) + cost

    handoffs.sort(key=lambda item: (int(item.get("seq") or 0), str(item.get("subject_hash") or "")))
    return {
        "attributions": attributions,
        "total_cost_tokens": total,
        "by_handoff": handoffs,
        "by_decision": sorted_counts(by_decision),
        "by_agent": sorted_counts(by_agent),
    }


def summarize_nagent(event_log_path: Path, run_log_path: Path) -> dict[str, Any]:
    events = read_jsonl(event_log_path)
    entries = read_entries(run_log_path)

    routing_assignments: list[dict[str, Any]] = []
    author_exclusions_by_task: dict[str, int] = {}
    for entry in entries:
        unit = entry.get("unit") if isinstance(entry.get("unit"), dict) else {}
        decision = routing_decision_from_unit(unit)
        if not decision:
            continue
        task_id = str(unit.get("task_id") or entry.get("task_id") or "none")
        assignment = assignment_from_decision(task_id, unit.get("owner"), decision)
        routing_assignments.append(assignment)
        excluded = sum(1 for item in assignment["filtered"] if item.get("reason") == "author_excluded")
        if excluded:
            increment(author_exclusions_by_task, task_id, excluded)

    routing_by_agent: dict[str, int] = {}
    for assignment in routing_assignments:
        if assignment.get("selected"):
            increment(routing_by_agent, assignment["selected"])

    qa_cycles_by_task: dict[str, int] = {}
    fencing_by_task: dict[str, int] = {}
    escalations_by_task: dict[str, int] = {}
    escalations_by_type: dict[str, int] = {}

    for event in events:
        payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
        task_id = str(payload.get("task_id") or event.get("aggregate_id") or "none")
        event_name = review_qa_event(payload)
        if event_name in {"fail_qa", "pass_qa"}:
            increment(qa_cycles_by_task, task_id)
        if event.get("type") == "state.stale_fencing_rejected":
            increment(fencing_by_task, task_id)
        target = transition_target(payload.get("transition"))
        if target in {"architect_review", "blocked"}:
            increment(escalations_by_task, task_id)
            increment(escalations_by_type, target)

    if not qa_cycles_by_task:
        for entry in entries:
            target = transition_target(entry.get("transition"))
            if target in {"qa_failed", "architect_review", "done"}:
                increment(qa_cycles_by_task, entry.get("task_id") or "none")

    for entry in entries:
        target = transition_target(entry.get("transition"))
        if target in {"architect_review", "blocked"}:
            increment(escalations_by_task, entry.get("task_id") or "none")
            increment(escalations_by_type, target)
        elif entry.get("outcome") == "blocked":
            increment(escalations_by_task, entry.get("task_id") or "none")
            increment(escalations_by_type, "blocked")

    return {
        "run_id": entries[0].get("run_id") if entries else None,
        "routing": {
            "assignments": len(routing_assignments),
            "by_agent": sorted_counts(routing_by_agent),
            "fairness": fairness_summary(routing_assignments),
        },
        "qa_cycles": {
            "total": sum(qa_cycles_by_task.values()),
            "by_task": sorted_counts(qa_cycles_by_task),
        },
        "fencing_conflicts": {
            "total": sum(fencing_by_task.values()),
            "by_task": sorted_counts(fencing_by_task),
        },
        "escalations": {
            "total": sum(escalations_by_task.values()),
            "by_task": sorted_counts(escalations_by_task),
            "by_type": sorted_counts(escalations_by_type),
        },
        "author_exclusions": {
            "total": sum(author_exclusions_by_task.values()),
            "by_task": sorted_counts(author_exclusions_by_task),
        },
    }
