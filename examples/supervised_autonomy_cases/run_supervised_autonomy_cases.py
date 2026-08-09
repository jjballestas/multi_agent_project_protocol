#!/usr/bin/env python3
"""Golden cases for supervised-autonomy shadow envelope."""

from __future__ import annotations

import json
import os
import shlex
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


def task(task_id: str, *, status: str = "ready", owner: str = "Codex", overrides: dict[str, Any] | None = None) -> dict[str, Any]:
    payload = {
        "id": task_id,
        "owner": owner,
        "status": status,
        "type": "implementation",
        "priority": "normal",
        "phase": "P2",
        "spec_id": "Area_comun/specs/SPEC-9600-fixture.md",
        "linked_decisions": ["DECISION-0024"],
        "file": f"Area_comun/tasks/{task_id}.md",
        "depends_on": [],
        "deliverables": [],
    }
    payload.update(overrides or {})
    return payload


def claim_id_for(task_id: str, owner: str) -> str:
    return f"CLAIM-{task_id}-{owner.lower().replace(' ', '-')}"


def claim(task_id: str, *, owner: str = "Codex") -> dict[str, Any]:
    return {
        "claim_id": claim_id_for(task_id, owner),
        "task_id": task_id,
        "owner": owner,
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


def supervised_config(
    *,
    enabled: bool,
    max_turns: int = 2,
    wall_clock_ms: int = 1000,
    human_checkpoint_every_k: int = 2,
    valid: bool = True,
) -> dict[str, Any]:
    payload: dict[str, Any] = {
        "enabled": enabled,
        "activation_decision": "DECISION-0024" if valid else "",
        "approved_by": "operador humano" if valid else "",
        "approved_at": "2026-06-08" if valid else "",
        "caps": {
            "max_turns": max_turns,
            "wall_clock_ms": wall_clock_ms,
            "human_checkpoint_every_k": human_checkpoint_every_k,
        },
    }
    return payload


def real_invoker_config(*, enabled: bool = True, valid: bool = True) -> dict[str, Any]:
    return {
        "enabled": enabled,
        "activation_decision": "DECISION-0021" if valid else "",
        "approved_by": "operador humano" if valid else "",
        "approved_at": "2026-06-08" if valid else "",
    }


def build_fixture(
    root: Path,
    *,
    task_ids: list[str],
    supervised: dict[str, Any] | None = None,
    real_invoker: dict[str, Any] | None = None,
    task_statuses: dict[str, str] | None = None,
    task_owners: dict[str, str] | None = None,
    task_overrides: dict[str, dict[str, Any]] | None = None,
    claim_owners: dict[str, str] | None = None,
    quality_policy: dict[str, Any] | None = None,
) -> None:
    task_statuses = task_statuses or {}
    task_owners = task_owners or {}
    task_overrides = task_overrides or {}
    claim_owners = claim_owners or {}
    tasks = [
        task(
            task_id,
            status=task_statuses.get(task_id, "ready"),
            owner=task_owners.get(task_id, "Codex"),
            overrides=task_overrides.get(task_id),
        )
        for task_id in task_ids
    ]
    runtime_config: dict[str, Any] = {"enabled": True, "entrypoint": "runtime/orchestrator.py"}
    if supervised is not None:
        runtime_config["supervised_autonomy"] = supervised
    if real_invoker is not None:
        runtime_config["real_invoker"] = real_invoker
    config_payload = {
        "schema_version": "1.0",
        "runtime": runtime_config,
        "domain_neutrality": {
            "enabled": True,
            "denylist": [],
            "scan_globs": ["Area_comun/tasks/*.md"],
            "exempt_globs": [],
        },
        "state_invariants": [{"path": "status", "equals": "active"}],
    }
    if quality_policy is not None:
        config_payload["quality_policy"] = quality_policy
    write_json(root / "protocol.config.json", config_payload)
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
    write_json(
        root / "Area_comun/state/CLAIMS.json",
        {
            "schema_version": "1.0",
            "claims": [claim(item["id"], owner=claim_owners.get(item["id"], item["owner"])) for item in tasks],
        },
    )
    write_json(root / "Area_comun/state/CLAIMS_ARCHIVE.json", {"schema_version": "1.0", "claims": []})
    write_json(root / "Area_comun/state/TASK_INDEX_ARCHIVE.json", {"schema_version": "1.0", "tasks": []})
    for item in tasks:
        task_path = root / item["file"]
        task_path.parent.mkdir(parents=True, exist_ok=True)
        task_path.write_text(f"---\nid: {item['id']}\nstatus: {item['status']}\n---\n\n# Fixture\n", encoding="utf-8")
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
        "obstacles": [],
        "transitions": {
            "task_status": {"from": "ready", "to": "done"},
            "claims": [{"op": "release", "claim_id": claim_id_for(task_id, "Codex")}],
        },
        "commit_message": f"test(runtime): supervised {task_id}",
        "gate": {"human_required": False},
        "next_hint": None,
        "cost": {"tokens": 3},
    }


def failed_check() -> dict[str, str]:
    return {
        "check_id": "review-cycle",
        "error_class": "ReviewFinding",
        "artifact_path": "Area_comun/reports/review-cycle.txt",
        "log": "ts=2026-06-08 id=abc123",
    }


def review_rejection_report(task_id: str) -> dict[str, Any]:
    return {
        "turn_id": f"RUN-fixture-review-{task_id}",
        "task_id": task_id,
        "agent": "Claude",
        "outcome": "ok",
        "summary": f"Reject {task_id} in review.",
        "changed_paths": [
            f"Area_comun/tasks/{task_id}.md",
            f"Area_comun/state/TASK_INDEX.json#{task_id}",
            f"Area_comun/state/PROJECT_STATE.json#active_tasks/{task_id}",
            "Area_comun/state/CLAIMS.json",
        ],
        "obstacles": [
            {
                "what": "The fixture review was rejected.",
                "root_cause": "The deliberate review-cycle check failed.",
                "resolution": "Return the fixture task for remediation.",
                "recurrence_risk": "low",
            }
        ],
        "transitions": {
            "task_status": {"from": "in_review", "to": "changes_requested"},
            "review_qa": {"event": "reject_review", "reviewer": "Claude", "checks_failed": [failed_check()]},
            "claims": [{"op": "release", "claim_id": claim_id_for(task_id, "Claude")}],
        },
        "commit_message": f"test(runtime): supervised review {task_id}",
        "gate": {"human_required": False},
        "next_hint": None,
        "cost": {"tokens": 5},
    }


def write_transcripts(root: Path, task_ids: list[str]) -> Path:
    return write_report_transcripts(root, [turn_report(task_id) for task_id in task_ids])


def write_report_transcripts(root: Path, reports: list[dict[str, Any]]) -> Path:
    path = root / "transcripts"
    path.mkdir(parents=True, exist_ok=True)
    for index, report in enumerate(reports, start=1):
        task_id = str(report["task_id"])
        write_json(
            path / f"{index:02d}-{task_id}.json",
            {
                "format": "recorded_invoker.v1",
                "expected_prompt_contains": [task_id, "SPEC-9600 fixture"],
                "report": report,
            },
        )
    return path


def command_arg(value: Path | str) -> str:
    text = str(value)
    if os.name == "nt":
        return '"' + text.replace('"', r'\"') + '"'
    return shlex.quote(text)


def write_dynamic_subprocess_agent(root: Path, reports: list[dict[str, Any]]) -> Path:
    script = root / "agent script dir" / "supervised_subprocess_agent.py"
    by_task = {str(report["task_id"]): report for report in reports}
    payload = json.dumps(by_task, sort_keys=True)
    script.parent.mkdir(parents=True, exist_ok=True)
    script.write_text(
        "\n".join(
            [
                "import json",
                "import sys",
                "prompt = sys.stdin.read()",
                f"reports = json.loads({payload!r})",
                "for task_id, report in reports.items():",
                "    if task_id in prompt:",
                "        print(json.dumps(report))",
                "        break",
                "else:",
                "    raise SystemExit('no task id in prompt')",
            ]
        ),
        encoding="utf-8",
    )
    return script


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
        assert "caps.wall_clock_ms: 1000" in text
        assert "caps.human_checkpoint_every_k: 2" in text


def case_human_checkpoint_every_k_stops_with_human_required() -> None:
    with tempfile.TemporaryDirectory(prefix="supervised-human-checkpoint-") as temp:
        fixture = Path(temp)
        task_ids = ["TASK-9600", "TASK-9601", "TASK-9602"]
        build_fixture(
            fixture,
            task_ids=task_ids,
            supervised=supervised_config(enabled=True, max_turns=5, human_checkpoint_every_k=2),
        )
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
                "RUN-supervised-human-checkpoint",
                "--replay-report",
                str(transcripts),
            ],
        )
        result = json.loads(completed.stdout)
        assert result["ok"] is True, result
        assert git_count(fixture) == before + 2
        assert statuses(fixture) == ["done", "done", "ready"]
        last = result["turns"][-1]
        assert last["outcome"] == "human_checkpoint", result
        assert last["human_required"] is True, result
        assert "caps.human_checkpoint_every_k=2" in last["reason"], result
        text = Path(result["run_report"]).read_text(encoding="utf-8-sig")
        assert "human_checkpoint" in text
        assert "caps.human_checkpoint_every_k: 2" in text


def case_fix_cycles_trigger_human_checkpoint() -> None:
    with tempfile.TemporaryDirectory(prefix="supervised-fix-cycle-checkpoint-") as temp:
        fixture = Path(temp)
        task_ids = ["TASK-9600", "TASK-9601"]
        build_fixture(
            fixture,
            task_ids=task_ids,
            supervised=supervised_config(enabled=True, max_turns=5, human_checkpoint_every_k=5),
            task_statuses={"TASK-9600": "in_review"},
            task_owners={"TASK-9600": "Codex"},
            task_overrides={"TASK-9600": {"review_attempts": 2}},
            claim_owners={"TASK-9600": "Claude"},
            quality_policy={"max_review_cycles": 3, "max_qa_cycles": 3},
        )
        transcripts = write_report_transcripts(fixture, [review_rejection_report("TASK-9600"), turn_report("TASK-9601")])
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
                "RUN-supervised-fix-cycle-checkpoint",
                "--replay-report",
                str(transcripts),
            ],
        )
        result = json.loads(completed.stdout)
        assert result["ok"] is True, result
        assert git_count(fixture) == before + 1
        assert statuses(fixture) == ["changes_requested", "ready"]
        last = result["turns"][-1]
        assert last["outcome"] == "human_checkpoint", result
        assert last["human_required"] is True, result
        assert "quality_policy.max_review_cycles=3" in last["reason"], result
        text = Path(result["run_report"]).read_text(encoding="utf-8-sig")
        assert "human_checkpoint" in text
        assert "quality_policy.max_review_cycles=3" in text


def case_pause_sentinel_stops_before_turn_without_mutating_state() -> None:
    with tempfile.TemporaryDirectory(prefix="supervised-pause-") as temp:
        fixture = Path(temp)
        task_ids = ["TASK-9600"]
        build_fixture(fixture, task_ids=task_ids, supervised=supervised_config(enabled=True, max_turns=2))
        transcripts = write_transcripts(fixture, task_ids)
        pause = fixture / "runtime/state/PAUSE"
        pause.parent.mkdir(parents=True, exist_ok=True)
        pause.write_text("paused by fixture\n", encoding="utf-8")
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
                "RUN-supervised-pause",
                "--replay-report",
                str(transcripts),
            ],
        )
        result = json.loads(completed.stdout)
        assert result["ok"] is True, result
        assert git_count(fixture) == before
        assert statuses(fixture) == ["ready"]
        assert result["turns"][0]["outcome"] == "paused", result
        assert result["turns"][0]["trace"] == ["supervised_autonomy", "pause"], result
        assert Path(result["run_report"]).exists()


def case_wall_clock_stops_before_turn_that_would_exceed_cap() -> None:
    with tempfile.TemporaryDirectory(prefix="supervised-wallclock-") as temp:
        fixture = Path(temp)
        task_ids = ["TASK-9600", "TASK-9601"]
        build_fixture(fixture, task_ids=task_ids, supervised=supervised_config(enabled=True, max_turns=5, wall_clock_ms=150))
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
                "RUN-supervised-wallclock",
                "--clock-fixed",
                "100",
                "--replay-report",
                str(transcripts),
            ],
        )
        result = json.loads(completed.stdout)
        assert result["ok"] is True, result
        assert git_count(fixture) == before + 1
        assert statuses(fixture) == ["done", "ready"]
        assert result["turns"][-1]["outcome"] == "wallclock_exhausted", result
        assert result["turns"][-1]["trace"] == ["supervised_autonomy", "wall_clock"], result
        text = Path(result["run_report"]).read_text(encoding="utf-8-sig")
        assert "wallclock_exhausted" in text
        assert "caps.wall_clock_ms: 150" in text


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


def case_real_subprocess_multiturn_requires_registered_supervision_and_real_invoker() -> None:
    with tempfile.TemporaryDirectory(prefix="supervised-real-multiturn-") as temp:
        fixture = Path(temp)
        task_ids = ["TASK-9600", "TASK-9601"]
        build_fixture(
            fixture,
            task_ids=task_ids,
            supervised=supervised_config(enabled=True, max_turns=2, human_checkpoint_every_k=5),
            real_invoker=real_invoker_config(enabled=True),
        )
        script = write_dynamic_subprocess_agent(fixture, [turn_report(task_id) for task_id in task_ids])
        before = git_count(fixture)
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
                f"{command_arg(sys.executable)} {command_arg(script)}",
                "--max-iter",
                "2",
                "--run-id",
                "RUN-supervised-real-multiturn",
            ],
        )
        result = json.loads(completed.stdout)
        assert result["ok"] is True, result
        assert git_count(fixture) == before + 2
        assert statuses(fixture) == ["done", "done"]
        assert "run_report" in result, result
        assert result["supervised_autonomy"]["caps"]["max_turns"] == 2
        assert [turn["task_id"] for turn in result["turns"]] == task_ids


def case_real_subprocess_consecutive_runs_use_distinct_logs() -> None:
    with tempfile.TemporaryDirectory(prefix="supervised-real-distinct-runs-") as temp:
        fixture = Path(temp)
        task_ids = ["TASK-9600", "TASK-9601"]
        build_fixture(
            fixture,
            task_ids=task_ids,
            supervised=supervised_config(enabled=True, max_turns=2, human_checkpoint_every_k=5),
            real_invoker=real_invoker_config(enabled=True),
        )
        script = write_dynamic_subprocess_agent(fixture, [turn_report(task_id) for task_id in task_ids])
        common = [
            "--run",
            "--adapter",
            "llm",
            "--llm-invoker",
            "subprocess",
            "--allow-real-invoker",
            "--allow-supervised-autonomy",
            "--llm-command",
            f"{command_arg(sys.executable)} {command_arg(script)}",
            "--once",
        ]
        first = json.loads(run_orchestrator(fixture, [*common, "--run-id", "RUN-real-pass-1"]).stdout)
        second = json.loads(run_orchestrator(fixture, [*common, "--run-id", "RUN-real-pass-2"]).stdout)

        assert first["ok"] is True, first
        assert second["ok"] is True, second
        assert first["run_id"] == "RUN-real-pass-1"
        assert second["run_id"] == "RUN-real-pass-2"
        assert first["run_log"] != second["run_log"]
        assert first["metrics"]["turns_total"] == 1, first
        assert second["metrics"]["turns_total"] == 1, second
        assert [turn["task_id"] for turn in first["turns"]] == ["TASK-9600"]
        assert [turn["task_id"] for turn in second["turns"]] == ["TASK-9601"]
        assert len([line for line in Path(first["run_log"]).read_text(encoding="utf-8-sig").splitlines() if line.strip()]) == 1
        assert len([line for line in Path(second["run_log"]).read_text(encoding="utf-8-sig").splitlines() if line.strip()]) == 1


def main() -> int:
    cases = [
        case_max_turns_stops_recorded_loop_and_writes_runreport,
        case_human_checkpoint_every_k_stops_with_human_required,
        case_fix_cycles_trigger_human_checkpoint,
        case_pause_sentinel_stops_before_turn_without_mutating_state,
        case_wall_clock_stops_before_turn_that_would_exceed_cap,
        case_activation_without_valid_registration_rejects_before_run,
        case_flag_absent_keeps_existing_multi_turn_behavior,
        case_real_invoker_lock_remains_intact_in_sa1,
        case_real_subprocess_multiturn_requires_registered_supervision_and_real_invoker,
        case_real_subprocess_consecutive_runs_use_distinct_logs,
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
