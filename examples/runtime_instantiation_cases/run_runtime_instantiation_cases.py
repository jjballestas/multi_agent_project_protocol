#!/usr/bin/env python3
"""Golden cases for tier-aware protocol instantiation."""

from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
NEW_INSTANCE = ROOT / "scripts" / "new_instance.py"
VALIDATOR = ROOT / "scripts" / "validate_collaboration_state.py"
SCAN_ENCODING = ROOT / "scripts" / "scan_encoding.py"
SCAN_NEUTRALITY = ROOT / "scripts" / "scan_domain_neutrality.py"

GATE_SCRIPTS = {
    "check_commit_trailers.py",
    "check_falsification_contracts.py",
    "falsification_contracts.py",
    "test_falsification_contracts.py",
    "ledger_head.py",
    "validate_collaboration_state.py",
    "validate_collaboration_state.ps1",
    "scan_encoding.py",
    "scan_encoding.ps1",
    "scan_domain_neutrality.py",
    "scan_domain_neutrality.ps1",
    "measure_context_cost.py",
    "generate_human_guide.py",
    "prune_state.py",
    "prune_state.ps1",
    "keygen_agent.py",
}


def run(command: list[str], *, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)


def assert_ok(result: subprocess.CompletedProcess[str]) -> None:
    assert result.returncode == 0, "\n".join([result.stdout, result.stderr])


def generate(target: Path, tier: str | None = None) -> None:
    project_name = f"{tier or 'coordination'}_project"
    command = [
        sys.executable,
        str(NEW_INSTANCE),
        "--source-template",
        str(ROOT),
        "--target",
        str(target),
        "--project-name",
        project_name,
        "--project-goal",
        "Validate tier-aware instantiation.",
        "--project-description",
        "Generated fixture for tier-aware instantiation.",
        "--architect",
        "Claude",
        "--implementer",
        "Codex",
        "--analyst",
        "Analyst",
        "--human-owner",
        "Human",
        "--phase-id",
        "P2",
        "--phase-name",
        "Instantiation fixture",
        "--phase-goal",
        "Keep the fixture valid.",
    ]
    if tier is not None:
        command.extend(["--tier", tier])
    assert_ok(run(command))


def load_config(root: Path) -> dict:
    return json.loads((root / "protocol.config.json").read_text(encoding="utf-8-sig"))


def assert_generated_tier(root: Path, requested_tier: str) -> None:
    actual_tier = load_config(root).get("adoption_tier")
    assert actual_tier == requested_tier, (
        f"generated tier mismatch: requested={requested_tier!r}, actual={actual_tier!r}"
    )


def assert_hooks_are_active(root: Path) -> None:
    configured = run(["git", "config", "--get", "core.hooksPath"], cwd=root)
    assert_ok(configured)
    assert configured.stdout.strip() == ".githooks"


def assert_broken_governed_state_is_rejected(root: Path) -> None:
    run(["git", "config", "user.name", "Fixture"], cwd=root)
    run(["git", "config", "user.email", "fixture@example.invalid"], cwd=root)
    assert_ok(run(["git", "add", "--", "."], cwd=root))
    assert_ok(run(["git", "commit", "--no-verify", "-m", "fixture baseline"], cwd=root))
    task_index = root / "Area_comun" / "state" / "TASK_INDEX.json"
    task_index.write_text("{broken\n", encoding="utf-8")
    assert_ok(run(["git", "add", "--", "Area_comun/state/TASK_INDEX.json"], cwd=root))
    rejected = run(["git", "commit", "-m", "broken governed state"], cwd=root)
    assert rejected.returncode != 0, "active generated hook accepted broken governed state"


def validate_with_repo_tools(root: Path) -> None:
    assert_ok(run([sys.executable, str(VALIDATOR), "--root", str(root)]))
    assert_ok(run([sys.executable, str(SCAN_ENCODING), "--root", str(root)]))
    assert_ok(run([sys.executable, str(SCAN_NEUTRALITY), "--root", str(root)]))


def validate_with_instance_tools(root: Path) -> None:
    assert_ok(run([sys.executable, str(root / "scripts" / "check_falsification_contracts.py"), "--root", str(root)]))
    assert_ok(run([sys.executable, str(root / "scripts" / "validate_collaboration_state.py"), "--root", str(root)]))
    assert_ok(run([sys.executable, str(root / "scripts" / "scan_encoding.py"), "--root", str(root)]))
    assert_ok(run([sys.executable, str(root / "scripts" / "scan_domain_neutrality.py"), "--root", str(root)]))
    assert_ok(run([sys.executable, str(root / "scripts" / "prune_state.py"), "--root", str(root), "--check"]))


def file_snapshot(root: Path) -> dict[str, str]:
    snapshot: dict[str, str] = {}
    for path in sorted(item for item in root.rglob("*") if item.is_file()):
        relative = path.relative_to(root).as_posix()
        if "__pycache__" in path.parts:
            continue
        snapshot[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    return snapshot


def assert_runtime_artifacts_not_copied(root: Path) -> None:
    assert not (root / "runtime" / "state").exists()
    assert not (root / "runtime" / "runs").exists()
    assert not any("__pycache__" in path.parts for path in (root / "runtime").rglob("*"))


def case_coordination_default_and_flag() -> None:
    with tempfile.TemporaryDirectory(prefix="tier-coordination-") as temp:
        default_root = Path(temp) / "default"
        explicit_root = Path(temp) / "explicit"
        generate(default_root)
        generate(explicit_root, "coordination")
        for root in (default_root, explicit_root):
            assert_generated_tier(root, "coordination")
            assert_hooks_are_active(root)
            assert (root / "runtime" / "protocol_replay.py").exists()
            assert {path.name for path in (root / "scripts").iterdir() if path.is_file()} == GATE_SCRIPTS
            assert not (root / ".github" / "workflows" / "validate.yml").exists()
            validate_with_repo_tools(root)
            validate_with_instance_tools(root)
        assert file_snapshot(default_root) == file_snapshot(explicit_root)


def case_runtime_tier_scaffolds_motor_gates_ci_off() -> None:
    with tempfile.TemporaryDirectory(prefix="tier-runtime-") as temp:
        root = Path(temp) / "runtime"
        generate(root, "runtime")
        assert_generated_tier(root, "runtime")
        assert_hooks_are_active(root)
        config = load_config(root)
        assert config["runtime"]["enabled"] is False
        assert config["tool_policy"]["enabled"] is False
        assert config["event_auth"]["enabled"] is False
        assert (root / "runtime" / "turn_schema.json").exists()
        assert (root / ".github" / "workflows" / "validate.yml").exists()
        assert {path.name for path in (root / "scripts").iterdir() if path.is_file()} == GATE_SCRIPTS
        validate_with_repo_tools(root)
        validate_with_instance_tools(root)


def case_generated_hook_rejects_broken_governed_state() -> None:
    with tempfile.TemporaryDirectory(prefix="tier-hook-negative-") as temp:
        root = Path(temp) / "coordination"
        generate(root, "coordination")
        assert_hooks_are_active(root)
        assert_broken_governed_state_is_rejected(root)


def case_missing_exported_ledger_head_is_detected() -> None:
    with tempfile.TemporaryDirectory(prefix="tier-ledger-head-negative-") as temp:
        root = Path(temp) / "runtime"
        generate(root, "runtime")
        ledger_head = root / "scripts" / "ledger_head.py"
        assert ledger_head.exists(), "generated instance did not export scripts/ledger_head.py"
        ledger_head.unlink()
        result = run(
            [sys.executable, str(root / "scripts" / "prune_state.py"), "--root", str(root), "--check"]
        )
        assert result.returncode != 0, "prune_state stayed green without exported ledger_head.py"


def case_declared_tier_mismatch_is_detected() -> None:
    with tempfile.TemporaryDirectory(prefix="tier-declaration-negative-") as temp:
        root = Path(temp) / "runtime"
        generate(root, "runtime")
        config_path = root / "protocol.config.json"
        config = load_config(root)
        config["adoption_tier"] = "coordination"
        config_path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
        try:
            assert_generated_tier(root, "runtime")
        except AssertionError:
            return
        raise AssertionError("runner accepted a generated tier that differs from the requested tier")


def case_runtime_excludes_execution_artifacts() -> None:
    with tempfile.TemporaryDirectory(prefix="tier-runtime-excludes-") as temp:
        root = Path(temp) / "runtime"
        generate(root, "runtime")
        assert_runtime_artifacts_not_copied(root)


def case_minimal_instance_stays_coordination() -> None:
    minimal = ROOT / "examples" / "minimal_instance"
    assert not (minimal / "runtime").exists()
    validate_with_repo_tools(minimal)


def case_generation_is_deterministic_per_tier() -> None:
    with tempfile.TemporaryDirectory(prefix="tier-determinism-") as temp:
        temp_root = Path(temp)
        for tier in ("coordination", "runtime"):
            left = temp_root / f"{tier}-left"
            right = temp_root / f"{tier}-right"
            generate(left, tier)
            generate(right, tier)
            assert file_snapshot(left) == file_snapshot(right)


def case_powershell_validator_parity_if_available() -> None:
    shell = shutil.which("pwsh") or shutil.which("powershell")
    if not shell:
        return
    with tempfile.TemporaryDirectory(prefix="tier-ps-") as temp:
        root = Path(temp) / "runtime"
        generate(root, "runtime")
        assert_ok(run([shell, "-NoProfile", "-File", str(VALIDATOR.with_suffix(".ps1")), "-Root", str(root)]))


def main() -> int:
    cases = [
        case_coordination_default_and_flag,
        case_runtime_tier_scaffolds_motor_gates_ci_off,
        case_generated_hook_rejects_broken_governed_state,
        case_missing_exported_ledger_head_is_detected,
        case_declared_tier_mismatch_is_detected,
        case_runtime_excludes_execution_artifacts,
        case_minimal_instance_stays_coordination,
        case_generation_is_deterministic_per_tier,
        case_powershell_validator_parity_if_available,
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
    print("OK: runtime instantiation cases passed (8 + ps1 parity when available).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
