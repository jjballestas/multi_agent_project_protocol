#!/usr/bin/env python3
"""Read-only fast and full drift gates for the derived memory database."""

from __future__ import annotations

import argparse
import json
import sqlite3
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

import build_memory_db as memory_db
import dump_memory_db


def _readonly_connection(path: Path) -> sqlite3.Connection:
    if not path.is_file():
        raise ValueError(f"memory DB is missing: {path}")
    connection = sqlite3.connect(f"{path.resolve().as_uri()}?mode=ro", uri=True)
    memory_db.validate_existing_db(connection)
    return connection


def _active_decisions(artifacts: list[memory_db.SourceArtifact]) -> set[str]:
    return {
        artifact.artifact_id
        for artifact in artifacts
        if artifact.artifact_type == "decision"
        and artifact.metadata.get("status") == "active"
    }


def fast_check(root: Path, *, at: str = "HEAD") -> dict[str, Any]:
    """Validate canonical hot inputs without opening or probing SQLite."""
    root = root.resolve()
    commit = memory_db.git_commit(root, at)
    artifacts, warnings = memory_db.load_artifacts(root, commit)
    packs = memory_db.load_cold_packs(root, commit)
    rules = memory_db.load_hot_cold_rules(root, commit)
    active = _active_decisions(artifacts)
    missing: list[str] = []
    for row in rules:
        created_by_decision = row[-1]
        if created_by_decision and created_by_decision not in active:
            missing.append(str(created_by_decision))
    if missing:
        raise ValueError(
            "hot/cold rule references an absent or inactive decision: "
            + ", ".join(sorted(set(missing)))
        )
    return {
        "mode": "fast",
        "result": "pass",
        "commit": commit,
        "artifact_count": len(artifacts),
        "active_decision_count": len(active),
        "manifest_count": len(packs),
        "rule_count": len(rules),
        "warnings": warnings,
        "database_read": False,
        "stubs": "noop-until-f2",
    }


def _publicable_pii_errors(
    connection: sqlite3.Connection,
    domain_pii_terms: list[str],
) -> list[str]:
    errors: list[str] = []
    rows = connection.execute(
        """
        SELECT a.artifact_id,a.title,a.summary_short,a.summary_long,a.owner,
               a.is_pii_safe,c.plain_text_excerpt,c.redaction_state,
               p.pii_state,p.finding_count,p.public_plane_allowed
        FROM artifacts AS a
        LEFT JOIN artifact_content_index AS c USING(artifact_id)
        LEFT JOIN pii_classification AS p USING(artifact_id)
        WHERE a.is_pii_safe=1 OR c.redaction_state='public_ok'
              OR p.public_plane_allowed=1
        """
    )
    for row in rows:
        (
            artifact_id,
            title,
            summary_short,
            summary_long,
            owner,
            _is_pii_safe,
            excerpt,
            _redaction_state,
            pii_state,
            finding_count,
            _public_plane_allowed,
        ) = row
        if pii_state != "clean" or finding_count not in (0, None):
            errors.append(f"publicable artifact is not classified clean: {artifact_id}")
        for value in (title, summary_short, summary_long, owner, excerpt):
            if value is not None and memory_db.contains_pii(
                str(value), domain_pii_terms
            ):
                errors.append(f"publicable artifact contains PII: {artifact_id}")
                break
    return errors


def _sweep_database(
    root: Path,
    connection: sqlite3.Connection,
    artifacts: list[memory_db.SourceArtifact],
    commit: str,
) -> list[str]:
    errors: list[str] = []
    source_by_id = {artifact.artifact_id: artifact for artifact in artifacts}
    db_ids: set[str] = set()
    for artifact_id, path, row_commit, digest in connection.execute(
        "SELECT artifact_id,original_path,git_commit,sha256 FROM artifacts"
    ):
        db_ids.add(str(artifact_id))
        source = source_by_id.get(str(artifact_id))
        if source is None:
            errors.append(f"database artifact has no canonical source: {artifact_id}")
            continue
        if str(path) != source.relative_path:
            errors.append(f"database path differs from canonical scan: {artifact_id}")
        if str(row_commit) != commit:
            errors.append(f"database commit differs from HEAD: {artifact_id}")
        actual = memory_db.sha256_bytes(source.data)
        if str(digest) != actual:
            errors.append(f"database sha256 differs from git blob: {artifact_id}")
    for artifact_id in sorted(set(source_by_id) - db_ids):
        errors.append(f"canonical artifact has no database row: {artifact_id}")
    domain_pii_terms = memory_db.memory_index_policy(root, commit)[
        "domain_pii_terms"
    ]
    errors.extend(_publicable_pii_errors(connection, domain_pii_terms))
    return errors


def _clone_instance(root: Path, destination: Path) -> Path:
    top = Path(
        subprocess.check_output(
            ["git", "rev-parse", "--show-toplevel"], cwd=root, text=True
        ).strip()
    ).resolve()
    relative = root.relative_to(top)
    subprocess.check_call(
        ["git", "clone", "--quiet", "--no-hardlinks", str(top), str(destination)]
    )
    return destination / relative


def _round_trip_matches(root: Path, current_dump: bytes, commit: str) -> None:
    with tempfile.TemporaryDirectory(prefix="memory-full-") as temp:
        clone_root = _clone_instance(root, Path(temp) / "repo")
        memory_db.build(clone_root, rebuild=True, at=commit)
        rebuilt_dump = dump_memory_db.dump_bytes(clone_root / memory_db.DB_PATH)
    if current_dump != rebuilt_dump:
        raise ValueError("canonical incremental dump differs from fresh rebuild")


def full_check(
    root: Path,
    db_path: Path = memory_db.DB_PATH,
    *,
    at: str = "HEAD",
) -> dict[str, Any]:
    """Fail closed on DB/file drift and prove the derived round-trip."""
    root = root.resolve()
    commit = memory_db.git_commit(root, at)
    artifacts, warnings = memory_db.load_artifacts(root, commit)
    # Parse every canonical manifest/rule even when the instance has none.
    packs = memory_db.load_cold_packs(root, commit)
    rules = memory_db.load_hot_cold_rules(root, commit)
    absolute_db = (db_path if db_path.is_absolute() else root / db_path).resolve()
    expected_db = (root / memory_db.DB_PATH).resolve()
    if absolute_db != expected_db:
        raise ValueError(f"database source must be {expected_db}")
    connection = _readonly_connection(absolute_db)
    try:
        errors = _sweep_database(root, connection, artifacts, commit)
    finally:
        connection.close()
    if errors:
        raise ValueError("; ".join(errors))
    current_dump = dump_memory_db.dump_bytes(absolute_db)
    _round_trip_matches(root, current_dump, commit)
    return {
        "mode": "full",
        "result": "pass",
        "commit": commit,
        "artifact_count": len(artifacts),
        "manifest_count": len(packs),
        "rule_count": len(rules),
        "warnings": warnings,
        "round_trip": "pass",
        "sweep": "bidirectional-pass",
        "database_written": False,
        "stubs": "noop-until-f2",
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    modes = parser.add_mutually_exclusive_group(required=True)
    modes.add_argument("--fast", action="store_true")
    modes.add_argument("--full", action="store_true")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--db", type=Path, default=memory_db.DB_PATH)
    parser.add_argument("--at", default="HEAD")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        result = (
            fast_check(args.root, at=args.at)
            if args.fast
            else full_check(args.root, args.db, at=args.at)
        )
    except (ValueError, OSError, sqlite3.Error, subprocess.SubprocessError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(json.dumps(result, sort_keys=True, separators=(",", ":")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
