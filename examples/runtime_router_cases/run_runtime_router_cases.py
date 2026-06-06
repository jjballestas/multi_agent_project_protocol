#!/usr/bin/env python3
"""Golden cases for the deterministic runtime router."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from runtime.router import evaluate_fairness, select_next  # noqa: E402


def state(tasks, claims=None, mailbox=None, agent_registry=None, config=None):
    payload = {
        "task_index": {"tasks": tasks},
        "claims": {"claims": claims or []},
        "mailbox_open": mailbox or [],
    }
    if agent_registry is not None:
        payload["agent_registry"] = agent_registry
    if config is not None:
        payload["config"] = config
    return payload


def registry(*agents):
    return {
        "enabled": True,
        "routing_policy": "weighted_least_loaded_deterministic",
        "agents": list(agents),
    }


def agent(agent_id, capabilities, max_active_claims=None):
    payload = {"id": agent_id, "capabilities": capabilities, "enabled": True}
    if max_active_claims is not None:
        payload["max_active_claims"] = max_active_claims
    return payload


ROUTING_CONFIG = {
    "routing_epoch": "router-golden-v1",
    "routing_weights": {
        "active_claims": 10,
        "pending_reviews": 6,
        "pending_qa": 6,
        "open_fix_cycles": 4,
        "cooldown_penalty": 1,
        "capability_affinity": 1,
    },
}


CASES = [
    {
        "name": "human_gate",
        "state": state(
            [
                {
                    "id": "TASK-0100",
                    "owner": "Codex",
                    "status": "blocked",
                    "priority": "normal",
                    "review": "HUMAN_REQUIRED: confirm policy.",
                }
            ]
        ),
        "expected": {"action": "escalate", "task_id": "TASK-0100", "owner": "operador humano"},
    },
    {
        "name": "mailbox_before_review",
        "state": state(
            [{"id": "TASK-0101", "owner": "Codex", "status": "in_review", "priority": "high"}],
            mailbox=[
                {
                    "message_id": "MSG-001",
                    "task_id": "TASK-0102",
                    "requires_response": True,
                    "response_owner": "Codex",
                }
            ],
        ),
        "expected": {"action": "answer_mailbox", "task_id": "TASK-0102", "owner": "Codex"},
    },
    {
        "name": "review",
        "state": state([{"id": "TASK-0103", "owner": "Codex", "status": "in_review", "priority": "high"}]),
        "expected": {"action": "review", "task_id": "TASK-0103", "owner": "Claude"},
    },
    {
        "name": "ready_priority_and_deps",
        "state": state(
            [
                {"id": "TASK-0104", "owner": "Codex", "status": "ready", "priority": "normal", "depends_on": []},
                {"id": "TASK-0105", "owner": "Codex", "status": "ready", "priority": "high", "depends_on": []},
                {"id": "TASK-0106", "owner": "Codex", "status": "ready", "priority": "critical", "depends_on": ["TASK-0999"]},
            ]
        ),
        "expected": {"action": "execute", "task_id": "TASK-0105", "owner": "Codex"},
    },
    {
        "name": "ready_claimed_by_other",
        "state": state(
            [
                {
                    "id": "TASK-0107",
                    "owner": "Codex",
                    "status": "ready",
                    "priority": "high",
                    "file": "Area_comun/tasks/TASK-0107.md",
                }
            ],
            claims=[
                {
                    "claim_id": "CLAIM-other",
                    "task_id": "none",
                    "owner": "Claude",
                    "status": "active",
                    "scope": ["Area_comun/tasks/TASK-0107.md"],
                }
            ],
        ),
        "expected": None,
    },
    {
        "name": "ready_required_capability_uses_load_score",
        "state": state(
            [
                {
                    "id": "TASK-0200",
                    "owner": "LegacyOwner",
                    "status": "ready",
                    "priority": "high",
                    "required_capability": "implementer",
                    "depends_on": [],
                }
            ],
            claims=[{"claim_id": "CLAIM-alpha", "owner": "Alpha", "status": "active", "scope": []}],
            agent_registry=registry(agent("Alpha", ["implementer"]), agent("Beta", ["implementer"])),
            config=ROUTING_CONFIG,
        ),
        "expected": {"action": "execute", "task_id": "TASK-0200", "owner": "Beta"},
        "requires_routing_decision": True,
        "expected_selected": "Beta",
        "requires_score": True,
    },
    {
        "name": "max_active_claims_filters_candidate",
        "state": state(
            [
                {
                    "id": "TASK-0201",
                    "owner": "LegacyOwner",
                    "status": "ready",
                    "priority": "high",
                    "required_capability": "implementer",
                    "depends_on": [],
                }
            ],
            claims=[{"claim_id": "CLAIM-alpha", "owner": "Alpha", "status": "active", "scope": []}],
            agent_registry=registry(agent("Alpha", ["implementer"], max_active_claims=1), agent("Beta", ["implementer"])),
            config=ROUTING_CONFIG,
        ),
        "expected": {"action": "execute", "task_id": "TASK-0201", "owner": "Beta"},
        "requires_filtered_reason": "max_active_claims",
    },
    {
        "name": "review_excludes_author_even_with_reviewer_capability",
        "state": state(
            [{"id": "TASK-0202", "owner": "Author", "status": "in_review", "priority": "high"}],
            agent_registry=registry(
                agent("Author", ["reviewer", "architect", "orchestrator"]),
                agent("Reviewer", ["reviewer"]),
            ),
            config=ROUTING_CONFIG,
        ),
        "expected": {"action": "review", "task_id": "TASK-0202", "owner": "Reviewer"},
        "expected_selected": "Reviewer",
        "requires_filtered_reason": "author_excluded",
    },
    {
        "name": "review_author_only_escalates_without_self_review",
        "state": state(
            [{"id": "TASK-0203", "owner": "Solo", "status": "in_review", "priority": "high"}],
            agent_registry=registry(agent("Solo", ["reviewer", "architect", "orchestrator"])),
            config=ROUTING_CONFIG,
        ),
        "expected": {"action": "escalate", "task_id": "TASK-0203", "owner": "Solo"},
        "requires_filtered_reason": "author_excluded",
    },
    {
        "name": "qa_excludes_author_even_with_qa_capability",
        "state": state(
            [{"id": "TASK-0204", "owner": "Author", "status": "qa_pending", "priority": "high"}],
            agent_registry=registry(agent("Author", ["qa"]), agent("QA", ["qa"])),
            config=ROUTING_CONFIG,
        ),
        "expected": {"action": "qa", "task_id": "TASK-0204", "owner": "QA"},
        "expected_selected": "QA",
        "requires_filtered_reason": "author_excluded",
    },
]


def matches(actual, expected):
    if expected is None:
        return actual is None
    return actual is not None and all(actual.get(key) == value for key, value in expected.items())


def routing_checks(case, actual):
    if actual is None:
        return []
    errors = []
    decision = actual.get("routing_decision")
    explanation = (decision or {}).get("explanation") or {}
    if case.get("requires_routing_decision") and not decision:
        errors.append("missing routing_decision")
    if case.get("expected_selected") and explanation.get("selected") != case["expected_selected"]:
        errors.append(f"selected mismatch: {explanation.get('selected')}")
    if case.get("requires_filtered_reason"):
        reasons = [item.get("reason") for item in explanation.get("filtered") or []]
        if case["requires_filtered_reason"] not in reasons:
            errors.append(f"missing filtered reason: {case['requires_filtered_reason']}")
    if case.get("requires_score"):
        scores = [item.get("score") for item in explanation.get("candidates") or []]
        if not scores or any(not isinstance(score, list) or len(score) != 3 for score in scores):
            errors.append("missing score tuple")
    return errors


def fairness_cases():
    failures = []
    agents = registry(agent("AgentA", ["implementer"]), agent("AgentB", ["implementer"]), agent("AgentC", ["implementer"]))
    assignments = []
    for index in range(100):
        result = select_next(
            state(
                [
                    {
                        "id": f"TASK-F{index:04d}",
                        "owner": "LegacyOwner",
                        "status": "ready",
                        "priority": "normal",
                        "required_capability": "implementer",
                        "depends_on": [],
                    }
                ],
                agent_registry=agents,
                config=ROUTING_CONFIG,
            )
        )
        explanation = result["routing_decision"]["explanation"]
        assignments.append({"selected": result["owner"], "eligible_agents": explanation["candidate_agents"]})
    report = evaluate_fairness(assignments, minimum_sample=30, max_fairness_ratio=2.0, max_weighted_share_delta=0.20)
    if not report["ok"]:
        failures.append({"case": "fairness_100_tasks_three_identical_agents", "report": report})

    starvation = [{"selected": "AgentA", "eligible_agents": ["AgentA", "AgentB", "AgentC"]} for _ in range(30)]
    starvation_report = evaluate_fairness(starvation, minimum_sample=30)
    if starvation_report["ok"] or not starvation_report["starvation"]:
        failures.append({"case": "fairness_detects_starvation", "report": starvation_report})

    weighted = []
    weighted.extend({"selected": "Wide", "eligible_agents": ["Wide", "Narrow"], "weights": {"Wide": 2, "Narrow": 1}} for _ in range(60))
    weighted.extend({"selected": "Narrow", "eligible_agents": ["Wide", "Narrow"], "weights": {"Wide": 2, "Narrow": 1}} for _ in range(30))
    weighted_report = evaluate_fairness(weighted, minimum_sample=30, max_weighted_share_delta=0.01)
    if not weighted_report["ok"]:
        failures.append({"case": "fairness_weighted_expected_vs_observed", "report": weighted_report})

    zero_report = evaluate_fairness([{"selected": "AgentA", "eligible_agents": ["AgentA"], "weights": {"AgentA": 0}}])
    if not zero_report["ok"] or not zero_report["denominator_zero"]:
        failures.append({"case": "fairness_denominator_zero_guard", "report": zero_report})

    return failures


def main() -> int:
    failures = []
    for case in CASES:
        first = select_next(case["state"])
        second = select_next(case["state"])
        check_errors = routing_checks(case, first)
        if first != second or not matches(first, case["expected"]) or check_errors:
            failures.append(
                {
                    "case": case["name"],
                    "expected": case["expected"],
                    "actual": first,
                    "second": second,
                    "check_errors": check_errors,
                }
            )

    failures.extend(fairness_cases())

    if failures:
        print(json.dumps({"status": "FAILED", "failures": failures}, indent=2))
        return 1
    print(f"OK: {len(CASES)} router golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
