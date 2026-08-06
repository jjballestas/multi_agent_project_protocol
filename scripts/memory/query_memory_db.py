#!/usr/bin/env python3
"""Query allowlisted memory metadata or retrieve one sha-verified git blob."""

from __future__ import annotations

import argparse
import json
import re
import sqlite3
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import build_memory_db as memory_db


def _connection(path: Path, *, writable: bool) -> sqlite3.Connection:
    if not path.is_file():
        raise ValueError(f"memory DB is missing: {path}; use canonical files or git grep")
    mode = "rw" if writable else "ro"
    connection = sqlite3.connect(f"{path.resolve().as_uri()}?mode={mode}", uri=True)
    memory_db.validate_existing_db(connection)
    return connection


def _database_path(root: Path, db_path: Path) -> Path:
    absolute = (db_path if db_path.is_absolute() else root / db_path).resolve()
    expected = (root / memory_db.DB_PATH).resolve()
    if absolute != expected:
        raise ValueError(f"database source must be {expected}")
    return absolute


def _query_terms(query: str) -> list[str]:
    terms = re.findall(r"[A-Za-z0-9][A-Za-z0-9._-]*", query.lower())
    if not terms:
        raise ValueError("query must contain at least one searchable metadata term")
    return list(dict.fromkeys(terms))


def _fts_available(connection: sqlite3.Connection) -> bool:
    return bool(
        connection.execute(
            "SELECT sqlite_compileoption_used('ENABLE_FTS5')"
        ).fetchone()[0]
    )


def _fts_ids(connection: sqlite3.Connection, terms: list[str], limit: int) -> list[str]:
    connection.execute(
        "CREATE VIRTUAL TABLE temp.memory_metadata_fts "
        "USING fts5(artifact_id,title,summary)"
    )
    connection.execute(
        """
        INSERT INTO temp.memory_metadata_fts(artifact_id,title,summary)
        SELECT artifact_id,coalesce(title,''),coalesce(summary_short,'')
        FROM artifacts
        """
    )
    expression = " OR ".join('"' + term.replace('"', '""') + '"' for term in terms)
    return [
        str(row[0])
        for row in connection.execute(
            """
            SELECT artifact_id FROM temp.memory_metadata_fts
            WHERE memory_metadata_fts MATCH ?
            ORDER BY bm25(memory_metadata_fts),artifact_id LIMIT ?
            """,
            (expression, limit),
        )
    ]


def _fallback_ids(
    connection: sqlite3.Connection, terms: list[str], limit: int
) -> list[str]:
    clauses = " OR ".join("lower(term) LIKE ?" for _ in terms)
    parameters: list[Any] = [f"%{term}%" for term in terms]
    parameters.append(limit)
    return [
        str(row[0])
        for row in connection.execute(
            f"""
            SELECT artifact_id
            FROM search_terms
            WHERE {clauses}
            GROUP BY artifact_id
            ORDER BY COUNT(*) DESC,artifact_id
            LIMIT ?
            """,
            parameters,
        )
    ]


def _edges(connection: sqlite3.Connection, artifact_id: str) -> list[dict[str, str]]:
    rows = connection.execute(
        """
        SELECT from_artifact_id,to_artifact_id,edge_type
        FROM artifact_edges
        WHERE from_artifact_id=? OR to_artifact_id=?
        ORDER BY edge_type,from_artifact_id,to_artifact_id
        """,
        (artifact_id, artifact_id),
    )
    return [
        {"from": str(source), "to": str(target), "type": str(edge_type)}
        for source, target, edge_type in rows
    ]


def query(
    root: Path,
    text: str,
    db_path: Path = memory_db.DB_PATH,
    *,
    limit: int = 20,
    force_fallback: bool = False,
) -> dict[str, Any]:
    root = root.resolve()
    absolute_db = _database_path(root, db_path)
    terms = _query_terms(text)
    connection = _connection(absolute_db, writable=False)
    try:
        use_fts = not force_fallback and _fts_available(connection)
        try:
            ids = (
                _fts_ids(connection, terms, limit)
                if use_fts
                else _fallback_ids(connection, terms, limit)
            )
            mode = "fts5-metadata" if use_fts else "fallback-search_terms-like"
        except sqlite3.Error:
            ids = _fallback_ids(connection, terms, limit)
            mode = "fallback-search_terms-like"
        results: list[dict[str, Any]] = []
        for artifact_id in ids:
            row = connection.execute(
                """
                SELECT artifact_id,original_path,summary_short
                FROM artifacts WHERE artifact_id=?
                """,
                (artifact_id,),
            ).fetchone()
            if row is None:
                continue
            results.append(
                {
                    "artifact_id": str(row[0]),
                    "path": str(row[1]),
                    "summary": row[2],
                    "edges": _edges(connection, artifact_id),
                }
            )
    finally:
        connection.close()
    return {
        "mode": mode,
        "degraded": mode.startswith("fallback-"),
        "metadata_only": True,
        "query_terms": terms,
        "results": results,
    }


def retrieve(
    root: Path,
    artifact_id: str,
    db_path: Path = memory_db.DB_PATH,
    *,
    requested_by: str,
    task_id: str | None,
    reason: str | None,
) -> bytes:
    root = root.resolve()
    absolute_db = _database_path(root, db_path)
    connection = _connection(absolute_db, writable=True)
    try:
        row = connection.execute(
            """
            SELECT original_path,hot_path,cold_path,git_commit,sha256
            FROM artifacts WHERE artifact_id=?
            """,
            (artifact_id,),
        ).fetchone()
        if row is None:
            raise ValueError(f"unknown artifact_id: {artifact_id}")
        original_path, hot_path, cold_path, commit, expected_sha = row
        source_path = cold_path or hot_path or original_path
        blob = memory_db.git_blob(root, str(commit), str(source_path))
        actual_sha = memory_db.sha256_bytes(blob)
        if actual_sha != str(expected_sha):
            raise ValueError(f"sha256 mismatch for artifact_id: {artifact_id}")
        agents = memory_db.configured_agents(root, str(commit))
        if requested_by not in agents:
            raise ValueError("requested_by must be a configured agent id")
        if task_id is not None and not memory_db.ID_RE.fullmatch(task_id):
            raise ValueError("task_id must be a canonical id")
        if reason is not None:
            if (
                not reason
                or any(ord(char) > 127 for char in reason)
                or memory_db.contains_pii(reason)
            ):
                raise ValueError("reason must be non-empty ASCII without PII")
        retrieved_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace(
            "+00:00", "Z"
        )
        with connection:
            connection.execute(
                """
                INSERT INTO retrieval_log(
                  requested_by,task_id,artifact_id,reason,retrieved_at,
                  source_commit,sha256_verified
                ) VALUES(?,?,?,?,?,?,1)
                """,
                (
                    requested_by,
                    task_id,
                    artifact_id,
                    reason,
                    retrieved_at,
                    str(commit),
                ),
            )
        return blob
    finally:
        connection.close()


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?")
    parser.add_argument("--retrieve")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--db", type=Path, default=memory_db.DB_PATH)
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--force-fallback", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--requested-by", default="Codex")
    parser.add_argument("--task-id")
    parser.add_argument("--reason")
    args = parser.parse_args(argv)
    if bool(args.retrieve) == bool(args.query):
        parser.error("provide exactly one query or --retrieve ARTIFACT_ID")
    if args.limit < 1 or args.limit > 100:
        parser.error("--limit must be between 1 and 100")
    return args


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        if args.retrieve:
            blob = retrieve(
                args.root,
                args.retrieve,
                args.db,
                requested_by=args.requested_by,
                task_id=args.task_id,
                reason=args.reason,
            )
            sys.stdout.buffer.write(blob)
        else:
            result = query(
                args.root,
                args.query,
                args.db,
                limit=args.limit,
                force_fallback=args.force_fallback,
            )
            print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    except (ValueError, OSError, sqlite3.Error) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
