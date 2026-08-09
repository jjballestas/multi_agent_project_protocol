#!/usr/bin/env python3
"""Golden cases for runtime M2 observability."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
ORCHESTRATOR = ROOT / "runtime" / "orchestrator.py"


def run(command: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=check)


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def task(task_id: str) -> dict[str, Any]:
    return {
        "id": task_id,
        "owner": "Codex",
        "status": "ready",
        "type": "implementation",
        "priority": "normal",
        "phase": "P2",
        "file": f"Area_comun/tasks/{task_id}.md",
        "depends_on": [],
        "deliverables": [],
    }


def claim(task_id: str) -> dict[str, Any]:
    return {
        "claim_id": f"CLAIM-{task_id}-codex",
        "task_id": task_id,
        "owner": "Codex",
        "status": "active",
        "scope": [
            f"Area_comun/tasks/{task_id}.md",
            f"Area_comun/state/TASK_INDEX.json#{task_id}",
            f"Area_comun/state/PROJECT_STATE.json#active_tasks/{task_id}",
            "Area_comun/state/CLAIMS.json",
        ],
        "started_at": "2026-06-06",
        "updated_at": "2026-06-06",
        "expires_at": "2026-06-07",
        "notes": "runtime observability fixture",
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
            "active_tasks": [{"id": item["id"], "owner": "Codex", "status": "ready", "title": "Fixture"} for item in tasks],
        },
    )
    write_json(root / "Area_comun/state/TASK_INDEX.json", {"schema_version": "1.0", "tasks": tasks})
    write_json(root / "Area_comun/state/CLAIMS.json", {"schema_version": "1.0", "claims": [claim(item["id"]) for item in tasks]})
    for item in tasks:
        path = root / item["file"]
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"---\nid: {item['id']}\nstatus: ready\n---\n\n# Fixture\n", encoding="utf-8")
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


def turn_report(task_id: str, cost: int = 3) -> dict[str, Any]:
    return {
        "turn_id": f"RUN-fixture-{task_id}",
        "task_id": task_id,
        "agent": "Codex",
        "outcome": "done",
        "summary": f"Move {task_id}.",
        "changed_paths": [
            f"Area_comun/tasks/{task_id}.md",
            f"Area_comun/state/TASK_INDEX.json#{task_id}",
            f"Area_comun/state/PROJECT_STATE.json#active_tasks/{task_id}",
            "Area_comun/state/CLAIMS.json",
        ],
        "obstacles": [],
        "transitions": {
            "task_status": {"from": "ready", "to": "done"},
            "claims": [{"op": "release", "claim_id": f"CLAIM-{task_id}-codex"}],
        },
        "commit_message": f"test(runtime): observe {task_id}",
        "gate": {"human_required": False},
        "next_hint": None,
        "cost": {"tokens": cost},
    }


def write_reports(root: Path, reports: list[dict[str, Any]]) -> Path:
    report_dir = root / "replay"
    report_dir.mkdir(parents=True, exist_ok=True)
    for index, report in enumerate(reports, start=1):
        write_json(report_dir / f"{index:02d}-{report['task_id']}.json", report)
    return report_dir


def run_orchestrator(root: Path, args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return run([sys.executable, str(ORCHESTRATOR), "--root", str(root), *args], ROOT, check=check)


def load_json(path: str | Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8-sig"))


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def case_enriched_log_and_summary() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-observe-enriched-") as temp:
        fixture = Path(temp)
        build_fixture(fixture)
        report_dir = write_reports(fixture, [turn_report("TASK-9000", cost=7)])
        completed = run_orchestrator(
            fixture,
            ["--run", "--once", "--run-id", "RUN-observe-one", "--clock-fixed", "42", "--replay-report", str(report_dir)],
        )
        result = json.loads(completed.stdout)
        entry = load_jsonl(result["run_log"])[0]
        assert entry["trace"] == ["gate_pre", "route", "claim", "adapter", "validate", "human_gate", "apply", "gate_post", "commit"]
        assert entry["changed_paths"] == turn_report("TASK-9000")["changed_paths"]
        assert entry["cost"] == {"tokens": 7}
        assert entry["duration_ms"] == 42
        assert entry["collision_avoided"] == 0
        summary = load_json(result["summary"])
        assert summary == {
            "run_id": "RUN-observe-one",
            "turns_total": 1,
            "turns_per_task": {"TASK-9000": 1},
            "gates_green_pct": 100.0,
            "reverts": 0,
            "collisions_avoided": 0,
            "cost_total": 7,
            "cost_per_task": {"TASK-9000": 7},
            "duration_ms_total": 42,
        }


def case_budget_exhausted() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-observe-budget-") as temp:
        fixture = Path(temp)
        build_fixture(fixture, task_ids=["TASK-9000", "TASK-9001"])
        report_dir = write_reports(fixture, [turn_report("TASK-9000", cost=5), turn_report("TASK-9001", cost=5)])
        completed = run_orchestrator(
            fixture,
            ["--run", "--run-id", "RUN-observe-budget", "--budget-tokens", "5", "--replay-report", str(report_dir)],
        )
        result = json.loads(completed.stdout)
        entries = load_jsonl(result["run_log"])
        assert [entry["outcome"] for entry in entries] == ["done", "budget_exhausted"]
        assert load_json(result["summary"])["cost_total"] == 5


def case_max_iter_cuts() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-observe-max-") as temp:
        fixture = Path(temp)
        build_fixture(fixture, task_ids=["TASK-9000", "TASK-9001"])
        report_dir = write_reports(fixture, [turn_report("TASK-9000"), turn_report("TASK-9001")])
        completed = run_orchestrator(fixture, ["--run", "--max-iter", "1", "--replay-report", str(report_dir)])
        result = json.loads(completed.stdout)
        assert load_json(result["summary"])["turns_total"] == 1


def case_plan_is_read_only() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-observe-plan-") as temp:
        fixture = Path(temp)
        build_fixture(fixture, enabled=False)
        before = run(["git", "status", "--short"], fixture).stdout
        completed = run_orchestrator(fixture, ["--plan"])
        assert json.loads(completed.stdout)["dry_run"] is True
        assert run(["git", "status", "--short"], fixture).stdout == before


def case_enabled_false_aborts_run() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-observe-disabled-") as temp:
        fixture = Path(temp)
        build_fixture(fixture, enabled=False)
        report_dir = write_reports(fixture, [turn_report("TASK-9000")])
        completed = run_orchestrator(fixture, ["--run", "--once", "--replay-report", str(report_dir)], check=False)
        result = json.loads(completed.stdout)
        assert completed.returncode == 1
        assert result["ok"] is False
        assert "runtime.enabled is false" in result["reason"]


def main() -> int:
    cases = [
        case_enriched_log_and_summary,
        case_budget_exhausted,
        case_max_iter_cuts,
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
    print(f"OK: {len(cases)} runtime observability golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
