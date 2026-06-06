#!/usr/bin/env python3
"""Golden cases for runtime event log, replay, idempotency and fencing."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from runtime.eventlog import (  # noqa: E402
    EventLogError,
    EventWriter,
    assert_snapshot_matches,
    canonical_hash,
    read_jsonl_torn_safe,
    rebuild_snapshot,
    replay_without_side_effects,
)


def case_seq_writer_only_and_torn_write() -> None:
    with tempfile.TemporaryDirectory(prefix="eventlog-seq-") as temp:
        root = Path(temp)
        writer = EventWriter(root)
        first = writer.acquire_claim(
            task_id="TASK-1000",
            owner="Codex",
            lease_until="2026-06-06T12:30:00Z",
            idempotency_key="Codex:TASK-1000:claim:attempt-1:0",
        )
        second = writer.apply_intent(
            task_id="TASK-1000",
            actor_id="Codex",
            transition="submit",
            attempt_id="attempt-1",
            fencing_token=int(first["fencing_token"]),
        )
        assert first["seq"] == 1
        assert second["seq"] == 2
        with writer.log_path.open("a", encoding="utf-8") as handle:
            handle.write('{"seq":')
        assert [event["seq"] for event in read_jsonl_torn_safe(writer.log_path)] == [1, 2]


def case_idempotency_before_and_after_compaction() -> None:
    with tempfile.TemporaryDirectory(prefix="eventlog-idem-") as temp:
        root = Path(temp)
        writer = EventWriter(root)
        claim = writer.acquire_claim(
            task_id="TASK-1001",
            owner="Codex",
            lease_until="2026-06-06T12:30:00Z",
            idempotency_key="Codex:TASK-1001:claim:attempt-1:0",
        )
        first = writer.apply_intent(
            task_id="TASK-1001",
            actor_id="Codex",
            transition="submit",
            attempt_id="attempt-1",
            fencing_token=int(claim["fencing_token"]),
        )
        duplicate = writer.apply_intent(
            task_id="TASK-1001",
            actor_id="Codex",
            transition="submit",
            attempt_id="attempt-1",
            fencing_token=int(claim["fencing_token"]),
        )
        assert duplicate["seq"] == first["seq"]
        assert duplicate["deduped"] is True
        writer.write_snapshot()
        writer.compact_through(int(first["seq"]))
        duplicate_after_compaction = writer.apply_intent(
            task_id="TASK-1001",
            actor_id="Codex",
            transition="submit",
            attempt_id="attempt-1",
            fencing_token=int(claim["fencing_token"]),
        )
        assert duplicate_after_compaction["seq"] == first["seq"]
        assert duplicate_after_compaction["deduped"] is True
        assert len([event for event in writer.events() if event["type"] == "intent.applied"]) == 1


def case_lease_reclaim_and_stale_fencing_rejection() -> None:
    with tempfile.TemporaryDirectory(prefix="eventlog-fence-") as temp:
        root = Path(temp)
        writer = EventWriter(root)
        stale = writer.acquire_claim(
            task_id="TASK-1002",
            owner="Codex",
            lease_until="2026-06-06T12:30:00Z",
            idempotency_key="Codex:TASK-1002:claim:attempt-1:0",
        )
        fresh = writer.acquire_claim(
            task_id="TASK-1002",
            owner="Builder",
            lease_until="2026-06-06T13:00:00Z",
            idempotency_key="Builder:TASK-1002:claim:attempt-2:1",
        )
        assert fresh["fencing_token"] > stale["fencing_token"]
        rejected = writer.apply_intent(
            task_id="TASK-1002",
            actor_id="Codex",
            transition="submit",
            attempt_id="attempt-1",
            fencing_token=int(stale["fencing_token"]),
        )
        assert rejected["type"] == "state.stale_fencing_rejected"
        assert rejected["applied"] is False
        state = writer.state()
        assert state["aggregate_versions"]["TASK-1002"] == fresh["aggregate_version"]
        assert state["rejections"][0]["current_fencing_token"] == fresh["fencing_token"]


def case_snapshot_replay_hash_and_mismatch_gate() -> None:
    with tempfile.TemporaryDirectory(prefix="eventlog-snapshot-") as temp:
        root = Path(temp)
        writer = EventWriter(root)
        claim = writer.acquire_claim(
            task_id="TASK-1003",
            owner="Codex",
            lease_until="2026-06-06T12:30:00Z",
            idempotency_key="Codex:TASK-1003:claim:attempt-1:0",
        )
        writer.apply_intent(
            task_id="TASK-1003",
            actor_id="Codex",
            transition="submit",
            attempt_id="attempt-1",
            fencing_token=int(claim["fencing_token"]),
        )
        snapshot = writer.write_snapshot()
        rebuilt = rebuild_snapshot(root)
        assert canonical_hash(snapshot["state"]) == canonical_hash(rebuilt["state"])
        assert_snapshot_matches(root)
        snapshot_path = root / "runtime" / "state" / "snapshot.json"
        mutated = json.loads(snapshot_path.read_text(encoding="utf-8-sig"))
        mutated["state"]["aggregate_versions"]["TASK-1003"] = 999
        snapshot_path.write_text(json.dumps(mutated, indent=2), encoding="utf-8")
        try:
            assert_snapshot_matches(root)
        except EventLogError:
            return
        raise AssertionError("snapshot mismatch was accepted")


def case_negative_replay_does_not_call_external_effects() -> None:
    with tempfile.TemporaryDirectory(prefix="eventlog-negative-replay-") as temp:
        root = Path(temp)
        writer = EventWriter(root)
        writer.acquire_claim(
            task_id="TASK-1004",
            owner="Codex",
            lease_until="2026-06-06T12:30:00Z",
            idempotency_key="Codex:TASK-1004:claim:attempt-1:0",
        )

        def forbidden() -> None:
            raise AssertionError("replay invoked an external effect")

        before = rebuild_snapshot(root)
        after = replay_without_side_effects(root, forbidden)
        assert canonical_hash(before["state"]) == canonical_hash(after["state"])


def main() -> int:
    cases = [
        case_seq_writer_only_and_torn_write,
        case_idempotency_before_and_after_compaction,
        case_lease_reclaim_and_stale_fencing_rejection,
        case_snapshot_replay_hash_and_mismatch_gate,
        case_negative_replay_does_not_call_external_effects,
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
    print(f"OK: {len(cases)} runtime event log golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
