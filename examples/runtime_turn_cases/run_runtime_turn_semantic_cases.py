#!/usr/bin/env python3
"""Semantic golden cases for runtime turn validation."""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from runtime.turn_validate import load_report, validate_turn  # noqa: E402


EXPECTED = {
    "semantic_valid.json": True,
    "semantic_out_of_allowlist.json": False,
    "semantic_stale_from.json": False,
    "semantic_third_agent_valid.json": True,
    "semantic_unregistered_agent.json": False,
}


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def build_fixture_root(target: Path) -> None:
    (target / "runtime").mkdir(parents=True)
    shutil.copy2(ROOT / "runtime" / "turn_schema.json", target / "runtime" / "turn_schema.json")
    write_json(target / "Area_comun" / "state" / "PROJECT_STATE.json", {"status": "active"})
    write_json(
        target / "Area_comun" / "state" / "TASK_INDEX.json",
        {
            "tasks": [
                {
                    "id": "TASK-0099",
                    "owner": "Codex",
                    "status": "in_progress",
                    "priority": "high",
                    "file": "Area_comun/tasks/TASK-0099.md",
                },
                {
                    "id": "TASK-0100",
                    "owner": "Builder",
                    "status": "in_progress",
                    "priority": "normal",
                    "file": "Area_comun/tasks/TASK-0100.md",
                }
            ]
        },
    )
    write_json(
        target / "Area_comun" / "state" / "CLAIMS.json",
        {
            "claims": [
                {
                    "claim_id": "CLAIM-TASK-0099-codex",
                    "task_id": "TASK-0099",
                    "owner": "Codex",
                    "status": "active",
                    "scope": [
                        "runtime/",
                        "Area_comun/tasks/TASK-0099.md",
                        "Area_comun/state/TASK_INDEX.json#TASK-0099",
                        "Area_comun/state/PROJECT_STATE.json#active_tasks/TASK-0099",
                        "Area_comun/state/CLAIMS.json",
                    ],
                },
                {
                    "claim_id": "CLAIM-TASK-0100-builder",
                    "task_id": "TASK-0100",
                    "owner": "Builder",
                    "status": "active",
                    "scope": [
                        "runtime/",
                        "Area_comun/tasks/TASK-0100.md",
                        "Area_comun/state/TASK_INDEX.json#TASK-0100",
                        "Area_comun/state/PROJECT_STATE.json#active_tasks/TASK-0100",
                        "Area_comun/state/CLAIMS.json",
                    ],
                }
            ]
        },
    )
    write_json(
        target / "protocol.config.json",
        {
            "agent_registry": {
                "enabled": True,
                "agents": [
                    {"id": "Claude", "capabilities": ["architect", "reviewer", "orchestrator", "qa"], "enabled": True},
                    {"id": "Codex", "capabilities": ["implementer", "test_engineer"], "enabled": True},
                    {"id": "Builder", "capabilities": ["implementer"], "enabled": True},
                    {"id": "DisabledBuilder", "capabilities": ["implementer"], "enabled": False},
                    {"id": "ReviewerOnly", "capabilities": ["reviewer"], "enabled": True},
                ],
            }
        },
    )
    (target / "Area_comun" / "mailbox" / "open").mkdir(parents=True)


def main() -> int:
    failures = []
    with tempfile.TemporaryDirectory(prefix="runtime-turn-cases-") as temp:
        fixture_root = Path(temp)
        build_fixture_root(fixture_root)
        for name, expected_valid in EXPECTED.items():
            errors = validate_turn(load_report(ROOT / "examples" / "runtime_turn_cases" / name), fixture_root)
            actual_valid = not errors
            if actual_valid != expected_valid:
                failures.append({"case": name, "expected_valid": expected_valid, "errors": errors})

    if failures:
        print(json.dumps({"status": "FAILED", "failures": failures}, indent=2))
        return 1
    print(f"OK: {len(EXPECTED)} semantic turn golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
