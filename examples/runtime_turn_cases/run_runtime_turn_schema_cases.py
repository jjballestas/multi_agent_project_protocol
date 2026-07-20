#!/usr/bin/env python3
"""Schema golden cases for runtime turn reports."""

from __future__ import annotations

import json
from pathlib import Path

import jsonschema

ROOT = Path(__file__).resolve().parents[2]


EXPECTED = {
    "valid_in_review.json": True,
    "valid_human_required.json": True,
    "valid_obstacles_populated.json": True,
    "valid_obstacles_empty.json": True,
    "invalid_missing_required.json": False,
    "invalid_human_gate.json": False,
    "invalid_empty_agent.json": False,
    "invalid_obstacle_malformed.json": False,
}


def main() -> int:
    schema = json.loads((ROOT / "runtime" / "turn_schema.json").read_text(encoding="utf-8-sig"))
    validator = jsonschema.Draft7Validator(schema)
    failures = []

    for name, expected_valid in EXPECTED.items():
        report = json.loads((ROOT / "examples" / "runtime_turn_cases" / name).read_text(encoding="utf-8-sig"))
        errors = sorted(validator.iter_errors(report), key=lambda item: list(item.path))
        actual_valid = not errors
        if actual_valid != expected_valid:
            failures.append(
                {"case": name, "expected_valid": expected_valid, "errors": [error.message for error in errors]}
            )

    if failures:
        print(json.dumps({"status": "FAILED", "failures": failures}, indent=2))
        return 1
    print(f"OK: {len(EXPECTED)} schema turn golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
