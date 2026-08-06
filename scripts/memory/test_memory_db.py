#!/usr/bin/env python3
"""Acceptance tests for F1-U1/U2/U3 memory indexing, drift, and retrieval."""

from __future__ import annotations

import importlib.util
import json
import re
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
MODULE_PATH = Path(__file__).with_name("build_memory_db.py")
DUMP_MODULE_PATH = Path(__file__).with_name("dump_memory_db.py")
DRIFT_MODULE_PATH = Path(__file__).with_name("check_memory_db_drift.py")
QUERY_MODULE_PATH = Path(__file__).with_name("query_memory_db.py")
REVIVE_MODULE_PATH = Path(__file__).with_name("revive_pack.py")
SPEC = importlib.util.spec_from_file_location("build_memory_db", MODULE_PATH)
assert SPEC and SPEC.loader
memory_db = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = memory_db
SPEC.loader.exec_module(memory_db)
DUMP_SPEC = importlib.util.spec_from_file_location("dump_memory_db", DUMP_MODULE_PATH)
assert DUMP_SPEC and DUMP_SPEC.loader
dump_memory_db = importlib.util.module_from_spec(DUMP_SPEC)
sys.modules[DUMP_SPEC.name] = dump_memory_db
DUMP_SPEC.loader.exec_module(dump_memory_db)
DRIFT_SPEC = importlib.util.spec_from_file_location(
    "check_memory_db_drift", DRIFT_MODULE_PATH
)
assert DRIFT_SPEC and DRIFT_SPEC.loader
check_memory_db_drift = importlib.util.module_from_spec(DRIFT_SPEC)
sys.modules[DRIFT_SPEC.name] = check_memory_db_drift
DRIFT_SPEC.loader.exec_module(check_memory_db_drift)
QUERY_SPEC = importlib.util.spec_from_file_location(
    "query_memory_db", QUERY_MODULE_PATH
)
assert QUERY_SPEC and QUERY_SPEC.loader
query_memory_db = importlib.util.module_from_spec(QUERY_SPEC)
sys.modules[QUERY_SPEC.name] = query_memory_db
QUERY_SPEC.loader.exec_module(query_memory_db)
REVIVE_SPEC = importlib.util.spec_from_file_location("revive_pack", REVIVE_MODULE_PATH)
assert REVIVE_SPEC and REVIVE_SPEC.loader
revive_pack = importlib.util.module_from_spec(REVIVE_SPEC)
sys.modules[REVIVE_SPEC.name] = revive_pack
REVIVE_SPEC.loader.exec_module(revive_pack)


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(
        ["git", *args], cwd=root, text=True, stderr=subprocess.STDOUT
    ).strip()


def make_fixture(root: Path) -> None:
    config = {
        "project_name": "fixture-project",
        "agent_roles": {"human_owner": "Human"},
        "agent_registry": {
            "agents": [
                {"id": "Codex"}, {"id": "Arquitecto"}, {"id": "Analista"},
                {"id": "X"}, {"id": "Y"},
            ]
        }
    }
    write(root / "protocol.config.json", json.dumps(config))
    write(
        root / memory_db.POLICY_PATH,
        json.dumps(
            {
                "schema_version": 1,
                "domain_pii_terms": [],
                "identity_aliases": [],
                "revive_pack": {
                    "max_bytes": 131072,
                    "max_inline_source_bytes": 65536,
                    "chars_per_token": 4,
                },
            },
            sort_keys=True,
        )
        + "\n",
    )
    write(root / "AGENTS.md", "# Fixture\n")
    write(
        root / "runtime/state/events.jsonl",
        json.dumps({"seq": 1, "type": "fixture.created"}, separators=(",", ":"))
        + "\n",
    )
    write(root / ".gitignore", "runtime/memory/\n")
    git(root, "init", "--quiet")
    git(root, "config", "user.name", "Codex")
    git(root, "config", "user.email", "codex@local.invalid")
    git(root, "config", "core.autocrlf", "false")
    commit_fixture(root, "fixture base")


def commit_fixture(root: Path, message: str = "fixture update") -> str:
    git(root, "add", "-A")
    git(root, "commit", "--quiet", "-m", message)
    return git(root, "rev-parse", "HEAD")


def table_text_values(connection: sqlite3.Connection) -> str:
    values: list[str] = []
    tables = [
        row[0] for row in connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
    ]
    for table in tables:
        columns = [row[1] for row in connection.execute(f"PRAGMA table_info({table})") if row[2] == "TEXT"]
        if not columns:
            continue
        for row in connection.execute(f"SELECT {','.join(columns)} FROM {table}"):
            values.extend(str(value) for value in row if value is not None)
    return "\n".join(values)


class MemoryDbTests(unittest.TestCase):
    maxDiff = None

    def test_p01_domain_lexicon_is_external_and_empty_by_default(self) -> None:
        legacy_terms = ("sal" + "ary", "employ" + "ee", "i" + "ban")
        core = MODULE_PATH.read_text(encoding="utf-8").casefold()
        for term in legacy_terms:
            self.assertNotIn(term, core)
            self.assertFalse(memory_db.contains_pii(term))
            self.assertTrue(memory_db.contains_pii(term, [term]))

    def test_p02_project_is_derived_from_instance_config(self) -> None:
        with tempfile.TemporaryDirectory(prefix="memory-project-") as temp:
            root = Path(temp)
            make_fixture(root)
            memory_db.build(root)
            connection = sqlite3.connect(root / memory_db.DB_PATH)
            projects = {row[0] for row in connection.execute("SELECT DISTINCT project FROM artifacts")}
            connection.close()
            self.assertEqual({"fixture-project"}, projects)

    def test_p03_dump_format_is_protocol_neutral(self) -> None:
        self.assertEqual("protocol-memory-derived-v1", dump_memory_db.DUMP_FORMAT)
        self.assertNotIn("no" + "va", dump_memory_db.DUMP_FORMAT.casefold())

    def test_p04_module_documentation_is_product_neutral(self) -> None:
        source = MODULE_PATH.read_text(encoding="utf-8").casefold()
        for marker in ("ae" + "gis instance", "ze" + "us-protocol"):
            self.assertNotIn(marker, source)
        self.assertIn("superseded m6 prototype", source)

    def test_p05_protocol_timestamp_id_is_not_a_phone(self) -> None:
        self.assertFalse(
            memory_db.contains_pii("MSG-20260619-092823-Codex-to-Arquitecto")
        )
        self.assertTrue(memory_db.contains_pii("+34 612 345 678"))

    def test_p06_ids_accept_dots_but_remain_anchored(self) -> None:
        self.assertIsNotNone(memory_db.ID_RE.fullmatch("MSG-release-v0.10.0"))
        self.assertIsNone(memory_db.ID_RE.fullmatch("MSG-release-v0.10.0 extra"))
        self.assertIsNone(memory_db.ID_RE.fullmatch("msg-release-v0.10.0"))

    def test_p07_titles_accept_bounded_printable_unicode_and_keep_pii_gate(self) -> None:
        title = "Evaluación técnica " + ("a" * 210) + " con precisión"
        self.assertTrue(memory_db.title_is_safe(title))
        self.assertFalse(memory_db.title_is_safe("x" * (memory_db.TITLE_MAX_LENGTH + 1)))
        self.assertFalse(memory_db.title_is_safe("line\nbreak"))
        self.assertFalse(memory_db.title_is_safe("contact person@example.invalid"))

    def test_p08_identities_are_registry_human_owner_or_declared_aliases_only(self) -> None:
        with tempfile.TemporaryDirectory(prefix="memory-identities-") as temp:
            root = Path(temp)
            make_fixture(root)
            policy_path = root / memory_db.POLICY_PATH
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            policy["identity_aliases"] = ["Historical"]
            write(policy_path, json.dumps(policy, sort_keys=True) + "\n")
            commit = commit_fixture(root)
            agents = memory_db.configured_agents(root, commit)
            self.assertTrue({"Codex", "Human", "Historical"} <= agents)
            accepted, warnings = memory_db.validate_metadata(
                {"owner": "Historical", "from": "Human", "to": "Unknown"}, agents
            )
            self.assertEqual({"from": "Human", "owner": "Historical"}, accepted)
            self.assertEqual(["rejected frontmatter key to"], warnings)

    def test_p09_protocol_status_and_type_vocabularies_remain_finite(self) -> None:
        accepted, warnings = memory_db.validate_metadata(
            {"status": "ready_for_review", "type": "HANDOFF"}, {"Codex"}
        )
        self.assertEqual({"status": "ready_for_review", "type": "HANDOFF"}, accepted)
        self.assertEqual([], warnings)
        accepted, warnings = memory_db.validate_metadata(
            {"status": "arbitrary status", "type": "arbitrary type"}, {"Codex"}
        )
        self.assertEqual({}, accepted)
        self.assertEqual(
            ["rejected frontmatter key status", "rejected frontmatter key type"], warnings
        )

    def test_p10_template_conventions_and_placeholder_ids_are_excluded(self) -> None:
        self.assertTrue(memory_db.is_excluded("Area_comun/specs/SPEC_TEMPLATE.md"))
        self.assertTrue(memory_db.is_excluded("Area_comun/specs/SPEC.template.md"))
        fallback = memory_db.artifact_id_for(
            "spec", "Area_comun/specs/SPEC_TEMPLATE.md", {"spec_id": "SPEC-XXXX-short"}
        )
        self.assertEqual("spec:Area_comun/specs/SPEC_TEMPLATE.md", fallback)

    def test_p11_revive_pack_is_bounded_recent_first_and_declares_omissions(self) -> None:
        with tempfile.TemporaryDirectory(prefix="memory-budget-") as temp:
            root = Path(temp)
            make_fixture(root)
            policy_path = root / memory_db.POLICY_PATH
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            policy["revive_pack"] = {
                "max_bytes": 65536,
                "max_inline_source_bytes": 49152,
                "chars_per_token": 4,
            }
            write(policy_path, json.dumps(policy, sort_keys=True) + "\n")
            write(root / "Area_comun/state/TASK_INDEX.json", '{"tasks":[]}\n')
            write(root / "Area_comun/state/CLAIMS.json", '{"claims":[]}\n')
            write(
                root / "personal/Codex/NEW.md",
                "---\ncreated_at: 2026-08-02\n---\nnewest-marker\n" + ("n" * 20000),
            )
            write(
                root / "personal/Codex/OLD.md",
                "---\ncreated_at: 2026-01-01\n---\noldest-marker\n" + ("o" * 20000),
            )
            for index in range(305):
                write(
                    root / f"personal/Codex/OMITTED-{index:03d}.md",
                    f"---\ncreated_at: 2025-01-{(index % 28) + 1:02d}\n---\n"
                    + ("x" * 1024),
                )
            commit_fixture(root)
            memory_db.build(root)
            pack = revive_pack.compose_pack(root, "Codex")
            text = pack.decode("utf-8")
            self.assertLessEqual(len(pack), 65536)
            self.assertIn("- budget_bytes: 65536", text)
            self.assertIn("newest-marker", text)
            self.assertNotIn("oldest-marker", text)
            self.assertIn("personal/Codex/OLD.md", text)
            self.assertIn("inline budget", text)
            self.assertRegex(text, r'"omitted_entries_total": 30[0-9]')
            self.assertIn('"details_omitted":', text)
            self.assertGreater(
                len(json.dumps([
                    {"kind": "memory", "memory_id": f"memory-{index:03d}",
                     "path": f"personal/Codex/OMITTED-{index:03d}.md",
                     "sha256": "f" * 64, "bytes": 1024,
                     "valid_from": f"2025-01-{(index % 28) + 1:02d}",
                     "valid_until": None, "reason": "inline budget"}
                    for index in range(305)
                ], indent=2)),
                65536,
            )
            self.assertRegex(text, r"- token_estimate: \d+")

    def test_timestamp_pii_suffix_is_rejected(self) -> None:
        suffix_vectors = (
            "2026-06-19Tperson@example.invalid",
            "2026-06-19TES9121000418450200051332",
            "2026-06-19T+34612345678",
            "2026-06-19T612345678",
            "2026-06-19T0000000000000",
            "2026-06-19TDNI",
            "2026-06-19Ttrading",
            "2026-06-19T../../etc/passwd",
            "2026-06-19T<script>",
            "2026-06-19T09:28:23Z;DROP",
            "2026-06-19T\x00",
        )
        for timestamp in suffix_vectors:
            with self.subTest(timestamp=timestamp):
                accepted, warnings = memory_db.validate_metadata(
                    {"created_at": timestamp}, {"Codex"}
                )
                self.assertEqual({}, accepted)
                self.assertEqual(["rejected frontmatter key created_at"], warnings)

    def test_supported_timestamps_and_medium_priority_are_accepted(self) -> None:
        dates = ("2026-01-01", "2026-06-19", "2026-12-31")
        times = ("09:28:23", "092823", "00:00:00", "23:59:59")
        fractions = ("", ".1", ".12", ".123", ".1234", ".12345", ".123456")
        offsets = ("", "Z", "+02:00", "-05:00", "-12:30")
        timestamps = set(dates)
        timestamps.update(
            timestamp
            for date in dates
            for time_value in times
            for fraction in fractions
            for offset in offsets
            if memory_db.DATE_RE.fullmatch(
                timestamp := f"{date}T{time_value}{fraction}{offset}"
            )
        )
        self.assertEqual(333, len(timestamps))
        for timestamp in timestamps:
            with self.subTest(timestamp=timestamp):
                accepted, warnings = memory_db.validate_metadata(
                    {"created_at": timestamp}, {"Codex"}
                )
                self.assertEqual({"created_at": timestamp}, accepted)
                self.assertEqual([], warnings)
        accepted, warnings = memory_db.validate_metadata(
            {"priority": "medium"}, {"Codex"}
        )
        self.assertEqual({"priority": "medium"}, accepted)
        self.assertEqual([], warnings)

    def test_p12_empty_supersedes_is_valid_and_produces_no_edge(self) -> None:
        accepted, warnings = memory_db.validate_metadata(
            {"supersedes": []}, {"Codex"}
        )
        self.assertEqual({"supersedes": []}, accepted)
        self.assertEqual([], warnings)
        artifact = memory_db.SourceArtifact(
            Path("x"), "Area_comun/tasks/TASK-EMPTY.md", "task", "TASK-EMPTY",
            b"", {"supersedes": []}, accepted,
        )
        self.assertEqual([], memory_db.extract_edges(artifact))

    def test_new_instance_exports_complete_memory_toolchain(self) -> None:
        module_path = ROOT / "scripts/new_instance.py"
        module_spec = importlib.util.spec_from_file_location("new_instance_memory_test", module_path)
        assert module_spec and module_spec.loader
        new_instance = importlib.util.module_from_spec(module_spec)
        module_spec.loader.exec_module(new_instance)
        with tempfile.TemporaryDirectory(prefix="memory-export-") as temp:
            target = Path(temp)
            new_instance.copy_gate_scripts(ROOT, target)
            new_instance.ensure_protocol_secrets_gitignored(target)
            exported = target / "scripts/memory"
            self.assertEqual(
                {
                    "build_memory_db.py",
                    "check_memory_db_drift.py",
                    "dump_memory_db.py",
                    "query_memory_db.py",
                    "revive_pack.py",
                    "test_memory_db.py",
                },
                {path.name for path in exported.glob("*.py")},
            )
            self.assertEqual(
                "Area_comun/protocol/MEMORY_INDEX_POLICY.json",
                new_instance.CANONICAL_TEMPLATE_FILES[
                    "Area_comun/protocol/MEMORY_INDEX_POLICY.template.json"
                ],
            )
            self.assertIn(
                "runtime/memory/",
                (target / ".gitignore").read_text(encoding="utf-8").splitlines(),
            )

    def test_ddl_v1_has_exact_15_tables_checks_and_fk_policy(self) -> None:
        connection = sqlite3.connect(":memory:")
        memory_db.init_db(connection)
        tables = {
            row[0] for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
            )
        }
        self.assertEqual(
            {
                "artifacts", "artifact_edges", "agent_memory", "cold_packs",
                "retrieval_log", "artifact_versions", "artifact_content_index",
                "policy_status", "hot_cold_rules", "stubs", "validation_runs",
                "pii_classification", "search_terms", "embeddings", "task_context_cache",
            },
            tables,
        )
        self.assertEqual(1, connection.execute("PRAGMA user_version").fetchone()[0])
        self.assertEqual(1, connection.execute("PRAGMA foreign_keys").fetchone()[0])
        for table in ("artifact_edges", "artifact_content_index", "stubs", "pii_classification", "search_terms"):
            foreign_keys = connection.execute(f"PRAGMA foreign_key_list({table})").fetchall()
            self.assertTrue(foreign_keys, table)
            self.assertTrue(all(row[6] == "CASCADE" for row in foreign_keys), table)
        for table in ("artifact_versions", "retrieval_log", "embeddings", "task_context_cache"):
            self.assertEqual([], connection.execute(f"PRAGMA foreign_key_list({table})").fetchall())
        with self.assertRaises(sqlite3.IntegrityError):
            connection.execute(
                "INSERT INTO artifacts(artifact_id,artifact_type,original_path,git_commit,sha256,canonicality,retention_class) VALUES('bad','unknown','x','0','0','canonical_file','hot')"
            )
        connection.close()

    def test_mapping_is_key_exact_normalized_and_deduplicated(self) -> None:
        with tempfile.TemporaryDirectory(prefix="memory-map-") as temp:
            root = Path(temp)
            make_fixture(root)
            write(
                root / "Area_comun/tasks/TASK-0001.md",
                """---
task_id: TASK-0001
title: "Safe task"
status: ready
type: feature
owner: Codex
relates_to: [SPEC-MEMORY]
linked_decisions: [DECISION-NEW]
file: Area_comun/artifacts/output.md
---
Body mentions DECISION-GHOST but must not create an edge.
""",
            )
            write(root / "Area_comun/artifacts/output.md", "# Output\n")
            write(
                root / "Area_comun/decisions/DECISION-OLD.md",
                """---
decision_id: DECISION-OLD
status: superseded
superseded_by: DECISION-NEW
---
""",
            )
            write(
                root / "Area_comun/decisions/DECISION-NEW.md",
                """---
decision_id: DECISION-NEW
status: active
supersedes: DECISION-OLD
---
""",
            )
            commit_fixture(root)
            db = root / "runtime/memory/index.db"
            memory_db.build(root, db)
            connection = sqlite3.connect(db)
            edges = set(connection.execute(
                "SELECT from_artifact_id,to_artifact_id,edge_type FROM artifact_edges"
            ))
            connection.close()
            self.assertEqual(
                {
                    ("TASK-0001", "SPEC-MEMORY", "mentions"),
                    ("TASK-0001", "DECISION-NEW", "decision_for"),
                    ("TASK-0001", "artifact:Area_comun/artifacts/output.md", "implements"),
                    ("DECISION-NEW", "DECISION-OLD", "supersedes"),
                },
                edges,
            )

    def test_i9_no_relationship_keys_means_no_edges_and_reserved_types_fail(self) -> None:
        with tempfile.TemporaryDirectory(prefix="memory-i9-") as temp:
            root = Path(temp)
            make_fixture(root)
            write(
                root / "Area_comun/tasks/TASK-0002.md",
                """---
task_id: TASK-0002
title: "No relations"
status: ready
type: feature
owner: Codex
---
DECISION-9999 SPEC-GHOST TASK-1234 are body text only.
""",
            )
            commit_fixture(root)
            db = root / "runtime/memory/index.db"
            memory_db.build(root, db)
            connection = sqlite3.connect(db)
            self.assertEqual(0, connection.execute("SELECT COUNT(*) FROM artifact_edges").fetchone()[0])
            connection.close()
        for edge_type in sorted(memory_db.RESERVED_EDGE_TYPES):
            with self.assertRaises(ValueError):
                memory_db.validate_f1_edge_type(edge_type)

    def test_i6_agent_identity_is_derived_and_mismatch_rejected(self) -> None:
        self.assertEqual("X", memory_db.derive_agent_id("personal/X/MEMORY.md"))
        with self.assertRaisesRegex(ValueError, "agent_id mismatch"):
            memory_db.derive_agent_id("personal/X/MEMORY.md", "Y")
        with tempfile.TemporaryDirectory(prefix="memory-i6-") as temp:
            root = Path(temp)
            make_fixture(root)
            write(
                root / "personal/X/MEMORY.md",
                "---\nagent_id: Y\ntitle: Safe memory\n---\n",
            )
            commit_fixture(root)
            with self.assertRaisesRegex(ValueError, "agent_id mismatch"):
                memory_db.build(root, root / "runtime/memory/index.db")

    def test_structural_pii_is_default_closed_and_not_publicable(self) -> None:
        planted = "Contact person@example.invalid"
        with tempfile.TemporaryDirectory(prefix="memory-pii-") as temp:
            root = Path(temp)
            make_fixture(root)
            write(
                root / "Area_comun/tasks/TASK-0003.md",
                f"""---
task_id: TASK-0003
title: "{planted}"
status: ready
type: person@example.invalid
owner: Codex
---
{planted}
""",
            )
            commit_fixture(root)
            db = root / "runtime/memory/index.db"
            memory_db.build(root, db)
            connection = sqlite3.connect(db)
            row = connection.execute(
                """SELECT a.title,c.plain_text_excerpt,c.frontmatter_json,p.public_plane_allowed
                FROM artifacts a JOIN artifact_content_index c USING(artifact_id)
                JOIN pii_classification p USING(artifact_id)
                WHERE a.artifact_id='TASK-0003'"""
            ).fetchone()
            self.assertEqual((None, None, '{"owner":"Codex","status":"ready","task_id":"TASK-0003"}', 0), row)
            public_text = table_text_values(connection)
            connection.close()
            for secret in ("person@example.invalid", "987654", "person@example.invalid"):
                self.assertNotIn(secret, public_text)
            memory_db.build(root, rebuild=True)
            connection = sqlite3.connect(db)
            self.assertEqual(
                0,
                connection.execute(
                    "SELECT COUNT(*) FROM pii_classification"
                ).fetchone()[0],
            )
            rebuilt_text = table_text_values(connection)
            connection.close()
            for secret in ("person@example.invalid", "987654", "person@example.invalid"):
                self.assertNotIn(secret, rebuilt_text)

    def test_artifact_ids_exclusions_summaries_and_terms_are_metadata_only(self) -> None:
        with tempfile.TemporaryDirectory(prefix="memory-meta-") as temp:
            root = Path(temp)
            make_fixture(root)
            write(root / "Area_comun/reports/report.md", "# body secretphrase\n")
            write(root / "examples/TASK-0001.md", "---\ntask_id: TASK-0001\n---\n")
            write(root / ".protocol-tmp/TASK-0001.md", "---\ntask_id: TASK-0001\n---\n")
            write(root / "Area_comun/tasks/ignored.template.md", "---\ntask_id: TASK-0001\n---\n")
            commit_fixture(root)
            db = root / "runtime/memory/index.db"
            memory_db.build(root, db)
            connection = sqlite3.connect(db)
            report_id = "report:Area_comun/reports/report.md"
            self.assertEqual(1, connection.execute(
                "SELECT COUNT(*) FROM artifacts WHERE artifact_id=?", (report_id,)
            ).fetchone()[0])
            self.assertEqual(0, connection.execute(
                "SELECT COUNT(*) FROM search_terms WHERE term='secretphrase'"
            ).fetchone()[0])
            self.assertIsNone(connection.execute(
                "SELECT summary_short FROM artifacts WHERE artifact_id=?", (report_id,)
            ).fetchone()[0])
            self.assertEqual(0, connection.execute(
                "SELECT COUNT(*) FROM artifacts WHERE original_path LIKE 'examples/%' OR original_path LIKE '.protocol-tmp/%' OR original_path LIKE '%.template.%'"
            ).fetchone()[0])
            connection.close()

    def test_i2_build_is_read_only_on_clean_fixture_repo(self) -> None:
        with tempfile.TemporaryDirectory(prefix="memory-readonly-") as temp:
            root = Path(temp)
            make_fixture(root)
            write(
                root / "Area_comun/tasks/TASK-0004.md",
                "---\ntask_id: TASK-0004\ntitle: Safe\nstatus: ready\ntype: feature\nowner: Codex\n---\n",
            )
            write(root / ".gitignore", "runtime/memory/\n")
            commit_fixture(root)
            self.assertEqual("", git(root, "status", "--porcelain"))
            result = memory_db.build(root)
            self.assertEqual(15, result["table_count"])
            self.assertEqual("", git(root, "status", "--porcelain"))
            self.assertTrue((root / memory_db.DB_PATH).exists())
            self.assertNotIn("submit_intent", MODULE_PATH.read_text(encoding="utf-8").split("import", 1)[1].split("DDL =", 1)[0])

    def test_i2_rejects_noncanonical_db_targets_without_touching_bytes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="memory-sink-") as temp:
            root = Path(temp) / "repo"
            root.mkdir()
            make_fixture(root)
            governed = root / "Area_comun/state/PROJECT_STATE.json"
            write(governed, '{"sentinel":"governed"}\n')
            outside_traversal = root.parent / "outside-traversal.db"
            outside_absolute = root.parent / "outside-absolute.db"
            outside_traversal.write_bytes(b"traversal-sentinel")
            outside_absolute.write_bytes(b"absolute-sentinel")
            commit_fixture(root)
            targets = (
                (governed, governed.read_bytes()),
                (Path("runtime/memory/../../../outside-traversal.db"), b"traversal-sentinel"),
                (outside_absolute.resolve(), b"absolute-sentinel"),
            )
            for target, expected in targets:
                result = subprocess.run(
                    [sys.executable, str(MODULE_PATH), "--root", str(root), "--db", str(target)],
                    text=True, capture_output=True, check=False,
                )
                self.assertNotEqual(0, result.returncode, target)
                resolved = (target if target.is_absolute() else root / target).resolve()
                self.assertEqual(expected, resolved.read_bytes(), target)

    def test_allowlisted_keys_reject_structural_pii_and_type_is_finite_enum(self) -> None:
        planted = "person@example.invalid"
        malicious_id = "TASK-person@example.invalid"
        values = {
            "task_id": malicious_id, "decision_id": malicious_id,
            "spec_id": malicious_id, "message_id": malicious_id,
            "title": planted, "status": planted, "type": planted,
            "owner": planted, "from": planted, "to": planted,
            "created_at": planted, "updated_at": planted, "closed_at": planted,
            "phase": planted, "priority": planted,
            "relates_to": [malicious_id], "linked_decisions": [malicious_id],
            "supersedes": [malicious_id], "superseded_by": [malicious_id],
            "applies_to": [planted],
            "file": f"Area_comun/artifacts/{planted}.md",
        }
        self.assertEqual(memory_db.ALLOWLIST_KEYS, set(values))
        for key, value in values.items():
            accepted, warnings = memory_db.validate_metadata({key: value}, {"Codex"})
            self.assertNotIn(key, accepted, key)
            self.assertEqual([f"rejected frontmatter key {key}"], warnings, key)
        accepted, warnings = memory_db.validate_metadata(
            {"type": "feature", "status": "for_review"}, {"Codex"}
        )
        self.assertEqual({"status": "for_review", "type": "feature"}, accepted)
        self.assertEqual([], warnings)

    def _assert_pii_rejected_in_key(self, key: str, value: object) -> None:
        planted_parts = (
            "person@example.invalid",
            "person@example.invalid",
            "person@example.invalid",
        )
        with tempfile.TemporaryDirectory(prefix=f"memory-pii-{key}-") as temp:
            root = Path(temp)
            make_fixture(root)
            fixture = root / "Area_comun/decisions/DECISION-0001.md"
            frontmatter = {
                "decision_id": "DECISION-0001",
                "status": "active",
                key: value,
            }
            write(
                fixture,
                "---\n"
                + "\n".join(
                    f"{field}: {json.dumps(item, separators=(',', ':'))}"
                    for field, item in frontmatter.items()
                )
                + "\n---\nSafe fixture body.\n",
            )
            commit_fixture(root)
            db = root / "runtime/memory/index.db"
            result = memory_db.build(root, db)
            self.assertIn(
                f"Area_comun/decisions/DECISION-0001.md: rejected frontmatter key {key}",
                result["warnings"],
            )

            connection = sqlite3.connect(db)
            publicable = connection.execute(
                """SELECT a.summary_short, c.frontmatter_json,
                          GROUP_CONCAT(s.term, ' ')
                   FROM artifacts a
                   JOIN artifact_content_index c USING(artifact_id)
                   LEFT JOIN search_terms s USING(artifact_id)
                   WHERE a.original_path=?
                   GROUP BY a.artifact_id""",
                ("Area_comun/decisions/DECISION-0001.md",),
            ).fetchone()
            self.assertIsNotNone(publicable)
            publicable_text = "\n".join(str(item) for item in publicable if item is not None)
            accepted_frontmatter = json.loads(publicable[1])
            indexed_rows = connection.execute(
                """SELECT COUNT(*)
                   FROM search_terms s
                   JOIN artifacts a USING(artifact_id)
                   WHERE a.original_path=? AND s.field=?""",
                ("Area_comun/decisions/DECISION-0001.md", key),
            ).fetchone()[0]
            edge_rows = connection.execute(
                "SELECT COUNT(*) FROM artifact_edges WHERE source_path=?",
                ("Area_comun/decisions/DECISION-0001.md",),
            ).fetchone()[0]
            connection.close()

            self.assertNotIn(key, accepted_frontmatter)
            self.assertEqual(0, indexed_rows)
            self.assertEqual(0, edge_rows)
            for part in planted_parts:
                self.assertNotIn(part, publicable_text)

    def test_pii_rejected_in_closed_at_key(self) -> None:
        self._assert_pii_rejected_in_key(
            "closed_at",
            "person@example.invalid",
        )

    def test_pii_rejected_in_decision_id_key(self) -> None:
        self._assert_pii_rejected_in_key(
            "decision_id",
            "DECISION-person@example.invalid-person@example.invalid-person@example.invalid",
        )

    def test_pii_rejected_in_file_key(self) -> None:
        self._assert_pii_rejected_in_key(
            "file",
            "Area_comun/artifacts/person@example.invalid.md",
        )

    def test_pii_rejected_in_from_key(self) -> None:
        self._assert_pii_rejected_in_key(
            "from",
            "person@example.invalid",
        )

    def test_pii_rejected_in_relates_to_key(self) -> None:
        self._assert_pii_rejected_in_key(
            "relates_to",
            ["TASK-person@example.invalid-person@example.invalid-person@example.invalid"],
        )

    def test_pii_rejected_in_superseded_by_key(self) -> None:
        self._assert_pii_rejected_in_key(
            "superseded_by",
            ["DECISION-person@example.invalid-person@example.invalid-person@example.invalid"],
        )

    def test_pii_rejected_in_title_key(self) -> None:
        self._assert_pii_rejected_in_key(
            "title",
            "person@example.invalid",
        )

    def test_pii_rejected_in_to_key(self) -> None:
        self._assert_pii_rejected_in_key(
            "to",
            "person@example.invalid",
        )

    def test_pii_rejected_in_type_key(self) -> None:
        self._assert_pii_rejected_in_key(
            "type",
            "person@example.invalid",
        )

    def test_pii_rejected_in_updated_at_key(self) -> None:
        self._assert_pii_rejected_in_key(
            "updated_at",
            "person@example.invalid",
        )

    def test_pii_rejected_in_created_at_key(self) -> None:
        self._assert_pii_rejected_in_key(
            "created_at",
            "person@example.invalid",
        )

    def test_pii_rejected_in_linked_decisions_key(self) -> None:
        self._assert_pii_rejected_in_key(
            "linked_decisions",
            ["DECISION-person@example.invalid-person@example.invalid-person@example.invalid"],
        )

    def test_pii_rejected_in_message_id_key(self) -> None:
        self._assert_pii_rejected_in_key(
            "message_id",
            "MSG-person@example.invalid-person@example.invalid-person@example.invalid",
        )

    def test_pii_rejected_in_owner_key(self) -> None:
        self._assert_pii_rejected_in_key(
            "owner",
            "person@example.invalid",
        )

    def test_pii_rejected_in_phase_key(self) -> None:
        self._assert_pii_rejected_in_key(
            "phase",
            "person@example.invalid",
        )

    def test_pii_rejected_in_priority_key(self) -> None:
        self._assert_pii_rejected_in_key(
            "priority",
            "person@example.invalid",
        )

    def test_pii_rejected_in_spec_id_key(self) -> None:
        self._assert_pii_rejected_in_key(
            "spec_id",
            "SPEC-person@example.invalid-person@example.invalid-person@example.invalid",
        )

    def test_pii_rejected_in_status_key(self) -> None:
        self._assert_pii_rejected_in_key(
            "status",
            "person@example.invalid",
        )

    def test_pii_rejected_in_supersedes_key(self) -> None:
        self._assert_pii_rejected_in_key(
            "supersedes",
            ["DECISION-person@example.invalid-person@example.invalid-person@example.invalid"],
        )

    def test_pii_rejected_in_task_id_key(self) -> None:
        self._assert_pii_rejected_in_key(
            "task_id",
            "TASK-person@example.invalid-person@example.invalid-person@example.invalid",
        )

    def test_git_blob_hash_provenance_ignores_dirty_tree_and_preserves_crlf(self) -> None:
        with tempfile.TemporaryDirectory(prefix="memory-blob-") as temp:
            root = Path(temp)
            make_fixture(root)
            report = root / "Area_comun/reports/crlf.md"
            report.parent.mkdir(parents=True, exist_ok=True)
            blob = b"---\r\ntitle: Safe CRLF\r\n---\r\nblob bytes\r\n"
            report.write_bytes(blob)
            commit = commit_fixture(root)
            (root / "AGENTS.md").write_bytes(b"dirty working tree\n")
            report.write_bytes(b"dirty report\n")
            db = root / "runtime/memory/index.db"
            memory_db.build(root, db)
            connection = sqlite3.connect(db)
            rows = dict(connection.execute(
                "SELECT original_path,sha256 FROM artifacts WHERE original_path IN ('AGENTS.md','Area_comun/reports/crlf.md')"
            ))
            commits = set(connection.execute("SELECT DISTINCT git_commit FROM artifacts"))
            connection.close()
            self.assertEqual(memory_db.sha256_bytes(blob), rows["Area_comun/reports/crlf.md"])
            self.assertEqual(
                memory_db.sha256_bytes(memory_db.git_blob(root, commit, "AGENTS.md")),
                rows["AGENTS.md"],
            )
            self.assertEqual({(commit,)}, commits)

    def test_canonical_dump_excludes_operational_state_and_round_trips(self) -> None:
        with tempfile.TemporaryDirectory(prefix="memory-roundtrip-") as temp:
            root = Path(temp)
            make_fixture(root)
            write(
                root / "Area_comun/tasks/TASK-AC5.md",
                """---
task_id: TASK-AC5
title: Safe round trip
status: ready
type: feature
owner: Codex
---
Body is not indexed.
""",
            )
            write(root / "Area_comun/reports/changed.md", "# Changed before\n")
            write(root / "Area_comun/reports/deleted.md", "# Delete me\n")
            write(root / "Area_comun/reports/stable.md", "# Stable\n")
            commit_fixture(root, "seed incremental database")
            db = root / memory_db.DB_PATH
            normal = memory_db.build(root)
            self.assertEqual("normal", normal["mode"])
            self.assertEqual(1, normal["event_count"])

            stable_id = "report:Area_comun/reports/stable.md"
            connection = sqlite3.connect(db)
            connection.execute(
                """UPDATE artifacts
                SET is_pii_safe=1,last_verified_at='incremental-sentinel'
                WHERE artifact_id=?""",
                (stable_id,),
            )
            connection.execute(
                """UPDATE pii_classification
                SET classifier_version='incremental-sentinel'
                WHERE artifact_id=?""",
                (stable_id,),
            )
            connection.execute(
                """INSERT INTO retrieval_log(
                requested_by,artifact_id,reason,retrieved_at,source_commit,
                sha256_verified
                ) VALUES('incremental-sentinel',?,'preserve','run-value',?,1)""",
                (stable_id, git(root, "rev-parse", "HEAD")),
            )
            connection.execute(
                """INSERT INTO validation_runs(
                run_type,started_at,finished_at,actor,git_commit,result
                ) VALUES('drift_check','run-value','run-value',
                'incremental-sentinel',?,'pass')""",
                (git(root, "rev-parse", "HEAD"),),
            )
            connection.commit()
            connection.close()

            write(root / "Area_comun/reports/changed.md", "# Changed after\n")
            (root / "Area_comun/reports/deleted.md").unlink()
            write(root / "Area_comun/reports/added.md", "# Added\n")
            commit = commit_fixture(root, "mutate canonical inputs")

            incremental = memory_db.build(root)
            self.assertEqual("normal", incremental["mode"])
            dump_a = dump_memory_db.dump_bytes(db)
            self.assertEqual(dump_a, dump_memory_db.dump_bytes(db))
            self.assertTrue(dump_a.endswith(b"\n"))
            self.assertNotIn(b"validation_runs", dump_a)
            self.assertNotIn(b"pii_classification", dump_a)
            self.assertNotIn(b"plain_text_excerpt", dump_a)
            connection = sqlite3.connect(db)
            artifact_ids = {
                row[0] for row in connection.execute("SELECT artifact_id FROM artifacts")
            }
            self.assertIn("report:Area_comun/reports/added.md", artifact_ids)
            self.assertNotIn("report:Area_comun/reports/deleted.md", artifact_ids)
            changed = connection.execute(
                """SELECT git_commit,sha256 FROM artifacts
                WHERE artifact_id='report:Area_comun/reports/changed.md'"""
            ).fetchone()
            self.assertEqual(commit, changed[0])
            self.assertEqual(
                memory_db.sha256_bytes(
                    memory_db.git_blob(
                        root, commit, "Area_comun/reports/changed.md"
                    )
                ),
                changed[1],
            )
            self.assertEqual(
                (1, "incremental-sentinel"),
                connection.execute(
                    """SELECT is_pii_safe,last_verified_at FROM artifacts
                    WHERE artifact_id=?""",
                    (stable_id,),
                ).fetchone(),
            )
            self.assertEqual(
                ("incremental-sentinel",),
                connection.execute(
                    """SELECT classifier_version FROM pii_classification
                    WHERE artifact_id=?""",
                    (stable_id,),
                ).fetchone(),
            )
            self.assertEqual(
                1,
                connection.execute(
                    """SELECT COUNT(*) FROM retrieval_log
                    WHERE requested_by='incremental-sentinel'"""
                ).fetchone()[0],
            )
            self.assertEqual(
                1,
                connection.execute(
                    """SELECT COUNT(*) FROM validation_runs
                    WHERE actor='incremental-sentinel'"""
                ).fetchone()[0],
            )
            connection.close()

            # A second normal build is idempotent for the canonical partition.
            memory_db.build(root)
            self.assertEqual(dump_a, dump_memory_db.dump_bytes(db))

            # The independent rebuild starts without the incremental database.
            db.unlink()
            rebuilt = memory_db.build(root, rebuild=True, at=commit)
            self.assertEqual("rebuild", rebuilt["mode"])
            dump_b = dump_memory_db.dump_bytes(db)
            self.assertEqual(dump_a, dump_b)
            connection = sqlite3.connect(db)
            self.assertEqual(
                0, connection.execute("SELECT COUNT(*) FROM retrieval_log").fetchone()[0]
            )
            self.assertEqual(
                0,
                connection.execute(
                    "SELECT COUNT(*) FROM validation_runs"
                ).fetchone()[0],
            )
            self.assertEqual(
                0,
                connection.execute(
                    "SELECT COUNT(*) FROM pii_classification"
                ).fetchone()[0],
            )
            states = set(
                connection.execute(
                    "SELECT plain_text_excerpt,redaction_state FROM artifact_content_index"
                )
            )
            connection.close()
            self.assertEqual({(None, "unclassified")}, states)

    def test_rebuild_reads_manifests_rules_and_historical_git_commit(self) -> None:
        with tempfile.TemporaryDirectory(prefix="memory-canon-") as temp:
            root = Path(temp)
            make_fixture(root)
            manifest = {
                "pack_id": "CP-20260717-safe",
                "pack_type": "task_history",
                "path": "Area_comun/archive/cold-packs/CP-20260717-safe",
                "git_ref": "refs/heads/main",
                "created_at": "2026-07-17",
                "artifacts": [
                    {
                        "artifact_id": "TASK-OLD",
                        "original_path": "Area_comun/tasks/TASK-OLD.md",
                        "cold_path": "Area_comun/archive/cold-packs/CP-20260717-safe/Area_comun/tasks/TASK-OLD.md",
                        "sha256": "0" * 64,
                    }
                ],
            }
            write(
                root
                / "Area_comun/archive/cold-packs/CP-20260717-safe/pack.manifest.json",
                json.dumps(manifest, sort_keys=True, separators=(",", ":")) + "\n",
            )
            rules = {
                "rules": [
                    {
                        "rule_id": "RULE-TASK-DONE",
                        "artifact_type": "task",
                        "selector": "status=done",
                        "target_retention_class": "cold",
                        "window_days": 45,
                        "window_count": 20,
                        "requires_stub": 1,
                        "requires_active_policy_check": 0,
                        "enabled": 0,
                        "created_by_decision": None,
                    }
                ]
            }
            write(
                root / memory_db.RULES_PATH,
                json.dumps(rules, sort_keys=True, separators=(",", ":")) + "\n",
            )
            commit = commit_fixture(root)
            write(root / "AGENTS.md", "# Dirty tree must not enter historical build\n")
            result = memory_db.build(root, rebuild=True, at=commit)
            self.assertEqual(1, result["cold_pack_count"])
            self.assertEqual(1, result["rules_count"])
            connection = sqlite3.connect(root / memory_db.DB_PATH)
            pack = connection.execute(
                """SELECT pack_id,artifact_count,validated_at,validator_result
                FROM cold_packs"""
            ).fetchone()
            rule = connection.execute(
                "SELECT rule_id,enabled FROM hot_cold_rules"
            ).fetchone()
            agent_hash = connection.execute(
                "SELECT sha256 FROM artifacts WHERE original_path='AGENTS.md'"
            ).fetchone()[0]
            connection.close()
            self.assertEqual(("CP-20260717-safe", 1, None, None), pack)
            self.assertEqual(("RULE-TASK-DONE", 0), rule)
            self.assertEqual(
                memory_db.sha256_bytes(memory_db.git_blob(root, commit, "AGENTS.md")),
                agent_hash,
            )

    def test_event_reader_tolerates_torn_tail_and_lock_probe_is_nonblocking(self) -> None:
        with tempfile.TemporaryDirectory(prefix="memory-events-") as temp:
            root = Path(temp)
            events = root / memory_db.EVENTS_PATH
            lock = root / memory_db.LEDGER_LOCK_PATH
            events.parent.mkdir(parents=True)
            events.write_bytes(
                b'{"seq":1,"type":"complete"}\n{"seq":2,"type":"torn"'
            )
            lock.write_bytes(b"\0")
            parsed = memory_db.read_events_torn_safe(root)
            self.assertEqual([{"seq": 1, "type": "complete"}], parsed)
            with lock.open("r+b") as handle:
                if sys.platform == "win32":
                    import msvcrt

                    handle.seek(0)
                    msvcrt.locking(handle.fileno(), msvcrt.LK_NBLCK, 1)
                    try:
                        with self.assertRaisesRegex(ValueError, "writer is busy"):
                            memory_db.read_events_torn_safe(
                                root, attempts=1, backoff_seconds=0
                            )
                    finally:
                        handle.seek(0)
                        msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
                else:
                    import fcntl

                    fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    try:
                        with self.assertRaisesRegex(ValueError, "writer is busy"):
                            memory_db.read_events_torn_safe(
                                root, attempts=1, backoff_seconds=0
                            )
                    finally:
                        fcntl.flock(handle.fileno(), fcntl.LOCK_UN)

    def test_scan_encoding_excludes_runtime_memory(self) -> None:
        scan_path = ROOT / "scripts/scan_encoding.py"
        scan_spec = importlib.util.spec_from_file_location("scan_encoding", scan_path)
        assert scan_spec and scan_spec.loader
        scan_module = importlib.util.module_from_spec(scan_spec)
        sys.modules[scan_spec.name] = scan_module
        scan_spec.loader.exec_module(scan_module)
        with tempfile.TemporaryDirectory(prefix="memory-scan-") as temp:
            root = Path(temp)
            write(root / "runtime/memory/bad.txt", "\u00c3\n")
            self.assertEqual([], scan_module.scan(root))

    def test_current_tree_build_does_not_change_tracked_status(self) -> None:
        before = git(ROOT, "status", "--porcelain")
        memory_db.build(ROOT)
        after = git(ROOT, "status", "--porcelain")
        self.assertEqual(before, after)

    def test_fast_gate_never_reads_db_and_rejects_missing_active_decision(self) -> None:
        with tempfile.TemporaryDirectory(prefix="memory-fast-") as temp:
            root = Path(temp)
            make_fixture(root)
            db = root / memory_db.DB_PATH
            db.parent.mkdir(parents=True, exist_ok=True)
            db.write_bytes(b"not a sqlite database")
            result = check_memory_db_drift.fast_check(root)
            self.assertFalse(result["database_read"])
            self.assertEqual("noop-until-f2", result["stubs"])
            db.unlink()
            self.assertEqual("pass", check_memory_db_drift.fast_check(root)["result"])
            write(
                root / memory_db.RULES_PATH,
                json.dumps(
                    {
                        "rules": [
                            {
                                "rule_id": "RULE-MISSING",
                                "artifact_type": "task",
                                "selector": "status=done",
                                "target_retention_class": "cold",
                                "requires_stub": 0,
                                "requires_active_policy_check": 1,
                                "enabled": 1,
                                "created_by_decision": "DECISION-MISSING",
                            }
                        ]
                    }
                )
                + "\n",
            )
            commit_fixture(root)
            with self.assertRaisesRegex(ValueError, "absent or inactive"):
                check_memory_db_drift.fast_check(root)

    def test_full_gate_fails_closed_for_each_required_mutation(self) -> None:
        mutations = ("sha", "path", "missing_row", "public_pii")
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                with tempfile.TemporaryDirectory(prefix=f"memory-full-{mutation}-") as temp:
                    root = Path(temp)
                    make_fixture(root)
                    write(
                        root / "Area_comun/tasks/TASK-DRIFT.md",
                        "---\ntask_id: TASK-DRIFT\ntitle: Safe drift\n"
                        "status: ready\ntype: feature\nowner: Codex\n---\n",
                    )
                    commit_fixture(root)
                    db = root / memory_db.DB_PATH
                    memory_db.build(root)
                    connection = sqlite3.connect(db)
                    if mutation == "sha":
                        connection.execute(
                            "UPDATE artifacts SET sha256=? WHERE artifact_id='TASK-DRIFT'",
                            ("0" * 64,),
                        )
                    elif mutation == "path":
                        connection.execute(
                            "UPDATE artifacts SET original_path=? "
                            "WHERE artifact_id='TASK-DRIFT'",
                            ("Area_comun/tasks/DELETED.md",),
                        )
                    elif mutation == "missing_row":
                        connection.execute(
                            "DELETE FROM artifacts WHERE artifact_id='TASK-DRIFT'"
                        )
                    else:
                        connection.execute(
                            """
                            UPDATE artifacts SET
                              title='person@example.invalid',
                              is_pii_safe=1
                            WHERE artifact_id='TASK-DRIFT'
                            """
                        )
                        connection.execute(
                            """
                            UPDATE pii_classification SET
                              classifier_version='fixture',
                              classified_at='2026-07-17',
                              pii_state='findings',
                              finding_count=1,
                              public_plane_allowed=1,
                              redaction_required=1
                            WHERE artifact_id='TASK-DRIFT'
                            """
                        )
                    connection.commit()
                    connection.close()
                    with self.assertRaises(ValueError):
                        check_memory_db_drift.full_check(root)

    def test_full_gate_round_trip_passes_without_writing_source_repo(self) -> None:
        with tempfile.TemporaryDirectory(prefix="memory-full-pass-") as temp:
            root = Path(temp)
            make_fixture(root)
            write(
                root / "Area_comun/tasks/TASK-FULL.md",
                "---\ntask_id: TASK-FULL\ntitle: Full gate\n"
                "status: ready\ntype: feature\nowner: Codex\n---\n",
            )
            commit_fixture(root)
            memory_db.build(root)
            before = git(root, "status", "--porcelain")
            result = check_memory_db_drift.full_check(root)
            after = git(root, "status", "--porcelain")
            self.assertEqual("pass", result["round_trip"])
            self.assertEqual("bidirectional-pass", result["sweep"])
            self.assertEqual(before, after)

    def test_query_fts_or_declared_fallback_returns_metadata_and_edges(self) -> None:
        with tempfile.TemporaryDirectory(prefix="memory-query-") as temp:
            root = Path(temp)
            make_fixture(root)
            write(
                root / "Area_comun/tasks/TASK-QUERY.md",
                "---\ntask_id: TASK-QUERY\ntitle: Quartz domain-free lookup\n"
                "status: ready\ntype: feature\nowner: Codex\n"
                "relates_to: [SPEC-QUERY]\n---\nbody-secret-must-not-leak\n",
            )
            commit_fixture(root)
            memory_db.build(root)
            fallback = query_memory_db.query(root, "quartz", force_fallback=True)
            self.assertEqual("fallback-search_terms-like", fallback["mode"])
            self.assertTrue(fallback["degraded"])
            self.assertTrue(fallback["metadata_only"])
            self.assertEqual("TASK-QUERY", fallback["results"][0]["artifact_id"])
            self.assertEqual(
                [{"from": "TASK-QUERY", "to": "SPEC-QUERY", "type": "mentions"}],
                fallback["results"][0]["edges"],
            )
            self.assertNotIn("body-secret", json.dumps(fallback))
            automatic = query_memory_db.query(root, "quartz")
            self.assertIn(
                automatic["mode"],
                {"fts5-metadata", "fallback-search_terms-like"},
            )
            by_id = query_memory_db.query(root, "TASK-QUERY")
            self.assertEqual("TASK-QUERY", by_id["results"][0]["artifact_id"])

    def test_retrieve_verifies_git_blob_and_logs_exactly_once(self) -> None:
        with tempfile.TemporaryDirectory(prefix="memory-retrieve-") as temp:
            root = Path(temp)
            make_fixture(root)
            content = (
                "---\ntask_id: TASK-RETRIEVE\ntitle: Retrieve fixture\n"
                "status: ready\ntype: feature\nowner: Codex\n---\nbody\n"
            )
            write(root / "Area_comun/tasks/TASK-RETRIEVE.md", content)
            commit_fixture(root)
            db = root / memory_db.DB_PATH
            memory_db.build(root)
            blob = query_memory_db.retrieve(
                root,
                "TASK-RETRIEVE",
                requested_by="Codex",
                task_id="TASK-RETRIEVE",
                reason="acceptance",
            )
            self.assertEqual(content.encode(), blob)
            connection = sqlite3.connect(db)
            self.assertEqual(
                1,
                connection.execute("SELECT COUNT(*) FROM retrieval_log").fetchone()[0],
            )
            connection.close()
            with self.assertRaisesRegex(ValueError, "configured agent"):
                query_memory_db.retrieve(
                    root,
                    "TASK-RETRIEVE",
                    requested_by="Unknown",
                    task_id=None,
                    reason=None,
                )
            with self.assertRaisesRegex(ValueError, "without PII"):
                query_memory_db.retrieve(
                    root,
                    "TASK-RETRIEVE",
                    requested_by="Codex",
                    task_id=None,
                    reason="person@example.invalid",
                )
            connection = sqlite3.connect(db)
            connection.execute(
                "UPDATE artifacts SET sha256=? WHERE artifact_id='TASK-RETRIEVE'",
                ("0" * 64,),
            )
            connection.commit()
            connection.close()
            with self.assertRaisesRegex(ValueError, "sha256 mismatch"):
                query_memory_db.retrieve(
                    root,
                    "TASK-RETRIEVE",
                    requested_by="Codex",
                    task_id=None,
                    reason=None,
                )
            connection = sqlite3.connect(db)
            self.assertEqual(
                1,
                connection.execute("SELECT COUNT(*) FROM retrieval_log").fetchone()[0],
            )
            connection.close()

    def test_revive_pack_is_deterministic_complete_attested_and_agent_scoped(self) -> None:
        with tempfile.TemporaryDirectory(prefix="memory-revive-") as temp:
            root = Path(temp)
            make_fixture(root)
            write(root / "personal/Codex/MEMORY.md", "# Codex memory\ncodex-only-marker\n")
            write(root / "personal/Y/MEMORY.md", "# Y memory\ny-only-marker\n")
            write(
                root / "Area_comun/tasks/TASK-LIVE.md",
                "---\ntask_id: TASK-LIVE\ntitle: Live task\n"
                "status: in_progress\ntype: feature\nowner: Codex\n---\n"
                "live-task-marker\n",
            )
            write(
                root / "Area_comun/state/TASK_INDEX.json",
                json.dumps(
                    {
                        "tasks": [
                            {
                                "id": "TASK-LIVE",
                                "owner": "Codex",
                                "status": "in_progress",
                                "file": "Area_comun/tasks/TASK-LIVE.md",
                            },
                            {
                                "id": "TASK-DONE",
                                "owner": "Codex",
                                "status": "done",
                                "file": "Area_comun/tasks/TASK-DONE.md",
                            },
                        ]
                    },
                    sort_keys=True,
                )
                + "\n",
            )
            write(
                root / "Area_comun/state/CLAIMS.json",
                json.dumps(
                    {
                        "claims": [
                            {
                                "claim_id": "CLAIM-LIVE",
                                "task_id": "TASK-LIVE",
                                "owner": "Codex",
                                "status": "active",
                                "scope": ["scripts/memory/"],
                            },
                            {
                                "claim_id": "CLAIM-OTHER",
                                "task_id": "TASK-X",
                                "owner": "X",
                                "status": "active",
                                "scope": ["x/"],
                            },
                        ]
                    },
                    sort_keys=True,
                )
                + "\n",
            )
            write(
                root / "Area_comun/mailbox/open/MSG-FIXTURE.md",
                "---\nmessage_id: MSG-FIXTURE\nfrom: Arquitecto\nto: Codex\n"
                "type: FYI\nstatus: open\ncreated_at: 2026-07-17\n---\n"
                "mailbox-marker\n",
            )
            write(
                root / "Area_comun/decisions/DECISION-LIVE.md",
                "---\ndecision_id: DECISION-LIVE\nstatus: active\n"
                "applies_to: [Codex]\ncreated_at: 2026-07-17\n---\n"
                "decision-marker\n",
            )
            write(
                root / "unmanaged-private.txt",
                "person@example.invalid must never enter a revive pack\n",
            )
            commit = commit_fixture(root)
            db = root / memory_db.DB_PATH
            memory_db.build(root)
            connection = sqlite3.connect(db)
            connection.execute(
                """
                INSERT INTO task_context_cache(
                  task_id,context_hash,generated_at,included_artifacts_json,
                  excluded_artifacts_json,summary,token_estimate,
                  valid_until_event_seq
                ) VALUES(?,?,?,?,?,?,?,?)
                """,
                (
                    "TASK-LIVE",
                    "ctx-1",
                    "2026-07-17T00:00:00Z",
                    '["TASK-LIVE"]',
                    "[]",
                    "context-cache-marker",
                    5,
                    1,
                ),
            )
            connection.commit()
            connection.close()

            before = git(root, "status", "--porcelain")
            first = revive_pack.compose_pack(root, "Codex")
            second = revive_pack.compose_pack(root, "Codex")
            after = git(root, "status", "--porcelain")
            self.assertEqual(first, second)
            self.assertEqual(before, after)
            text = first.decode("utf-8")
            for heading in (
                "## 1. Memoria vigente",
                "## 2. Tareas vivas y claims activos",
                "## 3. Mailbox open dirigido al agente",
                "## 4. Decisiones activas aplicables",
                "## 5. Task context cache fresco",
                "## ATESTACION DE FUENTES",
            ):
                self.assertIn(heading, text)
            for marker in (
                "codex-only-marker",
                "live-task-marker",
                "CLAIM-LIVE",
                "mailbox-marker",
                "decision-marker",
                "context-cache-marker",
            ):
                self.assertIn(marker, text)
            self.assertNotIn("y-only-marker", text)
            self.assertNotIn("CLAIM-OTHER", text)
            self.assertNotIn("person@example.invalid", text)
            self.assertIn(revive_pack.NO_AUTHORITY_NOTE, text)
            self.assertIn(f"- git_commit: {commit}", text)
            estimate_line = next(
                line for line in text.splitlines() if line.startswith("- token_estimate:")
            )
            estimate = int(estimate_line.split(":", 1)[1].strip())
            self.assertGreater(estimate, 0)
            self.assertGreater(estimate, len(first) // 8)
            self.assertLess(estimate, len(first) // 2)
            for path in (
                "protocol.config.json",
                "personal/Codex/MEMORY.md",
                "Area_comun/state/TASK_INDEX.json",
                "Area_comun/state/CLAIMS.json",
                "Area_comun/tasks/TASK-LIVE.md",
                "Area_comun/mailbox/open/MSG-FIXTURE.md",
                "Area_comun/decisions/DECISION-LIVE.md",
            ):
                self.assertRegex(
                    text,
                    rf"\| `{re.escape(path)}` \| `[0-9a-f]{{40}}` \| `[0-9a-f]{{64}}` \|",
                )

            y_text = revive_pack.compose_pack(root, "Y").decode("utf-8")
            self.assertIn("y-only-marker", y_text)
            self.assertNotIn("codex-only-marker", y_text)
            self.assertGreaterEqual(y_text.count("- EMPTY"), 4)
            with self.assertRaisesRegex(ValueError, "not registered"):
                revive_pack.compose_pack(root, "Unknown")

    def test_revive_pack_attestation_fails_closed_without_stdout(self) -> None:
        with tempfile.TemporaryDirectory(prefix="memory-revive-sha-") as temp:
            root = Path(temp)
            make_fixture(root)
            write(root / "personal/Codex/MEMORY.md", "# Memory\nsafe-marker\n")
            write(root / "Area_comun/state/TASK_INDEX.json", '{"tasks":[]}\n')
            write(root / "Area_comun/state/CLAIMS.json", '{"claims":[]}\n')
            commit_fixture(root)
            db = root / memory_db.DB_PATH
            memory_db.build(root)
            connection = sqlite3.connect(db)
            connection.execute(
                "UPDATE agent_memory SET sha256=? WHERE agent_id='Codex'",
                ("0" * 64,),
            )
            connection.commit()
            connection.close()
            process = subprocess.run(
                [
                    sys.executable,
                    str(REVIVE_MODULE_PATH),
                    "Codex",
                    "--root",
                    str(root),
                ],
                text=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            self.assertNotEqual(0, process.returncode)
            self.assertEqual(b"", process.stdout)
            self.assertIn(b"sha256 mismatch", process.stderr)


if __name__ == "__main__":
    unittest.main(verbosity=2)
