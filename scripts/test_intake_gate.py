#!/usr/bin/env python3
"""Regression tests for the deterministic task intake gate."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

import sys

sys.path.insert(0, str(ROOT))

from runtime.submit_intent import IntentValidationError, submit_intent
from scripts.validate_collaboration_state import validate


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="ascii", newline="\n")


def base_instance(root: Path, *, task_id: str, status: str, task_body: str, events: str = "") -> None:
    write(
        root / "protocol.config.json",
        json.dumps(
            {
                "schema_version": "1.0",
                "protocol_version": "1.14.0",
                "project_name": "intake_gate_case",
                "adoption_tier": "coordination",
                "agent_registry": {
                    "enabled": True,
                    "agents": [{"id": "implementer_agent", "enabled": True, "capabilities": ["implementer"]}],
                },
                "intake_gate": {
                    "enabled": True,
                    "start_task_id": "TASK-0238",
                    "enforcement": "post_start_ready_requires_intake",
                },
                "state_invariants": [{"path": "status", "equals": "active"}],
            },
            indent=2,
        )
        + "\n",
    )
    write(root / "Area_comun/state/PROJECT_STATE.json", '{"status":"active","active_tasks":[],"decisions":[]}\n')
    write(
        root / "Area_comun/state/TASK_INDEX.json",
        json.dumps(
            {
                "schema_version": "1.0",
                "tasks": [
                    {
                        "id": task_id,
                        "file": f"Area_comun/tasks/{task_id.lower()}.md",
                        "owner": "implementer_agent",
                        "status": status,
                        "type": "build",
                    }
                ],
            },
            indent=2,
        )
        + "\n",
    )
    write(root / "Area_comun/state/CLAIMS.json", '{"schema_version":"1.0","claims":[]}\n')
    write(root / "Area_comun/tasks" / f"{task_id.lower()}.md", task_body)
    for folder in ("open", "answered", "archived"):
        write(root / "Area_comun/mailbox" / folder / ".gitkeep", "")
    write(root / "Area_comun/reports/HUMAN_REPORT_TEMPLATE.md", "# Report\n")
    if events:
        write(root / "runtime/state/events.jsonl", events)


VALID_INTAKE = """intake:
  type: feature
  goal: Deterministic ready gate.
  acceptance:
    - Validator accepts complete intake.
  verification_cmd:
    - python scripts/validate_collaboration_state.py --root .
  scope_routes:
    - Area_comun/tasks/
  out_of_scope:
    - Runtime state manual edits.
  risk: low
  estimate: S
"""


def task_markdown(task_id: str, status: str, intake: str = "") -> str:
    return f"""---
task_id: {task_id}
status: {status}
owner: implementer_agent
type: build
file: Area_comun/tasks/{task_id.lower()}.md
{intake}---

# {task_id}
"""


class IntakeGateTests(unittest.TestCase):
    def run_case(self, task_id: str, status: str, intake: str = "", events: str = ""):
        temp = Path(tempfile.mkdtemp(prefix="intake-gate-"))
        self.addCleanup(lambda: shutil.rmtree(temp, ignore_errors=True))
        base_instance(temp, task_id=task_id, status=status, task_body=task_markdown(task_id, status, intake), events=events)
        return validate(temp)

    def test_p1_proposed_without_intake_validates(self) -> None:
        self.assertFalse(self.run_case("TASK-0239", "proposed").errors)

    def test_p2_ready_with_complete_intake_validates(self) -> None:
        self.assertFalse(self.run_case("TASK-0239", "ready", VALID_INTAKE).errors)

    def test_p3_ready_with_recorded_exception_validates(self) -> None:
        intake = "intake:\n  intake_exempt: true\n  exception_ref: 1\n"
        self.assertFalse(self.run_case("TASK-0239", "ready", intake).errors)

    def test_p4_pre_start_task_without_intake_validates(self) -> None:
        self.assertFalse(self.run_case("TASK-0238", "done").errors)

    def test_p5_post_start_in_review_with_intake_validates(self) -> None:
        self.assertFalse(self.run_case("TASK-0239", "in_review", VALID_INTAKE).errors)

    def test_n1_ready_without_intake_fails(self) -> None:
        self.assertIn("missing intake block", "\n".join(self.run_case("TASK-0239", "ready").errors))

    def test_n2_empty_goal_fails(self) -> None:
        bad = VALID_INTAKE.replace("  goal: Deterministic ready gate.", "  goal: ''")
        self.assertIn("goal", "\n".join(self.run_case("TASK-0239", "ready", bad).errors))

    def test_n3_placeholder_acceptance_fails(self) -> None:
        bad = VALID_INTAKE.replace("    - Validator accepts complete intake.", "    - TBD")
        self.assertIn("acceptance", "\n".join(self.run_case("TASK-0239", "ready", bad).errors))

    def test_n4_bad_risk_fails(self) -> None:
        bad = VALID_INTAKE.replace("  risk: low", "  risk: severe")
        self.assertIn("risk", "\n".join(self.run_case("TASK-0239", "ready", bad).errors))

    def test_n5_exempt_without_exception_ref_fails(self) -> None:
        errors = self.run_case("TASK-0239", "ready", "intake:\n  intake_exempt: true\n").errors
        self.assertIn("exception_ref", "\n".join(errors))

    def test_n6_submit_intent_rejects_invalid_ready_transition_atomically(self) -> None:
        temp = Path(tempfile.mkdtemp(prefix="intake-submit-"))
        self.addCleanup(lambda: shutil.rmtree(temp, ignore_errors=True))
        base_instance(temp, task_id="TASK-0239", status="proposed", task_body=task_markdown("TASK-0239", "proposed"))
        claims = {
            "schema_version": "1.0",
            "claims": [
                {
                    "claim_id": "CLAIM-test",
                    "owner": "implementer_agent",
                    "task_id": "TASK-0239",
                    "status": "active",
                    "scope": [
                        "Area_comun/state/TASK_INDEX.json#TASK-0239",
                        "Area_comun/state/PROJECT_STATE.json#active_tasks/TASK-0239",
                        "Area_comun/tasks/task-0239.md",
                    ],
                }
            ],
        }
        write(temp / "Area_comun/state/CLAIMS.json", json.dumps(claims, indent=2) + "\n")
        with self.assertRaises(IntentValidationError):
            submit_intent(
                temp,
                "implementer_agent",
                {"type": "task_status", "task_id": "TASK-0239", "from": "proposed", "to": "ready"},
                timestamp="2026-07-02T00:00:00Z",
                commit="test",
            )
        state = json.loads((temp / "Area_comun/state/TASK_INDEX.json").read_text(encoding="utf-8"))
        self.assertEqual(state["tasks"][0]["status"], "proposed")


if __name__ == "__main__":
    unittest.main()
