#!/usr/bin/env python3
"""Runtime orchestrator entry point.

--plan is read-only. --run is opt-in via protocol.config.json runtime.enabled
and executes deterministic replay turns in M1.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

try:
    from .context import load_state
    from .router import select_next
    from .adapters.base import ContextPack
    from .adapters.replay import ReplayAdapter, replay_paths
    from .apply import apply_gate_and_commit
    from .gate import run_gate
    from .runlog import RunLog, deterministic_run_id
    from .turn_validate import validate_turn
except ImportError:  # pragma: no cover - direct script execution
    from context import load_state
    from router import select_next
    from adapters.base import ContextPack
    from adapters.replay import ReplayAdapter, replay_paths
    from apply import apply_gate_and_commit
    from gate import run_gate
    from runlog import RunLog, deterministic_run_id
    from turn_validate import validate_turn


HUMAN_OUTCOMES = {"decision_required", "human_required"}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def runtime_enabled(root: Path) -> bool:
    config = read_json(root / "protocol.config.json")
    runtime = config.get("runtime") or {}
    return runtime.get("enabled") is True


def task_for_unit(state: dict[str, Any], unit: dict[str, Any] | None) -> dict[str, Any] | None:
    if not unit:
        return None
    task_id = unit.get("task_id")
    for task in state.get("task_index", {}).get("tasks") or []:
        if task.get("id") == task_id:
            return task
    return None


def build_context(
    *,
    state: dict[str, Any],
    unit: dict[str, Any] | None,
    replay_report_path: Path,
    turn_index: int,
) -> ContextPack:
    task = task_for_unit(state, unit)
    spec_paths = tuple([str(task.get("spec_id"))] if task and task.get("spec_id") else [])
    decision_ids = tuple(task.get("linked_decisions") or []) if task else ()
    return ContextPack(
        unit=unit,
        task=task,
        spec_paths=spec_paths,
        decision_ids=decision_ids,
        replay_report_path=replay_report_path,
        turn_index=turn_index,
    )


def default_run_id(reports: list[Path]) -> str:
    parts = [str(path.as_posix()) for path in reports]
    for path in reports:
        if path.exists() and path.is_file():
            parts.append(path.read_text(encoding="utf-8-sig"))
    return deterministic_run_id(parts)


def run_loop(
    root: Path,
    replay_path: Path,
    *,
    once: bool = False,
    max_iter: int | None = None,
    run_id: str | None = None,
) -> dict[str, Any]:
    root = root.resolve()
    if not runtime_enabled(root):
        return {"ok": False, "reason": "runtime.enabled is false; --run is disabled"}

    reports = replay_paths(replay_path)
    if not reports:
        return {"ok": False, "reason": f"no replay reports found: {replay_path}"}

    limit = 1 if once else (max_iter if max_iter is not None else len(reports))
    if limit < 1:
        return {"ok": False, "reason": "--max-iter must be >= 1"}

    adapter = ReplayAdapter()
    runlog = RunLog(root, run_id=run_id or default_run_id(reports[:limit]))
    turns: list[dict[str, Any]] = []

    for index, report_path in enumerate(reports[:limit], start=1):
        gate_pre = run_gate(root)
        if not gate_pre["green"]:
            entry = {"turn": index, "outcome": "stopped", "reason": "pre-gate failed", "gate": gate_pre}
            runlog.append(entry)
            turns.append(entry)
            break

        state = load_state(root)
        unit = select_next(state)
        if unit is None or unit.get("action") == "escalate":
            entry = {"turn": index, "unit": unit, "outcome": "stopped", "reason": "no runnable unit or human gate"}
            runlog.append(entry)
            turns.append(entry)
            break

        context = build_context(state=state, unit=unit, replay_report_path=report_path, turn_index=index)
        report = adapter.run_turn(context=context, root=root)
        errors = validate_turn(report, root)
        if errors:
            entry = {"turn": index, "unit": unit, "outcome": "rejected", "errors": errors}
            runlog.append(entry)
            turns.append(entry)
            break

        human_gate = report.get("outcome") in HUMAN_OUTCOMES or (report.get("gate") or {}).get("human_required") is True
        if human_gate:
            entry = {
                "turn": index,
                "unit": unit,
                "agent": report.get("agent"),
                "task_id": report.get("task_id"),
                "outcome": report.get("outcome"),
                "human_required": True,
                "commit": None,
            }
            runlog.append(entry)
            turns.append(entry)
            break

        result = apply_gate_and_commit(report, root)
        entry = {
            "turn": index,
            "unit": unit,
            "agent": report.get("agent"),
            "task_id": report.get("task_id"),
            "outcome": report.get("outcome"),
            "transition": (report.get("transitions") or {}).get("task_status"),
            "gate_green": result.get("green"),
            "commit": result.get("commit"),
            "reverted": result.get("reverted", False),
        }
        runlog.append(entry)
        turns.append(entry)
        if not result.get("green"):
            break

    return {"ok": True, "run_id": runlog.run_id, "run_log": str(runlog.path), "turns": turns}


def main() -> int:
    parser = argparse.ArgumentParser(description="Protocol runtime orchestrator.")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--plan", action="store_true", help="Dry-run: print next action without mutating state")
    parser.add_argument("--run", action="store_true", help="Execute deterministic runtime turns")
    parser.add_argument("--once", action="store_true", help="Execute exactly one turn")
    parser.add_argument("--max-iter", type=int, default=None, help="Maximum turns to execute")
    parser.add_argument("--adapter", choices=["replay"], default="replay")
    parser.add_argument("--replay-report", help="Replay report JSON file or directory")
    parser.add_argument("--run-id", help="Deterministic run-log id; defaults to a replay-input hash")
    args = parser.parse_args()

    if args.plan and args.run:
        parser.error("choose either --plan or --run")
    if not args.plan and not args.run:
        parser.error("choose --plan or --run")

    root = Path(args.root).resolve()

    if args.plan:
        result = select_next(load_state(root))
        print(json.dumps({"dry_run": True, "next": result}, indent=2, ensure_ascii=False))
        return 0

    if args.adapter != "replay":
        parser.error("M1 only supports the replay adapter")
    if not args.replay_report:
        parser.error("--run requires --replay-report in M1")

    result = run_loop(root, Path(args.replay_report), once=args.once, max_iter=args.max_iter, run_id=args.run_id)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
