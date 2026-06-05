#!/usr/bin/env python3
"""Golden cases for the deterministic runtime router."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from runtime.router import select_next  # noqa: E402


def state(tasks, claims=None, mailbox=None):
    return {
        "task_index": {"tasks": tasks},
        "claims": {"claims": claims or []},
        "mailbox_open": mailbox or [],
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
]


def matches(actual, expected):
    if expected is None:
        return actual is None
    return actual is not None and all(actual.get(key) == value for key, value in expected.items())


def main() -> int:
    failures = []
    for case in CASES:
        first = select_next(case["state"])
        second = select_next(case["state"])
        if first != second or not matches(first, case["expected"]):
            failures.append({"case": case["name"], "expected": case["expected"], "actual": first, "second": second})

    if failures:
        print(json.dumps({"status": "FAILED", "failures": failures}, indent=2))
        return 1
    print(f"OK: {len(CASES)} router golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
