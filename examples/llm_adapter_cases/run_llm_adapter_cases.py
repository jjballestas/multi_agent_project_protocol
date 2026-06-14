#!/usr/bin/env python3
"""Golden cases for the runtime LLM adapter."""

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
    path.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")


def task(task_id: str) -> dict[str, Any]:
    return {
        "id": task_id,
        "owner": "Codex",
        "status": "ready",
        "type": "implementation",
        "priority": "normal",
        "phase": "P2",
        "spec_id": "Area_comun/specs/SPEC-9000-fixture.md",
        "linked_decisions": ["DECISION-0009"],
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
        "notes": "llm adapter fixture",
    }


def build_fixture(root: Path, *, enabled: bool = True, task_id: str = "TASK-9000", real_invoker_enabled: bool = False) -> None:
    item = task(task_id)
    runtime_config: dict[str, Any] = {"enabled": enabled, "entrypoint": "runtime/orchestrator.py"}
    if real_invoker_enabled:
        runtime_config["real_invoker"] = {
            "enabled": True,
            "activation_decision": "DECISION-0021",
            "approved_by": "Fixture Owner",
            "approved_at": "2026-06-07",
        }
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
            "active_tasks": [{"id": item["id"], "owner": "Codex", "status": "ready", "title": "Fixture"}],
        },
    )
    write_json(root / "Area_comun/state/TASK_INDEX.json", {"schema_version": "1.0", "tasks": [item]})
    write_json(root / "Area_comun/state/CLAIMS.json", {"schema_version": "1.0", "claims": [claim(item["id"])]})
    task_path = root / item["file"]
    task_path.parent.mkdir(parents=True, exist_ok=True)
    task_path.write_text(f"---\nid: {item['id']}\nstatus: ready\n---\n\n# Fixture\n", encoding="utf-8")
    spec_path = root / "Area_comun/specs/SPEC-9000-fixture.md"
    spec_path.parent.mkdir(parents=True, exist_ok=True)
    spec_path.write_text("# SPEC-9000 fixture\n", encoding="utf-8")
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


def turn_report(task_id: str, *, cost: int = 3, outside_scope: bool = False) -> dict[str, Any]:
    changed_paths = [
        f"Area_comun/tasks/{task_id}.md",
        f"Area_comun/state/TASK_INDEX.json#{task_id}",
        f"Area_comun/state/PROJECT_STATE.json#active_tasks/{task_id}",
        "Area_comun/state/CLAIMS.json",
    ]
    if outside_scope:
        changed_paths.append("Area_comun/decisions/DECISION-9999-fixture.md")
    return {
        "turn_id": f"RUN-fixture-{task_id}",
        "task_id": task_id,
        "agent": "Codex",
        "outcome": "done",
        "summary": f"Move {task_id}.",
        "changed_paths": changed_paths,
        "transitions": {
            "task_status": {"from": "ready", "to": "done"},
            "claims": [{"op": "release", "claim_id": f"CLAIM-{task_id}-codex"}],
        },
        "commit_message": f"test(runtime): llm {task_id}",
        "gate": {"human_required": False},
        "next_hint": None,
        "cost": {"tokens": cost},
    }


def write_transcript(root: Path, report: dict[str, Any]) -> Path:
    path = root / "transcripts/01-recorded.json"
    write_json(
        path,
        {
            "format": "recorded_invoker.v1",
            "expected_prompt_contains": [report["task_id"], "SPEC-9000 fixture"],
            "report": report,
        },
    )
    return path.parent


def write_replay(root: Path, report: dict[str, Any]) -> Path:
    path = root / "replay/01-report.json"
    write_json(path, report)
    return path.parent


def command_arg(value: Path | str) -> str:
    text = str(value)
    if os.name == "nt":
        return '"' + text.replace('"', r'\"') + '"'
    return shlex.quote(text)


def write_subprocess_agent(root: Path, report: dict[str, Any]) -> Path:
    script = root / "agent script dir" / "fixture_agent.py"
    payload = json.dumps(report, sort_keys=True)
    script.parent.mkdir(parents=True, exist_ok=True)
    script.write_text(
        "\n".join(
            [
                "import json",
                "import sys",
                "prompt = sys.stdin.read()",
                "if 'SPEC-9000 fixture' not in prompt:",
                "    raise SystemExit('missing spec in prompt')",
                f"report = json.loads({payload!r})",
                "print(json.dumps(report))",
            ]
        ),
        encoding="utf-8",
    )
    return script


def run_orchestrator(root: Path, args: list[str], check: bool = True) -> subprocess.CompletedProcess[str]:
    return run([sys.executable, str(ORCHESTRATOR), "--root", str(root), *args], ROOT, check=check)


def git_count(root: Path) -> int:
    return int(run(["git", "rev-list", "--count", "HEAD"], root).stdout.strip())


def task_status(root: Path) -> str:
    return json.loads((root / "Area_comun/state/TASK_INDEX.json").read_text(encoding="utf-8-sig"))["tasks"][0]["status"]


def case_recorded_llm_once_commits() -> None:
    with tempfile.TemporaryDirectory(prefix="llm-adapter-once-") as temp:
        fixture = Path(temp)
        build_fixture(fixture)
        before = git_count(fixture)
        transcripts = write_transcript(fixture, turn_report("TASK-9000"))
        completed = run_orchestrator(
            fixture,
            ["--run", "--adapter", "llm", "--llm-invoker", "recorded", "--once", "--replay-report", str(transcripts)],
        )
        result = json.loads(completed.stdout)
        assert result["ok"] is True, result
        assert git_count(fixture) == before + 1
        assert task_status(fixture) == "done"
        assert result["turns"][0]["trace"] == ["gate_pre", "route", "claim", "adapter", "validate", "human_gate", "apply", "gate_post", "commit"]


def case_replay_comparative() -> None:
    with tempfile.TemporaryDirectory(prefix="llm-adapter-compare-") as temp:
        base = Path(temp)
        replay_root = base / "replay-root"
        llm_root = base / "llm-root"
        report = turn_report("TASK-9000")
        build_fixture(replay_root)
        build_fixture(llm_root)
        replay_reports = write_replay(replay_root, report)
        transcripts = write_transcript(llm_root, report)
        replay_result = json.loads(run_orchestrator(replay_root, ["--run", "--once", "--replay-report", str(replay_reports)]).stdout)
        llm_result = json.loads(
            run_orchestrator(
                llm_root,
                ["--run", "--adapter", "llm", "--llm-invoker", "recorded", "--once", "--replay-report", str(transcripts)],
            ).stdout
        )
        assert replay_result["turns"][0]["transition"] == llm_result["turns"][0]["transition"] == {"from": "ready", "to": "done"}
        assert task_status(replay_root) == task_status(llm_root) == "done"
        assert git_count(replay_root) == git_count(llm_root) == 2


def case_outside_allowlist_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="llm-adapter-allowlist-") as temp:
        fixture = Path(temp)
        build_fixture(fixture)
        before = git_count(fixture)
        transcripts = write_transcript(fixture, turn_report("TASK-9000", outside_scope=True))
        completed = run_orchestrator(
            fixture,
            ["--run", "--adapter", "llm", "--llm-invoker", "recorded", "--once", "--replay-report", str(transcripts)],
        )
        result = json.loads(completed.stdout)
        assert result["turns"][0]["outcome"] == "rejected"
        assert "write outside active claim scope" in result["turns"][0]["errors"][0]
        assert git_count(fixture) == before
        assert task_status(fixture) == "ready"


def case_budget_abort_before_apply() -> None:
    with tempfile.TemporaryDirectory(prefix="llm-adapter-budget-") as temp:
        fixture = Path(temp)
        build_fixture(fixture)
        before = git_count(fixture)
        transcripts = write_transcript(fixture, turn_report("TASK-9000", cost=6))
        completed = run_orchestrator(
            fixture,
            [
                "--run",
                "--adapter",
                "llm",
                "--llm-invoker",
                "recorded",
                "--once",
                "--budget-tokens",
                "5",
                "--replay-report",
                str(transcripts),
            ],
        )
        result = json.loads(completed.stdout)
        assert result["turns"][0]["outcome"] == "budget_exhausted"
        assert git_count(fixture) == before
        assert task_status(fixture) == "ready"


def case_enabled_false_aborts() -> None:
    with tempfile.TemporaryDirectory(prefix="llm-adapter-disabled-") as temp:
        fixture = Path(temp)
        build_fixture(fixture, enabled=False)
        transcripts = write_transcript(fixture, turn_report("TASK-9000"))
        completed = run_orchestrator(
            fixture,
            ["--run", "--adapter", "llm", "--llm-invoker", "recorded", "--once", "--replay-report", str(transcripts)],
            check=False,
        )
        result = json.loads(completed.stdout)
        assert completed.returncode == 1
        assert result["ok"] is False
        assert "runtime.enabled is false" in result["reason"]


def case_subprocess_native_command_commits() -> None:
    with tempfile.TemporaryDirectory(prefix="llm-adapter-subprocess-") as temp:
        fixture = Path(temp)
        build_fixture(fixture, real_invoker_enabled=True)
        before = git_count(fixture)
        script = write_subprocess_agent(fixture, turn_report("TASK-9000"))
        command = f"{command_arg(sys.executable)} {command_arg(script)}"
        assert "\\" in command if os.name == "nt" else "/" in command
        completed = run_orchestrator(
            fixture,
            [
                "--run",
                "--adapter",
                "llm",
                "--llm-invoker",
                "subprocess",
                "--allow-real-invoker",
                "--llm-command",
                command,
                "--once",
                "--run-id",
                "RUN-llm-subprocess-native",
            ],
        )
        result = json.loads(completed.stdout)
        assert result["ok"] is True, result
        assert git_count(fixture) == before + 1
        assert task_status(fixture) == "done"


def main() -> int:
    cases = [
        case_recorded_llm_once_commits,
        case_replay_comparative,
        case_outside_allowlist_rejected,
        case_budget_abort_before_apply,
        case_enabled_false_aborts,
        case_subprocess_native_command_commits,
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
    print(f"OK: {len(cases)} llm adapter golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
