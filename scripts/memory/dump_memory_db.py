#!/usr/bin/env python3
"""Emit the byte-stable canonical dump of the derived memory DB partition."""

from __future__ import annotations

import argparse
import json
import sqlite3
from pathlib import Path
from typing import Any


DB_PATH = Path("runtime/memory/index.db")
# Changing this identifier intentionally invalidates earlier canonical dumps.
DUMP_FORMAT = "protocol-memory-derived-v1"

# SPEC-MEMORIA-HIBRIDA v0.2.1 s.6. Operational tables and columns are
# deliberately absent. Column order is part of the dump contract.
DERIVED_COLUMNS: dict[str, tuple[str, ...]] = {
    "artifacts": (
        "artifact_id", "artifact_type", "title", "status", "original_path",
        "hot_path", "cold_path", "git_commit", "sha256", "created_at",
        "updated_at", "closed_at", "owner", "project", "is_active_policy",
        "is_hot", "summary_short", "summary_long", "canonicality",
        "retention_class", "cold_reason", "schema_version",
    ),
    "artifact_edges": (
        "from_artifact_id", "to_artifact_id", "edge_type", "source_path",
        "source_commit",
    ),
    "agent_memory": (
        "memory_id", "agent_id", "scope", "summary", "source_path",
        "source_commit", "event_seq", "sha256", "valid_from", "valid_until",
        "is_current",
    ),
    "policy_status": (
        "decision_id", "policy_state", "superseded_by", "supersedes",
        "active_from", "active_until", "applies_to", "hot_required", "reason",
    ),
    "stubs": (
        "stub_id", "artifact_id", "stub_path", "original_path", "cold_path",
        "git_commit", "sha256", "summary", "rehydration_command", "created_at",
    ),
    "cold_packs": (
        "pack_id", "pack_type", "path", "git_ref", "created_at",
        "sha256_manifest", "artifact_count",
    ),
    "search_terms": ("artifact_id", "term", "field", "weight", "source"),
    "hot_cold_rules": (
        "rule_id", "artifact_type", "selector", "target_retention_class",
        "window_days", "window_count", "requires_stub",
        "requires_active_policy_check", "enabled", "created_by_decision",
    ),
    "artifact_versions": (
        "artifact_id", "version_id", "git_commit", "event_seq",
        "path_at_commit", "sha256", "changed_at", "changed_by", "change_kind",
        "status_at_version",
    ),
    "artifact_content_index": (
        "artifact_id", "content_sha256", "language", "token_estimate",
        "line_count", "has_frontmatter", "frontmatter_json",
    ),
}


def quoted(identifier: str) -> str:
    if not identifier.replace("_", "").isalnum():
        raise ValueError(f"unsafe SQLite identifier: {identifier}")
    return f'"{identifier}"'


def canonical_payload(connection: sqlite3.Connection) -> dict[str, Any]:
    if connection.execute("PRAGMA user_version").fetchone()[0] != 1:
        raise ValueError("memory DB schema version must be 1")
    table_names = {
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table'"
        )
    }
    missing = set(DERIVED_COLUMNS) - table_names
    if missing:
        raise ValueError(f"memory DB is missing derived tables: {sorted(missing)}")

    tables: dict[str, list[list[Any]]] = {}
    for table, columns in DERIVED_COLUMNS.items():
        available = {
            row[1] for row in connection.execute(f"PRAGMA table_info({quoted(table)})")
        }
        absent = set(columns) - available
        if absent:
            raise ValueError(f"{table} is missing derived columns: {sorted(absent)}")
        projection = ",".join(quoted(column) for column in columns)
        ordering = ",".join(quoted(column) for column in columns)
        rows = connection.execute(
            f"SELECT {projection} FROM {quoted(table)} ORDER BY {ordering}"
        ).fetchall()
        tables[table] = [list(row) for row in rows]
    return {
        "format": DUMP_FORMAT,
        "schema_version": 1,
        "tables": tables,
    }


def dump_bytes(db_path: Path) -> bytes:
    absolute = db_path.resolve()
    if not absolute.is_file():
        raise ValueError(f"memory DB does not exist: {absolute}")
    uri = absolute.as_uri() + "?mode=ro"
    connection = sqlite3.connect(uri, uri=True)
    try:
        payload = canonical_payload(connection)
    finally:
        connection.close()
    text = json.dumps(
        payload,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )
    return (text + "\n").encode("ascii")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--db", default=str(DB_PATH))
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(args.root).resolve()
    db_path = Path(args.db)
    absolute = db_path if db_path.is_absolute() else root / db_path
    data = dump_bytes(absolute)
    import sys

    sys.stdout.buffer.write(data)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
