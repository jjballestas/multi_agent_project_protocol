#!/usr/bin/env python3
"""Regression tests for exception.recorded intents."""

from __future__ import annotations

import json
import shutil
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

import sys

sys.path.insert(0, str(ROOT))

from runtime.protocol_replay import exception_recorded_events, protocol_state_drift
from runtime.submit_intent import IntentValidationError, submit_intent


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="ascii", newline="\n")


def base_instance(root: Path) -> None:
    write(
        root / "protocol.config.json",
        json.dumps(
            {
                "schema_version": "1.0",
                "protocol_version": "1.14.0",
                "project_name": "exception_case",
                "adoption_tier": "coordination",
                "agent_registry": {
                    "enabled": True,
                    "agents": [{"id": "implementer_agent", "enabled": True, "capabilities": ["implementer"]}],
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
                        "id": "TASK-0239",
                        "file": "Area_comun/tasks/task-0239.md",
                        "owner": "implementer_agent",
                        "status": "in_progress",
                        "type": "build",
                    }
                ],
            },
            indent=2,
        )
        + "\n",
    )
    write(
        root / "Area_comun/state/CLAIMS.json",
        json.dumps(
            {
                "schema_version": "1.0",
                "claims": [
                    {
                        "claim_id": "CLAIM-test",
                        "owner": "implementer_agent",
                        "task_id": "TASK-0239",
                        "status": "active",
                        "scope": ["Area_comun/state/CLAIMS.json#CLAIM-test"],
                    }
                ],
            },
            indent=2,
        )
        + "\n",
    )
    write(
        root / "Area_comun/tasks/task-0239.md",
        "---\ntask_id: TASK-0239\nstatus: in_progress\nowner: implementer_agent\nfile: Area_comun/tasks/task-0239.md\n---\n",
    )


def exception_payload(exception_id: str, kind: str = "assist", task_id: str | None = "TASK-0239") -> dict[str, object]:
    return {
        "type": "exception",
        "exception_id": exception_id,
        "kind": kind,
        "task_id": task_id,
        "actor": "implementer_agent",
        "beneficiary": "reviewer_agent",
        "summary": "Recorded assistance for deterministic fixture.",
        "channel": "mailbox",
        "impact": "time",
        "publishable": True,
    }


def exceptions_for_task(root: Path, task_id: str) -> list[dict[str, object]]:
    return exception_recorded_events(root, task_id)


class ExceptionRecordedTests(unittest.TestCase):
    def setUp(self) -> None:
        self.root = Path(tempfile.mkdtemp(prefix="exception-recorded-"))
        self.addCleanup(lambda: shutil.rmtree(self.root, ignore_errors=True))
        base_instance(self.root)

    def submit(self, payload: dict[str, object]) -> dict[str, object]:
        return submit_intent(self.root, "implementer_agent", payload, timestamp="2026-07-02T00:00:00Z", commit="test")

    def test_rejects_kind_outside_enum(self) -> None:
        with self.assertRaisesRegex(IntentValidationError, "kind out of range"):
            self.submit(exception_payload("EXC-bad-kind", kind="free_text"))

    def test_rejects_non_ascii_summary(self) -> None:
        payload = exception_payload("EXC-non-ascii")
        payload["summary"] = "Resumen con acento: á"
        with self.assertRaisesRegex(IntentValidationError, "summary must be ASCII"):
            self.submit(payload)

    def test_rejects_duplicate_exception_id(self) -> None:
        self.submit(exception_payload("EXC-duplicate"))
        payload = exception_payload("EXC-duplicate")
        payload["idempotency_key"] = "different-key"
        with self.assertRaisesRegex(IntentValidationError, "exception_id already exists"):
            self.submit(payload)

    def test_rejects_missing_task_id(self) -> None:
        with self.assertRaisesRegex(IntentValidationError, "task not found"):
            self.submit(exception_payload("EXC-missing-task", task_id="TASK-9999"))

    def test_round_trip_two_events_listable_by_task_with_zero_drift(self) -> None:
        self.submit(exception_payload("EXC-assist", kind="assist"))
        self.submit(exception_payload("EXC-arbitration", kind="arbitration"))

        recorded = exceptions_for_task(self.root, "TASK-0239")
        self.assertEqual(["EXC-assist", "EXC-arbitration"], [event["payload"]["exception_id"] for event in recorded])
        self.assertTrue(all(event.get("actor_auth") for event in recorded))
        self.assertFalse(protocol_state_drift(self.root)["has_drift"])


if __name__ == "__main__":
    unittest.main()
