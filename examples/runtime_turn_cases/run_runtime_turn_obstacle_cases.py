#!/usr/bin/env python3
"""Conditional obstacle cases for delivery turn reports."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import runtime.turn_validate as turn_validate  # noqa: E402


FALSIFICATION_CONTRACTS = (
    {
        "id": "NEG-TURN-DELIVERY-OBSTACLES",
        "negative": "A delivery report cannot bypass the non-empty obstacles gate.",
        "mutation": "turn_validate.is_delivery_turn = lambda report: False",
        "boundaries": (
            "assert missing_errors == [EXPECTED_ERROR]",
            "assert empty_errors == [EXPECTED_ERROR]",
            "assert turn_validate.validate_delivery_obstacles(non_delivery) == []",
            "assert turn_validate.validate_delivery_obstacles(delivery_with_obstacle) == []",
            "assert turn_validate.validate_delivery_obstacles(delivery_missing) == []",
        ),
        "exercised_by": "main",
    },
)

EXPECTED_ERROR = (
    "semantic: delivery turn is missing non-empty obstacles; "
    "report what was encountered and resolved"
)


def main() -> int:
    """PERMANENT_NEGATIVE: NEG-TURN-DELIVERY-OBSTACLES"""
    delivery_missing = {"outcome": "in_review"}
    delivery_empty = {"outcome": "done", "obstacles": []}
    non_delivery = {"outcome": "ok"}
    delivery_with_obstacle = {
        "outcome": "in_review",
        "obstacles": [
            {
                "what": "A fixture initially omitted delivery evidence.",
                "root_cause": "The conditional semantic gate did not exist.",
                "resolution": "The validator now requires a non-empty obstacle account.",
                "recurrence_risk": "low",
            }
        ],
    }

    missing_errors = turn_validate.validate_delivery_obstacles(delivery_missing)
    empty_errors = turn_validate.validate_delivery_obstacles(delivery_empty)
    assert missing_errors == [EXPECTED_ERROR]
    assert empty_errors == [EXPECTED_ERROR]
    assert turn_validate.validate_delivery_obstacles(non_delivery) == []
    assert turn_validate.validate_delivery_obstacles(delivery_with_obstacle) == []

    original = turn_validate.is_delivery_turn
    try:
        turn_validate.is_delivery_turn = lambda report: False
        assert turn_validate.validate_delivery_obstacles(delivery_missing) == []
    finally:
        turn_validate.is_delivery_turn = original

    print("OK: delivery obstacles are required, non-delivery remains optional, and the sensor mutant is killed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
