#!/usr/bin/env python3
"""Golden cases for runtime tool-policy and action-gate validation."""

from __future__ import annotations

import hashlib
import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from runtime.context import load_agent_registry  # noqa: E402
from runtime.tool_policy import TOOL_DENIED_EVENT, classify_action, gate_for_action  # noqa: E402
from runtime.turn_validate import validate_turn  # noqa: E402


TASK_ID = "TASK-9901"


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def config_with_tool_policy(*, registry: bool = True, policy: bool = True) -> dict:
    config: dict = {
        "agent_roles": {
            "architect": "Claude",
            "implementer": "Codex",
            "human_owner": "operador humano",
        },
        "quality_policy": {"max_qa_cycles": 3},
    }
    if registry:
        config["agent_registry"] = {
            "enabled": True,
            "agents": [
                {"id": "Claude", "capabilities": ["architect", "reviewer", "orchestrator", "qa"], "enabled": True},
                {
                    "id": "Codex",
                    "capabilities": ["implementer", "test_engineer"],
                    "enabled": True,
                    "tool_policy_ref": "policy.implementer",
                },
            ],
        }
    if policy:
        config["tool_policy"] = {
            "enabled": True,
            "default": "deny",
            "agent_policies": {"Codex": "policy.implementer"},
            "policies": {
                "policy.implementer": {
                    "allow": [
                        {
                            "tool": "local.patch",
                            "capabilities": ["implementer"],
                            "scope": ["runtime/", "examples/runtime_tool_policy_cases/"],
                            "actions": ["local_write"],
                        },
                        {
                            "tool": "local.shell",
                            "capabilities": ["test_engineer"],
                            "scope": ["runtime/", "examples/runtime_tool_policy_cases/"],
                            "actions": ["read", "local_exec"],
                        },
                    ]
                }
            },
        }
    return config


def build_fixture(root: Path, *, registry: bool = True, policy: bool = True) -> None:
    write_json(root / "protocol.config.json", config_with_tool_policy(registry=registry, policy=policy))
    write_json(
        root / "Area_comun/state/PROJECT_STATE.json",
        {"status": "active", "active_tasks": [{"id": TASK_ID, "owner": "Codex", "status": "in_progress"}]},
    )
    write_json(
        root / "Area_comun/state/TASK_INDEX.json",
        {
            "schema_version": "1.0",
            "tasks": [
                {
                    "id": TASK_ID,
                    "owner": "Codex",
                    "status": "in_progress",
                    "type": "implementation",
                    "priority": "high",
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
                    "claim_id": "CLAIM-tool-policy-codex",
                    "task_id": TASK_ID,
                    "owner": "Codex",
                    "status": "active",
                    "scope": [
                        "runtime/",
                        "examples/runtime_tool_policy_cases/",
                        f"Area_comun/tasks/{TASK_ID}.md",
                        f"Area_comun/state/TASK_INDEX.json#{TASK_ID}",
                        f"Area_comun/state/PROJECT_STATE.json#active_tasks/{TASK_ID}",
                        "Area_comun/state/CLAIMS.json",
                    ],
                }
            ],
        },
    )
    task_path = root / "Area_comun/tasks" / f"{TASK_ID}.md"
    task_path.parent.mkdir(parents=True, exist_ok=True)
    task_path.write_text(f"---\nid: {TASK_ID}\nstatus: in_progress\n---\n\n# Fixture\n", encoding="utf-8")
    (root / "Area_comun/mailbox/open").mkdir(parents=True, exist_ok=True)
    schema_target = root / "runtime/turn_schema.json"
    schema_target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / "runtime/turn_schema.json", schema_target)


def turn_report(**overrides) -> dict:
    report = {
        "turn_id": "RUN-tool-policy",
        "task_id": TASK_ID,
        "agent": "Codex",
        "outcome": "ok",
        "summary": "Validate tool policy fixture.",
        "changed_paths": [],
        "transitions": {"claims": [], "mailbox": [], "handoff": None},
        "commit_message": "test(runtime): tool policy fixture",
        "gate": {"human_required": False},
        "next_hint": None,
    }
    report.update(overrides)
    return report


def assert_has(errors: list[str], needle: str) -> None:
    if not any(needle in error for error in errors):
        raise AssertionError({"needle": needle, "errors": errors})


def case_agent_without_tool_permission_is_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-tool-denied-") as temp:
        root = Path(temp)
        build_fixture(root)
        report = turn_report(
            tools=[{"name": "external.deploy", "action_type": "external", "scope": ["runtime/tool_policy.py"]}]
        )
        errors = validate_turn(report, root)
        assert_has(errors, TOOL_DENIED_EVENT)


def case_contract_change_without_decision_refs_fails() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-tool-contract-") as temp:
        root = Path(temp)
        build_fixture(root)
        report = turn_report(
            changed_paths=["runtime/turn_schema.json"],
            actions=[{"type": "contract_change", "summary": "Extend turn report schema"}],
        )
        errors = validate_turn(report, root)
        assert_has(errors, "decision_refs")


def case_sensitive_action_requires_human_gate() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-tool-sensitive-") as temp:
        root = Path(temp)
        build_fixture(root)
        missing_gate = turn_report(actions=[{"type": "sensitive", "summary": "Touch protected credential"}])
        assert_has(validate_turn(missing_gate, root), "gate.human_required")

        paused = turn_report(
            outcome="human_required",
            actions=[{"type": "sensitive", "summary": "Touch protected credential"}],
            gate={"human_required": True, "reason": "sensitive action"},
        )
        assert validate_turn(paused, root) == []
        assert gate_for_action("sensitive")["human_required"] is True


def case_allowed_policy_and_action_type_passes() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-tool-allowed-") as temp:
        root = Path(temp)
        build_fixture(root)
        report = turn_report(
            changed_paths=["runtime/tool_policy.py"],
            tools=[{"name": "local.patch", "action_type": "local_write", "scope": ["runtime/tool_policy.py"]}],
            actions=[{"type": "local_write", "summary": "Edit local runtime file"}],
        )
        assert validate_turn(report, root) == []
        assert classify_action({"summary": "update public API schema"}) == "contract_change"


def case_no_policy_or_no_tools_preserves_legacy_fallback() -> None:
    report = turn_report(changed_paths=[f"Area_comun/tasks/{TASK_ID}.md"])
    with tempfile.TemporaryDirectory(prefix="runtime-tool-legacy-") as left_temp, tempfile.TemporaryDirectory(
        prefix="runtime-tool-policy-empty-"
    ) as right_temp:
        left = Path(left_temp)
        right = Path(right_temp)
        build_fixture(left, registry=False, policy=False)
        build_fixture(right, registry=False, policy=True)
        assert load_agent_registry(left)["source"] == "agent_roles"
        assert validate_turn(report, left) == validate_turn(report, right) == []


def case_determinism() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-tool-determinism-") as temp:
        root = Path(temp)
        build_fixture(root)
        report = turn_report(
            tools=[{"name": "external.deploy", "action_type": "external", "scope": ["runtime/tool_policy.py"]}]
        )
        left = validate_turn(report, root)
        right = validate_turn(report, root)
        assert left == right
        left_hash = hashlib.sha256(json.dumps(left, sort_keys=True).encode("utf-8")).hexdigest()
        right_hash = hashlib.sha256(json.dumps(right, sort_keys=True).encode("utf-8")).hexdigest()
        assert left_hash == right_hash


def main() -> int:
    cases = [
        case_agent_without_tool_permission_is_rejected,
        case_contract_change_without_decision_refs_fails,
        case_sensitive_action_requires_human_gate,
        case_allowed_policy_and_action_type_passes,
        case_no_policy_or_no_tools_preserves_legacy_fallback,
        case_determinism,
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
    print(f"OK: {len(cases)} runtime tool-policy cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
