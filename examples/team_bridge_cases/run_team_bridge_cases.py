#!/usr/bin/env python3
"""Golden cases for the Agent Teams hook bridge layers A+B."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
BRIDGE = ROOT / "runtime" / "team_bridge.py"
OBSERVED_AT = "2026-06-08T10:00:00Z"


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True, sort_keys=True) + "\n", encoding="utf-8")


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_audit(root: Path) -> list[dict[str, Any]]:
    path = root / "Area_comun/state/team_audit.jsonl"
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="ascii").splitlines() if line.strip()]


def bridge_config(*, enabled: bool, layers: list[str] | None = None, valid: bool = True) -> dict[str, Any]:
    return {
        "enabled": enabled,
        "layers": layers or [],
        "activation_decision": "DECISION-0025" if valid else "",
        "approved_by": "operador humano" if valid else "",
        "approved_at": "2026-06-08" if valid else "",
    }


def build_fixture(root: Path, *, bridge: dict[str, Any], valid_state: bool = True) -> None:
    write_json(
        root / "protocol.config.json",
        {
            "schema_version": "1.0",
            "runtime": {"enabled": True, "team_bridge": bridge},
            "domain_neutrality": {
                "enabled": True,
                "denylist": ["forbidden-domain-term"],
                "scan_globs": ["Area_comun/tasks/*.md", "runtime/**/*.py"],
                "exempt_globs": [],
            },
            "state_invariants": [{"path": "status", "equals": "active"}],
        },
    )
    write_json(
        root / "Area_comun/state/PROJECT_STATE.json",
        {
            "project": "team_bridge_fixture",
            "status": "active" if valid_state else "broken",
            "agents": {"architect": "Claude", "implementer": "Codex", "human_owner": "operador humano"},
            "active_tasks": [{"id": "TASK-9900", "owner": "Codex", "status": "done", "title": "Fixture"}],
            "open_questions": [],
            "risks": [],
            "next_actions": [],
        },
    )
    write_json(
        root / "Area_comun/state/TASK_INDEX.json",
        {
            "schema_version": "1.0",
            "tasks": [
                {
                    "id": "TASK-9900",
                    "owner": "Codex",
                    "status": "done",
                    "type": "documentation",
                    "priority": "normal",
                    "phase": "P2",
                    "title": "Fixture",
                    "file": "Area_comun/tasks/TASK-9900.md",
                    "depends_on": [],
                    "relates_to": [],
                    "relevant_files": [],
                    "deliverables": [],
                    "blocked_by_questions": [],
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
                    "claim_id": "CLAIM-TASK-9900-codex",
                    "task_id": "TASK-9900",
                    "owner": "Codex",
                    "status": "released",
                    "scope": ["Area_comun/"],
                    "started_at": "2026-06-08",
                    "updated_at": "2026-06-08",
                    "expires_at": "2026-06-09",
                    "notes": "fixture",
                }
            ],
        },
    )
    write_json(root / "Area_comun/state/CLAIMS_ARCHIVE.json", {"schema_version": "1.0", "claims": []})
    write_json(root / "Area_comun/state/TASK_INDEX_ARCHIVE.json", {"schema_version": "1.0", "tasks": []})
    task_path = root / "Area_comun/tasks/TASK-9900.md"
    task_path.parent.mkdir(parents=True, exist_ok=True)
    task_path.write_text("---\nid: TASK-9900\nstatus: done\n---\n\n# Fixture\n", encoding="utf-8")
    for folder in ("open", "answered", "archived"):
        (root / "Area_comun/mailbox" / folder).mkdir(parents=True, exist_ok=True)
    reports = root / "Area_comun/reports"
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "HUMAN_REPORT_TEMPLATE.md").write_text("# Human report\n", encoding="utf-8")


def run_bridge(root: Path, event: str, payload: dict[str, Any], *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(BRIDGE), "--root", str(root), "--event", event, "--observed-at", OBSERVED_AT],
        input=json.dumps(payload, ensure_ascii=True),
        text=True,
        capture_output=True,
        check=check,
    )


def case_off_without_activation_is_noop() -> None:
    with tempfile.TemporaryDirectory(prefix="team-bridge-off-") as temp:
        root = Path(temp)
        build_fixture(root, bridge=bridge_config(enabled=False, layers=["gate", "audit"]))
        before_state = read_json(root / "Area_comun/state/TASK_INDEX.json")
        completed = run_bridge(root, "TaskCompleted", {"subject": "[TASK-9900] done"})
        result = json.loads(completed.stdout)
        assert result["active"] is False, result
        assert "enabled is not true" in result["reason"], result
        assert read_json(root / "Area_comun/state/TASK_INDEX.json") == before_state
        assert read_audit(root) == []


def case_audit_only_appends_jsonl() -> None:
    with tempfile.TemporaryDirectory(prefix="team-bridge-audit-") as temp:
        root = Path(temp)
        build_fixture(root, bridge=bridge_config(enabled=True, layers=["audit"]))
        completed = run_bridge(root, "TaskCreated", {"subject": "new work", "task": {"title": "Fixture"}})
        result = json.loads(completed.stdout)
        assert result["audit"]["written"] is True, result
        entries = read_audit(root)
        assert entries == [
            {
                "hook": "TaskCreated",
                "observed_at": OBSERVED_AT,
                "subject": "new work",
                "task": {"title": "Fixture"},
            }
        ]


def case_gate_pass_exits_zero() -> None:
    with tempfile.TemporaryDirectory(prefix="team-bridge-gate-pass-") as temp:
        root = Path(temp)
        build_fixture(root, bridge=bridge_config(enabled=True, layers=["gate"]))
        completed = run_bridge(root, "TaskCompleted", {"subject": "done"})
        result = json.loads(completed.stdout)
        assert completed.returncode == 0
        assert result["gate"]["ok"] is True, result
        assert [check["label"] for check in result["gate"]["checks"]] == [
            "validate_collaboration_state",
            "scan_domain_neutrality",
        ]
        assert read_audit(root) == []


def case_gate_fail_exits_two_with_stderr() -> None:
    with tempfile.TemporaryDirectory(prefix="team-bridge-gate-fail-") as temp:
        root = Path(temp)
        build_fixture(root, bridge=bridge_config(enabled=True, layers=["gate"]), valid_state=False)
        completed = run_bridge(root, "TaskCompleted", {"subject": "done"}, check=False)
        assert completed.returncode == 2, completed.stdout
        assert "team_bridge gate failed" in completed.stderr
        assert "validate_collaboration_state" in completed.stderr
        result = json.loads(completed.stdout)
        assert result["gate"]["ok"] is False, result


def case_gate_and_audit() -> None:
    with tempfile.TemporaryDirectory(prefix="team-bridge-ab-") as temp:
        root = Path(temp)
        build_fixture(root, bridge=bridge_config(enabled=True, layers=["gate", "audit"]))
        completed = run_bridge(root, "TeammateIdle", {"teammate": "Codex", "reason": "idle"})
        result = json.loads(completed.stdout)
        assert result["gate"]["ok"] is True, result
        assert result["audit"]["written"] is True, result
        assert read_audit(root)[0]["hook"] == "TeammateIdle"


def case_task_marker_only_audits_without_ledger_mapping() -> None:
    with tempfile.TemporaryDirectory(prefix="team-bridge-marker-") as temp:
        root = Path(temp)
        build_fixture(root, bridge=bridge_config(enabled=True, layers=["gate", "audit"]))
        before = read_json(root / "Area_comun/state/TASK_INDEX.json")
        completed = run_bridge(root, "TaskCreated", {"subject": "[TASK-1234] draft task"})
        result = json.loads(completed.stdout)
        assert result["gate"]["skipped"] is True, result
        assert read_json(root / "Area_comun/state/TASK_INDEX.json") == before
        assert read_audit(root)[0]["subject"] == "[TASK-1234] draft task"


def case_audit_error_does_not_break_team() -> None:
    with tempfile.TemporaryDirectory(prefix="team-bridge-audit-error-") as temp:
        root = Path(temp)
        build_fixture(root, bridge=bridge_config(enabled=True, layers=["audit"]))
        audit_path = root / "Area_comun/state/team_audit.jsonl"
        audit_path.mkdir(parents=True)
        completed = run_bridge(root, "TaskCreated", {"subject": "audit failure"}, check=False)
        assert completed.returncode == 0, completed.stderr
        assert "team_bridge audit warning" in completed.stderr
        result = json.loads(completed.stdout)
        assert result["audit"]["written"] is False, result


def main() -> int:
    cases = [
        case_off_without_activation_is_noop,
        case_audit_only_appends_jsonl,
        case_gate_pass_exits_zero,
        case_gate_fail_exits_two_with_stderr,
        case_gate_and_audit,
        case_task_marker_only_audits_without_ledger_mapping,
        case_audit_error_does_not_break_team,
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
    print(f"OK: {len(cases)} team bridge golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
