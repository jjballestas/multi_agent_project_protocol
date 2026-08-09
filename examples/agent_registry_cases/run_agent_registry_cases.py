#!/usr/bin/env python3
"""Golden cases for the N-agent registry resolver and semantic validation."""

from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from runtime.context import agents_with_capability, has_capability, load_agent_registry  # noqa: E402
from runtime.turn_validate import validate_turn  # noqa: E402


TASK_ID = "TASK-0200"


def write_json(path: Path, payload) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def build_fixture(target: Path, config: dict | None = None, *, owner: str = "Codex") -> None:
    (target / "runtime").mkdir(parents=True)
    shutil.copy2(ROOT / "runtime" / "turn_schema.json", target / "runtime" / "turn_schema.json")
    if config is not None:
        write_json(target / "protocol.config.json", config)
    write_json(target / "Area_comun" / "state" / "PROJECT_STATE.json", {"status": "active"})
    write_json(
        target / "Area_comun" / "state" / "TASK_INDEX.json",
        {
            "tasks": [
                {
                    "id": TASK_ID,
                    "owner": owner,
                    "status": "in_progress",
                    "priority": "normal",
                    "file": f"Area_comun/tasks/{TASK_ID}.md",
                }
            ]
        },
    )
    write_json(
        target / "Area_comun" / "state" / "CLAIMS.json",
        {
            "claims": [
                {
                    "claim_id": f"CLAIM-{TASK_ID}-{owner}",
                    "task_id": TASK_ID,
                    "owner": owner,
                    "status": "active",
                    "scope": [
                        "runtime/",
                        f"Area_comun/tasks/{TASK_ID}.md",
                        f"Area_comun/state/TASK_INDEX.json#{TASK_ID}",
                        f"Area_comun/state/PROJECT_STATE.json#active_tasks/{TASK_ID}",
                        "Area_comun/state/CLAIMS.json",
                    ],
                }
            ]
        },
    )
    (target / "Area_comun" / "mailbox" / "open").mkdir(parents=True)


def explicit_registry() -> dict:
    return {
        "agent_registry": {
            "enabled": True,
            "routing_policy": "weighted_least_loaded_deterministic",
            "agents": [
                {"id": "Planner", "capabilities": ["architect", "reviewer"], "enabled": True},
                {"id": "Builder", "capabilities": ["implementer", "test_engineer"], "enabled": True},
                {"id": "DisabledBuilder", "capabilities": ["implementer"], "enabled": False},
                {"id": "ReviewerOnly", "capabilities": ["reviewer"], "enabled": True},
            ],
        }
    }


def agent_roles_config() -> dict:
    return {
        "agent_roles": {
            "architect": "Lead",
            "implementer": "Maker",
            "human_owner": "Owner",
        }
    }


def turn_report(agent: str) -> dict:
    return {
        "turn_id": f"RUN-{TASK_ID}-{agent}",
        "task_id": TASK_ID,
        "agent": agent,
        "outcome": "in_review",
        "summary": f"Move {TASK_ID} to review.",
        "changed_paths": ["runtime/context.py", f"Area_comun/tasks/{TASK_ID}.md"],
        "obstacles": [],
        "transitions": {
            "task_status": {"from": "in_progress", "to": "in_review"},
            "claims": [{"op": "release", "claim_id": f"CLAIM-{TASK_ID}-{agent}"}],
            "mailbox": [],
            "handoff": None,
        },
        "commit_message": "feat(runtime): validate registry agent",
        "gate": {"human_required": False},
        "next_hint": None,
    }


def case_explicit_registry() -> None:
    with tempfile.TemporaryDirectory(prefix="agent-registry-explicit-") as temp:
        root = Path(temp)
        build_fixture(root, explicit_registry(), owner="Builder")
        registry = load_agent_registry(root)
        assert registry["source"] == "agent_registry"
        assert has_capability(registry, "Builder", "implementer")
        assert [agent["id"] for agent in agents_with_capability(registry, "reviewer")] == ["Planner", "ReviewerOnly"]
        assert validate_turn(turn_report("Builder"), root) == []


def case_agent_roles_fallback() -> None:
    with tempfile.TemporaryDirectory(prefix="agent-registry-roles-") as temp:
        root = Path(temp)
        build_fixture(root, agent_roles_config(), owner="Maker")
        registry = load_agent_registry(root)
        assert registry["source"] == "agent_roles"
        assert has_capability(registry, "Lead", "architect")
        assert has_capability(registry, "Lead", "reviewer")
        assert has_capability(registry, "Maker", "implementer")
        assert has_capability(registry, "Owner", "human_owner")


def case_default_fallback() -> None:
    with tempfile.TemporaryDirectory(prefix="agent-registry-default-") as temp:
        root = Path(temp)
        build_fixture(root, None)
        registry = load_agent_registry(root)
        assert registry["source"] == "default"
        assert has_capability(registry, "Claude", "architect")
        assert has_capability(registry, "Claude", "reviewer")
        assert has_capability(registry, "Codex", "implementer")
        assert has_capability(registry, "operador humano", "human_owner")


def case_reject_unregistered_disabled_and_uncapable() -> None:
    with tempfile.TemporaryDirectory(prefix="agent-registry-reject-") as temp:
        root = Path(temp)
        build_fixture(root, explicit_registry(), owner="Builder")
        unregistered = validate_turn({**turn_report("Mystery"), "task_id": TASK_ID}, root)
        disabled = validate_turn({**turn_report("DisabledBuilder"), "task_id": TASK_ID}, root)
        uncapable = validate_turn({**turn_report("ReviewerOnly"), "task_id": TASK_ID}, root)
        assert any("agent not registered" in error for error in unregistered)
        assert any("agent disabled" in error or "agent not enabled" in error for error in disabled)
        assert any("lacks required capability: implementer" in error for error in uncapable)


def main() -> int:
    cases = [
        case_explicit_registry,
        case_agent_roles_fallback,
        case_default_fallback,
        case_reject_unregistered_disabled_and_uncapable,
    ]
    failures = []
    for case in cases:
        try:
            case()
        except Exception as exc:  # noqa: BLE001 - golden harness reports compact failures
            failures.append({"case": case.__name__, "error": str(exc)})
    if failures:
        print(json.dumps({"status": "FAILED", "failures": failures}, indent=2))
        return 1
    print(f"OK: {len(cases)} agent registry golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
