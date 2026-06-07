#!/usr/bin/env python3
"""Golden cases for deterministic runtime event envelope authentication."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from runtime import eventlog  # noqa: E402
from runtime.eventlog import (  # noqa: E402
    UNAUTHENTICATED_EVENT,
    EventWriter,
    canonical_hash,
    canonical_json,
    rebuild_snapshot,
    replay_without_side_effects,
    verify_event_auth,
)


TASK_ID = "TASK-9200"


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def write_config(root: Path, *, enabled: bool | None = True, agent_auth: dict | None = None) -> None:
    if enabled is None:
        return
    write_json(
        root / "protocol.config.json",
        {
            "schema_version": "1.0",
            "event_auth": {
                "enabled": enabled,
                "method": "hmac-sha256",
                "issuer": "fixture-runtime",
                "audience": "fixture-event-log",
                "keys": {"Codex": {"key_id": "fixture-codex", "secret": "test-only-hmac-secret"}},
            },
            "agent_registry": {
                "enabled": True,
                "agents": [
                    {
                        "id": "Codex",
                        "capabilities": ["implementer"],
                        "enabled": True,
                        "auth": agent_auth or {},
                    }
                ],
            },
        },
    )


def read_events(root: Path) -> list[dict]:
    path = root / eventlog.LOG_PATH
    return [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def write_events(root: Path, events: list[dict]) -> None:
    path = root / eventlog.LOG_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(item, sort_keys=True, separators=(",", ":")) + "\n" for item in events), encoding="utf-8")


def fixed_clock():
    return "2026-06-07T00:00:00Z"


def with_fixed_clock(callback):
    original = eventlog.utc_now
    eventlog.utc_now = fixed_clock
    try:
        return callback()
    finally:
        eventlog.utc_now = original


def case_valid_signature_is_accepted() -> None:
    with tempfile.TemporaryDirectory(prefix="event-auth-valid-") as temp:
        root = Path(temp)
        write_config(root)
        event = with_fixed_clock(
            lambda: EventWriter(root).acquire_claim(
                task_id=TASK_ID,
                owner="Codex",
                lease_until="2026-06-07T12:00:00Z",
                idempotency_key=f"Codex:{TASK_ID}:claim:attempt-1:0",
            )
        )
        assert "event_auth" in event
        assert verify_event_auth(event, eventlog.read_protocol_config(root))["valid"] is True
        state = rebuild_snapshot(root)["state"]
        assert state["rejections"] == []
        assert state["aggregate_versions"][TASK_ID] == event["aggregate_version"]


def case_missing_or_altered_signature_is_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="event-auth-invalid-") as temp:
        root = Path(temp)
        write_config(root)
        writer = EventWriter(root)
        with_fixed_clock(
            lambda: writer.acquire_claim(
                task_id=TASK_ID,
                owner="Codex",
                lease_until="2026-06-07T12:00:00Z",
                idempotency_key=f"Codex:{TASK_ID}:claim:attempt-1:0",
            )
        )
        missing = read_events(root)
        missing[0].pop("event_auth")
        write_events(root, missing)
        state = rebuild_snapshot(root)["state"]
        assert state["rejections"][0]["event"] == UNAUTHENTICATED_EVENT
        assert state["rejections"][0]["reason"] == "missing_signature"
        assert TASK_ID not in state["aggregate_versions"]

        altered = read_events(root)
        altered[0]["event_auth"] = {"method": "hmac-sha256", "key_id": "fixture-codex", "signature": "bad"}
        write_events(root, altered)
        state = rebuild_snapshot(root)["state"]
        assert state["rejections"][0]["event"] == UNAUTHENTICATED_EVENT
        assert state["rejections"][0]["reason"] == "invalid_signature"
        assert TASK_ID not in state["aggregate_versions"]


def case_replay_is_deterministic_and_negative_replay_safe() -> None:
    with tempfile.TemporaryDirectory(prefix="event-auth-replay-") as temp:
        root = Path(temp)
        write_config(root)
        writer = EventWriter(root)
        claim = with_fixed_clock(
            lambda: writer.acquire_claim(
                task_id=TASK_ID,
                owner="Codex",
                lease_until="2026-06-07T12:00:00Z",
                idempotency_key=f"Codex:{TASK_ID}:claim:attempt-1:0",
            )
        )
        with_fixed_clock(
            lambda: writer.apply_intent(
                task_id=TASK_ID,
                actor_id="Codex",
                transition="submit",
                attempt_id="attempt-1",
                fencing_token=int(claim["fencing_token"]),
            )
        )

        def forbidden() -> None:
            raise AssertionError("negative replay invoked external effect")

        before = rebuild_snapshot(root)
        after = replay_without_side_effects(root, forbidden)
        assert canonical_hash(before["state"]) == canonical_hash(after["state"])
        assert before["state"]["rejections"] == []


def case_signing_off_or_absent_is_byte_equivalent() -> None:
    def produce(root: Path, enabled: bool | None) -> str:
        write_config(root, enabled=enabled)
        writer = EventWriter(root)
        event = with_fixed_clock(
            lambda: writer.acquire_claim(
                task_id=TASK_ID,
                owner="Codex",
                lease_until="2026-06-07T12:00:00Z",
                idempotency_key=f"Codex:{TASK_ID}:claim:attempt-1:0",
            )
        )
        assert "event_auth" not in event
        return canonical_json(event)

    with tempfile.TemporaryDirectory(prefix="event-auth-off-") as left_temp, tempfile.TemporaryDirectory(
        prefix="event-auth-absent-"
    ) as right_temp:
        assert produce(Path(left_temp), False) == produce(Path(right_temp), None)


def case_issuer_audience_placeholder_is_structural_only() -> None:
    with tempfile.TemporaryDirectory(prefix="event-auth-placeholder-") as temp:
        root = Path(temp)
        write_config(root, agent_auth={"issuer": "agent-card-fixture", "audience": "protocol-runtime"})
        event = with_fixed_clock(
            lambda: EventWriter(root).acquire_claim(
                task_id=TASK_ID,
                owner="Codex",
                lease_until="2026-06-07T12:00:00Z",
                idempotency_key=f"Codex:{TASK_ID}:claim:attempt-1:0",
            )
        )
        auth = event["event_auth"]
        assert auth["issuer"] == "agent-card-fixture"
        assert auth["audience"] == "protocol-runtime"
        assert verify_event_auth(event, eventlog.read_protocol_config(root))["valid"] is True


def main() -> int:
    cases = [
        case_valid_signature_is_accepted,
        case_missing_or_altered_signature_is_rejected,
        case_replay_is_deterministic_and_negative_replay_safe,
        case_signing_off_or_absent_is_byte_equivalent,
        case_issuer_audience_placeholder_is_structural_only,
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
    print(f"OK: {len(cases)} runtime event auth cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
