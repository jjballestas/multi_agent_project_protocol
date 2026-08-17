#!/usr/bin/env python3
"""Append-only event log primitives for the N-agent runtime."""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import re
import sys
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Iterator


EVENT_SCHEMA_VERSION = "1.0"
TRACE_ID_VERSION = "trace.v1"
UNAUTHENTICATED_EVENT = "security.unauthenticated_event"
LOG_PATH = Path("runtime") / "state" / "events.jsonl"
SNAPSHOT_PATH = Path("runtime") / "state" / "snapshot.json"
LEDGER_LOCK_PATH = Path("runtime") / "state" / ".ledger.lock"
ARCHIVE_DIR = Path("runtime") / "state" / "archives"
STATE_DIR = Path("runtime") / "state"
SECRET_DIRS = {"secrets", ".protocol-secrets"}
# DECISION-0046: distinguish 'verification unavailable here' (no secret material in this
# checkout -> environment, NOT a security finding) from real tamper. UNVERIFIABLE reasons must
# NOT mutate the materialized state, so the canonical state hash is secret-independent.
EVENT_AUTH_UNVERIFIABLE_REASONS = {"unresolved_key", "missing_key", "key_unavailable"}
EVENT_AUTH_TAMPER_REASONS = {"invalid_signature", "missing_signature"}
EVENT_AUTH_ROTATION_DECLARATION = "event_auth.key_rotation_declared"
EVENT_AUTH_REGISTRY_ANCHOR = "event_auth.registry_anchor"
EVENT_AUTH_KEY_REGISTRY_PATH = Path("Area_comun") / "protocol" / "EVENT_AUTH_KEY_REGISTRY.json"
ACTOR_AUTH_TAMPER_REASONS = {
    "invalid_signature",
    "keyid_mismatch",
    "missing_keyid",
    "missing_signature",
    "unknown_keyid",
    "unsupported_method",
}
EVENT_STATE_RUNTIME_CONFIG_ENV = "EVENT_STATE_RUNTIME_CONFIG_PATH"
EVENT_STATE_RUNTIME_CONFIG_DEFAULT = "event-state.runtime.json"
ACTOR_AUTH_RUNTIME_CONFIG_ENV = EVENT_STATE_RUNTIME_CONFIG_ENV
ACTOR_AUTH_RUNTIME_CONFIG_DEFAULT = EVENT_STATE_RUNTIME_CONFIG_DEFAULT
CHECKPOINT_INTEGRITY_METHOD = "hmac-sha256"
CHECKPOINT_SIGNING_ACTOR = "runtime"
CHECKPOINT_DEFAULT_MAX_INCREMENTAL_EVENTS = 128
CHECKPOINT_DEFAULT_COMPACTION_THRESHOLD = 1024
CHECKPOINT_POLICY_PATH = Path("runtime") / "CHECKPOINT_POLICY.json"
ARCHIVE_HASH_SUFFIX = ".sha256"


class EventLogError(RuntimeError):
    pass


class EventAuthSecretResolutionError(EventLogError):
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


class EventLogIntegrityError(RuntimeError):
    pass


def truncate_torn_jsonl_tail(path: Path) -> dict[str, Any] | None:
    """Remove an invalid JSONL tail so future appends stay visible to torn-safe readers."""
    if not path.exists():
        return None

    records: list[dict[str, Any]] = []
    offset = 0
    line_number = 0
    data = path.read_bytes()
    for raw_line in data.splitlines(keepends=True):
        line_number += 1
        next_offset = offset + len(raw_line)
        stripped = raw_line.strip()
        if not stripped:
            records.append({"valid": True, "end": next_offset, "blank": True})
            offset = next_offset
            continue
        try:
            decoded = raw_line.decode("utf-8-sig" if offset == 0 else "utf-8")
            event = json.loads(decoded)
        except (UnicodeDecodeError, json.JSONDecodeError):
            records.append({"valid": False, "line": line_number, "end": next_offset, "blank": False})
            offset = next_offset
            continue
        if not isinstance(event, dict):
            records.append({"valid": False, "line": line_number, "end": next_offset, "blank": False})
            offset = next_offset
            continue
        records.append({"valid": True, "end": next_offset, "blank": False})
        offset = next_offset

    valid_end = 0
    for index, record in enumerate(records):
        if record["valid"]:
            valid_end = int(record["end"])
            continue
        has_later_valid_event = any(
            later["valid"] and not later.get("blank", False) for later in records[index + 1 :]
        )
        if has_later_valid_event:
            raise EventLogIntegrityError(
                f"event log integrity error: invalid JSONL line {record['line']} has valid event records after it; "
                "refusing to truncate mid-file corruption"
            )
        with path.open("r+b") as handle:
            handle.truncate(valid_end)
            handle.flush()
            os.fsync(handle.fileno())
        return {
            "path": str(path),
            "line": record["line"],
            "truncated_bytes": len(data) - valid_end,
            "valid_bytes": valid_end,
        }
    return None


def atomic_append_jsonl(path: Path, event: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())


@contextmanager
def ledger_file_lock(root: Path) -> Iterator[None]:
    """Serialize event-log writers across processes before reading chain head."""
    lock_path = root.resolve() / LEDGER_LOCK_PATH
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    with lock_path.open("a+b") as handle:
        if sys.platform == "win32":
            import msvcrt

            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
            try:
                yield
            finally:
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            try:
                yield
            finally:
                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)


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
    payload.pop("event_auth", None)
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


def event_state_runtime_config_path(root: Path) -> Path:
    configured = os.environ.get(EVENT_STATE_RUNTIME_CONFIG_ENV)
    if configured:
        path = Path(configured)
        resolved = path.resolve() if path.is_absolute() else (root / path).resolve()
        if not path.is_absolute() and resolved != root.resolve() and root.resolve() not in resolved.parents:
            raise EventLogError("event_state runtime override path outside repository root")
        return resolved
    return (root / EVENT_STATE_RUNTIME_CONFIG_DEFAULT).resolve()


def actor_auth_runtime_config_path(root: Path) -> Path:
    return event_state_runtime_config_path(root)


def event_state_runtime_override(root: Path | None = None) -> dict[str, Any]:
    if root is None:
        return {}
    path = event_state_runtime_config_path(root)
    if not path.exists():
        return {}
    try:
        payload = json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:
        raise EventLogError(f"invalid event_state runtime override: {path}") from exc
    if not isinstance(payload, dict):
        raise EventLogError("event_state runtime override must be a JSON object")
    event_state = payload.get("event_state")
    if event_state is None:
        return {}
    if not isinstance(event_state, dict):
        raise EventLogError("event_state runtime override event_state must be an object")
    allowed = {"actor_auth_enforce", "actor_auth_config", "event_auth"}
    unsupported = sorted(str(key) for key in event_state if key not in allowed)
    if unsupported:
        raise EventLogError(f"event_state runtime override contains unsupported event_state keys: {', '.join(unsupported)}")
    event_auth = event_state.get("event_auth")
    if event_auth is not None:
        if not isinstance(event_auth, dict):
            raise EventLogError("event_state runtime override event_auth must be an object")
        allowed_event_auth = {"keys"}
        unsupported_event_auth = sorted(str(key) for key in event_auth if key not in allowed_event_auth)
        if unsupported_event_auth:
            raise EventLogError(
                f"event_state runtime override event_auth contains unsupported keys: {', '.join(unsupported_event_auth)}"
            )
        keys = event_auth.get("keys")
        if keys is not None and not isinstance(keys, dict):
            raise EventLogError("event_state runtime override event_auth.keys must be an object")
    return event_state


def actor_auth_runtime_override(root: Path | None = None) -> dict[str, Any]:
    override = event_state_runtime_override(root)
    return {key: value for key, value in override.items() if key in {"actor_auth_enforce", "actor_auth_config"}}


def actor_auth_event_state(config: dict[str, Any] | None, root: Path | None = None) -> dict[str, Any]:
    event_state = (config or {}).get("event_state")
    merged = dict(event_state) if isinstance(event_state, dict) else {}
    merged.pop("actor_auth_enforce", None)
    merged.pop("actor_auth_config", None)
    merged.update(actor_auth_runtime_override(root))
    return merged


def actor_auth_enforce_enabled(config: dict[str, Any] | None, root: Path | None = None) -> bool:
    event_state = actor_auth_event_state(config, root)
    return event_state.get("actor_auth_enforce") is True


def actor_auth_config(config: dict[str, Any] | None, root: Path | None = None) -> dict[str, Any]:
    event_state = actor_auth_event_state(config, root)
    value = event_state.get("actor_auth_config")
    return value if isinstance(value, dict) else {}


def actor_keyid(actor: str, config: dict[str, Any] | None, root: Path | None = None) -> str:
    cfg = actor_auth_config(config, root)
    keyids = cfg.get("keyids")
    if isinstance(keyids, dict) and str(keyids.get(actor) or "").strip():
        return str(keyids[actor])
    return {"Arquitecto": "arquitecto:v1", "Codex": "codex:v1", "Analista": "analista:v1"}.get(actor, f"{actor}:v1")


def actor_auth_signable_event(event: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(event)
    payload.pop("actor_auth", None)
    payload.pop("event_auth", None)
    payload.pop("prev_hash", None)
    payload.pop("deduped", None)
    return payload


def actor_auth_message(event: dict[str, Any]) -> bytes:
    return canonical_json(actor_auth_signable_event(event)).encode("utf-8")


def actor_auth_private_key_path(actor: str, keyid: str, config: dict[str, Any], *, root: Path) -> Path:
    cfg = actor_auth_config(config, root)
    files = cfg.get("private_key_files")
    configured = files.get(actor) if isinstance(files, dict) else None
    if configured is None and isinstance(files, dict):
        configured = files.get(keyid)
    if configured is not None:
        raw = Path(str(configured))
    else:
        base = Path(str(cfg.get("secret_root") or "D:/Agentes/protocol-secrets"))
        raw = base / f"{keyid.replace(':', '-')}.pem"
    if not raw.is_absolute():
        raw = root / raw
    resolved = raw.resolve()
    allowed_roots = [Path("D:/Agentes/protocol-secrets").resolve()]
    configured_root = cfg.get("secret_root")
    if configured_root:
        allowed_roots.append(Path(str(configured_root)).resolve())
    if configured is not None:
        allowed_roots.append(root.resolve())
    if not any(resolved == allowed or allowed in resolved.parents for allowed in allowed_roots):
        raise EventLogError("actor_auth private key path outside allowed roots")
    return resolved


def actor_public_keys(config: dict[str, Any] | None) -> dict[str, str]:
    event_state = (config or {}).get("event_state")
    sig_config = event_state.get("signature_config") if isinstance(event_state, dict) else {}
    keys = sig_config.get("public_keys") if isinstance(sig_config, dict) else {}
    return {str(key): str(value) for key, value in (keys or {}).items()} if isinstance(keys, dict) else {}


def sign_actor_auth(event: dict[str, Any], config: dict[str, Any], *, root: Path) -> dict[str, str]:
    try:
        from cryptography.hazmat.primitives import serialization  # type: ignore
    except ImportError as exc:
        raise EventLogError("cryptography package is required for actor_auth Ed25519 signing") from exc
    actor = str(event.get("actor") or "")
    keyid = actor_keyid(actor, config, root)
    private_key_path = actor_auth_private_key_path(actor, keyid, config, root=root)
    if not private_key_path.exists():
        raise EventLogError(f"actor_auth private signing key missing for actor: {actor}")
    key = serialization.load_pem_private_key(private_key_path.read_bytes(), password=None)
    signature = key.sign(actor_auth_message(event))
    return {"method": "ed25519", "keyid": keyid, "sig": base64.b64encode(signature).decode("ascii")}


def verify_actor_auth(event: dict[str, Any], config: dict[str, Any] | None, root: Path | None = None) -> dict[str, Any]:
    auth = event.get("actor_auth")
    if not isinstance(auth, dict):
        return {"valid": False, "reason": "unsupported_method"}
    method = str(auth.get("method") or "")
    if method == "not_enforced_phase2":
        return {"valid": True, "reason": "not_enforced_phase2"}
    if method != "ed25519":
        return {"valid": False, "reason": "unsupported_method"}
    keyid = str(auth.get("keyid") or "")
    if not keyid:
        return {"valid": False, "reason": "missing_keyid"}
    actor = str(event.get("actor") or "")
    if keyid != actor_keyid(actor, config, root):
        return {"valid": False, "reason": "keyid_mismatch"}
    signature = str(auth.get("sig") or "")
    if not signature:
        return {"valid": False, "reason": "missing_signature"}
    public_key_text = actor_public_keys(config).get(keyid)
    if not public_key_text:
        return {"valid": False, "reason": "unknown_keyid"}
    try:
        from cryptography.exceptions import InvalidSignature  # type: ignore
        from cryptography.hazmat.primitives import serialization  # type: ignore
        from cryptography.hazmat.primitives.asymmetric import ed25519  # type: ignore
    except ImportError as exc:
        raise EventLogError("actor_auth verification unavailable: cryptography package is required") from exc
    try:
        raw_signature = base64.b64decode(signature, validate=True)
        key_text = public_key_text.strip()
        if "BEGIN PUBLIC KEY" in key_text:
            key = serialization.load_pem_public_key(key_text.encode("ascii"))
        else:
            key = ed25519.Ed25519PublicKey.from_public_bytes(base64.b64decode(key_text, validate=True))
        if not isinstance(key, ed25519.Ed25519PublicKey):
            return {"valid": False, "reason": "invalid_signature"}
        key.verify(raw_signature, actor_auth_message(event))
        return {"valid": True, "reason": "valid"}
    except InvalidSignature:
        return {"valid": False, "reason": "invalid_signature"}
    except Exception:
        return {"valid": False, "reason": "invalid_signature"}

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


COST_ATTRIBUTION_EVENT_TYPE = "cost.attributed"
COST_ATTRIBUTION_DIMENSIONS = ("handoff", "decision", "agent")
# Canonical `subject` key per dimension (DECISION-0033 hardening, analista pasada-3 C1): the subject
# is built from a single typed identifier so two logically-equal emissions hash identically; no prose.
COST_ATTRIBUTION_SUBJECT_KEY = {"handoff": "handoff_id", "decision": "decision_id", "agent": "agent_id"}
# Default unit/version tags carried by every cost.attributed payload (C2). `tokens_total` = producer's
# input(context)+output(generation) tokens (self-reported scalar). `context_tokens` = the producer's
# INPUT-context measure (runtime `assembled_context_tokens`, a chars/divisor proxy; the invoker exposes
# no prompt/completion split). schema "2" carries cost_tokens + context_tokens. Bump on any change.
COST_ATTRIBUTION_DEFAULT_UNIT = "tokens_total"
COST_ATTRIBUTION_DEFAULT_CONTEXT_UNIT = "context_tokens_proxy_chars_div"
COST_ATTRIBUTION_DEFAULT_SCHEMA = "2"


def cost_attribution_enabled(config: dict[str, Any] | None) -> bool:
    metrics = (config or {}).get("metrics")
    return isinstance(metrics, dict) and metrics.get("cost_attribution_enabled") is True


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


def event_auth_runtime_config(config: dict[str, Any] | None, root: Path | None = None) -> dict[str, Any]:
    config_event_auth = (config or {}).get("event_auth")
    merged = dict(config_event_auth) if isinstance(config_event_auth, dict) else {}
    override = event_state_runtime_override(root)
    override_event_auth = override.get("event_auth")
    if isinstance(override_event_auth, dict):
        for key, value in override_event_auth.items():
            if key == "keys" and isinstance(value, dict):
                current = merged.get("keys")
                keys = dict(current) if isinstance(current, dict) else {}
                keys.update(value)
                merged["keys"] = keys
            else:
                merged[key] = value
    return merged


def agent_auth_config(config: dict[str, Any], actor: str, *, root: Path | None = None) -> dict[str, Any]:
    event_auth = event_auth_runtime_config(config, root)
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


def secret_root_dirs(config: dict[str, Any]) -> set[str]:
    event_auth = config.get("event_auth") if isinstance(config.get("event_auth"), dict) else {}
    configured = event_auth.get("secret_dirs") if isinstance(event_auth, dict) else None
    if not isinstance(configured, list):
        return set(SECRET_DIRS)
    values = {str(item).strip().replace("\\", "/").strip("/") for item in configured if str(item).strip()}
    return values or set(SECRET_DIRS)


def resolve_secret_file(path_text: str, *, root: Path, config: dict[str, Any]) -> str:
    if root is None:
        raise EventAuthSecretResolutionError("unresolved_key: secret_file requires explicit root")
    raw_path = Path(str(path_text or ""))
    if raw_path.is_absolute():
        raise EventAuthSecretResolutionError("unresolved_key: secret_file must be relative")
    normalized = raw_path.as_posix()
    if not normalized or normalized.startswith("../") or "/../" in normalized or normalized == "..":
        raise EventAuthSecretResolutionError("unresolved_key: secret_file traversal rejected")
    first_part = normalized.split("/", 1)[0]
    if first_part not in secret_root_dirs(config):
        raise EventAuthSecretResolutionError("unresolved_key: secret_file outside allowed dirs")
    path = (root.resolve() / raw_path).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as exc:
        raise EventAuthSecretResolutionError("unresolved_key: secret_file escaped root") from exc
    try:
        value = path.read_text(encoding="utf-8-sig").strip()
    except OSError as exc:
        raise EventAuthSecretResolutionError("unresolved_key: secret_file unreadable") from exc
    if not value:
        raise EventAuthSecretResolutionError("unresolved_key: secret_file empty")
    return value


def resolve_event_auth_secret(auth: dict[str, Any], *, root: Path | None, config: dict[str, Any]) -> str | None:
    for key in ("secret", "hmac_secret", "signing_secret", "key"):
        value = auth.get(key)
        if str(value or "").strip():
            return str(value)
    if str(auth.get("secret_file") or "").strip():
        if root is None:
            raise EventAuthSecretResolutionError("unresolved_key: secret_file requires explicit root")
        return resolve_secret_file(str(auth["secret_file"]), root=root, config=config)
    if str(auth.get("secret_env") or "").strip():
        value = os.environ.get(str(auth["secret_env"]))
        if not str(value or "").strip():
            raise EventAuthSecretResolutionError("unresolved_key: secret_env missing")
        return str(value)
    return None


def signing_secret(config: dict[str, Any], actor: str, *, root: Path | None = None) -> str | None:
    auth = agent_auth_config(config, actor, root=root)
    return resolve_event_auth_secret(auth, root=root, config=config)


def signing_key_id(config: dict[str, Any], actor: str, *, root: Path | None = None) -> str:
    auth = agent_auth_config(config, actor, root=root)
    return str(auth.get("key_id") or f"{actor}:local")


def event_auth_config_for_key_id(
    config: dict[str, Any], key_id: str, *, root: Path | None = None
) -> dict[str, Any] | None:
    """Resolve verification material by the identifier carried by the event."""
    event_auth = event_auth_runtime_config(config, root)
    keys = event_auth.get("keys") or {}
    if not isinstance(keys, dict):
        return None
    for actor, entry in keys.items():
        candidate = agent_auth_config(config, str(actor), root=root)
        if str(candidate.get("key_id") or f"{actor}:local") == key_id:
            return candidate
    return None


def event_auth_key_registry(config: dict[str, Any] | None, *, root: Path | None = None) -> dict[str, dict[str, Any]]:
    """Return the versioned identity/lifetime registry, or configured keys for legacy instances."""
    if root is not None:
        path = root.resolve() / EVENT_AUTH_KEY_REGISTRY_PATH
        if path.exists():
            try:
                payload = json.loads(path.read_text(encoding="utf-8-sig"))
            except (OSError, json.JSONDecodeError):
                return {}
            keys = payload.get("keys") if isinstance(payload, dict) else None
            return {str(key): value for key, value in (keys or {}).items() if isinstance(value, dict)}
    derived: dict[str, dict[str, Any]] = {}
    keys = event_auth_runtime_config(config, root).get("keys") or {}
    if isinstance(keys, dict):
        for actor, entry in keys.items():
            if not isinstance(entry, dict):
                continue
            key_id = str(entry.get("key_id") or f"{actor}:local")
            derived[key_id] = {"actor": str(actor), "status": "active", "valid_through_seq": None}
    return derived


def event_auth_registry_sha256(root: Path) -> str:
    path = root.resolve() / EVENT_AUTH_KEY_REGISTRY_PATH
    if not path.is_file():
        return ""
    return hashlib.sha256(path.read_bytes()).hexdigest()


def validate_event_auth_registry_anchor(events: list[dict[str, Any]], *, root: Path) -> dict[str, Any]:
    if not (root.resolve() / EVENT_AUTH_KEY_REGISTRY_PATH).is_file():
        return {"valid": True, "reason": "registry_absent", "checked": 0}
    anchors = [event for event in events if str(event.get("type") or "") == EVENT_AUTH_REGISTRY_ANCHOR]
    if not anchors:
        return {"valid": False, "reason": "registry_anchor_missing", "checked": 0}
    latest = max(anchors, key=lambda item: int(item.get("seq") or 0))
    payload = latest.get("payload") if isinstance(latest.get("payload"), dict) else {}
    expected = str(payload.get("registry_sha256") or "")
    actual = event_auth_registry_sha256(root)
    if not re.fullmatch(r"[0-9a-f]{64}", expected):
        return {"valid": False, "reason": "registry_anchor_invalid", "seq": latest.get("seq"), "checked": len(anchors)}
    if not actual:
        return {"valid": False, "reason": "registry_missing", "seq": latest.get("seq"), "checked": len(anchors)}
    if not hmac.compare_digest(expected, actual):
        return {
            "valid": False,
            "reason": "registry_anchor_mismatch",
            "seq": latest.get("seq"),
            "expected": expected,
            "actual": actual,
            "checked": len(anchors),
        }
    return {"valid": True, "reason": "registry_anchor_valid", "seq": latest.get("seq"), "checked": len(anchors)}


def signable_event(event: dict[str, Any]) -> dict[str, Any]:
    payload = deepcopy(event)
    payload.pop("event_auth", None)
    payload.pop("deduped", None)
    return payload


def event_signature(event: dict[str, Any], secret: str) -> str:
    return hmac.new(secret.encode("utf-8"), canonical_json(signable_event(event)).encode("utf-8"), hashlib.sha256).hexdigest()


def sign_event(event: dict[str, Any], config: dict[str, Any], *, root: Path | None = None) -> dict[str, Any]:
    if not event_auth_enabled(config):
        return event
    actor = str(event.get("actor") or "")
    secret = signing_secret(config, actor, root=root)
    if not secret:
        raise EventLogError(f"event auth signing key missing for actor: {actor}")
    auth = agent_auth_config(config, actor, root=root)
    signed = dict(event)
    signed["event_auth"] = {
        "method": str(auth.get("method") or (config.get("event_auth") or {}).get("method") or "hmac-sha256"),
        "key_id": signing_key_id(config, actor, root=root),
        "signature": event_signature(signed, secret),
    }
    if str(auth.get("issuer") or "").strip():
        signed["event_auth"]["issuer"] = str(auth["issuer"])
    if str(auth.get("audience") or "").strip():
        signed["event_auth"]["audience"] = str(auth["audience"])
    return signed


def verify_event_auth(
    event: dict[str, Any],
    config: dict[str, Any] | None,
    *,
    root: Path | None = None,
    declared_unavailable_key_ids: set[str] | None = None,
) -> dict[str, Any]:
    if not event_auth_enabled(config):
        return {"valid": True, "reason": "event_auth_disabled"}
    auth = event.get("event_auth")
    if not isinstance(auth, dict):
        return {"valid": False, "reason": "missing_signature"}
    signature = str(auth.get("signature") or "")
    if not signature:
        return {"valid": False, "reason": "missing_signature"}
    key_id = str(auth.get("key_id") or "")
    if not key_id:
        return {"valid": False, "reason": "missing_key_id"}
    registry_entry = event_auth_key_registry(config, root=root).get(key_id)
    if registry_entry is None:
        return {"valid": False, "reason": "unknown_key_id", "key_id": key_id}
    registered_actor = str(registry_entry.get("actor") or "")
    if not registered_actor or registered_actor != str(event.get("actor") or ""):
        return {"valid": False, "reason": "key_actor_mismatch", "key_id": key_id}
    status = str(registry_entry.get("status") or "")
    valid_through = registry_entry.get("valid_through_seq")
    if status == "active":
        if valid_through is not None:
            return {"valid": False, "reason": "active_key_has_boundary", "key_id": key_id}
    elif status == "retired":
        if valid_through is None:
            return {"valid": False, "reason": "retired_key_missing_boundary", "key_id": key_id}
    else:
        return {"valid": False, "reason": "invalid_key_status", "key_id": key_id}
    if status == "retired" and int(event.get("seq") or 0) > int(valid_through):
        return {"valid": False, "reason": "key_outside_validity", "key_id": key_id}
    key_config = event_auth_config_for_key_id(config or {}, key_id, root=root)
    if key_config is None:
        return {"valid": False, "reason": "unresolved_key", "key_id": key_id}
    try:
        secret = resolve_event_auth_secret(key_config, root=root, config=config or {})
    except EventAuthSecretResolutionError:
        return {"valid": False, "reason": "unresolved_key", "key_id": key_id}
    if not secret:
        return {"valid": False, "reason": "missing_key", "key_id": key_id}
    expected = event_signature(event, secret)
    if not hmac.compare_digest(signature, expected):
        return {"valid": False, "reason": "invalid_signature"}
    return {"valid": True, "reason": "valid"}


def attested_unavailable_event_auth_key_ids(
    events: list[dict[str, Any]], config: dict[str, Any] | None, *, root: Path | None = None
) -> set[str]:
    """Legacy declaration reader retained for compatibility; the versioned registry is authoritative."""
    declared: set[str] = set()
    for event in events:
        if str(event.get("type") or "") != EVENT_AUTH_ROTATION_DECLARATION:
            continue
        if verify_event_auth(event, config, root=root).get("valid") is not True:
            continue
        payload = event.get("payload")
        key_ids = payload.get("unavailable_key_ids") if isinstance(payload, dict) else None
        if not isinstance(key_ids, list):
            continue
        declared.update(str(item).strip() for item in key_ids if str(item).strip())
    return declared


def event_auth_verification_boundaries(
    events: list[dict[str, Any]], config: dict[str, Any] | None, *, root: Path | None = None
) -> list[dict[str, Any]]:
    declared = attested_unavailable_event_auth_key_ids(events, config, root=root)
    boundaries: list[dict[str, Any]] = []
    for event in sorted(events, key=lambda item: int(item.get("seq") or 0)):
        result = verify_event_auth(
            event,
            config,
            root=root,
            declared_unavailable_key_ids=declared,
        )
        if result.get("reason") in EVENT_AUTH_UNVERIFIABLE_REASONS:
            boundaries.append(
                {
                    "seq": event.get("seq"),
                    "actor": event.get("actor"),
                    "key_id": result.get("key_id"),
                    "status": result.get("reason"),
                }
            )
    return boundaries


def checkpoint_runtime_config(config: dict[str, Any] | None, root: Path | None = None) -> dict[str, Any]:
    checkpoint: Any = None
    if root is not None:
        path = root.resolve() / CHECKPOINT_POLICY_PATH
        if path.exists():
            try:
                payload = json.loads(path.read_text(encoding="utf-8-sig"))
            except Exception as exc:
                raise EventLogError(f"invalid checkpoint runtime registry: {path}") from exc
            if not isinstance(payload, dict):
                raise EventLogError("checkpoint runtime registry must be a JSON object")
            checkpoint = payload
    if not isinstance(checkpoint, dict):
        checkpoint = {}
    try:
        return {
            "max_incremental_events": int(
                checkpoint.get("max_incremental_events", CHECKPOINT_DEFAULT_MAX_INCREMENTAL_EVENTS)
            ),
            "compaction_threshold": int(
                checkpoint.get("compaction_threshold", CHECKPOINT_DEFAULT_COMPACTION_THRESHOLD)
            ),
        }
    except (TypeError, ValueError) as exc:
        raise EventLogError("checkpoint runtime registry contains a non-numeric limit") from exc


def checkpoint_signable_payload(snapshot: dict[str, Any], checkpoint_event: dict[str, Any]) -> dict[str, Any]:
    try:
        up_to_seq = int(snapshot.get("up_to_seq") or 0)
    except (TypeError, ValueError) as exc:
        raise EventLogError("checkpoint up_to_seq must be numeric") from exc
    return {
        "canonical_hash": str(snapshot.get("canonical_hash") or ""),
        "up_to_seq": up_to_seq,
        "prev_hash": str(checkpoint_event.get("prev_hash") or ""),
    }


def sign_snapshot_checkpoint(
    snapshot: dict[str, Any],
    checkpoint_event: dict[str, Any],
    config: dict[str, Any],
    *,
    root: Path,
) -> dict[str, Any]:
    secret = signing_secret(config, CHECKPOINT_SIGNING_ACTOR, root=root)
    if not secret:
        raise EventLogError("checkpoint signing key missing for runtime")
    payload = checkpoint_signable_payload(snapshot, checkpoint_event)
    signature = hmac.new(
        secret.encode("utf-8"),
        canonical_json(payload).encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    return {
        "method": CHECKPOINT_INTEGRITY_METHOD,
        "key_id": signing_key_id(config, CHECKPOINT_SIGNING_ACTOR, root=root),
        "signature": signature,
        **payload,
    }


def verify_snapshot_checkpoint(
    root: Path,
    snapshot: dict[str, Any] | None = None,
    events: list[dict[str, Any]] | None = None,
    *,
    max_incremental_events: int | None = None,
) -> dict[str, Any]:
    """Return a trusted replay base or a fail-safe reason for full verification."""
    try:
        stored = snapshot if snapshot is not None else load_snapshot(root)
    except (OSError, ValueError, json.JSONDecodeError):
        return {"trusted": False, "reason": "invalid_snapshot"}
    integrity = stored.get("integrity")
    if not isinstance(integrity, dict):
        return {"trusted": False, "reason": "missing_integrity"}
    if str(integrity.get("method") or "") != CHECKPOINT_INTEGRITY_METHOD:
        return {"trusted": False, "reason": "unsupported_method"}

    if archive_integrity(root).get("valid") is not True:
        return {"trusted": False, "reason": "invalid_archive_integrity"}
    try:
        ordered = sorted(
            events if events is not None else all_events(root),
            key=lambda item: int(item.get("seq") or 0),
        )
        up_to_seq = int(stored.get("up_to_seq") or 0)
        head_seq = int(ordered[-1].get("seq") or 0) if ordered else 0
    except (TypeError, ValueError):
        return {"trusted": False, "reason": "invalid_checkpoint_sequence"}
    if not ordered:
        return {"trusted": False, "reason": "empty_log"}
    try:
        limit = (
            int(max_incremental_events)
            if max_incremental_events is not None
            else checkpoint_runtime_config(read_protocol_config(root), root)["max_incremental_events"]
        )
    except (EventLogError, TypeError, ValueError):
        return {"trusted": False, "reason": "invalid_checkpoint_policy"}
    if up_to_seq <= 0 or up_to_seq > head_seq:
        return {"trusted": False, "reason": "checkpoint_out_of_range"}
    if limit < 0 or head_seq - up_to_seq > limit:
        return {"trusted": False, "reason": "stale_checkpoint"}

    checkpoint_event = next(
        (event for event in ordered if int(event.get("seq") or 0) == up_to_seq),
        None,
    )
    if checkpoint_event is None:
        return {"trusted": False, "reason": "checkpoint_event_missing"}
    state_hash = canonical_hash(stored.get("state") or {})
    if state_hash != str(stored.get("canonical_hash") or ""):
        return {"trusted": False, "reason": "state_hash_mismatch"}
    expected_payload = checkpoint_signable_payload(stored, checkpoint_event)
    if any(integrity.get(key) != value for key, value in expected_payload.items()):
        return {"trusted": False, "reason": "checkpoint_metadata_mismatch"}

    config = read_protocol_config(root)
    try:
        secret = signing_secret(config, CHECKPOINT_SIGNING_ACTOR, root=root)
    except EventAuthSecretResolutionError:
        return {"trusted": False, "reason": "unresolved_key"}
    if not secret:
        return {"trusted": False, "reason": "missing_key"}
    if str(integrity.get("key_id") or "") != signing_key_id(
        config, CHECKPOINT_SIGNING_ACTOR, root=root
    ):
        return {"trusted": False, "reason": "key_id_mismatch"}
    expected_signature = hmac.new(
        secret.encode("utf-8"),
        canonical_json(expected_payload).encode("utf-8"),
        hashlib.sha256,
    ).hexdigest()
    if not hmac.compare_digest(str(integrity.get("signature") or ""), expected_signature):
        return {"trusted": False, "reason": "invalid_signature"}
    return {
        "trusted": True,
        "reason": "valid",
        "up_to_seq": up_to_seq,
        "base_state": deepcopy(stored.get("state") or {}),
        "incremental_events": [
            event for event in ordered if int(event.get("seq") or 0) > up_to_seq
        ],
    }


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


def archive_hash_path(path: Path) -> Path:
    return path.with_name(path.name + ARCHIVE_HASH_SUFFIX)


def archive_integrity(root: Path) -> dict[str, Any]:
    """Verify every compacted file before the live path trusts its checkpoint."""
    archive_dir = root / ARCHIVE_DIR
    if not archive_dir.exists():
        return {"valid": True, "checked": 0}
    checked = 0
    for path in sorted(archive_dir.glob("events-*.jsonl")):
        digest_path = archive_hash_path(path)
        try:
            expected = digest_path.read_text(encoding="ascii").strip().lower()
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
        except OSError:
            return {"valid": False, "reason": "archive_hash_unreadable", "path": str(path)}
        if len(expected) != 64 or not hmac.compare_digest(expected, actual):
            return {"valid": False, "reason": "archive_hash_mismatch", "path": str(path)}
        checked += 1
    return {"valid": True, "checked": checked}


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
    root: Path | None = None,
) -> dict[str, Any]:
    state = deepcopy(base_state) if base_state is not None else empty_snapshot()["state"]
    state.setdefault("aggregate_versions", {})
    state.setdefault("fencing_tokens", {})
    state.setdefault("leases", {})
    state.setdefault("idempotency_keys", {})
    state.setdefault("events_applied", 0)
    state.setdefault("rejections", [])
    declared_unavailable_key_ids = attested_unavailable_event_auth_key_ids(events, config, root=root)

    for event in sorted(events, key=lambda item: int(item.get("seq") or 0)):
        event_type = str(event.get("type") or "")
        aggregate_id = str(event.get("aggregate_id") or "")
        auth_result = verify_event_auth(
            event,
            config,
            root=root,
            declared_unavailable_key_ids=declared_unavailable_key_ids,
        )
        actor_auth_result = verify_actor_auth(event, config, root)
        if (
            auth_result.get("valid") is not True
            and str(auth_result.get("reason")) not in EVENT_AUTH_UNVERIFIABLE_REASONS
        ):
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
        if actor_auth_result.get("valid") is not True and str(actor_auth_result.get("reason")) in ACTOR_AUTH_TAMPER_REASONS:
            state["rejections"].append(
                {
                    "seq": event.get("seq"),
                    "aggregate_id": aggregate_id,
                    "event": "security.invalid_actor_auth",
                    "reason": actor_auth_result.get("reason"),
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
        "state": replay_events(events, config=read_protocol_config(root), root=root),
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
        events = self.events()
        config = read_protocol_config(self.root)
        checkpoint = verify_snapshot_checkpoint(self.root, events=events)
        if checkpoint.get("trusted") is True:
            return replay_events(
                checkpoint["incremental_events"],
                base_state=checkpoint["base_state"],
                config=config,
                root=self.root,
            )
        return replay_events(events, config=config, root=self.root)

    def next_seq(self) -> int:
        events = self.events()
        return (int(events[-1].get("seq") or 0) + 1) if events else 1

    def chain_anchor(
        self,
        config: dict[str, Any],
        verified_state: dict[str, Any] | None = None,
    ) -> str:
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
        genesis = sign_event(genesis, config, root=self.root)
        atomic_append_jsonl(self.log_path, genesis)
        if verified_state is not None:
            advanced = replay_events([genesis], base_state=verified_state, config=config, root=self.root)
            verified_state.clear()
            verified_state.update(advanced)
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
        verified_state: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        state = verified_state if verified_state is not None else self.state()
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
        if actor_auth is None and actor_auth_enforce_enabled(config, self.root):
            event["actor_auth"] = sign_actor_auth(event, config, root=self.root)
        if chain_enabled(config):
            previous_hash = self.chain_anchor(config, verified_state)
            event["seq"] = self.next_seq()
            if actor_auth is None and actor_auth_enforce_enabled(config, self.root):
                event["actor_auth"] = sign_actor_auth(event, config, root=self.root)
        if observability_enabled(config):
            event["trace_id"] = event_trace_id(event)
        if chain_enabled(config):
            event["prev_hash"] = compute_event_prev_hash(event, previous_hash)
        event = sign_event(event, config, root=self.root)
        atomic_append_jsonl(self.log_path, event)
        if verified_state is not None:
            advanced = replay_events([event], base_state=state, config=config, root=self.root)
            verified_state.clear()
            verified_state.update(advanced)
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

    def append_cost_attribution(
        self,
        *,
        dimension: str,
        actor_id: str,
        subject_hash: str,
        cost_tokens: int,
        cost_unit: str = COST_ATTRIBUTION_DEFAULT_UNIT,
        cost_schema: str = COST_ATTRIBUTION_DEFAULT_SCHEMA,
        context_tokens: int | None = None,
        context_unit: str = COST_ATTRIBUTION_DEFAULT_CONTEXT_UNIT,
        subject_seq: int | None = None,
        task_id: str | None = None,
        decision_id: str | None = None,
        idempotency_key: str | None = None,
        ts: str | None = None,
    ) -> dict[str, Any] | None:
        """Emit a `cost.attributed` annotation event (DECISION-0033, two-plane).

        Protocol plane only: structured metric + `subject_hash` reference; no free text. The event is
        `applied:false` so `protocol_replay.replay_protocol_state` skips it (no state mutation, no
        drift). Off-by-default: returns None and writes nothing unless `metrics.cost_attribution_enabled`.

        `cost_unit`/`cost_schema` (analista pasada-3 C2) are ALWAYS carried so the immutable corpus is
        self-describing; the summarizer rejects rows without them. `cost_unit` defaults to
        `tokens_total` (producer input+output). `subject_hash` is a SEUDONIMO, not anonymous
        (DECISION-0033): the payload plane is retained and re-linkable by this hash.
        """
        config = read_protocol_config(self.root)
        if not cost_attribution_enabled(config):
            return None
        dimension = str(dimension or "")
        if dimension not in COST_ATTRIBUTION_DIMENSIONS:
            raise EventLogError(f"invalid cost attribution dimension: {dimension}")
        unit = str(cost_unit or "").strip()
        schema = str(cost_schema or "").strip()
        if not unit or not schema:
            raise EventLogError("cost.attributed requires non-empty cost_unit and cost_schema")
        payload: dict[str, Any] = {
            "dimension": dimension,
            "subject_hash": str(subject_hash),
            "subject_seq": int(subject_seq) if subject_seq is not None else None,
            "cost_tokens": int(cost_tokens),
            "cost_unit": unit,
            "cost_schema": schema,
            "context_tokens": int(context_tokens) if context_tokens is not None else None,
            "context_unit": str(context_unit or "").strip() or COST_ATTRIBUTION_DEFAULT_CONTEXT_UNIT,
        }
        if task_id:
            payload["task_id"] = str(task_id)
        if decision_id:
            payload["decision_id"] = str(decision_id)
        return self.append_event(
            event_type=COST_ATTRIBUTION_EVENT_TYPE,
            aggregate_id=str(task_id or decision_id or subject_hash),
            actor_id=actor_id,
            idempotency_key=idempotency_key,
            applied=False,
            payload=payload,
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
        verified_state: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        state = verified_state if verified_state is not None else self.state()
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
            verified_state=verified_state,
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
        verified_state: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        state = verified_state if verified_state is not None else self.state()
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
                verified_state=verified_state,
            )
        return self.append_event(
            event_type="intent.applied",
            aggregate_id=task_id,
            actor_id=actor_id,
            idempotency_key=key,
            fencing_token=fencing_token,
            payload={"transition": transition, "attempt_id": attempt_id, **(payload or {})},
            verified_state=verified_state,
        )

    def write_snapshot(self, verified_state: dict[str, Any] | None = None) -> dict[str, Any]:
        if verified_state is None:
            snapshot = rebuild_snapshot(self.root)
        else:
            events = self.events()
            snapshot = {
                "up_to_seq": int(events[-1]["seq"]) if events else 0,
                "state": deepcopy(verified_state),
            }
            snapshot["canonical_hash"] = canonical_hash(snapshot["state"])
        events = self.events()
        if events:
            config = read_protocol_config(self.root)
            if event_auth_enabled(config):
                try:
                    snapshot["integrity"] = sign_snapshot_checkpoint(
                        snapshot,
                        events[-1],
                        config,
                        root=self.root,
                    )
                except (EventAuthSecretResolutionError, EventLogError):
                    snapshot.pop("integrity", None)
        write_snapshot(self.root, snapshot)
        try:
            policy = checkpoint_runtime_config(read_protocol_config(self.root), self.root)
            threshold = int(policy["compaction_threshold"])
        except (EventLogError, TypeError, ValueError):
            threshold = -1
        if (
            snapshot.get("integrity")
            and threshold >= 0
            and len(read_jsonl_torn_safe(self.log_path)) > threshold
        ):
            self.compact_through(int(snapshot["up_to_seq"]))
        return snapshot

    def compact_through(self, up_to_seq: int) -> Path | None:
        live_events = read_jsonl_torn_safe(self.log_path)
        archive_events = [event for event in live_events if int(event.get("seq") or 0) <= up_to_seq]
        remaining = [event for event in live_events if int(event.get("seq") or 0) > up_to_seq]
        if not archive_events:
            return None
        archive_path = self.root / ARCHIVE_DIR / f"events-{archive_events[0]['seq']:06d}-{archive_events[-1]['seq']:06d}.jsonl"
        archive_path.parent.mkdir(parents=True, exist_ok=True)
        archive_bytes = "".join(
            json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
            for event in archive_events
        ).encode("utf-8")
        archive_temp = archive_path.with_suffix(archive_path.suffix + ".tmp")
        archive_temp.write_bytes(archive_bytes)
        archive_temp.replace(archive_path)
        digest_path = archive_hash_path(archive_path)
        digest_temp = digest_path.with_suffix(digest_path.suffix + ".tmp")
        digest_temp.write_text(hashlib.sha256(archive_bytes).hexdigest() + "\n", encoding="ascii")
        digest_temp.replace(digest_path)
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        log_temp = self.log_path.with_suffix(self.log_path.suffix + ".tmp")
        log_temp.write_text(
            "".join(json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n" for event in remaining),
            encoding="utf-8",
        )
        log_temp.replace(self.log_path)
        return archive_path


def replay_without_side_effects(root: Path, forbidden_callback: Callable[[], None] | None = None) -> dict[str, Any]:
    if forbidden_callback is not None:
        # The callback is deliberately not invoked. Golden tests pass a callback that raises.
        pass
    return rebuild_snapshot(root)
