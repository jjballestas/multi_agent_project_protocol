from __future__ import annotations

import json
import shutil
import unittest
import uuid
from pathlib import Path
from unittest.mock import patch

from runtime.eventlog import EventWriter, canonical_hash, read_jsonl_torn_safe
from runtime.protocol_replay import validate_chain


ROOT = Path(__file__).resolve().parents[1]


class SubmitIntentStateOnceTests(unittest.TestCase):
    def make_root(self) -> Path:
        parent = Path("D:/Aegis_Scratch/multi_agent_project_protocol/task0305-tests")
        parent.mkdir(parents=True, exist_ok=True)
        root = parent / uuid.uuid4().hex
        root.mkdir()
        self.addCleanup(shutil.rmtree, root, True)
        shutil.copy2(ROOT / "protocol.config.json", root / "protocol.config.json")
        shutil.copytree(ROOT / "secrets", root / "secrets")
        return root

    @staticmethod
    def append_sequence(writer: EventWriter, state: dict | None) -> list[dict]:
        events = []
        for index, aggregate in enumerate(("TASK-A", "TASK-A", "TASK-B"), start=1):
            kwargs = {"verified_state": state} if state is not None else {}
            events.append(
                writer.append_event(
                    event_type="intent.applied",
                    aggregate_id=aggregate,
                    actor_id="Codex",
                    idempotency_key=f"task0305:{index}",
                    payload={"index": index},
                    ts="2026-07-29T20:30:00Z",
                    **kwargs,
                )
            )
        return events

    def test_differential_output_is_byte_identical_and_chain_valid(self) -> None:
        legacy_root, optimized_root = self.make_root(), self.make_root()
        legacy, optimized = EventWriter(legacy_root), EventWriter(optimized_root)

        legacy_events = self.append_sequence(legacy, None)
        optimized_state = optimized.state()
        optimized_events = self.append_sequence(optimized, optimized_state)

        self.assertEqual(legacy_events, optimized_events)
        self.assertEqual(
            (legacy_root / "runtime/state/events.jsonl").read_bytes(),
            (optimized_root / "runtime/state/events.jsonl").read_bytes(),
        )
        legacy_snapshot = legacy.write_snapshot()
        optimized_snapshot = optimized.write_snapshot(optimized_state)
        self.assertEqual(legacy_snapshot, optimized_snapshot)
        self.assertEqual(
            (legacy_root / "runtime/state/snapshot.json").read_bytes(),
            (optimized_root / "runtime/state/snapshot.json").read_bytes(),
        )
        config = json.loads((optimized_root / "protocol.config.json").read_text(encoding="utf-8"))
        self.assertTrue(validate_chain(optimized.events(), config, root=optimized_root)["valid"])
        self.assertEqual(optimized_events[1]["aggregate_version"], 2)

    def test_one_full_state_verification_and_tamper_detection(self) -> None:
        root = self.make_root()
        writer = EventWriter(root)
        original_state = EventWriter.state
        calls = 0

        def counted_state(instance: EventWriter) -> dict:
            nonlocal calls
            calls += 1
            return original_state(instance)

        with patch.object(EventWriter, "state", counted_state):
            state = writer.state()
            self.append_sequence(writer, state)
            writer.write_snapshot(state)
        self.assertEqual(calls, 1)

        events = read_jsonl_torn_safe(writer.log_path)
        events[-1]["payload"]["index"] = 999
        writer.log_path.write_text(
            "".join(json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for event in events),
            encoding="utf-8",
        )
        tampered = original_state(writer)
        self.assertTrue(any(item.get("event") == "security.unauthenticated_event" for item in tampered["rejections"]))
        self.assertNotEqual(canonical_hash(tampered), canonical_hash(state))


if __name__ == "__main__":
    unittest.main()
