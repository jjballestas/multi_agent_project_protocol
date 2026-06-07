#!/usr/bin/env python3
"""Golden cases for runtime budget/deadline escalation."""

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
        "started_at": "2026-06-07",
        "updated_at": "2026-06-07",
        "expires_at": "2026-06-08",
        "notes": "runtime budget fixture",
    }


def build_fixture(root: Path, *, budget: dict[str, Any] | None = None, task_ids: list[str] | None = None) -> None:
    task_ids = task_ids or ["TASK-9000"]
    tasks = [task(task_id) for task_id in task_ids]
    config: dict[str, Any] = {
        "schema_version": "1.0",
        "runtime": {"enabled": True, "entrypoint": "runtime/orchestrator.py"},
        "domain_neutrality": {
            "enabled": True,
            "denylist": [],
            "scan_globs": ["Area_comun/tasks/*.md"],
            "exempt_globs": [],
        },
        "state_invariants": [{"path": "status", "equals": "active"}],
    }
    if budget is not None:
        config["budget"] = budget
    write_json(root / "protocol.config.json", config)
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


def turn_report(task_id: str, *, cost: int = 1) -> dict[str, Any]:
    return {
        "turn_id": f"RUN-budget-{task_id}",
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
        "transitions": {
            "task_status": {"from": "ready", "to": "done"},
            "claims": [{"op": "release", "claim_id": f"CLAIM-{task_id}-codex"}],
        },
        "commit_message": f"test(runtime): budget {task_id}",
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


def run_orchestrator(root: Path, args: list[str]) -> dict[str, Any]:
    completed = run([sys.executable, str(ORCHESTRATOR), "--root", str(root), *args], ROOT)
    return json.loads(completed.stdout)


def load_jsonl(path: str | Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8-sig").splitlines() if line.strip()]


def git_count(root: Path) -> int:
    return int(run(["git", "rev-list", "--count", "HEAD"], root).stdout.strip())


def task_status(root: Path, task_id: str = "TASK-9000") -> str:
    tasks = json.loads((root / "Area_comun/state/TASK_INDEX.json").read_text(encoding="utf-8-sig"))["tasks"]
    return next(item["status"] for item in tasks if item["id"] == task_id)


def case_soft_threshold_warns_without_stopping() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-budget-soft-") as temp:
        root = Path(temp)
        build_fixture(root, budget={"enabled": True, "soft_cost_tokens": 5, "hard_cost_tokens": 99})
        report_dir = write_reports(root, [turn_report("TASK-9000", cost=5)])
        result = run_orchestrator(root, ["--run", "--once", "--run-id", "RUN-budget-soft", "--replay-report", str(report_dir)])
        entry = load_jsonl(result["run_log"])[0]
        assert entry["outcome"] == "done", entry
        assert "budget_escalation" not in entry
        assert entry["budget_warning"] == {
            "reason": "soft_cost_tokens",
            "consumed": {"cost_tokens": 5},
            "limit": {"cost_tokens": 5},
            "last_responsible": {"agent": "Codex", "task_id": "TASK-9000"},
        }
        assert task_status(root) == "done"


def case_hard_threshold_escalates_before_apply() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-budget-hard-") as temp:
        root = Path(temp)
        build_fixture(root, budget={"enabled": True, "hard_cost_tokens": 5})
        before = git_count(root)
        report_dir = write_reports(root, [turn_report("TASK-9000", cost=5)])
        result = run_orchestrator(root, ["--run", "--once", "--run-id", "RUN-budget-hard", "--replay-report", str(report_dir)])
        entry = load_jsonl(result["run_log"])[0]
        assert entry["outcome"] == "budget_exhausted", entry
        assert entry["reason"] == "hard_cost_tokens"
        assert entry["budget_escalation"] == {
            "reason": "hard_cost_tokens",
            "consumed": {"cost_tokens": 5},
            "limit": {"cost_tokens": 5},
            "last_responsible": {"agent": "Codex", "task_id": "TASK-9000"},
        }
        assert git_count(root) == before
        assert task_status(root) == "ready"


def case_logical_deadline_escalates_without_wall_clock() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-budget-deadline-") as temp:
        root = Path(temp)
        build_fixture(root, budget={"enabled": True, "task_deadlines": {"TASK-9000": 0}})
        before = git_count(root)
        report_dir = write_reports(root, [turn_report("TASK-9000", cost=1)])
        result = run_orchestrator(root, ["--run", "--once", "--run-id", "RUN-budget-deadline", "--replay-report", str(report_dir)])
        entry = load_jsonl(result["run_log"])[0]
        assert entry["trace"] == ["gate_pre", "route", "budget"], entry
        assert entry["outcome"] == "budget_exhausted"
        assert entry["budget_escalation"] == {
            "reason": "deadline_turn",
            "consumed": {"turn": 1},
            "limit": {"deadline_turn": 0},
            "last_responsible": {"agent": "Codex", "task_id": "TASK-9000"},
        }
        assert git_count(root) == before


def case_queue_limit_escalates_before_turn() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-budget-queue-") as temp:
        root = Path(temp)
        build_fixture(root, budget={"enabled": True, "max_queue_length": 1}, task_ids=["TASK-9000", "TASK-9001"])
        before = git_count(root)
        report_dir = write_reports(root, [turn_report("TASK-9000"), turn_report("TASK-9001")])
        result = run_orchestrator(root, ["--run", "--run-id", "RUN-budget-queue", "--replay-report", str(report_dir)])
        entry = load_jsonl(result["run_log"])[0]
        assert entry["trace"] == ["budget"], entry
        assert entry["outcome"] == "budget_exhausted"
        assert entry["budget_escalation"] == {
            "reason": "max_queue_length",
            "consumed": {"queue_length": 2},
            "limit": {"queue_length": 1},
            "last_responsible": {"agent": "runtime", "task_id": "none"},
        }
        assert git_count(root) == before


def case_budget_disabled_matches_absent_behavior() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-budget-off-") as temp:
        root = Path(temp)
        absent = root / "absent"
        disabled = root / "disabled"
        build_fixture(absent)
        build_fixture(disabled, budget={"enabled": False, "soft_cost_tokens": 1, "hard_cost_tokens": 1, "max_queue_length": 0})
        absent_reports = write_reports(absent, [turn_report("TASK-9000", cost=5)])
        disabled_reports = write_reports(disabled, [turn_report("TASK-9000", cost=5)])
        absent_result = run_orchestrator(absent, ["--run", "--once", "--run-id", "RUN-budget-off", "--replay-report", str(absent_reports)])
        disabled_result = run_orchestrator(disabled, ["--run", "--once", "--run-id", "RUN-budget-off", "--replay-report", str(disabled_reports)])
        absent_entry = load_jsonl(absent_result["run_log"])[0]
        disabled_entry = load_jsonl(disabled_result["run_log"])[0]
        for entry in (absent_entry, disabled_entry):
            assert entry["outcome"] == "done", entry
            assert "budget_warning" not in entry
            assert "budget_escalation" not in entry
        comparable_keys = ["run_id", "turn", "trace", "task_id", "agent", "outcome", "reason", "errors", "changed_paths", "cost"]
        assert {key: absent_entry.get(key) for key in comparable_keys} == {key: disabled_entry.get(key) for key in comparable_keys}


def main() -> int:
    cases = [
        case_soft_threshold_warns_without_stopping,
        case_hard_threshold_escalates_before_apply,
        case_logical_deadline_escalates_without_wall_clock,
        case_queue_limit_escalates_before_turn,
        case_budget_disabled_matches_absent_behavior,
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
    print(f"OK: {len(cases)} runtime budget golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
