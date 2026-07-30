#!/usr/bin/env python3
"""Golden cases for runtime event log, replay, idempotency and fencing."""

from __future__ import annotations

import json
import hashlib
import sys
import tempfile
from copy import deepcopy
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from runtime.eventlog import (  # noqa: E402
    EventLogError,
    EventWriter,
    archive_hash_path,
    archive_integrity,
    assert_snapshot_matches,
    canonical_json,
    canonical_hash,
    read_jsonl_torn_safe,
    rebuild_snapshot,
    replay_events,
    replay_without_side_effects,
    verify_event_auth,
    verify_snapshot_checkpoint,
)
from runtime.protocol_replay import validate_chain  # noqa: E402


def checkpoint_fixture(root: Path) -> EventWriter:
    (root / "secrets").mkdir(parents=True)
    (root / "secrets" / "runtime.key").write_text("runtime-fixture-secret", encoding="ascii")
    (root / "secrets" / "codex.key").write_text("codex-fixture-secret", encoding="ascii")
    config = {
        "event_auth": {
            "enabled": True,
            "method": "hmac-sha256",
            "keys": {
                "runtime": {
                    "key_id": "runtime-hmac:v1",
                    "secret_file": "secrets/runtime.key",
                },
                "Codex": {
                    "key_id": "codex-hmac:v1",
                    "secret_file": "secrets/codex.key",
                },
            },
        },
        "event_state": {"chain_enabled": True},
    }
    (root / "protocol.config.json").write_text(
        json.dumps(config, indent=2, sort_keys=True),
        encoding="ascii",
    )
    (root / "runtime").mkdir(parents=True, exist_ok=True)
    (root / "runtime" / "CHECKPOINT_POLICY.json").write_text(
        json.dumps({"max_incremental_events": 8, "compaction_threshold": 1024}, indent=2),
        encoding="ascii",
    )
    return EventWriter(root)


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


def case_signed_checkpoint_incremental_and_fail_safe() -> None:
    with tempfile.TemporaryDirectory(prefix="eventlog-checkpoint-") as temp:
        root = Path(temp)
        writer = checkpoint_fixture(root)
        claim = writer.acquire_claim(
            task_id="TASK-1005",
            owner="Codex",
            lease_until="2026-06-06T12:30:00Z",
            idempotency_key="Codex:TASK-1005:claim:attempt-1:0",
        )
        writer.apply_intent(
            task_id="TASK-1005",
            actor_id="Codex",
            transition="submit",
            attempt_id="attempt-1",
            fencing_token=int(claim["fencing_token"]),
        )
        snapshot = writer.write_snapshot()
        assert snapshot["integrity"]["key_id"] == "runtime-hmac:v1"
        assert verify_snapshot_checkpoint(root, snapshot, writer.events())["trusted"] is True

        writer.apply_intent(
            task_id="TASK-1005",
            actor_id="Codex",
            transition="review",
            attempt_id="attempt-2",
            fencing_token=int(claim["fencing_token"]),
        )
        events = writer.events()
        full_state = replay_events(events, config=json.loads((root / "protocol.config.json").read_text()), root=root)
        original_verify = verify_event_auth
        verified_seqs: list[int] = []

        def counting_verify(event, config, *, root=None):
            verified_seqs.append(int(event.get("seq") or 0))
            return original_verify(event, config, root=root)

        with patch("runtime.eventlog.verify_event_auth", counting_verify):
            incremental_state = writer.state()
        assert verified_seqs == [int(events[-1]["seq"])]
        assert canonical_json(incremental_state) == canonical_json(full_state)
        incremental_snapshot = writer.write_snapshot(incremental_state)
        full_snapshot = {
            "up_to_seq": int(events[-1]["seq"]),
            "state": full_state,
            "canonical_hash": canonical_hash(full_state),
        }
        assert canonical_json(
            {key: incremental_snapshot[key] for key in full_snapshot}
        ) == canonical_json(full_snapshot)

        snapshot_path = root / "runtime" / "state" / "snapshot.json"
        valid = json.loads(snapshot_path.read_text(encoding="utf-8"))
        fail_safe_cases = []

        bad_signature = deepcopy(valid)
        bad_signature["integrity"]["signature"] = "0" * 64
        fail_safe_cases.append(("invalid_signature", bad_signature, None))

        bad_state = deepcopy(valid)
        bad_state["state"]["aggregate_versions"]["TASK-1005"] = 999
        fail_safe_cases.append(("state_hash_mismatch", bad_state, None))

        stale = deepcopy(valid)
        fail_safe_cases.append(("stale_checkpoint", stale, -1))

        for expected_reason, candidate, limit in fail_safe_cases:
            snapshot_path.write_text(json.dumps(candidate, indent=2, sort_keys=True), encoding="utf-8")
            verdict = verify_snapshot_checkpoint(
                root,
                candidate,
                events,
                max_incremental_events=limit,
            )
            assert verdict == {"trusted": False, "reason": expected_reason}
            verified_seqs.clear()
            runtime_override = {"max_incremental_events": limit if limit is not None else 8}
            (root / "runtime" / "CHECKPOINT_POLICY.json").write_text(
                json.dumps(runtime_override, indent=2),
                encoding="ascii",
            )
            with patch("runtime.eventlog.verify_event_auth", counting_verify):
                writer.state()
            assert verified_seqs == [int(event["seq"]) for event in events], (
                expected_reason,
                verified_seqs,
                [int(event["seq"]) for event in events],
            )

        snapshot_path.write_text(json.dumps(valid, indent=2, sort_keys=True), encoding="utf-8")
        (root / "runtime" / "CHECKPOINT_POLICY.json").write_text(
            json.dumps({"max_incremental_events": 8}, indent=2),
            encoding="ascii",
        )
        tampered_events = deepcopy(events)
        tampered_events[0]["payload"]["owner"] = "Mallory"
        assert verify_snapshot_checkpoint(root, valid, tampered_events)["trusted"] is True
        assert validate_chain(tampered_events, json.loads((root / "protocol.config.json").read_text()), root=root)["valid"] is False


def case_checkpoint_compaction_preserves_union_and_offline_audit() -> None:
    with tempfile.TemporaryDirectory(prefix="eventlog-compaction-") as temp:
        root = Path(temp)
        writer = checkpoint_fixture(root)
        policy_path = root / "runtime" / "CHECKPOINT_POLICY.json"
        policy_path.write_text(
            json.dumps({"max_incremental_events": 8, "compaction_threshold": 1}, indent=2),
            encoding="ascii",
        )
        claim = writer.acquire_claim(
            task_id="TASK-1006",
            owner="Codex",
            lease_until="2026-06-06T12:30:00Z",
            idempotency_key="Codex:TASK-1006:claim:attempt-1:0",
        )
        writer.apply_intent(
            task_id="TASK-1006",
            actor_id="Codex",
            transition="submit",
            attempt_id="attempt-1",
            fencing_token=int(claim["fencing_token"]),
        )
        before = writer.events()
        before_state = replay_events(
            before,
            config=json.loads((root / "protocol.config.json").read_text()),
            root=root,
        )
        writer.write_snapshot(before_state)
        archives = sorted((root / "runtime" / "state" / "archives").glob("events-*.jsonl"))
        assert len(archives) == 1
        assert archive_integrity(root) == {"valid": True, "checked": 1}
        assert read_jsonl_torn_safe(writer.log_path) == []
        after = writer.events()
        assert canonical_json(after) == canonical_json(before)
        after_state = replay_events(
            after,
            config=json.loads((root / "protocol.config.json").read_text()),
            root=root,
        )
        assert canonical_hash(after_state) == canonical_hash(before_state)
        assert validate_chain(
            after,
            json.loads((root / "protocol.config.json").read_text()),
            root=root,
        )["valid"] is True

        writer.apply_intent(
            task_id="TASK-1006",
            actor_id="Codex",
            transition="review",
            attempt_id="attempt-2",
            fencing_token=int(claim["fencing_token"]),
        )
        full_events = writer.events()
        full_state = replay_events(
            full_events,
            config=json.loads((root / "protocol.config.json").read_text()),
            root=root,
        )
        verified_seqs: list[int] = []
        original_verify = verify_event_auth

        def counting_verify(event, config, *, root=None):
            verified_seqs.append(int(event.get("seq") or 0))
            return original_verify(event, config, root=root)

        with patch("runtime.eventlog.verify_event_auth", counting_verify):
            incremental_state = writer.state()
        assert verified_seqs == [int(full_events[-1]["seq"])]
        assert canonical_json(incremental_state) == canonical_json(full_state)

        archive_payload = read_jsonl_torn_safe(archives[0])
        archive_payload[0]["payload"]["owner"] = "Mallory"
        archives[0].write_text(
            "".join(canonical_json(event) + "\n" for event in archive_payload),
            encoding="utf-8",
        )
        assert archive_integrity(root)["valid"] is False
        verified_seqs.clear()
        with patch("runtime.eventlog.verify_event_auth", counting_verify):
            writer.state()
        assert verified_seqs == [int(event["seq"]) for event in writer.events()]
        assert validate_chain(
            writer.events(),
            json.loads((root / "protocol.config.json").read_text()),
            root=root,
        )["valid"] is False

        archive_hash_path(archives[0]).write_text(
            hashlib.sha256(archives[0].read_bytes()).hexdigest() + "\n",
            encoding="ascii",
        )
        assert archive_integrity(root)["valid"] is True
        assert validate_chain(
            writer.events(),
            json.loads((root / "protocol.config.json").read_text()),
            root=root,
        )["valid"] is False

        malformed_snapshot = json.loads(
            (root / "runtime" / "state" / "snapshot.json").read_text(encoding="utf-8")
        )
        malformed_snapshot["up_to_seq"] = "not-a-number"
        assert verify_snapshot_checkpoint(root, malformed_snapshot, writer.events()) == {
            "trusted": False,
            "reason": "invalid_checkpoint_sequence",
        }
        policy_path.write_text(
            json.dumps(
                {"max_incremental_events": "not-a-number", "compaction_threshold": 1024},
                indent=2,
            ),
            encoding="ascii",
        )
        valid_snapshot = json.loads(
            (root / "runtime" / "state" / "snapshot.json").read_text(encoding="utf-8")
        )
        assert verify_snapshot_checkpoint(root, valid_snapshot, writer.events()) == {
            "trusted": False,
            "reason": "invalid_checkpoint_policy",
        }


def main() -> int:
    cases = [
        case_seq_writer_only_and_torn_write,
        case_idempotency_before_and_after_compaction,
        case_lease_reclaim_and_stale_fencing_rejection,
        case_snapshot_replay_hash_and_mismatch_gate,
        case_negative_replay_does_not_call_external_effects,
        case_signed_checkpoint_incremental_and_fail_safe,
        case_checkpoint_compaction_preserves_union_and_offline_audit,
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
