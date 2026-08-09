#!/usr/bin/env python3
"""Deterministic concurrency simulation for the N-agent runtime.

Scenario size is fixed and declared: 10 implementers, 100 tasks, seed
``concurrency-v1``. The simulation is enumerated by construction: no random
numbers, no wall-clock decisions, no network, and no silent truncation.
"""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

import runtime.eventlog as eventlog  # noqa: E402
from runtime.eventlog import EventWriter, assert_snapshot_matches, canonical_hash, rebuild_snapshot  # noqa: E402
from runtime.router import evaluate_fairness, select_next  # noqa: E402
from runtime.turn_validate import validate_turn  # noqa: E402


SEED = "concurrency-v1"
IMPLEMENTER_COUNT = 10
TASK_COUNT = 100
DISABLE_AT = 50
DISABLED_AFTER_MIDPOINT = {"Impl09", "Impl10"}
COLLISION_INDICES = {3, 17, 41, 63, 88}
LEASE_RECLAIM_INDICES = {11, 37, 72}
TURN_VALIDATE_INDICES = {0, 50, 99}
FAIRNESS_RATIO = 3.0
MAX_WEIGHTED_SHARE_DELTA = 0.12

ROUTING_CONFIG = {
    "routing_epoch": SEED,
    "routing_weights": {
        "active_claims": 10,
        "pending_reviews": 6,
        "pending_qa": 6,
        "open_fix_cycles": 4,
        "cooldown_penalty": 1,
        "capability_affinity": 1,
    },
}


class SimulationFailure(AssertionError):
    def __init__(self, message: str, counterexample: dict[str, Any] | None = None):
        super().__init__(message)
        self.counterexample = counterexample or {}


def fail(message: str, counterexample: dict[str, Any] | None = None) -> None:
    raise SimulationFailure(message, counterexample)


def check(condition: bool, message: str, counterexample: dict[str, Any] | None = None) -> None:
    if not condition:
        fail(message, counterexample)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")


def implementer_ids() -> list[str]:
    return [f"Impl{index:02d}" for index in range(1, IMPLEMENTER_COUNT + 1)]


def enabled_agents_for(task_index: int) -> set[str]:
    enabled = set(implementer_ids())
    if task_index >= DISABLE_AT:
        enabled -= DISABLED_AFTER_MIDPOINT
    return enabled


def agent(agent_id: str, *, enabled: bool) -> dict[str, Any]:
    return {"id": agent_id, "capabilities": ["implementer"], "enabled": enabled}


def registry_for(task_index: int) -> dict[str, Any]:
    enabled = enabled_agents_for(task_index)
    return {
        "enabled": True,
        "routing_policy": "weighted_least_loaded_deterministic",
        "agents": [agent(agent_id, enabled=agent_id in enabled) for agent_id in implementer_ids()],
    }


def task_payload(task_id: str, status: str = "ready") -> dict[str, Any]:
    return {
        "id": task_id,
        "owner": "RuntimeOwner",
        "status": status,
        "type": "implementation",
        "priority": "high",
        "phase": "P2",
        "file": f"Area_comun/tasks/{task_id}.md",
        "depends_on": [],
        "deliverables": [],
        "required_capability": "implementer",
    }


def router_state(task_id: str, task_index: int, active_claims: list[dict[str, Any]]) -> dict[str, Any]:
    return {
        "task_index": {"tasks": [task_payload(task_id)]},
        "claims": {"claims": active_claims},
        "mailbox_open": [],
        "agent_registry": registry_for(task_index),
        "config": ROUTING_CONFIG,
    }


def claim_for_router(task_id: str, owner: str, index: int) -> dict[str, Any]:
    return {
        "claim_id": f"CLAIM-{task_id}-{owner}-{index:04d}",
        "task_id": task_id,
        "owner": owner,
        "status": "active",
        "scope": [f"Area_comun/tasks/{task_id}.md"],
    }


def other_enabled_agent(owner: str, task_index: int) -> str:
    enabled = enabled_agents_for(task_index)
    for candidate in implementer_ids():
        if candidate not in enabled:
            continue
        if candidate != owner:
            return candidate
    fail("no alternate enabled agent", {"owner": owner, "task_index": task_index})
    return owner


def build_turn_fixture(root: Path, task_id: str, actor: str) -> None:
    agents = [{"id": item, "capabilities": ["implementer"], "enabled": True} for item in implementer_ids()]
    write_json(
        root / "protocol.config.json",
        {
            "schema_version": "1.0",
            "agent_registry": {
                "enabled": True,
                "routing_policy": "weighted_least_loaded_deterministic",
                "agents": agents,
            },
            "routing_weights": ROUTING_CONFIG["routing_weights"],
            "domain_neutrality": {"enabled": False},
            "state_invariants": [{"path": "status", "equals": "active"}],
        },
    )
    write_json(root / "Area_comun/state/PROJECT_STATE.json", {"status": "active"})
    write_json(root / "Area_comun/state/TASK_INDEX.json", {"schema_version": "1.0", "tasks": [task_payload(task_id)]})
    write_json(
        root / "Area_comun/state/CLAIMS.json",
        {
            "schema_version": "1.0",
            "claims": [
                {
                    "claim_id": f"CLAIM-{task_id}-{actor}",
                    "task_id": task_id,
                    "owner": actor,
                    "status": "active",
                    "scope": [
                        f"Area_comun/state/TASK_INDEX.json#{task_id}",
                        f"Area_comun/state/PROJECT_STATE.json#active_tasks/{task_id}",
                    ],
                }
            ],
        },
    )
    task_path = root / "Area_comun/tasks" / f"{task_id}.md"
    task_path.parent.mkdir(parents=True, exist_ok=True)
    task_path.write_text(f"---\nid: {task_id}\nstatus: ready\n---\n\n# Fixture\n", encoding="utf-8")
    schema_target = root / "runtime/turn_schema.json"
    schema_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "runtime/turn_schema.json", schema_target)
    for folder in ("open", "answered", "archived"):
        (root / "Area_comun/mailbox" / folder).mkdir(parents=True, exist_ok=True)


def validate_execute_turn(task_id: str, actor: str, sample_index: int) -> None:
    report = {
        "turn_id": f"RUN-{SEED}-{sample_index:03d}",
        "task_id": task_id,
        "agent": actor,
        "outcome": "in_review",
        "summary": "Concurrency simulation execute transition.",
        "changed_paths": [],
        "obstacles": [],
        "transitions": {
            "task_status": {"from": "ready", "to": "in_review"},
            "review_qa": None,
            "claims": [],
            "mailbox": [],
            "handoff": None,
        },
        "commit_message": "test(runtime): concurrency execute transition",
        "gate": {"human_required": False},
        "next_hint": None,
    }
    with tempfile.TemporaryDirectory(prefix="runtime-concurrency-turn-") as temp:
        root = Path(temp)
        build_turn_fixture(root, task_id, actor)
        errors = validate_turn(report, root)
        check(not errors, "turn_validate rejected execute sample", {"sample_index": sample_index, "report": report, "errors": errors})


def apply_success_with_duplicate(
    writer: EventWriter,
    *,
    task_id: str,
    actor: str,
    fencing_token: int,
    attempt_id: str,
    metrics: dict[str, Any],
) -> dict[str, Any]:
    first = writer.apply_intent(
        task_id=task_id,
        actor_id=actor,
        transition="execute",
        attempt_id=attempt_id,
        fencing_token=fencing_token,
        payload={"seed": SEED},
    )
    duplicate = writer.apply_intent(
        task_id=task_id,
        actor_id=actor,
        transition="execute",
        attempt_id=attempt_id,
        fencing_token=fencing_token,
        payload={"seed": SEED},
    )
    check(duplicate.get("deduped") is True, "duplicate intent retry was not deduped", {"task_id": task_id, "first": first, "duplicate": duplicate})
    check(duplicate["seq"] == first["seq"], "duplicate intent retry changed seq", {"task_id": task_id, "first": first, "duplicate": duplicate})
    metrics["duplicate_retries"] += 1
    metrics["dedups"] += 1
    return first


def simulate() -> dict[str, Any]:
    original_utc_now = eventlog.utc_now
    eventlog.utc_now = lambda: "2026-06-06T00:00:00Z"
    try:
        with tempfile.TemporaryDirectory(prefix="runtime-concurrency-") as temp:
            root = Path(temp)
            writer = EventWriter(root)
            router_claims: list[dict[str, Any]] = []
            assignments: list[dict[str, Any]] = []
            assignment_counts = {agent_id: 0 for agent_id in implementer_ids()}
            post_disable_assignments: list[dict[str, Any]] = []
            successful_attempts: set[str] = set()
            metrics: dict[str, Any] = {
                "seed": SEED,
                "implementers": IMPLEMENTER_COUNT,
                "tasks": TASK_COUNT,
                "disabled_at": DISABLE_AT,
                "disabled_agents": sorted(DISABLED_AFTER_MIDPOINT),
                "collisions": 0,
                "lease_reclaims": 0,
                "stale_fencing_rejections": 0,
                "duplicate_retries": 0,
                "dedups": 0,
                "turn_validate_samples": 0,
            }

            for index in range(TASK_COUNT):
                task_id = f"TASK-{6001 + index:04d}"
                selected = select_next(router_state(task_id, index, router_claims))
                check(selected is not None, "router returned no assignment", {"index": index, "task_id": task_id})
                check(selected.get("action") == "execute", "router did not select execute", {"index": index, "selected": selected})
                owner = str(selected.get("owner") or "")
                check(owner in enabled_agents_for(index), "router assigned a disabled agent", {"index": index, "owner": owner, "selected": selected})

                explanation = selected.get("routing_decision", {}).get("explanation", {})
                eligible = [str(item.get("agent")) for item in explanation.get("candidates") or [] if item.get("agent")]
                assignments.append({"selected": owner, "eligible_agents": eligible, "weights": {agent_id: 1 for agent_id in eligible}})
                if index >= DISABLE_AT:
                    post_disable_assignments.append({"index": index, "owner": owner})
                assignment_counts[owner] += 1
                router_claims.append(claim_for_router(task_id, owner, index))

                if index in TURN_VALIDATE_INDICES:
                    validate_execute_turn(task_id, owner, index)
                    metrics["turn_validate_samples"] += 1

                claim = writer.acquire_claim(
                    task_id=task_id,
                    owner=owner,
                    lease_until=f"2026-06-06T01:{index % 60:02d}:00Z",
                    idempotency_key=f"{owner}:{task_id}:claim:{SEED}:{index}:0",
                )

                if index in COLLISION_INDICES:
                    loser = other_enabled_agent(owner, index)
                    rejected = writer.apply_intent(
                        task_id=task_id,
                        actor_id=loser,
                        transition="execute",
                        attempt_id=f"{SEED}-collision-{index}",
                        fencing_token=0,
                        payload={"collision_with": owner},
                    )
                    check(rejected["type"] == "state.stale_fencing_rejected", "collision was not recorded as stale fencing", {"index": index, "event": rejected})
                    check(rejected.get("applied") is False, "collision rejection was applied", {"index": index, "event": rejected})
                    metrics["collisions"] += 1
                    metrics["stale_fencing_rejections"] += 1

                final_owner = owner
                final_fencing = int(claim["fencing_token"])
                if index in LEASE_RECLAIM_INDICES:
                    reclaimer = other_enabled_agent(owner, index)
                    fresh = writer.acquire_claim(
                        task_id=task_id,
                        owner=reclaimer,
                        lease_until=f"2026-06-06T02:{index % 60:02d}:00Z",
                        idempotency_key=f"{reclaimer}:{task_id}:claim:{SEED}:{index}:1",
                    )
                    stale = writer.apply_intent(
                        task_id=task_id,
                        actor_id=owner,
                        transition="execute",
                        attempt_id=f"{SEED}-expired-{index}",
                        fencing_token=final_fencing,
                        payload={"reclaimed_by": reclaimer},
                    )
                    check(fresh["fencing_token"] > final_fencing, "re-claim did not advance fencing token", {"index": index, "claim": claim, "fresh": fresh})
                    check(stale["type"] == "state.stale_fencing_rejected", "expired lease did not record stale fencing rejection", {"index": index, "event": stale})
                    final_owner = reclaimer
                    final_fencing = int(fresh["fencing_token"])
                    metrics["lease_reclaims"] += 1
                    metrics["stale_fencing_rejections"] += 1

                attempt_id = f"{SEED}-apply-{index}"
                apply_success_with_duplicate(
                    writer,
                    task_id=task_id,
                    actor=final_owner,
                    fencing_token=final_fencing,
                    attempt_id=attempt_id,
                    metrics=metrics,
                )
                successful_attempts.add(f"{final_owner}:{task_id}:execute:{attempt_id}:{final_fencing}")

            fairness = evaluate_fairness(
                assignments,
                minimum_sample=10,
                max_fairness_ratio=FAIRNESS_RATIO,
                max_weighted_share_delta=MAX_WEIGHTED_SHARE_DELTA,
            )
            check(fairness["ok"] is True, "fairness gate failed", {"fairness": fairness, "assignment_counts": assignment_counts})
            disabled_late = [item for item in post_disable_assignments if item["owner"] in DISABLED_AFTER_MIDPOINT]
            check(not disabled_late, "disabled agent received an assignment after disable point", {"disabled_late": disabled_late})

            snapshot = writer.write_snapshot()
            assert_snapshot_matches(root)
            rebuilt = rebuild_snapshot(root)
            check(
                canonical_hash(snapshot["state"]) == canonical_hash(rebuilt["state"]),
                "snapshot hash mismatch after replay",
                {"snapshot": snapshot, "rebuilt": rebuilt},
            )

            events = writer.events()
            applied_intents = [event for event in events if event.get("type") == "intent.applied" and event.get("applied") is True]
            stale_rejections = [event for event in events if event.get("type") == "state.stale_fencing_rejected"]
            unique_applied_keys = {str(event.get("idempotency_key")) for event in applied_intents}
            check(len(applied_intents) == TASK_COUNT, "unexpected number of applied intents", {"applied": len(applied_intents), "expected": TASK_COUNT})
            check(len(unique_applied_keys) == len(applied_intents), "an intent was applied more than once", {"applied_intents": applied_intents})
            check(len(successful_attempts) == TASK_COUNT, "successful attempt set is incomplete", {"successful_attempts": len(successful_attempts)})
            check(len(stale_rejections) == metrics["stale_fencing_rejections"], "stale rejection metric mismatch", {"metrics": metrics, "events": stale_rejections})

            metrics.update(
                {
                    "assignment_counts": assignment_counts,
                    "fairness": fairness,
                    "applied_intents": len(applied_intents),
                    "unique_applied_intents": len(unique_applied_keys),
                    "events": len(events),
                    "snapshot_hash": canonical_hash(snapshot["state"]),
                }
            )
            return metrics
    finally:
        eventlog.utc_now = original_utc_now


def main() -> int:
    try:
        metrics = simulate()
    except Exception as exc:  # noqa: BLE001 - compact reproducible failure report
        failure: dict[str, Any] = {"status": "FAILED", "seed": SEED, "error": str(exc)}
        counterexample = getattr(exc, "counterexample", None)
        if counterexample:
            failure["counterexample"] = counterexample
        print(json.dumps(failure, indent=2, ensure_ascii=False, sort_keys=True))
        return 1

    print(
        "OK: deterministic concurrency simulation passed "
        f"(seed={SEED}, implementers={IMPLEMENTER_COUNT}, tasks={TASK_COUNT}). "
        f"assignments={metrics['assignment_counts']}; "
        f"collisions={metrics['collisions']}; lease_reclaims={metrics['lease_reclaims']}; "
        f"stale_fencing_rejections={metrics['stale_fencing_rejections']}; "
        f"dedups={metrics['dedups']}; applied_intents={metrics['applied_intents']}; "
        f"fairness_ratio={metrics['fairness']['fairness_ratio']}; "
        f"max_weighted_share_delta={metrics['fairness']['max_weighted_share_delta']}; "
        f"snapshot_hash={metrics['snapshot_hash']}. "
        "No random, wall-clock selection, network, runtime edits, or truncation."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
