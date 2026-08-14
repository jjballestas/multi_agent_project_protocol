#!/usr/bin/env python3
"""Acceptance tests for F1-U1/U2/U3 memory indexing, drift, and retrieval."""

from __future__ import annotations

import ast
import importlib.util
import json
import random
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

FALSIFICATION_CONTRACTS = (
    {
        "id": "NEG-MEMORY-INSTANCE-STATUS-DECLARATION",
        "negative": "Removing a declared instance status makes its artifact warn again.",
        "mutation": "policy[\"extra_status_values\"].remove(declared_status)",
        "boundaries": (
            "self.assertNotIn(expected_warning, declared_warnings)",
            "self.assertIn(expected_warning, undeclared_warnings)",
        ),
        "exercised_by": "test_p09_instance_status_policy_is_closed_and_falsifiable",
    },
    {
        "id": "NEG-MEMORY-INSTANCE-TYPE-DECLARATION",
        "negative": "Removing a declared instance type makes its artifact warn again.",
        "mutation": "policy[\"extra_type_values\"].remove(declared_type)",
        "boundaries": (
            "self.assertIn(expected_warning, unattested_warnings)",
            "self.assertNotIn(expected_warning, declared_warnings)",
            "self.assertIn(expected_warning, undeclared_warnings)",
        ),
        "exercised_by": "test_p09_instance_type_policy_is_attested_closed_and_falsifiable",
    },
    {
        "id": "NEG-MEMORY-DATE-EXEMPTION-PHONE-ONLY",
        "negative": "Moving the date exemption above the phone heuristic bypasses later PII checks.",
        "mutation": "mutant_source = source.replace(normalized_line, early_date_exemption)",
        "boundaries": (
            "self.assertTrue(memory_db.contains_pii(timestamp, [domain_term]))",
            "self.assertFalse(mutant.contains_pii(timestamp, [domain_term]))",
        ),
        "exercised_by": "test_timestamp_exemption_is_phone_only_and_falsifiable",
    },
    {
        "id": "NEG-MEMORY-DATE-RANGE-VALIDATION",
        "negative": "Restoring the broad timestamp grammar accepts out-of-range components.",
        "mutation": "mutant_source = source.replace(narrow_date_re_source, broad_date_re_source)",
        "boundaries": (
            "self.assertIsNone(memory_db.DATE_RE.fullmatch(timestamp))",
            "self.assertIsNotNone(mutant.DATE_RE.fullmatch(timestamp))",
        ),
        "exercised_by": "test_timestamp_ranges_reject_syntactic_non_dates",
    },
    {
        "id": "NEG-MEMORY-DATE-EXEMPTION-NO-EARLY-EXIT",
        "negative": "An early exit from the contains_pii item loop bypasses later PII checks.",
        "mutation": "mutant_break_source = source.replace(phone_loop, phone_loop + early_break)",
        "boundaries": (
            "self.assertEqual([], source_early_exits)",
            "self.assertNotEqual([], mutant_break_early_exits)",
            "self.assertEqual([], nested_break_early_exits)",
            "self.assertEqual([], nested_continue_early_exits)",
            "self.assertNotEqual([], nested_else_break_early_exits)",
            "self.assertNotEqual([], nested_else_continue_early_exits)",
        ),
        "exercised_by": "test_contains_pii_item_loop_has_no_early_exit",
    },
    {
        "id": "NEG-MEMORY-DATE-OFFSET-COVERAGE",
        "negative": "Restricting valid timezone offsets outside the sampled family rejects legitimate timestamps.",
        "mutation": "mutant_source = source.replace(offset_grammar, restricted_offset_grammar)",
        "boundaries": (
            "self.assertIsNotNone(memory_db.DATE_RE.fullmatch(timestamp))",
            "self.assertIsNone(mutant.DATE_RE.fullmatch(timestamp))",
        ),
        "exercised_by": "test_valid_offset_complement_is_falsifiable",
    },
    {
        "id": "NEG-MEMORY-DOMAIN-PII-PUBLICATION",
        "negative": "Ignoring instance terms authorizes a publicable database row with domain PII.",
        "mutation": "memory_db.contains_pii = lambda value, terms, **kwargs: original_contains_pii(value, [], **kwargs)",
        "boundaries": (
            "self.assertIn(expected_error, guarded_errors)",
            "self.assertNotIn(expected_error, mutant_errors)",
        ),
        "exercised_by": "test_domain_pii_publication_gate_is_attested_and_falsifiable",
    },
    {
        "id": "NEG-MEMORY-DOMAIN-PII-INGESTION",
        "negative": "Ignoring instance terms admits a cold-pack field containing domain PII.",
        "mutation": "memory_db.contains_pii = lambda value, terms, **kwargs: original_contains_pii(value, [], **kwargs)",
        "boundaries": (
            "with self.assertRaisesRegex(ValueError, \"contains prohibited PII\")",
            "self.assertEqual(1, len(mutant_rows))",
        ),
        "exercised_by": "test_domain_pii_ingestion_gate_is_attested_and_falsifiable",
    },
    {
        "id": "NEG-MEMORY-DOMAIN-PII-RETRIEVAL-REASON",
        "negative": "Ignoring instance terms writes a retrieval reason containing domain PII.",
        "mutation": "memory_db.contains_pii = lambda value, terms, **kwargs: original_contains_pii(value, [], **kwargs)",
        "boundaries": (
            "with self.assertRaisesRegex(ValueError, \"without PII\")",
            "self.assertEqual(1, retrieval_log_count)",
        ),
        "exercised_by": "test_domain_pii_retrieval_reason_is_attested_and_falsifiable",
    },
    {
        "id": "NEG-MEMORY-DATE-OFFSET-PII-BEHAVIOR",
        "negative": "A date exemption keyed by coordinate, input order, or timestamp format suppresses observable PII checks.",
        "mutation": "mutant_sources = {",
        "boundaries": (
            "self.assertEqual(expected_product_size, source_product_passed)",
            "self.assertEqual((False, True, False), mutant_results[\"coordinate\"])",
            "self.assertEqual((False, True), mutant_results[\"order\"])",
            "self.assertEqual((False, True, False), mutant_results[\"format\"])",
            "self.assertEqual(3, mutant_caught)",
        ),
        "exercised_by": "test_date_offset_pii_behavior_is_falsifiable",
    },
    {
        "id": "NEG-MEMORY-ACCOUNT-IDENTIFIER-PRESENTATION",
        "negative": "A single candidate cut, first-start-only scan, checksum gate on the contiguous silhouette, missing integral pre-exemption branch, circular corpus admission, missing prefix terminator, unbounded alphanumeric run, or exemption beyond an integrally explained coordinate envelope either narrows prior coverage, loses coordinate-invariant detections, or marks governed protocol identities.",
        "mutation": "mutant_sources = {",
        "boundaries": (
            "self.assertEqual(5400, previous_positive_count)",
            "self.assertEqual(0, lost)",
            "self.assertGreater(gained, 2700)",
            "self.assertTrue(all(source_context_results))",
            "self.assertFalse(all(mutant_context_results[\"single_cut\"]))",
            "self.assertFalse(all(mutant_context_results[\"first_start\"]))",
            "self.assertGreater(mutant_lost[\"checksum_contiguous\"], 0)",
            "self.assertEqual([], governed_identity_hits)",
            "self.assertGreater(len(mutant_governed_gains[\"missing_terminator\"]), 0)",
            "self.assertEqual([], source_object_id_errors)",
            "self.assertGreater(len(mutant_object_id_hits), 0)",
            "self.assertEqual(4, sum(phone_only_compact))",
            "self.assertEqual(phone_only_compact, phone_only_grouped)", "self.assertGreater(sum(coordinate_previous_results), 0)", "self.assertTrue(all(coordinate_current_results))", "self.assertGreater(len(coordinate_types), 2)", "self.assertEqual({\"before\", \"inside\", \"after\"}, coordinate_orders)", "{\"valid-contiguous\", \"valid-grouped\", \"invalid-contiguous\"}", "self.assertEqual({}, accepted_file)", "with self.assertRaisesRegex(ValueError, \"path contains prohibited PII\")", "mutant_coordinate_lost[name] > 0", "mutant_raw_guard_lost[name] > 0", "self.assertEqual([], raw_contiguous_governed_gains)",
        ),
        "exercised_by": "test_account_identifier_presentations_are_structural_and_falsifiable",
    },
    {"id": "NEG-MEMORY-CURRENT-DECISION-PROPERTY", "negative": "Ignoring either supersession or a declared non-current status lets unsafe policy back live rules.", "mutation": "mutant_current = lambda artifact: not memory_db.value_list(artifact.metadata.get(\"superseded_by\"))", "boundaries": ("self.assertEqual(expected_shipped_currentness, shipped_currentness)", "self.assertEqual(cited, hot)", "self.assertNotEqual(cited, literal_mutant_hot)", "self.assertNotEqual(hot, mutant_hot)", "self.assertEqual(\"active\", third_state_row[1])", "with self.assertRaisesRegex(ValueError, \"not classified\")", "self.assertEqual(\"superseded\", rows[\"DECISION-PROPOSED\"][1])", "self.assertEqual(\"superseded\", rows[\"DECISION-REJECTED\"][1])", "self.assertEqual(\"superseded\", rows[\"DECISION-RETIRED\"][1])", "with self.assertRaisesRegex(ValueError, \"absent or inactive\")"), "exercised_by": "test_current_decision_is_attested_property_not_status_literal"},)
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
                "extra_status_values": [],
                "extra_type_values": [],
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
            self.assertFalse(memory_db.contains_pii(term, []))
            self.assertTrue(memory_db.contains_pii(term, [term]))

    def test_p01_domain_pii_parameters_are_required(self) -> None:
        module_paths = tuple(sorted(p for p in Path(__file__).parent.glob("*.py") if not p.name.startswith("test_")))
        violations = domain_pii_default_violations(module_paths)
        self.assertEqual([], violations)
        # Directory placement and structural ast.arguments define both complete sets.

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
            memory_db.contains_pii(
                "MSG-20260619-092823-Codex-to-Arquitecto", [], coordinate="message_id",
            )
        )
        self.assertTrue(memory_db.contains_pii("+34 612 345 678", []))

    def test_p06_ids_accept_dots_but_remain_anchored(self) -> None:
        self.assertIsNotNone(memory_db.ID_RE.fullmatch("MSG-release-v0.10.0"))
        self.assertIsNone(memory_db.ID_RE.fullmatch("MSG-release-v0.10.0 extra"))
        self.assertIsNone(memory_db.ID_RE.fullmatch("msg-release-v0.10.0"))

    def test_p07_titles_accept_bounded_printable_unicode_and_keep_pii_gate(self) -> None:
        title = "Evaluación técnica " + ("a" * 210) + " con precisión"
        self.assertTrue(memory_db.title_is_safe(title, []))
        self.assertFalse(
            memory_db.title_is_safe("x" * (memory_db.TITLE_MAX_LENGTH + 1), [])
        )
        self.assertFalse(memory_db.title_is_safe("line\nbreak", []))
        self.assertFalse(
            memory_db.title_is_safe("contact person@example.invalid", [])
        )

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
            accepted, warnings = memory_db.validate_metadata(  # Identity policy only: no instance terms.
                {"owner": "Historical", "from": "Human", "to": "Unknown"}, agents, []
            )
            self.assertEqual({"from": "Human", "owner": "Historical"}, accepted)
            self.assertEqual(["rejected frontmatter key to"], warnings)

    def test_p09_protocol_status_and_type_vocabularies_remain_finite(self) -> None:
        accepted, warnings = memory_db.validate_metadata(  # Core vocabularies only: no instance terms.
            {"status": "ready_for_review", "type": "HANDOFF"}, {"Codex"}, []
        )
        self.assertEqual({"status": "ready_for_review", "type": "HANDOFF"}, accepted)
        self.assertEqual([], warnings)
        accepted, warnings = memory_db.validate_metadata(
            {"status": "arbitrary status", "type": "arbitrary type"}, {"Codex"}, []
        )
        self.assertEqual({}, accepted)
        self.assertEqual(
            ["rejected frontmatter key status", "rejected frontmatter key type"], warnings
        )

    def test_p09_instance_status_policy_is_closed_and_falsifiable(self) -> None:
        """PERMANENT_NEGATIVE: NEG-MEMORY-INSTANCE-STATUS-DECLARATION"""
        declared_status = "instance-only-status"
        expected_warning = (
            "Area_comun/tasks/TASK-STATUS.md: rejected frontmatter key status"
        )
        with tempfile.TemporaryDirectory(prefix="memory-status-policy-") as temp:
            root = Path(temp)
            make_fixture(root)
            policy_path = root / memory_db.POLICY_PATH
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            policy["extra_status_values"] = [declared_status]
            write(policy_path, json.dumps(policy, sort_keys=True) + "\n")
            write(
                root / "Area_comun/tasks/TASK-STATUS.md",
                "---\ntask_id: TASK-STATUS\ntitle: Status policy fixture\n"
                f"status: {declared_status}\ntype: feature\nowner: Codex\n---\n",
            )
            declared_commit = commit_fixture(root, "declare instance status")
            _, declared_warnings = memory_db.load_artifacts(root, declared_commit)
            self.assertNotIn(expected_warning, declared_warnings)

            policy["extra_status_values"].remove(declared_status)
            write(policy_path, json.dumps(policy, sort_keys=True) + "\n")
            undeclared_commit = commit_fixture(root, "remove instance status declaration")
            _, undeclared_warnings = memory_db.load_artifacts(root, undeclared_commit)
            self.assertIn(expected_warning, undeclared_warnings)

    def test_p09_core_statuses_exclude_instance_vocabulary_and_template_is_empty(self) -> None:
        instance_values = {
            "DRAFT-PENDIENTE-DE-FIRMA-DEL-OPERADOR",
            "GO-PROMOVER-OFF",
            "OK-CERRABLE",
            "OK_CERRABLE",
            "cambio-requerido",
            "draft (pendiente GO operador)",
            "draft-reviewed-informal",
            "hallazgo-confirmado",
        }
        self.assertFalse(instance_values & memory_db.CORE_STATUS_VALUES)
        template = json.loads(
            (ROOT / "Area_comun/protocol/MEMORY_INDEX_POLICY.template.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual([], template["extra_status_values"])

    def test_p09_instance_type_policy_is_attested_closed_and_falsifiable(self) -> None:
        """PERMANENT_NEGATIVE: NEG-MEMORY-INSTANCE-TYPE-DECLARATION"""
        declared_type = "instance-only-type"
        expected_warning = "Area_comun/tasks/TASK-TYPE.md: rejected frontmatter key type"
        with tempfile.TemporaryDirectory(prefix="memory-type-policy-") as temp:
            root = Path(temp)
            make_fixture(root)
            write(
                root / "Area_comun/tasks/TASK-TYPE.md",
                "---\ntask_id: TASK-TYPE\ntitle: Type policy fixture\n"
                f"status: ready\ntype: {declared_type}\nowner: Codex\n---\n",
            )
            artifact_commit = commit_fixture(root, "add instance type artifact")
            policy_path = root / memory_db.POLICY_PATH
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            policy["extra_type_values"] = [declared_type]
            write(policy_path, json.dumps(policy, sort_keys=True) + "\n")

            _, unattested_warnings = memory_db.load_artifacts(root, artifact_commit)
            self.assertIn(expected_warning, unattested_warnings)

            declared_commit = commit_fixture(root, "declare instance type")
            _, declared_warnings = memory_db.load_artifacts(root, declared_commit)
            self.assertNotIn(expected_warning, declared_warnings)

            policy["extra_type_values"].remove(declared_type)
            write(policy_path, json.dumps(policy, sort_keys=True) + "\n")
            undeclared_commit = commit_fixture(root, "remove instance type declaration")
            _, undeclared_warnings = memory_db.load_artifacts(root, undeclared_commit)
            self.assertIn(expected_warning, undeclared_warnings)

    def test_p09_core_types_exclude_instance_vocabulary_and_template_is_empty(self) -> None:
        instance_values = {
            "CAMBIO", "CONSULTA", "COORD", "DIRECTIVA", "FIRMA", "GO",
            "RECONCILE", "REPORTE", "RESP", "RESPUESTA",
        }
        self.assertEqual(60, len(memory_db.TYPE_VALUES))
        self.assertFalse(instance_values & memory_db.TYPE_VALUES)
        template = json.loads(
            (ROOT / "Area_comun/protocol/MEMORY_INDEX_POLICY.template.json").read_text(
                encoding="utf-8"
            )
        )
        self.assertEqual([], template["extra_type_values"])

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
                accepted, warnings = memory_db.validate_metadata(  # Timestamp syntax only: no instance terms.
                    {"created_at": timestamp}, {"Codex"}, []
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
                accepted, warnings = memory_db.validate_metadata(  # Timestamp syntax only: no instance terms.
                    {"created_at": timestamp}, {"Codex"}, []
                )
                self.assertEqual({"created_at": timestamp}, accepted)
                self.assertEqual([], warnings)
        accepted, warnings = memory_db.validate_metadata(  # Core priority only: no instance terms.
            {"priority": "medium"}, {"Codex"}, []
        )
        self.assertEqual({"priority": "medium"}, accepted)
        self.assertEqual([], warnings)

    def test_timestamp_ranges_reject_syntactic_non_dates(self) -> None:
        """PERMANENT_NEGATIVE: NEG-MEMORY-DATE-RANGE-VALIDATION"""
        valid_boundaries = (
            "0000-01-01",
            "9999-12-31T23:59:59.123456Z",
            "2026-02-31T000000+00:00",
            "2026-06-19T23:59:59-13:59",
            "2026-06-19T00:00:00+14:00",
            "2026-06-19T00:00:00-14:00",
        )
        invalid_ranges = (
            "2026-00-01",
            "2026-13-01",
            "2026-01-00",
            "2026-01-32",
            "2026-01-01T24:00:00Z",
            "2026-01-01T00:60:00Z",
            "2026-01-01T00:00:60Z",
            "2026-01-01T240000Z",
            "2026-01-01T006000Z",
            "2026-01-01T000060Z",
            "2026-01-01T00:00:00+15:00",
            "2026-01-01T00:00:00-14:01",
            "2026-01-01T00:00:00+00:60",
            "2026-01-01T00:00:61.234567-89:00",
        )
        for timestamp in valid_boundaries:
            with self.subTest(valid=timestamp):
                self.assertIsNotNone(memory_db.DATE_RE.fullmatch(timestamp))
        for timestamp in invalid_ranges:
            with self.subTest(invalid=timestamp):
                self.assertIsNone(memory_db.DATE_RE.fullmatch(timestamp))
                accepted, warnings = memory_db.validate_metadata(  # Timestamp syntax only: no instance terms.
                    {"created_at": timestamp}, {"Codex"}, []
                )
                self.assertEqual({}, accepted)
                self.assertEqual(["rejected frontmatter key created_at"], warnings)

        source = MODULE_PATH.read_text(encoding="utf-8")
        narrow_date_re_source = (
            'DATE_RE = re.compile(\n'
            '    r"^\\d{4}-(?:0[1-9]|1[0-2])-(?:0[1-9]|[12]\\d|3[01])"\n'
            '    r"(?:T(?:(?:[01]\\d|2[0-3]):[0-5]\\d:[0-5]\\d(?:\\.\\d{1,6})?"\n'
            '    r"|(?:[01]\\d|2[0-3])[0-5]\\d[0-5]\\d)"\n'
            '    r"(?:Z|[+-](?:(?:0\\d|1[0-3]):[0-5]\\d|14:00))?)?$"\n'
            ')\n'
        )
        broad_date_re_source = (
            'DATE_RE = re.compile(\n'
            '    r"^\\d{4}-\\d{2}-\\d{2}"\n'
            '    r"(?:T(?:\\d{2}:\\d{2}:\\d{2}(?:\\.\\d{1,6})?|\\d{6})"\n'
            '    r"(?:Z|[+-]\\d{2}:\\d{2})?)?$"\n'
            ')\n'
        )
        self.assertEqual(1, source.count(narrow_date_re_source))
        mutant_source = source.replace(narrow_date_re_source, broad_date_re_source)
        self.assertNotEqual(source, mutant_source)
        with tempfile.TemporaryDirectory(prefix="memory-date-range-mutant-") as temp:
            mutant_path = Path(temp) / "build_memory_db_mutant.py"
            write(mutant_path, mutant_source)
            spec = importlib.util.spec_from_file_location(
                "build_memory_db_date_range_mutant", mutant_path
            )
            assert spec and spec.loader
            mutant = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = mutant
            try:
                spec.loader.exec_module(mutant)
            finally:
                sys.modules.pop(spec.name, None)
            for timestamp in invalid_ranges:
                with self.subTest(mutant=timestamp):
                    self.assertIsNotNone(mutant.DATE_RE.fullmatch(timestamp))

    def test_timestamp_range_narrowing_reduces_carrier_population(self) -> None:
        """Measure the published 2.9% -> 0.05% carrier-population benchmark."""
        broad_date_re = re.compile(
            r"^\d{4}-\d{2}-\d{2}"
            r"(?:T(?:\d{2}:\d{2}:\d{2}(?:\.\d{1,6})?|\d{6})"
            r"(?:Z|[+-]\d{2}:\d{2})?)?$"
        )
        generator = random.Random(20260805)
        syntactic_population: list[str] = []
        for _ in range(200_000):
            date = (
                f"{generator.randrange(10_000):04d}-"
                f"{generator.randrange(100):02d}-{generator.randrange(100):02d}"
            )
            if generator.random() < 0.22:
                timestamp = date
            else:
                if generator.random() < 0.5:
                    time = (
                        f"{generator.randrange(100):02d}:"
                        f"{generator.randrange(100):02d}:"
                        f"{generator.randrange(100):02d}"
                    )
                    fraction_length = generator.randrange(7)
                    fraction = (
                        ""
                        if fraction_length == 0
                        else "." + "".join(
                            str(generator.randrange(10))
                            for _ in range(fraction_length)
                        )
                    )
                else:
                    time = f"{generator.randrange(1_000_000):06d}"
                    fraction = ""
                if generator.random() < 0.52:
                    offset = (
                        f"{generator.choice('+-')}"
                        f"{generator.randrange(100):02d}:"
                        f"{generator.randrange(100):02d}"
                    )
                else:
                    offset = "" if generator.random() < 0.5 else "Z"
                timestamp = f"{date}T{time}{fraction}{offset}"
            self.assertIsNotNone(broad_date_re.fullmatch(timestamp))
            syntactic_population.append(timestamp)

        def carries_phone_candidate(value: str) -> bool:
            return any(
                9 <= len(re.sub(r"\D", "", match.group(0))) <= 15
                for match in memory_db.PHONE_CANDIDATE_RE.finditer(value)
            )

        broad_carriers = sum(map(carries_phone_candidate, syntactic_population))
        narrowed_population = [
            value for value in syntactic_population if memory_db.DATE_RE.fullmatch(value)
        ]
        narrowed_carriers = sum(map(carries_phone_candidate, narrowed_population))
        self.assertEqual(5_789, broad_carriers)
        self.assertEqual(2.9, round(100 * broad_carriers / len(syntactic_population), 1))
        self.assertEqual(2_006, len(narrowed_population))
        self.assertEqual(1, narrowed_carriers)
        self.assertEqual(
            0.05,
            round(100 * narrowed_carriers / len(narrowed_population), 2),
        )

    def test_timestamp_exemption_is_phone_only_and_falsifiable(self) -> None:
        """PERMANENT_NEGATIVE: NEG-MEMORY-DATE-EXEMPTION-PHONE-ONLY"""
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
        domain_term = "2026"
        for timestamp in timestamps:
            with self.subTest(implementation="source", timestamp=timestamp):
                self.assertTrue(memory_db.contains_pii(timestamp, [domain_term]))

        source = MODULE_PATH.read_text(encoding="utf-8")
        phone_guard = "        if not DATE_RE.fullmatch(item) and any(\n"
        self.assertNotIn("protocol_identity", phone_guard)
        early_date_exemption = (
            "    if DATE_RE.fullmatch(item):\n"
            "        return False\n"
            "    normalized = re.sub(r\"[_/\\\\.-]+\", \" \", item)\n"
        )
        normalized_line = "    normalized = re.sub(r\"[_/\\\\.-]+\", \" \", item)\n"
        self.assertEqual(1, source.count(phone_guard))
        self.assertEqual(1, source.count(normalized_line))
        mutant_source = source.replace(normalized_line, early_date_exemption)
        self.assertNotEqual(source, mutant_source)

        with tempfile.TemporaryDirectory(prefix="memory-date-exemption-mutant-") as temp:
            mutant_path = Path(temp) / "build_memory_db_mutant.py"
            write(mutant_path, mutant_source)
            spec = importlib.util.spec_from_file_location(
                "build_memory_db_date_exemption_mutant", mutant_path
            )
            assert spec and spec.loader
            mutant = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = mutant
            try:
                spec.loader.exec_module(mutant)
            finally:
                sys.modules.pop(spec.name, None)
            for timestamp in timestamps:
                with self.subTest(implementation="mutant", timestamp=timestamp):
                    self.assertFalse(mutant.contains_pii(timestamp, [domain_term]))

    def test_contains_pii_item_loop_has_no_early_exit(self) -> None:
        """PERMANENT_NEGATIVE: NEG-MEMORY-DATE-EXEMPTION-NO-EARLY-EXIT"""

        def contains_pii_loop(source_text: str) -> ast.For:
            tree = ast.parse(source_text)
            functions = [
                node
                for node in tree.body
                if isinstance(node, ast.FunctionDef) and node.name == "contains_pii"
            ]
            self.assertEqual(1, len(functions))
            loops = [node for node in functions[0].body if isinstance(node, ast.For)]
            self.assertEqual(1, len(loops))
            return loops[0]

        def item_loop_early_exits(source_text: str) -> list[ast.stmt]:
            class OuterLoopControlFlow(ast.NodeVisitor):
                def __init__(self) -> None:
                    self.early_exits: list[ast.stmt] = []

                def visit_Break(self, node: ast.Break) -> None:
                    self.early_exits.append(node)

                def visit_Continue(self, node: ast.Continue) -> None:
                    self.early_exits.append(node)

                def _nested_loop(self, node: ast.For | ast.AsyncFor | ast.While) -> None:
                    for statement in node.orelse:
                        self.visit(statement)

                def visit_For(self, node: ast.For) -> None:
                    self._nested_loop(node)

                def visit_AsyncFor(self, node: ast.AsyncFor) -> None:
                    self._nested_loop(node)

                def visit_While(self, node: ast.While) -> None:
                    self._nested_loop(node)

                def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
                    return None

                def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
                    return None

                def visit_Lambda(self, node: ast.Lambda) -> None:
                    return None

            loop = contains_pii_loop(source_text)
            visitor = OuterLoopControlFlow()
            for statement in (*loop.body, *loop.orelse):
                visitor.visit(statement)
            return visitor.early_exits

        source = MODULE_PATH.read_text(encoding="utf-8")
        source_early_exits = item_loop_early_exits(source)
        self.assertEqual([], source_early_exits)

        phone_loop = "    for item in items:\n"
        early_continue = (
            "        if DATE_RE.fullmatch(item) and item.endswith(\"+05:45\"):\n"
            "            continue\n"
        )
        early_break = (
            "        if DATE_RE.fullmatch(item) and item.endswith(\"+05:45\"):\n"
            "            break\n"
        )
        nested_break = "        for nested_item in ():\n            break\n"
        nested_continue = "        for nested_item in ():\n            continue\n"
        nested_else_break = (
            "        for nested_item in ():\n"
            "            pass\n"
            "        else:\n"
            "            if DATE_RE.fullmatch(item) and item.endswith(\"+05:45\"):\n"
            "                break\n"
        )
        nested_else_continue = (
            "        while False:\n"
            "            pass\n"
            "        else:\n"
            "            if DATE_RE.fullmatch(item) and item.endswith(\"+05:45\"):\n"
            "                continue\n"
        )
        self.assertEqual(1, source.count(phone_loop))
        mutant_continue_source = source.replace(
            phone_loop, phone_loop + early_continue
        )
        mutant_break_source = source.replace(phone_loop, phone_loop + early_break)
        nested_break_source = source.replace(
            phone_loop, phone_loop + nested_break
        )
        nested_continue_source = source.replace(
            phone_loop, phone_loop + nested_continue
        )
        nested_else_break_source = source.replace(
            phone_loop, phone_loop + nested_else_break
        )
        nested_else_continue_source = source.replace(
            phone_loop, phone_loop + nested_else_continue
        )
        self.assertNotEqual(source, mutant_continue_source)
        self.assertNotEqual(source, mutant_break_source)
        mutant_continue_early_exits = item_loop_early_exits(mutant_continue_source)
        mutant_break_early_exits = item_loop_early_exits(mutant_break_source)
        nested_break_early_exits = item_loop_early_exits(nested_break_source)
        nested_continue_early_exits = item_loop_early_exits(nested_continue_source)
        nested_else_break_early_exits = item_loop_early_exits(nested_else_break_source)
        nested_else_continue_early_exits = item_loop_early_exits(
            nested_else_continue_source
        )
        self.assertNotEqual([], mutant_continue_early_exits)
        self.assertNotEqual([], mutant_break_early_exits)
        self.assertEqual([], nested_break_early_exits)
        self.assertEqual([], nested_continue_early_exits)
        self.assertNotEqual([], nested_else_break_early_exits)
        self.assertNotEqual([], nested_else_continue_early_exits)

    def test_valid_offset_complement_is_falsifiable(self) -> None:
        """PERMANENT_NEGATIVE: NEG-MEMORY-DATE-OFFSET-COVERAGE"""
        valid_offsets = (
            "2026-06-19T09:28:23+05:45",
            "2026-06-19T09:28:23-09:45",
            "2026-06-19T09:28:23+13:00",
            "2026-06-19T09:28:23+14:00",
        )
        for timestamp in valid_offsets:
            with self.subTest(implementation="source", timestamp=timestamp):
                self.assertIsNotNone(memory_db.DATE_RE.fullmatch(timestamp))

        source = MODULE_PATH.read_text(encoding="utf-8")
        offset_grammar = '    r"(?:Z|[+-](?:(?:0\\d|1[0-3]):[0-5]\\d|14:00))?)?$"\n'
        restricted_offset_grammar = '    r"(?:Z|[+-](?:0\\d|1[0-2]):(?:00|30))?)?$"\n'
        self.assertEqual(1, source.count(offset_grammar))
        mutant_source = source.replace(offset_grammar, restricted_offset_grammar)
        self.assertNotEqual(source, mutant_source)
        with tempfile.TemporaryDirectory(prefix="memory-date-offset-mutant-") as temp:
            mutant_path = Path(temp) / "build_memory_db_mutant.py"
            write(mutant_path, mutant_source)
            spec = importlib.util.spec_from_file_location(
                "build_memory_db_date_offset_mutant", mutant_path
            )
            assert spec and spec.loader
            mutant = importlib.util.module_from_spec(spec)
            sys.modules[spec.name] = mutant
            try:
                spec.loader.exec_module(mutant)
            finally:
                sys.modules.pop(spec.name, None)
            for timestamp in valid_offsets:
                with self.subTest(implementation="mutant", timestamp=timestamp):
                    self.assertIsNone(mutant.DATE_RE.fullmatch(timestamp))

    def test_p12_empty_supersedes_is_valid_and_produces_no_edge(self) -> None:
        accepted, warnings = memory_db.validate_metadata(  # Graph metadata only: no instance terms.
            {"supersedes": []}, {"Codex"}, []
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
        for key, value in values.items():  # Structural PII only: no instance terms.
            accepted, warnings = memory_db.validate_metadata({key: value}, {"Codex"}, [])
            self.assertNotIn(key, accepted, key)
            self.assertEqual([f"rejected frontmatter key {key}"], warnings, key)
        accepted, warnings = memory_db.validate_metadata(
            {"type": "feature", "status": "for_review"}, {"Codex"}, []
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

    def test_domain_pii_publication_gate_is_attested_and_falsifiable(self) -> None:
        """PERMANENT_NEGATIVE: NEG-MEMORY-DOMAIN-PII-PUBLICATION"""
        domain_term = "Acme SL"
        expected_error = "publicable artifact contains PII: TASK-DOMAIN-PUBLIC"
        with tempfile.TemporaryDirectory(prefix="memory-domain-public-") as temp:
            root = Path(temp)
            make_fixture(root)
            policy_path = root / memory_db.POLICY_PATH
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            policy["domain_pii_terms"] = [domain_term]
            write(policy_path, json.dumps(policy, sort_keys=True) + "\n")
            write(
                root / "Area_comun/tasks/TASK-DOMAIN-PUBLIC.md",
                "---\ntask_id: TASK-DOMAIN-PUBLIC\ntitle: Safe public title\n"
                "status: ready\ntype: feature\nowner: Codex\n---\n",
            )
            commit = commit_fixture(root, "declare domain PII and public artifact")
            memory_db.build(root)
            artifacts, _warnings = memory_db.load_artifacts(root, commit)
            connection = sqlite3.connect(root / memory_db.DB_PATH)
            connection.execute(
                "UPDATE artifacts SET title=?,is_pii_safe=1 WHERE artifact_id=?",
                (domain_term, "TASK-DOMAIN-PUBLIC"),
            )
            connection.commit()
            guarded_errors = check_memory_db_drift._sweep_database(
                root, connection, artifacts, commit
            )
            self.assertIn(expected_error, guarded_errors)

            original_contains_pii = memory_db.contains_pii
            memory_db.contains_pii = lambda value, terms, **kwargs: original_contains_pii(value, [], **kwargs)
            try:
                mutant_errors = check_memory_db_drift._sweep_database(
                    root, connection, artifacts, commit
                )
            finally:
                memory_db.contains_pii = original_contains_pii
                connection.close()
            self.assertNotIn(expected_error, mutant_errors)

    def test_domain_pii_ingestion_gate_is_attested_and_falsifiable(self) -> None:
        """PERMANENT_NEGATIVE: NEG-MEMORY-DOMAIN-PII-INGESTION"""
        domain_term = "Acme SL"
        with tempfile.TemporaryDirectory(prefix="memory-domain-ingest-") as temp:
            root = Path(temp)
            make_fixture(root)
            manifest = {
                "pack_id": domain_term,
                "pack_type": "task_history",
                "path": "Area_comun/archive/cold-packs/domain-fixture",
                "git_ref": "refs/heads/main",
                "created_at": "2026-08-07",
                "artifacts": [],
            }
            write(
                root
                / "Area_comun/archive/cold-packs/domain-fixture/pack.manifest.json",
                json.dumps(manifest, sort_keys=True) + "\n",
            )
            unattested_commit = commit_fixture(root, "add domain pack fixture")
            self.assertEqual(
                1, len(memory_db.load_cold_packs(root, unattested_commit))
            )

            policy_path = root / memory_db.POLICY_PATH
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            policy["domain_pii_terms"] = [domain_term]
            write(policy_path, json.dumps(policy, sort_keys=True) + "\n")
            self.assertEqual(
                1, len(memory_db.load_cold_packs(root, unattested_commit))
            )
            attested_commit = commit_fixture(root, "declare domain PII")
            with self.assertRaisesRegex(ValueError, "contains prohibited PII"):
                memory_db.load_cold_packs(root, attested_commit)

            original_contains_pii = memory_db.contains_pii
            memory_db.contains_pii = lambda value, terms, **kwargs: original_contains_pii(value, [], **kwargs)
            try:
                mutant_rows = memory_db.load_cold_packs(root, attested_commit)
            finally:
                memory_db.contains_pii = original_contains_pii
            self.assertEqual(1, len(mutant_rows))

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

    def test_domain_pii_retrieval_reason_is_attested_and_falsifiable(self) -> None:
        """PERMANENT_NEGATIVE: NEG-MEMORY-DOMAIN-PII-RETRIEVAL-REASON"""
        domain_term = "Acme SL"
        with tempfile.TemporaryDirectory(prefix="memory-domain-reason-") as temp:
            root = Path(temp)
            make_fixture(root)
            policy_path = root / memory_db.POLICY_PATH
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            policy["domain_pii_terms"] = [domain_term]
            write(policy_path, json.dumps(policy, sort_keys=True) + "\n")
            content = (
                "---\ntask_id: TASK-DOMAIN-REASON\ntitle: Safe retrieval title\n"
                "status: ready\ntype: feature\nowner: Codex\n---\nbody\n"
            )
            write(root / "Area_comun/tasks/TASK-DOMAIN-REASON.md", content)
            commit_fixture(root, "declare domain PII and retrieval artifact")
            db = root / memory_db.DB_PATH
            memory_db.build(root)
            with self.assertRaisesRegex(ValueError, "without PII"):
                query_memory_db.retrieve(
                    root,
                    "TASK-DOMAIN-REASON",
                    requested_by="Codex",
                    task_id=None,
                    reason=domain_term,
                )
            connection = sqlite3.connect(db)
            self.assertEqual(
                0,
                connection.execute("SELECT COUNT(*) FROM retrieval_log").fetchone()[0],
            )
            connection.close()

            original_contains_pii = memory_db.contains_pii
            memory_db.contains_pii = lambda value, terms, **kwargs: original_contains_pii(value, [], **kwargs)
            try:
                query_memory_db.retrieve(
                    root,
                    "TASK-DOMAIN-REASON",
                    requested_by="Codex",
                    task_id=None,
                    reason=domain_term,
                )
            finally:
                memory_db.contains_pii = original_contains_pii
            connection = sqlite3.connect(db)
            retrieval_log_count = connection.execute(
                "SELECT COUNT(*) FROM retrieval_log"
            ).fetchone()[0]
            connection.close()
            self.assertEqual(1, retrieval_log_count)

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

    def test_date_offset_pii_behavior_is_falsifiable(self) -> None:
        """PERMANENT_NEGATIVE: NEG-MEMORY-DATE-OFFSET-PII-BEHAVIOR"""
        numeric_offsets = tuple(
            f"{sign}{hour:02d}:{minute:02d}"
            for sign in "+-"
            for hour in range(15)
            for minute in range(60)
            if hour < 14 or minute == 0
        )
        valid_offsets = ("", "Z", *numeric_offsets)
        months = tuple(range(1, 13))
        hours = tuple(range(24))
        formats = ("extended", "basic", "fractional")
        email = "contact@example.invalid"
        self.assertEqual(1_684, len(valid_offsets))

        def timestamp_for(
            month: int, hour: int, offset: str, format_name: str, ordinal: int
        ) -> str:
            year = ordinal % 10_000
            day = ordinal % 31 + 1
            minute = ordinal % 60
            second = (ordinal * 7) % 60
            date = f"{year:04d}-{month:02d}-{day:02d}"
            if format_name == "basic":
                return f"{date}T{hour:02d}{minute:02d}{second:02d}{offset}"
            fraction = "" if format_name == "extended" else "." + "1" * (ordinal % 6 + 1)
            return f"{date}T{hour:02d}:{minute:02d}:{second:02d}{fraction}{offset}"

        expected_product_size = len(months) * len(hours) * len(valid_offsets) * len(formats)
        source_product_passed = 0
        ordinal = 0
        for month in months:
            for hour in hours:
                for offset in valid_offsets:
                    for format_name in formats:
                        timestamp = timestamp_for(month, hour, offset, format_name, ordinal)
                        ordinal += 1
                        self.assertIsNotNone(memory_db.DATE_RE.fullmatch(timestamp))
                        if memory_db.contains_pii([timestamp, email], []):
                            source_product_passed += 1
        self.assertEqual(expected_product_size, source_product_passed)

        source = MODULE_PATH.read_text(encoding="utf-8")
        two_phase_body = (
            "    items = value_list(value)\n"
            "    if any(non_phone_pii_is_detected(item, domain_patterns, coordinate) for item in items):\n"
            "        return True\n"
            "    coordinate_bound = False\n"
            "    for item in items:\n"
            "        if not DATE_RE.fullmatch(item) and any(\n"
            "            phone_number_is_detected(pii_value, coordinate_bound=coordinate_bound)\n"
            "            for pii_value in pii_values_for_coordinate(item, coordinate)\n"
            "        ):\n"
            "            return True\n"
        )
        self.assertEqual(1, source.count(two_phase_body))

        target_offset = valid_offsets[len(valid_offsets) // 3]
        target_month = months[len(months) // 2]
        target_hour = hours[len(hours) // 2]
        target_extended = timestamp_for(target_month, target_hour, target_offset, "extended", 37)
        target_basic = timestamp_for(target_month, target_hour, target_offset, "basic", 41)
        target_domain = f"{37 % 10_000:04d}"
        coordinate_guard = (
            f"DATE_RE.fullmatch(item) and item[5:7] == {f'{target_month:02d}'!r} "
            f"and item[11:13] == {f'{target_hour:02d}'!r} and item.endswith({target_offset!r})"
        )
        single_pass_body = (
            "    for item in value_list(value):\n"
            f"        if {coordinate_guard}:\n"
            "            return False\n"
            "        if non_phone_pii_is_detected(item, domain_patterns, coordinate):\n"
            "            return True\n"
            "        if not DATE_RE.fullmatch(item) and any(\n"
            "            phone_number_is_detected(pii_value, coordinate_bound=False)\n"
            "            for pii_value in pii_values_for_coordinate(item, coordinate)\n"
            "        ):\n"
            "            return True\n"
        )
        order_body = (
            "    items = value_list(value)\n"
            "    if items and DATE_RE.fullmatch(items[0]):\n"
            "        return False\n"
            + two_phase_body
        )
        format_guard = (
            "DATE_RE.fullmatch(item) and len(item) > 16 and item[13] != ':'"
        )
        format_body = (
            "    for item in value_list(value):\n"
            f"        if {format_guard}:\n"
            "            return False\n"
            "        if non_phone_pii_is_detected(item, domain_patterns, coordinate):\n"
            "            return True\n"
            "        if not DATE_RE.fullmatch(item) and any(\n"
            "            phone_number_is_detected(pii_value, coordinate_bound=False)\n"
            "            for pii_value in pii_values_for_coordinate(item, coordinate)\n"
            "        ):\n"
            "            return True\n"
        )
        mutant_sources = {
            "coordinate": source.replace(two_phase_body, single_pass_body),
            "order": source.replace(two_phase_body, order_body),
            "format": source.replace(two_phase_body, format_body),
        }
        self.assertTrue(all(mutant_source != source for mutant_source in mutant_sources.values()))

        mutant_results: dict[str, tuple[bool, ...]] = {}
        with tempfile.TemporaryDirectory(prefix="memory-date-product-mutants-") as temp:
            for name, mutant_source in mutant_sources.items():
                mutant_path = Path(temp) / f"build_memory_db_{name}_mutant.py"
                write(mutant_path, mutant_source)
                spec = importlib.util.spec_from_file_location(
                    f"build_memory_db_date_product_{name}_mutant", mutant_path
                )
                assert spec and spec.loader
                mutant = importlib.util.module_from_spec(spec)
                sys.modules[spec.name] = mutant
                try:
                    spec.loader.exec_module(mutant)
                    if name == "coordinate":
                        mutant_results[name] = (
                            mutant.contains_pii([target_extended, email], []),
                            mutant.contains_pii([email, target_extended], []),
                            mutant.contains_pii(target_extended, [target_domain]),
                        )
                    elif name == "order":
                        mutant_results[name] = (
                            mutant.contains_pii([target_extended, email], []),
                            mutant.contains_pii([email, target_extended], []),
                        )
                    else:
                        mutant_results[name] = (
                            mutant.contains_pii([target_basic, email], []),
                            mutant.contains_pii([email, target_basic], []),
                            mutant.contains_pii(target_basic, [f"{41 % 10_000:04d}"]),
                        )
                finally:
                    sys.modules.pop(spec.name, None)

        self.assertEqual((False, True, False), mutant_results["coordinate"])
        self.assertEqual((False, True), mutant_results["order"])
        self.assertEqual((False, True, False), mutant_results["format"])
        mutant_caught = sum(any(not result for result in results) for results in mutant_results.values())
        self.assertEqual(3, mutant_caught)
        print(
            "TASK0332_BEHAVIOR "
            f"product={expected_product_size} source={source_product_passed} "
            f"mutants={mutant_caught}/{len(mutant_results)} "
            f"coordinate={mutant_results['coordinate']} "
            f"order={mutant_results['order']} format={mutant_results['format']}"
        )

    def test_account_identifier_presentations_are_structural_and_falsifiable(self) -> None:
        """PERMANENT_NEGATIVE: NEG-MEMORY-ACCOUNT-IDENTIFIER-PRESENTATION"""
        compact = "ES9121000418450200051332"
        grouped = "ES91 2100 0418 4502 0005 1332"
        presentations = (
            compact,
            grouped,
            "ES91-21000418-45020005-1332",
            "ES91\u00a021000418\u200945020005\u202f1332",
            "ES91 2100-04184502\u202f0005 1332",
        )
        for presentation in presentations:
            with self.subTest(presentation=presentation):
                self.assertTrue(memory_db.contains_pii(presentation, []))

        left_contexts = ("", "prefix ", "AB12 ", "xAB 34 payload ", "x")
        right_contexts = ("", " suffix", " AB12 suffix", "x")
        context_values = tuple(
            left + presentation + right
            for presentation in (compact, grouped)
            for left in left_contexts
            for right in right_contexts
        )
        source_context_results = tuple(
            memory_db.contains_pii(value, []) for value in context_values
        )
        self.assertTrue(all(source_context_results))

        invalid_contiguous = compact + "A"
        self.assertFalse(
            memory_db.account_identifier_checksum_is_valid(invalid_contiguous)
        )
        self.assertTrue(memory_db.contains_pii(invalid_contiguous, []))

        protocol_like = "MSG-20260707-Maker-to-Checker-GO-1105-infra-fixture"
        self.assertIsNotNone(memory_db.STRUCTURAL_PII_PATTERNS[1].search(protocol_like))
        self.assertFalse(memory_db.contains_pii(protocol_like, []))

        governed_metadata_values = tuple(
            (key, item, relative)
            for path, relative in memory_db.iter_source_paths(ROOT, "HEAD")
            for key, value in memory_db.parse_frontmatter(
                path.read_text(encoding="utf-8")
            ).items()
            if key in memory_db.ALLOWLIST_KEYS
            for item in memory_db.value_list(value)
        )
        governed_identities = tuple(
            entry
            for entry in governed_metadata_values
            if entry[0] in {
                "task_id", "decision_id", "spec_id", "message_id",
                "relates_to", "linked_decisions", "supersedes", "superseded_by",
            }
        )
        governed_identity_hits = [
            entry
            for entry in governed_identities
            if memory_db.contains_pii(entry[1], [], coordinate=entry[0])
        ]
        self.assertEqual([], governed_identity_hits)
        governed_current_results = tuple(
            memory_db.contains_pii(value, [], coordinate=coordinate)
            for coordinate, value, _ in governed_metadata_values
        )

        object_ids = tuple(git(ROOT, "rev-list", "--all").splitlines())
        self.assertGreater(len(object_ids), 100)
        self.assertFalse(
            any(memory_db.account_identifier_contiguous_is_bounded(item) for item in object_ids)
        )
        self.assertGreater(
            sum(bool(memory_db.ACCOUNT_IDENTIFIER_CONTIGUOUS_RE.search(item)) for item in object_ids),
            0,
        )
        source_object_id_errors = []
        for object_id in object_ids:
            try:
                memory_db.require_safe_text(
                    object_id,
                    "git_ref",
                    domain_pii_terms=[],
                    pii_check=memory_db.git_ref_requires_pii_check(object_id),
                )
            except ValueError as error:
                source_object_id_errors.append(str(error))
        self.assertEqual([], source_object_id_errors)

        minimum = "GB82WEST123456"
        maximum = "GB82" + ("A" * 30)
        self.assertEqual(14, len(minimum))
        self.assertEqual(34, len(maximum))
        self.assertIsNotNone(memory_db.STRUCTURAL_PII_PATTERNS[1].fullmatch(minimum))
        self.assertIsNotNone(memory_db.STRUCTURAL_PII_PATTERNS[1].fullmatch(maximum))
        self.assertIsNone(memory_db.STRUCTURAL_PII_PATTERNS[1].fullmatch("GB82" + ("A" * 9)))
        self.assertIsNone(memory_db.STRUCTURAL_PII_PATTERNS[1].fullmatch("GB82" + ("A" * 31)))

        def phone_band_detects(value: str) -> bool:
            return any(
                9 <= len(re.sub(r"\D", "", candidate.group(0))) <= 15
                for candidate in memory_db.PHONE_CANDIDATE_RE.finditer(value)
            )

        country_samples = (
            "ES9121000418450200051332",
            "GB33BUKB20201555555555",
            "NL91ABNA0417164300",
            "BE68539007547034",
            "NO9386011117947",
            "DE89370400440532013000",
            "FR1420041010050500013M02606",
            "IT60X0542811101000000123456",
            "CH9300762011623852957",
            "PL61109010140000071219812874",
        )
        grouped_country_samples = tuple(
            " ".join(value[index:index + 4] for index in range(0, len(value), 4))
            for value in country_samples
        )
        phone_only_compact = tuple(map(phone_band_detects, country_samples))
        phone_only_grouped = tuple(map(phone_band_detects, grouped_country_samples))
        self.assertEqual(4, sum(phone_only_compact))
        self.assertEqual(phone_only_compact, phone_only_grouped)

        def valid_identifier(index: int) -> str:
            body = f"{index:020d}"
            provisional = body + "142800"
            check_digits = 98 - (int(provisional) % 97)
            return f"ES{check_digits:02d}{body}"

        def invalid_silhouette(index: int) -> str:
            rng = random.Random(index)
            return "ES00" + "".join(str(rng.randrange(10)) for _ in range(20))

        neutral_contexts = ("", "prefix ", "record ")
        generated_start_contexts = tuple(
            f"{letters}{separator}{number:02d} payload "
            for letters, separator, number in zip(
                ("AB", "CD", "EF", "GH", "IJ", "KL"),
                ("", " ", "-", ".", "/", "_"),
                (12, 23, 34, 45, 56, 67),
            )
        )
        contexts = neutral_contexts + generated_start_contexts
        identifiers = tuple(valid_identifier(index) for index in range(300)) + tuple(
            invalid_silhouette(index) for index in range(300)
        )
        comparison_corpus = tuple(
            context + presentation
            for identifier in identifiers
            for context in contexts
            for presentation in (
                identifier,
                " ".join(
                    identifier[index:index + 4]
                    for index in range(0, len(identifier), 4)
                ),
            )
        )
        previous_pattern = re.compile(r"\b[A-Z]{2}\d{2}[A-Z0-9]{10,30}\b", re.I)
        previous_results = tuple(
            bool(previous_pattern.search(re.sub(r"[_/\\.-]+", " ", value)))
            or phone_band_detects(value)
            for value in comparison_corpus
        )
        current_results = tuple(
            memory_db.contains_pii(value, []) for value in comparison_corpus
        )
        previous_positive_count = sum(previous_results)
        lost = sum(old and not current for old, current in zip(previous_results, current_results))
        gained = sum(current and not old for old, current in zip(previous_results, current_results))
        self.assertEqual(5400, previous_positive_count)
        self.assertEqual(0, lost)
        self.assertGreater(gained, 2700)

        separator_chars = tuple(
            chr(codepoint)
            for codepoint in range(0x2030)
            if memory_db.ACCOUNT_IDENTIFIER_SEPARATORS_RE.fullmatch(chr(codepoint))
        )
        self.assertGreater(len(separator_chars), 5)
        admissible_lengths = tuple(
            length
            for length in range(memory_db.ACCOUNT_IDENTIFIER_MIN_LENGTH - 2,
                                memory_db.ACCOUNT_IDENTIFIER_MAX_LENGTH + 3)
            if memory_db.ACCOUNT_IDENTIFIER_MIN_LENGTH
            <= length
            <= memory_db.ACCOUNT_IDENTIFIER_MAX_LENGTH
        )
        self.assertEqual(
            (memory_db.ACCOUNT_IDENTIFIER_MIN_LENGTH,
             memory_db.ACCOUNT_IDENTIFIER_MAX_LENGTH),
            (admissible_lengths[0], admissible_lengths[-1]),
        )
        block_lengths = tuple(range(1, len(compact)))
        grouped_from_condition = tuple(
            compact[:4] + separator + separator.join(
                compact[index:index + block_length]
                for index in range(4, len(compact), block_length)
            )
            for separator in separator_chars
            for block_length in block_lengths
        )
        date_blocks = tuple(
            match.group(0)
            for match in re.finditer(r"(?:19|20)\d{6}", compact)
        )
        date_grouped_from_condition = tuple(
            separator.join(compact.partition(date_block))
            for separator in separator_chars
            for date_block in date_blocks
        )
        adjacency_chars = tuple(
            char for char in ("A", "z", "0", "9") if char.isalnum()
        )
        phone_core = "34600123456"
        adjacent_phone_from_condition = tuple(
            (char + phone_core if side == "left" else phone_core + char)
            for char in adjacency_chars
            for side in ("left", "right")
        )
        grouped_by_separator = tuple(
            compact[:4] + separator + separator.join(
                compact[index:index + 4] for index in range(4, len(compact), 4)
            )
            for separator in separator_chars
        )
        adjacent_account_from_condition = tuple(
            char + account
            for account in grouped_by_separator
            for char in adjacency_chars
        )
        coordinate_payloads = tuple(dict.fromkeys((
            compact,
            invalid_contiguous,
            *grouped_from_condition,
            *date_grouped_from_condition,
            *adjacent_phone_from_condition,
            *adjacent_account_from_condition,
        )))
        legacy_coordinate_corpus = tuple(
            (coordinate, rendered)
            for payload in coordinate_payloads
            for coordinate, rendered in (
                (None, payload),
                ("file", f"Area_comun/tasks/{payload}.md"),
                ("path", f"Area_comun/archive/{payload}/pack.manifest.json"),
                ("message_id", f"MSG-{payload}"),
            )
            if coordinate not in {"file", "path"}
            or not any(separator in payload for separator in ("/", "\\"))
        )
        legacy_coordinate_current_results = tuple(
            memory_db.contains_pii(value, [], coordinate=coordinate)
            for coordinate, value in legacy_coordinate_corpus
        )
        legacy_coordinate_previous_results = tuple(
            bool(previous_pattern.search(re.sub(r"[_/\\.-]+", " ", value)))
            or phone_band_detects(value)
            for _, value in legacy_coordinate_corpus
        )
        self.assertEqual(
            0,
            sum(
                previous and not current
                for previous, current in zip(
                    legacy_coordinate_previous_results,
                    legacy_coordinate_current_results,
                )
            ),
        )
        coordinate_envelopes_by_type: dict[str, list[str]] = {}
        for coordinate, value, _ in governed_metadata_values:
            if memory_db.contains_pii(value, [], coordinate=coordinate):
                continue
            if memory_db.pii_values_for_coordinate(value, coordinate) == (value,):
                continue
            coordinate_envelopes_by_type.setdefault(coordinate, []).append(value)
        coordinate_envelopes = tuple(
            (coordinate, value)
            for coordinate, values in sorted(coordinate_envelopes_by_type.items())
            for value in sorted(set(values), key=lambda item: (len(item), item))[:8]
        )
        self.assertGreater(len(coordinate_envelopes), 8)

        coordinate_formats_from_condition = tuple(dict.fromkeys((
            (compact, "valid-contiguous"),
            *((presentation, "valid-grouped") for presentation in grouped_by_separator),
            (
                compact[:4] + separator_chars[0] + compact[4:8]
                + separator_chars[-1] + compact[8:],
                "valid-grouped",
            ),
            *((invalid_silhouette(index), "invalid-contiguous") for index in range(12)),
        )))
        coordinate_cases: dict[tuple[str, str], tuple[str, str]] = {}
        for coordinate, envelope in coordinate_envelopes:
            boundaries = tuple(dict.fromkeys((
                0,
                *(match.end() for match in re.finditer(r"[-._/\\]+", envelope)),
                len(envelope),
            )))
            for boundary in boundaries:
                order = (
                    "before" if boundary == 0
                    else "after" if boundary == len(envelope)
                    else "inside"
                )
                left = envelope[:boundary]
                right = envelope[boundary:]
                for presentation, format_name in coordinate_formats_from_condition:
                    rendered = (
                        left
                        + ("-" if left and left[-1].isalnum() else "")
                        + presentation
                        + ("-" if right and right[0].isalnum() else "")
                        + right
                    )
                    if coordinate in {"file", "path"} and (
                        not memory_db.PATH_RE.fullmatch(rendered)
                        or ".." in Path(rendered).parts
                    ):
                        continue
                    parsed_values = memory_db.pii_values_for_coordinate(rendered, coordinate)
                    compact_presentation = memory_db.ACCOUNT_IDENTIFIER_SEPARATORS_RE.sub(
                        "", presentation
                    )
                    if any(
                        compact_presentation
                        in memory_db.ACCOUNT_IDENTIFIER_SEPARATORS_RE.sub("", parsed)
                        for parsed in parsed_values
                    ):
                        continue
                    coordinate_cases[(coordinate, rendered)] = (
                        order,
                        format_name,
                    )
        coordinate_corpus = tuple(coordinate_cases)
        coordinate_types = {coordinate for coordinate, _ in coordinate_corpus}
        coordinate_orders = {order for order, _ in coordinate_cases.values()}
        coordinate_formats = {format_name for _, format_name in coordinate_cases.values()}
        self.assertGreater(len(coordinate_types), 2)
        self.assertEqual({"before", "inside", "after"}, coordinate_orders)
        self.assertEqual(
            {"valid-contiguous", "valid-grouped", "invalid-contiguous"},
            coordinate_formats,
        )
        coordinate_previous_results = tuple(
            bool(previous_pattern.search(re.sub(r"[_/\\.-]+", " ", value)))
            or phone_band_detects(value)
            for _, value in coordinate_corpus
        )
        coordinate_current_results = tuple(
            memory_db.contains_pii(value, [], coordinate=coordinate)
            for coordinate, value in coordinate_corpus
        )
        self.assertGreater(sum(coordinate_previous_results), 0)
        self.assertEqual(
            0,
            sum(
                previous and not current
                for previous, current in zip(
                    coordinate_previous_results, coordinate_current_results
                )
            ),
        )
        self.assertTrue(all(coordinate_current_results))
        production_payloads = tuple(
            (coordinate, rendered)
            for coordinate, rendered in coordinate_corpus
            if coordinate in {"file", "path"}
        )
        self.assertGreater(len(production_payloads), 20)
        for coordinate, rendered in production_payloads:
            if coordinate == "file":
                accepted_file, warnings = memory_db.validate_metadata(
                    {"file": rendered}, set(), []
                )
                self.assertEqual({}, accepted_file)
                self.assertEqual(["rejected frontmatter key file"], warnings)
            else:
                with self.assertRaisesRegex(ValueError, "path contains prohibited PII"):
                    memory_db.require_safe_text(
                        rendered,
                        "path",
                        domain_pii_terms=[],
                    )
        print(
            "TASK-0328 derived-envelope balance: "
            f"population={len(coordinate_corpus)} "
            f"previous_positive={sum(coordinate_previous_results)} "
            f"current_positive={sum(coordinate_current_results)} "
            f"gained={sum(current and not previous for previous, current in zip(coordinate_previous_results, coordinate_current_results))} "
            f"lost={sum(previous and not current for previous, current in zip(coordinate_previous_results, coordinate_current_results))} "
            f"coordinates={len(coordinate_types)} "
            f"orders={len(coordinate_orders)} "
            f"formats={len(coordinate_formats)}"
        )
        clean_coordinates = (
            ("message_id", "MSG-20260809-Zeta-to-Omega-REVIEW-TASK-9999"),
            ("file", "Area_comun/tasks/TASK-9999-cosa.md"),
            ("path", "Area_comun/archive/2026-08/pack.manifest.json"),
        )
        self.assertFalse(
            any(
                memory_db.contains_pii(value, [], coordinate=coordinate)
                for coordinate, value in clean_coordinates
            )
        )

        source = MODULE_PATH.read_text(encoding="utf-8")
        prefix_guard_call = (
            "account_identifier_candidate_has_valid_prefix(\n"
            "            candidate.group(0), value[candidate.end():candidate.end() + 1]\n"
            "        )"
        )
        whole_match_guard_call = "account_identifier_checksum_is_valid(candidate.group(0))"
        all_starts_loop = (
            "def account_identifier_grouped_is_detected(value: str, *, coordinate_bound: bool) -> bool:\n"
            "    for start in ACCOUNT_IDENTIFIER_START_RE.finditer(value):"
        )
        first_start_loop = (
            "def account_identifier_grouped_is_detected(value: str, *, coordinate_bound: bool) -> bool:\n"
            "    for start in tuple(ACCOUNT_IDENTIFIER_START_RE.finditer(value))[:1]:"
        )
        contiguous_guard = (
            "        any(account_identifier_contiguous_is_bounded(candidate) for candidate in pii_values)\n"
            "        or "
        )
        terminator_guard = (
            "        next_char = value[end:end + 1] or following\n"
            "        if next_char and not ACCOUNT_IDENTIFIER_SEPARATORS_RE.fullmatch(next_char):\n"
            "            continue\n"
        )
        object_id_guard = (
            "def git_ref_requires_pii_check(value: Any) -> bool:\n"
            "    return not (\n"
            "        isinstance(value, str)\n"
            "        and bool(re.fullmatch(r\"[0-9a-f]{40}|[0-9a-f]{64}\", value, re.I))\n"
            "    )\n"
        )
        self.assertEqual(1, source.count(prefix_guard_call))
        self.assertEqual(1, source.count(all_starts_loop))
        self.assertEqual(1, source.count(contiguous_guard))
        self.assertEqual(1, source.count(terminator_guard))
        self.assertEqual(1, source.count(object_id_guard))
        coordinate_bound_line = "    coordinate_bound = False\n"
        self.assertEqual(1, source.count(coordinate_bound_line))
        coordinate_blind_identity_return = "        return unexplained_identity_parts(item)\n"
        coordinate_blind_message_return = (
            "        return unexplained_identity_parts(item, message=True)\n"
        )
        coordinate_blind_path_return = "        return tuple(values)\n"
        self.assertEqual(1, source.count(coordinate_blind_identity_return))
        self.assertEqual(1, source.count(coordinate_blind_message_return))
        self.assertEqual(1, source.count(coordinate_blind_path_return))
        pii_values_call = "    pii_values = pii_values_for_coordinate(item, coordinate)\n"
        self.assertEqual(1, source.count(pii_values_call))
        raw_account_guard = (
            "    if (\n"
            "        account_identifier_contiguous_is_bounded(item)\n"
            "        or account_identifier_grouped_is_detected(\n"
            "            item, coordinate_bound=account_coordinate_bound\n"
            "        )\n"
            "    ):\n"
            "        return True\n"
        )
        self.assertEqual(1, source.count(raw_account_guard))
        raw_contiguous_clause = (
            "        account_identifier_contiguous_is_bounded(item)\n"
            "        or "
        )
        self.assertEqual(1, source.count(raw_contiguous_clause))
        mutant_sources = {
            "single_cut": source.replace(
                prefix_guard_call, whole_match_guard_call, 1
            ),
            "first_start": source.replace(all_starts_loop, first_start_loop, 1),
            "checksum_contiguous": source.replace(contiguous_guard, "", 1).replace(
                raw_contiguous_clause, "", 1
            ),
            "missing_terminator": source.replace(terminator_guard, "", 1),
            "object_id_pii": source.replace(
                object_id_guard,
                "def git_ref_requires_pii_check(value: Any) -> bool:\n    return True\n",
                1,
            ),
            "coordinate_blind": source.replace(
                coordinate_blind_identity_return, "        return ()\n"
            ).replace(
                coordinate_blind_message_return, "        return ()\n", 1
            ).replace(coordinate_blind_path_return, "        return ()\n", 1),
            "coordinate_adjacency_blind": source.replace(
                coordinate_bound_line,
                "    coordinate_bound = coordinate is not None\n",
                1,
            ),
            "coordinate_date_blind": source.replace(
                pii_values_call,
                "    pii_values = tuple(\n"
                "        re.sub(r\"(?<!\\d)(?:19|20)\\d{6}(?!\\d)\", \":\", part)\n"
                "        for part in pii_values_for_coordinate(item, coordinate)\n"
                "    )\n",
                1,
            ).replace(
                coordinate_bound_line,
                "    coordinate_bound = coordinate is not None\n",
                1,
            ),
            "coordinate_raw_account_blind": source.replace(raw_account_guard, "", 1),
            "coordinate_raw_contiguous_blind": source.replace(
                raw_contiguous_clause, "", 1
            ),
        }
        self.assertTrue(all(mutant != source for mutant in mutant_sources.values()))

        mutant_context_results: dict[str, tuple[bool, ...]] = {}
        mutant_lost: dict[str, int] = {}
        mutant_governed_gains: dict[str, list[tuple[str, str, str]]] = {}
        mutant_object_id_hits: list[str] = []
        mutant_coordinate_lost: dict[str, int] = {}
        mutant_raw_guard_lost: dict[str, int] = {}
        raw_contiguous_governed_gains: list[tuple[str, str, str]] = []
        with tempfile.TemporaryDirectory(prefix="memory-account-id-mutant-") as temp:
            for name, mutant_source in mutant_sources.items():
                mutant_path = Path(temp) / f"build_memory_db_{name}.py"
                write(mutant_path, mutant_source)
                spec = importlib.util.spec_from_file_location(
                    f"build_memory_db_account_id_{name}", mutant_path
                )
                assert spec and spec.loader
                mutant = importlib.util.module_from_spec(spec)
                sys.modules[spec.name] = mutant
                try:
                    spec.loader.exec_module(mutant)
                    if name in {"single_cut", "first_start", "checksum_contiguous"}:
                        mutant_context_results[name] = tuple(
                            mutant.contains_pii(value, []) for value in context_values
                        )
                        mutant_results = tuple(
                            mutant.contains_pii(value, []) for value in comparison_corpus
                        )
                        mutant_lost[name] = sum(
                            old and not current
                            for old, current in zip(previous_results, mutant_results)
                        )
                    if name == "missing_terminator":
                        mutant_governed_gains[name] = [
                            entry
                            for entry in governed_metadata_values
                            if mutant.contains_pii(entry[1], [])
                            and not memory_db.contains_pii(entry[1], [])
                        ]
                    if name == "object_id_pii":
                        for object_id in object_ids:
                            try:
                                mutant.require_safe_text(
                                    object_id,
                                    "git_ref",
                                    domain_pii_terms=[],
                                    pii_check=mutant.git_ref_requires_pii_check(object_id),
                                )
                            except ValueError:
                                mutant_object_id_hits.append(object_id)
                    if name in {
                        "coordinate_blind", "coordinate_adjacency_blind",
                        "coordinate_date_blind",
                    }:
                        mutant_coordinate_results = tuple(
                            mutant.contains_pii(value, [], coordinate=coordinate)
                            for coordinate, value in legacy_coordinate_corpus
                        )
                        mutant_coordinate_lost[name] = sum(
                            current and not mutant_result
                            for current, mutant_result in zip(
                                legacy_coordinate_current_results,
                                mutant_coordinate_results,
                            )
                        )
                    if name in {
                        "coordinate_raw_account_blind",
                        "coordinate_raw_contiguous_blind",
                    }:
                        mutant_coordinate_results = tuple(
                            mutant.contains_pii(value, [], coordinate=coordinate)
                            for coordinate, value in coordinate_corpus
                        )
                        mutant_raw_guard_lost[name] = sum(
                            current and not mutant_result
                            for current, mutant_result in zip(
                                coordinate_current_results, mutant_coordinate_results
                            )
                        )
                    if name == "coordinate_raw_contiguous_blind":
                        mutant_governed_results = tuple(
                            mutant.contains_pii(value, [], coordinate=coordinate)
                            for coordinate, value, _ in governed_metadata_values
                        )
                        raw_contiguous_governed_gains = [
                            entry
                            for entry, current, mutant_result in zip(
                                governed_metadata_values,
                                governed_current_results,
                                mutant_governed_results,
                            )
                            if current and not mutant_result
                        ]
                finally:
                    sys.modules.pop(spec.name, None)
        self.assertFalse(all(mutant_context_results["single_cut"]))
        self.assertFalse(all(mutant_context_results["first_start"]))
        self.assertGreater(mutant_lost["checksum_contiguous"], 0)
        self.assertGreater(len(mutant_governed_gains["missing_terminator"]), 0)
        self.assertGreater(len(mutant_object_id_hits), 0)
        self.assertTrue(
            all(
                mutant_coordinate_lost[name] > 0
                for name in (
                    "coordinate_blind", "coordinate_adjacency_blind",
                    "coordinate_date_blind",
                )
            ),
            mutant_coordinate_lost,
        )
        self.assertTrue(
            all(
                mutant_raw_guard_lost[name] > 0
                for name in (
                    "coordinate_raw_account_blind",
                    "coordinate_raw_contiguous_blind",
                )
            ),
            mutant_raw_guard_lost,
        )
        self.assertEqual([], raw_contiguous_governed_gains)
        print(
            "TASK-0328 raw-contiguous governed price: "
            f"population={len(governed_metadata_values)} new_marks=0"
        )

    def test_current_decision_is_attested_property_not_status_literal(self) -> None:
        """PERMANENT_NEGATIVE: NEG-MEMORY-CURRENT-DECISION-PROPERTY"""
        with tempfile.TemporaryDirectory(prefix="memory-current-decision-") as temp:
            root = Path(temp)
            make_fixture(root)
            policy_path = root / memory_db.POLICY_PATH
            policy = json.loads(policy_path.read_text(encoding="utf-8"))
            policy["extra_status_values"] = ["future-vocabulary"]
            expected_shipped_currentness = {
                "current": "active", "non_current": "superseded",
                "non_current_when": "superseded_by_present_or_status_declared_non_current",
                "current_statuses": ["accepted", "active", "approved"],
                "non_current_statuses": [
                    "archived", "cancelled", "draft", "proposed", "rejected", "superseded",
                ],
                "missing_status": "current_with_warning",
            }
            shipped_policy = json.loads((ROOT / memory_db.POLICY_PATH).read_text(encoding="utf-8"))
            shipped_currentness = shipped_policy["decision_policy_state"]
            self.assertEqual(expected_shipped_currentness, shipped_currentness)
            policy["decision_policy_state"] = json.loads(json.dumps(shipped_currentness))
            policy["decision_policy_state"]["current_statuses"].append("future-vocabulary")
            write(policy_path, json.dumps(policy, sort_keys=True) + "\n")
            live_contract = (ROOT / "AGENTS.md").read_text(encoding="utf-8-sig")
            cited = set(re.findall(r"DECISION-[0-9]{4}", live_contract))
            write(root / "AGENTS.md", live_contract)
            for decision_id in cited:
                matches = list((ROOT / "Area_comun/decisions").glob(f"{decision_id}-*.md"))
                self.assertEqual(1, len(matches), decision_id)
                write(
                    root / f"Area_comun/decisions/{matches[0].name}",
                    matches[0].read_text(encoding="utf-8-sig"),
                )
            for decision_id, status in {
                "DECISION-ACCEPTED": "accepted", "DECISION-FUTURE": "future-vocabulary",
                "DECISION-OLD": "accepted", "DECISION-PROPOSED": "proposed",
                "DECISION-REJECTED": "rejected", "DECISION-RETIRED": "superseded",
            }.items():
                superseded = "superseded_by: DECISION-ACCEPTED\n" if decision_id == "DECISION-OLD" else ""
                write(root / f"Area_comun/decisions/{decision_id}.md", f"---\ndecision_id: {decision_id}\nstatus: {status}\n{superseded}---\n")
            write(
                root / "Area_comun/decisions/DECISION-MISSING-STATUS.md",
                "---\ndecision_id: DECISION-MISSING-STATUS\n---\n",
            )
            commit = commit_fixture(root, "declare currentness policy")
            artifacts, _ = memory_db.load_artifacts(root, commit)
            attested_policy = memory_db.memory_index_policy(root, commit)
            cited = set(re.findall(r"DECISION-[0-9]{4}", memory_db.git_blob(root, commit, "AGENTS.md").decode("utf-8")))
            rows = {artifact.artifact_id: memory_db.policy_row(artifact, attested_policy) for artifact in artifacts if artifact.artifact_type == "decision"}
            hot = {decision_id for decision_id in cited if rows[decision_id][7] == 1}
            self.assertEqual(cited, hot)
            literal_mutant_hot = {
                artifact.artifact_id for artifact in artifacts
                if artifact.artifact_type == "decision"
                and artifact.metadata.get("status") == "active"
            }
            self.assertNotEqual(cited, literal_mutant_hot)
            mutant_current = lambda artifact: not memory_db.value_list(artifact.metadata.get("superseded_by"))
            mutant_hot = {
                artifact.artifact_id for artifact in artifacts
                if artifact.artifact_type == "decision"
                and mutant_current(artifact)
            }
            self.assertNotEqual(hot, mutant_hot)
            third_state_row = rows["DECISION-FUTURE"]
            self.assertEqual("active", third_state_row[1])
            self.assertEqual("superseded", rows["DECISION-PROPOSED"][1])
            self.assertEqual("superseded", rows["DECISION-REJECTED"][1])
            self.assertEqual("superseded", rows["DECISION-RETIRED"][1])
            self.assertEqual("superseded", rows["DECISION-OLD"][1])
            self.assertEqual("active", rows["DECISION-MISSING-STATUS"][1])
            production_hot = {
                decision_id for decision_id, row in rows.items() if row[7] == 1
            }
            same_population_pointer_mutant = production_hot | {"DECISION-OLD"}
            self.assertNotEqual(production_hot, same_population_pointer_mutant)
            write(
                root / "Area_comun/decisions/DECISION-UNREGISTERED-RETIRED.md",
                "---\ndecision_id: DECISION-UNREGISTERED-RETIRED\nstatus: retired\n---\n",
            )
            unregistered_commit = commit_fixture(root, "unregistered retirement vocabulary")
            with self.assertRaisesRegex(
                ValueError,
                r"DECISION-UNREGISTERED-RETIRED\.md: decision currentness status 'retired' is not classified",
            ):
                memory_db.load_artifacts(root, unregistered_commit)
            (root / "Area_comun/decisions/DECISION-UNREGISTERED-RETIRED.md").unlink()
            commit_fixture(root, "remove unregistered retirement vocabulary")
            unclassified = json.loads(policy_path.read_text(encoding="utf-8"))
            unclassified["decision_policy_state"]["current_statuses"].remove("future-vocabulary")
            write(policy_path, json.dumps(unclassified, sort_keys=True) + "\n")
            unclassified_commit = commit_fixture(root, "unclassified currentness vocabulary")
            with self.assertRaisesRegex(ValueError, "not classified"):
                memory_db.load_artifacts(root, unclassified_commit)
            write(policy_path, json.dumps(attested_policy, sort_keys=True) + "\n")
            unattested = json.loads(policy_path.read_text(encoding="utf-8"))
            unattested["decision_policy_state"]["current"] = "historical"
            write(policy_path, json.dumps(unattested, sort_keys=True) + "\n")
            self.assertEqual(attested_policy, memory_db.memory_index_policy(root, commit))
            write(policy_path, json.dumps(attested_policy, sort_keys=True) + "\n")
            write(root / memory_db.RULES_PATH, json.dumps({"rules": [{"rule_id": "RULE-PRESENT", "artifact_type": "task", "selector": "status=done", "target_retention_class": "cold", "requires_stub": 0, "requires_active_policy_check": 1, "enabled": 1, "created_by_decision": "DECISION-ACCEPTED"}]}) + "\n")
            commit_fixture(root, "accepted-backed rule")
            self.assertEqual("pass", check_memory_db_drift.fast_check(root)["result"])
            rules = json.loads((root / memory_db.RULES_PATH).read_text(encoding="utf-8"))
            rules["rules"][0]["created_by_decision"] = "DECISION-MISSING"
            write(root / memory_db.RULES_PATH, json.dumps(rules) + "\n")
            commit_fixture(root, "missing-backed rule")
            with self.assertRaisesRegex(ValueError, "absent or inactive"):
                check_memory_db_drift.fast_check(root)
            rules["rules"][0]["created_by_decision"] = "DECISION-PROPOSED"
            write(root / memory_db.RULES_PATH, json.dumps(rules) + "\n")
            commit_fixture(root, "proposed-backed rule")
            with self.assertRaisesRegex(ValueError, "absent or inactive"):
                check_memory_db_drift.fast_check(root)
            rules["rules"][0]["created_by_decision"] = "DECISION-RETIRED"
            write(root / memory_db.RULES_PATH, json.dumps(rules) + "\n")
            commit_fixture(root, "retired-backed rule")
            with self.assertRaisesRegex(ValueError, "absent or inactive"):
                check_memory_db_drift.fast_check(root)


def domain_pii_default_violations(module_paths: tuple[Path, ...]) -> list[str]:
    violations: list[str] = []
    for module_path in module_paths:
        tree = ast.parse(module_path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            arguments = getattr(node, "args", None)
            if not isinstance(arguments, ast.arguments):
                continue
            positional = [*arguments.posonlyargs, *arguments.args]
            positional_defaults = (
                positional[-len(arguments.defaults) :] if arguments.defaults else []
            )
            for argument in positional_defaults:
                if argument.arg == "domain_pii_terms":
                    violations.append(f"{module_path.name}:{argument.lineno}")
            for argument, default in zip(arguments.kwonlyargs, arguments.kw_defaults):
                if argument.arg == "domain_pii_terms" and default is not None:
                    violations.append(f"{module_path.name}:{argument.lineno}")
    return violations


if __name__ == "__main__":
    unittest.main(verbosity=2)
