#!/usr/bin/env python3
"""Scratch-only behavioral cases for the turn-zero plan approval gate."""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from copy import deepcopy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.orchestrator import plan_approval_error, render_plan, run_loop


TASK_TEMPLATE = """---
task_id: {task_id}
title: "{title}"
status: ready
owner: Codex
file: Area_comun/tasks/{task_id}-case.md
linked_decisions: [DECISION-PLAN]
required_capability: implementer
intake:
  type: feature
  goal: {goal}
  acceptance:
    - {acceptance}
  verification_cmd:
    - python verify.py
  scope_routes:
    - runtime/
  out_of_scope:
    - none
  risk: {risk}
  estimate: M
---
"""


def write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n", encoding="utf-8")


def make_root(base: Path) -> tuple[Path, dict]:
    root = base / "instance"
    (root / "Area_comun/tasks").mkdir(parents=True)
    (root / "Area_comun/mailbox/open").mkdir(parents=True)
    (root / "runtime/state").mkdir(parents=True)
    config = {
        "runtime": {"enabled": True, "plan_approval": {"enabled": True, "decision_id": "DECISION-PLAN"}},
        "event_state": {"agent_signatures_enabled": False},
        "agent_registry": {
            "enabled": True,
            "agents": [
                {"id": "operador humano", "capabilities": ["human_owner"], "enabled": True},
                {"id": "Codex", "capabilities": ["implementer"], "enabled": True},
            ],
        },
    }
    write_json(root / "protocol.config.json", config)
    write_json(root / "Area_comun/state/PROJECT_STATE.json", {})
    write_json(root / "Area_comun/state/CLAIMS.json", {"claims": []})
    write_json(
        root / "Area_comun/state/TASK_INDEX.json",
        {"tasks": [{"id": "TASK-A", "file": "Area_comun/tasks/TASK-A-case.md", "status": "ready"}]},
    )
    (root / "Area_comun/tasks/TASK-A-case.md").write_text(
        TASK_TEMPLATE.format(task_id="TASK-A", title="Alpha", goal="Original goal", acceptance="Original acceptance", risk="medium"),
        encoding="utf-8",
    )
    return root, config


def approve(root: Path, plan: dict) -> None:
    event = {
        "type": "plan.approved",
        "actor": "operador humano",
        "payload": {"approval_hash": plan["approval_hash"], "render_hash": plan["render_hash"]},
    }
    (root / "runtime/state/events.jsonl").write_text(json.dumps(event) + "\n", encoding="utf-8")


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="runtime-plan-approval-") as temp:
        root, config = make_root(Path(temp))
        original = render_plan(root, decision_id="DECISION-PLAN")
        assert original["units"][0]["goal"] == "Original goal"
        assert original["units"][0]["required_capability"] == "implementer"
        assert plan_approval_error(root, config, original)
        replay = root / "report.json"
        write_json(replay, {"placeholder": True})
        refused = run_loop(root, replay, once=True)
        assert refused["ok"] is False and "turn-zero plan approval required" in refused["reason"]
        cli = subprocess.run(
            [sys.executable, str(ROOT / "runtime/orchestrator.py"), "--root", str(root), "--plan-all", "--plan-decision", "DECISION-PLAN"],
            check=False,
            capture_output=True,
            text=True,
        )
        assert cli.returncode == 0, cli.stderr
        assert json.loads(cli.stdout)["approval_hash"] == original["approval_hash"]

        approve(root, original)
        assert plan_approval_error(root, config, original) is None

        task_path = root / "Area_comun/tasks/TASK-A-case.md"
        task_path.write_text(task_path.read_text(encoding="utf-8").replace("Original goal", "Changed goal"), encoding="utf-8")
        nonmaterial = render_plan(root, decision_id="DECISION-PLAN")
        assert nonmaterial["units"][0]["goal"] == "Changed goal"
        assert nonmaterial["render_hash"] != original["render_hash"]
        assert nonmaterial["approval_hash"] == original["approval_hash"]
        assert plan_approval_error(root, config, nonmaterial) is None

        task_path.write_text(task_path.read_text(encoding="utf-8").replace("Original acceptance", "Changed acceptance"), encoding="utf-8")
        changed_acceptance = render_plan(root, decision_id="DECISION-PLAN")
        assert changed_acceptance["approval_hash"] != original["approval_hash"]
        assert plan_approval_error(root, config, changed_acceptance)

        task_b = TASK_TEMPLATE.format(task_id="TASK-B", title="Beta", goal="Beta goal", acceptance="Beta acceptance", risk="low")
        (root / "Area_comun/tasks/TASK-B-case.md").write_text(task_b, encoding="utf-8")
        index = json.loads((root / "Area_comun/state/TASK_INDEX.json").read_text(encoding="utf-8"))
        index["tasks"].append({"id": "TASK-B", "file": "Area_comun/tasks/TASK-B-case.md", "status": "ready"})
        write_json(root / "Area_comun/state/TASK_INDEX.json", index)
        added_unit = render_plan(root, decision_id="DECISION-PLAN")
        assert [unit["id"] for unit in added_unit["units"]] == ["TASK-A", "TASK-B"]
        assert plan_approval_error(root, config, added_unit)

        risk_root, risk_config = make_root(Path(temp) / "risk")
        risk_plan = render_plan(risk_root, decision_id="DECISION-PLAN")
        approve(risk_root, risk_plan)
        risk_path = risk_root / "Area_comun/tasks/TASK-A-case.md"
        risk_path.write_text(risk_path.read_text(encoding="utf-8").replace("risk: medium", "risk: high"), encoding="utf-8")
        changed_risk = render_plan(risk_root, decision_id="DECISION-PLAN")
        assert plan_approval_error(risk_root, risk_config, changed_risk)

        tampered = deepcopy(original)
        tampered["approval_hash"] = "0" * 64
        assert plan_approval_error(root, config, tampered)

    print("OK: runtime plan projection and turn-zero approval cases passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
