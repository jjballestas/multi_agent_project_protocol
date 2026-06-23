#!/usr/bin/env python3
"""Golden cases for SPEC-0083 / DECISION-0044."""

from __future__ import annotations

import ast
import hashlib
import json
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from connectors.framework import ConnectorDisabledError, ReadOnlyDeniedError
from connectors.sqlserver_readonly import FixtureBackend, load_connector_from_config, resolve_config_path


CONFIG = ROOT / "connectors" / "connectors.config.json"
QUERY = "SELECT id, label, contact_email FROM catalog.records"


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.exists() else "missing"


def state_fingerprint() -> dict[str, str]:
    paths = [
        ROOT / "runtime" / "state" / "events.jsonl",
        ROOT / "runtime" / "state" / "snapshot.json",
        ROOT / "Area_comun" / "state" / "CLAIMS.json",
        ROOT / "Area_comun" / "state" / "PROJECT_STATE.json",
        ROOT / "Area_comun" / "state" / "TASK_INDEX.json",
    ]
    return {path.relative_to(ROOT).as_posix(): file_hash(path) for path in paths}


def connector() -> Any:
    backend = FixtureBackend(
        {
            QUERY: [
                {"id": 1, "label": "alpha", "contact_email": "person@example.invalid"},
                {"id": 2, "label": "beta", "contact_email": "second@example.invalid"},
            ]
        }
    )
    return load_connector_from_config(CONFIG, "fixture-sqlserver-ro", backend=backend)


def case_ac1_trust_boundary() -> dict[str, Any]:
    c = connector()
    assert c.trust_boundary.read_only is True
    assert c.trust_boundary.grants_no_authority is True
    assert c.trust_boundary.persists_outputs is False
    try:
        c.read("SELECT id FROM other.records")
    except ReadOnlyDeniedError as exc:
        assert exc.reason_class == "object_not_allowlisted"
        return {"case": "AC1-trust-boundary-allowlist", "status": "pass"}
    raise AssertionError("object outside allowlist was not denied")


def case_ac2_read_positive() -> dict[str, Any]:
    c = connector()
    rows = c.read(QUERY)
    assert rows == [
        {"id": 1, "label": "alpha", "contact_email": "person@example.invalid"},
        {"id": 2, "label": "beta", "contact_email": "second@example.invalid"},
    ]
    assert c.backend.calls == [QUERY.lower()]
    return {"case": "AC2-fixture-read", "status": "pass", "rows": len(rows)}


def case_ac3_negative_vectors() -> dict[str, Any]:
    c = connector()
    vectors = {
        "INSERT INTO catalog.records VALUES (3)": "dml",
        "UPDATE catalog.records SET label = 'x'": "dml",
        "DELETE FROM catalog.records": "dml",
        "DROP TABLE catalog.records": "ddl",
        "EXEC refresh_records": "exec_not_allowlisted",
        "SELECT id FROM catalog.records; DELETE FROM catalog.records": "multi_statement",
        "UPSERT catalog.records": "unknown_verb",
    }
    before = list(c.backend.calls)
    observed: dict[str, str] = {}
    for sql, reason in vectors.items():
        try:
            c.read(sql)
        except ReadOnlyDeniedError as exc:
            observed[sql] = exc.reason_class
            assert exc.reason_class == reason
            continue
        raise AssertionError(f"mutating vector was not denied: {sql}")
    assert c.backend.calls == before
    return {"case": "AC3-negative-vectors", "status": "pass", "vectors": len(observed)}


def case_ac4_no_authority_gate() -> dict[str, Any]:
    forbidden_modules = {
        "runtime.eventlog",
        "runtime.ledger_ops",
        "runtime.submit_intent",
        "runtime.apply",
        "runtime.protocol_replay",
    }
    forbidden_names = {"EventWriter", "submit_intent", "apply_turn", "atomic_append_jsonl"}
    findings: list[str] = []
    for path in sorted((ROOT / "connectors").rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in forbidden_modules or alias.name.startswith("runtime."):
                        findings.append(f"{path.relative_to(ROOT)} imports {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                module = node.module or ""
                if module in forbidden_modules or module.startswith("runtime."):
                    findings.append(f"{path.relative_to(ROOT)} imports {module}")
                for alias in node.names:
                    if alias.name in forbidden_names:
                        findings.append(f"{path.relative_to(ROOT)} imports {alias.name}")
    assert not findings, findings

    before = state_fingerprint()
    _ = connector().read(QUERY)
    after = state_fingerprint()
    assert before == after
    return {"case": "AC4-no-authority-no-writes", "status": "pass"}


def case_ac5_off_by_default() -> dict[str, Any]:
    c = load_connector_from_config(CONFIG, "fixture-sqlserver-ro", backend=None)
    assert c.enabled is False
    try:
        c.open_live()
    except ConnectorDisabledError:
        return {"case": "AC5-off-by-default-live-fail-closed", "status": "pass"}
    raise AssertionError("live path did not fail closed")


def case_ac5_runtime_override_preferred() -> dict[str, Any]:
    with tempfile.TemporaryDirectory() as raw_dir:
        base = Path(raw_dir)
        config = base / "connectors.config.json"
        runtime = base / "connectors.runtime.json"
        config.write_text(
            json.dumps(
                {
                    "schema_version": "connectors.config.v1",
                    "connectors": [
                        {
                            "id": "sqlserver_readonly",
                            "kind": "sqlserver_readonly",
                            "enabled": False,
                            "trust_boundary": {
                                "read_only": True,
                                "grants_no_authority": True,
                                "persists_outputs": False,
                                "access": {"allow": {"schemas": ["connector"], "objects": ["connector.probe"]}},
                                "live_connection": {"principal_least_privilege_required": True},
                            },
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        runtime.write_text(
            json.dumps(
                {
                    "schema_version": "connectors.config.v1",
                    "connectors": [
                        {
                            "id": "sqlserver_readonly",
                            "kind": "sqlserver_readonly",
                            "enabled": True,
                            "trust_boundary": {
                                "read_only": True,
                                "grants_no_authority": True,
                                "persists_outputs": False,
                                "access": {"allow": {"schemas": ["connector"], "objects": ["connector.probe"]}},
                                "live_connection": {"principal_least_privilege_required": True},
                            },
                        }
                    ],
                }
            ),
            encoding="utf-8",
        )
        assert resolve_config_path(config) == runtime
        c = load_connector_from_config(config, "sqlserver_readonly", backend=FixtureBackend({"SELECT 1": [{"ok": 1}]}))
        assert c.enabled is True
    return {"case": "AC11-runtime-override-preferred", "status": "pass"}


def case_ac6_genesis_config_separate() -> dict[str, Any]:
    protocol_config = json.loads((ROOT / "protocol.config.json").read_text(encoding="utf-8-sig"))
    assert "connectors" not in protocol_config
    assert CONFIG.exists()
    return {"case": "AC6-registry-outside-protocol-config", "status": "pass"}


def case_ac7_pii_like_not_persisted() -> dict[str, Any]:
    before = state_fingerprint()
    rows = connector().read(QUERY)
    assert rows[0]["contact_email"] == "person@example.invalid"
    after = state_fingerprint()
    assert before == after
    return {"case": "AC7-data-boundary", "status": "pass"}


def main() -> int:
    cases = [
        case_ac1_trust_boundary(),
        case_ac2_read_positive(),
        case_ac3_negative_vectors(),
        case_ac4_no_authority_gate(),
        case_ac5_off_by_default(),
        case_ac5_runtime_override_preferred(),
        case_ac6_genesis_config_separate(),
        case_ac7_pii_like_not_persisted(),
    ]
    report = {"schema_version": "connector_sqlserver_readonly_cases.v1", "cases": cases}
    print(json.dumps(report, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
