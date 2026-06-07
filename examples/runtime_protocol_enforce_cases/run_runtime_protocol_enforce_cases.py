#!/usr/bin/env python3
"""Golden cases for protocol state drift enforcement B.3."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
MATERIALIZE_CASES = ROOT / "examples/runtime_protocol_materialize_cases"
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(MATERIALIZE_CASES))

from run_runtime_protocol_materialize_cases import (  # noqa: E402
    build_fixture,
    init_git,
    read_json,
    run,
    turn_report,
    write_json,
)
from runtime.apply import apply_gate_and_commit  # noqa: E402
from runtime.eventlog import read_jsonl_torn_safe  # noqa: E402
from runtime.protocol_replay import protocol_state_drift, write_genesis  # noqa: E402


def validator(root: Path, *, powershell: bool = False, check: bool = True) -> subprocess.CompletedProcess[str]:
    if powershell:
        shell = shutil.which("pwsh") or shutil.which("powershell")
        if not shell:
            return subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
        return run(
            [
                shell,
                "-NoProfile",
                "-ExecutionPolicy",
                "Bypass",
                "-File",
                str(ROOT / "scripts/validate_collaboration_state.ps1"),
                "-Root",
                str(root),
            ],
            check=check,
        )
    return run([sys.executable, str(ROOT / "scripts/validate_collaboration_state.py"), "--root", str(root)], check=check)


def diverge_project_title(root: Path) -> None:
    project = read_json(root / "Area_comun/state/PROJECT_STATE.json")
    project["active_tasks"][0]["title"] = "Diverged fixture title"
    write_json(root / "Area_comun/state/PROJECT_STATE.json", project)


def git_count(root: Path) -> int:
    return int(run(["git", "rev-list", "--count", "HEAD"], root).stdout.strip())


def task_status(root: Path) -> str:
    return read_json(root / "Area_comun/state/TASK_INDEX.json")["tasks"][0]["status"]


def event_types(root: Path) -> list[str]:
    return [event["type"] for event in read_jsonl_torn_safe(root / "runtime/state/events.jsonl")]


def build_runtime_fixture(root: Path, *, enforce: bool, materialize: bool = False) -> None:
    build_fixture(root, event_enabled=True, materialize=materialize, enforce=enforce, tier="runtime")


def case_validator_enforce_drift_hard_fails_py_and_ps() -> None:
    with tempfile.TemporaryDirectory(prefix="protocol-enforce-validator-") as temp:
        root = Path(temp)
        build_runtime_fixture(root, enforce=True)
        write_genesis(root)
        diverge_project_title(root)
        py = validator(root, check=False)
        assert py.returncode != 0, py.stdout
        assert "hard-fail B.3" in py.stdout, py.stdout
        assert "Area_comun/state/PROJECT_STATE.json" in py.stdout, py.stdout
        ps = validator(root, powershell=True, check=False)
        if ps.args:
            assert ps.returncode != 0, ps.stdout
            assert "hard-fail B.3" in ps.stdout, ps.stdout


def case_validator_enforce_coherent_passes() -> None:
    with tempfile.TemporaryDirectory(prefix="protocol-enforce-coherent-") as temp:
        root = Path(temp)
        build_runtime_fixture(root, enforce=True)
        write_genesis(root)
        assert "OK: collaboration state is valid." in validator(root).stdout
        ps = validator(root, powershell=True)
        if ps.args:
            assert "OK: collaboration state is valid." in ps.stdout


def case_enforce_false_or_no_runtime_state_is_warning_only() -> None:
    with tempfile.TemporaryDirectory(prefix="protocol-enforce-off-") as temp:
        root = Path(temp)
        build_runtime_fixture(root, enforce=False)
        write_genesis(root)
        diverge_project_title(root)
        py = validator(root, check=False)
        assert py.returncode == 0, py.stdout
        assert "warning-only B.1" in py.stdout, py.stdout

    with tempfile.TemporaryDirectory(prefix="protocol-enforce-no-state-") as temp:
        root = Path(temp)
        build_runtime_fixture(root, enforce=True)
        py = validator(root, check=False)
        assert py.returncode == 0, py.stdout
        assert "Runtime protocol state drift" not in py.stdout, py.stdout

    with tempfile.TemporaryDirectory(prefix="protocol-enforce-tier-") as temp:
        root = Path(temp)
        build_fixture(root, event_enabled=True, materialize=False, enforce=True, tier="coordination")
        write_genesis(root)
        diverge_project_title(root)
        py = validator(root, check=False)
        assert py.returncode == 0, py.stdout
        assert "warning-only B.1" in py.stdout, py.stdout


def case_apply_aborts_commit_when_enforced_drift_exists() -> None:
    with tempfile.TemporaryDirectory(prefix="protocol-enforce-apply-red-") as temp:
        root = Path(temp)
        build_runtime_fixture(root, enforce=True)
        write_genesis(root)
        diverge_project_title(root)
        init_git(root)
        before = git_count(root)
        result = apply_gate_and_commit(turn_report(), root)
        assert result["green"] is False, result
        assert result["blocked"] is True, result
        assert "event_state.enforce" in result["error"], result
        assert git_count(root) == before
        assert task_status(root) == "blocked"
        assert event_types(root) == ["protocol.genesis"]


def case_apply_commits_when_enforced_state_is_coherent() -> None:
    with tempfile.TemporaryDirectory(prefix="protocol-enforce-apply-green-") as temp:
        root = Path(temp)
        build_runtime_fixture(root, enforce=True)
        write_genesis(root)
        init_git(root)
        before = git_count(root)
        result = apply_gate_and_commit(turn_report(), root)
        assert result["green"] is True, result
        assert result["protocol_drift_gate"]["enforced"] is True, result
        assert git_count(root) == before + 1
        assert protocol_state_drift(root)["has_drift"] is False


def case_apply_tier_coordination_does_not_force_enforce() -> None:
    with tempfile.TemporaryDirectory(prefix="protocol-enforce-tier-apply-") as temp:
        root = Path(temp)
        build_fixture(root, event_enabled=True, materialize=False, enforce=True, tier="coordination")
        write_genesis(root)
        diverge_project_title(root)
        init_git(root)
        before = git_count(root)
        result = apply_gate_and_commit(turn_report(), root)
        assert result["green"] is True, result
        assert result["protocol_drift_gate"]["enforced"] is False, result
        assert git_count(root) == before + 1


def case_b1_b2_regression_suites_still_pass() -> None:
    replay = run([sys.executable, str(ROOT / "examples/runtime_protocol_replay_cases/run_runtime_protocol_replay_cases.py")])
    materialize = run([sys.executable, str(ROOT / "examples/runtime_protocol_materialize_cases/run_runtime_protocol_materialize_cases.py")])
    assert "OK:" in replay.stdout, replay.stdout
    assert "OK:" in materialize.stdout, materialize.stdout


def main() -> int:
    cases = [
        case_validator_enforce_drift_hard_fails_py_and_ps,
        case_validator_enforce_coherent_passes,
        case_enforce_false_or_no_runtime_state_is_warning_only,
        case_apply_aborts_commit_when_enforced_drift_exists,
        case_apply_commits_when_enforced_state_is_coherent,
        case_apply_tier_coordination_does_not_force_enforce,
        case_b1_b2_regression_suites_still_pass,
    ]
    failures: list[dict[str, Any]] = []
    for case in cases:
        try:
            case()
        except Exception as exc:  # noqa: BLE001 - compact golden failure reporting
            failures.append({"case": case.__name__, "error": str(exc)})
    if failures:
        print(json.dumps({"status": "FAILED", "failures": failures}, indent=2))
        return 1
    print(f"OK: {len(cases)} runtime protocol enforce golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
