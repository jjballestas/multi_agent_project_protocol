#!/usr/bin/env python3
"""Compose a deterministic, blob-attested startup pack for one registered agent."""

from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable

import build_memory_db as memory_db


LIVE_STATUSES = {
    "proposed",
    "ready",
    "claimed",
    "in_progress",
    "in_review",
    "review_approved",
    "blocked",
}
TASK_INDEX_PATH = "Area_comun/state/TASK_INDEX.json"
CLAIMS_PATH = "Area_comun/state/CLAIMS.json"
EVENTS_PATH = "runtime/state/events.jsonl"
CONFIG_PATH = "protocol.config.json"
POLICY_PATH = memory_db.POLICY_PATH
NO_AUTHORITY_NOTE = (
    "El pack NO otorga autoridad; las capabilities siguen en config/registry."
)


@dataclass(frozen=True)
class AttestedSource:
    path: str
    commit: str
    sha256: str
    data: bytes


def _read_json_blob(root: Path, commit: str, path: str) -> Any:
    data = memory_db.git_blob(root, commit, path)
    try:
        return json.loads(data.decode("utf-8-sig"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid canonical JSON: {path}") from error


def _source(
    root: Path,
    commit: str,
    path: str,
    expected_sha: str | None = None,
) -> AttestedSource:
    normalized = path.replace("\\", "/")
    data = memory_db.git_blob(root, commit, normalized)
    actual_sha = memory_db.sha256_bytes(data)
    if expected_sha is not None and actual_sha != expected_sha:
        raise ValueError(f"sha256 mismatch for source: {normalized}")
    return AttestedSource(normalized, commit, actual_sha, data)


def _text(source: AttestedSource) -> str:
    try:
        return source.data.decode("utf-8-sig").replace("\r\n", "\n").rstrip("\n")
    except UnicodeDecodeError as error:
        raise ValueError(f"source is not UTF-8 text: {source.path}") from error


def _read_connection(path: Path) -> sqlite3.Connection:
    if not path.is_file():
        raise ValueError(f"memory DB is missing: {path}")
    connection = sqlite3.connect(f"{path.resolve().as_uri()}?mode=ro", uri=True)
    memory_db.validate_existing_db(connection)
    return connection


def _database_path(root: Path, db_path: Path) -> Path:
    absolute = (db_path if db_path.is_absolute() else root / db_path).resolve()
    expected = (root / memory_db.DB_PATH).resolve()
    if absolute != expected:
        raise ValueError(f"database source must be {expected}")
    return absolute


def _registered_agents(root: Path, commit: str) -> set[str]:
    return memory_db.configured_agents(root, commit)


def _json_object(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError(f"{label} must be a JSON object")
    return value


def _json_array(value: Any, label: str) -> list[Any]:
    if not isinstance(value, list):
        raise ValueError(f"{label} must be a JSON array")
    return value


def _governed_source_for_agent(path: str, agent_id: str) -> bool:
    if path in {"AGENTS.md", CONFIG_PATH}:
        return True
    if path.startswith(("Area_comun/", "runtime/state/")):
        return True
    if path.startswith("personal/"):
        return path.startswith(f"personal/{agent_id}/")
    return False


def _event_seq(root: Path, commit: str) -> int:
    try:
        data = memory_db.git_blob(root, commit, EVENTS_PATH)
    except ValueError:
        return 0
    maximum = 0
    for raw in data.decode("utf-8-sig").splitlines():
        if not raw.strip():
            continue
        try:
            event = json.loads(raw)
        except json.JSONDecodeError:
            break
        seq = event.get("seq") if isinstance(event, dict) else None
        if isinstance(seq, int):
            maximum = max(maximum, seq)
    return maximum


def _applies_to(value: Any, agent_id: str) -> bool:
    if value is None:
        return False
    parsed = value
    if isinstance(value, str):
        try:
            parsed = json.loads(value)
        except json.JSONDecodeError:
            parsed = [part.strip() for part in value.split(",") if part.strip()]
    values = parsed if isinstance(parsed, list) else [parsed]
    return any(str(item) in {"*", "all", agent_id} for item in values)


def _indented(text: str) -> str:
    if not text:
        return "    (empty file)"
    return "\n".join(f"    {line}" if line else "    " for line in text.splitlines())


def _section(title: str, entries: Iterable[tuple[str, str]]) -> str:
    rendered = list(entries)
    lines = [f"## {title}", ""]
    if not rendered:
        lines.extend(["- EMPTY", ""])
        return "\n".join(lines)
    for label, content in rendered:
        lines.extend([f"### {label}", "", _indented(content), ""])
    return "\n".join(lines)


def compose_pack(
    root: Path,
    agent_id: str,
    db_path: Path = memory_db.DB_PATH,
    *,
    at: str = "HEAD",
) -> bytes:
    root = root.resolve()
    commit = memory_db.git_commit(root, at)
    agents = _registered_agents(root, commit)
    if agent_id not in agents:
        raise ValueError(f"agent_id is not registered and enabled: {agent_id}")

    sources: dict[str, AttestedSource] = {}

    def add_source(path: str, expected_sha: str | None = None) -> AttestedSource:
        source = _source(root, commit, path, expected_sha)
        existing = sources.get(source.path)
        if existing is not None and existing.sha256 != source.sha256:
            raise ValueError(f"conflicting attestations for source: {source.path}")
        sources[source.path] = source
        return source

    add_source(CONFIG_PATH)
    add_source(POLICY_PATH)
    policy = memory_db.memory_index_policy(root, commit)
    pack_policy = policy["revive_pack"]
    max_bytes = int(pack_policy["max_bytes"])
    max_inline_source_bytes = int(pack_policy["max_inline_source_bytes"])
    chars_per_token = int(pack_policy["chars_per_token"])
    task_index_source = add_source(TASK_INDEX_PATH)
    claims_source = add_source(CLAIMS_PATH)
    task_index = _json_object(
        json.loads(task_index_source.data.decode("utf-8-sig")), TASK_INDEX_PATH
    )
    claims_doc = _json_object(
        json.loads(claims_source.data.decode("utf-8-sig")), CLAIMS_PATH
    )
    tasks = [
        item
        for item in _json_array(task_index.get("tasks", []), f"{TASK_INDEX_PATH}.tasks")
        if isinstance(item, dict)
        and item.get("owner") == agent_id
        and item.get("status") in LIVE_STATUSES
    ]
    tasks.sort(key=lambda item: str(item.get("id", "")))
    active_claims = [
        item
        for item in _json_array(claims_doc.get("claims", []), f"{CLAIMS_PATH}.claims")
        if isinstance(item, dict)
        and item.get("owner") == agent_id
        and item.get("status") == "active"
    ]
    active_claims.sort(key=lambda item: str(item.get("claim_id", "")))

    connection = _read_connection(_database_path(root, db_path))
    try:
        memory_entries: list[tuple[str, str]] = []
        omitted_entries: list[dict[str, Any]] = []
        inline_source_bytes = 0
        memory_inline_bytes = 0
        memory_inline_limit = max_inline_source_bytes // 2
        for row in connection.execute(
            """
            SELECT memory_id,source_path,source_commit,sha256,valid_from,valid_until
            FROM agent_memory
            WHERE agent_id=? AND is_current=1
            ORDER BY coalesce(valid_from,'') DESC,source_path,memory_id
            """,
            (agent_id,),
        ):
            memory_id, path, source_commit, expected_sha = map(str, row[:4])
            valid_from, valid_until = row[4], row[5]
            derived = memory_db.derive_agent_id(path)
            if derived != agent_id or source_commit != commit:
                raise ValueError(f"identity or commit mismatch for memory: {memory_id}")
            source = _source(root, commit, path, expected_sha)
            size = len(source.data)
            if memory_inline_bytes + size <= memory_inline_limit:
                add_source(path, expected_sha)
                memory_entries.append((path, _text(source)))
                memory_inline_bytes += size
                inline_source_bytes += size
            else:
                omitted_entries.append(
                    {
                        "kind": "memory",
                        "memory_id": memory_id,
                        "path": path,
                        "sha256": expected_sha,
                        "bytes": size,
                        "valid_from": valid_from,
                        "valid_until": valid_until,
                        "reason": "inline budget",
                    }
                )

        task_entries: list[tuple[str, str]] = []
        for task in tasks:
            task_id = str(task.get("id") or "")
            path = str(task.get("file") or "")
            if not task_id or not path.startswith("Area_comun/tasks/"):
                raise ValueError(f"live task has no canonical task file: {task_id}")
            source = add_source(path)
            source_size = len(source.data)
            if inline_source_bytes + source_size <= max_inline_source_bytes:
                task_entries.append((f"{task_id} canonical task", _text(source)))
                inline_source_bytes += source_size
            else:
                task_entries.append(
                    (
                        f"{task_id} canonical task (metadata summary)",
                        json.dumps(task, ensure_ascii=True, sort_keys=True),
                    )
                )
                omitted_entries.append(
                    {"kind": "task", "path": path, "sha256": source.sha256,
                     "bytes": source_size, "reason": "inline budget"}
                )
        if active_claims:
            task_entries.append(
                (
                    "Active claims",
                    json.dumps(active_claims, ensure_ascii=True, sort_keys=True, indent=2),
                )
            )

        mailbox_entries: list[tuple[str, str]] = []
        mailbox_rows = connection.execute(
            """
            SELECT a.artifact_id,a.original_path,a.git_commit,a.sha256,
                   c.frontmatter_json
            FROM artifacts a
            JOIN artifact_content_index c USING(artifact_id)
            WHERE a.artifact_type='mailbox'
              AND a.original_path LIKE 'Area_comun/mailbox/open/%'
            ORDER BY a.original_path,a.artifact_id
            """
        )
        for artifact_id, path, source_commit, expected_sha, frontmatter_json in mailbox_rows:
            try:
                metadata = json.loads(frontmatter_json or "{}")
            except json.JSONDecodeError as error:
                raise ValueError(f"invalid mailbox metadata: {artifact_id}") from error
            if metadata.get("to") != agent_id or metadata.get("status") != "open":
                continue
            if str(source_commit) != commit:
                raise ValueError(f"mailbox commit mismatch: {artifact_id}")
            source = add_source(str(path), str(expected_sha))
            source_size = len(source.data)
            if inline_source_bytes + source_size <= max_inline_source_bytes:
                mailbox_entries.append((str(artifact_id), _text(source)))
                inline_source_bytes += source_size
            else:
                mailbox_entries.append(
                    (str(artifact_id) + " (metadata summary)", json.dumps(metadata, ensure_ascii=True, sort_keys=True))
                )
                omitted_entries.append(
                    {"kind": "mailbox", "path": str(path), "sha256": source.sha256,
                     "bytes": source_size, "reason": "inline budget"}
                )

        decision_entries: list[tuple[str, str]] = []
        decision_rows = connection.execute(
            """
            SELECT p.decision_id,p.applies_to,a.original_path,a.git_commit,a.sha256
            FROM policy_status p
            JOIN artifacts a ON a.artifact_id=p.decision_id
            WHERE p.policy_state='active'
            ORDER BY p.decision_id
            """
        )
        for decision_id, applies_to, path, source_commit, expected_sha in decision_rows:
            if not _applies_to(applies_to, agent_id):
                continue
            if str(source_commit) != commit:
                raise ValueError(f"decision commit mismatch: {decision_id}")
            source = add_source(str(path), str(expected_sha))
            source_size = len(source.data)
            if inline_source_bytes + source_size <= max_inline_source_bytes:
                decision_entries.append((str(decision_id), _text(source)))
                inline_source_bytes += source_size
            else:
                decision_entries.append(
                    (
                        str(decision_id) + " (metadata summary)",
                        json.dumps({"decision_id": decision_id, "applies_to": applies_to}, ensure_ascii=True, sort_keys=True),
                    )
                )
                omitted_entries.append(
                    {"kind": "decision", "path": str(path), "sha256": source.sha256,
                     "bytes": source_size, "reason": "inline budget"}
                )

        context_entries: list[tuple[str, str]] = []
        current_seq = _event_seq(root, commit)
        live_task_ids = [str(item.get("id")) for item in tasks]
        for task_id in live_task_ids:
            row = connection.execute(
                """
                SELECT context_hash,generated_at,included_artifacts_json,
                       excluded_artifacts_json,summary,token_estimate,
                       valid_until_event_seq
                FROM task_context_cache
                WHERE task_id=? AND valid_until_event_seq IS NOT NULL
                  AND valid_until_event_seq>=?
                ORDER BY generated_at DESC,context_hash
                LIMIT 1
                """,
                (task_id, current_seq),
            ).fetchone()
            if row is None:
                continue
            (
                context_hash,
                generated_at,
                included_json,
                excluded_json,
                summary,
                cache_tokens,
                valid_until,
            ) = row
            try:
                included = json.loads(included_json)
                excluded = json.loads(excluded_json) if excluded_json else []
            except json.JSONDecodeError as error:
                raise ValueError(f"invalid context cache JSON: {task_id}") from error
            if not isinstance(included, list) or not all(
                isinstance(item, str) for item in included
            ):
                raise ValueError(f"context cache sources must be a string array: {task_id}")
            for reference in sorted(set(included)):
                artifact = connection.execute(
                    """
                    SELECT original_path,git_commit,sha256
                    FROM artifacts
                    WHERE artifact_id=? OR original_path=?
                    ORDER BY artifact_id LIMIT 1
                    """,
                    (reference, reference),
                ).fetchone()
                if artifact is None:
                    raise ValueError(f"context cache source is unknown: {reference}")
                path, source_commit, expected_sha = map(str, artifact)
                if source_commit != commit or not _governed_source_for_agent(
                    path, agent_id
                ):
                    raise ValueError(f"context cache source is not eligible: {reference}")
                add_source(path, expected_sha)
            context_entries.append(
                (
                    f"{task_id} / {context_hash}",
                    json.dumps(
                        {
                            "generated_at": generated_at,
                            "included_artifacts": included,
                            "excluded_artifacts": excluded,
                            "summary": summary,
                            "token_estimate": cache_tokens,
                            "valid_until_event_seq": valid_until,
                        },
                        ensure_ascii=True,
                        sort_keys=True,
                        indent=2,
                    ),
                )
            )
    finally:
        connection.close()

    body = "\n".join(
        [
            f"# Revive pack: {agent_id}",
            "",
            f"- agent_id: {agent_id}",
            f"- git_commit: {commit}",
            f"- authority_note: {NO_AUTHORITY_NOTE}",
            f"- budget_bytes: {max_bytes}",
            f"- inline_source_budget_bytes: {max_inline_source_bytes}",
            f"- inline_source_bytes: {inline_source_bytes}",
            "",
            _section("1. Memoria vigente", memory_entries),
            _section("2. Tareas vivas y claims activos", task_entries),
            _section("3. Mailbox open dirigido al agente", mailbox_entries),
            _section("4. Decisiones activas aplicables", decision_entries),
            _section("5. Task context cache fresco", context_entries),
            _section(
                "6. Fuentes omitidas del cuerpo por presupuesto",
                [
                    (
                        "Declaracion de exclusion",
                        json.dumps(omitted_entries, ensure_ascii=True, sort_keys=True, indent=2),
                    )
                ] if omitted_entries else [],
            ),
        ]
    )
    attestations = [
        "## ATESTACION DE FUENTES",
        "",
        "| path | git_commit | sha256_blob |",
        "|---|---|---|",
    ]
    for source in sorted(sources.values(), key=lambda item: item.path):
        attestations.append(
            f"| `{source.path}` | `{source.commit}` | `{source.sha256}` |"
        )
    without_estimate = body + "\n" + "\n".join(attestations) + "\n"
    token_estimate = max(
        1,
        (len(without_estimate.encode("utf-8")) + chars_per_token - 1) // chars_per_token,
    )
    pack = (
        body
        + f"\n- token_estimate: {token_estimate}\n\n"
        + "\n".join(attestations)
        + "\n"
    )
    encoded = pack.replace("\r\n", "\n").encode("utf-8")
    if len(encoded) > max_bytes:
        raise ValueError(
            f"revive pack exceeds declared budget: {len(encoded)} > {max_bytes} bytes"
        )
    return encoded


def _validate_output(root: Path, output: Path) -> Path:
    absolute = output.resolve()
    try:
        relative = absolute.relative_to(root.resolve())
    except ValueError:
        return absolute
    allowed = (root.resolve() / "runtime" / "memory").resolve()
    try:
        absolute.relative_to(allowed)
    except ValueError as error:
        raise ValueError(
            f"output inside the repository must be under non-governed {allowed}"
        ) from error
    if relative.as_posix() == memory_db.DB_PATH.as_posix():
        raise ValueError("output must not replace the memory DB")
    return absolute


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("agent_id")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--db", type=Path, default=memory_db.DB_PATH)
    parser.add_argument("--at", default="HEAD")
    parser.add_argument("--output", type=Path)
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    try:
        root = args.root.resolve()
        output = _validate_output(root, args.output) if args.output else None
        pack = compose_pack(root, args.agent_id, args.db, at=args.at)
        if output is None:
            sys.stdout.buffer.write(pack)
        else:
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(pack)
    except (OSError, sqlite3.Error, ValueError) as error:
        print(f"ERROR: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
