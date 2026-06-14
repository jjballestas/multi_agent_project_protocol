#!/usr/bin/env python3
"""Golden cases for cost-attribution per handoff/decision/agent (DECISION-0033, SPEC-0079)."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
MATERIALIZE_CASES = ROOT / "examples/runtime_protocol_materialize_cases"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(MATERIALIZE_CASES))

from run_runtime_protocol_materialize_cases import build_fixture, read_json, write_json  # noqa: E402
from runtime.budget import attribute_cost, cost_attribution_idempotency_key, cost_attribution_record  # noqa: E402
from runtime.eventlog import EventWriter, canonical_hash, cost_attribution_enabled  # noqa: E402
from runtime.metrics import summarize_cost_attribution  # noqa: E402
from runtime.protocol_replay import current_protocol_snapshot, protocol_state_drift, write_genesis  # noqa: E402


def configure(root: Path, *, enabled: bool) -> None:
    write_config(root, {"schema_version": "1.0", "metrics": {"cost_attribution_enabled": enabled}})


def write_config(root: Path, config: dict[str, Any]) -> None:
    (root / "protocol.config.json").write_text(json.dumps(config, indent=2, sort_keys=True), encoding="utf-8")


def event_log(root: Path) -> Path:
    return root / "runtime/state/events.jsonl"


def case_single_handoff_attributed_to_agent() -> None:
    with tempfile.TemporaryDirectory(prefix="cost-single-") as temp:
        root = Path(temp)
        configure(root, enabled=True)
        writer = EventWriter(root)
        subject = {"handoff": "HANDOFF-TASK-A", "to": "Claude"}
        emitted = attribute_cost(
            writer,
            dimension="handoff",
            actor="Codex",
            subject=subject,
            cost_tokens=120,
            subject_seq=1,
            task_id="TASK-A",
        )
        assert emitted is not None and emitted["type"] == "cost.attributed"
        assert emitted["applied"] is False, emitted
        # Protocol plane carries only the metric + structured ids + subject hash, no free text.
        assert "handoff" not in json.dumps(emitted["payload"]).lower() or emitted["payload"]["subject_hash"]
        assert emitted["payload"]["subject_hash"] == canonical_hash(subject)
        assert "to" not in emitted["payload"] and "summary" not in emitted["payload"]

        summary = summarize_cost_attribution(event_log(root))
        assert summary == {
            "attributions": 1,
            "total_cost_tokens": 120,
            "by_handoff": [
                {
                    "seq": 1,
                    "subject_seq": 1,
                    "subject_hash": canonical_hash(subject),
                    "actor": "Codex",
                    "task_id": "TASK-A",
                    "cost_tokens": 120,
                }
            ],
            "by_decision": {},
            "by_agent": {"Codex": 120},
        }, summary


def case_multiple_handoffs_no_cross_aggregation() -> None:
    with tempfile.TemporaryDirectory(prefix="cost-multi-") as temp:
        root = Path(temp)
        configure(root, enabled=True)
        writer = EventWriter(root)
        attribute_cost(writer, dimension="handoff", actor="Codex", subject={"h": "H1"}, cost_tokens=100, subject_seq=1, task_id="TASK-A")
        attribute_cost(writer, dimension="handoff", actor="Codex", subject={"h": "H2"}, cost_tokens=50, subject_seq=2, task_id="TASK-A")
        attribute_cost(writer, dimension="handoff", actor="Claude", subject={"h": "H3"}, cost_tokens=30, subject_seq=3, task_id="TASK-B")

        summary = summarize_cost_attribution(event_log(root))
        # Each handoff stays a separate entry (no cross-aggregation), even the two by Codex.
        assert len(summary["by_handoff"]) == 3, summary
        hashes = [item["subject_hash"] for item in summary["by_handoff"]]
        assert len(set(hashes)) == 3, summary
        costs = [item["cost_tokens"] for item in summary["by_handoff"]]
        assert costs == [100, 50, 30], summary
        # by_agent IS the per-agent dimension: it sums across that agent's handoffs.
        assert summary["by_agent"] == {"Claude": 30, "Codex": 150}, summary
        assert summary["total_cost_tokens"] == 180 and summary["attributions"] == 3, summary


def case_decision_attribution() -> None:
    with tempfile.TemporaryDirectory(prefix="cost-decision-") as temp:
        root = Path(temp)
        configure(root, enabled=True)
        writer = EventWriter(root)
        attribute_cost(
            writer,
            dimension="decision",
            actor="Claude",
            subject={"decision": "DECISION-0033", "body_hash": "x"},
            cost_tokens=200,
            subject_seq=5,
            decision_id="DECISION-0033",
        )
        summary = summarize_cost_attribution(event_log(root))
        assert summary["by_decision"] == {"DECISION-0033": 200}, summary
        assert summary["by_agent"] == {"Claude": 200}, summary
        assert summary["by_handoff"] == [], summary


def case_disabled_byte_equivalent() -> None:
    with tempfile.TemporaryDirectory(prefix="cost-off-call-") as call_temp, tempfile.TemporaryDirectory(prefix="cost-off-skip-") as skip_temp:
        called = Path(call_temp)
        skipped = Path(skip_temp)
        configure(called, enabled=False)
        configure(skipped, enabled=False)
        writer = EventWriter(called)
        assert cost_attribution_enabled({"metrics": {"cost_attribution_enabled": False}}) is False
        # With the flag off, attribute_cost is a no-op and writes nothing.
        result = attribute_cost(writer, dimension="handoff", actor="Codex", subject={"h": "H1"}, cost_tokens=999, subject_seq=1)
        assert result is None
        attribute_cost(writer, dimension="decision", actor="Claude", subject={"d": "D"}, cost_tokens=1, subject_seq=2, decision_id="DECISION-9999")
        # The "called" log is byte-identical to the "skipped" log: neither file exists.
        assert not event_log(called).exists()
        assert not event_log(skipped).exists()
        assert summarize_cost_attribution(event_log(called)) == {
            "attributions": 0,
            "total_cost_tokens": 0,
            "by_handoff": [],
            "by_decision": {},
            "by_agent": {},
        }


def case_record_rejects_free_text_dimension() -> None:
    for bad in ("summary", "prose", ""):
        try:
            cost_attribution_record(dimension=bad, actor="Codex", subject={"x": 1}, cost_tokens=1)
        except ValueError:
            continue
        raise AssertionError(f"cost_attribution_record accepted invalid dimension: {bad!r}")
    record = cost_attribution_record(dimension="handoff", actor="Codex", subject={"x": 1}, cost_tokens=10, subject_seq=1)
    assert cost_attribution_idempotency_key(record).startswith("cost:handoff:")


def case_drift_unaffected() -> None:
    with tempfile.TemporaryDirectory(prefix="cost-drift-") as temp:
        root = Path(temp)
        build_fixture(root, event_enabled=True, materialize=True, enforce=True, authoritative=True, tier="runtime")
        config = read_json(root / "protocol.config.json")
        config["metrics"] = {"cost_attribution_enabled": True}
        write_json(root / "protocol.config.json", config)
        write_genesis(root)

        before = protocol_state_drift(root)
        assert before["enforced"] is True and before["has_drift"] is False, before
        replay_before = current_protocol_snapshot(root)["state"]

        writer = EventWriter(root)
        emitted = attribute_cost(
            writer,
            dimension="handoff",
            actor="Codex",
            subject={"handoff": "HANDOFF-TASK-9200"},
            cost_tokens=42,
            subject_seq=1,
            task_id="TASK-9200",
        )
        assert emitted is not None and emitted["applied"] is False
        writer.write_snapshot()

        after = protocol_state_drift(root)
        assert after["enforced"] is True and after["has_drift"] is False, after
        # The annotation is inert for protocol replay: materialized state is unchanged (replay==hot).
        assert current_protocol_snapshot(root)["state"] == replay_before
        # ...yet the imputation is captured and readable from the event log (hot).
        summary = summarize_cost_attribution(event_log(root))
        assert summary["by_agent"] == {"Codex": 42}, summary
        assert summary["by_handoff"][0]["task_id"] == "TASK-9200", summary


def main() -> int:
    cases = [
        case_single_handoff_attributed_to_agent,
        case_multiple_handoffs_no_cross_aggregation,
        case_decision_attribution,
        case_disabled_byte_equivalent,
        case_record_rejects_free_text_dimension,
        case_drift_unaffected,
    ]
    failures: list[dict[str, Any]] = []
    for case in cases:
        try:
            case()
        except Exception as exc:  # noqa: BLE001 - compact golden failure reporting
            failures.append({"case": case.__name__, "error": str(exc)})
    if failures:
        print(json.dumps({"status": "FAILED", "failures": failures}, indent=2))
        return 1
    print(f"OK: {len(cases)} cost-attribution golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
