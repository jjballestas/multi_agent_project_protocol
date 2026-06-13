#!/usr/bin/env python3
"""Append-only event log primitives for the N-agent runtime."""

from __future__ import annotations

import hashlib
import hmac
import json
import os
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable


EVENT_SCHEMA_VERSION = "1.0"
TRACE_ID_VERSION = "trace.v1"
UNAUTHENTICATED_EVENT = "security.unauthenticated_event"
LOG_PATH = Path("runtime") / "state" / "events.jsonl"
SNAPSHOT_PATH = Path("runtime") / "state" / "snapshot.json"
ARCHIVE_DIR = Path("runtime") / "state" / "archives"
STATE_DIR = Path("runtime") / "state"


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


def chain_enabled(config: dict[str, Any] | None) -> bool:
    event_state = (config or {}).get("event_state")
    return isinstance(event_state, dict) and event_state.get("chain_enabled") is True


def compute_genesis_prev_hash(config_path: Path = Path("protocol.config.json")) -> str:
    if not config_path.exists():
        raise EventLogError(f"config not found: {config_path}")
    config = json.loads(config_path.read_text(encoding="utf-8-sig"))
    return canonical_hash(config)


def event_without_chain_fields(event: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(event)
    payload.pop("prev_hash", None)
    payload.pop("deduped", None)
    return payload


def compute_event_prev_hash(event: dict[str, Any], prev_hash_of_previous: str) -> str:
    return hashlib.sha256(
        (canonical_json(event_without_chain_fields(event)) + str(prev_hash_of_previous)).encode("utf-8")
    ).hexdigest()


def agent_signatures_enabled(config: dict[str, Any] | None) -> bool:
    event_state = (config or {}).get("event_state")
    return isinstance(event_state, dict) and event_state.get("agent_signatures_enabled") is True


def anchor_enabled(config: dict[str, Any] | None) -> bool:
    event_state = (config or {}).get("event_state")
    return isinstance(event_state, dict) and event_state.get("anchor_enabled") is True


def anchor_config(config: dict[str, Any] | None) -> dict[str, Any]:
    event_state = (config or {}).get("event_state")
    if not isinstance(event_state, dict):
        return {}
    value = event_state.get("anchor_config")
    return value if isinstance(value, dict) else {}


def attestation_signing_payload(subject_digest: str, predicate: dict[str, Any]) -> bytes:
    return (str(subject_digest) + "\n" + canonical_json(predicate)).encode("utf-8")


def event_head_digest(event: dict[str, Any]) -> str:
    return "sha256:" + canonical_hash(event)


def anchor_to_git_remote(head_digest: str, config: dict[str, Any], *, now: str) -> dict[str, Any]:
    remote_url = str(config.get("remote_url") or "").strip()
    if not remote_url:
        raise EventLogError("anchor git-remote backend requires remote_url")
    if "://" in remote_url and not remote_url.startswith("file://"):
        raise EventLogError("external git-remote anchoring requires operator-provided credentials outside the repo")
    remote_path = Path(remote_url[7:] if remote_url.startswith("file://") else remote_url)
    remote_path.mkdir(parents=True, exist_ok=True)
    identity = str(config.get("identity") or "runtime-anchor")
    head_file = remote_path / "HEAD"
    anchors_log = remote_path / "anchors.log"
    line = f"{now} {head_digest} {identity}\n"
    head_file.write_text(head_digest + "\n", encoding="ascii")
    with anchors_log.open("a", encoding="ascii", newline="\n") as handle:
        handle.write(line)
    proof = canonical_hash({"head": head_digest, "identity": identity, "line": line, "backend": "git-remote"})
    return {"backend": "git-remote", "git_timestamp": now, "proof": proof, "remote_ref": str(remote_path)}


def anchor_due(last_anchor_ts: str | None, now: str, interval_seconds: int) -> bool:
    if interval_seconds <= 0 or not last_anchor_ts:
        return True
    try:
        last = datetime.fromisoformat(last_anchor_ts.replace("Z", "+00:00"))
        current = datetime.fromisoformat(now.replace("Z", "+00:00"))
    except ValueError:
        return True
    return (current - last).total_seconds() >= interval_seconds


def observability_config(config: dict[str, Any] | None) -> dict[str, Any]:
    config = config or {}
    observability = config.get("observability")
    if not isinstance(observability, dict):
        observability = (config.get("runtime") or {}).get("observability")
    return observability if isinstance(observability, dict) else {}


def observability_enabled(config: dict[str, Any] | None) -> bool:
    return observability_config(config).get("enabled") is True


def trace_value(*values: Any) -> str:
    for value in values:
        text = str(value or "").strip()
        if text:
            return text
    return "unknown"


def idempotency_attempt_id(idempotency_key: Any) -> str | None:
    parts = [part for part in str(idempotency_key or "").split(":") if part]
    if len(parts) >= 2 and parts[-1].isdigit():
        return parts[-2]
    return None


def deterministic_trace_id(*, run_id: Any, task_id: Any, attempt_id: Any, seq: Any) -> str:
    payload = {
        "version": TRACE_ID_VERSION,
        "run_id": trace_value(run_id),
        "task_id": trace_value(task_id),
        "attempt_id": trace_value(attempt_id),
        "seq": int(seq or 0),
    }
    return "TRACE-" + hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()[:16]


def event_trace_id(event: dict[str, Any]) -> str:
    payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
    idempotency_key = event.get("idempotency_key")
    return deterministic_trace_id(
        run_id=trace_value(payload.get("run_id"), payload.get("turn_id"), "run-unknown"),
        task_id=trace_value(payload.get("task_id"), event.get("aggregate_id"), "task-unknown"),
        attempt_id=trace_value(payload.get("attempt_id"), idempotency_attempt_id(idempotency_key), idempotency_key, "attempt-unknown"),
        seq=event.get("seq"),
    )


def read_protocol_config(root: Path) -> dict[str, Any]:
    path = root / "protocol.config.json"
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8-sig"))


def event_auth_enabled(config: dict[str, Any] | None) -> bool:
    event_auth = (config or {}).get("event_auth")
    return isinstance(event_auth, dict) and event_auth.get("enabled") is True


def agent_auth_config(config: dict[str, Any], actor: str) -> dict[str, Any]:
    event_auth = config.get("event_auth") or {}
    merged: dict[str, Any] = {}
    for agent in ((config.get("agent_registry") or {}).get("agents") or []):
        if isinstance(agent, dict) and str(agent.get("id") or "") == actor and isinstance(agent.get("auth"), dict):
            merged.update(agent["auth"])
            break
    keys = event_auth.get("keys") or {}
    entry = keys.get(actor) if isinstance(keys, dict) else None
    if isinstance(entry, str):
        merged["secret"] = entry
    elif isinstance(entry, dict):
        merged.update(entry)
    for key in ("issuer", "audience", "method"):
        if key in event_auth and key not in merged:
            merged[key] = event_auth[key]
    return merged


def signing_secret(config: dict[str, Any], actor: str) -> str | None:
    auth = agent_auth_config(config, actor)
    for key in ("secret", "hmac_secret", "signing_secret", "key"):
        value = auth.get(key)
        if str(value or "").strip():
            return str(value)
    return None


def signing_key_id(config: dict[str, Any], actor: str) -> str:
    auth = agent_auth_config(config, actor)
    return str(auth.get("key_id") or f"{actor}:local")


def signable_event(event: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(event)
    payload.pop("event_auth", None)
    payload.pop("deduped", None)
    return payload


def event_signature(event: dict[str, Any], secret: str) -> str:
    return hmac.new(secret.encode("utf-8"), canonical_json(signable_event(event)).encode("utf-8"), hashlib.sha256).hexdigest()


def sign_event(event: dict[str, Any], config: dict[str, Any]) -> dict[str, Any]:
    if not event_auth_enabled(config):
        return event
    actor = str(event.get("actor") or "")
    secret = signing_secret(config, actor)
    if not secret:
        raise EventLogError(f"event auth signing key missing for actor: {actor}")
    auth = agent_auth_config(config, actor)
    signed = dict(event)
    signed["event_auth"] = {
        "method": str(auth.get("method") or (config.get("event_auth") or {}).get("method") or "hmac-sha256"),
        "key_id": signing_key_id(config, actor),
        "signature": event_signature(signed, secret),
    }
    if str(auth.get("issuer") or "").strip():
        signed["event_auth"]["issuer"] = str(auth["issuer"])
    if str(auth.get("audience") or "").strip():
        signed["event_auth"]["audience"] = str(auth["audience"])
    return signed


def verify_event_auth(event: dict[str, Any], config: dict[str, Any] | None) -> dict[str, Any]:
    if not event_auth_enabled(config):
        return {"valid": True, "reason": "event_auth_disabled"}
    auth = event.get("event_auth")
    if not isinstance(auth, dict):
        return {"valid": False, "reason": "missing_signature"}
    signature = str(auth.get("signature") or "")
    if not signature:
        return {"valid": False, "reason": "missing_signature"}
    secret = signing_secret(config or {}, str(event.get("actor") or ""))
    if not secret:
        return {"valid": False, "reason": "missing_key"}
    expected = event_signature(event, secret)
    if not hmac.compare_digest(signature, expected):
        return {"valid": False, "reason": "invalid_signature"}
    return {"valid": True, "reason": "valid"}


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
    return sorted(events_in_log_order(root), key=lambda event: int(event.get("seq") or 0))


def events_in_log_order(root: Path) -> list[dict[str, Any]]:
    events: list[dict[str, Any]] = []
    archive_dir = root / ARCHIVE_DIR
    if archive_dir.exists():
        for path in sorted(archive_dir.glob("events-*.jsonl")):
            events.extend(read_jsonl_torn_safe(path))
    events.extend(read_jsonl_torn_safe(root / LOG_PATH))
    return events


def replay_events(
    events: list[dict[str, Any]],
    base_state: dict[str, Any] | None = None,
    config: dict[str, Any] | None = None,
) -> dict[str, Any]:
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
        auth_result = verify_event_auth(event, config)
        if auth_result.get("valid") is not True:
            state["rejections"].append(
                {
                    "seq": event.get("seq"),
                    "aggregate_id": aggregate_id,
                    "event": UNAUTHENTICATED_EVENT,
                    "reason": auth_result.get("reason"),
                    "actor": event.get("actor"),
                }
            )
            state["events_applied"] = int(state["events_applied"]) + 1
            continue
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
        "state": replay_events(events, config=read_protocol_config(root)),
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


def runtime_state_has_content(root: Path) -> bool:
    state_dir = root / STATE_DIR
    return state_dir.exists() and any(path.is_file() for path in state_dir.rglob("*"))


class EventWriter:
    def __init__(self, root: Path):
        self.root = root.resolve()

    @property
    def log_path(self) -> Path:
        return self.root / LOG_PATH

    def events(self) -> list[dict[str, Any]]:
        return all_events(self.root)

    def state(self) -> dict[str, Any]:
        return replay_events(self.events(), config=read_protocol_config(self.root))

    def next_seq(self) -> int:
        events = self.events()
        return (int(events[-1].get("seq") or 0) + 1) if events else 1

    def chain_anchor(self, config: dict[str, Any]) -> str:
        events = self.events()
        if not events:
            return compute_genesis_prev_hash(self.root / "protocol.config.json")
        last = events[-1]
        last_prev = last.get("prev_hash")
        if isinstance(last_prev, str) and last_prev:
            return last_prev
        genesis = {
            "seq": self.next_seq(),
            "event_schema_version": EVENT_SCHEMA_VERSION,
            "type": "chain.genesis",
            "aggregate_id": "eventlog-chain",
            "aggregate_version": 1,
            "actor": "runtime",
            "actor_auth": {"method": "not_enforced_phase2"},
            "idempotency_key": "eventlog-chain:genesis:v1",
            "fencing_token": None,
            "payload": {"reason": "chain_enabled"},
            "applied": False,
            "ts": utc_now(),
            "prev_hash": compute_genesis_prev_hash(self.root / "protocol.config.json"),
        }
        if observability_enabled(config):
            genesis["trace_id"] = event_trace_id(genesis)
        atomic_append_jsonl(self.log_path, sign_event(genesis, config))
        return str(genesis["prev_hash"])

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
        ts: str | None = None,
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
            "ts": str(ts or utc_now()),
        }
        config = read_protocol_config(self.root)
        if chain_enabled(config):
            previous_hash = self.chain_anchor(config)
            event["seq"] = self.next_seq()
        if observability_enabled(config):
            event["trace_id"] = event_trace_id(event)
        if chain_enabled(config):
            event["prev_hash"] = compute_event_prev_hash(event, previous_hash)
        event = sign_event(event, config)
        atomic_append_jsonl(self.log_path, event)
        return event

    def append_agent_attestation(
        self,
        *,
        agent_id: str,
        subject_digest: str,
        subject_reference: str,
        predicate: dict[str, Any],
        signature: dict[str, Any],
        verification_backend: str = "local-ed25519",
        idempotency_key: str | None = None,
        ts: str | None = None,
    ) -> dict[str, Any] | None:
        config = read_protocol_config(self.root)
        if not agent_signatures_enabled(config):
            return None
        return self.append_event(
            event_type="agent.attestation",
            aggregate_id=str(predicate.get("task_id") or predicate.get("reviewed_task") or subject_reference or agent_id),
            actor_id=agent_id,
            idempotency_key=idempotency_key,
            applied=False,
            payload={
                "agent_id": agent_id,
                "subject_digest": subject_digest,
                "subject_reference": subject_reference,
                "predicate": predicate,
                "signature": signature,
                "verification_backend": verification_backend,
            },
            ts=ts,
        )

    def last_anchor_timestamp(self) -> str | None:
        for event in reversed(self.events()):
            if event.get("type") == "chain.anchor":
                payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
                return str(payload.get("timestamp") or event.get("ts") or "")
        return None

    def periodic_anchor_if_due(self, *, now: str | None = None) -> dict[str, Any] | None:
        config = read_protocol_config(self.root)
        if not anchor_enabled(config):
            return None
        cfg = anchor_config(config)
        interval = int(cfg["interval_seconds"]) if "interval_seconds" in cfg else 3600
        timestamp = str(now or utc_now())
        if not anchor_due(self.last_anchor_timestamp(), timestamp, interval):
            return None
        events = self.events()
        if not events:
            return None
        head_event = events[-1]
        head_digest = event_head_digest(head_event)
        backend = str(cfg.get("backend") or "git-remote")
        if backend != "git-remote":
            raise EventLogError(f"unsupported anchor backend: {backend}")
        evidence = anchor_to_git_remote(head_digest, cfg, now=timestamp)
        return self.append_event(
            event_type="chain.anchor",
            aggregate_id="eventlog-chain",
            actor_id="runtime",
            applied=False,
            payload={
                "head_digest": head_digest,
                "head_seq": int(head_event.get("seq") or 0),
                "anchor_backend": backend,
                "anchor_config": {key: value for key, value in cfg.items() if "secret" not in key.lower() and "token" not in key.lower()},
                "anchor_evidence": evidence,
                "timestamp": timestamp,
            },
            ts=timestamp,
        )

    def acquire_claim(
        self,
        *,
        task_id: str,
        owner: str,
        lease_until: str,
        idempotency_key: str,
        claim_id: str | None = None,
    ) -> dict[str, Any]:
        state = self.state()
        fencing = int(state.get("fencing_tokens", {}).get(task_id) or 0) + 1
        payload = {"task_id": task_id, "owner": owner, "lease_until": lease_until}
        if claim_id:
            payload["claim_id"] = claim_id
        return self.append_event(
            event_type="claim.acquired",
            aggregate_id=task_id,
            actor_id=owner,
            idempotency_key=idempotency_key,
            fencing_token=fencing,
            payload=payload,
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
