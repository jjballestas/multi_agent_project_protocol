#!/usr/bin/env python3
"""Append-only event log primitives for the N-agent runtime."""

from __future__ import annotations

import hashlib
import json
import os
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


EVENT_SCHEMA_VERSION = "1.0"
LOG_PATH = Path("runtime") / "state" / "events.jsonl"
SNAPSHOT_PATH = Path("runtime") / "state" / "snapshot.json"
ARCHIVE_DIR = Path("runtime") / "state" / "archives"


class EventLogError(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_jsonl_torn_safe(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    events: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8-sig").splitlines():
        if not line.strip():
            continue
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            break
        if not isinstance(event, dict):
            break
        events.append(event)
    return events


def atomic_append_jsonl(path: Path, event: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())


def canonical_json(payload: Any) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def canonical_hash(payload: Any) -> str:
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def empty_snapshot() -> dict[str, Any]:
    return {
        "up_to_seq": 0,
        "state": {
            "aggregate_versions": {},
            "fencing_tokens": {},
            "leases": {},
            "idempotency_keys": {},
            "events_applied": 0,
            "rejections": [],
        },
    }


def load_snapshot(root: Path) -> dict[str, Any]:
    path = root / SNAPSHOT_PATH
    if not path.exists():
        return empty_snapshot()
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write_snapshot(root: Path, snapshot: dict[str, Any]) -> None:
    path = root / SNAPSHOT_PATH
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(snapshot, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    temp.replace(path)


def all_events(root: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    archive_dir = root / ARCHIVE_DIR
    if archive_dir.exists():
        for path in sorted(archive_dir.glob("events-*.jsonl")):
            events.extend(read_jsonl_torn_safe(path))
    events.extend(read_jsonl_torn_safe(root / LOG_PATH))
    return sorted(events, key=lambda event: int(event.get("seq") or 0))


def replay_events(events: list[dict[str, Any]], base_state: dict[str, Any] | None = None) -> dict[str, Any]:
    state = deepcopy(base_state) if base_state is not None else empty_snapshot()["state"]
    state.setdefault("aggregate_versions", {})
    state.setdefault("fencing_tokens", {})
    state.setdefault("leases", {})
    state.setdefault("idempotency_keys", {})
    state.setdefault("events_applied", 0)
    state.setdefault("rejections", [])

    for event in sorted(events, key=lambda item: int(item.get("seq") or 0)):
        event_type = str(event.get("type") or "")
        aggregate_id = str(event.get("aggregate_id") or "")
        key = event.get("idempotency_key")
        if key:
            state["idempotency_keys"][str(key)] = int(event.get("seq") or 0)
        if aggregate_id and event.get("applied", True) is True:
            state["aggregate_versions"][aggregate_id] = int(event.get("aggregate_version") or 0)
        if aggregate_id and isinstance(event.get("fencing_token"), int):
            current = int(state["fencing_tokens"].get(aggregate_id) or 0)
            state["fencing_tokens"][aggregate_id] = max(current, int(event["fencing_token"]))
        if event_type == "claim.acquired" and aggregate_id:
            payload = event.get("payload") or {}
            state["leases"][aggregate_id] = {
                "owner": payload.get("owner"),
                "lease_until": payload.get("lease_until"),
                "fencing_token": event.get("fencing_token"),
            }
        if event_type == "state.stale_fencing_rejected":
            state["rejections"].append(
                {
                    "seq": event.get("seq"),
                    "aggregate_id": aggregate_id,
                    "fencing_token": event.get("fencing_token"),
                    "current_fencing_token": (event.get("payload") or {}).get("current_fencing_token"),
                }
            )
        state["events_applied"] = int(state["events_applied"]) + 1
    return state


def rebuild_snapshot(root: Path) -> dict[str, Any]:
    events = all_events(root)
    snapshot = {
        "up_to_seq": int(events[-1]["seq"]) if events else 0,
        "state": replay_events(events),
    }
    snapshot["canonical_hash"] = canonical_hash(snapshot["state"])
    return snapshot


def assert_snapshot_matches(root: Path) -> None:
    stored = load_snapshot(root)
    rebuilt = rebuild_snapshot(root)
    if int(stored.get("up_to_seq") or 0) != int(rebuilt.get("up_to_seq") or 0):
        raise EventLogError("snapshot mismatch: up_to_seq differs")
    if canonical_hash(stored.get("state") or {}) != canonical_hash(rebuilt.get("state") or {}):
        raise EventLogError("snapshot mismatch: state hash differs")


class EventWriter:
    def __init__(self, root: Path):
        self.root = root.resolve()

    @property
    def log_path(self) -> Path:
        return self.root / LOG_PATH

    def events(self) -> list[dict[str, Any]]:
        return all_events(self.root)

    def state(self) -> dict[str, Any]:
        return replay_events(self.events())

    def next_seq(self) -> int:
        events = self.events()
        return (int(events[-1].get("seq") or 0) + 1) if events else 1

    def append_event(
        self,
        *,
        event_type: str,
        aggregate_id: str,
        actor_id: str,
        payload: dict[str, Any] | None = None,
        idempotency_key: str | None = None,
        fencing_token: int | None = None,
        applied: bool = True,
        actor_auth: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        state = self.state()
        if idempotency_key and idempotency_key in state.get("idempotency_keys", {}):
            seq = int(state["idempotency_keys"][idempotency_key])
            for event in self.events():
                if int(event.get("seq") or 0) == seq:
                    result = dict(event)
                    result["deduped"] = True
                    return result

        current_version = int(state.get("aggregate_versions", {}).get(aggregate_id) or 0)
        event = {
            "seq": self.next_seq(),
            "event_schema_version": EVENT_SCHEMA_VERSION,
            "type": event_type,
            "aggregate_id": aggregate_id,
            "aggregate_version": current_version + 1 if applied else current_version,
            "actor": actor_id,
            "actor_auth": actor_auth or {"method": "not_enforced_phase2"},
            "idempotency_key": idempotency_key,
            "fencing_token": fencing_token,
            "payload": payload or {},
            "applied": applied,
            "ts": utc_now(),
        }
        atomic_append_jsonl(self.log_path, event)
        return event

    def acquire_claim(
        self,
        *,
        task_id: str,
        owner: str,
        lease_until: str,
        idempotency_key: str,
    ) -> dict[str, Any]:
        state = self.state()
        fencing = int(state.get("fencing_tokens", {}).get(task_id) or 0) + 1
        return self.append_event(
            event_type="claim.acquired",
            aggregate_id=task_id,
            actor_id=owner,
            idempotency_key=idempotency_key,
            fencing_token=fencing,
            payload={"task_id": task_id, "owner": owner, "lease_until": lease_until},
        )

    def apply_intent(
        self,
        *,
        task_id: str,
        actor_id: str,
        transition: str,
        attempt_id: str,
        fencing_token: int,
        payload: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        state = self.state()
        current_fencing = int(state.get("fencing_tokens", {}).get(task_id) or 0)
        key = f"{actor_id}:{task_id}:{transition}:{attempt_id}:{fencing_token}"
        if fencing_token < current_fencing:
            return self.append_event(
                event_type="state.stale_fencing_rejected",
                aggregate_id=task_id,
                actor_id=actor_id,
                fencing_token=fencing_token,
                applied=False,
                payload={
                    "transition": transition,
                    "attempt_id": attempt_id,
                    "current_fencing_token": current_fencing,
                    **(payload or {}),
                },
            )
        return self.append_event(
            event_type="intent.applied",
            aggregate_id=task_id,
            actor_id=actor_id,
            idempotency_key=key,
            fencing_token=fencing_token,
            payload={"transition": transition, "attempt_id": attempt_id, **(payload or {})},
        )

    def write_snapshot(self) -> dict[str, Any]:
        snapshot = rebuild_snapshot(self.root)
        write_snapshot(self.root, snapshot)
        return snapshot

    def compact_through(self, up_to_seq: int) -> Path | None:
        live_events = read_jsonl_torn_safe(self.log_path)
        archive_events = [event for event in live_events if int(event.get("seq") or 0) <= up_to_seq]
        remaining = [event for event in live_events if int(event.get("seq") or 0) > up_to_seq]
        if not archive_events:
            return None
        archive_path = self.root / ARCHIVE_DIR / f"events-{archive_events[0]['seq']:06d}-{archive_events[-1]['seq']:06d}.jsonl"
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        archive_path.write_text(
            "".join(json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for event in archive_events),
            encoding="utf-8",
        )
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        self.log_path.write_text(
            "".join(json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for event in remaining),
            encoding="utf-8",
        )
        return archive_path


def replay_without_side_effects(root: Path, forbidden_callback: Callable[[], None] | None = None) -> dict[str, Any]:
    if forbidden_callback is not None:
        # The callback is deliberately not invoked. Golden tests pass a callback that raises.
        pass
    return rebuild_snapshot(root)
