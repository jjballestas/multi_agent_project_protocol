#!/usr/bin/env python3
"""Golden cases for tier-aware runtime upgrade reporting."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
UPGRADE_PY = ROOT / "scripts" / "upgrade_instance.py"
UPGRADE_PS = ROOT / "scripts" / "upgrade_instance.ps1"


def run(command: list[str], cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)


def assert_ok(result: subprocess.CompletedProcess[str]) -> None:
    assert result.returncode == 0, "\n".join([result.stdout, result.stderr])


def write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    write(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def build_master(root: Path) -> None:
    write_json(
        root / "protocol.config.json",
        {
            "schema_version": "1.0",
            "protocol_version": "2.0.0",
            "runtime_version": "2.0.0",
            "project_name": "runtime_upgrade_master",
        },
    )
    write_json(
        root / "protocol.config.template.json",
        {
            "schema_version": "1.0",
            "protocol_version": "{{PROTOCOL_VERSION}}",
            "runtime_version": "{{PROTOCOL_VERSION}}",
            "project_name": "{{PROJECT_NAME}}",
        },
    )
    write(root / "runtime/orchestrator.py", "# runtime orchestrator v2\n")
    write(root / "runtime/budget.py", "# runtime budget v2\n")
    write(root / "runtime/new_engine.py", "# new runtime file\n")
    write(root / ".github/workflows/validate.yml", "name: runtime-ci-v2\n")
    write(root / "runtime/state/events.jsonl", '{"seq":1}\n')
    write(root / "runtime/runs/RUN-fixture.jsonl", '{"turn":1}\n')
    write(root / "runtime/__pycache__/ignored.pyc", "ignored\n")


def build_instance(root: Path, *, tier: str | None = "runtime") -> None:
    config: dict[str, Any] = {
        "schema_version": "1.0",
        "protocol_version": "1.0.0",
        "runtime_version": "1.0.0",
        "project_name": f"runtime_upgrade_{tier or 'absent'}",
    }
    if tier is not None:
        config["adoption_tier"] = tier
    write_json(root / "protocol.config.json", config)
    write_json(
        root / "protocol.config.template.json",
        {
            "schema_version": "1.0",
            "protocol_version": "{{PROTOCOL_VERSION}}",
            "runtime_version": "{{PROTOCOL_VERSION}}",
            "project_name": "{{PROJECT_NAME}}",
        },
    )
    write(root / "runtime/orchestrator.py", "# runtime orchestrator v1\n")
    write(root / "runtime/legacy_engine.py", "# removed runtime file\n")
    write(root / ".github/workflows/validate.yml", "name: runtime-ci-v1\n")
    write(root / "runtime/state/events.jsonl", '{"seq":99}\n')
    write(root / "runtime/runs/RUN-old.jsonl", '{"turn":99}\n')
    write(root / "runtime/__pycache__/ignored.pyc", "ignored-old\n")


def file_snapshot(root: Path) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        snapshot[path.relative_to(root).as_posix()] = hashlib.sha256(path.read_bytes()).hexdigest()
    return snapshot


def report_py(instance: Path, master: Path) -> str:
    result = run([sys.executable, str(UPGRADE_PY), "--instance", str(instance), "--master", str(master)])
    assert_ok(result)
    return result.stdout


def report_ps(instance: Path, master: Path) -> str | None:
    shell = shutil.which("pwsh") or shutil.which("powershell")
    if not shell:
        return None
    result = run([shell, "-NoProfile", "-File", str(UPGRADE_PS), "-Instance", str(instance), "-Master", str(master)])
    assert_ok(result)
    return result.stdout.replace("\r\n", "\n")


def case_runtime_tier_reports_runtime_delta_and_version() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-upgrade-runtime-") as temp:
        root = Path(temp)
        master = root / "master"
        instance = root / "instance"
        build_master(master)
        build_instance(instance, tier="runtime")
        report = report_py(instance, master)
        assert "- Adoption tier de la instancia: `runtime`" in report
        assert "- Runtime version de la instancia: `1.0.0`" in report
        assert "- Runtime version del master: `2.0.0`" in report
        assert "| `runtime/orchestrator.py` | cambiado |" in report
        assert "| `runtime/budget.py` | nuevo |" in report
        assert "| `runtime/new_engine.py` | nuevo |" in report
        assert "| `runtime/legacy_engine.py` | eliminado |" in report
        assert "| `.github/workflows/validate.yml` | cambiado |" in report


def case_coordination_tier_does_not_report_runtime_delta() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-upgrade-coordination-") as temp:
        root = Path(temp)
        master = root / "master"
        instance = root / "instance"
        build_master(master)
        build_instance(instance, tier="coordination")
        report = report_py(instance, master)
        assert "Runtime version" not in report
        assert "Adoption tier de la instancia" not in report
        assert "runtime/" not in report
        assert ".github/workflows/validate.yml" not in report


def case_runtime_execution_artifacts_are_excluded() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-upgrade-excludes-") as temp:
        root = Path(temp)
        master = root / "master"
        instance = root / "instance"
        build_master(master)
        build_instance(instance, tier="runtime")
        report = report_py(instance, master)
        assert "runtime/state/" not in report
        assert "runtime/runs/" not in report
        assert "__pycache__" not in report


def case_hooks_are_adoptable_for_existing_instances() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-upgrade-hooks-") as temp:
        root = Path(temp)
        master = root / "master"
        instance = root / "instance"
        build_master(master)
        build_instance(instance, tier="coordination")
        write(master / ".githooks/pre-commit", "#!/bin/sh\nexit 0\n")
        report = report_py(instance, master)
        assert "| `.githooks/pre-commit` | nuevo |" in report


def case_inform_only_and_powershell_parity() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-upgrade-parity-") as temp:
        root = Path(temp)
        master = root / "master"
        instance = root / "instance"
        build_master(master)
        build_instance(instance, tier="runtime")
        before = file_snapshot(instance)
        py_report = report_py(instance, master)
        ps_report = report_ps(instance, master)
        after = file_snapshot(instance)
        assert before == after
        if ps_report is not None:
            assert py_report.replace("\r\n", "\n") == ps_report


def main() -> int:
    cases = [
        case_runtime_tier_reports_runtime_delta_and_version,
        case_coordination_tier_does_not_report_runtime_delta,
        case_runtime_execution_artifacts_are_excluded,
        case_hooks_are_adoptable_for_existing_instances,
        case_inform_only_and_powershell_parity,
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
    print(f"OK: {len(cases)} runtime upgrade golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
