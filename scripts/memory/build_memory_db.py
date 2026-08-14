#!/usr/bin/env python3
"""Build the read-only, derived SQLite memory index for a protocol instance.

DDL delta from the superseded M6 prototype: this module replaces the
divergent prototype schema with the 15-table SPEC-MEMORIA-HIBRIDA v0.2.1 s.3
schema. It restores the SPEC column names, CHECK constraints, composite keys,
explicit ON DELETE CASCADE clauses, nullable PII fields, and user_version=1;
removes the FTS table and all body-derived/heuristic indexing from F1; and
keeps embeddings as an empty schema-reserved table. No migration of a Zeus DB
is attempted: normal mode reconciles an existing SPEC v1 cache incrementally,
while --rebuild deletes it and reconstructs the derived partition from canon.
The SPEC intentionally omits foreign keys from artifact_edges.to_artifact_id,
artifact_versions, retrieval_log, embeddings, and task_context_cache because
those rows may reference pending or purged live-index identifiers.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sqlite3
import subprocess
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Iterator


DB_PATH = Path("runtime/memory/index.db")
SCHEMA_VERSION = 1

ARTIFACT_TYPES = {
    "decision", "task", "spec", "handoff", "mailbox", "report", "artifact",
    "memory", "state_snapshot", "eventlog", "runlog", "requirement",
}
EDGE_TYPES = {
    "implements", "reviews", "supersedes", "contradicts", "depends_on",
    "mentions", "handoff_for", "mailbox_for", "decision_for", "spec_for",
}
EDGE_PRODUCERS = {
    "relates_to": "mentions",
    "linked_decisions": "decision_for",
    "supersedes": "supersedes",
    "superseded_by": "supersedes",
    "file": "implements",
}
RESERVED_EDGE_TYPES = EDGE_TYPES - set(EDGE_PRODUCERS.values())
ALLOWLIST_KEYS = {
    "task_id", "decision_id", "spec_id", "message_id", "title", "status",
    "type", "owner", "from", "to", "created_at", "updated_at", "closed_at",
    "phase", "priority", "relates_to", "linked_decisions", "supersedes",
    "superseded_by", "applies_to", "file",
}
INTRINSIC_ID_KEYS = {
    "task": "task_id", "decision": "decision_id", "spec": "spec_id",
    "mailbox": "message_id", "handoff": "handoff_id",
    "requirement": "requirement_id",
}
CORE_STATUS_VALUES = frozenset({
    "proposed", "ready", "claimed", "in_progress", "in_review", "done",
    "blocked", "cancelled", "open", "answered", "archived", "superseded",
    "active", "draft", "accepted", "approved",
    "for_review", "for_implementation", "for_decision", "change_required",
    "delivered", "final", "ok", "ready_for_implementation",
    "ready_for_independent_review", "ready_for_review", "reviewed", "submitted",
})
TYPE_VALUES = {
    "feature", "implementation", "refactor", "integration", "migration",
    "security", "release", "discovery", "analysis", "review",
    "documentation", "triage", "ACK", "FYI", "OK", "REVIEW", "CHANGES",
    "BLOCKED", "DONE", "DECISION_REQUIRED", "HUMAN_REQUIRED", "ACTION",
    "ANOMALY", "ANSWER", "BLOCKER", "DECISION", "DECISION_REQUEST",
    "DIRECTIVE", "HANDOFF", "INFO", "QUESTION", "REMINDER", "REQUEST",
    "RESPONSE", "REVIEW-RESPONSE", "REVIEW_REQUEST",
    "REVIEW_RESULT", "REVIEW_VERDICT", "TASK_ASSIGNMENT", "adversarial_review",
    "anomaly", "artifact", "build", "connector", "coordination", "design", "design-spec",
    "doc", "docs", "evidence", "fix", "handoff", "infra", "product",
    "protocol", "requirement", "review-verdict", "review_result",
    "review_verdict", "status_note",
}
PRIORITY_VALUES = {"low", "normal", "medium", "high", "critical"}
ID_RE = re.compile(r"^[A-Z]+-[0-9A-Za-z._-]+$")
DATE_RE = re.compile(
    r"^\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\d|3[01])"
    r"(?:T(?:(?:[01]\d|2[0-3]):[0-5]\d:[0-5]\d(?:\.\d{1,6})?"
    r"|(?:[01]\d|2[0-3])[0-5]\d[0-5]\d)"
    r"(?:Z|[+-](?:(?:0\d|1[0-3]):[0-5]\d|14:00))?)?$"
)
PATH_RE = re.compile(r"^[A-Za-z0-9._/\\-]+$")
TITLE_MAX_LENGTH = 500
STRUCTURAL_PII_PATTERNS = (
    re.compile(r"[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}", re.I),
    re.compile(r"[A-Z]{2}[ \t\u00a0\u2009\u202f._/\\-]*\d{2}(?:[ \t\u00a0\u2009\u202f._/\\-]*[A-Z0-9]){10,30}", re.I | re.ASCII),
    re.compile(r"\b(?:NIF|NIE|NIT|DNI|SSN)\b", re.I),
)
PHONE_CANDIDATE_RE = re.compile(r"(?:\+?\d[\d .()-]{7,}\d)")
ACCOUNT_IDENTIFIER_SEPARATORS_RE = re.compile(r"[ \t\u00a0\u2009\u202f._/\\-]+")
ACCOUNT_IDENTIFIER_START_RE = re.compile(
    r"(?=[A-Z]{2}[ \t\u00a0\u2009\u202f._/\\-]*\d{2})", re.I | re.ASCII
)
ACCOUNT_IDENTIFIER_CONTIGUOUS_RE = re.compile(
    r"[A-Z]{2}\d{2}[A-Z0-9]{10,30}", re.I | re.ASCII
)
ACCOUNT_IDENTIFIER_MIN_LENGTH = 14
ACCOUNT_IDENTIFIER_MAX_LENGTH = 34
SECRET_SUFFIXES = {".key", ".pem"}
TEXT_SUFFIXES = {".md", ".json", ".jsonl", ".txt", ".yaml", ".yml"}
EVENTS_PATH = Path("runtime/state/events.jsonl")
LEDGER_LOCK_PATH = Path("runtime/state/.ledger.lock")
RULES_PATH = "Area_comun/protocol/MEMORY_HOT_COLD_RULES.json"
POLICY_PATH = "Area_comun/protocol/MEMORY_INDEX_POLICY.json"
def account_identifier_checksum_is_valid(value: str) -> bool:
    compact = ACCOUNT_IDENTIFIER_SEPARATORS_RE.sub("", value).upper()
    if not re.fullmatch(r"[A-Z]{2}\d{2}[A-Z0-9]{10,30}", compact, re.ASCII):
        return False
    numeric = "".join(
        str(ord(char) - 55) if "A" <= char <= "Z" else char
        for char in compact[4:] + compact[:4]
    )
    return int(numeric) % 97 == 1


def git_ref_requires_pii_check(value: Any) -> bool:
    return not (
        isinstance(value, str)
        and bool(re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", value, re.I))
    )


def account_identifier_candidate_has_valid_prefix(value: str, following: str) -> bool:
    compact_length = 0
    for index, char in enumerate(value):
        if char.isascii() and char.isalnum():
            compact_length += 1
        if not ACCOUNT_IDENTIFIER_MIN_LENGTH <= compact_length <= ACCOUNT_IDENTIFIER_MAX_LENGTH:
            continue
        end = index + 1
        next_char = value[end:end + 1] or following
        if next_char and not ACCOUNT_IDENTIFIER_SEPARATORS_RE.fullmatch(next_char):
            continue
        if account_identifier_checksum_is_valid(value[:end]):
            return True
    return False


def account_identifier_candidates(value: str) -> Iterator[tuple[str, str]]:
    for start in ACCOUNT_IDENTIFIER_START_RE.finditer(value):
        candidate = STRUCTURAL_PII_PATTERNS[1].match(value, start.start())
        if candidate is not None:
            yield candidate.group(0), value[candidate.end():candidate.end() + 1]


def account_identifier_contiguous_is_bounded(value: str) -> bool:
    for candidate in ACCOUNT_IDENTIFIER_CONTIGUOUS_RE.finditer(value):
        start = candidate.start()
        end = candidate.end()
        while start and value[start - 1].isascii() and value[start - 1].isalnum():
            start -= 1
        while end < len(value) and value[end].isascii() and value[end].isalnum():
            end += 1
        if end - start <= ACCOUNT_IDENTIFIER_MAX_LENGTH:
            return True
    return False


DDL = r"""
CREATE TABLE artifacts (
  artifact_id TEXT PRIMARY KEY,
  artifact_type TEXT NOT NULL CHECK (artifact_type IN ('decision','task','spec','handoff','mailbox','report','artifact','memory','state_snapshot','eventlog','runlog','requirement')),
  title TEXT, status TEXT, original_path TEXT NOT NULL, hot_path TEXT, cold_path TEXT,
  git_commit TEXT NOT NULL, sha256 TEXT NOT NULL,
  created_at TEXT, updated_at TEXT, closed_at TEXT, owner TEXT, project TEXT,
  is_active_policy INTEGER NOT NULL DEFAULT 0,
  is_hot INTEGER NOT NULL DEFAULT 1,
  is_pii_safe INTEGER,
  summary_short TEXT, summary_long TEXT,
  canonicality TEXT NOT NULL CHECK (canonicality IN ('canonical_file','stub','derived_index','cold_copy','external_pointer')),
  retention_class TEXT NOT NULL CHECK (retention_class IN ('hot','warm','cold','sealed','do_not_archive')),
  cold_reason TEXT, last_verified_at TEXT,
  schema_version INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX idx_artifacts_type_status ON artifacts(artifact_type, status);
CREATE INDEX idx_artifacts_hot ON artifacts(is_hot, retention_class);

CREATE TABLE artifact_edges (
  from_artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id) ON DELETE CASCADE,
  to_artifact_id TEXT NOT NULL,
  edge_type TEXT NOT NULL CHECK (edge_type IN ('implements','reviews','supersedes','contradicts','depends_on','mentions','handoff_for','mailbox_for','decision_for','spec_for')),
  source_path TEXT NOT NULL, source_commit TEXT NOT NULL,
  PRIMARY KEY (from_artifact_id, to_artifact_id, edge_type)
);

CREATE TABLE agent_memory (
  memory_id TEXT PRIMARY KEY, agent_id TEXT NOT NULL,
  scope TEXT NOT NULL CHECK (scope IN ('personal','compartido')),
  summary TEXT, source_path TEXT NOT NULL, source_commit TEXT NOT NULL,
  event_seq INTEGER, sha256 TEXT NOT NULL, valid_from TEXT, valid_until TEXT,
  is_current INTEGER NOT NULL DEFAULT 1
);
CREATE INDEX idx_agent_memory_current ON agent_memory(agent_id, is_current);

CREATE TABLE cold_packs (
  pack_id TEXT PRIMARY KEY, pack_type TEXT NOT NULL, path TEXT NOT NULL,
  git_ref TEXT NOT NULL, created_at TEXT NOT NULL, sha256_manifest TEXT NOT NULL,
  artifact_count INTEGER NOT NULL, validated_at TEXT, validator_result TEXT
);

CREATE TABLE retrieval_log (
  retrieval_id INTEGER PRIMARY KEY AUTOINCREMENT, requested_by TEXT NOT NULL,
  task_id TEXT, artifact_id TEXT NOT NULL, reason TEXT, retrieved_at TEXT NOT NULL,
  source_commit TEXT NOT NULL, sha256_verified INTEGER NOT NULL
);

CREATE TABLE artifact_versions (
  artifact_id TEXT NOT NULL, version_id INTEGER NOT NULL, git_commit TEXT NOT NULL,
  event_seq INTEGER, path_at_commit TEXT NOT NULL, sha256 TEXT NOT NULL,
  changed_at TEXT, changed_by TEXT, change_kind TEXT, status_at_version TEXT,
  PRIMARY KEY (artifact_id, version_id)
);

CREATE TABLE artifact_content_index (
  artifact_id TEXT PRIMARY KEY REFERENCES artifacts(artifact_id) ON DELETE CASCADE,
  content_sha256 TEXT NOT NULL, indexed_at TEXT NOT NULL, language TEXT,
  token_estimate INTEGER, line_count INTEGER, has_frontmatter INTEGER,
  frontmatter_json TEXT, plain_text_excerpt TEXT,
  redaction_state TEXT NOT NULL DEFAULT 'unclassified' CHECK (redaction_state IN ('unclassified','raw_private','redacted','public_ok'))
);

CREATE TABLE policy_status (
  decision_id TEXT PRIMARY KEY,
  policy_state TEXT NOT NULL CHECK (policy_state IN ('active','superseded','historical')),
  superseded_by TEXT, supersedes TEXT, active_from TEXT, active_until TEXT,
  applies_to TEXT, hot_required INTEGER NOT NULL DEFAULT 0, reason TEXT
);

CREATE TABLE hot_cold_rules (
  rule_id TEXT PRIMARY KEY, artifact_type TEXT NOT NULL, selector TEXT NOT NULL,
  target_retention_class TEXT NOT NULL, window_days INTEGER, window_count INTEGER,
  requires_stub INTEGER NOT NULL DEFAULT 0,
  requires_active_policy_check INTEGER NOT NULL DEFAULT 0,
  enabled INTEGER NOT NULL DEFAULT 0, created_by_decision TEXT
);

CREATE TABLE stubs (
  stub_id TEXT PRIMARY KEY,
  artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id) ON DELETE CASCADE,
  stub_path TEXT NOT NULL, original_path TEXT NOT NULL, cold_path TEXT NOT NULL,
  git_commit TEXT NOT NULL, sha256 TEXT NOT NULL, summary TEXT,
  rehydration_command TEXT NOT NULL, created_at TEXT NOT NULL, validated_at TEXT
);

CREATE TABLE validation_runs (
  validation_id INTEGER PRIMARY KEY AUTOINCREMENT,
  run_type TEXT NOT NULL CHECK (run_type IN ('hot_fast','full_rebuild','drift_check')),
  started_at TEXT NOT NULL, finished_at TEXT, actor TEXT NOT NULL,
  git_commit TEXT NOT NULL, event_seq INTEGER,
  result TEXT NOT NULL CHECK (result IN ('pass','fail')),
  errors_json TEXT, warnings_json TEXT, checked_artifact_count INTEGER,
  db_hash TEXT, manifest_hash TEXT
);

CREATE TABLE pii_classification (
  artifact_id TEXT PRIMARY KEY REFERENCES artifacts(artifact_id) ON DELETE CASCADE,
  classifier_version TEXT NOT NULL, classified_at TEXT NOT NULL,
  pii_state TEXT NOT NULL CHECK (pii_state IN ('clean','findings','not_scanned')),
  finding_count INTEGER NOT NULL DEFAULT 0, finding_types_json TEXT,
  public_plane_allowed INTEGER NOT NULL DEFAULT 0,
  redaction_required INTEGER NOT NULL DEFAULT 0, redaction_artifact_id TEXT
);

CREATE TABLE search_terms (
  artifact_id TEXT NOT NULL REFERENCES artifacts(artifact_id) ON DELETE CASCADE,
  term TEXT NOT NULL, field TEXT NOT NULL, weight REAL NOT NULL DEFAULT 1.0,
  source TEXT NOT NULL, PRIMARY KEY (artifact_id, term, field)
);

CREATE TABLE embeddings (
  artifact_id TEXT NOT NULL, chunk_id TEXT NOT NULL, model TEXT NOT NULL,
  dimension INTEGER NOT NULL, embedding BLOB NOT NULL,
  source_sha256 TEXT NOT NULL, created_at TEXT NOT NULL, pii_safe INTEGER NOT NULL,
  PRIMARY KEY (artifact_id, chunk_id, model)
);

CREATE TABLE task_context_cache (
  task_id TEXT NOT NULL, context_hash TEXT NOT NULL, generated_at TEXT NOT NULL,
  included_artifacts_json TEXT NOT NULL, excluded_artifacts_json TEXT,
  summary TEXT, token_estimate INTEGER, valid_until_event_seq INTEGER,
  PRIMARY KEY (task_id, context_hash)
);
"""


@dataclass(frozen=True)
class SourceArtifact:
    path: Path
    relative_path: str
    artifact_type: str
    artifact_id: str
    data: bytes
    frontmatter: dict[str, Any]
    metadata: dict[str, Any]


@dataclass(frozen=True)
class EdgeRecord:
    from_artifact_id: str
    to_artifact_id: str
    edge_type: str
    source_key: str


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_commit(root: Path, revision: str = "HEAD") -> str:
    try:
        commit = subprocess.check_output(
            ["git", "rev-parse", "--verify", f"{revision}^{{commit}}"],
            cwd=root, text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (FileNotFoundError, subprocess.CalledProcessError) as error:
        raise ValueError(f"cannot bind memory index to git commit {revision}") from error
    if not re.fullmatch(r"[0-9a-fA-F]{40}", commit):
        raise ValueError("git revision is not a full commit id")
    return commit


def git_head(root: Path) -> str:
    return git_commit(root)


def git_blob(root: Path, commit: str, relative_path: str) -> bytes:
    repository_path = f"{git_prefix(root)}{relative_path}"
    try:
        return subprocess.check_output(
            ["git", "show", f"{commit}:{repository_path}"], cwd=root,
            stderr=subprocess.DEVNULL,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as error:
        raise ValueError(
            f"cannot bind tracked source to git blob {commit}:{repository_path}"
        ) from error


def git_prefix(root: Path) -> str:
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "--show-prefix"], cwd=root, text=True,
            stderr=subprocess.DEVNULL,
        ).strip("\r\n")
    except (FileNotFoundError, subprocess.CalledProcessError) as error:
        raise ValueError("cannot resolve repository-relative source prefix") from error


def ledger_lock_is_idle(lock_path: Path) -> bool:
    """Probe the persistent writer lock without blocking or deleting it."""
    if not lock_path.exists():
        return True
    with lock_path.open("r+b") as handle:
        if sys.platform == "win32":
            import msvcrt

            handle.seek(0)
            try:
                msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError:
                return False
            handle.seek(0)
            msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            return True
        import fcntl

        try:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except OSError:
            return False
        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
        return True


def parse_complete_jsonl(data: bytes) -> list[dict[str, Any]]:
    """Parse complete JSONL records and tolerate one torn final append."""
    events: list[dict[str, Any]] = []
    for line_number, raw in enumerate(data.splitlines(keepends=True), start=1):
        if not raw.endswith(b"\n"):
            break
        text = raw.rstrip(b"\r\n")
        if not text:
            continue
        try:
            event = json.loads(text.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError(f"invalid complete events.jsonl record {line_number}") from error
        if not isinstance(event, dict):
            raise ValueError(f"events.jsonl record {line_number} is not an object")
        events.append(event)
    return events


def read_events_torn_safe(
    root: Path,
    attempts: int = 5,
    backoff_seconds: float = 0.02,
) -> list[dict[str, Any]]:
    """Read the event canon without writing it or waiting on its writer lock."""
    events_path = root.resolve() / EVENTS_PATH
    lock_path = root.resolve() / LEDGER_LOCK_PATH
    if not events_path.exists():
        return []
    for attempt in range(attempts):
        if not ledger_lock_is_idle(lock_path):
            if attempt + 1 < attempts:
                time.sleep(backoff_seconds * (attempt + 1))
                continue
            raise ValueError("event ledger writer is busy")
        before = events_path.stat()
        data = events_path.read_bytes()
        after = events_path.stat()
        if (
            before.st_size == after.st_size
            and before.st_mtime_ns == after.st_mtime_ns
        ):
            return parse_complete_jsonl(data)
        if attempt + 1 < attempts:
            time.sleep(backoff_seconds * (attempt + 1))
    raise ValueError("event ledger changed during every read attempt")


def git_tree_paths(root: Path, commit: str) -> list[str]:
    prefix = git_prefix(root)
    pathspec = f":(top){prefix}" if prefix else ":(top)"
    try:
        output = subprocess.check_output(
            [
                "git", "ls-tree", "-r", "--full-name", "--name-only", "-z",
                commit, "--", pathspec,
            ],
            cwd=root,
            stderr=subprocess.DEVNULL,
        )
    except (FileNotFoundError, subprocess.CalledProcessError) as error:
        raise ValueError(f"cannot list tracked sources at git commit {commit}") from error
    paths: list[str] = []
    for raw in sorted(item for item in output.split(b"\0") if item):
        repository_path = raw.decode("utf-8")
        if prefix and not repository_path.startswith(prefix):
            raise ValueError(f"git source escaped instance prefix: {repository_path}")
        paths.append(repository_path[len(prefix):])
    return paths


def parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if not value:
        return ""
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [parse_scalar(item) for item in inner.split(",")]
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {'"', "'"}:
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> dict[str, Any]:
    normalized = text.replace("\r\n", "\n")
    if not normalized.startswith("---\n"):
        return {}
    end = normalized.find("\n---\n", 4)
    if end < 0:
        return {}
    result: dict[str, Any] = {}
    active_list: str | None = None
    for line in normalized[4:end].splitlines():
        if line.startswith("  - ") and active_list:
            if result.get(active_list) == "":
                result[active_list] = []
            if isinstance(result.get(active_list), list):
                result[active_list].append(parse_scalar(line[4:]))
            continue
        if line.startswith((" ", "\t")) or ":" not in line:
            active_list = None
            continue
        key, raw = line.split(":", 1)
        key = key.strip()
        value = parse_scalar(raw)
        result[key] = value
        active_list = key if value == "" else None
    return result


def instance_config(root: Path, commit: str) -> dict[str, Any]:
    config = json.loads(git_blob(root, commit, "protocol.config.json").decode("utf-8-sig"))
    if not isinstance(config, dict):
        raise ValueError("protocol.config.json must contain a JSON object")
    return config


def memory_index_policy(root: Path, commit: str) -> dict[str, Any]:
    policy = json.loads(git_blob(root, commit, POLICY_PATH).decode("utf-8-sig"))
    if not isinstance(policy, dict) or policy.get("schema_version") != 1:
        raise ValueError(f"{POLICY_PATH} must use schema_version 1")
    allowed = {
        "schema_version", "domain_pii_terms", "identity_aliases",
        "extra_status_values", "extra_type_values", "decision_policy_state",
        "revive_pack",
    }
    if set(policy) - allowed:
        raise ValueError(f"{POLICY_PATH} contains unknown keys")
    for key, limit in (("domain_pii_terms", 128), ("identity_aliases", 128)):
        values = policy.get(key)
        if not isinstance(values, list) or len(values) > limit:
            raise ValueError(f"{POLICY_PATH}.{key} must be a bounded array")
        if not all(
            isinstance(value, str)
            and 0 < len(value) <= 100
            and value.isprintable()
            and value == value.strip()
            for value in values
        ):
            raise ValueError(f"{POLICY_PATH}.{key} contains an invalid value")
        if len(set(values)) != len(values):
            raise ValueError(f"{POLICY_PATH}.{key} contains duplicates")
    for key, core_values, label in (
        ("extra_status_values", CORE_STATUS_VALUES, "status"),
        ("extra_type_values", TYPE_VALUES, "type"),
    ):
        values = policy.setdefault(key, [])
        if not isinstance(values, list) or len(values) > 128:
            raise ValueError(f"{POLICY_PATH}.{key} must be a bounded array")
        if not all(
            isinstance(value, str)
            and 0 < len(value) <= 100
            and value.isprintable()
            and value == value.strip()
            for value in values
        ):
            raise ValueError(f"{POLICY_PATH}.{key} contains an invalid value")
        if len(set(values)) != len(values):
            raise ValueError(f"{POLICY_PATH}.{key} contains duplicates")
        if set(values) & core_values:
            raise ValueError(f"{POLICY_PATH}.{key} duplicates core {label} values")
    revive = policy.get("revive_pack")
    if not isinstance(revive, dict) or set(revive) != {
        "max_bytes", "max_inline_source_bytes", "chars_per_token"
    }:
        raise ValueError(f"{POLICY_PATH}.revive_pack has an invalid shape")
    for key in ("max_bytes", "max_inline_source_bytes", "chars_per_token"):
        if not isinstance(revive.get(key), int) or revive[key] <= 0:
            raise ValueError(f"{POLICY_PATH}.revive_pack.{key} must be a positive integer")
    if revive["max_bytes"] > 1_048_576 or revive["max_inline_source_bytes"] > revive["max_bytes"]:
        raise ValueError(f"{POLICY_PATH}.revive_pack exceeds the bounded limits")
    decision_state = policy.setdefault(
        "decision_policy_state",
        {
            "current": "active",
            "non_current": "superseded",
            "non_current_when": "superseded_by_present_or_status_declared_non_current",
            "current_statuses": ["accepted", "active", "approved"],
            "non_current_statuses": [
                "archived", "cancelled", "draft", "proposed", "rejected", "superseded",
            ],
            "missing_status": "current_with_warning",
        },
    )
    if not isinstance(decision_state, dict) or set(decision_state) != {
        "current", "non_current", "non_current_when", "current_statuses",
        "non_current_statuses", "missing_status",
    }:
        raise ValueError(
            f"{POLICY_PATH}.decision_policy_state has an invalid shape"
        )
    if (
        decision_state["current"] != "active"
        or decision_state["non_current"] != "superseded"
        or decision_state["non_current_when"]
        != "superseded_by_present_or_status_declared_non_current"
        or decision_state["missing_status"] != "current_with_warning"
    ):
        raise ValueError(
            f"{POLICY_PATH}.decision_policy_state must map explicit supersession "
            "or a declared non-current status to non-current"
        )
    current_statuses = decision_state["current_statuses"]
    non_current_statuses = decision_state["non_current_statuses"]
    declared_statuses = (current_statuses, non_current_statuses)
    if (
        any(not isinstance(values, list) or not values or len(values) > 32 for values in declared_statuses)
        or not all(
            isinstance(value, str)
            and 0 < len(value) <= 100
            and value.isprintable()
            and value == value.strip()
            and value == value.casefold()
            for values in declared_statuses for value in values
        )
        or any(len(set(values)) != len(values) for values in declared_statuses)
        or set(current_statuses) & set(non_current_statuses)
    ):
        raise ValueError(
            f"{POLICY_PATH}.decision_policy_state status classes must be "
            "non-empty disjoint bounded arrays of unique lowercase strings"
        )
    return policy


def configured_agents(
    root: Path,
    commit: str,
    policy: dict[str, Any] | None = None,
) -> set[str]:
    config = instance_config(root, commit)
    agents = {
        str(item["id"])
        for item in config.get("agent_registry", {}).get("agents", [])
        if isinstance(item, dict) and item.get("id")
    }
    human_owner = config.get("agent_roles", {}).get("human_owner")
    if isinstance(human_owner, str) and human_owner:
        agents.add(human_owner)
    if policy is None:
        policy = memory_index_policy(root, commit)
    agents.update(str(item) for item in policy["identity_aliases"])
    return agents


def configured_status_values(policy: dict[str, Any]) -> frozenset[str]:
    decision_state = policy["decision_policy_state"]
    return (
        CORE_STATUS_VALUES
        | frozenset(policy["extra_status_values"])
        | frozenset(decision_state["current_statuses"])
        | frozenset(decision_state["non_current_statuses"])
    )


def configured_type_values(policy: dict[str, Any]) -> frozenset[str]:
    return frozenset(TYPE_VALUES) | frozenset(policy["extra_type_values"])


def configured_project(root: Path, commit: str) -> str:
    project = instance_config(root, commit).get("project_name")
    if not isinstance(project, str) or not project or len(project) > 200 or not project.isprintable():
        raise ValueError("protocol.config.json.project_name must be non-empty printable text")
    return project


def value_list(value: Any) -> list[str]:
    if isinstance(value, list):
        return [str(item).strip() for item in value if str(item).strip()]
    if value in (None, ""):
        return []
    return [str(value).strip()]


def title_is_safe(value: str, domain_pii_terms: Iterable[str]) -> bool:
    return (
        0 < len(value) <= TITLE_MAX_LENGTH
        and value.isprintable()
        and not contains_pii(value, domain_pii_terms)
    )


COORDINATE_ID_ENVELOPE_RE = re.compile(
    r"^(?:(?:TASK|DECISION|SPEC)-\d{4}|REQ-[0-9A-F]{8,})(?:-|$)",
    re.I | re.ASCII,
)
COORDINATE_ACTOR_ARTIFACT_RE = re.compile(
    r"^[A-Z][A-Z0-9]*-(?=(?:TASK|DECISION|SPEC)-\d{4}(?:-|$))",
    re.I | re.ASCII,
)
COORDINATE_MESSAGE_ENVELOPE_RE = re.compile(
    r"^MSG-(?:19|20)\d{6}(?:T(?:[01]\d|2[0-3])[0-5]\d[0-5]\dZ"
    r"|-(?:[01]\d|2[0-3])[0-5]\d[0-5]\d)?-[A-Z][A-Z0-9]*"
    r"(?:-to-[A-Z][A-Z0-9]*)?(?:-[A-Z]+)?(?:-|$)",
    re.I | re.ASCII,
)
COORDINATE_COMPLETE_OPERATIONAL_ID_RE = re.compile(
    r"^[A-Z][A-Z0-9]*(?:-[A-Z][A-Z0-9]*(?:\.\d+)*)+-(?:19|20)\d{6}$",
    re.I | re.ASCII,
)


def unexplained_identity_parts(value: str, *, message: bool = False) -> tuple[str, ...]:
    if COORDINATE_COMPLETE_OPERATIONAL_ID_RE.fullmatch(value):
        return ()
    remainder = value
    if message:
        envelope = COORDINATE_MESSAGE_ENVELOPE_RE.match(remainder)
        if envelope is None:
            return (value,)
        remainder = remainder[envelope.end():]
    else:
        actor_envelope = COORDINATE_ACTOR_ARTIFACT_RE.match(remainder)
        if actor_envelope is not None:
            remainder = remainder[actor_envelope.end():]
        envelope = COORDINATE_ID_ENVELOPE_RE.match(remainder)
        if envelope is None:
            return (value,)
        remainder = remainder[envelope.end():]

    if re.fullmatch(r"(?:TASK|DECISION|SPEC)\d{4}", remainder, re.I | re.ASCII):
        return ()
    return (remainder,) if remainder else ()


def pii_values_for_coordinate(item: str, coordinate: str | None) -> tuple[str, ...]:
    if coordinate in {
        "task_id", "decision_id", "spec_id", "relates_to", "linked_decisions",
        "supersedes", "superseded_by",
    }:
        return unexplained_identity_parts(item)
    if coordinate == "message_id":
        return unexplained_identity_parts(item, message=True)
    if coordinate in {"file", "path"}:
        if not PATH_RE.fullmatch(item) or ".." in Path(item).parts:
            return (item,)
        values: list[str] = []
        for segment in re.split(r"[/\\]+", item):
            candidate_stem, suffix = os.path.splitext(segment)
            stem = candidate_stem if suffix.lower() in TEXT_SUFFIXES else segment
            if not stem:
                continue
            explained = unexplained_identity_parts(stem)
            values.extend(explained if explained != (stem,) else (stem,))
        return tuple(values)
    return (item,)


def account_identifier_grouped_is_detected(value: str, *, coordinate_bound: bool) -> bool:
    for start in ACCOUNT_IDENTIFIER_START_RE.finditer(value):
        candidate = STRUCTURAL_PII_PATTERNS[1].match(value, start.start())
        if (
            candidate is not None
            and coordinate_bound
            and start.start()
            and value[start.start() - 1].isalnum()
        ):
            compact = ACCOUNT_IDENTIFIER_SEPARATORS_RE.sub("", candidate.group(0))
            if (
                value[start.start() - 1].isascii()
                and value[start.start() - 1].isupper()
            ) or (
                not re.match(r"^[A-Z]{2}\d{2}", compact, re.I | re.ASCII)
                or sum(char.isdigit() for char in compact) < 8
            ):
                continue
        if candidate is not None and account_identifier_candidate_has_valid_prefix(
            candidate.group(0), value[candidate.end():candidate.end() + 1]
        ):
            return True
    return False


def phone_number_is_detected(value: str, *, coordinate_bound: bool) -> bool:
    for candidate in PHONE_CANDIDATE_RE.finditer(value):
        if coordinate_bound:
            previous = value[candidate.start() - 1:candidate.start()]
            following = value[candidate.end():candidate.end() + 1]
            if (previous and previous.isalnum()) or (following and following.isalnum()):
                continue
        if 9 <= len(re.sub(r"\D", "", candidate.group(0))) <= 15:
            return True
    return False


def non_phone_pii_is_detected(
    item: str,
    domain_patterns: tuple[re.Pattern[str], ...],
    coordinate: str | None,
) -> bool:
    normalized = re.sub(r"[_/\\.-]+", " ", item)
    account_coordinate_bound = coordinate is not None
    if (
        account_identifier_contiguous_is_bounded(item)
        or account_identifier_grouped_is_detected(
            item, coordinate_bound=account_coordinate_bound
        )
    ):
        return True
    pii_values = pii_values_for_coordinate(item, coordinate)
    if STRUCTURAL_PII_PATTERNS[0].search(item):
        return True
    if (
        any(account_identifier_contiguous_is_bounded(candidate) for candidate in pii_values)
        or any(
            account_identifier_grouped_is_detected(
                pii_value, coordinate_bound=account_coordinate_bound
            )
            for pii_value in pii_values
        )
    ) or STRUCTURAL_PII_PATTERNS[2].search(normalized):
        return True
    return any(pattern.search(normalized) for pattern in domain_patterns)


def contains_pii(
    value: Any,
    domain_pii_terms: Iterable[str],
    *,
    coordinate: str | None = None,
) -> bool:
    domain_patterns = tuple(
        re.compile(rf"\b{re.escape(term)}\b", re.I) for term in domain_pii_terms
    )
    items = value_list(value)
    if any(non_phone_pii_is_detected(item, domain_patterns, coordinate) for item in items):
        return True
    coordinate_bound = False
    for item in items:
        if not DATE_RE.fullmatch(item) and any(
            phone_number_is_detected(pii_value, coordinate_bound=coordinate_bound)
            for pii_value in pii_values_for_coordinate(item, coordinate)
        ):
            return True
    return False


def validate_metadata(
    frontmatter: dict[str, Any],
    agents: set[str],
    domain_pii_terms: Iterable[str],
    status_values: Iterable[str] = CORE_STATUS_VALUES,
    type_values: Iterable[str] = TYPE_VALUES,
) -> tuple[dict[str, Any], list[str]]:
    accepted: dict[str, Any] = {}
    warnings: list[str] = []
    id_keys = {"task_id", "decision_id", "spec_id", "message_id"}
    relationship_keys = {"relates_to", "linked_decisions", "supersedes", "superseded_by"}
    for key in sorted(ALLOWLIST_KEYS & set(frontmatter)):
        value = frontmatter[key]
        valid = True
        if key in id_keys:
            valid = isinstance(value, str) and bool(ID_RE.fullmatch(value))
        elif key in relationship_keys:
            values = value_list(value)
            valid = (isinstance(value, list) or bool(values)) and all(
                ID_RE.fullmatch(item) for item in values
            )
            value = values
        elif key == "applies_to":
            values = value_list(value)
            valid = bool(values) and all(
                item in agents or item in {"*", "all"} for item in values
            )
            value = values
        elif key in {"created_at", "updated_at", "closed_at"}:
            valid = isinstance(value, str) and bool(DATE_RE.fullmatch(value))
        elif key in {"owner", "from", "to"}:
            valid = isinstance(value, str) and value in agents
        elif key == "title":
            valid = isinstance(value, str) and title_is_safe(value, domain_pii_terms)
        elif key == "status":
            valid = isinstance(value, str) and value in status_values
        elif key == "type":
            valid = isinstance(value, str) and value in type_values
        elif key == "priority":
            valid = isinstance(value, str) and value in PRIORITY_VALUES
        elif key == "phase":
            valid = isinstance(value, str) and bool(re.fullmatch(r"P[0-9]+", value))
        elif key == "file":
            valid = isinstance(value, str) and bool(PATH_RE.fullmatch(value)) and ".." not in Path(value).parts
            if valid:
                value = value.replace("\\", "/")
        if valid and contains_pii(value, domain_pii_terms, coordinate=key):
            valid = False
        if valid:
            accepted[key] = value
        else:
            warnings.append(f"rejected frontmatter key {key}")
    return accepted, warnings


def artifact_type_for(relative_path: str) -> str:
    mappings = (
        ("Area_comun/tasks/", "task"),
        ("Area_comun/decisions/", "decision"),
        ("Area_comun/specs/", "spec"),
        ("Area_comun/handoffs/", "handoff"),
        ("Area_comun/mailbox/", "mailbox"),
        ("Area_comun/reports/", "report"),
        ("Area_comun/artifacts/", "artifact"),
        ("Area_comun/requirements/", "requirement"),
        ("Area_comun/state/", "state_snapshot"),
        ("personal/", "memory"),
        ("runtime/state/", "eventlog"),
    )
    for prefix, artifact_type in mappings:
        if relative_path.startswith(prefix):
            return artifact_type
    return "artifact"


def artifact_id_for(artifact_type: str, relative_path: str, frontmatter: dict[str, Any]) -> str:
    key = INTRINSIC_ID_KEYS.get(artifact_type)
    if (
        key
        and isinstance(frontmatter.get(key), str)
        and ID_RE.fullmatch(frontmatter[key])
        and "XXXX" not in frontmatter[key].split("-")
    ):
        return str(frontmatter[key])
    return f"{artifact_type}:{relative_path}"


def is_excluded(relative_path: str) -> bool:
    path = Path(relative_path)
    parts = path.parts
    name = path.name.lower()
    if relative_path.startswith(("examples/", ".protocol-tmp/", "runtime/memory/", "protocol-secrets/")):
        return True
    if any(part in {".git", "__pycache__"} for part in parts):
        return True
    if (
        ".template." in name
        or re.search(r"(?:^|_)template(?:\.|$)", name)
        or name.endswith(tuple(SECRET_SUFFIXES))
        or name.startswith(".env")
    ):
        return True
    return relative_path == "event-state.runtime.json"


def iter_source_paths(root: Path, commit: str) -> Iterable[tuple[Path, str]]:
    for relative in git_tree_paths(root, commit):
        governed = relative in {"AGENTS.md", "protocol.config.json"} or relative.startswith(
            ("Area_comun/", "personal/", "runtime/state/")
        )
        if governed and not is_excluded(relative) and Path(relative).suffix.lower() in TEXT_SUFFIXES:
            yield root / Path(relative), relative


def derive_agent_id(relative_path: str, declared_agent_id: str | None = None) -> str:
    match = re.fullmatch(r"personal/([^/]+)/.+", relative_path)
    if not match:
        raise ValueError(f"agent memory outside personal/<id>: {relative_path}")
    derived = match.group(1)
    if declared_agent_id is not None and declared_agent_id != derived:
        raise ValueError(f"agent_id mismatch for {relative_path}: {declared_agent_id} != {derived}")
    return derived


def load_artifacts(root: Path, commit: str) -> tuple[list[SourceArtifact], list[str]]:
    policy = memory_index_policy(root, commit)
    agents = configured_agents(root, commit, policy)
    status_values = configured_status_values(policy)
    type_values = configured_type_values(policy)
    domain_pii_terms = policy["domain_pii_terms"]
    artifacts: list[SourceArtifact] = []
    warnings: list[str] = []
    seen_ids: dict[str, str] = {}
    for path, relative in iter_source_paths(root, commit):
        data = git_blob(root, commit, relative)
        text = data.decode("utf-8-sig", errors="replace")
        frontmatter = parse_frontmatter(text)
        artifact_type = artifact_type_for(relative)
        if artifact_type == "memory":
            declared = frontmatter.get("agent_id")
            derive_agent_id(relative, str(declared) if declared is not None else None)
        metadata, item_warnings = validate_metadata(
            frontmatter, agents, domain_pii_terms, status_values, type_values
        )
        if artifact_type == "decision":
            status = metadata.get("status")
            classified = (
                set(policy["decision_policy_state"]["current_statuses"])
                | set(policy["decision_policy_state"]["non_current_statuses"])
            )
            if status is None:
                item_warnings.append(
                    "decision currentness status is missing; attested policy treats it as current"
                )
            elif status.casefold() not in classified:
                raise ValueError(
                    f"{relative}: decision currentness status {status!r} is not classified "
                    f"by {POLICY_PATH}"
                )
        artifact_id = artifact_id_for(artifact_type, relative, metadata)
        if artifact_id in seen_ids:
            raise ValueError(f"duplicate artifact_id {artifact_id}: {seen_ids[artifact_id]} and {relative}")
        warnings.extend(f"{relative}: {warning}" for warning in item_warnings)
        artifacts.append(SourceArtifact(path, relative, artifact_type, artifact_id, data, frontmatter, metadata))
        seen_ids[artifact_id] = relative
    return artifacts, warnings


def file_target_id(value: str) -> str:
    return f"artifact:{value}"


def validate_f1_edge_type(edge_type: str) -> None:
    if edge_type not in set(EDGE_PRODUCERS.values()):
        raise ValueError(f"edge_type has no F1 producer: {edge_type}")


def extract_edges(artifact: SourceArtifact) -> list[EdgeRecord]:
    records: set[EdgeRecord] = set()
    metadata = artifact.metadata
    for key in ("relates_to", "linked_decisions", "supersedes"):
        for target in value_list(metadata.get(key)):
            records.add(EdgeRecord(artifact.artifact_id, target, EDGE_PRODUCERS[key], key))
    for superseder in value_list(metadata.get("superseded_by")):
        records.add(EdgeRecord(superseder, artifact.artifact_id, "supersedes", "superseded_by"))
    if artifact.artifact_type == "task" and isinstance(metadata.get("file"), str):
        records.add(EdgeRecord(artifact.artifact_id, file_target_id(metadata["file"]), "implements", "file"))
    for record in records:
        validate_f1_edge_type(record.edge_type)
    return sorted(records, key=lambda item: (item.from_artifact_id, item.to_artifact_id, item.edge_type))


def deterministic_summary(metadata: dict[str, Any]) -> str | None:
    fields: list[str] = []
    for key in ("title", "status", "type", "task_id", "decision_id", "spec_id", "message_id"):
        value = metadata.get(key)
        if isinstance(value, str) and value:
            fields.append(f"{key}={value}")
    return "; ".join(fields) if fields else None


def metadata_terms(artifact_id: str, metadata: dict[str, Any]) -> list[tuple[str, str]]:
    terms: set[tuple[str, str]] = {(artifact_id.lower(), "artifact_id")}
    for key in ("title", "status", "type", "task_id", "decision_id", "spec_id", "message_id"):
        value = metadata.get(key)
        if isinstance(value, str):
            for term in re.findall(r"[A-Za-z0-9][A-Za-z0-9._-]*", value.lower()):
                terms.add((term, key))
    return sorted(terms)


def require_safe_text(
    value: Any,
    field: str,
    *,
    domain_pii_terms: Iterable[str],
    pii_check: bool = True,
) -> str:
    if not isinstance(value, str) or not value or any(ord(char) > 127 for char in value):
        raise ValueError(f"{field} must be non-empty ASCII text")
    if pii_check and contains_pii(value, domain_pii_terms, coordinate=field):
        raise ValueError(f"{field} contains prohibited PII")
    return value


def load_cold_packs(root: Path, commit: str) -> list[tuple[Any, ...]]:
    domain_pii_terms = memory_index_policy(root, commit)["domain_pii_terms"]
    rows: list[tuple[Any, ...]] = []
    seen: set[str] = set()
    for relative in git_tree_paths(root, commit):
        if not (
            relative.startswith("Area_comun/archive/")
            and relative.endswith("pack.manifest.json")
        ):
            continue
        data = git_blob(root, commit, relative)
        try:
            payload = json.loads(data.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError(f"invalid cold-pack manifest: {relative}") from error
        if not isinstance(payload, dict):
            raise ValueError(f"cold-pack manifest must be an object: {relative}")
        header = payload.get("pack", payload)
        if not isinstance(header, dict):
            raise ValueError(f"cold-pack header must be an object: {relative}")
        artifacts = payload.get("artifacts", [])
        if not isinstance(artifacts, list) or not all(
            isinstance(item, dict) for item in artifacts
        ):
            raise ValueError(f"cold-pack artifacts must be objects: {relative}")
        pack_id = require_safe_text(
            header.get("pack_id"), "pack_id", domain_pii_terms=domain_pii_terms
        )
        if pack_id in seen:
            raise ValueError(f"duplicate cold-pack id: {pack_id}")
        pack_type = require_safe_text(
            header.get("pack_type"), "pack_type", domain_pii_terms=domain_pii_terms
        )
        path = require_safe_text(
            header.get("path"), "path", domain_pii_terms=domain_pii_terms
        ).replace("\\", "/")
        raw_git_ref = header.get("git_ref")
        git_ref = require_safe_text(
            raw_git_ref, "git_ref", domain_pii_terms=domain_pii_terms,
            pii_check=git_ref_requires_pii_check(raw_git_ref),
        )
        created_at = require_safe_text(
            header.get("created_at"), "created_at",
            domain_pii_terms=domain_pii_terms, pii_check=False
        )
        if not DATE_RE.fullmatch(created_at):
            raise ValueError(f"invalid cold-pack created_at: {created_at}")
        if not PATH_RE.fullmatch(path) or ".." in Path(path).parts:
            raise ValueError(f"invalid cold-pack path: {path}")
        rows.append(
            (
                pack_id,
                pack_type,
                path,
                git_ref,
                created_at,
                sha256_bytes(data),
                len(artifacts),
            )
        )
        seen.add(pack_id)
    return sorted(rows)


def load_hot_cold_rules(root: Path, commit: str) -> list[tuple[Any, ...]]:
    if RULES_PATH not in set(git_tree_paths(root, commit)):
        return []
    data = git_blob(root, commit, RULES_PATH)
    try:
        payload = json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid canonical hot/cold rules: {RULES_PATH}") from error
    rules = payload.get("rules") if isinstance(payload, dict) else payload
    if not isinstance(rules, list) or not all(isinstance(item, dict) for item in rules):
        raise ValueError("canonical hot/cold rules require a rules object array")
    rows: list[tuple[Any, ...]] = []
    seen: set[str] = set()
    domain_pii_terms = memory_index_policy(root, commit)["domain_pii_terms"]
    for item in rules:
        rule_id = require_safe_text(
            item.get("rule_id"), "rule_id", domain_pii_terms=domain_pii_terms
        )
        if rule_id in seen:
            raise ValueError(f"duplicate hot/cold rule id: {rule_id}")
        artifact_type = require_safe_text(
            item.get("artifact_type"), "artifact_type",
            domain_pii_terms=domain_pii_terms,
        )
        if artifact_type not in ARTIFACT_TYPES:
            raise ValueError(f"invalid rule artifact_type: {artifact_type}")
        selector = require_safe_text(
            item.get("selector"), "selector", domain_pii_terms=domain_pii_terms
        )
        target = require_safe_text(
            item.get("target_retention_class"), "target_retention_class",
            domain_pii_terms=domain_pii_terms,
        )
        if target not in {"hot", "warm", "cold", "sealed", "do_not_archive"}:
            raise ValueError(f"invalid target_retention_class: {target}")
        window_days = item.get("window_days")
        window_count = item.get("window_count")
        for field, value in (
            ("window_days", window_days),
            ("window_count", window_count),
        ):
            if value is not None and (not isinstance(value, int) or value < 0):
                raise ValueError(f"{field} must be a non-negative integer or null")
        bool_values: list[int] = []
        for field in (
            "requires_stub", "requires_active_policy_check", "enabled"
        ):
            value = item.get(field, 0)
            if value not in (0, 1, False, True):
                raise ValueError(f"{field} must be boolean")
            bool_values.append(int(value))
        decision = item.get("created_by_decision")
        if decision is not None:
            decision = require_safe_text(
                decision, "created_by_decision", domain_pii_terms=domain_pii_terms
            )
        if bool_values[2] and not decision:
            raise ValueError("enabled hot/cold rule requires created_by_decision")
        rows.append(
            (
                rule_id, artifact_type, selector, target, window_days,
                window_count, *bool_values, decision,
            )
        )
        seen.add(rule_id)
    return sorted(rows)


def decision_policy_state(metadata: dict[str, Any], policy: dict[str, Any]) -> str:
    """A decision is current unless supersession or its status says otherwise."""
    mapping = policy["decision_policy_state"]
    status = metadata.get("status")
    if status is None:
        return mapping["current"]
    normalized = status.casefold() if isinstance(status, str) else ""
    if normalized not in set(mapping["current_statuses"]) | set(mapping["non_current_statuses"]):
        raise ValueError(f"decision currentness status {status!r} is not classified")
    declared_non_current = (
        isinstance(status, str)
        and normalized in mapping["non_current_statuses"]
    )
    return (
        mapping["non_current"]
        if value_list(metadata.get("superseded_by")) or declared_non_current
        else mapping["current"]
    )


def policy_row(
    artifact: SourceArtifact, policy: dict[str, Any]
) -> tuple[Any, ...] | None:
    if artifact.artifact_type != "decision":
        return None
    policy_state = decision_policy_state(artifact.metadata, policy)
    superseded_by = value_list(artifact.metadata.get("superseded_by"))
    supersedes = value_list(artifact.metadata.get("supersedes"))
    applies_to = value_list(artifact.metadata.get("applies_to"))
    return (
        artifact.artifact_id,
        policy_state,
        superseded_by[0] if superseded_by else None,
        json.dumps(supersedes, separators=(",", ":")) if supersedes else None,
        artifact.metadata.get("created_at"),
        artifact.metadata.get("closed_at"),
        json.dumps(applies_to, separators=(",", ":")) if applies_to else None,
        int(policy_state == policy["decision_policy_state"]["current"]),
        None,
    )


def init_db(connection: sqlite3.Connection) -> None:
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(DDL)
    connection.execute(f"PRAGMA user_version = {SCHEMA_VERSION}")


def validate_existing_db(connection: sqlite3.Connection) -> None:
    connection.execute("PRAGMA foreign_keys = ON")
    version = connection.execute("PRAGMA user_version").fetchone()[0]
    if version != SCHEMA_VERSION:
        raise ValueError(
            f"existing memory DB schema version must be {SCHEMA_VERSION}, found {version}"
        )
    expected = {
        "artifacts", "artifact_edges", "agent_memory", "cold_packs",
        "retrieval_log", "artifact_versions", "artifact_content_index",
        "policy_status", "hot_cold_rules", "stubs", "validation_runs",
        "pii_classification", "search_terms", "embeddings",
        "task_context_cache",
    }
    actual = {
        row[0]
        for row in connection.execute(
            "SELECT name FROM sqlite_master "
            "WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
    }
    if actual != expected:
        raise ValueError("existing memory DB does not match the SPEC v1 table set")


def build(
    root: Path,
    db_path: Path = DB_PATH,
    *,
    rebuild: bool = False,
    at: str = "HEAD",
) -> dict[str, Any]:
    root = root.resolve()
    commit = git_commit(root, at)
    db_absolute = (db_path if db_path.is_absolute() else root / db_path).resolve()
    expected_db = (root / DB_PATH).resolve()
    if db_absolute != expected_db:
        raise ValueError(f"database target must be {expected_db}")
    project = configured_project(root, commit)
    policy = memory_index_policy(root, commit)
    artifacts, warnings = load_artifacts(root, commit)
    events = read_events_torn_safe(root)
    cold_packs = load_cold_packs(root, commit)
    hot_cold_rules = load_hot_cold_rules(root, commit)
    db_absolute.parent.mkdir(parents=True, exist_ok=True)
    existed = db_absolute.exists()
    if rebuild and existed:
        db_absolute.unlink()
    connection = sqlite3.connect(db_absolute)
    try:
        if rebuild or not existed:
            init_db(connection)
        else:
            validate_existing_db(connection)

        known_ids = {artifact.artifact_id for artifact in artifacts}
        if not rebuild and existed:
            existing_ids = {
                row[0] for row in connection.execute("SELECT artifact_id FROM artifacts")
            }
            connection.executemany(
                "DELETE FROM artifacts WHERE artifact_id=?",
                ((artifact_id,) for artifact_id in sorted(existing_ids - known_ids)),
            )

        # These tables are entirely derived. Replacing their rows inside the
        # incremental transaction preserves operational tables/columns while
        # converging to the same canonical partition as a fresh rebuild.
        for table in (
            "artifact_edges", "agent_memory", "policy_status", "stubs",
            "search_terms", "hot_cold_rules", "artifact_versions",
        ):
            connection.execute(f"DELETE FROM {table}")

        for artifact in artifacts:
            metadata = artifact.metadata
            digest = sha256_bytes(artifact.data)
            summary = deterministic_summary(metadata)
            connection.execute(
                """INSERT INTO artifacts(
                artifact_id,artifact_type,title,status,original_path,hot_path,git_commit,sha256,
                created_at,updated_at,closed_at,owner,project,is_active_policy,is_hot,is_pii_safe,
                summary_short,canonicality,retention_class,schema_version
                ) VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ON CONFLICT(artifact_id) DO UPDATE SET
                  artifact_type=excluded.artifact_type,
                  title=excluded.title,
                  status=excluded.status,
                  original_path=excluded.original_path,
                  hot_path=excluded.hot_path,
                  cold_path=excluded.cold_path,
                  git_commit=excluded.git_commit,
                  sha256=excluded.sha256,
                  created_at=excluded.created_at,
                  updated_at=excluded.updated_at,
                  closed_at=excluded.closed_at,
                  owner=excluded.owner,
                  project=excluded.project,
                  is_active_policy=excluded.is_active_policy,
                  is_hot=excluded.is_hot,
                  summary_short=excluded.summary_short,
                  summary_long=excluded.summary_long,
                  canonicality=excluded.canonicality,
                  retention_class=excluded.retention_class,
                  cold_reason=excluded.cold_reason,
                  schema_version=excluded.schema_version""",
                (
                    artifact.artifact_id, artifact.artifact_type, metadata.get("title"),
                    metadata.get("status"), artifact.relative_path, artifact.relative_path,
                    commit, digest, metadata.get("created_at"), metadata.get("updated_at"),
                    metadata.get("closed_at"), metadata.get("owner"), project, 0, 1,
                    None, summary, "canonical_file",
                    "do_not_archive" if artifact.artifact_type in {"state_snapshot", "eventlog"} else "hot",
                    SCHEMA_VERSION,
                ),
            )
            connection.execute(
                """INSERT INTO artifact_content_index(
                artifact_id,content_sha256,indexed_at,language,token_estimate,line_count,
                has_frontmatter,frontmatter_json,plain_text_excerpt,redaction_state
                ) VALUES(?,?,?,?,?,?,?,?,NULL,'unclassified')
                ON CONFLICT(artifact_id) DO UPDATE SET
                  content_sha256=excluded.content_sha256,
                  language=excluded.language,
                  token_estimate=excluded.token_estimate,
                  line_count=excluded.line_count,
                  has_frontmatter=excluded.has_frontmatter,
                  frontmatter_json=excluded.frontmatter_json""",
                (
                    artifact.artifact_id, digest, "1970-01-01T00:00:00Z", "und",
                    None, artifact.data.count(b"\n") + 1, int(bool(artifact.frontmatter)),
                    json.dumps(metadata, sort_keys=True, separators=(",", ":")),
                ),
            )
            if not rebuild:
                connection.execute(
                    """INSERT INTO pii_classification(
                    artifact_id,classifier_version,classified_at,pii_state,finding_count,
                    public_plane_allowed,redaction_required
                    ) VALUES(?,'none-f1','1970-01-01T00:00:00Z','not_scanned',0,0,0)
                    ON CONFLICT(artifact_id) DO NOTHING""",
                    (artifact.artifact_id,),
                )
            connection.execute(
                """INSERT INTO artifact_versions(
                artifact_id,version_id,git_commit,path_at_commit,sha256,status_at_version
                ) VALUES(?,1,?,?,?,?)""",
                (artifact.artifact_id, commit, artifact.relative_path, digest, metadata.get("status")),
            )
            if artifact.artifact_type == "memory":
                agent_id = derive_agent_id(artifact.relative_path)
                connection.execute(
                    """INSERT INTO agent_memory(
                    memory_id,agent_id,scope,summary,source_path,source_commit,sha256,
                    valid_from,valid_until,is_current
                    ) VALUES(?,?,'personal',?,?,?,?,?,?,?)""",
                    (
                        artifact.artifact_id,
                        agent_id,
                        summary,
                        artifact.relative_path,
                        commit,
                        digest,
                        metadata.get("updated_at") or metadata.get("created_at"),
                        metadata.get("closed_at"),
                        int(metadata.get("status") not in {"superseded", "archived"}),
                    ),
                )
            policy_status = policy_row(artifact, policy)
            if policy_status is not None:
                connection.execute(
                    """INSERT INTO policy_status(
                    decision_id,policy_state,superseded_by,supersedes,active_from,
                    active_until,applies_to,hot_required,reason
                    ) VALUES(?,?,?,?,?,?,?,?,?)""",
                    policy_status,
                )
            for term, field in metadata_terms(artifact.artifact_id, metadata):
                connection.execute(
                    "INSERT OR IGNORE INTO search_terms(artifact_id,term,field,weight,source) VALUES(?,?,?,1.0,'metadata_allowlist')",
                    (artifact.artifact_id, term, field),
                )
        for artifact in artifacts:
            for edge in extract_edges(artifact):
                if edge.from_artifact_id not in known_ids:
                    warnings.append(
                        f"{artifact.relative_path}: pending normalized source {edge.from_artifact_id} omitted"
                    )
                    continue
                connection.execute(
                    "INSERT OR IGNORE INTO artifact_edges(from_artifact_id,to_artifact_id,edge_type,source_path,source_commit) VALUES(?,?,?,?,?)",
                    (edge.from_artifact_id, edge.to_artifact_id, edge.edge_type, artifact.relative_path, commit),
                )
        current_pack_ids = {row[0] for row in cold_packs}
        if not rebuild and existed:
            existing_pack_ids = {
                row[0] for row in connection.execute("SELECT pack_id FROM cold_packs")
            }
            connection.executemany(
                "DELETE FROM cold_packs WHERE pack_id=?",
                ((pack_id,) for pack_id in sorted(existing_pack_ids - current_pack_ids)),
            )
        connection.executemany(
            """INSERT INTO cold_packs(
            pack_id,pack_type,path,git_ref,created_at,sha256_manifest,artifact_count
            ) VALUES(?,?,?,?,?,?,?)
            ON CONFLICT(pack_id) DO UPDATE SET
              pack_type=excluded.pack_type,
              path=excluded.path,
              git_ref=excluded.git_ref,
              created_at=excluded.created_at,
              sha256_manifest=excluded.sha256_manifest,
              artifact_count=excluded.artifact_count""",
            cold_packs,
        )
        connection.executemany(
            """INSERT INTO hot_cold_rules(
            rule_id,artifact_type,selector,target_retention_class,window_days,
            window_count,requires_stub,requires_active_policy_check,enabled,
            created_by_decision
            ) VALUES(?,?,?,?,?,?,?,?,?,?)""",
            hot_cold_rules,
        )
        if not rebuild:
            connection.execute(
                """INSERT INTO validation_runs(
                run_type,started_at,finished_at,actor,git_commit,result,warnings_json,checked_artifact_count
                ) VALUES('hot_fast','1970-01-01T00:00:00Z','1970-01-01T00:00:00Z','indexer',?,'pass',?,?)""",
                (commit, json.dumps(warnings, sort_keys=True), len(artifacts)),
            )
        connection.commit()
        foreign_keys = connection.execute("PRAGMA foreign_keys").fetchone()[0]
        user_version = connection.execute("PRAGMA user_version").fetchone()[0]
        table_count = connection.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        ).fetchone()[0]
        return {
            "artifact_count": len(artifacts),
            "cold_pack_count": len(cold_packs),
            "db_path": db_absolute.relative_to(root).as_posix() if db_absolute.is_relative_to(root) else str(db_absolute),
            "event_count": len(events),
            "foreign_keys": foreign_keys,
            "mode": "rebuild" if rebuild else "normal",
            "rules_count": len(hot_cold_rules),
            "schema_version": user_version,
            "table_count": table_count,
            "warnings": warnings,
        }
    except Exception:
        connection.close()
        if rebuild or not existed:
            db_absolute.unlink(missing_ok=True)
        raise
    finally:
        if connection:
            connection.close()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[2]))
    parser.add_argument("--db", default=str(DB_PATH))
    parser.add_argument("--at", default="HEAD")
    parser.add_argument("--rebuild", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    result = build(
        Path(args.root), Path(args.db), rebuild=args.rebuild, at=args.at
    )
    print(json.dumps(result, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
