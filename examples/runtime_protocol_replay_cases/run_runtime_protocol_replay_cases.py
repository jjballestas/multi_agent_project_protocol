#!/usr/bin/env python3
"""Golden cases for protocol state replay/materialization B.1."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from runtime.eventlog import rebuild_snapshot  # noqa: E402
from runtime.protocol_replay import (  # noqa: E402
    _drift_exit_code,
    build_genesis_snapshot,
    materialize_protocol_state,
    protocol_state_drift,
    replay_protocol_state,
)
from runtime.temp_paths import root_temp_dir  # noqa: E402


TASK_ID = "TASK-9000"

FALSIFICATION_CONTRACTS = (
    {
        "id": "protocol-replay-drift-exit",
        "negative": "a drifted hot state must make the CLI gate red",
        "mutation": "inverted = lambda value",
        "boundaries": ("assert dirty.returncode != 0", "assert inverted({\"has_drift\": True}) == 0"),
        "exercised_by": "case_cli_is_a_real_aborting_gate",
    },
    {
        "id": "protocol-replay-unknown-flag",
        "negative": "an unknown CLI flag must be rejected",
        "mutation": "isolated_unknown = run(command + [\"--bogus-flag\"]",
        "boundaries": ("assert isolated_unknown.returncode != 0",),
        "exercised_by": "case_cli_is_a_real_aborting_gate",
    },
)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


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
        "actor_auth": {"method": "not_enforced_phase2"},
        "idempotency_key": f"fixture:{seq}",
        "fencing_token": seq,
        "payload": payload,
        "applied": True,
        "ts": "2026-06-07T00:00:00Z",
    }


def run(command: list[str], cwd: Path = ROOT, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=check)


def hot_docs(status: str = "ready") -> dict[str, Any]:
    claim_status = "released" if status in {"in_review", "done"} else "active"
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
                    "scope": ["Area_comun/state/CLAIMS.json"],
                }
            ],
        },
    }


def build_fixture(root: Path, *, event_state_enabled: bool, hot_status: str = "ready") -> None:
    write_json(
        root / "protocol.config.json",
        {
            "schema_version": "1.0",
            "event_auth": {"enabled": False},
            "event_state": {"enabled": event_state_enabled},
            "domain_neutrality": {"enabled": True, "denylist": [], "scan_globs": [], "exempt_globs": []},
            "state_invariants": [{"path": "status", "equals": "active"}],
        },
    )
    docs = hot_docs(hot_status)
    write_json(root / "Area_comun/state/TASK_INDEX.json", docs["task_index"])
    write_json(root / "Area_comun/state/PROJECT_STATE.json", docs["project_state"])
    write_json(root / "Area_comun/state/CLAIMS.json", docs["claims"])
    write_json(root / "Area_comun/state/TASK_INDEX_ARCHIVE.json", {"schema_version": "1.0", "tasks": []})
    write_json(root / "Area_comun/state/CLAIMS_ARCHIVE.json", {"schema_version": "1.0", "claims": []})
    write(root / "Area_comun/tasks" / f"{TASK_ID}.md", f"---\nid: {TASK_ID}\nstatus: {hot_status}\n---\n")
    write(root / "Area_comun/reports/HUMAN_REPORT_TEMPLATE.md", "# Human report\n")
    for folder in ("open", "answered", "archived"):
        write(root / "Area_comun/mailbox" / folder / ".gitkeep", "\n")
    seed_events(root, [event(1, "protocol.genesis", {"state": hot_docs("ready")})])


def seed_events(root: Path, events: list[dict[str, Any]]) -> None:
    log_path = root / "runtime/state/events.jsonl"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    log_path.write_text(
        "".join(json.dumps(item, sort_keys=True, separators=(",", ":")) + "\n" for item in events),
        encoding="utf-8",
    )
    write_json(root / "runtime/state/snapshot.json", rebuild_snapshot(root))


def case_replay_sequence_materializes_protocol_state() -> None:
    events = [
        event(3, "decision.accepted", {"decision_id": "DECISION-0002"}),
        event(1, "protocol.genesis", {"state": hot_docs("ready")}),
        event(2, "task.status_changed", {"task_id": TASK_ID, "to": "in_progress"}, aggregate_id=TASK_ID),
        event(4, "claim.released", {"claim_id": f"CLAIM-{TASK_ID}-codex"}),
    ]
    materialized = materialize_protocol_state(replay_protocol_state(events))
    task = materialized["Area_comun/state/TASK_INDEX.json"]["tasks"][0]
    active = materialized["Area_comun/state/PROJECT_STATE.json"]["active_tasks"][0]
    claim = materialized["Area_comun/state/CLAIMS.json"]["claims"][0]
    assert task["status"] == "in_progress", task
    assert active["status"] == "in_progress", active
    assert claim["status"] == "released", claim
    assert "DECISION-0002" in materialized["Area_comun/state/PROJECT_STATE.json"]["decisions"]


def case_materialize_is_idempotent_and_canonical() -> None:
    events = [
        event(2, "task.upserted", {"task": {"id": "TASK-9002", "status": "ready"}}, aggregate_id="TASK-9002"),
        event(1, "task.upserted", {"task": {"id": "TASK-9001", "status": "done"}}, aggregate_id="TASK-9001"),
    ]
    first = materialize_protocol_state(replay_protocol_state(events))
    second = materialize_protocol_state(replay_protocol_state(list(reversed(events))))
    assert first == second
    ids = [task["id"] for task in first["Area_comun/state/TASK_INDEX.json"]["tasks"]]
    assert ids == ["TASK-9001", "TASK-9002"], ids


def case_genesis_round_trip_matches_hot_state() -> None:
    with root_temp_dir(ROOT, ".protocol-replay-genesis-") as root:
        build_fixture(root, event_state_enabled=False, hot_status="ready")
        genesis = build_genesis_snapshot(root)
        replayed = replay_protocol_state([event(1, "protocol.genesis", {"state": genesis["state"]})])
        assert materialize_protocol_state(replayed) == materialize_protocol_state(genesis)


def case_drift_detected_and_absent() -> None:
    with root_temp_dir(ROOT, ".protocol-replay-drift-") as root:
        build_fixture(root, event_state_enabled=True, hot_status="ready")
        assert protocol_state_drift(root)["has_drift"] is False
        write_json(root / "Area_comun/state/TASK_INDEX.json", hot_docs("done")["task_index"])
        drift = protocol_state_drift(root)
        assert drift["has_drift"] is True, drift
        assert any(entry["path"] == "Area_comun/state/TASK_INDEX.json" for entry in drift["entries"])


def case_cli_is_a_real_aborting_gate() -> None:
    with root_temp_dir(ROOT, ".protocol-replay-cli-") as root:
        build_fixture(root, event_state_enabled=True, hot_status="ready")
        command = [sys.executable, str(ROOT / "runtime/protocol_replay.py"), "--check-drift", "--root", str(root)]
        clean = run(command, check=False)
        assert clean.returncode == 0, clean.stdout + clean.stderr
        assert "verdict=CLEAN" in clean.stdout and "up_to_seq=1" in clean.stdout, clean.stdout

        isolated_unknown = run(command + ["--bogus-flag"], check=False)
        assert isolated_unknown.returncode != 0, isolated_unknown.stdout + isolated_unknown.stderr

        write_json(root / "Area_comun/state/TASK_INDEX.json", hot_docs("done")["task_index"])
        dirty = run(command, check=False)
        assert dirty.returncode != 0, dirty.stdout + dirty.stderr
        assert "verdict=DRIFT" in dirty.stdout and "up_to_seq=1" in dirty.stdout, dirty.stdout

        unknown = run([sys.executable, str(ROOT / "runtime/protocol_replay.py"), "--bogus-flag"], check=False)
        assert unknown.returncode != 0, unknown.stdout + unknown.stderr

        # Mutation control: an inverted verdict is killed by both branch assertions.
        assert _drift_exit_code({"has_drift": False}) == 0
        assert _drift_exit_code({"has_drift": True}) != 0
        inverted = lambda value: 0 if value.get("has_drift") is not False else 1
        assert inverted({"has_drift": False}) != 0
        assert inverted({"has_drift": True}) == 0


def case_pruned_archive_loss_is_drift() -> None:
    with root_temp_dir(ROOT, ".protocol-replay-archive-drift-") as root:
        build_fixture(root, event_state_enabled=True, hot_status="ready")
        events = [
            event(1, "protocol.genesis", {"state": hot_docs("done")}),
            event(2, "intent.applied", {"transitions": {"protocol_prune": {"task_ids": [TASK_ID]}}}),
        ]
        seed_events(root, events)
        write_json(root / "Area_comun/state/TASK_INDEX.json", {"schema_version": "1.0", "tasks": []})
        drift = protocol_state_drift(root)
        assert any(entry["path"] == "Area_comun/state/TASK_INDEX_ARCHIVE.json" for entry in drift["entries"]), drift
        write_json(root / "Area_comun/state/TASK_INDEX_ARCHIVE.json", hot_docs("done")["task_index"])
        repaired = protocol_state_drift(root)
        assert not any(entry["path"] == "Area_comun/state/TASK_INDEX_ARCHIVE.json" for entry in repaired["entries"]), repaired


def case_validator_cross_checks_task_files_and_rows() -> None:
    with root_temp_dir(ROOT, ".protocol-replay-task-cross-") as root:
        build_fixture(root, event_state_enabled=False, hot_status="ready")
        orphan = root / "Area_comun/tasks/TASK-9998.md"
        write(orphan, "---\nid: TASK-9998\nstatus: ready\n---\n")
        result = run([sys.executable, str(ROOT / "scripts/validate_collaboration_state.py"), "--root", str(root)], check=False)
        assert result.returncode == 1 and "Task file has no hot or archived index row" in result.stdout, result.stdout
        orphan.unlink()
        docs = hot_docs("ready")
        docs["task_index"]["tasks"][0]["file"] = "Area_comun/tasks/TASK-missing.md"
        write_json(root / "Area_comun/state/TASK_INDEX.json", docs["task_index"])
        result = run([sys.executable, str(ROOT / "scripts/validate_collaboration_state.py"), "--root", str(root)], check=False)
        assert result.returncode == 1 and "references missing task file" in result.stdout, result.stdout


def validator_stdout(root: Path, *, powershell: bool = False) -> str:
    if powershell:
        shell = shutil.which("pwsh") or shutil.which("powershell")
        if not shell:
            return ""
        result = run(
            [
                shell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(ROOT / "scripts/validate_collaboration_state.ps1"),
                "-Root",
                str(root),
            ]
        )
        return result.stdout
    result = run([sys.executable, str(ROOT / "scripts/validate_collaboration_state.py"), "--root", str(root)])
    return result.stdout


def case_validator_gate_off_is_silent_and_gate_on_warns() -> None:
    with root_temp_dir(ROOT, ".protocol-replay-validator-") as root:
        build_fixture(root, event_state_enabled=False, hot_status="done")
        stdout = validator_stdout(root)
        assert "Runtime protocol state drift" not in stdout, stdout
        write_json(root / "protocol.config.json", {**json.loads((root / "protocol.config.json").read_text()), "event_state": {"enabled": True}})
        stdout_on = validator_stdout(root)
        assert "Runtime protocol state drift detected" in stdout_on, stdout_on
        ps_stdout = validator_stdout(root, powershell=True)
        if ps_stdout:
            assert "Runtime protocol state drift detected" in ps_stdout, ps_stdout


def case_replay_has_no_side_effects() -> None:
    with root_temp_dir(ROOT, ".protocol-replay-negative-") as root:
        build_fixture(root, event_state_enabled=True, hot_status="ready")
        before = {
            path.relative_to(root).as_posix(): path.read_text(encoding="utf-8-sig")
            for path in sorted(root.rglob("*"))
            if path.is_file()
        }

        def forbidden() -> None:
            raise AssertionError("replay invoked an external effect")

        replay_protocol_state([event(1, "protocol.genesis", {"state": hot_docs("ready")})], forbidden_callback=forbidden)
        after = {
            path.relative_to(root).as_posix(): path.read_text(encoding="utf-8-sig")
            for path in sorted(root.rglob("*"))
            if path.is_file()
        }
        assert before == after


def main() -> int:
    cases = [
        case_replay_sequence_materializes_protocol_state,
        case_materialize_is_idempotent_and_canonical,
        case_genesis_round_trip_matches_hot_state,
        case_drift_detected_and_absent,
        case_cli_is_a_real_aborting_gate,
        case_pruned_archive_loss_is_drift,
        case_validator_cross_checks_task_files_and_rows,
        case_validator_gate_off_is_silent_and_gate_on_warns,
        case_replay_has_no_side_effects,
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
    print(f"OK: {len(cases)} runtime protocol replay golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
