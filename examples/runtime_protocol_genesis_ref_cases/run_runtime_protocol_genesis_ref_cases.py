#!/usr/bin/env python3
"""Golden cases for protocol genesis-by-reference B.4."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
MATERIALIZE_CASES = ROOT / "examples/runtime_protocol_materialize_cases"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(MATERIALIZE_CASES))

from run_runtime_protocol_materialize_cases import (  # noqa: E402
    build_fixture,
    build_genesis_snapshot,
    init_git,
    read_json,
    run,
    turn_report,
    write_json,
)
from runtime.apply import apply_gate_and_commit  # noqa: E402
from runtime.eventlog import canonical_hash, read_jsonl_torn_safe  # noqa: E402
from runtime.protocol_replay import (  # noqa: E402
    PROTOCOL_SNAPSHOT_SCHEMA_VERSION,
    ProtocolSnapshotRefError,
    current_protocol_snapshot,
    materialize_protocol_state,
    materialize_to_disk,
    prepare_authoritative_migration,
    protocol_authoritative_enabled,
    protocol_state_drift,
    write_genesis_reference,
)


FIXED_TIMESTAMP = "2026-06-07T00:00:00Z"
FIXED_COMMIT = "commit-fixture"


def validator(root: Path, *, powershell: bool = False, check: bool = True) -> subprocess.CompletedProcess[str]:
    if powershell:
        shell = shutil.which("pwsh") or shutil.which("powershell")
        if not shell:
            return subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
        return run(
            [
                shell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(ROOT / "scripts/validate_collaboration_state.ps1"),
                "-Root",
                str(root),
            ],
            check=check,
        )
    return run([sys.executable, str(ROOT / "scripts/validate_collaboration_state.py"), "--root", str(root)], check=check)


def build_runtime_fixture(
    root: Path,
    *,
    event_enabled: bool = True,
    materialize: bool = False,
    enforce: bool = False,
    authoritative: bool = False,
    tier: str = "runtime",
    init_repo: bool = False,
) -> None:
    build_fixture(
        root,
        event_enabled=event_enabled,
        materialize=materialize,
        enforce=enforce,
        authoritative=authoritative,
        tier=tier,
        init_repo=init_repo,
    )


def genesis_ref(root: Path, *, actor: str = "Codex", timestamp: str = FIXED_TIMESTAMP) -> dict[str, Any]:
    return write_genesis_reference(root, actor_id=actor, timestamp=timestamp, commit=FIXED_COMMIT)


def event_payloads(root: Path) -> list[dict[str, Any]]:
    return [event.get("payload") or {} for event in read_jsonl_torn_safe(root / "runtime/state/events.jsonl")]


def diverge_project_title(root: Path) -> None:
    project = read_json(root / "Area_comun/state/PROJECT_STATE.json")
    project["active_tasks"][0]["title"] = "Manual edit after genesis-ref"
    write_json(root / "Area_comun/state/PROJECT_STATE.json", project)


def disable_event_state(root: Path) -> None:
    config = read_json(root / "protocol.config.json")
    config["event_state"] = {"enabled": False, "materialize": False, "enforce": False, "authoritative": False}
    write_json(root / "protocol.config.json", config)


def assert_snapshot_ref_shape(result: dict[str, Any]) -> None:
    event_payload = result["event"]["payload"]
    assert sorted(event_payload) == ["snapshot_ref"], event_payload
    assert "state" not in event_payload
    assert "protocol_state" not in event_payload
    ref = event_payload["snapshot_ref"]
    assert ref == result["snapshot_ref"], (ref, result["snapshot_ref"])
    assert ref["schema_version"] == PROTOCOL_SNAPSHOT_SCHEMA_VERSION
    assert ref["commit"] == FIXED_COMMIT
    assert ref["actor"] == "Codex"
    assert ref["timestamp"] == FIXED_TIMESTAMP


def case_genesis_ref_writes_snapshot_and_pointer_only_event() -> None:
    with tempfile.TemporaryDirectory(prefix="protocol-genesis-ref-shape-") as temp:
        root = Path(temp)
        build_runtime_fixture(root)
        result = genesis_ref(root)
        assert_snapshot_ref_shape(result)
        snapshot_path = Path(result["snapshot_path"])
        assert snapshot_path.exists(), snapshot_path
        document = read_json(snapshot_path)
        assert canonical_hash(document) == result["snapshot_ref"]["hash"]
        assert snapshot_path.name == f"{result['snapshot_ref']['hash']}.json"

        ref_payload_size = len(json.dumps(result["event"]["payload"], sort_keys=True))
        embedded_payload = {
            "state": result["snapshot"]["state"],
            "canonical_hash": result["snapshot"]["canonical_hash"],
        }
        embedded_payload_size = len(json.dumps(embedded_payload, sort_keys=True))
        assert ref_payload_size < embedded_payload_size, (ref_payload_size, embedded_payload_size)


def case_round_trip_genesis_ref_materializes_hot_state() -> None:
    with tempfile.TemporaryDirectory(prefix="protocol-genesis-ref-roundtrip-") as temp:
        root = Path(temp)
        build_runtime_fixture(root, materialize=True)
        expected = materialize_protocol_state(build_genesis_snapshot(root))
        result = genesis_ref(root)
        snapshot = current_protocol_snapshot(root)
        assert materialize_protocol_state(snapshot) == expected
        materialize = materialize_to_disk(root, snapshot)
        assert materialize["materialized"] is True, materialize
        assert {path: read_json(root / path) for path in expected} == expected
        assert event_payloads(root)[0] == {"snapshot_ref": result["snapshot_ref"]}


def case_snapshot_ref_integrity_missing_or_mismatch_blocks() -> None:
    with tempfile.TemporaryDirectory(prefix="protocol-genesis-ref-missing-") as temp:
        root = Path(temp)
        build_runtime_fixture(root)
        result = genesis_ref(root)
        Path(result["snapshot_path"]).unlink()
        try:
            current_protocol_snapshot(root)
        except ProtocolSnapshotRefError as exc:
            assert "missing" in str(exc)
        else:
            raise AssertionError("missing snapshot_ref content did not block replay")

    with tempfile.TemporaryDirectory(prefix="protocol-genesis-ref-mismatch-") as temp:
        root = Path(temp)
        build_runtime_fixture(root)
        result = genesis_ref(root)
        path = Path(result["snapshot_path"])
        document = read_json(path)
        document["snapshot"]["state"]["project_state"]["status"] = "tampered"
        write_json(path, document)
        try:
            current_protocol_snapshot(root)
        except ProtocolSnapshotRefError as exc:
            assert "hash mismatch" in str(exc)
        else:
            raise AssertionError("tampered snapshot_ref content did not block replay")


def case_validator_reports_snapshot_ref_integrity_errors_py_and_ps() -> None:
    with tempfile.TemporaryDirectory(prefix="protocol-genesis-ref-validator-") as temp:
        root = Path(temp)
        build_runtime_fixture(root, event_enabled=True, materialize=False)
        result = genesis_ref(root)
        Path(result["snapshot_path"]).unlink()
        py = validator(root, check=False)
        assert py.returncode != 0, py.stdout
        assert "Runtime protocol state drift check failed" in py.stdout, py.stdout
        ps = validator(root, powershell=True, check=False)
        if ps.args:
            assert ps.returncode != 0, ps.stdout
            assert "Runtime protocol state drift check failed" in ps.stdout, ps.stdout


def case_authoritative_on_manual_edit_hard_fails() -> None:
    with tempfile.TemporaryDirectory(prefix="protocol-genesis-ref-authoritative-") as temp:
        root = Path(temp)
        build_runtime_fixture(root, event_enabled=True, materialize=True, enforce=True, authoritative=True)
        assert protocol_authoritative_enabled(read_json(root / "protocol.config.json")) is True
        genesis_ref(root)
        diverge_project_title(root)
        py = validator(root, check=False)
        assert py.returncode != 0, py.stdout
        assert "hard-fail B.3" in py.stdout, py.stdout
        assert "Area_comun/state/PROJECT_STATE.json" in py.stdout, py.stdout
        ps = validator(root, powershell=True, check=False)
        if ps.args:
            assert ps.returncode != 0, ps.stdout
            assert "hard-fail B.3" in ps.stdout, ps.stdout


def case_off_and_coordination_tier_keep_manual_mode() -> None:
    with tempfile.TemporaryDirectory(prefix="protocol-genesis-ref-off-") as temp:
        root = Path(temp)
        build_runtime_fixture(root, event_enabled=False, materialize=False, enforce=False, authoritative=False)
        genesis_ref(root)
        diverge_project_title(root)
        py = validator(root, check=False)
        assert py.returncode == 0, py.stdout
        assert "Runtime protocol state drift" not in py.stdout, py.stdout

    with tempfile.TemporaryDirectory(prefix="protocol-genesis-ref-coordination-") as temp:
        root = Path(temp)
        build_runtime_fixture(root, event_enabled=True, materialize=True, enforce=True, authoritative=True, tier="coordination")
        assert protocol_authoritative_enabled(read_json(root / "protocol.config.json")) is False
        genesis_ref(root)
        diverge_project_title(root)
        py = validator(root, check=False)
        assert py.returncode == 0, py.stdout
        assert "warning-only B.1" in py.stdout, py.stdout


def case_rollback_by_flags_after_runtime_intent_is_reversible() -> None:
    with tempfile.TemporaryDirectory(prefix="protocol-genesis-ref-rollback-") as temp:
        root = Path(temp)
        build_runtime_fixture(root, event_enabled=True, materialize=True, enforce=True, authoritative=True)
        migration = prepare_authoritative_migration(root, actor_id="Codex", timestamp=FIXED_TIMESTAMP, commit=FIXED_COMMIT)
        assert migration["authoritative_ready"] is True
        assert Path(migration["snapshot_path"]).exists()
        init_git(root)
        result = apply_gate_and_commit(turn_report(), root)
        assert result["green"] is True, result
        assert result["protocol_materialization"]["materialized"] is True, result
        assert result["protocol_drift_gate"]["enforced"] is True, result
        assert protocol_state_drift(root)["has_drift"] is False

        disable_event_state(root)
        diverge_project_title(root)
        py = validator(root, check=False)
        assert py.returncode == 0, py.stdout
        assert "hard-fail B.3" not in py.stdout, py.stdout


def case_genesis_ref_is_deterministic_with_provided_metadata() -> None:
    with tempfile.TemporaryDirectory(prefix="protocol-genesis-ref-deterministic-") as temp:
        root = Path(temp)
        build_runtime_fixture(root)
        first = genesis_ref(root, timestamp=FIXED_TIMESTAMP)
        second = genesis_ref(root, timestamp=FIXED_TIMESTAMP)
        assert second["event"].get("deduped") is True, second["event"]
        assert first["snapshot_ref"] == second["snapshot_ref"]
        assert first["snapshot_ref"]["timestamp"] == FIXED_TIMESTAMP
        assert first["snapshot_ref"]["commit"] == FIXED_COMMIT


def case_b1_b2_b3_regression_suites_still_pass() -> None:
    replay = run([sys.executable, str(ROOT / "examples/runtime_protocol_replay_cases/run_runtime_protocol_replay_cases.py")])
    materialize = run([sys.executable, str(ROOT / "examples/runtime_protocol_materialize_cases/run_runtime_protocol_materialize_cases.py")])
    enforce = run([sys.executable, str(ROOT / "examples/runtime_protocol_enforce_cases/run_runtime_protocol_enforce_cases.py")])
    assert "OK:" in replay.stdout, replay.stdout
    assert "OK:" in materialize.stdout, materialize.stdout
    assert "OK:" in enforce.stdout, enforce.stdout


def main() -> int:
    cases = [
        case_genesis_ref_writes_snapshot_and_pointer_only_event,
        case_round_trip_genesis_ref_materializes_hot_state,
        case_snapshot_ref_integrity_missing_or_mismatch_blocks,
        case_validator_reports_snapshot_ref_integrity_errors_py_and_ps,
        case_authoritative_on_manual_edit_hard_fails,
        case_off_and_coordination_tier_keep_manual_mode,
        case_rollback_by_flags_after_runtime_intent_is_reversible,
        case_genesis_ref_is_deterministic_with_provided_metadata,
        case_b1_b2_b3_regression_suites_still_pass,
    ]
    failures: list[dict[str, Any]] = []
    for case in cases:
        try:
            case()
        except Exception as exc:  # noqa: BLE001 - compact golden failure reporting
            failures.append({"case": case.__name__, "error": str(exc)})
    if failures:
        print(json.dumps({"status": "FAILED", "failures": failures}, indent=2))
        return 1
    print(f"OK: {len(cases)} runtime protocol genesis-ref golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
