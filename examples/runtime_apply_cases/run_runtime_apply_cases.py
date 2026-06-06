#!/usr/bin/env python3
"""Golden cases for runtime M1 apply/gate/vcs."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from runtime.apply import ApplyError, apply_gate_and_commit, apply_turn  # noqa: E402
from runtime.vcs import VcsError, commit_turn  # noqa: E402


TASK_ID = "TASK-9000"


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=True)


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def build_fixture(root: Path, denylist: list[str] | None = None) -> None:
    write_json(
        root / "protocol.config.json",
        {
            "schema_version": "1.0",
            "domain_neutrality": {
                "enabled": True,
                "denylist": denylist or [],
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
                    "claim_id": "CLAIM-fixture-codex",
                    "task_id": TASK_ID,
                    "owner": "Codex",
                    "status": "active",
                    "scope": [
                        f"Area_comun/tasks/{TASK_ID}.md",
                        f"Area_comun/state/TASK_INDEX.json#{TASK_ID}",
                        f"Area_comun/state/PROJECT_STATE.json#active_tasks/{TASK_ID}",
                        "Area_comun/state/CLAIMS.json",
                    ],
                    "started_at": "2026-06-05",
                    "updated_at": "2026-06-05",
                    "expires_at": "2026-06-06",
                    "notes": "fixture",
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


def turn_report() -> dict:
    return {
        "turn_id": "RUN-fixture-0001",
        "task_id": TASK_ID,
        "agent": "Codex",
        "outcome": "in_review",
        "summary": "Move fixture task to review.",
        "changed_paths": [
            f"Area_comun/tasks/{TASK_ID}.md",
            f"Area_comun/state/TASK_INDEX.json#{TASK_ID}",
            f"Area_comun/state/PROJECT_STATE.json#active_tasks/{TASK_ID}",
            "Area_comun/state/CLAIMS.json",
        ],
        "transitions": {
            "task_status": {"from": "ready", "to": "in_review"},
            "claims": [{"op": "release", "claim_id": "CLAIM-fixture-codex"}],
        },
        "commit_message": "test(runtime): apply fixture turn",
        "gate": {"human_required": False},
        "next_hint": None,
    }


def git_count(root: Path) -> int:
    return int(run(["git", "rev-list", "--count", "HEAD"], root).stdout.strip())


def case_valid_commit() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-apply-valid-") as temp:
        fixture = Path(temp)
        build_fixture(fixture)
        before = git_count(fixture)
        result = apply_gate_and_commit(turn_report(), fixture)
        assert result["green"] is True, result
        assert git_count(fixture) == before + 1
        status = json.loads((fixture / "Area_comun/state/TASK_INDEX.json").read_text())["tasks"][0]["status"]
        assert status == "in_review"


def case_gate_red_reverts_turn() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-apply-red-") as temp:
        fixture = Path(temp)
        build_fixture(fixture, denylist=["in_review"])
        before = git_count(fixture)
        result = apply_gate_and_commit(turn_report(), fixture)
        assert result["green"] is False, result
        assert result["reverted"] is True
        assert git_count(fixture) == before
        status = json.loads((fixture / "Area_comun/state/TASK_INDEX.json").read_text())["tasks"][0]["status"]
        assert status == "blocked"


def case_policy_reject() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-apply-policy-") as temp:
        fixture = Path(temp)
        build_fixture(fixture)
        (fixture / "AGENTS.md").write_text("policy\n", encoding="utf-8")
        try:
            commit_turn(fixture, "policy change", ["AGENTS.md"])
        except VcsError:
            return
        raise AssertionError("commit_turn accepted a policy path without allow_policy=True")


def case_invalid_report_no_write() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-apply-invalid-") as temp:
        fixture = Path(temp)
        build_fixture(fixture)
        report = turn_report()
        report["transitions"]["task_status"]["from"] = "blocked"
        try:
            apply_turn(report, fixture)
        except ApplyError:
            pass
        else:
            raise AssertionError("apply_turn accepted a stale report")
        status = json.loads((fixture / "Area_comun/state/TASK_INDEX.json").read_text())["tasks"][0]["status"]
        assert status == "ready"


def main() -> int:
    cases = [case_valid_commit, case_gate_red_reverts_turn, case_policy_reject, case_invalid_report_no_write]
    failures = []
    for case in cases:
        try:
            case()
        except Exception as exc:
            failures.append({"case": case.__name__, "error": str(exc)})
    if failures:
        print(json.dumps({"status": "FAILED", "failures": failures}, indent=2))
        return 1
    print(f"OK: {len(cases)} runtime apply golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
