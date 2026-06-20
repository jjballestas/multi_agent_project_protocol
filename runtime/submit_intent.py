#!/usr/bin/env python3
"""Submit protocol-state intents through the runtime event log."""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

try:
    from .context import active_claims, has_capability, load_agent_registry, load_state, tasks_by_id
    from .eventlog import EventWriter, STATE_DIR, canonical_hash
    from .protocol_replay import (
        PROTOCOL_STATE_PATHS,
        apply_intent_event,
        current_protocol_snapshot,
        event_state_config_error,
        has_protocol_genesis,
        materialize_to_disk,
        protocol_state_drift,
        write_genesis_reference,
    )
    from .temp_paths import make_root_temp_dir, remove_root_temp_dir
except ImportError:  # pragma: no cover - direct script execution
    from context import active_claims, has_capability, load_agent_registry, load_state, tasks_by_id
    from eventlog import EventWriter, STATE_DIR, canonical_hash
    from protocol_replay import (
        PROTOCOL_STATE_PATHS,
        apply_intent_event,
        current_protocol_snapshot,
        event_state_config_error,
        has_protocol_genesis,
        materialize_to_disk,
        protocol_state_drift,
        write_genesis_reference,
    )
    from temp_paths import make_root_temp_dir, remove_root_temp_dir


VALID_TASK_STATUSES = {
    "proposed",
    "ready",
    "claimed",
    "in_progress",
    "in_review",
    "changes_requested",
    "review_approved",
    "qa_pending",
    "qa_failed",
    "architect_review",
    "done",
    "blocked",
    "cancelled",
}
INTENT_TYPES = {"task_status", "task_upsert", "claim", "decision", "project_narrative", "protocol_prune", "mailbox_archive"}
PROJECT_NARRATIVE_FIELDS = {"next_actions", "risks", "open_questions"}
MAILBOX_MESSAGE_ID_RE = re.compile(r"^MSG-[A-Za-z0-9._-]+$")
ROW_SCOPED_LEDGER_PATHS = {
    "Area_comun/state/TASK_INDEX.json",
    "Area_comun/state/PROJECT_STATE.json",
}


class IntentError(RuntimeError):
    pass


class IntentValidationError(IntentError):
    pass


class IntentApplyError(IntentError):
    pass


RuntimeStateBackup = tuple[Path, Path | None]
FileBackup = dict[str, bytes | None]


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def canonical_json_text(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=4, ensure_ascii=True, sort_keys=True) + "\n"


def normalized_path(path: str) -> str:
    return str(path or "").replace("\\", "/").strip()


def split_scope(scope: str) -> tuple[str, str | None]:
    path, separator, selector = normalized_path(scope).partition("#")
    return path, selector if separator else None


def mailbox_claim_scope_error(scope: str) -> str | None:
    path, _selector = split_scope(scope)
    mailbox_root = "Area_comun/mailbox"
    normalized = path.rstrip("/")
    if normalized != mailbox_root and not normalized.startswith(f"{mailbox_root}/"):
        return None
    filename = normalized.rsplit("/", 1)[-1]
    if filename.startswith("MSG-") and filename.endswith(".md"):
        return None
    return f"mailbox claim must be file-scoped: {scope}"


def scope_covers(scope_entry: str, required_entry: str) -> bool:
    scope_path, scope_selector = split_scope(scope_entry)
    required_path, required_selector = split_scope(required_entry)
    if scope_path == "*":
        return True
    if scope_path != required_path:
        if scope_selector is not None or required_selector is not None:
            return False
        return required_path.startswith(scope_path) if scope_path.endswith("/") else required_path == scope_path
    if scope_path in ROW_SCOPED_LEDGER_PATHS:
        if scope_selector is None:
            return True
        return required_selector is not None and scope_selector == required_selector
    if scope_selector is None and required_selector is None:
        return True
    return scope_selector == required_selector


def scopes_overlap(left: str, right: str) -> bool:
    return scope_covers(left, right) or scope_covers(right, left)


def snapshot_runtime_state(root: Path) -> RuntimeStateBackup:
    temp_root = make_root_temp_dir(root, ".submit-intent-runtime-backup-")
    state_dir = root / STATE_DIR
    backup_dir = temp_root / "state"
    if state_dir.exists():
        shutil.copytree(state_dir, backup_dir)
        return temp_root, backup_dir
    return temp_root, None


def restore_runtime_state(root: Path, backup: RuntimeStateBackup) -> None:
    temp_root, backup_dir = backup
    state_dir = root / STATE_DIR
    if state_dir.exists():
        shutil.rmtree(state_dir)
    if backup_dir is not None and backup_dir.exists():
        shutil.copytree(backup_dir, state_dir)
    remove_root_temp_dir(temp_root)


def cleanup_runtime_state_backup(backup: RuntimeStateBackup) -> None:
    remove_root_temp_dir(backup[0])


def snapshot_files(root: Path, relatives: list[str]) -> FileBackup:
    backup: FileBackup = {}
    for relative in sorted({normalized_path(item) for item in relatives if str(item).strip()}):
        path = root / relative
        backup[relative] = path.read_bytes() if path.exists() else None
    return backup


def restore_files(root: Path, backup: FileBackup) -> None:
    for relative, payload in backup.items():
        path = root / relative
        if payload is None:
            if path.exists():
                path.unlink()
            continue
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)


def parse_intent(intent: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    if not isinstance(intent, dict):
        raise IntentValidationError("intent must be a JSON object")
    explicit_type = str(intent.get("type") or "").strip()
    if explicit_type:
        if explicit_type not in INTENT_TYPES:
            raise IntentValidationError(f"unsupported intent type: {explicit_type}")
        payload = {key: value for key, value in intent.items() if key not in {"type", "idempotency_key"}}
        return explicit_type, payload
    keys = [key for key in INTENT_TYPES if key in intent]
    if len(keys) != 1:
        supported = ", ".join(sorted(INTENT_TYPES))
        raise IntentValidationError(f"intent must declare exactly one of: {supported}")
    payload = intent[keys[0]]
    if not isinstance(payload, dict):
        raise IntentValidationError(f"{keys[0]} intent payload must be an object")
    if "idempotency_key" in intent and "idempotency_key" not in payload:
        payload = {**payload, "idempotency_key": intent["idempotency_key"]}
    return keys[0], payload


def require_text(payload: dict[str, Any], key: str) -> str:
    value = str(payload.get(key) or "").strip()
    if not value:
        raise IntentValidationError(f"{key} is required")
    return value


def require_string_list(value: Any, key: str) -> list[str]:
    if not isinstance(value, list):
        raise IntentValidationError(f"{key} must be a list")
    result: list[str] = []
    for item in value:
        text = str(item or "").strip()
        if text:
            result.append(text)
    return result


def narrative_ops(payload: dict[str, Any]) -> dict[str, dict[str, list[str]]]:
    set_values = payload.get("set") if isinstance(payload.get("set"), dict) else {}
    append_values = payload.get("append") if isinstance(payload.get("append"), dict) else {}
    direct_set = {field: payload[field] for field in PROJECT_NARRATIVE_FIELDS if field in payload}
    set_payload = {**set_values, **direct_set}
    # Scalar `version` reconciliation: project_narrative may carry a single `version` string
    # (from `set.version` or a top-level `version`) to align PROJECT_STATE.version with the
    # authoritative protocol.config.json, via the state flow. It is not a narrative list-field.
    version = set_payload.pop("version", None)
    if version is None:
        version = payload.get("version")
    normalized: dict[str, Any] = {"set": {}, "append": {}}
    if version is not None:
        normalized["version"] = str(version)
    for mode, values in (("set", set_payload), ("append", append_values)):
        for field, raw in sorted(values.items()):
            if field not in PROJECT_NARRATIVE_FIELDS:
                raise IntentValidationError(f"unsupported project_narrative field: {field}")
            normalized[mode][field] = require_string_list(raw, f"project_narrative.{mode}.{field}")
    if not normalized["set"] and not normalized["append"] and "version" not in normalized:
        raise IntentValidationError("project_narrative requires set/append/version values")
    return normalized


def unique_text_list(value: Any, key: str) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in require_string_list(value or [], key):
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def mailbox_message_id(payload: dict[str, Any]) -> str:
    message_id = require_text(payload, "message_id")
    if "/" in message_id or "\\" in message_id or ".." in message_id or not MAILBOX_MESSAGE_ID_RE.fullmatch(message_id):
        raise IntentValidationError("mailbox_archive.message_id must be a safe MSG-* id")
    return message_id


def mailbox_archive_paths(message_id: str) -> tuple[str, str]:
    filename = f"{message_id}.md"
    return f"Area_comun/mailbox/open/{filename}", f"Area_comun/mailbox/archived/{filename}"


def mailbox_archive_path_status(root: Path, message_id: str) -> tuple[Path, Path, bool, bool]:
    open_relative, archived_relative = mailbox_archive_paths(message_id)
    open_path = root / open_relative
    archived_path = root / archived_relative
    return open_path, archived_path, open_path.exists(), archived_path.exists()


def mailbox_archive_accountability(payload: dict[str, Any]) -> dict[str, str]:
    author = require_text(payload, "author")
    relayed_by = require_text(payload, "relayed_by")
    endorsement = str(payload.get("endorsement") or "none").strip() or "none"
    return {"author": author, "relayed_by": relayed_by, "endorsement": endorsement}


def normalize_intent(intent: dict[str, Any]) -> dict[str, Any]:
    kind, payload = parse_intent(intent)
    common = {"kind": kind}
    if payload.get("idempotency_key"):
        common["idempotency_key"] = str(payload["idempotency_key"])

    if kind == "task_status":
        task_id = require_text(payload, "task_id")
        from_status = require_text(payload, "from")
        to_status = require_text(payload, "to")
        if from_status not in VALID_TASK_STATUSES:
            raise IntentValidationError(f"invalid task_status.from: {from_status}")
        if to_status not in VALID_TASK_STATUSES:
            raise IntentValidationError(f"invalid task_status.to: {to_status}")
        return {**common, "task_id": task_id, "from": from_status, "to": to_status}

    if kind == "task_upsert":
        task = payload.get("task") if isinstance(payload.get("task"), dict) else payload
        if not isinstance(task, dict):
            raise IntentValidationError("task_upsert requires a task object")
        task_id = str(task.get("id") or "").strip()
        if not task_id:
            raise IntentValidationError("task_upsert.task.id is required")
        task_copy = deepcopy(task)
        return {**common, "task_id": task_id, "task": task_copy}

    if kind == "claim":
        op = require_text(payload, "op")
        if op not in {"acquire", "release", "block"}:
            raise IntentValidationError("claim.op must be acquire, release or block")
        claim = payload.get("claim") if isinstance(payload.get("claim"), dict) else None
        claim_id = str((claim or payload).get("claim_id") or "").strip()
        if not claim_id:
            raise IntentValidationError("claim_id is required")
        normalized = {**common, "op": op, "claim_id": claim_id}
        if claim is not None:
            normalized["claim"] = deepcopy(claim)
            normalized["task_id"] = str(claim.get("task_id") or payload.get("task_id") or "").strip()
            normalized["owner"] = str(claim.get("owner") or payload.get("owner") or "").strip()
        else:
            for key in ("task_id", "owner", "status", "started_at", "updated_at", "expires_at", "notes"):
                if key in payload:
                    normalized[key] = payload[key]
            if isinstance(payload.get("scope"), list):
                normalized["scope"] = list(payload["scope"])
        return normalized

    if kind == "project_narrative":
        return {**common, **narrative_ops(payload)}

    if kind == "protocol_prune":
        task_ids = unique_text_list(payload.get("task_ids") or [], "protocol_prune.task_ids")
        active_task_ids = unique_text_list(payload.get("active_task_ids") or [], "protocol_prune.active_task_ids")
        claim_ids = unique_text_list(payload.get("claim_ids") or [], "protocol_prune.claim_ids")
        if not task_ids and not active_task_ids and not claim_ids:
            raise IntentValidationError("protocol_prune requires task_ids, active_task_ids, or claim_ids")
        return {**common, "task_ids": task_ids, "active_task_ids": active_task_ids, "claim_ids": claim_ids}

    if kind == "mailbox_archive":
        allowed = {"message_id", "author", "relayed_by", "endorsement", "idempotency_key"}
        unsupported = sorted(key for key in payload if key not in allowed)
        if unsupported:
            raise IntentValidationError(f"mailbox_archive contains unsupported fields: {', '.join(unsupported)}")
        return {
            **common,
            "message_id": mailbox_message_id(payload),
            **mailbox_archive_accountability(payload),
        }

    decision_id = str(payload.get("decision_id") or payload.get("id") or "").strip()
    if not decision_id:
        raise IntentValidationError("decision_id is required")
    return {**common, "decision_id": decision_id}


def idempotency_key(actor_id: str, normalized: dict[str, Any]) -> str:
    if normalized.get("idempotency_key"):
        return str(normalized["idempotency_key"])
    payload = {key: value for key, value in normalized.items() if key != "idempotency_key"}
    return f"intent:{actor_id}:{payload['kind']}:{canonical_hash(payload)}"


def aggregate_id_for(normalized: dict[str, Any]) -> str:
    if normalized.get("kind") == "project_narrative":
        return "PROJECT_STATE"
    if normalized.get("kind") == "protocol_prune":
        return "protocol-prune"
    for key in ("task_id", "decision_id", "claim_id", "message_id"):
        value = str(normalized.get(key) or "").strip()
        if value:
            return value
    return "protocol-state"


def event_payload_for(normalized: dict[str, Any], *, timestamp: str, commit: str | None = None) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "intent_type": normalized["kind"],
        "timestamp": timestamp,
        "transitions": {},
    }
    if commit:
        payload["commit"] = commit
    if normalized.get("task_id"):
        payload["task_id"] = normalized["task_id"]
    if normalized.get("message_id"):
        payload["message_id"] = normalized["message_id"]

    kind = normalized["kind"]
    if kind == "task_status":
        payload["transitions"]["task_status"] = {"from": normalized["from"], "to": normalized["to"]}
    elif kind == "task_upsert":
        task = deepcopy(normalized["task"])
        payload["task"] = task
        payload["transitions"]["task_upsert"] = {"task": task}
    elif kind == "claim":
        claim_transition = {key: deepcopy(value) for key, value in normalized.items() if key not in {"kind", "idempotency_key"}}
        payload["transitions"]["claims"] = [claim_transition]
    elif kind == "decision":
        payload["decision_id"] = normalized["decision_id"]
        payload["transitions"]["decision"] = {"decision_id": normalized["decision_id"]}
    elif kind == "project_narrative":
        transition = {
            key: deepcopy(normalized[key])
            for key in ("set", "append")
            if normalized.get(key)
        }
        if normalized.get("version"):
            transition["version"] = str(normalized["version"])
        payload["transitions"]["project_narrative"] = transition
    elif kind == "protocol_prune":
        transition = {
            key: deepcopy(normalized[key])
            for key in ("task_ids", "active_task_ids", "claim_ids")
            if normalized.get(key)
        }
        payload["transitions"]["protocol_prune"] = transition
    elif kind == "mailbox_archive":
        payload["transitions"]["mailbox_archive"] = {
            "message_id": normalized["message_id"],
            "from": "open",
            "to": "archived",
            "author": normalized["author"],
            "relayed_by": normalized["relayed_by"],
            "endorsement": normalized["endorsement"],
        }
    return payload


def transaction_idempotency_key(actor_id: str, normalized_intents: list[dict[str, Any]], explicit_key: str | None = None) -> str:
    if explicit_key:
        return str(explicit_key)
    payload = [{"key": idempotency_key(actor_id, normalized), "intent": normalized} for normalized in normalized_intents]
    return f"intent-tx:{actor_id}:{canonical_hash(payload)}"


def transaction_event_keys(actor_id: str, normalized_intents: list[dict[str, Any]]) -> list[str]:
    return [idempotency_key(actor_id, normalized) for normalized in normalized_intents]


def existing_events_for_keys(writer: EventWriter, keys: list[str]) -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    state_keys = writer.state().get("idempotency_keys", {})
    events = writer.events()
    for key in keys:
        seq = state_keys.get(key)
        if not seq:
            continue
        for event in events:
            if int(event.get("seq") or 0) == int(seq) and event.get("type") == "intent.applied":
                found = dict(event)
                found["deduped"] = True
                result[key] = found
                break
    return result


def protocol_state_view(state: dict[str, Any]) -> dict[str, Any]:
    view = deepcopy(state)
    if "project_state" not in view and isinstance(view.get("project"), dict):
        view["project_state"] = deepcopy(view["project"])
    return view


def advance_state_with_intent(
    state: dict[str, Any],
    normalized: dict[str, Any],
    *,
    actor_id: str,
    timestamp: str,
    commit: str | None,
) -> dict[str, Any]:
    updated = protocol_state_view(state)
    payload = event_payload_for(normalized, timestamp=timestamp, commit=commit)
    event = {
        "type": "intent.applied",
        "aggregate_id": aggregate_id_for(normalized),
        "actor": actor_id,
        "payload": payload,
        "applied": True,
        "seq": 0,
    }
    apply_intent_event(updated, event, payload)
    if isinstance(updated.get("project_state"), dict):
        updated["project"] = updated["project_state"]
    return updated


def validate_transaction(
    root: Path,
    actor_id: str,
    normalized_intents: list[dict[str, Any]],
    *,
    timestamp: str,
    commit: str | None,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    state = protocol_state_view(load_state(root))
    states_before: list[dict[str, Any]] = []
    for normalized in normalized_intents:
        state_before = deepcopy(state)
        validate_intent(root, actor_id, normalized, state_override=state_before)
        states_before.append(state_before)
        state = advance_state_with_intent(state_before, normalized, actor_id=actor_id, timestamp=timestamp, commit=commit)
    return state, states_before


def actor_enabled(registry: dict[str, Any], actor_id: str) -> bool:
    return any(
        isinstance(agent, dict) and agent.get("id") == actor_id and agent.get("enabled") is True
        for agent in registry.get("agents") or []
    )


def actor_has_any(registry: dict[str, Any], actor_id: str, capabilities: set[str]) -> bool:
    return any(has_capability(registry, actor_id, capability) for capability in capabilities)


def task_status_capability(normalized: dict[str, Any], state: dict[str, Any], actor_id: str) -> set[str]:
    from_status = str(normalized.get("from") or "")
    to_status = str(normalized.get("to") or "")
    task = tasks_by_id(state).get(normalized.get("task_id")) or {}
    actor_owns_task = task.get("owner") == actor_id
    if from_status == "in_review" and to_status in {"changes_requested", "review_approved", "qa_pending", "done"}:
        return {"reviewer"}
    if from_status == "qa_pending" and to_status in {"qa_failed", "architect_review", "done"}:
        return {"qa"}
    # DECISION-0032: the architect/orchestrator can advance/close ITS OWN analysis-tasks
    # (in_review/done/blocked) without an implementer/qa, since an analysis deliverable has no
    # separate implementer-vs-reviewer split. Only applies to type==analysis owned by the actor;
    # every other task type keeps requiring implementer below.
    task_type = str(task.get("type") or "")
    if task_type == "analysis" and actor_owns_task and to_status in {"in_review", "done", "blocked"}:
        return {"orchestrator", "architect"}
    if to_status in {"in_review", "done", "blocked"}:
        return {"implementer"}
    if to_status in {"ready", "claimed", "in_progress"} and actor_owns_task:
        return {"implementer", "orchestrator"}
    if to_status in {"ready", "claimed", "in_progress"}:
        return {"orchestrator"}
    return {"orchestrator"}


def claim_by_id(state: dict[str, Any], claim_id: str) -> dict[str, Any] | None:
    for claim in state.get("claims", {}).get("claims") or []:
        if isinstance(claim, dict) and claim.get("claim_id") == claim_id:
            return claim
    return None


def task_file_for(state: dict[str, Any], task_id: str) -> str | None:
    task = tasks_by_id(state).get(task_id) or {}
    value = str(task.get("file") or task.get("task_file") or "").strip()
    return normalized_path(value) if value else None


def required_scopes(normalized: dict[str, Any], state: dict[str, Any]) -> list[str]:
    kind = normalized["kind"]
    if kind in {"task_status", "task_upsert"}:
        task_id = str(normalized["task_id"])
        scopes = [
            f"Area_comun/state/TASK_INDEX.json#{task_id}",
            f"Area_comun/state/PROJECT_STATE.json#active_tasks/{task_id}",
        ]
        task_file = task_file_for(state, task_id)
        if task_file:
            scopes.append(task_file)
        return scopes
    if kind == "claim":
        return ["Area_comun/state/CLAIMS.json"]
    if kind == "decision":
        return ["Area_comun/state/PROJECT_STATE.json"]
    if kind == "project_narrative":
        return ["Area_comun/state/PROJECT_STATE.json"]
    if kind == "protocol_prune":
        scopes: list[str] = []
        if normalized.get("task_ids"):
            scopes.append("Area_comun/state/TASK_INDEX.json")
        if normalized.get("active_task_ids"):
            scopes.append("Area_comun/state/PROJECT_STATE.json")
        if normalized.get("claim_ids"):
            scopes.append("Area_comun/state/CLAIMS.json")
        return scopes
    if kind == "mailbox_archive":
        return list(mailbox_archive_paths(str(normalized.get("message_id") or "")))
    return []


def actor_claims_for_intent(state: dict[str, Any], actor_id: str, normalized: dict[str, Any]) -> list[dict[str, Any]]:
    claims = [claim for claim in active_claims(state) if claim.get("owner") == actor_id]
    task_id = str(normalized.get("task_id") or "")
    if task_id:
        matching = [claim for claim in claims if claim.get("task_id") == task_id]
        if matching:
            return matching
    return claims


def validate_scope_authority(state: dict[str, Any], actor_id: str, normalized: dict[str, Any]) -> None:
    if normalized["kind"] == "claim" and normalized["op"] == "acquire":
        owner = str(normalized.get("owner") or (normalized.get("claim") or {}).get("owner") or actor_id)
        if owner != actor_id:
            raise IntentValidationError("claim acquire owner must match actor_id")
        new_scope = [str(item) for item in normalized.get("scope") or (normalized.get("claim") or {}).get("scope") or []]
        for entry in new_scope:
            error = mailbox_claim_scope_error(entry)
            if error:
                raise IntentValidationError(error)
        for current in active_claims(state):
            if current.get("owner") == actor_id:
                continue
            for left in new_scope:
                for right in current.get("scope") or []:
                    if scopes_overlap(str(left), str(right)):
                        raise IntentValidationError(f"claim acquire overlaps active claim {current.get('claim_id')}: {left} / {right}")
        return

    required = required_scopes(normalized, state)
    claims = actor_claims_for_intent(state, actor_id, normalized)
    if not claims:
        raise IntentValidationError("no active claim for actor covers this intent")
    for required_entry in required:
        if not any(scope_covers(str(scope_entry), required_entry) for claim in claims for scope_entry in claim.get("scope") or []):
            raise IntentValidationError(f"write outside active claim scope: {required_entry}")


def validate_intent(root: Path, actor_id: str, normalized: dict[str, Any], state_override: dict[str, Any] | None = None) -> dict[str, Any]:
    registry = load_agent_registry(root)
    if not actor_enabled(registry, actor_id):
        raise IntentValidationError(f"actor not registered/enabled: {actor_id}")
    state = state_override if state_override is not None else load_state(root)
    kind = normalized["kind"]

    if kind == "task_status":
        required = task_status_capability(normalized, state, actor_id)
        if not actor_has_any(registry, actor_id, required):
            raise IntentValidationError(f"actor {actor_id} lacks required capability: {sorted(required)}")
        task = tasks_by_id(state).get(normalized["task_id"])
        if not task:
            raise IntentValidationError(f"task not found: {normalized['task_id']}")
        if task.get("status") != normalized["from"]:
            raise IntentValidationError(
                f"stale task_status.from for {normalized['task_id']}: expected {task.get('status')}, found {normalized['from']}"
            )
    elif kind == "task_upsert":
        if not actor_has_any(registry, actor_id, {"orchestrator"}):
            raise IntentValidationError(f"actor {actor_id} lacks required capability: orchestrator")
    elif kind == "project_narrative":
        if not actor_has_any(registry, actor_id, {"orchestrator"}):
            raise IntentValidationError(f"actor {actor_id} lacks required capability: orchestrator")
    elif kind == "protocol_prune":
        if not actor_has_any(registry, actor_id, {"orchestrator"}):
            raise IntentValidationError(f"actor {actor_id} lacks required capability: orchestrator")
        tasks = tasks_by_id(state)
        for task_id in normalized.get("task_ids") or []:
            task = tasks.get(task_id)
            if task and str(task.get("status") or "").lower() != "done":
                raise IntentValidationError(f"protocol_prune task is not done: {task_id}")
        project_doc = state.get("project_state") if isinstance(state.get("project_state"), dict) else state.get("project") or {}
        active_by_id = {
            item.get("id"): item
            for item in project_doc.get("active_tasks") or []
            if isinstance(item, dict) and item.get("id")
        }
        for task_id in normalized.get("active_task_ids") or []:
            task = active_by_id.get(task_id)
            if task and str(task.get("status") or "").lower() != "done":
                raise IntentValidationError(f"protocol_prune active task is not done: {task_id}")
        claims_by_id = {
            claim.get("claim_id"): claim
            for claim in state.get("claims", {}).get("claims") or []
            if isinstance(claim, dict) and claim.get("claim_id")
        }
        for claim_id in normalized.get("claim_ids") or []:
            claim = claims_by_id.get(claim_id)
            if claim and str(claim.get("status") or "").lower() != "released":
                raise IntentValidationError(f"protocol_prune claim is not released: {claim_id}")
    elif kind == "mailbox_archive":
        if not actor_has_any(registry, actor_id, {"orchestrator"}):
            raise IntentValidationError(f"actor {actor_id} lacks required capability: orchestrator")
        open_path, archived_path, open_exists, archived_exists = mailbox_archive_path_status(root, normalized["message_id"])
        mailbox_root = (root / "Area_comun" / "mailbox").resolve()
        for path in (open_path, archived_path):
            resolved = path.resolve()
            if resolved != mailbox_root and mailbox_root not in resolved.parents:
                raise IntentValidationError("mailbox_archive path escapes Area_comun/mailbox")
        if not open_exists and not archived_exists:
            raise IntentValidationError(f"mailbox message not found in open or archived: {normalized['message_id']}")
    elif kind == "claim":
        if not actor_has_any(registry, actor_id, {"implementer", "orchestrator", "reviewer"}):
            raise IntentValidationError(f"actor {actor_id} lacks required claim capability")
        existing = claim_by_id(state, normalized["claim_id"])
        if normalized["op"] == "acquire":
            if existing and existing.get("status") == "active":
                raise IntentValidationError(f"claim already active: {normalized['claim_id']}")
            claim = normalized.get("claim") if isinstance(normalized.get("claim"), dict) else normalized
            if not str(claim.get("task_id") or "").strip():
                raise IntentValidationError("claim acquire requires task_id")
            if not str(claim.get("owner") or actor_id).strip():
                raise IntentValidationError("claim acquire requires owner")
        else:
            if not existing:
                raise IntentValidationError(f"claim not found: {normalized['claim_id']}")
            if existing.get("owner") != actor_id and not actor_has_any(registry, actor_id, {"orchestrator"}):
                raise IntentValidationError("only the claim owner or an orchestrator can release/block a claim")
    elif kind == "decision":
        if not actor_has_any(registry, actor_id, {"orchestrator", "human_owner"}):
            raise IntentValidationError(f"actor {actor_id} lacks required decision capability")

    validate_scope_authority(state, actor_id, normalized)
    return state


def ensure_actor_enabled(root: Path, actor_id: str) -> None:
    registry = load_agent_registry(root)
    if not actor_enabled(registry, actor_id):
        raise IntentValidationError(f"actor not registered/enabled: {actor_id}")


def ensure_event_state_config_valid(root: Path) -> None:
    config_path = root.resolve() / "protocol.config.json"
    if not config_path.exists():
        return
    error = event_state_config_error(read_json(config_path))
    if error:
        raise IntentValidationError(f"invalid event_state config: {error}")


def existing_idempotent_event(writer: EventWriter, key: str) -> dict[str, Any] | None:
    seq = writer.state().get("idempotency_keys", {}).get(key)
    if not seq:
        return None
    for event in writer.events():
        if int(event.get("seq") or 0) == int(seq) and event.get("type") == "intent.applied":
            result = dict(event)
            result["deduped"] = True
            return result
    return None


def protocol_file_paths() -> list[str]:
    return [path.as_posix() for path in PROTOCOL_STATE_PATHS.values()]


def set_task_file_status(root: Path, relative: str, status: str) -> None:
    path = root / relative
    if not path.exists():
        return
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines(keepends=True)
    for index, line in enumerate(lines):
        if line.startswith("status:"):
            suffix = "\n" if line.endswith("\n") else ""
            lines[index] = f"status: {status}{suffix}"
            path.write_text("".join(lines), encoding="utf-8", newline="")
            return
    raise IntentApplyError(f"task file has no status field: {relative}")


def set_mailbox_file_status(path: Path, status: str, relative: str) -> None:
    text = path.read_text(encoding="utf-8-sig")
    lines = text.splitlines(keepends=True)
    for index, line in enumerate(lines):
        if line.startswith("status:"):
            suffix = "\n" if line.endswith("\n") else ""
            lines[index] = f"status: {status}{suffix}"
            path.write_text("".join(lines), encoding="utf-8", newline="")
            return
    raise IntentApplyError(f"mailbox message has no status field: {relative}")


def apply_task_file_side_effects(root: Path, normalized: dict[str, Any], state_before: dict[str, Any]) -> list[str]:
    if normalized["kind"] == "task_status":
        relative = task_file_for(state_before, normalized["task_id"])
        if relative:
            set_task_file_status(root, relative, normalized["to"])
            return [relative]
    if normalized["kind"] == "task_upsert":
        task = normalized.get("task") or {}
        relative = normalized_path(str(task.get("file") or task_file_for(state_before, normalized["task_id"]) or ""))
        status = str(task.get("status") or "").strip()
        if relative and status:
            set_task_file_status(root, relative, status)
            return [relative]
    return []


def apply_mailbox_side_effects(root: Path, normalized: dict[str, Any]) -> list[str]:
    if normalized["kind"] != "mailbox_archive":
        return []
    open_relative, archived_relative = mailbox_archive_paths(normalized["message_id"])
    open_path = root / open_relative
    archived_path = root / archived_relative
    if archived_path.exists() and open_path.exists():
        raise IntentApplyError(f"mailbox message exists in both open and archived: {normalized['message_id']}")
    if archived_path.exists() and not open_path.exists():
        set_mailbox_file_status(archived_path, "archived", archived_relative)
        return [archived_relative]
    if not open_path.exists():
        raise IntentApplyError(f"mailbox message not found in open: {normalized['message_id']}")
    archived_path.parent.mkdir(parents=True, exist_ok=True)
    set_mailbox_file_status(open_path, "archived", open_relative)
    open_path.replace(archived_path)
    return [open_relative, archived_relative]


def apply_file_side_effects(root: Path, normalized: dict[str, Any], state_before: dict[str, Any]) -> list[str]:
    updated = apply_task_file_side_effects(root, normalized, state_before)
    updated.extend(apply_mailbox_side_effects(root, normalized))
    return list(dict.fromkeys(updated))


def task_files_for_backup(normalized: dict[str, Any], state_before: dict[str, Any]) -> list[str]:
    paths: list[str] = []
    task_id = str(normalized.get("task_id") or "")
    if task_id:
        existing = task_file_for(state_before, task_id)
        if existing:
            paths.append(existing)
    if normalized["kind"] == "task_upsert":
        task = normalized.get("task") or {}
        declared = normalized_path(str(task.get("file") or ""))
        if declared:
            paths.append(declared)
    return list(dict.fromkeys(paths))


def mailbox_files_for_backup(normalized: dict[str, Any]) -> list[str]:
    if normalized["kind"] == "mailbox_archive":
        return list(mailbox_archive_paths(normalized["message_id"]))
    return []


def files_for_backup(normalized: dict[str, Any], state_before: dict[str, Any]) -> list[str]:
    return list(dict.fromkeys([*task_files_for_backup(normalized, state_before), *mailbox_files_for_backup(normalized)]))


def ensure_clean_replay_base(root: Path, events: list[dict[str, Any]]) -> None:
    if not has_protocol_genesis(events):
        return
    drift = protocol_state_drift(root)
    if drift.get("has_drift"):
        paths = ", ".join(str(item.get("path") or "<unknown>") for item in drift.get("entries") or [])
        raise IntentApplyError(f"protocol state drift exists before submit_intent: {paths}; write a fresh genesis first")


def submit_intent(
    root: Path,
    actor_id: str,
    intent: dict[str, Any],
    *,
    timestamp: str,
    commit: str | None = None,
    fail_after_writes: int | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    actor_id = str(actor_id or "").strip()
    timestamp = str(timestamp or "").strip()
    if not actor_id:
        raise IntentValidationError("actor_id is required")
    if not timestamp:
        raise IntentValidationError("timestamp is required")

    ensure_event_state_config_valid(root)
    normalized = normalize_intent(intent)
    ensure_actor_enabled(root, actor_id)
    writer = EventWriter(root)
    key = idempotency_key(actor_id, normalized)
    existing = existing_idempotent_event(writer, key)
    if existing is not None:
        state_before = load_state(root)
        file_backup = snapshot_files(root, [*protocol_file_paths(), *files_for_backup(normalized, state_before)])
        runtime_backup = snapshot_runtime_state(root)
        try:
            materialization = materialize_to_disk(root, current_protocol_snapshot(root), fail_after_writes=fail_after_writes)
            task_files_updated = apply_file_side_effects(root, normalized, state_before)
            runtime_snapshot = writer.write_snapshot()
            drift_after = protocol_state_drift(root)
            if drift_after.get("has_drift"):
                raise IntentApplyError(f"protocol state drift remains after submit_intent retry: {drift_after.get('entries')}")
            cleanup_runtime_state_backup(runtime_backup)
            return {
                "applied": True,
                "deduped": True,
                "event": existing,
                "genesis_event": None,
                "intent": normalized,
                "materialization": materialization,
                "runtime_snapshot": {"up_to_seq": runtime_snapshot.get("up_to_seq")},
                "task_files_updated": task_files_updated,
                "drift": drift_after,
            }
        except Exception as exc:
            restore_files(root, file_backup)
            restore_runtime_state(root, runtime_backup)
            if isinstance(exc, IntentError):
                raise
            raise IntentApplyError(str(exc)) from exc

    state_before = validate_intent(root, actor_id, normalized)
    file_backup = snapshot_files(root, [*protocol_file_paths(), *files_for_backup(normalized, state_before)])
    runtime_backup = snapshot_runtime_state(root)
    try:
        events_before = writer.events()
        ensure_clean_replay_base(root, events_before)
        genesis_result = None
        if not has_protocol_genesis(events_before):
            genesis_result = write_genesis_reference(
                root,
                actor_id=actor_id,
                timestamp=timestamp,
                commit=commit,
                idempotency_key=f"protocol-state:genesis-ref:{actor_id}:{timestamp}",
            )
            writer = EventWriter(root)

        payload = event_payload_for(normalized, timestamp=timestamp, commit=commit)
        event = writer.append_event(
            event_type="intent.applied",
            aggregate_id=aggregate_id_for(normalized),
            actor_id=actor_id,
            idempotency_key=key,
            payload=payload,
            ts=timestamp,
        )
        snapshot = current_protocol_snapshot(root)
        materialization = materialize_to_disk(root, snapshot, fail_after_writes=fail_after_writes)
        task_files_updated = apply_file_side_effects(root, normalized, state_before)
        runtime_snapshot = writer.write_snapshot()
        drift_after = protocol_state_drift(root)
        if drift_after.get("has_drift"):
            raise IntentApplyError(f"protocol state drift remains after submit_intent: {drift_after.get('entries')}")
        cleanup_runtime_state_backup(runtime_backup)
        return {
            "applied": True,
            "event": event,
            "genesis_event": (genesis_result or {}).get("event"),
            "intent": normalized,
            "materialization": materialization,
            "runtime_snapshot": {"up_to_seq": runtime_snapshot.get("up_to_seq")},
            "task_files_updated": task_files_updated,
            "drift": drift_after,
        }
    except Exception as exc:
        restore_files(root, file_backup)
        restore_runtime_state(root, runtime_backup)
        if isinstance(exc, IntentError):
            raise
        raise IntentApplyError(str(exc)) from exc


def submit_intents(
    root: Path,
    actor_id: str,
    intents: list[dict[str, Any]],
    *,
    timestamp: str,
    commit: str | None = None,
    transaction_key: str | None = None,
    fail_after_writes: int | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    actor_id = str(actor_id or "").strip()
    timestamp = str(timestamp or "").strip()
    if not actor_id:
        raise IntentValidationError("actor_id is required")
    if not timestamp:
        raise IntentValidationError("timestamp is required")
    if not intents:
        raise IntentValidationError("transaction requires at least one intent")

    ensure_event_state_config_valid(root)
    normalized_intents = [normalize_intent(intent) for intent in intents]
    keys = transaction_event_keys(actor_id, normalized_intents)
    if len(set(keys)) != len(keys):
        raise IntentValidationError("transaction contains duplicate intent idempotency keys")
    tx_key = transaction_idempotency_key(actor_id, normalized_intents, transaction_key)
    ensure_actor_enabled(root, actor_id)
    writer = EventWriter(root)
    existing = existing_events_for_keys(writer, keys)
    if existing:
        if len(existing) != len(keys):
            raise IntentApplyError("partial transaction idempotency state exists; refusing to continue")
        state_before = load_state(root)
        side_effect_paths: list[str] = []
        for normalized in normalized_intents:
            side_effect_paths.extend(files_for_backup(normalized, state_before))
        file_backup = snapshot_files(root, [*protocol_file_paths(), *side_effect_paths])
        runtime_backup = snapshot_runtime_state(root)
        try:
            materialization = materialize_to_disk(root, current_protocol_snapshot(root), fail_after_writes=fail_after_writes)
            task_files_updated: list[str] = []
            for normalized in normalized_intents:
                task_files_updated.extend(apply_file_side_effects(root, normalized, state_before))
            runtime_snapshot = writer.write_snapshot()
            drift_after = protocol_state_drift(root)
            if drift_after.get("has_drift"):
                raise IntentApplyError(f"protocol state drift remains after submit_intents retry: {drift_after.get('entries')}")
            cleanup_runtime_state_backup(runtime_backup)
            return {
                "applied": True,
                "deduped": True,
                "transaction": {
                    "idempotency_key": tx_key,
                    "intent_count": len(normalized_intents),
                    "event_keys": keys,
                },
                "events": [existing[key] for key in keys],
                "genesis_event": None,
                "intents": normalized_intents,
                "materialization": materialization,
                "runtime_snapshot": {"up_to_seq": runtime_snapshot.get("up_to_seq")},
                "task_files_updated": list(dict.fromkeys(task_files_updated)),
                "drift": drift_after,
            }
        except Exception as exc:
            restore_files(root, file_backup)
            restore_runtime_state(root, runtime_backup)
            if isinstance(exc, IntentError):
                raise
            raise IntentApplyError(str(exc)) from exc

    _, states_before = validate_transaction(root, actor_id, normalized_intents, timestamp=timestamp, commit=commit)
    task_file_paths: list[str] = []
    for normalized, state_before in zip(normalized_intents, states_before):
        task_file_paths.extend(files_for_backup(normalized, state_before))
    file_backup = snapshot_files(root, [*protocol_file_paths(), *task_file_paths])
    runtime_backup = snapshot_runtime_state(root)
    try:
        events_before = writer.events()
        ensure_clean_replay_base(root, events_before)
        genesis_result = None
        if not has_protocol_genesis(events_before):
            genesis_result = write_genesis_reference(
                root,
                actor_id=actor_id,
                timestamp=timestamp,
                commit=commit,
                idempotency_key=f"protocol-state:genesis-ref:{actor_id}:{timestamp}",
            )
            writer = EventWriter(root)

        events: list[dict[str, Any]] = []
        for index, normalized in enumerate(normalized_intents, start=1):
            payload = event_payload_for(normalized, timestamp=timestamp, commit=commit)
            payload["transaction"] = {
                "idempotency_key": tx_key,
                "index": index,
                "count": len(normalized_intents),
            }
            events.append(
                writer.append_event(
                    event_type="intent.applied",
                    aggregate_id=aggregate_id_for(normalized),
                    actor_id=actor_id,
                    idempotency_key=keys[index - 1],
                    payload=payload,
                    ts=timestamp,
                )
            )

        snapshot = current_protocol_snapshot(root)
        materialization = materialize_to_disk(root, snapshot, fail_after_writes=fail_after_writes)
        task_files_updated: list[str] = []
        for normalized, state_before in zip(normalized_intents, states_before):
            task_files_updated.extend(apply_file_side_effects(root, normalized, state_before))
        runtime_snapshot = writer.write_snapshot()
        drift_after = protocol_state_drift(root)
        if drift_after.get("has_drift"):
            raise IntentApplyError(f"protocol state drift remains after submit_intents: {drift_after.get('entries')}")
        cleanup_runtime_state_backup(runtime_backup)
        return {
            "applied": True,
            "events": events,
            "genesis_event": (genesis_result or {}).get("event"),
            "transaction": {
                "idempotency_key": tx_key,
                "intent_count": len(normalized_intents),
                "event_keys": keys,
            },
            "intents": normalized_intents,
            "materialization": materialization,
            "runtime_snapshot": {"up_to_seq": runtime_snapshot.get("up_to_seq")},
            "task_files_updated": list(dict.fromkeys(task_files_updated)),
            "drift": drift_after,
        }
    except Exception as exc:
        restore_files(root, file_backup)
        restore_runtime_state(root, runtime_backup)
        if isinstance(exc, IntentError):
            raise
        raise IntentApplyError(str(exc)) from exc


def load_intent_from_args(args: argparse.Namespace) -> dict[str, Any]:
    if args.intent_json:
        payload = json.loads(args.intent_json)
    elif args.intent:
        if args.intent == "-":
            payload = json.loads(sys.stdin.read())
        else:
            payload = read_json(Path(args.intent))
    else:
        raise IntentValidationError("--intent or --intent-json is required")
    if not isinstance(payload, dict):
        raise IntentValidationError("intent JSON must be an object")
    return payload


def load_transaction_from_args(args: argparse.Namespace) -> dict[str, Any]:
    if args.intents_json:
        payload = json.loads(args.intents_json)
    elif args.intents:
        if args.intents == "-":
            payload = json.loads(sys.stdin.read())
        else:
            payload = read_json(Path(args.intents))
    else:
        raise IntentValidationError("--intents or --intents-json is required")
    if not isinstance(payload, dict):
        raise IntentValidationError("transaction JSON must be an object")
    intents = payload.get("intents")
    if not isinstance(intents, list) or not all(isinstance(item, dict) for item in intents):
        raise IntentValidationError("transaction JSON requires intents: [object, ...]")
    return payload


def main() -> int:
    parser = argparse.ArgumentParser(description="Submit protocol-state intents through the runtime event log.")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--actor-id")
    parser.add_argument("--timestamp")
    parser.add_argument("--commit")
    parser.add_argument("--intent", help="Path to an intent JSON file, or '-' for stdin.")
    parser.add_argument("--intent-json", help="Inline intent JSON.")
    parser.add_argument("--intents", help="Path to a transaction JSON file, or '-' for stdin.")
    parser.add_argument("--intents-json", help="Inline transaction JSON.")
    parser.add_argument("--output", default="-", help="Output JSON path, or '-' for stdout.")
    args = parser.parse_args()

    try:
        if args.intents or args.intents_json:
            envelope = load_transaction_from_args(args)
            result = submit_intents(
                Path(args.root),
                args.actor_id or str(envelope.get("actor_id") or ""),
                [item for item in envelope["intents"] if isinstance(item, dict)],
                timestamp=args.timestamp or str(envelope.get("timestamp") or ""),
                commit=args.commit if args.commit is not None else (str(envelope.get("commit") or "") or None),
                transaction_key=str(envelope.get("idempotency_key") or envelope.get("transaction_idempotency_key") or "") or None,
            )
        else:
            result = submit_intent(
                Path(args.root),
                str(args.actor_id or ""),
                load_intent_from_args(args),
                timestamp=str(args.timestamp or ""),
                commit=args.commit,
            )
    except IntentError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    text = canonical_json_text(result)
    if args.output == "-":
        print(text, end="")
    else:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="ascii", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
