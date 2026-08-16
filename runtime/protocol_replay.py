#!/usr/bin/env python3
"""Read-only protocol state replay helpers.

B.1 intentionally observes drift only. It does not write hot state and does not
change the apply/orchestrator write path.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
import base64
from copy import deepcopy
from pathlib import Path
from typing import Any, Callable

try:
    from .eventlog import (
        EventWriter,
        all_events,
        attestation_signing_payload,
        anchor_enabled,
        canonical_hash,
        chain_enabled,
        compute_event_prev_hash,
        compute_genesis_prev_hash,
        event_auth_verification_boundaries,
        read_protocol_config,
    )
    from .temp_paths import make_root_temp_dir, remove_root_temp_dir
except ImportError:  # pragma: no cover - direct script execution
    from eventlog import (
        EventWriter,
        all_events,
        attestation_signing_payload,
        anchor_enabled,
        canonical_hash,
        chain_enabled,
        compute_event_prev_hash,
        compute_genesis_prev_hash,
        event_auth_verification_boundaries,
        read_protocol_config,
    )
    from temp_paths import make_root_temp_dir, remove_root_temp_dir


PROTOCOL_STATE_PATHS = {
    "task_index": Path("Area_comun/state/TASK_INDEX.json"),
    "project_state": Path("Area_comun/state/PROJECT_STATE.json"),
    "claims": Path("Area_comun/state/CLAIMS.json"),
}
SLIM_VIEW_PATHS = {
    "task_index_slim": Path("Area_comun/state/TASK_INDEX.slim.json"),
    "project_state_slim": Path("Area_comun/state/PROJECT_STATE.slim.json"),
    "claims_slim": Path("Area_comun/state/CLAIMS.slim.json"),
}
PRUNE_ARCHIVE_PATHS = {
    "task_index": Path("Area_comun/state/TASK_INDEX_ARCHIVE.json"),
    "claims": Path("Area_comun/state/CLAIMS_ARCHIVE.json"),
}
HOT_TASK_STATUSES = {
    "proposed",
    "ready",
    "claimed",
    "in_progress",
    "in_review",
    "changes_requested",
    "qa_pending",
    "qa_failed",
    "architect_review",
    "blocked",
}
TASK_TRANSITION_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_-]*)\s*->\s*([A-Za-z_][A-Za-z0-9_-]*)\s*$")
SNAPSHOT_HASH_RE = re.compile(r"^[0-9a-f]{64}$")
PROTOCOL_GENESIS_TYPES = {"protocol.genesis", "protocol_state.genesis"}
PROTOCOL_SNAPSHOT_SCHEMA_VERSION = "protocol_state_snapshot.v1"
PROTOCOL_SNAPSHOT_DIR = Path("runtime") / "state" / "snapshots"


class ProtocolMaterializationError(RuntimeError):
    pass


class ProtocolSnapshotRefError(ProtocolMaterializationError):
    pass


class ProtocolStateDriftError(RuntimeError):
    pass


class ChainValidationError(RuntimeError):
    pass


class AgentSignatureValidationError(RuntimeError):
    pass


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def event_state_enabled(config: dict[str, Any] | None) -> bool:
    event_state = (config or {}).get("event_state")
    return isinstance(event_state, dict) and event_state.get("enabled") is True


def event_state_materialize_enabled(config: dict[str, Any] | None) -> bool:
    event_state = (config or {}).get("event_state")
    return isinstance(event_state, dict) and event_state.get("materialize") is True


def event_state_enforce_enabled(config: dict[str, Any] | None) -> bool:
    event_state = (config or {}).get("event_state")
    return isinstance(event_state, dict) and event_state.get("enforce") is True


def event_state_authoritative_enabled(config: dict[str, Any] | None) -> bool:
    event_state = (config or {}).get("event_state")
    return isinstance(event_state, dict) and event_state.get("authoritative") is True


def slim_views_enabled(config: dict[str, Any] | None) -> bool:
    event_state = (config or {}).get("event_state")
    return isinstance(event_state, dict) and event_state.get("slim_views_enabled") is True


def event_state_config_error(config: dict[str, Any] | None) -> str | None:
    config = config or {}
    if config.get("adoption_tier") != "runtime":
        return None
    event_state = config.get("event_state")
    if not isinstance(event_state, dict):
        return None

    enabled = event_state.get("enabled") is True
    materialize = event_state.get("materialize") is True
    enforce = event_state.get("enforce") is True
    authoritative = event_state.get("authoritative") is True
    if authoritative and not enforce:
        return (
            "event_state.authoritative=true requires event_state.enforce=true "
            "for adoption_tier=runtime; set event_state.enforce=true or event_state.authoritative=false."
        )
    if enforce and not materialize:
        return (
            "event_state.enforce=true requires event_state.materialize=true "
            "for adoption_tier=runtime; set event_state.materialize=true or event_state.enforce=false."
        )
    if materialize and not enabled:
        return (
            "event_state.materialize=true requires event_state.enabled=true "
            "for adoption_tier=runtime; set event_state.enabled=true or event_state.materialize=false."
        )
    return None


def validate_chain(events: list[dict[str, Any]], config: dict[str, Any] | None, *, root: Path | None = None) -> dict[str, Any]:
    if not chain_enabled(config):
        return {"valid": True, "reason": "chain_disabled", "checked_events": 0}
    ordered = list(events)
    if not ordered:
        return {"valid": True, "reason": "no_events", "checked_events": 0}
    config_path = (root.resolve() / "protocol.config.json") if root is not None else Path("protocol.config.json")
    genesis_hash = compute_genesis_prev_hash(config_path)
    start_index = 0
    previous_seq: int | None = None
    previous_hash = genesis_hash

    for index, event in enumerate(ordered):
        if event.get("type") == "chain.genesis":
            actual = str(event.get("prev_hash") or "")
            if actual != genesis_hash:
                return {"valid": False, "reason": "genesis mismatch", "seq": event.get("seq")}
            start_index = index + 1
            previous_seq = int(event.get("seq") or 0)
            previous_hash = actual
            break
    else:
        if any("prev_hash" in event for event in ordered):
            first = ordered[0]
            actual = str(first.get("prev_hash") or "")
            if actual != compute_event_prev_hash(first, genesis_hash):
                return {"valid": False, "reason": "chain.genesis_missing", "seq": first.get("seq")}
            previous_hash = actual
            previous_seq = int(first.get("seq") or 0)
            start_index = 1
        else:
            return {"valid": False, "reason": "chain.genesis_missing", "seq": ordered[0].get("seq")}

    checked = 0
    for event in ordered[start_index:]:
        seq = int(event.get("seq") or 0)
        if previous_seq is not None:
            expected_seq = previous_seq + 1
            if seq != expected_seq:
                if event.get("type") == "chain.archive_boundary" and seq > expected_seq:
                    pass
                elif seq < expected_seq:
                    return {"valid": False, "reason": f"seq out of order at seq {seq}: expected {expected_seq}", "seq": seq}
                else:
                    return {"valid": False, "reason": f"gap at seq {seq}: expected {expected_seq}", "seq": seq}
        actual = str(event.get("prev_hash") or "")
        if not actual:
            return {"valid": False, "reason": f"missing prev_hash at seq {seq}", "seq": seq}
        expected = compute_event_prev_hash(event, previous_hash)
        if actual != expected:
            return {"valid": False, "reason": f"corruption at seq {seq}: hash mismatch", "seq": seq}
        previous_hash = actual
        previous_seq = seq
        checked += 1
    return {"valid": True, "reason": "chain valid", "checked_events": checked, "head": previous_hash}


def agent_signatures_enabled(config: dict[str, Any] | None) -> bool:
    event_state = (config or {}).get("event_state")
    return isinstance(event_state, dict) and event_state.get("agent_signatures_enabled") is True


def signature_config(config: dict[str, Any] | None) -> dict[str, Any]:
    event_state = (config or {}).get("event_state")
    if not isinstance(event_state, dict):
        return {}
    nested = event_state.get("signature_config")
    if isinstance(nested, dict):
        return nested
    return {}


def agent_registry_from_config(config: dict[str, Any] | None) -> dict[str, Any]:
    registry = (config or {}).get("agent_registry")
    if isinstance(registry, dict) and isinstance(registry.get("agents"), list):
        return registry
    roles = (config or {}).get("agent_roles") if isinstance((config or {}).get("agent_roles"), dict) else {}
    agents = []
    if roles:
        role_caps = {"architect": ["orchestrator", "reviewer"], "implementer": ["implementer"], "human_owner": ["human"]}
        for role, agent_id in sorted(roles.items()):
            if str(agent_id or "").strip():
                agents.append({"id": str(agent_id), "enabled": True, "capabilities": role_caps.get(role, [])})
    return {"enabled": True, "agents": agents}


def attestation_payload(event: dict[str, Any]) -> dict[str, Any]:
    payload = event.get("payload")
    if isinstance(payload, dict) and payload.get("agent_id"):
        return payload
    return event


def agents_by_id(registry: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {
        str(agent.get("id")): agent
        for agent in registry.get("agents") or []
        if isinstance(agent, dict) and str(agent.get("id") or "").strip()
    }


def public_key_for_attestation(agent: dict[str, Any], signature: dict[str, Any], config: dict[str, Any]) -> str | None:
    keyid = str(signature.get("keyid") or "")
    public_keys = config.get("public_keys")
    if isinstance(public_keys, dict) and keyid in public_keys:
        return str(public_keys[keyid])
    agent_public_keys = config.get("agent_public_keys")
    agent_id = str(agent.get("id") or "")
    if isinstance(agent_public_keys, dict) and agent_id in agent_public_keys:
        return str(agent_public_keys[agent_id])
    for container_key in ("signature", "auth"):
        container = agent.get(container_key)
        if isinstance(container, dict):
            if keyid and str(container.get("keyid") or "") not in {"", keyid}:
                continue
            for value_key in ("public_key", "public_key_pem", "ed25519_public_key"):
                if str(container.get(value_key) or "").strip():
                    return str(container[value_key])
    return None


def verify_ed25519_signature(public_key_text: str, signature_b64: str, message: bytes) -> tuple[bool, str]:
    try:
        from cryptography.exceptions import InvalidSignature  # type: ignore
        from cryptography.hazmat.primitives import serialization  # type: ignore
        from cryptography.hazmat.primitives.asymmetric import ed25519  # type: ignore
    except ImportError:
        return False, "backend_unavailable"
    try:
        raw_signature = base64.b64decode(signature_b64, validate=True)
        key_text = public_key_text.strip()
        if "BEGIN PUBLIC KEY" in key_text:
            key = serialization.load_pem_public_key(key_text.encode("ascii"))
        else:
            key = ed25519.Ed25519PublicKey.from_public_bytes(base64.b64decode(key_text, validate=True))
        if not isinstance(key, ed25519.Ed25519PublicKey):
            return False, "unsupported_public_key"
        key.verify(raw_signature, message)
        return True, "valid"
    except InvalidSignature:
        return False, "signature_invalid"
    except Exception:
        return False, "signature_invalid"


def validate_attestation_schema(payload: dict[str, Any]) -> str | None:
    for key in ("agent_id", "subject_digest", "predicate", "signature"):
        if key not in payload:
            return f"missing {key}"
    predicate = payload.get("predicate")
    if not isinstance(predicate, dict):
        return "predicate_not_object"
    signature = payload.get("signature")
    if not isinstance(signature, dict):
        return "signature_not_object"
    for key in ("agent_id", "role", "timestamp_claimed"):
        if not str(predicate.get(key) or "").strip():
            return f"missing predicate field: {key}"
    if not (str(predicate.get("task_id") or "").strip() or str(predicate.get("reviewed_task") or "").strip()):
        return "missing predicate field: task_id"
    for key in ("keyid", "sig", "algorithm"):
        if not str(signature.get(key) or "").strip():
            return f"missing signature field: {key}"
    return None


def validate_agent_signatures(events: list[dict[str, Any]], config: dict[str, Any] | None) -> dict[str, Any]:
    if not agent_signatures_enabled(config):
        return {"valid": True, "reason": "agent_signatures_disabled", "findings": [], "checked": 0}
    registry = agent_registry_from_config(config)
    agents = agents_by_id(registry)
    sig_config = signature_config(config)
    findings: list[dict[str, Any]] = []
    checked = 0
    for event in events:
        if event.get("type") != "agent.attestation":
            continue
        checked += 1
        payload = attestation_payload(event)
        seq = event.get("seq")
        schema_error = validate_attestation_schema(payload)
        agent_id = str(payload.get("agent_id") or "")
        if schema_error:
            findings.append({"seq": seq, "agent_id": agent_id, "error": schema_error})
            continue
        agent = agents.get(agent_id)
        if agent is None:
            findings.append({"seq": seq, "agent_id": agent_id, "error": "unknown_agent"})
            continue
        signature = payload["signature"]
        algorithm = str(signature.get("algorithm") or "").lower()
        backend = str(payload.get("verification_backend") or sig_config.get("backend") or "local-ed25519")
        if algorithm != "ed25519" or backend not in {"local-ed25519", "ed25519"}:
            findings.append({"seq": seq, "agent_id": agent_id, "error": "unsupported_signature_backend"})
            continue
        public_key = public_key_for_attestation(agent, signature, sig_config)
        if not public_key:
            findings.append({"seq": seq, "agent_id": agent_id, "error": "public_key_missing"})
            continue
        ok, reason = verify_ed25519_signature(
            public_key,
            str(signature.get("sig") or ""),
            attestation_signing_payload(str(payload["subject_digest"]), payload["predicate"]),
        )
        if not ok:
            findings.append({"seq": seq, "agent_id": agent_id, "error": reason})
    return {"valid": not findings, "reason": "agent signatures valid" if not findings else "agent signatures invalid", "findings": findings, "checked": checked}


def anchor_payload(event: dict[str, Any]) -> dict[str, Any]:
    payload = event.get("payload")
    if isinstance(payload, dict) and payload.get("head_digest"):
        return payload
    return event


def validate_anchor_schema(payload: dict[str, Any]) -> str | None:
    for key in ("head_digest", "head_seq", "anchor_backend", "anchor_evidence"):
        if key not in payload:
            return f"missing {key}"
    if not str(payload.get("head_digest") or "").startswith("sha256:"):
        return "invalid head_digest"
    try:
        int(payload.get("head_seq"))
    except (TypeError, ValueError):
        return "invalid head_seq"
    if not isinstance(payload.get("anchor_evidence"), dict):
        return "anchor_evidence_not_object"
    return None


def verify_anchor_monotonicity(events: list[dict[str, Any]], config: dict[str, Any] | None) -> dict[str, Any]:
    if not anchor_enabled(config):
        return {"valid": True, "reason": "anchor_disabled", "findings": [], "checked": 0}
    findings: list[dict[str, Any]] = []
    checked = 0
    last_event_seq = -1
    last_head_seq = -1
    seen_digests: set[str] = set()
    for event in events:
        if event.get("type") != "chain.anchor":
            continue
        checked += 1
        payload = anchor_payload(event)
        seq = int(event.get("seq") or 0)
        schema_error = validate_anchor_schema(payload)
        if schema_error:
            findings.append({"seq": seq, "error": schema_error})
            continue
        head_seq = int(payload.get("head_seq") or 0)
        digest = str(payload.get("head_digest") or "")
        if seq <= last_event_seq or head_seq <= last_head_seq:
            findings.append({"seq": seq, "error": "anchor_reordered"})
        if digest in seen_digests:
            findings.append({"seq": seq, "error": "anchor_duplicate"})
        last_event_seq = seq
        last_head_seq = head_seq
        seen_digests.add(digest)
    return {"valid": not findings, "reason": "anchors valid" if not findings else "anchors invalid", "findings": findings, "checked": checked}


def protocol_materialization_enabled(config: dict[str, Any] | None) -> bool:
    config = config or {}
    return event_state_enabled(config) and event_state_materialize_enabled(config) and config.get("adoption_tier") == "runtime"


def protocol_state_enforcement_enabled(config: dict[str, Any] | None) -> bool:
    config = config or {}
    return event_state_enabled(config) and event_state_enforce_enabled(config) and config.get("adoption_tier") == "runtime"


def protocol_authoritative_enabled(config: dict[str, Any] | None) -> bool:
    config = config or {}
    return (
        protocol_state_enforcement_enabled(config)
        and event_state_materialize_enabled(config)
        and event_state_authoritative_enabled(config)
    )


def protocol_materialization_disabled_reason(config: dict[str, Any] | None) -> str:
    config = config or {}
    if not event_state_enabled(config):
        return "event_state.enabled is false"
    if not event_state_materialize_enabled(config):
        return "event_state.materialize is false"
    if config.get("adoption_tier") != "runtime":
        return "adoption_tier is not runtime"
    return "enabled"


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


def is_hot_status(status: Any) -> bool:
    return str(status or "").strip() in HOT_TASK_STATUSES


def compact_task(task: dict[str, Any]) -> dict[str, Any]:
    compact = {
        key: task.get(key)
        for key in ("id", "status", "owner", "phase", "priority", "title")
        if task.get(key) is not None
    }
    blocked = task.get("blocked_by_questions")
    if isinstance(blocked, list) and blocked:
        compact["blocked_by_questions"] = blocked
    return compact


def compact_active_task(task: dict[str, Any]) -> dict[str, Any]:
    return {
        key: task.get(key)
        for key in ("id", "status", "owner", "title")
        if task.get(key) is not None
    }


def recent_window(config: dict[str, Any] | None, field: str) -> int:
    maintenance = (config or {}).get("maintenance")
    if not isinstance(maintenance, dict):
        return 8
    keys = [f"recent_{field}", "recent_next_actions"]
    for key in keys:
        try:
            value = int(maintenance.get(key))
        except (TypeError, ValueError):
            continue
        if value >= 0:
            return value
    return 8


def tail_strings(values: Any, limit: int) -> list[str]:
    if not isinstance(values, list):
        return []
    strings = [str(item) for item in values]
    if limit <= 0:
        return []
    return strings[-limit:]


def build_slim_views(snapshot_or_state: dict[str, Any], config: dict[str, Any] | None) -> dict[str, dict[str, Any]]:
    state = snapshot_or_state.get("state") if isinstance(snapshot_or_state.get("state"), dict) else snapshot_or_state
    canonical = canonicalize_protocol_state(state)
    task_index = canonical["task_index"]
    project_state = canonical["project_state"]
    claims = canonical["claims"]

    task_entries = [
        compact_task(task)
        for task in task_index.get("tasks") or []
        if isinstance(task, dict) and is_hot_status(task.get("status"))
    ]
    active_entries = [
        compact_active_task(task)
        for task in project_state.get("active_tasks") or []
        if isinstance(task, dict) and is_hot_status(task.get("status"))
    ]
    claim_entries = [
        {
            key: claim.get(key)
            for key in ("claim_id", "task_id", "owner", "scope")
            if claim.get(key) is not None
        }
        for claim in claims.get("claims") or []
        if isinstance(claim, dict) and str(claim.get("status") or "") == "active"
    ]

    return {
        SLIM_VIEW_PATHS["task_index_slim"].as_posix(): {
            "schema_version": "1.0",
            "view": "task_index.slim",
            "tasks": sort_by_key(task_entries, "id"),
        },
        SLIM_VIEW_PATHS["project_state_slim"].as_posix(): {
            "view": "project_state.slim",
            "status": project_state.get("status"),
            "active_tasks": sort_by_key(active_entries, "id"),
            "next_actions": tail_strings(project_state.get("next_actions"), recent_window(config, "next_actions")),
            "risks": tail_strings(project_state.get("risks"), recent_window(config, "risks")),
            "open_questions": tail_strings(project_state.get("open_questions"), recent_window(config, "open_questions")),
        },
        SLIM_VIEW_PATHS["claims_slim"].as_posix(): {
            "schema_version": "1.0",
            "view": "claims.slim",
            "claims": sort_by_key(claim_entries, "claim_id"),
        },
    }


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


def snapshot_document(snapshot: dict[str, Any]) -> dict[str, Any]:
    return {"schema_version": PROTOCOL_SNAPSHOT_SCHEMA_VERSION, "snapshot": snapshot}


def snapshot_ref_path(root: Path, snapshot_hash: str) -> Path:
    return root.resolve() / PROTOCOL_SNAPSHOT_DIR / f"{snapshot_hash}.json"


def write_snapshot_ref(root: Path, snapshot: dict[str, Any]) -> dict[str, str]:
    document = snapshot_document(snapshot)
    snapshot_hash = canonical_hash(document)
    path = snapshot_ref_path(root, snapshot_hash)
    write_text_ascii(path, canonical_json_text(document))
    return {"hash": snapshot_hash, "schema_version": PROTOCOL_SNAPSHOT_SCHEMA_VERSION}


def load_snapshot_ref(root: Path | None, snapshot_ref: dict[str, Any]) -> dict[str, Any]:
    if root is None:
        raise ProtocolSnapshotRefError("snapshot_ref replay requires an instance root")
    expected_hash = str(snapshot_ref.get("hash") or "").strip()
    if not expected_hash:
        raise ProtocolSnapshotRefError("snapshot_ref missing hash")
    if not SNAPSHOT_HASH_RE.match(expected_hash):
        raise ProtocolSnapshotRefError("snapshot_ref hash is not a canonical sha256 hex digest")
    path = snapshot_ref_path(root, expected_hash)
    if not path.exists():
        raise ProtocolSnapshotRefError(f"snapshot_ref missing content-addressed snapshot: {path.relative_to(root).as_posix()}")
    document = read_json(path)
    actual_hash = canonical_hash(document)
    if actual_hash != expected_hash:
        raise ProtocolSnapshotRefError(f"snapshot_ref hash mismatch: expected {expected_hash}, found {actual_hash}")
    if document.get("schema_version") != snapshot_ref.get("schema_version"):
        raise ProtocolSnapshotRefError(
            "snapshot_ref schema_version mismatch: "
            f"expected {snapshot_ref.get('schema_version')}, found {document.get('schema_version')}"
        )
    snapshot = document.get("snapshot")
    if not isinstance(snapshot, dict) or not isinstance(snapshot.get("state"), dict):
        raise ProtocolSnapshotRefError("snapshot_ref document has no protocol state snapshot")
    return snapshot


def current_git_commit(root: Path) -> str:
    completed = subprocess.run(["git", "rev-parse", "HEAD"], cwd=root.resolve(), text=True, capture_output=True, check=False)
    if completed.returncode != 0:
        return "unknown"
    return completed.stdout.strip() or "unknown"


def write_genesis(
    root: Path,
    *,
    actor_id: str = "runtime",
    idempotency_key: str = "protocol-state:genesis:v1",
) -> dict[str, Any]:
    root = root.resolve()
    snapshot = build_genesis_snapshot(root)
    writer = EventWriter(root)
    event = writer.append_event(
        event_type="protocol.genesis",
        aggregate_id="protocol-state",
        actor_id=actor_id,
        idempotency_key=idempotency_key,
        payload={"state": snapshot["state"], "canonical_hash": snapshot["canonical_hash"]},
    )
    writer.write_snapshot()
    return {"event": event, "snapshot": snapshot}


def write_genesis_reference(
    root: Path,
    *,
    actor_id: str,
    timestamp: str,
    commit: str | None = None,
    idempotency_key: str = "protocol-state:genesis-ref:v1",
) -> dict[str, Any]:
    if not str(actor_id or "").strip():
        raise ProtocolSnapshotRefError("actor_id is required for genesis snapshot_ref")
    if not str(timestamp or "").strip():
        raise ProtocolSnapshotRefError("timestamp is required for deterministic genesis snapshot_ref")
    root = root.resolve()
    writer = EventWriter(root)
    if idempotency_key:
        existing_seq = writer.state().get("idempotency_keys", {}).get(idempotency_key)
        if existing_seq:
            for existing in writer.events():
                if int(existing.get("seq") or 0) != int(existing_seq):
                    continue
                event = dict(existing)
                event["deduped"] = True
                existing_payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
                existing_ref = existing_payload.get("snapshot_ref") if isinstance(existing_payload, dict) else None
                if not isinstance(existing_ref, dict):
                    raise ProtocolSnapshotRefError("deduped genesis event has no snapshot_ref")
                snapshot = load_snapshot_ref(root, existing_ref)
                return {
                    "event": event,
                    "snapshot": snapshot,
                    "snapshot_ref": dict(existing_ref),
                    "snapshot_path": snapshot_ref_path(root, str(existing_ref.get("hash") or "")),
                }
    snapshot = build_genesis_snapshot(root)
    snapshot_ref = write_snapshot_ref(root, snapshot)
    snapshot_ref.update(
        {
            "commit": str(commit or current_git_commit(root)),
            "actor": str(actor_id),
            "timestamp": str(timestamp),
        }
    )
    event = writer.append_event(
        event_type="protocol.genesis",
        aggregate_id="protocol-state",
        actor_id=actor_id,
        idempotency_key=idempotency_key,
        payload={"snapshot_ref": snapshot_ref},
        ts=timestamp,
    )
    writer.write_snapshot()
    return {"event": event, "snapshot": snapshot, "snapshot_ref": snapshot_ref, "snapshot_path": snapshot_ref_path(root, snapshot_ref["hash"])}


def prepare_authoritative_migration(
    root: Path,
    *,
    actor_id: str,
    timestamp: str,
    commit: str | None = None,
) -> dict[str, Any]:
    result = write_genesis_reference(root, actor_id=actor_id, timestamp=timestamp, commit=commit)
    result["authoritative_ready"] = True
    result["activation_note"] = "Keep event_state.authoritative/enforce false until the operator approves activation."
    return result


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


def apply_project_narrative_event(state: dict[str, Any], payload: dict[str, Any]) -> None:
    project = state.setdefault("project_state", {})
    version = payload.get("version")
    if isinstance(version, str) and version:
        project["version"] = version
    set_values = payload.get("set") if isinstance(payload.get("set"), dict) else {}
    append_values = payload.get("append") if isinstance(payload.get("append"), dict) else {}
    for field, values in sorted(set_values.items()):
        if isinstance(values, list):
            project[field] = [str(item) for item in values]
    for field, values in sorted(append_values.items()):
        if not isinstance(values, list):
            continue
        current = project.setdefault(field, [])
        if not isinstance(current, list):
            current = []
            project[field] = current
        for item in values:
            text = str(item)
            if text not in current:
                current.append(text)


def apply_protocol_prune_event(state: dict[str, Any], payload: dict[str, Any]) -> None:
    task_ids = {str(item) for item in payload.get("task_ids") or [] if str(item)}
    active_task_ids = {str(item) for item in payload.get("active_task_ids") or [] if str(item)}
    claim_ids = {str(item) for item in payload.get("claim_ids") or [] if str(item)}
    if task_ids:
        tasks = state.setdefault("task_index", {}).setdefault("tasks", [])
        tasks[:] = [item for item in tasks if not (isinstance(item, dict) and str(item.get("id") or "") in task_ids)]
    if active_task_ids:
        active = state.setdefault("project_state", {}).setdefault("active_tasks", [])
        active[:] = [item for item in active if not (isinstance(item, dict) and str(item.get("id") or "") in active_task_ids)]
    if claim_ids:
        claims = state.setdefault("claims", {}).setdefault("claims", [])
        claims[:] = [item for item in claims if not (isinstance(item, dict) and str(item.get("claim_id") or "") in claim_ids)]


def apply_intent_event(state: dict[str, Any], event: dict[str, Any], payload: dict[str, Any]) -> None:
    task = payload.get("task")
    if isinstance(task, dict):
        upsert_task(state, task)
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
        task_upsert = transitions.get("task_upsert")
        if isinstance(task_upsert, dict):
            task_payload = task_upsert.get("task")
            if isinstance(task_payload, dict):
                upsert_task(state, task_payload)
        for claim_transition in transitions.get("claims") or []:
            if isinstance(claim_transition, dict):
                op = claim_transition.get("op")
                claim_payload = dict(claim_transition)
                if op == "acquire":
                    claim = claim_payload.get("claim")
                    if isinstance(claim, dict):
                        apply_claim_event(state, {"type": "claim.upserted"}, {"claim": claim})
                    else:
                        claim_payload.setdefault("status", "active")
                        apply_claim_event(state, {"type": "claim.upserted", "actor": event.get("actor")}, claim_payload)
                elif op == "block":
                    claim_payload.setdefault("status", "blocked")
                    apply_claim_event(state, {"type": "claim.blocked"}, claim_payload)
                else:
                    claim_payload.setdefault("status", "released")
                    apply_claim_event(state, {"type": "claim.released"}, claim_payload)
        decision_transition = transitions.get("decision")
        if isinstance(decision_transition, dict):
            apply_decision_event(state, decision_transition)
        narrative_transition = transitions.get("project_narrative")
        if isinstance(narrative_transition, dict):
            apply_project_narrative_event(state, narrative_transition)
        prune_transition = transitions.get("protocol_prune")
        if isinstance(prune_transition, dict):
            apply_protocol_prune_event(state, prune_transition)


def replay_protocol_state(
    events: list[dict[str, Any]],
    base_state: dict[str, Any] | None = None,
    forbidden_callback: Callable[[], None] | None = None,
    root: Path | None = None,
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
            snapshot_ref = payload.get("snapshot_ref")
            if isinstance(snapshot_ref, dict):
                genesis_snapshot = load_snapshot_ref(root, snapshot_ref)
                genesis = genesis_snapshot.get("state")
            else:
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
    return replay_protocol_state(all_events(root), root=root)


def exception_recorded_events(root: Path, task_id: str | None = None) -> list[dict[str, Any]]:
    """Return exception.recorded events, optionally filtered by task_id."""
    selected: list[dict[str, Any]] = []
    task_filter = str(task_id or "").strip()
    for event in all_events(root):
        if event.get("type") != "exception.recorded":
            continue
        payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
        if task_filter and str(payload.get("task_id") or "") != task_filter:
            continue
        selected.append(event)
    return selected


def canonical_json_text(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=4, ensure_ascii=True, sort_keys=True) + "\n"


def write_text_ascii(path: Path, text: str) -> None:
    text.encode("ascii")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="ascii", newline="\n") as handle:
        handle.write(text)


def materialize_to_disk(
    root: Path,
    snapshot_or_state: dict[str, Any],
    *,
    fail_after_writes: int | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    config = read_protocol_config(root)
    materialized = materialize_protocol_state(snapshot_or_state)
    if slim_views_enabled(config):
        materialized.update(build_slim_views(snapshot_or_state, config))
    ordered_paths = sorted(materialized)
    # Stage on the SAME filesystem as the targets so the atomic os.replace() below is an
    # intra-drive rename. Using the OS default temp dir breaks on Windows when temp and the
    # repo live on different drives (os.replace raises WinError 17 across drives).
    # Avoid tempfile.TemporaryDirectory(): on Python 3.12+ for Windows it can create 0o700
    # directories whose ACLs are too restrictive for unelevated sandbox tokens, and replace()
    # carries those file ACLs into the hot state. A normal repo-local mkdir inherits repo ACLs.
    temp_root = make_root_temp_dir(root, ".protocol-state-materialize-")
    try:
        staged_root = temp_root / "staged"
        backup_root = temp_root / "backup"
        backups: dict[str, Path | None] = {}

        for relative in ordered_paths:
            write_text_ascii(staged_root / relative, canonical_json_text(materialized[relative]))

        for relative in ordered_paths:
            target = root / relative
            if target.exists():
                backup = backup_root / relative
                backup.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(target, backup)
                backups[relative] = backup
            else:
                backups[relative] = None

        try:
            for index, relative in enumerate(ordered_paths, start=1):
                target = root / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                (staged_root / relative).replace(target)
                if fail_after_writes is not None and index >= fail_after_writes:
                    raise ProtocolMaterializationError("simulated materialization failure")
        except Exception:
            for relative in ordered_paths:
                target = root / relative
                backup = backups.get(relative)
                if backup is None:
                    if target.exists():
                        target.unlink()
                elif backup.exists():
                    target.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(backup, target)
            raise
    finally:
        remove_root_temp_dir(temp_root)

    return {
        "materialized": True,
        "paths": ordered_paths,
        "up_to_seq": int(snapshot_or_state.get("up_to_seq") or 0),
        "canonical_hash": canonical_hash(materialized),
    }


def has_protocol_genesis(events: list[dict[str, Any]]) -> bool:
    return any(event.get("type") in PROTOCOL_GENESIS_TYPES and event.get("applied", True) is True for event in events)


def materialize_from_event_log_if_enabled(root: Path) -> dict[str, Any]:
    root = root.resolve()
    config = read_protocol_config(root)
    if not protocol_materialization_enabled(config):
        return {"materialized": False, "reason": protocol_materialization_disabled_reason(config), "paths": []}
    events = all_events(root)
    if not has_protocol_genesis(events):
        raise ProtocolMaterializationError("protocol genesis event missing; run write_genesis(root) before enabling event_state.materialize")
    snapshot = replay_protocol_state(events, root=root)
    return materialize_to_disk(root, snapshot)


def drift_paths(drift: dict[str, Any]) -> str:
    return ", ".join(str(entry.get("path") or "<unknown>") for entry in drift.get("entries") or [])


def enforce_protocol_state_drift(root: Path) -> dict[str, Any]:
    root = root.resolve()
    config = read_protocol_config(root)
    if not protocol_state_enforcement_enabled(config):
        return {"enforced": False, "reason": "event_state.enforce is false or tier is not runtime"}
    drift = protocol_state_drift(root)
    if drift.get("has_drift"):
        paths = drift_paths(drift)
        raise ProtocolStateDriftError(
            "runtime protocol state drift detected under event_state.enforce: "
            f"{paths}. Reconcile by re-materializing from replay(log) or writing a fresh genesis."
        )
    return {"enforced": True, "has_drift": False, "up_to_seq": drift.get("up_to_seq"), "paths": []}


def drift_entries(hot: dict[str, Any], materialized: dict[str, Any]) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for path in sorted(set(hot) | set(materialized)):
        hot_hash = canonical_hash(hot.get(path) or {})
        replay_hash = canonical_hash(materialized.get(path) or {})
        if hot_hash != replay_hash:
            entries.append({"path": path, "hot_hash": hot_hash, "replay_hash": replay_hash})
    return entries


def expected_prune_archives(root: Path, events: list[dict[str, Any]]) -> dict[str, Any]:
    """Derive every row named by a prune event from the signed pre-prune state."""
    task_rows: dict[str, dict[str, Any]] = {}
    claim_rows: dict[str, dict[str, Any]] = {}
    ordered = sorted(events, key=lambda item: int(item.get("seq") or 0))
    for index, event in enumerate(ordered):
        if event.get("applied", True) is False or event.get("type") != "intent.applied":
            continue
        payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
        transitions = payload.get("transitions") if isinstance(payload.get("transitions"), dict) else {}
        prune = transitions.get("protocol_prune")
        if not isinstance(prune, dict):
            continue
        before = replay_protocol_state(ordered[:index], root=root)
        state = before.get("state") if isinstance(before.get("state"), dict) else {}
        tasks = state.get("task_index", {}).get("tasks", [])
        claims = state.get("claims", {}).get("claims", [])
        wanted_tasks = {str(item) for item in prune.get("task_ids") or []}
        wanted_claims = {str(item) for item in prune.get("claim_ids") or []}
        task_rows.update({str(row.get("id")): deepcopy(row) for row in tasks if isinstance(row, dict) and str(row.get("id")) in wanted_tasks})
        claim_rows.update({str(row.get("claim_id")): deepcopy(row) for row in claims if isinstance(row, dict) and str(row.get("claim_id")) in wanted_claims})
    return {
        PRUNE_ARCHIVE_PATHS["task_index"].as_posix(): {"tasks": [task_rows[key] for key in sorted(task_rows)]},
        PRUNE_ARCHIVE_PATHS["claims"].as_posix(): {"claims": [claim_rows[key] for key in sorted(claim_rows)]},
    }


def prune_archive_drift(root: Path, events: list[dict[str, Any]]) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    for relative, expected_doc in expected_prune_archives(root, events).items():
        field = "tasks" if "TASK_INDEX" in relative else "claims"
        key = "id" if field == "tasks" else "claim_id"
        actual_doc = read_json(root / relative) if (root / relative).exists() else {}
        actual_by_id = {str(row.get(key)): row for row in actual_doc.get(field, []) if isinstance(row, dict)}
        expected_by_id = {str(row.get(key)): row for row in expected_doc[field]}
        projected = {item_id: actual_by_id.get(item_id) for item_id in sorted(expected_by_id)}
        if projected != expected_by_id:
            entries.append({"path": relative, "hot_hash": canonical_hash(projected), "replay_hash": canonical_hash(expected_by_id)})
    return entries


def slim_view_drift(root: Path) -> dict[str, Any]:
    root = root.resolve()
    config = read_protocol_config(root)
    if not slim_views_enabled(config):
        return {
            "enabled": False,
            "has_drift": False,
            "up_to_seq": None,
            "entries": [],
        }
    replay_snapshot = current_protocol_snapshot(root)
    expected = build_slim_views(replay_snapshot, config)
    hot: dict[str, Any] = {}
    for relative in sorted(expected):
        path = root / relative
        hot[relative] = read_json(path) if path.exists() else {}
    entries = drift_entries(hot, expected)
    return {
        "enabled": True,
        "has_drift": bool(entries),
        "up_to_seq": replay_snapshot["up_to_seq"],
        "entries": entries,
        "hot_hash": canonical_hash(hot),
        "replay_hash": canonical_hash(expected),
    }


def protocol_state_drift(root: Path) -> dict[str, Any]:
    root = root.resolve()
    config = read_protocol_config(root)
    hot_snapshot = build_genesis_snapshot(root)
    events = all_events(root)
    replay_snapshot = replay_protocol_state(events, root=root)
    hot = materialize_protocol_state(hot_snapshot)
    materialized = materialize_protocol_state(replay_snapshot)
    entries = drift_entries(hot, materialized)
    entries.extend(prune_archive_drift(root, events))
    if slim_views_enabled(config):
        entries.extend(slim_view_drift(root).get("entries") or [])
    return {
        "enabled": event_state_enabled(config),
        "enforced": protocol_state_enforcement_enabled(config),
        "authoritative": protocol_authoritative_enabled(config),
        "has_drift": bool(entries),
        "up_to_seq": replay_snapshot["up_to_seq"],
        "entries": entries,
        "hot_hash": canonical_hash(hot),
        "replay_hash": canonical_hash(materialized),
        "event_auth_boundaries": event_auth_verification_boundaries(events, config, root=root),
    }


def _drift_exit_code(drift: dict[str, Any]) -> int:
    """Return the process verdict for the drift gate."""
    return 1 if drift.get("has_drift") is not False else 0


def main(argv: list[str] | None = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(description="Replay and verify runtime protocol state.")
    parser.add_argument("--check-drift", action="store_true", help="fail when canonical state differs from signed replay")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="protocol instance root (default: current directory)")
    args = parser.parse_args(argv)
    if not args.check_drift:
        parser.error("--check-drift is required")
    drift = protocol_state_drift(args.root)
    verdict = "CLEAN" if drift.get("has_drift") is False else "DRIFT"
    print(f"PROTOCOL_STATE_DRIFT verdict={verdict} up_to_seq={drift.get('up_to_seq')}")
    boundaries = drift.get("event_auth_boundaries") or []
    boundary_key_ids = sorted({str(item.get("key_id") or "") for item in boundaries if isinstance(item, dict)})
    print(f"EVENT_AUTH_BOUNDARIES count={len(boundaries)} key_ids={boundary_key_ids}")
    for entry in drift.get("entries") or []:
        print(f"DRIFT path={entry.get('path')}")
    return _drift_exit_code(drift)


if __name__ == "__main__":
    raise SystemExit(main())
