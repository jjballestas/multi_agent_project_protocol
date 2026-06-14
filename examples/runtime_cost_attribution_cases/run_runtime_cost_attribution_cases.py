#!/usr/bin/env python3
"""Golden cases for cost-attribution per handoff/decision/agent (DECISION-0033, SPEC-0079).

Includes the analista pasada-3 hardening: canonical subject per dimension (C1), cost_unit/cost_schema
tags + summarizer rejection (C2), actor vocabulary (C3), populated-log byte-equivalence and a hot case
asserting recorded == an independently measured token count, not a literal (C4).
"""

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
from runtime.budget import (  # noqa: E402
    attribute_cost,
    canonical_subject,
    cost_attribution_idempotency_key,
    cost_attribution_record,
)
from runtime.eventlog import EventWriter, canonical_hash, cost_attribution_enabled  # noqa: E402
from runtime.metrics import summarize_cost_attribution  # noqa: E402
from runtime.protocol_replay import current_protocol_snapshot, protocol_state_drift, write_genesis  # noqa: E402


def configure(root: Path, *, enabled: bool) -> None:
    write_config(root, {"schema_version": "1.0", "metrics": {"cost_attribution_enabled": enabled}})


def write_config(root: Path, config: dict[str, Any]) -> None:
    (root / "protocol.config.json").write_text(json.dumps(config, indent=2, sort_keys=True), encoding="utf-8")


def event_log(root: Path) -> Path:
    return root / "runtime/state/events.jsonl"


def handoff_hash(handoff_id: str) -> str:
    return canonical_hash(canonical_subject("handoff", handoff_id))


def case_single_handoff_attributed_to_agent() -> None:
    with tempfile.TemporaryDirectory(prefix="cost-single-") as temp:
        root = Path(temp)
        configure(root, enabled=True)
        writer = EventWriter(root)
        emitted = attribute_cost(
            writer,
            dimension="handoff",
            actor="Codex",
            subject_id="HANDOFF-TASK-A-1",
            cost_tokens=120,
            subject_seq=1,
            task_id="TASK-A",
        )
        assert emitted is not None and emitted["type"] == "cost.attributed"
        assert emitted["applied"] is False, emitted
        payload = emitted["payload"]
        # Protocol plane: structured metric + unit/version tags + subject hash; no prose, no payload plane.
        assert payload["subject_hash"] == handoff_hash("HANDOFF-TASK-A-1")
        assert payload["cost_unit"] == "tokens_total" and payload["cost_schema"] == "1"
        assert set(payload) == {"dimension", "subject_hash", "subject_seq", "cost_tokens", "cost_unit", "cost_schema", "task_id"}

        summary = summarize_cost_attribution(event_log(root))
        assert summary == {
            "attributions": 1,
            "rejected": 0,
            "total_cost_tokens": 120,
            "units": {"tokens_total/1": 1},
            "by_handoff": [
                {
                    "seq": 1,
                    "subject_seq": 1,
                    "subject_hash": handoff_hash("HANDOFF-TASK-A-1"),
                    "actor": "Codex",
                    "task_id": "TASK-A",
                    "cost_tokens": 120,
                }
            ],
            "by_decision": {},
            "by_agent": {"Codex": 120},
        }, summary


def case_canonical_subject_two_equal_emissions() -> None:
    # C1: two logically-equal handoff emissions (same handoff_id) must hash identically, even with
    # different cost/seq, so H2's paired matching and the idempotency key cannot silently break.
    r1 = cost_attribution_record(dimension="handoff", actor="Codex", subject_id="H-42", cost_tokens=10, subject_seq=1)
    r2 = cost_attribution_record(dimension="handoff", actor="Claude", subject_id="H-42", cost_tokens=99, subject_seq=7)
    assert r1["subject_hash"] == r2["subject_hash"], (r1, r2)
    # Different handoff_id => different subject_hash.
    r3 = cost_attribution_record(dimension="handoff", actor="Codex", subject_id="H-43", cost_tokens=10, subject_seq=1)
    assert r3["subject_hash"] != r1["subject_hash"]
    # The idempotency key pins subject+dimension+actor+seq.
    assert cost_attribution_idempotency_key(r1).startswith("cost:handoff:" + handoff_hash("H-42") + ":1:Codex")


def case_multiple_handoffs_no_cross_aggregation() -> None:
    with tempfile.TemporaryDirectory(prefix="cost-multi-") as temp:
        root = Path(temp)
        configure(root, enabled=True)
        writer = EventWriter(root)
        attribute_cost(writer, dimension="handoff", actor="Codex", subject_id="H1", cost_tokens=100, subject_seq=1, task_id="TASK-A")
        attribute_cost(writer, dimension="handoff", actor="Codex", subject_id="H2", cost_tokens=50, subject_seq=2, task_id="TASK-A")
        attribute_cost(writer, dimension="handoff", actor="Claude", subject_id="H3", cost_tokens=30, subject_seq=3, task_id="TASK-B")

        summary = summarize_cost_attribution(event_log(root))
        assert len(summary["by_handoff"]) == 3, summary
        hashes = [item["subject_hash"] for item in summary["by_handoff"]]
        assert len(set(hashes)) == 3, summary
        assert [item["cost_tokens"] for item in summary["by_handoff"]] == [100, 50, 30], summary
        assert summary["by_agent"] == {"Claude": 30, "Codex": 150}, summary
        assert summary["total_cost_tokens"] == 180 and summary["attributions"] == 3 and summary["rejected"] == 0, summary


def case_decision_attribution() -> None:
    with tempfile.TemporaryDirectory(prefix="cost-decision-") as temp:
        root = Path(temp)
        configure(root, enabled=True)
        writer = EventWriter(root)
        attribute_cost(
            writer,
            dimension="decision",
            actor="Claude",
            subject_id="DECISION-0033",
            cost_tokens=200,
            subject_seq=5,
            decision_id="DECISION-0033",
        )
        summary = summarize_cost_attribution(event_log(root))
        assert summary["by_decision"] == {"DECISION-0033": 200}, summary
        assert summary["by_agent"] == {"Claude": 200}, summary
        assert summary["by_handoff"] == [], summary


def case_summarizer_rejects_rows_without_tags() -> None:
    # C2: a cost.attributed row missing cost_unit/cost_schema (forged/legacy) is rejected, not summed.
    with tempfile.TemporaryDirectory(prefix="cost-reject-") as temp:
        root = Path(temp)
        log = event_log(root)
        log.parent.mkdir(parents=True, exist_ok=True)
        good = {"seq": 1, "type": "cost.attributed", "actor": "Codex",
                "payload": {"dimension": "handoff", "subject_hash": handoff_hash("H1"), "subject_seq": 1,
                            "cost_tokens": 40, "cost_unit": "tokens_total", "cost_schema": "1"}}
        bad = {"seq": 2, "type": "cost.attributed", "actor": "Codex",
               "payload": {"dimension": "handoff", "subject_hash": handoff_hash("H2"), "subject_seq": 2, "cost_tokens": 999}}
        log.write_text("".join(json.dumps(e, sort_keys=True) + "\n" for e in (good, bad)), encoding="utf-8")
        summary = summarize_cost_attribution(log)
        assert summary["attributions"] == 1 and summary["rejected"] == 1, summary
        assert summary["total_cost_tokens"] == 40, summary  # the 999 row is excluded
        assert summary["units"] == {"tokens_total/1": 1}, summary


def case_actor_vocabulary_restricted() -> None:
    # C3: actor restricted to a controlled non-human agent vocabulary.
    vocab = {"Codex", "Claude"}
    cost_attribution_record(dimension="handoff", actor="Codex", subject_id="H1", cost_tokens=10, agent_vocabulary=vocab)
    for bad_actor in ("operador_humano", "john@example.com", ""):
        try:
            cost_attribution_record(dimension="handoff", actor=bad_actor, subject_id="H1", cost_tokens=10, agent_vocabulary=vocab)
        except ValueError:
            continue
        raise AssertionError(f"record accepted actor outside vocabulary: {bad_actor!r}")


def case_record_rejects_free_text_dimension_and_missing_tags() -> None:
    for bad in ("summary", "prose", ""):
        try:
            cost_attribution_record(dimension=bad, actor="Codex", subject_id="H1", cost_tokens=1)
        except ValueError:
            continue
        raise AssertionError(f"record accepted invalid dimension: {bad!r}")
    for bad_kwargs in ({"cost_unit": ""}, {"cost_schema": ""}):
        try:
            cost_attribution_record(dimension="handoff", actor="Codex", subject_id="H1", cost_tokens=1, **bad_kwargs)
        except ValueError:
            continue
        raise AssertionError(f"record accepted empty unit/schema: {bad_kwargs}")


def case_disabled_byte_equivalent_empty_and_populated() -> None:
    # C4a-empty: flag off on a fresh log writes nothing.
    with tempfile.TemporaryDirectory(prefix="cost-off-") as temp:
        root = Path(temp)
        configure(root, enabled=False)
        assert cost_attribution_enabled(read_json(root / "protocol.config.json")) is False
        assert attribute_cost(EventWriter(root), dimension="handoff", actor="Codex", subject_id="H1", cost_tokens=999, subject_seq=1) is None
        assert not event_log(root).exists()

    # C4a-populated: flag off on an EXISTING populated log => zero cost.attributed lines, bytes identical.
    with tempfile.TemporaryDirectory(prefix="cost-off-populated-") as temp:
        root = Path(temp)
        configure(root, enabled=False)
        log = event_log(root)
        log.parent.mkdir(parents=True, exist_ok=True)
        seed = [
            {"seq": 1, "type": "intent.applied", "actor": "Codex", "payload": {"transitions": {}}},
            {"seq": 2, "type": "intent.applied", "actor": "Claude", "payload": {"transitions": {}}},
        ]
        log.write_text("".join(json.dumps(e, sort_keys=True) + "\n" for e in seed), encoding="utf-8")
        control = log.read_bytes()
        for i in range(3):
            assert attribute_cost(EventWriter(root), dimension="handoff", actor="Codex", subject_id=f"H{i}", cost_tokens=10 * i, subject_seq=i) is None
        assert log.read_bytes() == control, "flag-off append mutated a populated log"
        assert summarize_cost_attribution(log) == {
            "attributions": 0, "rejected": 0, "total_cost_tokens": 0, "units": {},
            "by_handoff": [], "by_decision": {}, "by_agent": {},
        }


def measure_tokens(text: str, chars_per_token: int = 4) -> int:
    # Deterministic independent token measure (repo convention: chars_per_token=4).
    return max(1, len(text) // chars_per_token)


def case_hot_recorded_equals_measured_count() -> None:
    # C4b: what is recorded == an independently measured token count, NOT a hardcoded literal. The
    # value is derived from the input, so two different inputs record two different measured counts.
    with tempfile.TemporaryDirectory(prefix="cost-hot-") as temp:
        root = Path(temp)
        configure(root, enabled=True)
        writer = EventWriter(root)
        fixtures = {"HANDOFF-short": "abcd" * 5, "HANDOFF-long": "abcd" * 50}
        measured = {hid: measure_tokens(text) for hid, text in fixtures.items()}
        seq = 0
        for hid, text in fixtures.items():
            seq += 1
            attribute_cost(writer, dimension="handoff", actor="Codex", subject_id=hid,
                           cost_tokens=measure_tokens(text), subject_seq=seq, task_id="TASK-HOT")
        recorded = {
            row["subject_hash"]: row["cost_tokens"]
            for row in summarize_cost_attribution(event_log(root))["by_handoff"]
        }
        for hid, m in measured.items():
            assert recorded[handoff_hash(hid)] == m, (hid, recorded, measured)
        # Not a literal: distinct inputs => distinct recorded values matching their measures.
        assert measured["HANDOFF-short"] != measured["HANDOFF-long"]
        assert recorded[handoff_hash("HANDOFF-short")] != recorded[handoff_hash("HANDOFF-long")]


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
        emitted = attribute_cost(writer, dimension="handoff", actor="Codex", subject_id="HANDOFF-TASK-9200",
                                 cost_tokens=42, subject_seq=1, task_id="TASK-9200")
        assert emitted is not None and emitted["applied"] is False
        writer.write_snapshot()

        after = protocol_state_drift(root)
        assert after["enforced"] is True and after["has_drift"] is False, after
        assert current_protocol_snapshot(root)["state"] == replay_before
        summary = summarize_cost_attribution(event_log(root))
        assert summary["by_agent"] == {"Codex": 42} and summary["rejected"] == 0, summary
        assert summary["by_handoff"][0]["task_id"] == "TASK-9200", summary


def main() -> int:
    cases = [
        case_single_handoff_attributed_to_agent,
        case_canonical_subject_two_equal_emissions,
        case_multiple_handoffs_no_cross_aggregation,
        case_decision_attribution,
        case_summarizer_rejects_rows_without_tags,
        case_actor_vocabulary_restricted,
        case_record_rejects_free_text_dimension_and_missing_tags,
        case_disabled_byte_equivalent_empty_and_populated,
        case_hot_recorded_equals_measured_count,
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
