#!/usr/bin/env python3
"""Golden cases for event chain + event auth + cost attribution together."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
MATERIALIZE_CASES = ROOT / "examples/runtime_protocol_materialize_cases"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(MATERIALIZE_CASES))

from run_runtime_protocol_materialize_cases import build_fixture, read_json, write_json  # noqa: E402
from runtime.budget import attribute_cost  # noqa: E402
from runtime.eventlog import EventWriter, events_in_log_order, verify_event_auth  # noqa: E402
from runtime.protocol_replay import protocol_state_drift, validate_chain, write_genesis  # noqa: E402
from runtime.temp_paths import root_temp_dir  # noqa: E402


def combined_config(root: Path) -> dict[str, Any]:
    config = read_json(root / "protocol.config.json")
    config["event_auth"] = {
        "enabled": True,
        "method": "hmac-sha256",
        "issuer": "fixture-runtime",
        "audience": "fixture-event-log",
        "keys": {
            "runtime": {"key_id": "fixture-runtime", "secret": "runtime-test-secret"},
            "Codex": {"key_id": "fixture-codex", "secret": "codex-test-secret"},
        },
    }
    config["event_state"]["chain_enabled"] = True
    config["metrics"] = {"cost_attribution_enabled": True}
    return config


def prepare_root(root: Path) -> None:
    build_fixture(root, event_enabled=True, materialize=True, enforce=True, authoritative=True, tier="runtime")
    write_json(root / "protocol.config.json", combined_config(root))
    write_genesis(root)


def assert_all_events_authenticated(root: Path) -> None:
    config = read_json(root / "protocol.config.json")
    for event in events_in_log_order(root):
        result = verify_event_auth(event, config)
        assert result["valid"] is True, {"seq": event.get("seq"), "result": result}


def emit_cost(root: Path) -> dict[str, Any]:
    writer = EventWriter(root)
    event = attribute_cost(
        writer,
        dimension="handoff",
        actor="Codex",
        subject_id="HANDOFF-TASK-0111-review",
        cost_tokens=77,
        context_tokens=55,
        subject_seq=1,
        task_id="TASK-0111",
    )
    assert event is not None and event["type"] == "cost.attributed", event
    assert event["applied"] is False, event
    writer.write_snapshot()
    return event


def case_chain_auth_cost_positive() -> None:
    with root_temp_dir(ROOT, ".chain-auth-cost-positive-") as root:
        prepare_root(root)
        emit_cost(root)
        config = read_json(root / "protocol.config.json")
        events = events_in_log_order(root)
        assert any(event.get("type") == "cost.attributed" for event in events), events
        assert_all_events_authenticated(root)
        chain = validate_chain(events, config, root=root)
        assert chain["valid"] is True, chain
        drift = protocol_state_drift(root)
        assert drift["enforced"] is True and drift["has_drift"] is False, drift


def case_chain_auth_cost_tampering_detected() -> None:
    with root_temp_dir(ROOT, ".chain-auth-cost-tamper-") as root:
        prepare_root(root)
        emit_cost(root)
        log_path = root / "runtime/state/events.jsonl"
        events = [json.loads(line) for line in log_path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]
        cost_event = next(event for event in events if event.get("type") == "cost.attributed")
        cost_event["payload"]["cost_tokens"] = 78
        log_path.write_text(
            "".join(json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for event in events),
            encoding="utf-8",
        )
        config = read_json(root / "protocol.config.json")
        chain = validate_chain(events_in_log_order(root), config, root=root)
        assert chain["valid"] is False, chain
        auth = verify_event_auth(cost_event, config)
        assert auth["valid"] is False, auth


def main() -> int:
    cases = [case_chain_auth_cost_positive, case_chain_auth_cost_tampering_detected]
    failures: list[dict[str, Any]] = []
    for case in cases:
        try:
            case()
        except Exception as exc:  # noqa: BLE001 - compact golden failure reporting
            failures.append({"case": case.__name__, "error": str(exc)})
    if failures:
        print(json.dumps({"status": "FAILED", "failures": failures}, indent=2, sort_keys=True))
        return 1
    print(f"OK: {len(cases)} chain+auth+cost golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
