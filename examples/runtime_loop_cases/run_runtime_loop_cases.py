#!/usr/bin/env python3
"""Golden cases for runtime M1 replay loop."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
ORCHESTRATOR = ROOT / "runtime" / "orchestrator.py"


def run(command: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=check)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def task(task_id: str, status: str = "ready") -> dict:
    return {
        "id": task_id,
        "owner": "Codex",
        "status": status,
        "type": "implementation",
        "priority": "normal",
        "phase": "P2",
        "file": f"Area_comun/tasks/{task_id}.md",
        "depends_on": [],
        "deliverables": [],
    }


def claim(task_id: str) -> dict:
    return {
        "claim_id": f"CLAIM-{task_id}-codex",
        "task_id": task_id,
        "owner": "Codex",
        "status": "active",
        "scope": [
            f"Area_comun/tasks/{task_id}.md",
            f"Area_comun/state/TASK_INDEX.json#{task_id}",
            f"Area_comun/state/PROJECT_STATE.json#active_tasks/{task_id}",
        ],
        "started_at": "2026-06-06",
        "updated_at": "2026-06-06",
        "expires_at": "2026-06-07",
        "notes": "runtime loop fixture",
    }


def build_fixture(root: Path, *, enabled: bool = True, task_ids: list[str] | None = None) -> None:
    task_ids = task_ids or ["TASK-9000"]
    tasks = [task(task_id) for task_id in task_ids]
    write_json(
        root / "protocol.config.json",
        {
            "schema_version": "1.0",
            "runtime": {"enabled": enabled, "entrypoint": "runtime/orchestrator.py"},
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
            "active_tasks": [{"id": item["id"], "owner": "Codex", "status": item["status"], "title": "Fixture"} for item in tasks],
        },
    )
    write_json(root / "Area_comun/state/TASK_INDEX.json", {"schema_version": "1.0", "tasks": tasks})
    write_json(root / "Area_comun/state/CLAIMS.json", {"schema_version": "1.0", "claims": [claim(item["id"]) for item in tasks]})
    for item in tasks:
        task_path = root / item["file"]
        task_path.parent.mkdir(parents=True, exist_ok=True)
        task_path.write_text(f"---\nid: {item['id']}\nstatus: {item['status']}\n---\n\n# Fixture\n", encoding="utf-8")
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


def turn_report(task_id: str, *, outcome: str = "done", to_status: str = "done") -> dict:
    return {
        "turn_id": f"RUN-fixture-{task_id}",
        "task_id": task_id,
        "agent": "Codex",
        "outcome": outcome,
        "summary": f"Move {task_id}.",
        "changed_paths": [
            f"Area_comun/tasks/{task_id}.md",
            f"Area_comun/state/TASK_INDEX.json#{task_id}",
            f"Area_comun/state/PROJECT_STATE.json#active_tasks/{task_id}",
        ],
        "transitions": {"task_status": {"from": "ready", "to": to_status}},
        "commit_message": f"test(runtime): replay {task_id}",
        "gate": {"human_required": False},
        "next_hint": None,
    }


def human_report(task_id: str) -> dict:
    report = turn_report(task_id, outcome="human_required", to_status="blocked")
    report["changed_paths"] = []
    report["transitions"] = {}
    report["commit_message"] = f"test(runtime): human gate {task_id}"
    report["gate"] = {"human_required": True, "reason": "fixture human gate"}
    return report


def git_count(root: Path) -> int:
    return int(run(["git", "rev-list", "--count", "HEAD"], root).stdout.strip())


def git_dirty(root: Path) -> str:
    return run(["git", "status", "--short"], root).stdout.strip()


def write_reports(root: Path, reports: list[dict]) -> Path:
    report_dir = root / "replay"
    report_dir.mkdir(parents=True, exist_ok=True)
    for index, report in enumerate(reports, start=1):
        write_json(report_dir / f"{index:02d}-{report['task_id']}.json", report)
    return report_dir


def run_orchestrator(root: Path, args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return run([sys.executable, str(ORCHESTRATOR), "--root", str(root), *args], ROOT, check=check)


def case_once_commits_one_turn() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-loop-once-") as temp:
        fixture = Path(temp)
        build_fixture(fixture)
        report_dir = write_reports(fixture, [turn_report("TASK-9000")])
        before = git_count(fixture)
        completed = run_orchestrator(
            fixture,
            ["--run", "--once", "--run-id", "RUN-fixture-once", "--replay-report", str(report_dir)],
        )
        result = json.loads(completed.stdout)
        assert result["ok"] is True, result
        assert git_count(fixture) == before + 1
        status = json.loads((fixture / "Area_comun/state/TASK_INDEX.json").read_text())["tasks"][0]["status"]
        assert status == "done"
        assert result["run_id"] == "RUN-fixture-once"
        assert (fixture / "runtime/runs/RUN-fixture-once.jsonl").exists()


def case_sequence_max_iter_cuts() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-loop-seq-") as temp:
        fixture = Path(temp)
        build_fixture(fixture, task_ids=["TASK-9000", "TASK-9001"])
        report_dir = write_reports(fixture, [turn_report("TASK-9000"), turn_report("TASK-9001")])
        before = git_count(fixture)
        completed = run_orchestrator(fixture, ["--run", "--max-iter", "1", "--replay-report", str(report_dir)])
        result = json.loads(completed.stdout)
        assert result["ok"] is True, result
        assert len(result["turns"]) == 1
        assert git_count(fixture) == before + 1
        statuses = [item["status"] for item in json.loads((fixture / "Area_comun/state/TASK_INDEX.json").read_text())["tasks"]]
        assert statuses == ["done", "ready"]


def case_human_required_stops_without_commit() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-loop-human-") as temp:
        fixture = Path(temp)
        build_fixture(fixture)
        report_dir = write_reports(fixture, [human_report("TASK-9000"), turn_report("TASK-9000")])
        before = git_count(fixture)
        completed = run_orchestrator(fixture, ["--run", "--replay-report", str(report_dir)])
        result = json.loads(completed.stdout)
        assert result["ok"] is True, result
        assert result["turns"][0]["human_required"] is True
        assert git_count(fixture) == before
        status = json.loads((fixture / "Area_comun/state/TASK_INDEX.json").read_text())["tasks"][0]["status"]
        assert status == "ready"


def case_plan_is_read_only() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-loop-plan-") as temp:
        fixture = Path(temp)
        build_fixture(fixture, enabled=False)
        before_count = git_count(fixture)
        before_dirty = git_dirty(fixture)
        completed = run_orchestrator(fixture, ["--plan"])
        result = json.loads(completed.stdout)
        assert result["dry_run"] is True, result
        assert git_count(fixture) == before_count
        assert git_dirty(fixture) == before_dirty


def case_enabled_false_aborts_run() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-loop-disabled-") as temp:
        fixture = Path(temp)
        build_fixture(fixture, enabled=False)
        report_dir = write_reports(fixture, [turn_report("TASK-9000")])
        before = git_count(fixture)
        completed = run_orchestrator(fixture, ["--run", "--once", "--replay-report", str(report_dir)], check=False)
        result = json.loads(completed.stdout)
        assert completed.returncode == 1
        assert result["ok"] is False
        assert "runtime.enabled is false" in result["reason"]
        assert git_count(fixture) == before


def main() -> int:
    cases = [
        case_once_commits_one_turn,
        case_sequence_max_iter_cuts,
        case_human_required_stops_without_commit,
        case_plan_is_read_only,
        case_enabled_false_aborts_run,
    ]
    failures = []
    for case in cases:
        try:
            case()
        except Exception as exc:
            failures.append({"case": case.__name__, "error": str(exc)})
    if failures:
        print(json.dumps({"status": "FAILED", "failures": failures}, indent=2))
        return 1
    print(f"OK: {len(cases)} runtime loop golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
