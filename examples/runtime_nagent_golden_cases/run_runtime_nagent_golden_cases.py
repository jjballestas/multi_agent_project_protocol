#!/usr/bin/env python3
"""Golden N=3/N=5 cases for the N-agent runtime router."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from runtime.router import select_next  # noqa: E402


ROUTING_CONFIG = {
    "routing_epoch": "nagent-golden-v1",
    "routing_weights": {
        "active_claims": 10,
        "pending_reviews": 6,
        "pending_qa": 6,
        "open_fix_cycles": 4,
        "cooldown_penalty": 1,
        "capability_affinity": 1,
    },
}


def agent(agent_id: str, capabilities: list[str]) -> dict:
    return {"id": agent_id, "capabilities": capabilities, "enabled": True}


def registry(*agents: dict) -> dict:
    return {
        "enabled": True,
        "routing_policy": "weighted_least_loaded_deterministic",
        "agents": list(agents),
    }


def state(tasks: list[dict], *, claims: list[dict] | None = None, agents: dict | None = None, config: dict | None = None) -> dict:
    return {
        "task_index": {"tasks": tasks},
        "claims": {"claims": claims or []},
        "mailbox_open": [],
        "agent_registry": agents or registry(),
        "config": config or ROUTING_CONFIG,
    }


def task(task_id: str, status: str, **extra) -> dict:
    payload = {
        "id": task_id,
        "owner": "Author",
        "author": "Author",
        "original_author": "Author",
        "status": status,
        "priority": "high",
        "depends_on": [],
    }
    payload.update(extra)
    return payload


def active_claim(owner: str, index: int) -> dict:
    return {
        "claim_id": f"CLAIM-{owner}-{index:04d}",
        "task_id": f"TASK-CLAIM-{index:04d}",
        "owner": owner,
        "status": "active",
        "scope": [],
    }


def n3_registry() -> dict:
    return registry(
        agent("Author", ["implementer", "reviewer", "qa"]),
        agent("Reviewer", ["reviewer"]),
        agent("QA", ["qa"]),
    )


def case_n3_review_goes_to_non_author() -> None:
    result = select_next(state([task("TASK-N3-REVIEW", "in_review")], agents=n3_registry()))
    assert result["action"] == "review", result
    assert result["owner"] == "Reviewer", result
    assert result["owner"] != "Author", result
    filtered = result["routing_decision"]["explanation"]["filtered"]
    assert any(item.get("reason") == "author_excluded" and item.get("agent") == "Author" for item in filtered), result


def case_n3_qa_goes_to_non_author() -> None:
    result = select_next(state([task("TASK-N3-QA", "qa_pending")], agents=n3_registry()))
    assert result["action"] == "qa", result
    assert result["owner"] == "QA", result
    assert result["owner"] != "Author", result
    filtered = result["routing_decision"]["explanation"]["filtered"]
    assert any(item.get("reason") == "author_excluded" and item.get("agent") == "Author" for item in filtered), result


def case_n3_author_only_review_escalates() -> None:
    agents = registry(
        agent("Author", ["implementer", "reviewer", "qa"]),
        agent("Builder", ["implementer"]),
        agent("Observer", ["implementer"]),
    )
    result = select_next(state([task("TASK-N3-ESC-REVIEW", "in_review")], agents=agents))
    assert result["action"] == "escalate", result
    assert "author exclusion" in result["reason"], result
    assert not result["routing_decision"]["explanation"]["candidates"], result


def case_n3_author_only_qa_escalates() -> None:
    agents = registry(
        agent("Author", ["implementer", "reviewer", "qa"]),
        agent("Builder", ["implementer"]),
        agent("Observer", ["implementer"]),
    )
    result = select_next(state([task("TASK-N3-ESC-QA", "qa_pending")], agents=agents))
    assert result["action"] == "escalate", result
    assert "author exclusion" in result["reason"], result
    assert not result["routing_decision"]["explanation"]["candidates"], result


def n5_registry() -> dict:
    return registry(
        agent("ImplA", ["implementer"]),
        agent("ImplB", ["implementer"]),
        agent("ImplC", ["implementer"]),
        agent("ImplD", ["implementer"]),
        agent("ImplE", ["implementer"]),
    )


def case_n5_replay_identical_assignment() -> None:
    tasks = [task("TASK-N5-REPLAY", "ready", owner="LegacyOwner", required_capability="implementer")]
    snapshot = state(tasks, agents=n5_registry())
    first = select_next(snapshot)
    second = select_next(snapshot)
    assert first == second, {"first": first, "second": second}
    assert first["action"] == "execute", first
    assert first["owner"] in {"ImplA", "ImplB", "ImplC", "ImplD", "ImplE"}, first


def case_n5_weighted_least_loaded_balances_claims() -> None:
    agents = n5_registry()
    claims: list[dict] = []
    counts = {agent_id: 0 for agent_id in ["ImplA", "ImplB", "ImplC", "ImplD", "ImplE"]}
    for index in range(25):
        task_id = f"TASK-N5-BAL-{index:04d}"
        result = select_next(
            state(
                [task(task_id, "ready", owner="LegacyOwner", required_capability="implementer")],
                claims=claims,
                agents=agents,
            )
        )
        owner = result["owner"]
        counts[owner] += 1
        claims.append(active_claim(owner, index))
    assert set(counts) == {"ImplA", "ImplB", "ImplC", "ImplD", "ImplE"}, counts
    assert min(counts.values()) > 0, counts
    assert max(counts.values()) - min(counts.values()) <= 1, counts


def main() -> int:
    cases = [
        case_n3_review_goes_to_non_author,
        case_n3_qa_goes_to_non_author,
        case_n3_author_only_review_escalates,
        case_n3_author_only_qa_escalates,
        case_n5_replay_identical_assignment,
        case_n5_weighted_least_loaded_balances_claims,
    ]
    failures = []
    for case in cases:
        try:
            case()
        except Exception as exc:  # noqa: BLE001 - compact golden failure reporting
            failures.append({"case": case.__name__, "error": str(exc)})
    if failures:
        print(json.dumps({"status": "FAILED", "failures": failures}, indent=2))
        return 1
    print(f"OK: {len(cases)} N-agent N=3/N=5 golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
