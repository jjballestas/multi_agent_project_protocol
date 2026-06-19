#!/usr/bin/env python3
"""Golden cases for SPEC-0085 / DECISION-0048."""

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

from connectors.framework import ConnectorDisabledError, ReadOnlyDeniedError
from connectors.git_readonly import FixtureBackend, classify_git_operation, load_connector_from_config


CONFIG = ROOT / "connectors" / "connectors.config.json"
LOG_COMMAND = "git log --oneline --max-count=2"
DIFF_COMMAND = "git diff --stat HEAD~1 HEAD"
PII_COMMAND = "git show HEAD:sample.txt"


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
            LOG_COMMAND: [
                {"stdout": "a1b2c3d neutral change\nb2c3d4e previous neutral change\n", "stderr": "", "exit_code": 0}
            ],
            DIFF_COMMAND: [{"stdout": " README.md | 2 ++\n 1 file changed, 2 insertions(+)\n", "stderr": "", "exit_code": 0}],
            PII_COMMAND: [{"stdout": "contact: person@example.invalid\n", "stderr": "", "exit_code": 0}],
        }
    )
    return load_connector_from_config(CONFIG, "fixture-git-ro", backend=backend)


def case_ac1_trust_boundary_allowlist() -> dict[str, Any]:
    c = connector()
    assert c.trust_boundary.read_only is True
    assert c.trust_boundary.grants_no_authority is True
    assert c.trust_boundary.persists_outputs is False
    assert set(c.trust_boundary.allowed_objects) == {"status", "log", "diff", "show", "ls-files", "rev-parse", "blame"}
    try:
        c.read("git grep marker")
    except ReadOnlyDeniedError as exc:
        assert exc.reason_class == "unknown_verb"
        return {"case": "AC1-trust-boundary-allowlist", "status": "pass"}
    raise AssertionError("operation outside allowlist was not denied")


def case_ac2_fixture_inspection() -> dict[str, Any]:
    c = connector()
    rows = c.read(LOG_COMMAND)
    assert rows == [{"stdout": "a1b2c3d neutral change\nb2c3d4e previous neutral change\n", "stderr": "", "exit_code": 0}]
    assert c.backend.calls == [LOG_COMMAND]
    rows = c.read(DIFF_COMMAND)
    assert "README.md" in rows[0]["stdout"]
    assert c.backend.calls == [LOG_COMMAND, DIFF_COMMAND]
    return {"case": "AC2-fixture-inspection", "status": "pass", "reads": 2}


def case_ac3_negative_vectors() -> dict[str, Any]:
    c = connector()
    vectors = [
        ("git commit -m x", "mutating_verb"),
        ("git push origin main", "mutating_verb"),
        ("git reset --hard HEAD", "mutating_verb"),
        ("git clean -fd", "mutating_verb"),
        ("git checkout main", "mutating_verb"),
        ("git branch -D old", "mutating_verb"),
        ("git log; rm -rf .", "shell_injection"),
        (["git", "log", "git", "status"], "multi_command"),
        ("git frobnicate", "unknown_verb"),
        ("git log --upload-pack=helper", "unsafe_argument"),
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
    _ = connector().read(LOG_COMMAND)
    after = state_fingerprint()
    assert before == after
    return {"case": "AC4-no-authority-no-writes", "status": "pass"}


def case_ac5_off_by_default() -> dict[str, Any]:
    c = load_connector_from_config(CONFIG, "fixture-git-ro", backend=None)
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
    rows = connector().read(PII_COMMAND)
    assert rows[0]["stdout"] == "contact: person@example.invalid\n"
    after = state_fingerprint()
    assert before == after
    return {"case": "AC7-data-boundary", "status": "pass"}


def case_classifier_entrypoint() -> dict[str, Any]:
    classification = classify_git_operation("git status --short")
    assert classification.reason_class == "inspection"
    assert classification.normalized == "git status --short"
    return {"case": "classifier-entrypoint", "status": "pass"}


def main() -> int:
    cases = [
        case_ac1_trust_boundary_allowlist(),
        case_ac2_fixture_inspection(),
        case_ac3_negative_vectors(),
        case_ac4_no_authority_gate(),
        case_ac5_off_by_default(),
        case_ac6_registry_outside_protocol_config(),
        case_ac7_pii_like_not_persisted(),
        case_classifier_entrypoint(),
    ]
    report = {"schema_version": "connector_git_cases.v1", "cases": cases}
    print(json.dumps(report, indent=2, ensure_ascii=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
