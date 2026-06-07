#!/usr/bin/env python3
"""Write a fresh protocol-state genesis reference from the current hot state."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

try:
    from .eventlog import EventWriter, canonical_hash
    from .protocol_replay import build_genesis_snapshot, protocol_state_drift, write_genesis_reference
except ImportError:  # pragma: no cover - direct script execution
    from eventlog import EventWriter, canonical_hash
    from protocol_replay import build_genesis_snapshot, protocol_state_drift, write_genesis_reference


class RegenesisError(RuntimeError):
    pass


def canonical_json_text(payload: dict[str, Any]) -> str:
    return json.dumps(payload, indent=4, ensure_ascii=True, sort_keys=True) + "\n"


def default_idempotency_key(actor_id: str, timestamp: str, hot_snapshot: dict[str, Any]) -> str:
    payload = {
        "actor_id": actor_id,
        "timestamp": timestamp,
        "hot_hash": hot_snapshot.get("canonical_hash"),
    }
    return f"protocol-state:regenesis-ref:{canonical_hash(payload)}"


def regenesis(
    root: Path,
    *,
    actor_id: str,
    timestamp: str,
    commit: str | None = None,
    idempotency_key: str | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    actor_id = str(actor_id or "").strip()
    timestamp = str(timestamp or "").strip()
    if not actor_id:
        raise RegenesisError("actor_id is required")
    if not timestamp:
        raise RegenesisError("timestamp is required")
    drift_before = protocol_state_drift(root)
    hot_snapshot = build_genesis_snapshot(root)
    key = idempotency_key or default_idempotency_key(actor_id, timestamp, hot_snapshot)
    result = write_genesis_reference(
        root,
        actor_id=actor_id,
        timestamp=timestamp,
        commit=commit,
        idempotency_key=key,
    )
    runtime_snapshot = EventWriter(root).write_snapshot()
    drift_after = protocol_state_drift(root)
    if drift_after.get("has_drift"):
        raise RegenesisError(f"protocol state drift remains after regenesis: {drift_after.get('entries')}")
    return {
        "schema_version": "protocol_regenesis.v1",
        "applied": True,
        "deduped": bool((result.get("event") or {}).get("deduped")),
        "event": result.get("event"),
        "snapshot_ref": result.get("snapshot_ref"),
        "snapshot_path": Path(result["snapshot_path"]).relative_to(root).as_posix(),
        "runtime_snapshot": {"up_to_seq": runtime_snapshot.get("up_to_seq")},
        "drift_before": drift_before,
        "drift_after": drift_after,
        "history_preserved": True,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Write a fresh protocol-state genesis reference from hot state.")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--actor-id", required=True)
    parser.add_argument("--timestamp", required=True)
    parser.add_argument("--commit")
    parser.add_argument("--idempotency-key")
    parser.add_argument("--output", default="-", help="Output JSON path, or '-' for stdout.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        result = regenesis(
            Path(args.root),
            actor_id=args.actor_id,
            timestamp=args.timestamp,
            commit=args.commit,
            idempotency_key=args.idempotency_key,
        )
    except RegenesisError as exc:
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
