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
    from .budget import Budget
    from .context import load_state
    from .metrics import summarize
    from .router import select_next
    from .adapters.base import ContextPack
    from .adapters.replay import ReplayAdapter, replay_paths
    from .apply import apply_gate_and_commit
    from .gate import run_gate
    from .runlog import RunLog, deterministic_run_id, turn_entry
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
    from budget import Budget
    from metrics import summarize
    from runlog import turn_entry


HUMAN_OUTCOMES = {"decision_required", "human_required"}
TURN_SCHEMA_KEYS = {
    "turn_id",
    "task_id",
    "agent",
    "outcome",
    "summary",
    "changed_paths",
    "transitions",
    "commit_message",
    "gate",
    "next_hint",
}


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


def schema_report(report: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in report.items() if key in TURN_SCHEMA_KEYS}


def report_cost_tokens(report: dict[str, Any]) -> int | None:
    cost = report.get("cost")
    if isinstance(cost, int):
        return cost
    if isinstance(cost, dict) and isinstance(cost.get("tokens"), int):
        return cost["tokens"]
    return None


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")


def run_loop(
    root: Path,
    replay_path: Path,
    *,
    once: bool = False,
    max_iter: int | None = None,
    run_id: str | None = None,
    budget_tokens: int | None = None,
    clock_fixed: int = 0,
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
    budget = Budget(max_iter=limit, max_cost_tokens=budget_tokens)
    turns: list[dict[str, Any]] = []

    for index, report_path in enumerate(reports[:limit], start=1):
        trace: list[str] = ["gate_pre"]
        gate_pre = run_gate(root)
        if not gate_pre["green"]:
            entry = turn_entry(turn=index, trace=trace, outcome="stopped", reason="pre-gate failed", duration_ms=clock_fixed)
            entry["gate"] = gate_pre
            runlog.append(entry)
            turns.append(entry)
            break

        state = load_state(root)
        trace.append("route")
        unit = select_next(state)
        if unit is None or unit.get("action") == "escalate":
            entry = turn_entry(
                turn=index,
                trace=trace,
                unit=unit,
                outcome="stopped",
                reason="no runnable unit or human gate",
                duration_ms=clock_fixed,
            )
            runlog.append(entry)
            turns.append(entry)
            break

        trace.append("claim")
        context = build_context(state=state, unit=unit, replay_report_path=report_path, turn_index=index)
        trace.append("adapter")
        report = adapter.run_turn(context=context, root=root)
        clean_report = schema_report(report)
        trace.append("validate")
        errors = validate_turn(clean_report, root)
        if errors:
            entry = turn_entry(
                turn=index,
                trace=trace,
                unit=unit,
                report=report,
                outcome="rejected",
                errors=errors,
                duration_ms=clock_fixed,
            )
            runlog.append(entry)
            turns.append(entry)
            break

        trace.append("human_gate")
        human_gate = clean_report.get("outcome") in HUMAN_OUTCOMES or (clean_report.get("gate") or {}).get("human_required") is True
        if human_gate:
            entry = turn_entry(turn=index, trace=trace, unit=unit, report=report, duration_ms=clock_fixed)
            entry["human_required"] = True
            runlog.append(entry)
            turns.append(entry)
            break

        trace.append("apply")
        result = apply_gate_and_commit(clean_report, root)
        trace.extend(["gate_post", "commit"])
        entry = turn_entry(
            turn=index,
            trace=trace,
            unit=unit,
            report=report,
            transition=(clean_report.get("transitions") or {}).get("task_status"),
            gate_green=result.get("green"),
            commit=result.get("commit"),
            reverted=result.get("reverted", False),
            duration_ms=clock_fixed,
        )
        runlog.append(entry)
        turns.append(entry)
        budget.consume(cost_tokens=report_cost_tokens(report))
        if not result.get("green"):
            break
        if budget.exceeded() and index < len(reports[:limit]):
            budget_entry = turn_entry(
                turn=index + 1,
                trace=["budget"],
                outcome="budget_exhausted",
                reason=budget.reason,
                duration_ms=clock_fixed,
            )
            runlog.append(budget_entry)
            turns.append(budget_entry)
            break

    summary = summarize(runlog.path)
    summary_path = runlog.path.with_suffix(".summary.json")
    write_json(summary_path, summary)
    return {
        "ok": True,
        "run_id": runlog.run_id,
        "run_log": str(runlog.path),
        "summary": str(summary_path),
        "metrics": summary,
        "turns": turns,
    }


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
    parser.add_argument("--budget-tokens", type=int, default=None, help="Maximum declared turn cost in tokens")
    parser.add_argument("--clock-fixed", type=int, default=0, help="Deterministic duration_ms value for tests")
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

    result = run_loop(
        root,
        Path(args.replay_report),
        once=args.once,
        max_iter=args.max_iter,
        run_id=args.run_id,
        budget_tokens=args.budget_tokens,
        clock_fixed=args.clock_fixed,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
