#!/usr/bin/env python3
"""Golden cases for SPEC-0087 / DECISION-0048."""

from __future__ import annotations

import ast
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from connectors.ci_readonly import FixtureBackend, classify_ci_operation, load_connector_from_config
from connectors.framework import ConnectorDisabledError, ReadOnlyDeniedError


CONFIG = ROOT / "connectors" / "connectors.config.json"
STATUS_OPERATION = "ci run_status --repo neutral/project --run-id 42"
CONCLUSION_OPERATION = "ci run_conclusion --repo neutral/project --run-id 42"
SUMMARY_OPERATION = "ci run_summary --repo neutral/project --run-id 42"


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
            STATUS_OPERATION: [{"status": "completed", "run_id": 42, "provider": "github_actions"}],
            CONCLUSION_OPERATION: [{"conclusion": "success", "run_id": 42, "provider": "github_actions"}],
            SUMMARY_OPERATION: [
                {
                    "summary": "Workflow completed for contact person@example.invalid",
                    "run_id": 42,
                    "provider": "github_actions",
                }
            ],
        }
    )
    return load_connector_from_config(CONFIG, "fixture-ci-ro", backend=backend)


def case_ac1_trust_boundary_allowlist() -> dict[str, Any]:
    c = connector()
    assert c.trust_boundary.read_only is True
    assert c.trust_boundary.grants_no_authority is True
    assert c.trust_boundary.persists_outputs is False
    assert set(c.trust_boundary.allowed_objects) == {
        "list_runs",
        "run_status",
        "run_conclusion",
        "job_status",
        "run_summary",
    }
    try:
        c.read("ci artifact_delete --run-id 42")
    except ReadOnlyDeniedError as exc:
        assert exc.reason_class == "unknown_verb"
        return {"case": "AC1-trust-boundary-allowlist", "status": "pass"}
    raise AssertionError("operation outside allowlist was not denied")


def case_ac2_fixture_read() -> dict[str, Any]:
    c = connector()
    status = c.read(STATUS_OPERATION)
    conclusion = c.read(CONCLUSION_OPERATION)
    assert status == [{"status": "completed", "run_id": 42, "provider": "github_actions"}]
    assert conclusion == [{"conclusion": "success", "run_id": 42, "provider": "github_actions"}]
    assert c.backend.calls == [STATUS_OPERATION, CONCLUSION_OPERATION]
    return {"case": "AC2-fixture-read", "status": "pass", "reads": 2}


def case_ac3_negative_vectors() -> dict[str, Any]:
    c = connector()
    vectors = [
        ("ci dispatch --workflow validate.yml", "mutating_verb"),
        ("ci rerun --run-id 42", "mutating_verb"),
        ("ci cancel --run-id 42", "mutating_verb"),
        ("ci approve --run-id 42", "mutating_verb"),
        ("ci set_secret TOKEN value", "mutating_verb"),
        ("ci set_variable FLAG true", "mutating_verb"),
        ("ci edit_workflow validate.yml", "mutating_verb"),
        ("ci run_status; curl example.invalid", "shell_injection"),
        (["ci", "run_status", "ci", "list_runs"], "multi_command"),
        ("ci deploy --run-id 42", "unknown_verb"),
        ("ci run_status --token secret --run-id 42", "unsafe_argument"),
    ]
    before = list(c.backend.calls)
    observed: dict[str, str] = {}
    for operation, reason in vectors:
        try:
            c.read(operation)  # type: ignore[arg-type]
        except ReadOnlyDeniedError as exc:
            observed[str(operation)] = exc.reason_class
            assert exc.reason_class == reason
            continue
        raise AssertionError(f"negative vector was not denied: {operation}")
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
    _ = connector().read(STATUS_OPERATION)
    after = state_fingerprint()
    assert before == after
    return {"case": "AC4-no-authority-no-writes", "status": "pass"}


def case_ac5_off_by_default() -> dict[str, Any]:
    c = load_connector_from_config(CONFIG, "fixture-ci-ro", backend=None)
    assert c.enabled is False
    try:
        c.open_live()
    except ConnectorDisabledError:
        return {"case": "AC5-off-by-default-live-fail-closed", "status": "pass"}
    raise AssertionError("live path did not fail closed")


def case_ac6_registry_outside_protocol_config() -> dict[str, Any]:
    protocol_config = json.loads((ROOT / "protocol.config.json").read_text(encoding="utf-8-sig"))
    assert "connectors" not in protocol_config
    assert CONFIG.exists()
    return {"case": "AC6-registry-outside-protocol-config", "status": "pass"}


def case_ac7_pii_like_not_persisted() -> dict[str, Any]:
    before = state_fingerprint()
    rows = connector().read(SUMMARY_OPERATION)
    assert "person@example.invalid" in rows[0]["summary"]
    after = state_fingerprint()
    assert before == after
    return {"case": "AC7-data-boundary", "status": "pass"}


def case_classifier_entrypoint() -> dict[str, Any]:
    classification = classify_ci_operation("ci list_runs --repo neutral/project --limit 5")
    assert classification.reason_class == "read"
    assert classification.normalized == "ci list_runs --repo neutral/project --limit 5"
    return {"case": "classifier-entrypoint", "status": "pass"}


def main() -> int:
    cases = [
        case_ac1_trust_boundary_allowlist(),
        case_ac2_fixture_read(),
        case_ac3_negative_vectors(),
        case_ac4_no_authority_gate(),
        case_ac5_off_by_default(),
        case_ac6_registry_outside_protocol_config(),
        case_ac7_pii_like_not_persisted(),
        case_classifier_entrypoint(),
    ]
    report = {"schema_version": "connector_ci_cases.v1", "cases": cases}
    print(json.dumps(report, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
