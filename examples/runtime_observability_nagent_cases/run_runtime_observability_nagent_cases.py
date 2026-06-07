#!/usr/bin/env python3
"""Golden cases for N-agent runtime observability."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import runtime.eventlog as eventlog_module  # noqa: E402
from runtime.apply import emit_runtime_eventlog  # noqa: E402
from runtime.eventlog import (  # noqa: E402
    EventWriter,
    assert_snapshot_matches,
    canonical_hash,
    deterministic_trace_id,
    rebuild_snapshot,
    replay_without_side_effects,
)
from runtime.metrics import summarize_nagent  # noqa: E402
from runtime.review_qa import review_qa_span  # noqa: E402
from runtime.router import select_next  # noqa: E402


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def write_jsonl(path: Path, entries: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(entry, sort_keys=True) + "\n" for entry in entries), encoding="utf-8")


def configure(root: Path, *, enabled: bool) -> None:
    write_json(root / "protocol.config.json", {"schema_version": "1.0", "observability": {"enabled": enabled}})


def write_trace_event(root: Path) -> dict[str, Any]:
    writer = EventWriter(root)
    return writer.append_event(
        event_type="intent.applied",
        aggregate_id="TASK-9100",
        actor_id="Codex",
        idempotency_key="Codex:TASK-9100:observe:attempt-1:1",
        payload={"run_id": "RUN-nagent", "task_id": "TASK-9100", "attempt_id": "attempt-1"},
    )


def router_state(*, observability: bool) -> dict[str, Any]:
    config = {
        "routing_epoch": "nagent-observe-v1",
        "routing_weights": {
            "active_claims": 10,
            "pending_reviews": 6,
            "pending_qa": 6,
            "open_fix_cycles": 4,
            "cooldown_penalty": 1,
            "capability_affinity": 1,
        },
    }
    if observability:
        config["observability"] = {"enabled": True}
    return {
        "run_id": "RUN-router",
        "config": config,
        "task_index": {
            "tasks": [
                {
                    "id": "TASK-9200",
                    "owner": "Author",
                    "author": "Author",
                    "status": "in_review",
                    "priority": "high",
                }
            ]
        },
        "claims": {"claims": []},
        "mailbox_open": [],
        "agent_registry": {
            "enabled": True,
            "routing_policy": "weighted_least_loaded_deterministic",
            "agents": [
                {"id": "Author", "capabilities": ["reviewer"], "enabled": True},
                {"id": "Reviewer", "capabilities": ["reviewer"], "enabled": True},
            ],
        },
    }


def case_trace_id_present_and_deterministic() -> None:
    with tempfile.TemporaryDirectory(prefix="nagent-trace-left-") as left_temp, tempfile.TemporaryDirectory(prefix="nagent-trace-right-") as right_temp:
        left = Path(left_temp)
        right = Path(right_temp)
        configure(left, enabled=True)
        configure(right, enabled=True)
        first = write_trace_event(left)
        second = write_trace_event(right)
        expected = deterministic_trace_id(run_id="RUN-nagent", task_id="TASK-9100", attempt_id="attempt-1", seq=1)
        assert first["trace_id"] == expected
        assert second["trace_id"] == expected


def case_spans_by_transition() -> None:
    routed = select_next(router_state(observability=True))
    assert routed is not None
    router_span = routed["routing_decision"]["span"]
    assert routed["span"] == router_span
    assert router_span["name"] == "router.review"
    assert router_span["attrs"]["task_id"] == "TASK-9200"
    assert router_span["attrs"]["owner"] == "Reviewer"

    span = review_qa_span(
        task_id="TASK-9300",
        event="fail_qa",
        from_status="qa_pending",
        to_status="architect_review",
        actor="QA",
        run_id="RUN-review",
        attempt_id="attempt-qa-1",
        seq=7,
    )
    assert span["name"] == "review_qa.fail_qa"
    assert span["trace_id"] == deterministic_trace_id(run_id="RUN-review", task_id="TASK-9300", attempt_id="attempt-qa-1", seq=7)

    with tempfile.TemporaryDirectory(prefix="nagent-review-event-") as temp:
        root = Path(temp)
        configure(root, enabled=True)
        events = emit_runtime_eventlog(
            root,
            {
                "turn_id": "RUN-review",
                "attempt_id": "attempt-qa-1",
                "task_id": "TASK-9300",
                "agent": "QA",
                "outcome": "ok",
                "changed_paths": [],
                "transitions": {
                    "task_status": {"from": "qa_pending", "to": "architect_review"},
                    "review_qa": {"event": "fail_qa", "qa": "QA", "attempt_id": "attempt-qa-1"},
                },
            },
            {"claim_id": "CLAIM-9300-QA", "expires_at": "2026-06-08"},
        )
        intent = events[1]
        review_span = intent["payload"]["review_qa"]["span"]
        assert review_span["name"] == "review_qa.fail_qa"
        assert review_span["trace_id"] == intent["trace_id"]


def case_summarize_nagent_synthetic() -> None:
    with tempfile.TemporaryDirectory(prefix="nagent-summary-") as temp:
        root = Path(temp)
        run_log = root / "runtime/runs/RUN-nagent.jsonl"
        event_log = root / "runtime/state/events.jsonl"
        decision = {
            "policy": "weighted_least_loaded_deterministic",
            "transition": "review",
            "required_capability": "reviewer",
            "explanation": {
                "selected": "Reviewer",
                "weights": {"QA": 1, "Reviewer": 1},
                "candidates": [{"agent": "QA"}, {"agent": "Reviewer"}],
                "filtered": [{"agent": "Author", "reason": "author_excluded"}],
            },
        }
        qa_decision = {
            "policy": "weighted_least_loaded_deterministic",
            "transition": "qa",
            "required_capability": "qa",
            "explanation": {
                "selected": "QA",
                "weights": {"QA": 1, "Reviewer": 1},
                "candidates": [{"agent": "QA"}, {"agent": "Reviewer"}],
                "filtered": [],
            },
        }
        write_jsonl(
            run_log,
            [
                {"run_id": "RUN-nagent", "task_id": "TASK-A", "unit": {"task_id": "TASK-A", "owner": "Reviewer", "routing_decision": decision}},
                {"run_id": "RUN-nagent", "task_id": "TASK-B", "unit": {"task_id": "TASK-B", "owner": "QA", "routing_decision": qa_decision}},
            ],
        )
        write_jsonl(
            event_log,
            [
                {
                    "seq": 1,
                    "type": "intent.applied",
                    "aggregate_id": "TASK-B",
                    "payload": {"transition": "qa_pending->architect_review", "review_qa": {"event": "fail_qa"}},
                },
                {"seq": 2, "type": "state.stale_fencing_rejected", "aggregate_id": "TASK-C", "payload": {"current_fencing_token": 2}},
            ],
        )
        assert summarize_nagent(event_log, run_log) == {
            "run_id": "RUN-nagent",
            "routing": {
                "assignments": 2,
                "by_agent": {"QA": 1, "Reviewer": 1},
                "fairness": {
                    "assignments": 2,
                    "counts": {"QA": 1, "Reviewer": 1},
                    "expected": {"QA": 1.0, "Reviewer": 1.0},
                    "fairness_ratio": 1.0,
                    "weighted_share_delta": {"QA": 0.0, "Reviewer": 0.0},
                    "max_weighted_share_delta": 0.0,
                    "denominator_zero": False,
                },
            },
            "qa_cycles": {"total": 1, "by_task": {"TASK-B": 1}},
            "fencing_conflicts": {"total": 1, "by_task": {"TASK-C": 1}},
            "escalations": {"total": 1, "by_task": {"TASK-B": 1}, "by_type": {"architect_review": 1}},
            "author_exclusions": {"total": 1, "by_task": {"TASK-A": 1}},
        }


def case_replay_with_trace_id_hash_negative_safe() -> None:
    with tempfile.TemporaryDirectory(prefix="nagent-replay-") as temp:
        root = Path(temp)
        configure(root, enabled=True)
        writer = EventWriter(root)
        claim = writer.acquire_claim(
            task_id="TASK-9400",
            owner="Codex",
            lease_until="2026-06-08T00:00:00Z",
            idempotency_key="Codex:TASK-9400:claim:attempt-1:0",
        )
        writer.apply_intent(
            task_id="TASK-9400",
            actor_id="Codex",
            transition="ready->in_progress",
            attempt_id="attempt-1",
            fencing_token=int(claim["fencing_token"]),
            payload={"run_id": "RUN-replay", "task_id": "TASK-9400"},
        )
        assert all(event.get("trace_id") for event in writer.events())
        snapshot = writer.write_snapshot()
        rebuilt = rebuild_snapshot(root)
        assert canonical_hash(snapshot["state"]) == canonical_hash(rebuilt["state"])
        assert_snapshot_matches(root)

        def forbidden() -> None:
            raise AssertionError("negative replay invoked an external effect")

        replayed = replay_without_side_effects(root, forbidden)
        assert canonical_hash(rebuilt["state"]) == canonical_hash(replayed["state"])


def case_observability_disabled_byte_equivalent() -> None:
    original_utc_now = eventlog_module.utc_now
    eventlog_module.utc_now = lambda: "2026-06-07T00:00:00Z"
    try:
        with tempfile.TemporaryDirectory(prefix="nagent-disabled-left-") as left_temp, tempfile.TemporaryDirectory(prefix="nagent-disabled-right-") as right_temp:
            left = Path(left_temp)
            right = Path(right_temp)
            configure(right, enabled=False)
            write_trace_event(left)
            write_trace_event(right)
            assert (left / "runtime/state/events.jsonl").read_bytes() == (right / "runtime/state/events.jsonl").read_bytes()
    finally:
        eventlog_module.utc_now = original_utc_now

    without_config = select_next(router_state(observability=False))
    disabled = router_state(observability=False)
    disabled["config"]["observability"] = {"enabled": False}
    assert without_config == select_next(disabled)
    assert "span" not in without_config


def main() -> int:
    cases = [
        case_trace_id_present_and_deterministic,
        case_spans_by_transition,
        case_summarize_nagent_synthetic,
        case_replay_with_trace_id_hash_negative_safe,
        case_observability_disabled_byte_equivalent,
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
    print(f"OK: {len(cases)} N-agent observability golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
