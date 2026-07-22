#!/usr/bin/env python3
"""Conditional obstacle cases for authoritative delivery and friction signals."""

from __future__ import annotations

import sys
import tempfile
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import runtime.turn_validate as turn_validate  # noqa: E402
from examples.runtime_turn_cases.run_runtime_turn_semantic_cases import build_fixture_root  # noqa: E402


FALSIFICATION_CONTRACTS = (
    {
        "id": "NEG-TURN-AUTHORITATIVE-DELIVERY-OBSTACLES",
        "negative": "A delivery transition cannot be hidden by a divergent outcome label.",
        "mutation": "turn_validate.is_delivery_turn = lambda report: False",
        "boundaries": (
            "assert turn_validate.validate_delivery_obstacles(delivery_missing) == [DELIVERY_ERROR]",
            "assert turn_validate.validate_delivery_obstacles(delivery_clean) == []",
            "assert turn_validate.validate_delivery_obstacles(delivery_missing) == []",
        ),
        "exercised_by": "main",
    },
    {
        "id": "NEG-TURN-FRICTION-OBSTACLES",
        "negative": "Objective gate, retry, or revert friction cannot carry empty obstacles.",
        "mutation": "turn_validate.friction_sensors = lambda report: []",
        "boundaries": (
            "assert turn_validate.validate_delivery_obstacles(gate_red) == [GATE_ERROR]",
            "assert turn_validate.validate_delivery_obstacles(retry) == [ATTEMPT_ERROR]",
            "assert turn_validate.validate_delivery_obstacles(revert) == [REVERT_ERROR]",
            "assert turn_validate.validate_delivery_obstacles(gate_red) == []",
        ),
        "exercised_by": "main",
    },
)

DELIVERY_ERROR = "semantic: delivery turn is missing the obstacles block; use [] when there was no friction"
GATE_ERROR = "semantic: objective friction (gate_green:false) requires non-empty obstacles"
ATTEMPT_ERROR = "semantic: objective friction (attempt>1) requires non-empty obstacles"
REVERT_ERROR = "semantic: objective friction (revert) requires non-empty obstacles"


def main() -> int:
    """PERMANENT_NEGATIVE: NEG-TURN-AUTHORITATIVE-DELIVERY-OBSTACLES, NEG-TURN-FRICTION-OBSTACLES"""
    delivery_missing = {
        "outcome": "ok",
        "transitions": {"task_status": {"from": "in_progress", "to": "in_review"}},
    }
    delivery_clean = {**delivery_missing, "obstacles": []}
    gate_red = {"outcome": "blocked", "gate_green": False, "obstacles": []}
    retry = {"outcome": "ok", "attempt_id": "attempt-2", "obstacles": []}
    revert = {
        "outcome": "ok",
        "actions": [{"type": "local_exec", "summary": "Reverted the failed change."}],
        "obstacles": [],
    }
    obstacle = [{"what": "Gate failed.", "root_cause": "Invalid state.", "resolution": "State repaired.", "recurrence_risk": "low"}]

    assert turn_validate.is_delivery_turn(delivery_missing)
    assert turn_validate.validate_delivery_obstacles(delivery_missing) == [DELIVERY_ERROR]
    assert turn_validate.validate_delivery_obstacles(delivery_clean) == []
    assert turn_validate.validate_delivery_obstacles(gate_red) == [GATE_ERROR]
    assert turn_validate.validate_delivery_obstacles(retry) == [ATTEMPT_ERROR]
    assert turn_validate.validate_delivery_obstacles(revert) == [REVERT_ERROR]
    assert turn_validate.validate_delivery_obstacles({**gate_red, "obstacles": obstacle}) == []
    assert turn_validate.validate_delivery_obstacles({"outcome": "ok"}) == []

    with tempfile.TemporaryDirectory(prefix="runtime-turn-obstacles-") as temp:
        fixture_root = Path(temp)
        build_fixture_root(fixture_root)
        full_delivery = json.loads((ROOT / "examples/runtime_turn_cases/semantic_valid.json").read_text(encoding="utf-8"))
        full_delivery["outcome"] = "ok"
        full_delivery.pop("obstacles")
        full_errors = turn_validate.validate_turn(full_delivery, fixture_root)
        assert DELIVERY_ERROR in full_errors

    original_delivery = turn_validate.is_delivery_turn
    try:
        turn_validate.is_delivery_turn = lambda report: False
        assert turn_validate.validate_delivery_obstacles(delivery_missing) == []
    finally:
        turn_validate.is_delivery_turn = original_delivery

    original_friction = turn_validate.friction_sensors
    try:
        turn_validate.friction_sensors = lambda report: []
        assert turn_validate.validate_delivery_obstacles(gate_red) == []
    finally:
        turn_validate.friction_sensors = original_friction

    print("OK: authoritative delivery, objective friction, and anti-theater controls are mutation-proved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
