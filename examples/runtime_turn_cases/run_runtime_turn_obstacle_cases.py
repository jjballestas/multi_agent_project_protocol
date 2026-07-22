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
        "id": "NEG-TURN-STATUS-FRICTION-OBSTACLES",
        "negative": "An authoritative friction status transition cannot carry empty obstacles.",
        "mutation": "remove task_status.to handling from friction_sensors",
        "boundaries": (
            "assert STATUS_ERROR in validate_turn(blocked_empty)",
            "assert STATUS_ERROR not in validate_turn(blocked_empty) after mutation",
        ),
        "exercised_by": "main",
    },
    {
        "id": "NEG-TURN-REVIEW-FRICTION-OBSTACLES",
        "negative": "An authoritative review/QA friction event cannot carry empty obstacles.",
        "mutation": "remove review_qa handling from friction_sensors",
        "boundaries": (
            "assert REVIEW_ERROR in validate_turn(review_empty)",
            "assert REVIEW_ERROR not in validate_turn(review_empty) after mutation",
        ),
        "exercised_by": "main",
    },
    {
        "id": "NEG-TURN-CHECKS-FRICTION-OBSTACLES",
        "negative": "Non-empty failed checks cannot carry empty obstacles.",
        "mutation": "remove review_qa.checks_failed handling from friction_sensors",
        "boundaries": (
            "assert CHECKS_ERROR in validate_turn(checks_empty)",
            "assert CHECKS_ERROR not in validate_turn(checks_empty) after mutation",
        ),
        "exercised_by": "main",
    },
    {
        "id": "NEG-TURN-REVERT-PROXY-OBSTACLES",
        "negative": "A declared revert action proxy cannot carry empty obstacles.",
        "mutation": "remove action-summary revert proxy from friction_sensors",
        "boundaries": (
            "assert REVERT_ERROR in validate_turn(revert)",
            "assert REVERT_ERROR not in validate_turn(revert) after mutation",
        ),
        "exercised_by": "main",
    },
    {
        "id": "NEG-TURN-ATTEMPT-ID-NOT-A-COUNTER",
        "negative": "An idempotency attempt_id suffix cannot create friction.",
        "mutation": "restore trailing-integer parsing of attempt_id",
        "boundaries": (
            "assert validate_turn(first_attempt_0042) == []",
            "assert ATTEMPT_ERROR in validate_turn(first_attempt_0042) after mutation",
        ),
        "exercised_by": "main",
    },
)

DELIVERY_ERROR = "semantic: delivery turn is missing the obstacles block; use [] when there was no friction"
STATUS_ERROR = "semantic: objective friction (task_status:blocked) requires non-empty obstacles"
REVIEW_ERROR = "semantic: objective friction (review_qa:assign_fix) requires non-empty obstacles"
CHECKS_ERROR = "semantic: objective friction (review_qa:checks_failed) requires non-empty obstacles"
REVERT_ERROR = "semantic: objective friction (revert:action-summary-proxy) requires non-empty obstacles"
ATTEMPT_ERROR = "semantic: objective friction (attempt>1) requires non-empty obstacles"


def main() -> int:
    """PERMANENT_NEGATIVE: NEG-TURN-AUTHORITATIVE-DELIVERY-OBSTACLES, NEG-TURN-FRICTION-OBSTACLES"""
    delivery_missing = {
        "outcome": "ok",
        "transitions": {"task_status": {"from": "in_progress", "to": "in_review"}},
    }
    delivery_clean = {**delivery_missing, "obstacles": []}
    obstacle = [{"what": "Gate failed.", "root_cause": "Invalid state.", "resolution": "State repaired.", "recurrence_risk": "low"}]

    assert turn_validate.is_delivery_turn(delivery_missing)
    assert turn_validate.validate_delivery_obstacles(delivery_missing) == [DELIVERY_ERROR]
    assert turn_validate.validate_delivery_obstacles(delivery_clean) == []
    assert turn_validate.validate_delivery_obstacles({"outcome": "ok"}) == []

    with tempfile.TemporaryDirectory(prefix="runtime-turn-obstacles-") as temp:
        fixture_root = Path(temp)
        build_fixture_root(fixture_root)
        full_delivery = json.loads((ROOT / "examples/runtime_turn_cases/semantic_valid.json").read_text(encoding="utf-8"))
        full_delivery["outcome"] = "ok"
        full_delivery.pop("obstacles")
        full_errors = turn_validate.validate_turn(full_delivery, fixture_root)
        assert DELIVERY_ERROR in full_errors

        clean = json.loads((ROOT / "examples/runtime_turn_cases/semantic_valid.json").read_text(encoding="utf-8"))
        clean["obstacles"] = []
        assert turn_validate.validate_turn(clean, fixture_root) == []

        blocked_empty = {**clean, "outcome": "blocked", "transitions": {**clean["transitions"], "task_status": {"from": "in_progress", "to": "blocked"}}}
        blocked_with_obstacle = {**blocked_empty, "obstacles": obstacle}
        assert STATUS_ERROR in turn_validate.validate_turn(blocked_empty, fixture_root)
        assert STATUS_ERROR not in turn_validate.validate_turn(blocked_with_obstacle, fixture_root)

        review_empty = {
            **clean,
            "outcome": "blocked",
            "transitions": {
                **clean["transitions"],
                "task_status": {"from": "in_progress", "to": "blocked"},
                "review_qa": {"event": "assign_fix"},
            },
        }
        review_errors = turn_validate.validate_turn(review_empty, fixture_root)
        assert REVIEW_ERROR.replace("review_qa:assign_fix", "task_status:blocked, review_qa:assign_fix") in review_errors

        checks_empty = {
            **clean,
            "outcome": "blocked",
            "transitions": {
                **clean["transitions"],
                "review_qa": {
                    "event": "approve_review",
                    "checks_failed": [{"check_id": "gate", "error_class": "failure", "artifact_path": "runtime/gate.log"}],
                },
            },
        }
        assert CHECKS_ERROR in turn_validate.validate_turn(checks_empty, fixture_root)

        revert = {**clean, "actions": [{"type": "local_exec", "summary": "Reverted the failed change."}]}
        assert REVERT_ERROR in turn_validate.validate_turn(revert, fixture_root)

        first_attempt_0042 = {**clean, "attempt_id": "TASK-0259-codex-0042"}
        assert turn_validate.validate_turn(first_attempt_0042, fixture_root) == []

        original_friction = turn_validate.friction_sensors
        try:
            turn_validate.friction_sensors = lambda report: [
                sensor for sensor in original_friction(report) if not sensor.startswith("task_status:")
            ]
            assert STATUS_ERROR not in turn_validate.validate_turn(blocked_empty, fixture_root)

            turn_validate.friction_sensors = lambda report: [
                sensor for sensor in original_friction(report) if not sensor.startswith("review_qa:")
            ]
            mutated_review_errors = turn_validate.validate_turn(review_empty, fixture_root)
            assert all("review_qa:assign_fix" not in error for error in mutated_review_errors)

            turn_validate.friction_sensors = lambda report: [
                sensor for sensor in original_friction(report) if sensor != "review_qa:checks_failed"
            ]
            assert CHECKS_ERROR not in turn_validate.validate_turn(checks_empty, fixture_root)

            turn_validate.friction_sensors = lambda report: [
                sensor for sensor in original_friction(report) if sensor != "revert:action-summary-proxy"
            ]
            assert REVERT_ERROR not in turn_validate.validate_turn(revert, fixture_root)

            turn_validate.friction_sensors = lambda report: original_friction(report) + (
                ["attempt>1"] if report.get("attempt_id") == "TASK-0259-codex-0042" else []
            )
            assert ATTEMPT_ERROR in turn_validate.validate_turn(first_attempt_0042, fixture_root)
        finally:
            turn_validate.friction_sensors = original_friction

    original_delivery = turn_validate.is_delivery_turn
    try:
        turn_validate.is_delivery_turn = lambda report: False
        assert turn_validate.validate_delivery_obstacles(delivery_missing) == []
    finally:
        turn_validate.is_delivery_turn = original_delivery

    print("OK: authoritative delivery and in-schema friction controls are mutation-proved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
