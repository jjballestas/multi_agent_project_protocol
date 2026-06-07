#!/usr/bin/env python3
"""Read-only protocol state replay helpers.

B.1 intentionally observes drift only. It does not write hot state and does not
change the apply/orchestrator write path.
"""

from __future__ import annotations

import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

try:
    from .eventlog import all_events, canonical_hash, read_protocol_config
except ImportError:  # pragma: no cover - direct script execution
    from eventlog import all_events, canonical_hash, read_protocol_config


PROTOCOL_STATE_PATHS = {
    "task_index": Path("Area_comun/state/TASK_INDEX.json"),
    "project_state": Path("Area_comun/state/PROJECT_STATE.json"),
    "claims": Path("Area_comun/state/CLAIMS.json"),
}
TASK_TRANSITION_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_-]*)\s*->\s*([A-Za-z_][A-Za-z0-9_-]*)\s*$")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def event_state_enabled(config: dict[str, Any] | None) -> bool:
    event_state = (config or {}).get("event_state")
    return isinstance(event_state, dict) and event_state.get("enabled") is True


def sort_by_key(items: list[Any], key: str) -> list[Any]:
    return sorted(
        items,
        key=lambda item: str(item.get(key) or "") if isinstance(item, dict) else json.dumps(item, sort_keys=True),
    )


def canonicalize_document(name: str, document: dict[str, Any] | None) -> dict[str, Any]:
    doc = deepcopy(document) if isinstance(document, dict) else {}
    if name == "task_index":
        doc["tasks"] = sort_by_key([item for item in doc.get("tasks") or [] if isinstance(item, dict)], "id")
    elif name == "project_state":
        doc["active_tasks"] = sort_by_key([item for item in doc.get("active_tasks") or [] if isinstance(item, dict)], "id")
        if isinstance(doc.get("decisions"), list):
            doc["decisions"] = sorted(str(item) for item in doc["decisions"])
    elif name == "claims":
        doc["claims"] = sort_by_key([item for item in doc.get("claims") or [] if isinstance(item, dict)], "claim_id")
    return doc


def canonicalize_protocol_state(state: dict[str, Any] | None) -> dict[str, Any]:
    state = state if isinstance(state, dict) else {}
    return {
        "task_index": canonicalize_document("task_index", state.get("task_index")),
        "project_state": canonicalize_document("project_state", state.get("project_state")),
        "claims": canonicalize_document("claims", state.get("claims")),
    }


def empty_protocol_state() -> dict[str, Any]:
    return canonicalize_protocol_state(
        {
            "task_index": {"schema_version": "1.0", "tasks": []},
            "project_state": {"status": "active", "decisions": [], "active_tasks": []},
            "claims": {"schema_version": "1.0", "claims": []},
        }
    )


def load_hot_protocol_state(root: Path) -> dict[str, Any]:
    root = root.resolve()
    return canonicalize_protocol_state(
        {
            name: read_json(root / relative)
            for name, relative in PROTOCOL_STATE_PATHS.items()
            if (root / relative).exists()
        }
    )


def materialize_protocol_state(snapshot_or_state: dict[str, Any]) -> dict[str, Any]:
    state = snapshot_or_state.get("state") if isinstance(snapshot_or_state.get("state"), dict) else snapshot_or_state
    canonical = canonicalize_protocol_state(state)
    return {
        PROTOCOL_STATE_PATHS["task_index"].as_posix(): canonical["task_index"],
        PROTOCOL_STATE_PATHS["project_state"].as_posix(): canonical["project_state"],
        PROTOCOL_STATE_PATHS["claims"].as_posix(): canonical["claims"],
    }


def protocol_snapshot(state: dict[str, Any], *, up_to_seq: int = 0) -> dict[str, Any]:
    canonical = canonicalize_protocol_state(state)
    return {
        "up_to_seq": int(up_to_seq or 0),
        "state": canonical,
        "canonical_hash": canonical_hash(materialize_protocol_state(canonical)),
    }


def build_genesis_snapshot(root: Path) -> dict[str, Any]:
    return protocol_snapshot(load_hot_protocol_state(root), up_to_seq=0)


def task_id_from_event(event: dict[str, Any], payload: dict[str, Any]) -> str:
    return str(payload.get("task_id") or event.get("aggregate_id") or "").strip()


def update_or_append(items: list[dict[str, Any]], key: str, value: str, patch: dict[str, Any]) -> None:
    for item in items:
        if str(item.get(key) or "") == value:
            item.update(patch)
            return
    items.append(dict(patch))


def remove_by_key(items: list[dict[str, Any]], key: str, value: str) -> None:
    items[:] = [item for item in items if str(item.get(key) or "") != value]


def set_task_status(state: dict[str, Any], task_id: str, status: str) -> None:
    if not task_id or not status:
        return
    tasks = state.setdefault("task_index", {}).setdefault("tasks", [])
    active = state.setdefault("project_state", {}).setdefault("active_tasks", [])
    update_or_append(tasks, "id", task_id, {"id": task_id, "status": status})
    update_or_append(active, "id", task_id, {"id": task_id, "status": status})


def upsert_task(state: dict[str, Any], task: dict[str, Any]) -> None:
    task_id = str(task.get("id") or "").strip()
    if not task_id:
        return
    tasks = state.setdefault("task_index", {}).setdefault("tasks", [])
    update_or_append(tasks, "id", task_id, task)
    active_payload = {"id": task_id, "owner": task.get("owner"), "status": task.get("status"), "title": task.get("title")}
    active_payload = {key: value for key, value in active_payload.items() if value is not None}
    active = state.setdefault("project_state", {}).setdefault("active_tasks", [])
    update_or_append(active, "id", task_id, active_payload)


def apply_task_transition_event(state: dict[str, Any], event: dict[str, Any], payload: dict[str, Any]) -> None:
    task = payload.get("task")
    if isinstance(task, dict):
        upsert_task(state, task)
        return
    task_id = task_id_from_event(event, payload)
    status = str(payload.get("status") or payload.get("to") or "").strip()
    transition = str(payload.get("transition") or "")
    if not status:
        match = TASK_TRANSITION_RE.match(transition)
        if match:
            status = match.group(2)
    set_task_status(state, task_id, status)


def apply_claim_event(state: dict[str, Any], event: dict[str, Any], payload: dict[str, Any]) -> None:
    claims = state.setdefault("claims", {}).setdefault("claims", [])
    claim = payload.get("claim")
    if isinstance(claim, dict):
        claim_id = str(claim.get("claim_id") or "").strip()
        if claim_id:
            update_or_append(claims, "claim_id", claim_id, claim)
        return
    claim_id = str(payload.get("claim_id") or event.get("idempotency_key") or "").strip()
    if not claim_id:
        owner = str(payload.get("owner") or event.get("actor") or "")
        task_id = task_id_from_event(event, payload)
        claim_id = f"CLAIM-{task_id}-{owner}".strip("-")
    if event.get("type") in {"claim.released", "claim.blocked"}:
        status = "blocked" if event.get("type") == "claim.blocked" else "released"
        update_or_append(claims, "claim_id", claim_id, {"claim_id": claim_id, "status": status})
        return
    update_or_append(
        claims,
        "claim_id",
        claim_id,
        {
            "claim_id": claim_id,
            "task_id": task_id_from_event(event, payload),
            "owner": payload.get("owner") or event.get("actor"),
            "status": payload.get("status") or "active",
        },
    )


def apply_decision_event(state: dict[str, Any], payload: dict[str, Any]) -> None:
    decision_id = str(payload.get("decision_id") or payload.get("id") or "").strip()
    if not decision_id:
        return
    decisions = state.setdefault("project_state", {}).setdefault("decisions", [])
    if decision_id not in decisions:
        decisions.append(decision_id)


def apply_intent_event(state: dict[str, Any], event: dict[str, Any], payload: dict[str, Any]) -> None:
    transition = payload.get("transition")
    if isinstance(transition, str):
        apply_task_transition_event(state, event, {"task_id": task_id_from_event(event, payload), "transition": transition})
    transitions = payload.get("transitions")
    if isinstance(transitions, dict):
        task_transition = transitions.get("task_status")
        if isinstance(task_transition, dict):
            apply_task_transition_event(
                state,
                event,
                {
                    "task_id": task_id_from_event(event, payload),
                    "to": task_transition.get("to"),
                },
            )
        for claim_transition in transitions.get("claims") or []:
            if isinstance(claim_transition, dict):
                op = claim_transition.get("op")
                claim_payload = dict(claim_transition)
                claim_payload.setdefault("status", "released" if op == "release" else "active")
                apply_claim_event(state, {"type": "claim.released" if op == "release" else "claim.upserted"}, claim_payload)


def replay_protocol_state(
    events: list[dict[str, Any]],
    base_state: dict[str, Any] | None = None,
    forbidden_callback: Callable[[], None] | None = None,
) -> dict[str, Any]:
    if forbidden_callback is not None:
        # Deliberately unused: replay is pure and must not call external effects.
        pass
    state = canonicalize_protocol_state(base_state) if base_state is not None else empty_protocol_state()
    up_to_seq = 0
    for event in sorted(events, key=lambda item: int(item.get("seq") or 0)):
        if event.get("applied", True) is False:
            up_to_seq = max(up_to_seq, int(event.get("seq") or 0))
            continue
        event_type = str(event.get("type") or "")
        payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
        if event_type in {"protocol.genesis", "protocol_state.genesis"}:
            genesis = payload.get("state") or payload.get("protocol_state")
            if isinstance(genesis, dict):
                state = canonicalize_protocol_state(genesis)
        elif event_type in {"task.created", "task.upserted", "task.status_changed", "protocol.task_status_changed"}:
            apply_task_transition_event(state, event, payload)
        elif event_type in {"claim.acquired", "claim.upserted", "claim.released", "claim.blocked"}:
            apply_claim_event(state, event, payload)
        elif event_type in {"decision.accepted", "decision.recorded"}:
            apply_decision_event(state, payload)
        elif event_type == "intent.applied":
            apply_intent_event(state, event, payload)
        up_to_seq = max(up_to_seq, int(event.get("seq") or 0))
    return protocol_snapshot(state, up_to_seq=up_to_seq)


def current_protocol_snapshot(root: Path) -> dict[str, Any]:
    return replay_protocol_state(all_events(root))


def drift_entries(hot: dict[str, Any], materialized: dict[str, Any]) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for path in sorted(set(hot) | set(materialized)):
        hot_hash = canonical_hash(hot.get(path) or {})
        replay_hash = canonical_hash(materialized.get(path) or {})
        if hot_hash != replay_hash:
            entries.append({"path": path, "hot_hash": hot_hash, "replay_hash": replay_hash})
    return entries


def protocol_state_drift(root: Path) -> dict[str, Any]:
    root = root.resolve()
    hot_snapshot = build_genesis_snapshot(root)
    replay_snapshot = current_protocol_snapshot(root)
    hot = materialize_protocol_state(hot_snapshot)
    materialized = materialize_protocol_state(replay_snapshot)
    entries = drift_entries(hot, materialized)
    return {
        "enabled": event_state_enabled(read_protocol_config(root)),
        "has_drift": bool(entries),
        "up_to_seq": replay_snapshot["up_to_seq"],
        "entries": entries,
        "hot_hash": canonical_hash(hot),
        "replay_hash": canonical_hash(materialized),
    }
