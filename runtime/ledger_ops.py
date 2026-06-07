#!/usr/bin/env python3
"""Build common protocol ledger transactions for submit_intent --intents."""

from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from pathlib import Path
from typing import Any

try:
    from .submit_intent import submit_intents
except ImportError:  # pragma: no cover - direct script execution
    from submit_intent import submit_intents


SCHEMA_VERSION = "protocol_ledger_ops.v1"
AUTO_CLAIM = "auto-claim"
HANDOFF_RELEASE = "handoff-release"


class LedgerOpsError(RuntimeError):
    pass


def canonical_json_text(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=4, ensure_ascii=True, sort_keys=True) + "\n"


def require_text(value: str | None, name: str) -> str:
    text = str(value or "").strip()
    if not text:
        raise LedgerOpsError(f"{name} is required")
    return text


def normalized_scope(scope: list[str] | tuple[str, ...]) -> list[str]:
    normalized: list[str] = []
    for item in scope:
        text = str(item or "").replace("\\", "/").strip()
        if text and text not in normalized:
            normalized.append(text)
    return normalized


def ledger_key(operation: str, task_id: str, claim_id: str, suffix: str) -> str:
    return f"ledger-op:{operation}:{task_id}:{claim_id}:{suffix}"


def transaction_key(operation: str, task_id: str, claim_id: str) -> str:
    return ledger_key(operation, task_id, claim_id, "tx")


def task_status_intent(
    *,
    task_id: str,
    from_status: str,
    to_status: str,
    idempotency_key: str,
) -> dict[str, Any]:
    return {
        "task_status": {
            "from": require_text(from_status, "from_status"),
            "idempotency_key": require_text(idempotency_key, "idempotency_key"),
            "task_id": require_text(task_id, "task_id"),
            "to": require_text(to_status, "to_status"),
        }
    }


def claim_acquire_intent(
    *,
    claim_id: str,
    task_id: str,
    owner: str,
    scope: list[str],
    started_at: str,
    updated_at: str,
    expires_at: str,
    notes: str,
    idempotency_key: str,
) -> dict[str, Any]:
    clean_scope = normalized_scope(scope)
    if not clean_scope:
        raise LedgerOpsError("scope requires at least one path")
    claim = {
        "claim_id": require_text(claim_id, "claim_id"),
        "expires_at": require_text(expires_at, "expires_at"),
        "notes": str(notes or ""),
        "owner": require_text(owner, "owner"),
        "scope": clean_scope,
        "started_at": require_text(started_at, "started_at"),
        "status": "active",
        "task_id": require_text(task_id, "task_id"),
        "updated_at": require_text(updated_at, "updated_at"),
    }
    return {
        "claim": {
            "claim": claim,
            "idempotency_key": require_text(idempotency_key, "idempotency_key"),
            "op": "acquire",
        }
    }


def claim_release_intent(*, claim_id: str, idempotency_key: str) -> dict[str, Any]:
    return {
        "claim": {
            "claim_id": require_text(claim_id, "claim_id"),
            "idempotency_key": require_text(idempotency_key, "idempotency_key"),
            "op": "release",
        }
    }


def task_upsert_intent(*, task: dict[str, Any], idempotency_key: str) -> dict[str, Any]:
    if not isinstance(task, dict):
        raise LedgerOpsError("task_upsert requires a task object")
    task_id = require_text(str(task.get("id") or ""), "task.id")
    return {
        "task_upsert": {
            "idempotency_key": require_text(idempotency_key, "idempotency_key"),
            "task": {**deepcopy(task), "id": task_id},
        }
    }


def envelope(
    *,
    operation: str,
    actor_id: str,
    timestamp: str,
    commit: str | None,
    task_id: str,
    claim_id: str,
    intents: list[dict[str, Any]],
) -> dict[str, Any]:
    operation = require_text(operation, "operation")
    task_id = require_text(task_id, "task_id")
    claim_id = require_text(claim_id, "claim_id")
    if not intents:
        raise LedgerOpsError("envelope requires at least one intent")
    payload: dict[str, Any] = {
        "actor_id": require_text(actor_id, "actor_id"),
        "idempotency_key": transaction_key(operation, task_id, claim_id),
        "intents": intents,
        "operation": operation,
        "schema_version": SCHEMA_VERSION,
        "task_id": task_id,
        "timestamp": require_text(timestamp, "timestamp"),
    }
    if commit:
        payload["commit"] = str(commit)
    return payload


def auto_claim_envelope(
    *,
    actor_id: str,
    timestamp: str,
    task_id: str,
    claim_id: str,
    scope: list[str],
    expires_at: str,
    commit: str | None = None,
    owner: str | None = None,
    from_status: str = "ready",
    to_status: str = "in_progress",
    started_at: str | None = None,
    updated_at: str | None = None,
    notes: str = "Acquired via submit_intent --intents ledger operation.",
) -> dict[str, Any]:
    task_id = require_text(task_id, "task_id")
    claim_id = require_text(claim_id, "claim_id")
    actor_id = require_text(actor_id, "actor_id")
    timestamp = require_text(timestamp, "timestamp")
    owner = require_text(owner or actor_id, "owner")
    intents = [
        claim_acquire_intent(
            claim_id=claim_id,
            task_id=task_id,
            owner=owner,
            scope=scope,
            started_at=started_at or timestamp,
            updated_at=updated_at or timestamp,
            expires_at=expires_at,
            notes=notes,
            idempotency_key=ledger_key(AUTO_CLAIM, task_id, claim_id, "claim-acquire"),
        ),
        task_status_intent(
            task_id=task_id,
            from_status=from_status,
            to_status=to_status,
            idempotency_key=ledger_key(AUTO_CLAIM, task_id, claim_id, "task-status"),
        ),
    ]
    return envelope(
        operation=AUTO_CLAIM,
        actor_id=actor_id,
        timestamp=timestamp,
        commit=commit,
        task_id=task_id,
        claim_id=claim_id,
        intents=intents,
    )


def handoff_release_envelope(
    *,
    actor_id: str,
    timestamp: str,
    task_id: str,
    claim_id: str,
    commit: str | None = None,
    from_status: str = "in_progress",
    to_status: str = "in_review",
    task_upserts: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    task_id = require_text(task_id, "task_id")
    claim_id = require_text(claim_id, "claim_id")
    intents = [
        task_status_intent(
            task_id=task_id,
            from_status=from_status,
            to_status=to_status,
            idempotency_key=ledger_key(HANDOFF_RELEASE, task_id, claim_id, "task-status"),
        )
    ]
    for index, task in enumerate(task_upserts or [], start=1):
        upsert_task_id = require_text(str(task.get("id") or ""), "task.id")
        intents.append(
            task_upsert_intent(
                task=task,
                idempotency_key=ledger_key(HANDOFF_RELEASE, task_id, claim_id, f"task-upsert-{index}-{upsert_task_id}"),
            )
        )
    intents.append(
        claim_release_intent(
            claim_id=claim_id,
            idempotency_key=ledger_key(HANDOFF_RELEASE, task_id, claim_id, "claim-release"),
        )
    )
    return envelope(
        operation=HANDOFF_RELEASE,
        actor_id=actor_id,
        timestamp=timestamp,
        commit=commit,
        task_id=task_id,
        claim_id=claim_id,
        intents=intents,
    )


def submit_envelope(root: Path, payload: dict[str, Any], *, fail_after_writes: int | None = None) -> dict[str, Any]:
    intents = payload.get("intents")
    if not isinstance(intents, list) or not all(isinstance(item, dict) for item in intents):
        raise LedgerOpsError("envelope requires intents: [object, ...]")
    commit = str(payload.get("commit") or "") or None
    return submit_intents(
        Path(root),
        require_text(str(payload.get("actor_id") or ""), "actor_id"),
        intents,
        timestamp=require_text(str(payload.get("timestamp") or ""), "timestamp"),
        commit=commit,
        transaction_key=str(payload.get("idempotency_key") or payload.get("transaction_idempotency_key") or "") or None,
        fail_after_writes=fail_after_writes,
    )


def parse_task_upserts(values: list[str] | None) -> list[dict[str, Any]]:
    tasks: list[dict[str, Any]] = []
    for raw in values or []:
        payload = json.loads(raw)
        if isinstance(payload, list):
            items = payload
        else:
            items = [payload]
        for item in items:
            if not isinstance(item, dict):
                raise LedgerOpsError("--task-upsert-json entries must be JSON objects")
            tasks.append(item)
    return tasks


def build_from_args(args: argparse.Namespace) -> dict[str, Any]:
    if args.operation == AUTO_CLAIM:
        return auto_claim_envelope(
            actor_id=args.actor_id,
            timestamp=args.timestamp,
            commit=args.commit,
            task_id=args.task_id,
            claim_id=args.claim_id,
            scope=args.scope or [],
            expires_at=args.expires_at,
            owner=args.owner or None,
            from_status=args.from_status or "ready",
            to_status=args.to_status or "in_progress",
            started_at=args.started_at or None,
            updated_at=args.updated_at or None,
            notes=args.notes or "Acquired via submit_intent --intents ledger operation.",
        )
    if args.operation == HANDOFF_RELEASE:
        return handoff_release_envelope(
            actor_id=args.actor_id,
            timestamp=args.timestamp,
            commit=args.commit,
            task_id=args.task_id,
            claim_id=args.claim_id,
            from_status=args.from_status or "in_progress",
            to_status=args.to_status or "in_review",
            task_upserts=parse_task_upserts(args.task_upsert_json),
        )
    raise LedgerOpsError(f"unsupported operation: {args.operation}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build Codex-loop ledger operation envelopes.")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--operation", required=True, choices=[AUTO_CLAIM, HANDOFF_RELEASE])
    parser.add_argument("--actor-id", required=True)
    parser.add_argument("--timestamp", required=True)
    parser.add_argument("--commit")
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--claim-id", required=True)
    parser.add_argument("--from-status")
    parser.add_argument("--to-status")
    parser.add_argument("--scope", action="append", default=[])
    parser.add_argument("--owner")
    parser.add_argument("--expires-at")
    parser.add_argument("--started-at")
    parser.add_argument("--updated-at")
    parser.add_argument("--notes")
    parser.add_argument("--task-upsert-json", action="append", default=[])
    parser.add_argument("--submit", action="store_true")
    parser.add_argument("--output", default="-", help="Output JSON path, or '-' for stdout.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        payload = build_from_args(args)
        result = submit_envelope(Path(args.root), payload) if args.submit else payload
    except (LedgerOpsError, json.JSONDecodeError) as exc:
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
