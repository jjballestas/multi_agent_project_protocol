#!/usr/bin/env python3
"""Golden cases for the runtime event-log gate wiring."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ORCHESTRATOR = ROOT / "runtime" / "orchestrator.py"
sys.path.insert(0, str(ROOT))

from runtime.apply import apply_gate_and_commit  # noqa: E402
from runtime.eventlog import EventWriter, assert_snapshot_matches, read_jsonl_torn_safe  # noqa: E402


TASK_ID = "TASK-9100"


def run(command: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=check)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def build_fixture(root: Path) -> None:
    write_json(
        root / "protocol.config.json",
        {
            "schema_version": "1.0",
            "runtime": {"enabled": True, "entrypoint": "runtime/orchestrator.py"},
            "domain_neutrality": {
                "enabled": True,
                "denylist": [],
                "scan_globs": ["Area_comun/tasks/*.md"],
                "exempt_globs": [],
            },
            "state_invariants": [{"path": "status", "equals": "active"}],
        },
    )
    write_json(
        root / "Area_comun/state/PROJECT_STATE.json",
        {
            "status": "active",
            "active_tasks": [{"id": TASK_ID, "owner": "Codex", "status": "ready", "title": "Fixture"}],
        },
    )
    write_json(
        root / "Area_comun/state/TASK_INDEX.json",
        {
            "schema_version": "1.0",
            "tasks": [
                {
                    "id": TASK_ID,
                    "owner": "Codex",
                    "status": "ready",
                    "type": "implementation",
                    "priority": "normal",
                    "phase": "P2",
                    "file": f"Area_comun/tasks/{TASK_ID}.md",
                    "depends_on": [],
                    "deliverables": [],
                }
            ],
        },
    )
    write_json(
        root / "Area_comun/state/CLAIMS.json",
        {
            "schema_version": "1.0",
            "claims": [
                {
                    "claim_id": f"CLAIM-{TASK_ID}-codex",
                    "task_id": TASK_ID,
                    "owner": "Codex",
                    "status": "active",
                    "scope": [
                        f"Area_comun/tasks/{TASK_ID}.md",
                        f"Area_comun/state/TASK_INDEX.json#{TASK_ID}",
                        f"Area_comun/state/PROJECT_STATE.json#active_tasks/{TASK_ID}",
                        "Area_comun/state/CLAIMS.json",
                    ],
                    "started_at": "2026-06-06",
                    "updated_at": "2026-06-06",
                    "expires_at": "2026-06-07",
                    "notes": "eventlog gate fixture",
                }
            ],
        },
    )
    task_path = root / "Area_comun/tasks" / f"{TASK_ID}.md"
    task_path.parent.mkdir(parents=True, exist_ok=True)
    task_path.write_text(f"---\nid: {TASK_ID}\nstatus: ready\n---\n\n# Fixture\n", encoding="utf-8")
    for folder in ("open", "answered", "archived"):
        (root / "Area_comun/mailbox" / folder).mkdir(parents=True, exist_ok=True)
    reports = root / "Area_comun/reports"
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "HUMAN_REPORT_TEMPLATE.md").write_text("# Human report\n", encoding="utf-8")
    schema_target = root / "runtime/turn_schema.json"
    schema_target.parent.mkdir(parents=True, exist_ok=True)
    schema_target.write_text((ROOT / "runtime/turn_schema.json").read_text(encoding="utf-8-sig"), encoding="utf-8")
    run(["git", "init"], root)
    run(["git", "config", "user.email", "runtime@example.invalid"], root)
    run(["git", "config", "user.name", "Runtime Test"], root)
    run(["git", "add", "."], root)
    run(["git", "commit", "-m", "fixture baseline"], root)


def turn_report() -> dict[str, Any]:
    return {
        "turn_id": "RUN-eventlog-gate-0001",
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
        "obstacles": [],
        "transitions": {
            "task_status": {"from": "ready", "to": "done"},
            "claims": [{"op": "release", "claim_id": f"CLAIM-{TASK_ID}-codex"}],
        },
        "commit_message": "test(runtime): eventlog gate fixture",
        "gate": {"human_required": False},
        "next_hint": None,
    }


def git_count(root: Path) -> int:
    return int(run(["git", "rev-list", "--count", "HEAD"], root).stdout.strip())


def git_dirty(root: Path) -> str:
    return run(["git", "status", "--short"], root).stdout.strip()


def task_status(root: Path) -> str:
    return json.loads((root / "Area_comun/state/TASK_INDEX.json").read_text(encoding="utf-8-sig"))["tasks"][0]["status"]


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def write_reports(root: Path, reports: list[dict[str, Any]]) -> Path:
    report_dir = root / "replay"
    report_dir.mkdir(parents=True, exist_ok=True)
    for index, report in enumerate(reports, start=1):
        write_json(report_dir / f"{index:02d}-{report['task_id']}.json", report)
    return report_dir


def seed_mismatched_snapshot(root: Path) -> None:
    writer = EventWriter(root)
    writer.acquire_claim(
        task_id=TASK_ID,
        owner="Codex",
        lease_until="2026-06-07",
        idempotency_key=f"Codex:{TASK_ID}:claim:seed:0",
    )
    snapshot = writer.write_snapshot()
    snapshot["state"]["aggregate_versions"][TASK_ID] = 999
    (root / "runtime/state/snapshot.json").write_text(json.dumps(snapshot, indent=2), encoding="utf-8")


def case_apply_commits_eventlog_and_snapshot() -> None:
    with tempfile.TemporaryDirectory(prefix="eventlog-gate-commit-") as temp:
        fixture = Path(temp)
        build_fixture(fixture)
        before = git_count(fixture)
        result = apply_gate_and_commit(turn_report(), fixture)
        assert result["green"] is True, result
        assert git_count(fixture) == before + 1
        assert git_dirty(fixture) == ""
        assert_snapshot_matches(fixture)
        events = read_jsonl_torn_safe(fixture / "runtime/state/events.jsonl")
        assert [event["type"] for event in events] == ["claim.acquired", "intent.applied"]
        snapshot = json.loads((fixture / "runtime/state/snapshot.json").read_text(encoding="utf-8-sig"))
        assert snapshot["up_to_seq"] == 2
        tracked = run(["git", "ls-files", "runtime/state"], fixture).stdout
        assert "runtime/state/events.jsonl" in tracked
        assert "runtime/state/snapshot.json" in tracked


def case_orchestrator_run_logs_eventlog_events() -> None:
    with tempfile.TemporaryDirectory(prefix="eventlog-gate-orchestrator-") as temp:
        fixture = Path(temp)
        build_fixture(fixture)
        report_dir = write_reports(fixture, [turn_report()])
        completed = run(
            [
                sys.executable,
                str(ORCHESTRATOR),
                "--root",
                str(fixture),
                "--run",
                "--once",
                "--run-id",
                "RUN-eventlog-gate",
                "--replay-report",
                str(report_dir),
            ],
            ROOT,
        )
        result = json.loads(completed.stdout)
        assert result["ok"] is True, result
        entry = load_jsonl(fixture / "runtime/runs/RUN-eventlog-gate.jsonl")[0]
        assert entry["eventlog_events"] == [
            {"aggregate_id": TASK_ID, "seq": 1, "type": "claim.acquired"},
            {"aggregate_id": TASK_ID, "seq": 2, "type": "intent.applied"},
        ]
        assert_snapshot_matches(fixture)


def case_snapshot_mismatch_blocks_without_commit() -> None:
    with tempfile.TemporaryDirectory(prefix="eventlog-gate-mismatch-") as temp:
        fixture = Path(temp)
        build_fixture(fixture)
        seed_mismatched_snapshot(fixture)
        run(["git", "add", "runtime/state"], fixture)
        run(["git", "commit", "-m", "fixture mismatched eventlog"], fixture)
        before = git_count(fixture)
        result = apply_gate_and_commit(turn_report(), fixture)
        assert result["green"] is False, result
        assert "snapshot mismatch" in result["error"]
        assert git_count(fixture) == before
        assert task_status(fixture) == "blocked"
        dirty = git_dirty(fixture)
        assert "runtime/state" not in dirty
        events = read_jsonl_torn_safe(fixture / "runtime/state/events.jsonl")
        assert [event["type"] for event in events] == ["claim.acquired"]


def case_global_validator_fallback_without_runtime_state() -> None:
    with tempfile.TemporaryDirectory(prefix="eventlog-gate-fallback-") as temp:
        fixture = Path(temp)
        build_fixture(fixture)
        py = run([sys.executable, str(ROOT / "scripts/validate_collaboration_state.py"), "--root", str(fixture)], ROOT)
        ps = run(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(ROOT / "scripts/validate_collaboration_state.ps1"),
                "-Root",
                str(fixture),
            ],
            ROOT,
        )
        assert "OK: collaboration state is valid." in py.stdout
        assert "OK: collaboration state is valid." in ps.stdout


def case_global_validator_detects_runtime_state_mismatch() -> None:
    with tempfile.TemporaryDirectory(prefix="eventlog-gate-validator-") as temp:
        fixture = Path(temp)
        build_fixture(fixture)
        seed_mismatched_snapshot(fixture)
        py = run([sys.executable, str(ROOT / "scripts/validate_collaboration_state.py"), "--root", str(fixture)], ROOT, check=False)
        ps = run(
            [
                "powershell",
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(ROOT / "scripts/validate_collaboration_state.ps1"),
                "-Root",
                str(fixture),
            ],
            ROOT,
            check=False,
        )
        assert py.returncode == 1, py.stdout
        assert ps.returncode == 1, ps.stdout
        assert "Runtime event log snapshot mismatch" in py.stdout
        assert "Runtime event log snapshot mismatch" in ps.stdout


def main() -> int:
    cases = [
        case_apply_commits_eventlog_and_snapshot,
        case_orchestrator_run_logs_eventlog_events,
        case_snapshot_mismatch_blocks_without_commit,
        case_global_validator_fallback_without_runtime_state,
        case_global_validator_detects_runtime_state_mismatch,
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
    print(f"OK: {len(cases)} runtime event log gate golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
