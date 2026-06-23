#!/usr/bin/env python3
"""Golden cases for row-scoped state ledger claims."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def claim(suffix: str, owner: str, scope: list[str]) -> dict:
    return {
        "claim_id": f"CLAIM-row-scope-{suffix}",
        "task_id": "TASK-0100",
        "owner": owner,
        "status": "active",
        "scope": scope,
        "started_at": "2026-06-05",
        "updated_at": "2026-06-05",
        "expires_at": "2026-06-06",
        "notes": "golden case",
    }


CASES = [
    {
        "name": "distinct_rows_ok",
        "claims": [
            claim("A", "Claude", ["Area_comun/state/TASK_INDEX.json#TASK-0100"]),
            claim("B", "Codex", ["Area_comun/state/TASK_INDEX.json#TASK-0101"]),
        ],
        "valid": True,
    },
    {
        "name": "same_row_conflict",
        "claims": [
            claim("A", "Claude", ["Area_comun/state/TASK_INDEX.json#TASK-0100"]),
            claim("B", "Codex", ["Area_comun/state/TASK_INDEX.json#TASK-0100"]),
        ],
        "valid": False,
    },
    {
        "name": "bare_vs_row_conflict",
        "claims": [
            claim("A", "Claude", ["Area_comun/state/TASK_INDEX.json"]),
            claim("B", "Codex", ["Area_comun/state/TASK_INDEX.json#TASK-0100"]),
        ],
        "valid": False,
    },
    {
        "name": "legacy_bare_unchanged",
        "claims": [
            claim("A", "Claude", ["Area_comun/state/PROJECT_STATE.json"]),
            claim("B", "Codex", ["Area_comun/state/PROJECT_STATE.json"]),
        ],
        "valid": False,
    },
    {
        "name": "claims_distinct_rows_ok",
        "claims": [
            claim("A", "Claude", ["Area_comun/state/CLAIMS.json#CLAIM-row-scope-A"]),
            claim("B", "Codex", ["Area_comun/state/CLAIMS.json#CLAIM-row-scope-B"]),
        ],
        "valid": True,
    },
    {
        "name": "claims_same_row_conflict",
        "claims": [
            claim("A", "Claude", ["Area_comun/state/CLAIMS.json#CLAIM-row-scope-A"]),
            claim("B", "Codex", ["Area_comun/state/CLAIMS.json#CLAIM-row-scope-A"]),
        ],
        "valid": False,
    },
    {
        "name": "claims_bare_vs_row_conflict",
        "claims": [
            claim("A", "Claude", ["Area_comun/state/CLAIMS.json"]),
            claim("B", "Codex", ["Area_comun/state/CLAIMS.json#CLAIM-row-scope-B"]),
        ],
        "valid": False,
    },
    {
        "name": "invalid_selector",
        "claims": [
            claim("A", "Claude", ["Area_comun/state/TASK_INDEX.json#not-a-task"]),
        ],
        "valid": False,
    },
]


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def build_fixture(root: Path, claims: list[dict]) -> None:
    write_json(
        root / "protocol.config.json",
        {"schema_version": "1.0", "state_invariants": [{"path": "status", "equals": "active"}]},
    )
    write_json(root / "Area_comun/state/PROJECT_STATE.json", {"status": "active"})
    write_json(root / "Area_comun/state/TASK_INDEX.json", {"schema_version": "1.0", "tasks": []})
    write_json(root / "Area_comun/state/CLAIMS.json", {"schema_version": "1.0", "claims": claims})
    for folder in ("open", "answered", "archived"):
        (root / "Area_comun/mailbox" / folder).mkdir(parents=True, exist_ok=True)
    reports = root / "Area_comun/reports"
    reports.mkdir(parents=True, exist_ok=True)
    (reports / "HUMAN_REPORT_TEMPLATE.md").write_text("# Human report\n", encoding="utf-8")


def run_command(command: list[str], fixture_root: Path) -> tuple[bool, str]:
    completed = subprocess.run(command, cwd=ROOT, text=True, capture_output=True)
    return completed.returncode == 0, (completed.stdout + completed.stderr).strip()


def main() -> int:
    failures = []
    ps_exe = shutil.which("powershell") or shutil.which("pwsh")
    for case in CASES:
        with tempfile.TemporaryDirectory(prefix=f"row-scope-{case['name']}-") as temp:
            fixture_root = Path(temp)
            build_fixture(fixture_root, case["claims"])
            commands = [
                ["python", "scripts/validate_collaboration_state.py", "--root", str(fixture_root)],
            ]
            if ps_exe:
                commands.append(
                    [
                        ps_exe,
                        "-NoProfile",
                        "-ExecutionPolicy",
                        "Bypass",
                        "-File",
                        "scripts/validate_collaboration_state.ps1",
                        "-Root",
                        str(fixture_root),
                    ]
                )
            for command in commands:
                ok, output = run_command(command, fixture_root)
                if ok != case["valid"]:
                    failures.append(
                        {
                            "case": case["name"],
                            "command": command[0],
                            "expected_valid": case["valid"],
                            "output": output,
                        }
                    )
    if failures:
        print(json.dumps({"status": "FAILED", "failures": failures}, indent=2))
        return 1
    ps_note = "with PowerShell parity" if ps_exe else "without PowerShell runtime"
    print(f"OK: {len(CASES)} row-scoped claim cases passed ({ps_note}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
