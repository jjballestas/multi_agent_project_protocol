#!/usr/bin/env python3
"""Golden cases for runtime M1 replay loop."""

from __future__ import annotations

import json
import shutil
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


def claim(task_id: str, *, extra_scope: list[str] | None = None) -> dict:
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
            *(extra_scope or []),
        ],
        "started_at": "2026-06-06",
        "updated_at": "2026-06-06",
        "expires_at": "2026-06-07",
        "notes": "runtime loop fixture",
    }


def released_claim(index: int) -> dict:
    return {
        "claim_id": f"CLAIM-released-{index:04d}",
        "task_id": "none",
        "owner": "Codex",
        "status": "released",
        "scope": ["Area_comun/state/CLAIMS.json"],
        "started_at": "2026-06-06",
        "updated_at": "2026-06-06",
        "expires_at": "2026-06-07",
        "notes": "released fixture",
    }


def build_fixture(
    root: Path,
    *,
    enabled: bool = True,
    task_ids: list[str] | None = None,
    released_claims: int = 0,
    extra_claim_scope: list[str] | None = None,
    with_prune_scripts: bool = False,
) -> None:
    task_ids = task_ids or ["TASK-9000"]
    tasks = [task(task_id) for task_id in task_ids]
    write_json(
        root / "protocol.config.json",
        {
            "schema_version": "1.0",
            "runtime": {"enabled": enabled, "entrypoint": "runtime/orchestrator.py"},
            "maintenance": {
                "enabled": True,
                "cold_start_tokens_hard": 20000,
                "done_ratio_hard": 85,
                "released_ratio_hard": 90,
                "recent_done_tasks": 2,
                "recent_released_claims": 4,
                "mailbox_keep_recent": 8,
            },
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
    claims = [claim(item["id"], extra_scope=extra_claim_scope) for item in tasks]
    claims.extend(released_claim(index) for index in range(1, released_claims + 1))
    write_json(root / "Area_comun/state/CLAIMS.json", {"schema_version": "1.0", "claims": claims})
    write_json(root / "Area_comun/state/CLAIMS_ARCHIVE.json", {"schema_version": "1.0", "claims": []})
    write_json(root / "Area_comun/state/TASK_INDEX_ARCHIVE.json", {"schema_version": "1.0", "tasks": []})
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
    if with_prune_scripts:
        scripts = root / "scripts"
        scripts.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / "scripts/prune_state.py", scripts / "prune_state.py")
        shutil.copy2(ROOT / "scripts/measure_context_cost.py", scripts / "measure_context_cost.py")
    run(["git", "init"], root)
    run(["git", "config", "user.email", "runtime@example.invalid"], root)
    run(["git", "config", "user.name", "Runtime Test"], root)
    run(["git", "add", "."], root)
    run(["git", "commit", "-m", "fixture baseline"], root)


def install_prune_hook(root: Path) -> None:
    hook = root / ".git/hooks/pre-commit"
    hook.write_text(
        "\n".join(
            [
                "#!/usr/bin/env python",
                "import subprocess",
                "import sys",
                "raise SystemExit(subprocess.run([sys.executable, 'scripts/prune_state.py', '--root', '.', '--check']).returncode)",
            ]
        ),
        encoding="utf-8",
    )


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
            "Area_comun/state/CLAIMS.json",
        ],
        "transitions": {
            "task_status": {"from": "ready", "to": to_status},
            "claims": [{"op": "release", "claim_id": f"CLAIM-{task_id}-codex"}],
        },
        "commit_message": f"test(runtime): replay {task_id}",
        "gate": {"human_required": False},
        "next_hint": None,
    }


def policy_path_report(task_id: str) -> dict:
    report = turn_report(task_id)
    report["changed_paths"] = [*report["changed_paths"], "AGENTS.md"]
    report["commit_message"] = f"test(runtime): policy fail {task_id}"
    return report


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


def task_status(root: Path) -> str:
    return json.loads((root / "Area_comun/state/TASK_INDEX.json").read_text(encoding="utf-8-sig"))["tasks"][0]["status"]


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


def case_runtime_commit_bypasses_prune_hook_and_auto_prunes() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-loop-prune-hook-") as temp:
        fixture = Path(temp)
        build_fixture(fixture, released_claims=4, with_prune_scripts=True)
        install_prune_hook(fixture)
        report_dir = write_reports(fixture, [turn_report("TASK-9000")])
        before = git_count(fixture)
        completed = run_orchestrator(fixture, ["--run", "--once", "--run-id", "RUN-prune-hook", "--replay-report", str(report_dir)])
        result = json.loads(completed.stdout)
        assert result["ok"] is True, result
        assert git_count(fixture) == before + 2
        assert result["maintenance"]["due"] is True
        assert result["maintenance"]["commit"]
        assert run([sys.executable, "scripts/prune_state.py", "--root", ".", "--check"], fixture, check=False).returncode == 0
        claims = json.loads((fixture / "Area_comun/state/CLAIMS.json").read_text(encoding="utf-8-sig"))["claims"]
        assert len([item for item in claims if item["status"] == "released"]) <= 4


def case_manual_commit_still_uses_prune_hook() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-loop-manual-hook-") as temp:
        fixture = Path(temp)
        build_fixture(fixture, released_claims=10, with_prune_scripts=True)
        install_prune_hook(fixture)
        (fixture / "manual.txt").write_text("manual\n", encoding="utf-8")
        run(["git", "add", "manual.txt"], fixture)
        completed = run(["git", "commit", "-m", "manual should be gated"], fixture, check=False)
        assert completed.returncode != 0
        assert "PRUNE DUE" in completed.stderr


def case_commit_failure_discards_half_applied_turn_and_blocks() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-loop-commit-fail-") as temp:
        fixture = Path(temp)
        build_fixture(fixture, extra_claim_scope=["AGENTS.md"])
        (fixture / "AGENTS.md").write_text("# Fixture policy\n", encoding="utf-8")
        run(["git", "add", "AGENTS.md"], fixture)
        run(["git", "commit", "-m", "add policy fixture"], fixture)
        report_dir = write_reports(fixture, [policy_path_report("TASK-9000")])
        before = git_count(fixture)
        completed = run_orchestrator(fixture, ["--run", "--once", "--replay-report", str(report_dir)])
        result = json.loads(completed.stdout)
        assert result["ok"] is True, result
        assert git_count(fixture) == before
        assert result["turns"][0]["reverted"] is True
        assert task_status(fixture) == "blocked"
        claims = json.loads((fixture / "Area_comun/state/CLAIMS.json").read_text(encoding="utf-8-sig"))["claims"]
        assert claims[0]["status"] == "active"


def main() -> int:
    cases = [
        case_once_commits_one_turn,
        case_sequence_max_iter_cuts,
        case_human_required_stops_without_commit,
        case_plan_is_read_only,
        case_enabled_false_aborts_run,
        case_runtime_commit_bypasses_prune_hook_and_auto_prunes,
        case_manual_commit_still_uses_prune_hook,
        case_commit_failure_discards_half_applied_turn_and_blocks,
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
