#!/usr/bin/env python3
"""Golden cases for supervised-autonomy SA.1 shadow envelope."""

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
    path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8", newline="\n")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def task(task_id: str) -> dict[str, Any]:
    return {
        "id": task_id,
        "owner": "Codex",
        "status": "ready",
        "type": "implementation",
        "priority": "normal",
        "phase": "P2",
        "spec_id": "Area_comun/specs/SPEC-9600-fixture.md",
        "linked_decisions": ["DECISION-0024"],
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
        "started_at": "2026-06-08",
        "updated_at": "2026-06-08",
        "expires_at": "2026-06-09",
        "notes": "supervised autonomy fixture",
    }


def supervised_config(*, enabled: bool, max_turns: int = 2, valid: bool = True) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "enabled": enabled,
        "activation_decision": "DECISION-0024" if valid else "",
        "approved_by": "operador humano" if valid else "",
        "approved_at": "2026-06-08" if valid else "",
        "caps": {"max_turns": max_turns},
    }
    return payload


def build_fixture(
    root: Path,
    *,
    task_ids: list[str],
    supervised: dict[str, Any] | None = None,
) -> None:
    tasks = [task(task_id) for task_id in task_ids]
    runtime_config: dict[str, Any] = {"enabled": True, "entrypoint": "runtime/orchestrator.py"}
    if supervised is not None:
        runtime_config["supervised_autonomy"] = supervised
    write_json(
        root / "protocol.config.json",
        {
            "schema_version": "1.0",
            "runtime": runtime_config,
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
            "active_tasks": [
                {"id": item["id"], "owner": "Codex", "status": item["status"], "title": "Fixture"} for item in tasks
            ],
        },
    )
    write_json(root / "Area_comun/state/TASK_INDEX.json", {"schema_version": "1.0", "tasks": tasks})
    write_json(root / "Area_comun/state/CLAIMS.json", {"schema_version": "1.0", "claims": [claim(item["id"]) for item in tasks]})
    write_json(root / "Area_comun/state/CLAIMS_ARCHIVE.json", {"schema_version": "1.0", "claims": []})
    write_json(root / "Area_comun/state/TASK_INDEX_ARCHIVE.json", {"schema_version": "1.0", "tasks": []})
    for item in tasks:
        task_path = root / item["file"]
        task_path.parent.mkdir(parents=True, exist_ok=True)
        task_path.write_text(f"---\nid: {item['id']}\nstatus: ready\n---\n\n# Fixture\n", encoding="utf-8")
    spec_path = root / "Area_comun/specs/SPEC-9600-fixture.md"
    spec_path.parent.mkdir(parents=True, exist_ok=True)
    spec_path.write_text("# SPEC-9600 fixture\n", encoding="utf-8")
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


def turn_report(task_id: str) -> dict[str, Any]:
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
        "transitions": {
            "task_status": {"from": "ready", "to": "done"},
            "claims": [{"op": "release", "claim_id": f"CLAIM-{task_id}-codex"}],
        },
        "commit_message": f"test(runtime): supervised {task_id}",
        "gate": {"human_required": False},
        "next_hint": None,
        "cost": {"tokens": 3},
    }


def write_transcripts(root: Path, task_ids: list[str]) -> Path:
    path = root / "transcripts"
    path.mkdir(parents=True, exist_ok=True)
    for index, task_id in enumerate(task_ids, start=1):
        report = turn_report(task_id)
        write_json(
            path / f"{index:02d}-{task_id}.json",
            {
                "format": "recorded_invoker.v1",
                "expected_prompt_contains": [task_id, "SPEC-9600 fixture"],
                "report": report,
            },
        )
    return path


def run_orchestrator(root: Path, args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return run([sys.executable, str(ORCHESTRATOR), "--root", str(root), *args], ROOT, check=check)


def git_count(root: Path) -> int:
    return int(run(["git", "rev-list", "--count", "HEAD"], root).stdout.strip())


def statuses(root: Path) -> list[str]:
    return [item["status"] for item in read_json(root / "Area_comun/state/TASK_INDEX.json")["tasks"]]


def case_max_turns_stops_recorded_loop_and_writes_runreport() -> None:
    with tempfile.TemporaryDirectory(prefix="supervised-max-turns-") as temp:
        fixture = Path(temp)
        task_ids = ["TASK-9600", "TASK-9601", "TASK-9602"]
        build_fixture(fixture, task_ids=task_ids, supervised=supervised_config(enabled=True, max_turns=2))
        transcripts = write_transcripts(fixture, task_ids)
        before = git_count(fixture)
        completed = run_orchestrator(
            fixture,
            [
                "--run",
                "--adapter",
                "llm",
                "--llm-invoker",
                "recorded",
                "--allow-supervised-autonomy",
                "--run-id",
                "RUN-supervised-max-turns",
                "--replay-report",
                str(transcripts),
            ],
        )
        result = json.loads(completed.stdout)
        assert result["ok"] is True, result
        assert git_count(fixture) == before + 2
        assert statuses(fixture) == ["done", "done", "ready"]
        assert result["turns"][-1]["outcome"] == "max_turns_reached", result
        assert result["supervised_autonomy"]["caps"]["max_turns"] == 2
        report = Path(result["run_report"])
        assert report.exists(), result
        text = report.read_text(encoding="utf-8-sig")
        assert "max_turns_reached" in text
        assert "caps.max_turns: 2" in text


def case_activation_without_valid_registration_rejects_before_run() -> None:
    with tempfile.TemporaryDirectory(prefix="supervised-invalid-") as temp:
        fixture = Path(temp)
        task_ids = ["TASK-9600"]
        build_fixture(fixture, task_ids=task_ids, supervised=supervised_config(enabled=True, valid=False))
        transcripts = write_transcripts(fixture, task_ids)
        before = git_count(fixture)
        completed = run_orchestrator(
            fixture,
            [
                "--run",
                "--adapter",
                "llm",
                "--llm-invoker",
                "recorded",
                "--allow-supervised-autonomy",
                "--replay-report",
                str(transcripts),
            ],
            check=False,
        )
        result = json.loads(completed.stdout)
        assert completed.returncode == 1
        assert result["ok"] is False
        assert "supervised autonomy requires registered activation" in result["reason"]
        assert git_count(fixture) == before
        assert statuses(fixture) == ["ready"]


def case_flag_absent_keeps_existing_multi_turn_behavior() -> None:
    with tempfile.TemporaryDirectory(prefix="supervised-off-") as temp:
        fixture = Path(temp)
        task_ids = ["TASK-9600", "TASK-9601"]
        build_fixture(fixture, task_ids=task_ids, supervised=supervised_config(enabled=True, max_turns=1))
        transcripts = write_transcripts(fixture, task_ids)
        before = git_count(fixture)
        completed = run_orchestrator(
            fixture,
            [
                "--run",
                "--adapter",
                "llm",
                "--llm-invoker",
                "recorded",
                "--run-id",
                "RUN-supervised-off",
                "--replay-report",
                str(transcripts),
            ],
        )
        result = json.loads(completed.stdout)
        assert result["ok"] is True, result
        assert "run_report" not in result
        assert "supervised_autonomy" not in result
        assert git_count(fixture) == before + 2
        assert statuses(fixture) == ["done", "done"]
        assert not (fixture / "runtime/runs/RUN-supervised-off.runreport.md").exists()


def case_real_invoker_lock_remains_intact_in_sa1() -> None:
    with tempfile.TemporaryDirectory(prefix="supervised-real-lock-") as temp:
        fixture = Path(temp)
        build_fixture(fixture, task_ids=["TASK-9600"], supervised=supervised_config(enabled=True, max_turns=2))
        completed = run_orchestrator(
            fixture,
            [
                "--run",
                "--adapter",
                "llm",
                "--llm-invoker",
                "subprocess",
                "--allow-real-invoker",
                "--allow-supervised-autonomy",
                "--llm-command",
                "python should_not_run.py",
            ],
            check=False,
        )
        result = json.loads(completed.stdout)
        assert completed.returncode == 1
        assert result["ok"] is False
        assert "subprocess llm invoker requires --once" in result["reason"], result


def main() -> int:
    cases = [
        case_max_turns_stops_recorded_loop_and_writes_runreport,
        case_activation_without_valid_registration_rejects_before_run,
        case_flag_absent_keeps_existing_multi_turn_behavior,
        case_real_invoker_lock_remains_intact_in_sa1,
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
    print(f"OK: {len(cases)} supervised autonomy golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
