#!/usr/bin/env python3
"""Deterministic property-style coverage for runtime invariants I1-I8.

The sample set is enumerated by construction. Each sample gets a stable
``property-###`` seed only for reproducible counterexample reporting; the
harness does not use random data, wall-clock time, network access, or
truncation.
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import runtime.eventlog as eventlog  # noqa: E402
from runtime.context import active_claims  # noqa: E402
from runtime.eventlog import EventWriter, canonical_hash, rebuild_snapshot  # noqa: E402
from runtime.router import select_next  # noqa: E402
from runtime.turn_validate import validate_turn  # noqa: E402


TASK_ID = "TASK-6100"
ROUTING_CONFIG = {
    "routing_epoch": "property-v1",
    "routing_weights": {
        "active_claims": 10,
        "pending_reviews": 6,
        "pending_qa": 6,
        "open_fix_cycles": 4,
        "cooldown_penalty": 1,
        "capability_affinity": 1,
    },
}


class PropertyFailure(AssertionError):
    def __init__(self, message: str, counterexample: dict[str, Any] | None = None):
        super().__init__(message)
        self.counterexample = counterexample or {}


@dataclass(frozen=True)
class Sample:
    name: str
    invariants: tuple[str, ...]
    run: Callable[[str], None]


def check(condition: bool, message: str, counterexample: dict[str, Any] | None = None) -> None:
    if not condition:
        raise PropertyFailure(message, counterexample)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")


def agent(agent_id: str, capabilities: list[str], *, enabled: bool = True, max_active_claims: int | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {"id": agent_id, "capabilities": capabilities, "enabled": enabled}
    if max_active_claims is not None:
        payload["max_active_claims"] = max_active_claims
    return payload


def registry(*agents: dict[str, Any]) -> dict[str, Any]:
    return {
        "enabled": True,
        "routing_policy": "weighted_least_loaded_deterministic",
        "agents": list(agents),
    }


def roster_registry(size: int) -> dict[str, Any]:
    if size == 2:
        return registry(
            agent("Author", ["implementer", "reviewer", "qa"]),
            agent("ReviewerQA", ["reviewer", "qa", "orchestrator", "architect"]),
        )
    if size == 3:
        return registry(
            agent("Author", ["implementer", "reviewer", "qa"]),
            agent("Reviewer", ["reviewer", "orchestrator", "architect"]),
            agent("QA", ["qa"]),
        )
    if size == 5:
        return registry(
            agent("Author", ["implementer", "reviewer", "qa"]),
            agent("ReviewerA", ["reviewer", "orchestrator", "architect"]),
            agent("ReviewerB", ["reviewer"]),
            agent("QA1", ["qa"]),
            agent("QA2", ["qa"]),
        )
    raise ValueError(f"unsupported roster size: {size}")


def author_only_registry(size: int) -> dict[str, Any]:
    filler = [agent(f"Builder{index}", ["implementer"]) for index in range(1, size)]
    return registry(agent("Author", ["implementer", "reviewer", "qa", "orchestrator", "architect"]), *filler)


def task(task_id: str, status: str, **extra: Any) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "id": task_id,
        "owner": "Author",
        "author": "Author",
        "original_author": "Author",
        "status": status,
        "type": "implementation",
        "priority": "high",
        "phase": "P2",
        "file": f"Area_comun/tasks/{task_id}.md",
        "depends_on": [],
        "deliverables": [],
    }
    payload.update(extra)
    return payload


def state(
    tasks: list[dict[str, Any]],
    *,
    agents: dict[str, Any],
    claims: list[dict[str, Any]] | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
    return {
        "task_index": {"tasks": tasks},
        "claims": {"claims": claims or []},
        "mailbox_open": [],
        "agent_registry": agents,
        "config": config or ROUTING_CONFIG,
    }


def active_claim(owner: str, task_id: str, index: int) -> dict[str, Any]:
    return {
        "claim_id": f"CLAIM-{task_id}-{owner}-{index:04d}",
        "task_id": task_id,
        "owner": owner,
        "status": "active",
        "scope": [f"Area_comun/tasks/{task_id}.md"],
    }


def duplicate_active_claim_tasks(runtime_state: dict[str, Any]) -> dict[str, list[str]]:
    owners_by_task: dict[str, list[str]] = {}
    for claim in active_claims(runtime_state):
        task_id = str(claim.get("task_id") or "")
        if task_id:
            owners_by_task.setdefault(task_id, []).append(str(claim.get("owner") or ""))
    return {task_id: owners for task_id, owners in owners_by_task.items() if len(owners) > 1}


def sample_router_transition(roster_size: int, transition: str) -> Callable[[str], None]:
    def run(seed: str) -> None:
        task_id = f"TASK-62{roster_size}{1 if transition == 'review' else 2}"
        status = "in_review" if transition == "review" else "qa_pending"
        result = select_next(state([task(task_id, status)], agents=roster_registry(roster_size)))
        check(
            result is not None and result.get("action") == transition,
            "router did not select the expected transition",
            {"seed": seed, "roster_size": roster_size, "transition": transition, "result": result},
        )
        check(
            result.get("owner") != "Author",
            f"{transition} selected the task author",
            {"seed": seed, "roster_size": roster_size, "transition": transition, "result": result},
        )
        filtered = result.get("routing_decision", {}).get("explanation", {}).get("filtered", [])
        check(
            any(item.get("agent") == "Author" and item.get("reason") == "author_excluded" for item in filtered),
            "router did not expose author_excluded in the decision",
            {"seed": seed, "roster_size": roster_size, "transition": transition, "result": result},
        )

    return run


def sample_router_execute(roster_size: int) -> Callable[[str], None]:
    def run(seed: str) -> None:
        task_id = f"TASK-63{roster_size}0"
        runtime_state = state(
            [task(task_id, "ready", owner="LegacyOwner", required_capability="implementer")],
            agents=roster_registry(roster_size),
        )
        first = select_next(runtime_state)
        second = select_next(runtime_state)
        eligible = {
            item["id"]
            for item in roster_registry(roster_size)["agents"]
            if "implementer" in item.get("capabilities", []) and item.get("enabled") is True
        }
        check(first == second, "execute routing is not replay deterministic", {"seed": seed, "first": first, "second": second})
        check(first is not None and first.get("action") == "execute", "router did not select execute", {"seed": seed, "result": first})
        check(first.get("owner") in eligible, "execute owner lacks implementer capability", {"seed": seed, "eligible": sorted(eligible), "result": first})

    return run


def sample_router_author_only_escalates(transition: str) -> Callable[[str], None]:
    def run(seed: str) -> None:
        status = "in_review" if transition == "review" else "qa_pending"
        result = select_next(state([task("TASK-6401", status)], agents=author_only_registry(3)))
        check(result is not None and result.get("action") == "escalate", "author-only reviewer/QA did not escalate", {"seed": seed, "result": result})
        decision = result.get("routing_decision", {}).get("explanation", {})
        check(not decision.get("candidates"), "author-only reviewer/QA left eligible candidates", {"seed": seed, "result": result})
        check(
            any(item.get("agent") == "Author" and item.get("reason") == "author_excluded" for item in decision.get("filtered", [])),
            "author-only escalation did not record author_excluded",
            {"seed": seed, "result": result},
        )

    return run


def fixture_agents() -> list[dict[str, Any]]:
    return [
        agent("Author", ["implementer", "reviewer", "qa"]),
        agent("Reviewer", ["reviewer"]),
        agent("QA", ["qa"]),
        agent("Architect", ["architect", "orchestrator", "reviewer", "qa"]),
    ]


def build_turn_fixture(root: Path, task_payload: dict[str, Any], actor: str) -> None:
    write_json(
        root / "protocol.config.json",
        {
            "schema_version": "1.0",
            "agent_registry": {"enabled": True, "routing_policy": "weighted_least_loaded_deterministic", "agents": fixture_agents()},
            "routing_weights": ROUTING_CONFIG["routing_weights"],
            "domain_neutrality": {"enabled": False},
            "state_invariants": [{"path": "status", "equals": "active"}],
        },
    )
    write_json(
        root / "Area_comun/state/PROJECT_STATE.json",
        {"status": "active", "active_tasks": [{"id": TASK_ID, "owner": task_payload["owner"], "status": task_payload["status"]}]},
    )
    write_json(root / "Area_comun/state/TASK_INDEX.json", {"schema_version": "1.0", "tasks": [task_payload]})
    write_json(
        root / "Area_comun/state/CLAIMS.json",
        {
            "schema_version": "1.0",
            "claims": [
                {
                    "claim_id": f"CLAIM-{TASK_ID}-{actor}",
                    "task_id": TASK_ID,
                    "owner": actor,
                    "status": "active",
                    "scope": [
                        f"Area_comun/state/TASK_INDEX.json#{TASK_ID}",
                        f"Area_comun/state/PROJECT_STATE.json#active_tasks/{TASK_ID}",
                    ],
                }
            ],
        },
    )
    task_path = root / "Area_comun/tasks" / f"{TASK_ID}.md"
    task_path.parent.mkdir(parents=True, exist_ok=True)
    task_path.write_text(f"---\nid: {TASK_ID}\nstatus: {task_payload['status']}\n---\n\n# Fixture\n", encoding="utf-8")
    schema_target = root / "runtime/turn_schema.json"
    schema_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "runtime/turn_schema.json", schema_target)
    for folder in ("open", "answered", "archived"):
        (root / "Area_comun/mailbox" / folder).mkdir(parents=True, exist_ok=True)


def check_payload() -> dict[str, str]:
    return {"check_id": "unit", "error_class": "AssertionError", "artifact_path": "reports/property.txt"}


def turn_report(actor: str, from_status: str, to_status: str, review_qa: dict[str, Any] | None) -> dict[str, Any]:
    return {
        "turn_id": f"RUN-{actor}-{from_status}-{to_status}",
        "task_id": TASK_ID,
        "agent": actor,
        "outcome": "done" if to_status == "done" else "in_review" if to_status == "in_review" else "ok",
        "summary": "Exercise property transition.",
        "changed_paths": [],
        "transitions": {
            "task_status": {"from": from_status, "to": to_status},
            "review_qa": review_qa,
            "claims": [],
            "mailbox": [],
            "handoff": None,
        },
        "commit_message": "test(runtime): property transition",
        "gate": {"human_required": False},
        "next_hint": None,
    }


def validate_report_sample(
    seed: str,
    *,
    status: str,
    actor: str,
    to_status: str,
    review_qa: dict[str, Any] | None,
    expected_valid: bool,
    expected_error: str | None = None,
) -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-property-turn-") as temp:
        root = Path(temp)
        build_turn_fixture(root, task(TASK_ID, status), actor)
        report = turn_report(actor, status, to_status, review_qa)
        errors = validate_turn(report, root)
        valid = not errors
        check(
            valid is expected_valid,
            "turn_validate returned unexpected validity",
            {"seed": seed, "report": report, "expected_valid": expected_valid, "errors": errors},
        )
        if expected_error is not None:
            check(
                any(expected_error in error for error in errors),
                "turn_validate did not return expected error",
                {"seed": seed, "expected_error": expected_error, "errors": errors, "report": report},
            )


def sample_turn_execute_valid(seed: str) -> None:
    validate_report_sample(seed, status="ready", actor="Author", to_status="in_review", review_qa=None, expected_valid=True)


def sample_turn_review_non_author_valid(seed: str) -> None:
    validate_report_sample(
        seed,
        status="in_review",
        actor="Reviewer",
        to_status="changes_requested",
        review_qa={"event": "reject_review", "reviewer": "Reviewer", "checks_failed": [check_payload()]},
        expected_valid=True,
    )


def sample_turn_review_author_rejected(seed: str) -> None:
    validate_report_sample(
        seed,
        status="in_review",
        actor="Author",
        to_status="changes_requested",
        review_qa={"event": "reject_review", "reviewer": "Author", "checks_failed": [check_payload()]},
        expected_valid=False,
        expected_error="reviewer actor is task author",
    )


def sample_turn_qa_non_author_done_with_evidence(seed: str) -> None:
    validate_report_sample(
        seed,
        status="qa_pending",
        actor="QA",
        to_status="done",
        review_qa={"event": "pass_qa", "qa": "QA", "evidence": ["reports/qa-property.md"]},
        expected_valid=True,
    )


def sample_turn_qa_author_rejected(seed: str) -> None:
    validate_report_sample(
        seed,
        status="qa_pending",
        actor="Author",
        to_status="done",
        review_qa={"event": "pass_qa", "qa": "Author", "evidence": ["reports/qa-property.md"]},
        expected_valid=False,
        expected_error="qa actor is task author",
    )


def sample_turn_done_without_evidence_rejected(seed: str) -> None:
    validate_report_sample(
        seed,
        status="qa_pending",
        actor="QA",
        to_status="done",
        review_qa={"event": "pass_qa", "qa": "QA", "evidence": []},
        expected_valid=False,
        expected_error="pass_qa requires evidence",
    )


def sample_claims_unique(roster_size: int) -> Callable[[str], None]:
    def run(seed: str) -> None:
        claims = [active_claim(f"Owner{index}", f"TASK-65{roster_size}{index}", index) for index in range(1, roster_size + 1)]
        runtime_state = state([task(claim["task_id"], "in_progress") for claim in claims], agents=roster_registry(roster_size), claims=claims)
        duplicates = duplicate_active_claim_tasks(runtime_state)
        check(not duplicates, "generated valid claim state has duplicate active claims", {"seed": seed, "duplicates": duplicates, "claims": claims})

    return run


def sample_claims_double_attempt_detected(seed: str) -> None:
    claims = [
        active_claim("Author", "TASK-6601", 1),
        active_claim("Reviewer", "TASK-6601", 2),
    ]
    runtime_state = state([task("TASK-6601", "in_progress")], agents=roster_registry(3), claims=claims)
    duplicates = duplicate_active_claim_tasks(runtime_state)
    check(
        duplicates == {"TASK-6601": ["Author", "Reviewer"]},
        "double active claim attempt was not detected",
        {"seed": seed, "duplicates": duplicates, "claims": claims},
    )


def with_fixed_event_time(seed: str, callback: Callable[[Path], None]) -> None:
    original_utc_now = eventlog.utc_now
    eventlog.utc_now = lambda: f"2026-06-06T00:{int(seed[-3:]) % 60:02d}:00Z"
    try:
        with tempfile.TemporaryDirectory(prefix="runtime-property-eventlog-") as temp:
            callback(Path(temp))
    finally:
        eventlog.utc_now = original_utc_now


def sample_event_sequence(transition: str) -> Callable[[str], None]:
    def run(seed: str) -> None:
        def exercise(root: Path) -> None:
            writer = EventWriter(root)
            task_id = f"TASK-67{int(seed[-3:]) % 100:02d}"
            claim = writer.acquire_claim(
                task_id=task_id,
                owner="Author",
                lease_until="2026-06-06T01:00:00Z",
                idempotency_key=f"Author:{task_id}:claim:{seed}:0",
            )
            applied = writer.apply_intent(
                task_id=task_id,
                actor_id="Author",
                transition=transition,
                attempt_id=seed,
                fencing_token=int(claim["fencing_token"]),
                payload={"sample_seed": seed},
            )
            check(claim["seq"] == 1 and applied["seq"] == 2, "event seq did not increment monotonically", {"claim": claim, "applied": applied})
            check(
                claim["aggregate_version"] == 1 and applied["aggregate_version"] == 2,
                "applied event did not increment aggregate_version",
                {"claim": claim, "applied": applied},
            )
            for event in writer.events():
                if event.get("applied") is True:
                    check(
                        bool(event.get("actor")) and bool(event.get("actor_auth")),
                        "applied event is not attributed/authenticated",
                        {"event": event},
                    )
            snapshot = writer.write_snapshot()
            rebuilt = rebuild_snapshot(root)
            check(
                canonical_hash(snapshot["state"]) == canonical_hash(rebuilt["state"]),
                "replay snapshot hash mismatch",
                {"snapshot": snapshot, "rebuilt": rebuilt},
            )

        with_fixed_event_time(seed, exercise)

    return run


def sample_event_duplicate_intent_retry(seed: str) -> None:
    def exercise(root: Path) -> None:
        writer = EventWriter(root)
        task_id = "TASK-6801"
        claim = writer.acquire_claim(
            task_id=task_id,
            owner="Author",
            lease_until="2026-06-06T01:00:00Z",
            idempotency_key=f"Author:{task_id}:claim:{seed}:0",
        )
        first = writer.apply_intent(
            task_id=task_id,
            actor_id="Author",
            transition="execute",
            attempt_id=seed,
            fencing_token=int(claim["fencing_token"]),
        )
        duplicate = writer.apply_intent(
            task_id=task_id,
            actor_id="Author",
            transition="execute",
            attempt_id=seed,
            fencing_token=int(claim["fencing_token"]),
        )
        matching = [
            event
            for event in writer.events()
            if event.get("type") == "intent.applied"
            and event.get("aggregate_id") == task_id
            and (event.get("payload") or {}).get("attempt_id") == seed
        ]
        check(duplicate.get("deduped") is True, "duplicate intent retry was not deduped", {"first": first, "duplicate": duplicate})
        check(duplicate["seq"] == first["seq"], "duplicate intent changed seq", {"first": first, "duplicate": duplicate})
        check(len(matching) == 1, "duplicate intent was applied more than once", {"events": writer.events()})

    with_fixed_event_time(seed, exercise)


def sample_event_double_claim_attempt_current_lease(seed: str) -> None:
    def exercise(root: Path) -> None:
        writer = EventWriter(root)
        first = writer.acquire_claim(
            task_id="TASK-6802",
            owner="Author",
            lease_until="2026-06-06T01:00:00Z",
            idempotency_key=f"Author:TASK-6802:claim:{seed}:0",
        )
        second = writer.acquire_claim(
            task_id="TASK-6802",
            owner="Reviewer",
            lease_until="2026-06-06T02:00:00Z",
            idempotency_key=f"Reviewer:TASK-6802:claim:{seed}:1",
        )
        current = writer.state()["leases"]["TASK-6802"]
        check(second["seq"] == first["seq"] + 1, "claim reacquire did not advance seq", {"first": first, "second": second})
        check(second["aggregate_version"] == first["aggregate_version"] + 1, "claim reacquire did not advance aggregate_version", {"first": first, "second": second})
        check(second["fencing_token"] > first["fencing_token"], "claim reacquire did not advance fencing token", {"first": first, "second": second})
        check(
            current["owner"] == "Reviewer" and current["fencing_token"] == second["fencing_token"],
            "event log state does not keep exactly the latest active lease",
            {"state": writer.state(), "first": first, "second": second},
        )

    with_fixed_event_time(seed, exercise)


def samples() -> list[Sample]:
    generated: list[Sample] = []
    for roster_size in (2, 3, 5):
        generated.append(Sample(f"router-n{roster_size}-review-author-excluded", ("I1",), sample_router_transition(roster_size, "review")))
        generated.append(Sample(f"router-n{roster_size}-qa-author-excluded", ("I2",), sample_router_transition(roster_size, "qa")))
        generated.append(Sample(f"router-n{roster_size}-execute-deterministic", ("I5", "I6"), sample_router_execute(roster_size)))
        generated.append(Sample(f"claims-n{roster_size}-unique-active-by-task", ("I4",), sample_claims_unique(roster_size)))
    generated.extend(
        [
            Sample("router-author-only-review-escalates", ("I1",), sample_router_author_only_escalates("review")),
            Sample("router-author-only-qa-escalates", ("I2",), sample_router_author_only_escalates("qa")),
            Sample("turn-validate-execute-valid", ("I1", "I2", "I3"), sample_turn_execute_valid),
            Sample("turn-validate-review-non-author-valid", ("I1",), sample_turn_review_non_author_valid),
            Sample("turn-validate-review-author-rejected", ("I1",), sample_turn_review_author_rejected),
            Sample("turn-validate-qa-non-author-done-with-evidence", ("I2", "I3"), sample_turn_qa_non_author_done_with_evidence),
            Sample("turn-validate-qa-author-rejected", ("I2",), sample_turn_qa_author_rejected),
            Sample("turn-validate-done-without-evidence-rejected", ("I3",), sample_turn_done_without_evidence_rejected),
            Sample("claims-double-active-attempt-detected", ("I4",), sample_claims_double_attempt_detected),
            Sample("eventlog-execute-seq-replay-auth", ("I5", "I6", "I7"), sample_event_sequence("execute")),
            Sample("eventlog-review-seq-replay-auth", ("I5", "I6", "I7"), sample_event_sequence("review")),
            Sample("eventlog-qa-seq-replay-auth", ("I5", "I6", "I7"), sample_event_sequence("qa")),
            Sample("eventlog-duplicate-intent-retry-deduped", ("I8",), sample_event_duplicate_intent_retry),
            Sample("eventlog-double-claim-attempt-current-lease", ("I4", "I5", "I7"), sample_event_double_claim_attempt_current_lease),
        ]
    )
    return generated


def main() -> int:
    generated = samples()
    failures: list[dict[str, Any]] = []
    covered = sorted({invariant for sample in generated for invariant in sample.invariants})
    for index, sample in enumerate(generated, start=1):
        seed = f"property-{index:03d}"
        try:
            sample.run(seed)
        except Exception as exc:  # noqa: BLE001 - compact counterexample reporting
            failure: dict[str, Any] = {
                "sample": sample.name,
                "seed": seed,
                "invariants": list(sample.invariants),
                "error": str(exc),
            }
            counterexample = getattr(exc, "counterexample", None)
            if counterexample:
                failure["counterexample"] = counterexample
            failures.append(failure)

    if failures:
        print(json.dumps({"status": "FAILED", "failures": failures}, indent=2, ensure_ascii=False, sort_keys=True))
        return 1

    print(
        "OK: "
        f"{len(generated)} deterministic property samples passed "
        f"({', '.join(covered)}). "
        "Generation: enumerated rosters N=2/3/5; transitions review/qa/execute; "
        "claims include unique active states plus a double-claim attempt; "
        "event sequences include execute/review/qa, replay hash, attribution/auth, "
        "and duplicate intent retry. No random, clock-derived selection, network, or truncation."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
