#!/usr/bin/env python3
"""Golden cases for eventlog prev_hash chaining."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.eventlog import EventWriter, atomic_append_jsonl, compute_event_prev_hash, compute_genesis_prev_hash
from runtime.protocol_replay import validate_chain
from runtime.temp_paths import make_root_temp_dir, remove_root_temp_dir


BASE_CONFIG: dict[str, Any] = {
    "schema_version": "1.0",
    "adoption_tier": "runtime",
    "event_state": {"enabled": True, "materialize": True, "enforce": True, "authoritative": True, "chain_enabled": True},
}
LEGACY_CONFIG: dict[str, Any] = {
    "schema_version": "1.0",
    "adoption_tier": "runtime",
    "event_state": {"enabled": True, "materialize": True, "enforce": True, "authoritative": True, "chain_enabled": False},
}


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=True, sort_keys=True, indent=2) + "\n", encoding="ascii")


def event(seq: int, value: str) -> dict[str, Any]:
    return {
        "seq": seq,
        "event_schema_version": "1.0",
        "type": "intent.applied",
        "aggregate_id": "TASK-GOLDEN",
        "aggregate_version": seq,
        "actor": "Codex",
        "actor_auth": {"method": "not_enforced_phase2"},
        "idempotency_key": f"golden:{seq}",
        "fencing_token": None,
        "payload": {"value": value},
        "applied": True,
        "ts": f"2026-06-13T00:00:{seq:02d}Z",
    }


def chained_events(tmp: Path, count: int = 10) -> list[dict[str, Any]]:
    write_json(tmp / "protocol.config.json", BASE_CONFIG)
    previous = compute_genesis_prev_hash(tmp / "protocol.config.json")
    events: list[dict[str, Any]] = []
    for seq in range(1, count + 1):
        item = event(seq, f"value-{seq}")
        item["prev_hash"] = compute_event_prev_hash(item, previous)
        previous = item["prev_hash"]
        events.append(item)
    return events


def valid_result(tmp: Path, events: list[dict[str, Any]], config: dict[str, Any] | None = None) -> dict[str, Any]:
    return validate_chain(events, config or BASE_CONFIG, root=tmp)


def run_case(name: str, builder) -> dict[str, Any]:
    tmp = make_root_temp_dir(ROOT, f"chain-{name.lower()}-")
    try:
        outcome = builder(tmp)
        passed = bool(outcome.pop("passed"))
        return {"case": name, "status": "pass" if passed else "fail", **outcome}
    finally:
        remove_root_temp_dir(tmp, strict=True)


def expect_valid(tmp: Path) -> dict[str, Any]:
    result = valid_result(tmp, chained_events(tmp))
    return {"passed": result["valid"] is True, "message": result["reason"], "events_count": 10}


def expect_point_mutation(tmp: Path) -> dict[str, Any]:
    events = chained_events(tmp)
    events[4]["payload"]["value"] = "mutated"
    result = valid_result(tmp, events)
    return {"passed": result["valid"] is False and "hash mismatch" in result["reason"], "message": result["reason"]}


def expect_deletion(tmp: Path) -> dict[str, Any]:
    events = [item for item in chained_events(tmp) if item["seq"] != 5]
    result = valid_result(tmp, events)
    return {"passed": result["valid"] is False and "gap at seq 6" in result["reason"], "message": result["reason"]}


def expect_reorder(tmp: Path) -> dict[str, Any]:
    events = chained_events(tmp)
    events[6], events[7] = events[7], events[6]
    result = validate_chain(events, BASE_CONFIG, root=tmp)
    return {"passed": result["valid"] is False and ("seq out of order" in result["reason"] or "gap at seq" in result["reason"]), "message": result["reason"]}


def expect_insertion(tmp: Path) -> dict[str, Any]:
    events = chained_events(tmp)
    fake = event(5, "fake")
    fake["prev_hash"] = "0" * 64
    events.insert(5, fake)
    result = valid_result(tmp, events)
    return {"passed": result["valid"] is False and ("hash mismatch" in result["reason"] or "seq out of order" in result["reason"]), "message": result["reason"]}


def expect_legacy(tmp: Path) -> dict[str, Any]:
    write_json(tmp / "protocol.config.json", LEGACY_CONFIG)
    events = [event(seq, f"legacy-{seq}") for seq in range(1, 11)]
    result = validate_chain(events, LEGACY_CONFIG, root=tmp)
    return {"passed": result["valid"] is True and result["reason"] == "chain_disabled", "message": result["reason"]}


def expect_legacy_migration(tmp: Path) -> dict[str, Any]:
    write_json(tmp / "protocol.config.json", BASE_CONFIG)
    log_path = tmp / "runtime" / "state" / "events.jsonl"
    for seq in range(1, 6):
        atomic_append_jsonl(log_path, event(seq, f"legacy-{seq}"))
    writer = EventWriter(tmp)
    writer.append_event(
        event_type="intent.applied",
        aggregate_id="TASK-GOLDEN",
        actor_id="Codex",
        payload={"value": "after-migration"},
        idempotency_key="golden:migration",
        ts="2026-06-13T00:01:00Z",
    )
    events = writer.events()
    result = valid_result(tmp, events)
    has_genesis = any(item.get("type") == "chain.genesis" for item in events)
    return {"passed": result["valid"] is True and has_genesis, "message": result["reason"], "events_count": len(events)}


def expect_genesis_mismatch(tmp: Path) -> dict[str, Any]:
    events = chained_events(tmp)
    genesis = event(0, "genesis")
    genesis["type"] = "chain.genesis"
    genesis["applied"] = False
    genesis["prev_hash"] = "f" * 64
    result = valid_result(tmp, [genesis, *events])
    return {"passed": result["valid"] is False and "genesis mismatch" in result["reason"], "message": result["reason"]}


def expect_archive_boundary(tmp: Path) -> dict[str, Any]:
    events = chained_events(tmp, count=9)
    boundary = event(15, "archive-boundary")
    boundary["type"] = "chain.archive_boundary"
    boundary["payload"] = {"archive_ref": "chain_manifest.json", "last_seq_before_prune": 9}
    boundary["prev_hash"] = compute_event_prev_hash(boundary, events[-1]["prev_hash"])
    next_event = event(16, "after-boundary")
    next_event["prev_hash"] = compute_event_prev_hash(next_event, boundary["prev_hash"])
    result = valid_result(tmp, [*events, boundary, next_event])
    return {"passed": result["valid"] is True, "message": result["reason"], "events_count": 11}


def expect_boundary_missing(tmp: Path) -> dict[str, Any]:
    events = chained_events(tmp)
    events[9]["seq"] = 11
    result = valid_result(tmp, events)
    return {"passed": result["valid"] is False and "gap at seq 11" in result["reason"], "message": result["reason"]}


CASES = [
    ("GC-1-valid-chain", expect_valid),
    ("GC-2-point-mutation", expect_point_mutation),
    ("GC-3-delete-event", expect_deletion),
    ("GC-4-reorder-events", expect_reorder),
    ("GC-5-insert-event", expect_insertion),
    ("GC-6-legacy-disabled", expect_legacy),
    ("GC-7-legacy-migration", expect_legacy_migration),
    ("GC-8-genesis-mismatch", expect_genesis_mismatch),
    ("GC-9-archive-boundary", expect_archive_boundary),
    ("GC-10-boundary-missing", expect_boundary_missing),
]


def main() -> int:
    results = [run_case(name, builder) for name, builder in CASES]
    print(json.dumps({"schema_version": "chain_cases.v1", "results": results}, indent=2, sort_keys=True))
    return 0 if all(item["status"] == "pass" for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
