#!/usr/bin/env python3
"""Golden cases for protocol state materialization B.2."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from runtime.apply import apply_gate_and_commit  # noqa: E402
from runtime.protocol_replay import (  # noqa: E402
    ProtocolMaterializationError,
    build_genesis_snapshot,
    current_protocol_snapshot,
    materialize_protocol_state,
    materialize_to_disk,
    protocol_state_drift,
    replay_protocol_state,
    write_genesis,
)


TASK_ID = "TASK-9200"
RUNTIME_TIER_REQUIRED_PATHS = [
    "scripts/validate_collaboration_state.py",
    "scripts/validate_collaboration_state.ps1",
    "scripts/scan_encoding.py",
    "scripts/scan_encoding.ps1",
    "scripts/scan_domain_neutrality.py",
    "scripts/scan_domain_neutrality.ps1",
    "scripts/measure_context_cost.py",
    "scripts/prune_state.py",
    "scripts/prune_state.ps1",
    ".github/workflows/validate.yml",
]


def run(command: list[str], cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=check)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def event(seq: int, event_type: str, payload: dict[str, Any], *, aggregate_id: str = "protocol-state") -> dict[str, Any]:
    return {
        "seq": seq,
        "event_schema_version": "1.0",
        "type": event_type,
        "aggregate_id": aggregate_id,
        "aggregate_version": seq,
        "actor": "Codex",
        "actor_auth": {"method": "not_enforced_phaseB2"},
        "idempotency_key": f"fixture:{seq}",
        "fencing_token": seq,
        "payload": payload,
        "applied": True,
        "ts": "2026-06-07T00:00:00Z",
    }


def hot_docs(status: str = "ready", claim_status: str = "active") -> dict[str, Any]:
    return {
        "task_index": {
            "schema_version": "1.0",
            "tasks": [
                {
                    "id": TASK_ID,
                    "owner": "Codex",
                    "status": status,
                    "type": "implementation",
                    "priority": "normal",
                    "phase": "P2",
                    "file": f"Area_comun/tasks/{TASK_ID}.md",
                    "depends_on": [],
                    "deliverables": [],
                }
            ],
        },
        "project_state": {
            "status": "active",
            "decisions": ["DECISION-0001"],
            "active_tasks": [{"id": TASK_ID, "owner": "Codex", "status": status, "title": "Fixture"}],
        },
        "claims": {
            "schema_version": "1.0",
            "claims": [
                {
                    "claim_id": f"CLAIM-{TASK_ID}-codex",
                    "task_id": TASK_ID,
                    "owner": "Codex",
                    "status": claim_status,
                    "scope": [
                        f"Area_comun/tasks/{TASK_ID}.md",
                        f"Area_comun/state/TASK_INDEX.json#{TASK_ID}",
                        f"Area_comun/state/PROJECT_STATE.json#active_tasks/{TASK_ID}",
                        "Area_comun/state/CLAIMS.json",
                    ],
                    "started_at": "2026-06-07",
                    "updated_at": "2026-06-07",
                    "expires_at": "2026-06-08",
                    "notes": "protocol materialization fixture",
                }
            ],
        },
    }


def write_hot_state(root: Path, docs: dict[str, Any], *, task_status: str = "ready") -> None:
    write_json(root / "Area_comun/state/TASK_INDEX.json", docs["task_index"])
    write_json(root / "Area_comun/state/PROJECT_STATE.json", docs["project_state"])
    write_json(root / "Area_comun/state/CLAIMS.json", docs["claims"])
    write(root / "Area_comun/tasks" / f"{TASK_ID}.md", f"---\nid: {TASK_ID}\nstatus: {task_status}\n---\n\n# Fixture\n")


def build_fixture(
    root: Path,
    *,
    event_enabled: bool,
    materialize: bool,
    enforce: bool = False,
    authoritative: bool = False,
    tier: str = "runtime",
    init_repo: bool = False,
) -> None:
    write_json(
        root / "protocol.config.json",
        {
            "schema_version": "1.0",
            "adoption_tier": tier,
            "runtime": {"enabled": True, "entrypoint": "runtime/orchestrator.py"},
            "event_auth": {"enabled": False},
            "event_state": {
                "enabled": event_enabled,
                "materialize": materialize,
                "enforce": enforce,
                "authoritative": authoritative,
            },
            "domain_neutrality": {"enabled": True, "denylist": [], "scan_globs": [], "exempt_globs": []},
            "state_invariants": [{"path": "status", "equals": "active"}],
        },
    )
    write_hot_state(root, hot_docs("ready", "active"))
    write_json(root / "Area_comun/state/CLAIMS_ARCHIVE.json", {"schema_version": "1.0", "claims": []})
    write_json(root / "Area_comun/state/TASK_INDEX_ARCHIVE.json", {"schema_version": "1.0", "tasks": []})
    for folder in ("open", "answered", "archived"):
        write(root / "Area_comun/mailbox" / folder / ".gitkeep", "\n")
    write(root / "Area_comun/reports/HUMAN_REPORT_TEMPLATE.md", "# Human report\n")
    write(root / "runtime/turn_schema.json", (ROOT / "runtime/turn_schema.json").read_text(encoding="utf-8-sig"))
    if tier == "runtime":
        install_runtime_tier_required_paths(root)
    if init_repo:
        init_git(root)


def install_runtime_tier_required_paths(root: Path) -> None:
    for relative in RUNTIME_TIER_REQUIRED_PATHS:
        source = ROOT / relative
        target = root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def init_git(root: Path) -> None:
    run(["git", "init"], root)
    run(["git", "config", "user.email", "runtime@example.invalid"], root)
    run(["git", "config", "user.name", "Runtime Test"], root)
    run(["git", "add", "."], root)
    run(["git", "commit", "-m", "fixture baseline"], root)


def turn_report() -> dict[str, Any]:
    return {
        "turn_id": "RUN-materialize-0001",
        "task_id": TASK_ID,
        "agent": "Codex",
        "outcome": "done",
        "summary": "Move fixture task to done.",
        "changed_paths": [
            f"Area_comun/tasks/{TASK_ID}.md",
            f"Area_comun/state/TASK_INDEX.json#{TASK_ID}",
            f"Area_comun/state/PROJECT_STATE.json#active_tasks/{TASK_ID}",
            "Area_comun/state/CLAIMS.json",
        ],
        "transitions": {
            "task_status": {"from": "ready", "to": "done"},
            "claims": [{"op": "release", "claim_id": f"CLAIM-{TASK_ID}-codex"}],
        },
        "commit_message": "test(runtime): materialize protocol state",
        "gate": {"human_required": False},
        "next_hint": None,
    }


def state_bytes(root: Path) -> dict[str, bytes]:
    paths = [
        "Area_comun/state/TASK_INDEX.json",
        "Area_comun/state/PROJECT_STATE.json",
        "Area_comun/state/CLAIMS.json",
    ]
    return {path: (root / path).read_bytes() for path in paths}


def validator_stdout(root: Path) -> str:
    result = run([sys.executable, str(ROOT / "scripts/validate_collaboration_state.py"), "--root", str(root)])
    return result.stdout


def case_materialize_writes_canonical_ascii_state() -> None:
    with tempfile.TemporaryDirectory(prefix="protocol-materialize-write-") as temp:
        root = Path(temp)
        snapshot = replay_protocol_state([event(1, "protocol.genesis", {"state": hot_docs("done", "released")})])
        result = materialize_to_disk(root, snapshot)
        expected = materialize_protocol_state(snapshot)
        assert result["paths"] == sorted(expected)
        before = state_bytes(root)
        for relative, document in expected.items():
            raw = (root / relative).read_bytes()
            assert not raw.startswith(b"\xef\xbb\xbf")
            raw.decode("ascii")
            assert read_json(root / relative) == document
        materialize_to_disk(root, snapshot)
        assert state_bytes(root) == before


def case_write_genesis_round_trip_is_idempotent() -> None:
    with tempfile.TemporaryDirectory(prefix="protocol-materialize-genesis-") as temp:
        root = Path(temp)
        build_fixture(root, event_enabled=True, materialize=False)
        expected = materialize_protocol_state(build_genesis_snapshot(root))
        first = write_genesis(root)
        assert first["event"]["type"] == "protocol.genesis"
        snapshot = current_protocol_snapshot(root)
        materialize_to_disk(root, snapshot)
        assert {path: read_json(root / path) for path in expected} == expected
        before = state_bytes(root)
        materialize_to_disk(root, snapshot)
        assert state_bytes(root) == before
        second = write_genesis(root)
        assert second["event"].get("deduped") is True


def case_materialize_rolls_back_on_mid_write_failure() -> None:
    with tempfile.TemporaryDirectory(prefix="protocol-materialize-atomic-") as temp:
        root = Path(temp)
        build_fixture(root, event_enabled=True, materialize=False)
        before = state_bytes(root)
        snapshot = replay_protocol_state([event(1, "protocol.genesis", {"state": hot_docs("done", "released")})])
        try:
            materialize_to_disk(root, snapshot, fail_after_writes=1)
        except ProtocolMaterializationError:
            pass
        else:
            raise AssertionError("materialize_to_disk did not fail")
        assert state_bytes(root) == before


def apply_and_return_state(*, event_enabled: bool, materialize: bool, tier: str) -> dict[str, bytes]:
    with tempfile.TemporaryDirectory(prefix="protocol-materialize-gate-") as temp:
        root = Path(temp)
        build_fixture(root, event_enabled=event_enabled, materialize=materialize, tier=tier, init_repo=True)
        result = apply_gate_and_commit(turn_report(), root)
        assert result["green"] is True, result
        assert result["protocol_materialization"]["materialized"] is False, result
        return state_bytes(root)


def case_runtime_gating_off_is_byte_equivalent() -> None:
    baseline = apply_and_return_state(event_enabled=False, materialize=False, tier="runtime")
    assert apply_and_return_state(event_enabled=True, materialize=False, tier="runtime") == baseline
    assert apply_and_return_state(event_enabled=True, materialize=True, tier="coordination") == baseline


def case_runtime_materialization_on_clears_drift_and_warns_on_divergence() -> None:
    with tempfile.TemporaryDirectory(prefix="protocol-materialize-runtime-") as temp:
        root = Path(temp)
        build_fixture(root, event_enabled=True, materialize=True, tier="runtime")
        write_genesis(root)
        init_git(root)
        result = apply_gate_and_commit(turn_report(), root)
        assert result["green"] is True, result
        assert result["protocol_materialization"]["materialized"] is True, result
        assert protocol_state_drift(root)["has_drift"] is False
        assert "Runtime protocol state drift detected" not in validator_stdout(root)
        project_state = read_json(root / "Area_comun/state/PROJECT_STATE.json")
        project_state["active_tasks"][0]["title"] = "Diverged fixture title"
        write_json(root / "Area_comun/state/PROJECT_STATE.json", project_state)
        stdout = validator_stdout(root)
        assert "Runtime protocol state drift detected" in stdout, stdout


def case_b1_replay_suite_still_passes() -> None:
    completed = run([sys.executable, str(ROOT / "examples/runtime_protocol_replay_cases/run_runtime_protocol_replay_cases.py")])
    assert "OK:" in completed.stdout, completed.stdout


def main() -> int:
    cases = [
        case_materialize_writes_canonical_ascii_state,
        case_write_genesis_round_trip_is_idempotent,
        case_materialize_rolls_back_on_mid_write_failure,
        case_runtime_gating_off_is_byte_equivalent,
        case_runtime_materialization_on_clears_drift_and_warns_on_divergence,
        case_b1_replay_suite_still_passes,
    ]
    failures = []
    for case in cases:
        try:
            case()
        except Exception as exc:  # noqa: BLE001 - compact golden failure reporting
            failures.append({"case": case.__name__, "error": str(exc)})
    if failures:
        print(json.dumps({"status": "FAILED", "failures": failures}, indent=2))
        return 1
    print(f"OK: {len(cases)} runtime protocol materialize golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
