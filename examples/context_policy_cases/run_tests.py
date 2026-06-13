#!/usr/bin/env python3
"""Golden cases for SPEC-0078 context policy."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import uuid
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from runtime.adapters.base import ContextPack  # noqa: E402
from runtime.orchestrator import (  # noqa: E402
    build_turn_context,
    context_policy,
    delegate_subagent,
    validate_task_close_summary,
)
from runtime.runlog import RunLog, turn_entry  # noqa: E402
from scripts.measure_context_cost import measure  # noqa: E402


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=True, sort_keys=True) + "\n", encoding="ascii", newline="\n")


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="ascii", newline="\n")


def base_config(*, compaction: bool = True, subagents: bool = False, warn_tokens: int | None = None) -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "token_cost": {
            "chars_per_token": 4,
            "coldstart_globs": [
                "AGENTS.md",
                "Area_comun/README.md",
                "Area_comun/protocol/TASK_PROTOCOL.md",
                "Area_comun/state/PROJECT_STATE.slim.json",
                "Area_comun/state/TASK_INDEX.slim.json",
                "Area_comun/state/CLAIMS.slim.json",
            ],
        },
        "runtime": {
            "enabled": True,
            "context_policy": {
                "compaction_enabled": compaction,
                "recent_turn_summaries": 2,
                "task_close_summary_max_tokens": 20,
                "subagents_enabled": subagents,
                "subagent_summary_max_tokens": 5,
                "assembled_context_warn_tokens": warn_tokens,
                "consolidation_trigger": "min(time, volume, tokens)",
                "consolidation_interval_minutes": 30,
                "consolidation_tool_call_count": 2,
                "consolidation_overhead_budget_pct": 5,
            },
        },
    }


def task() -> dict[str, Any]:
    return {
        "id": "TASK-9000",
        "status": "ready",
        "owner": "Codex",
        "phase": "P2",
        "priority": "normal",
        "title": "Context policy fixture",
        "spec_id": "Area_comun/specs/SPEC-9000.md",
        "linked_decisions": ["DECISION-9000"],
        "deliverables": ["runtime/orchestrator.py"],
    }


def unit() -> dict[str, Any]:
    return {"task_id": "TASK-9000", "owner": "Codex", "action": "implement"}


def make_repo(*, compaction: bool = True, subagents: bool = False, warn_tokens: int | None = None) -> Path:
    root = ROOT / ".tmp" / f"context-policy-case-{uuid.uuid4().hex}"
    root.mkdir(parents=True)
    write_text(root / "AGENTS.md", "agents\n")
    write_text(root / "Area_comun/README.md", "readme\n")
    write_text(root / "Area_comun/protocol/TASK_PROTOCOL.md", "task protocol\n")
    write_text(root / "Area_comun/specs/SPEC-9000.md", "spec content\n")
    write_json(root / "protocol.config.json", base_config(compaction=compaction, subagents=subagents, warn_tokens=warn_tokens))
    full_task = {**task(), "review": "full task detail " * 80}
    write_json(root / "Area_comun/state/TASK_INDEX.json", {"schema_version": "1.0", "tasks": [full_task]})
    write_json(
        root / "Area_comun/state/PROJECT_STATE.json",
        {"status": "active", "active_tasks": [{"id": "TASK-9000", "status": "ready", "notes": "full project detail " * 80}]},
    )
    write_json(root / "Area_comun/state/CLAIMS.json", {"schema_version": "1.0", "claims": [{"claim_id": "CLAIM-OLD", "status": "released", "notes": "released detail " * 80}]})
    write_json(root / "Area_comun/state/TASK_INDEX.slim.json", {"schema_version": "1.0", "tasks": [task()]})
    write_json(root / "Area_comun/state/PROJECT_STATE.slim.json", {"status": "active", "active_tasks": [{"id": "TASK-9000", "status": "ready"}]})
    write_json(root / "Area_comun/state/CLAIMS.slim.json", {"schema_version": "1.0", "claims": []})
    write_text(root / "runtime/state/events.jsonl", "{\"raw\":\"event\"}\n")
    return root


def cleanup(root: Path) -> None:
    shutil.rmtree(root, ignore_errors=True)


def state(root: Path) -> dict[str, Any]:
    return {"task_index": json.loads((root / "Area_comun/state/TASK_INDEX.json").read_text(encoding="ascii"))}


def append_turn(runlog: RunLog, turn: int, summary: str, *, raw: str = "", tools: int = 0) -> None:
    report = {
        "task_id": "TASK-9000",
        "agent": "Codex",
        "outcome": "done",
        "summary": summary,
        "changed_paths": [f"file-{turn}.md"],
        "tools": [{"name": f"tool-{index}", "raw": raw} for index in range(tools)],
        "stdout": raw,
    }
    runlog.append(turn_entry(turn=turn, trace=["adapter"], unit=unit(), report=report))


def context(root: Path, runlog: RunLog | None = None) -> ContextPack:
    config = json.loads((root / "protocol.config.json").read_text(encoding="ascii"))
    return build_turn_context(root=root, state=state(root), unit=unit(), replay_report_path=None, turn_index=4, config=config, runlog=runlog)


def gc_1_compact_assembly_sources() -> None:
    root = make_repo()
    try:
        runlog = RunLog(root, "RUN-context-gc1")
        for index in range(1, 6):
            append_turn(runlog, index, f"summary {index}")
        ctx = context(root, runlog)
        assert "Area_comun/state/TASK_INDEX.json" not in ctx.context_sources
        assert "runtime/state/events.jsonl" not in ctx.context_sources
        assert "Area_comun/state/TASK_INDEX.slim.json" in ctx.context_sources
        assert [item["summary"] for item in ctx.turn_summaries] == ["summary 4", "summary 5"]
    finally:
        cleanup(root)


def gc_2_tool_result_clearing() -> None:
    root = make_repo()
    try:
        runlog = RunLog(root, "RUN-context-gc2")
        append_turn(runlog, 1, "small summary", raw="RAW_TOOL_OUTPUT_SHOULD_NOT_RETURN", tools=1)
        ctx = context(root, runlog)
        serialized = json.dumps(list(ctx.turn_summaries), ensure_ascii=False)
        assert "small summary" in serialized
        assert "RAW_TOOL_OUTPUT_SHOULD_NOT_RETURN" not in serialized
    finally:
        cleanup(root)


def gc_3_rolling_summary() -> None:
    root = make_repo()
    try:
        runlog = RunLog(root, "RUN-context-gc3")
        for index in range(1, 5):
            append_turn(runlog, index, f"summary {index}")
        ctx = context(root, runlog)
        assert ctx.rolling_summary is not None
        assert "summary 1" in ctx.rolling_summary["summary"]
        assert "summary 2" in ctx.rolling_summary["summary"]
        assert [item["summary"] for item in ctx.turn_summaries] == ["summary 3", "summary 4"]
    finally:
        cleanup(root)


def gc_4_task_close_summary_gate() -> None:
    root = make_repo()
    try:
        config = json.loads((root / "protocol.config.json").read_text(encoding="ascii"))
        report = {"transitions": {"task_status": {"from": "in_progress", "to": "done"}}}
        assert validate_task_close_summary(report, config)
        ok = {**report, "task_close_summary": "short close summary"}
        assert validate_task_close_summary(ok, config) == []
    finally:
        cleanup(root)


def gc_5_subagent_isolated_and_capped() -> None:
    root = make_repo(subagents=True)
    try:
        config = json.loads((root / "protocol.config.json").read_text(encoding="ascii"))
        ctx = context(root)
        result = delegate_subagent(
            subtask={"id": "SUBTASK-1", "summary": "fallback"},
            context_pack=ctx,
            root=root,
            config=config,
            report={"summary": "x" * 200, "changed_paths": ["sub.md"]},
        )
        assert result["ok"] is True
        assert result["truncated"] is True
        assert result["summary_tokens"] <= 5
        disabled = delegate_subagent(subtask={}, context_pack=ctx, root=root, config=base_config(subagents=False))
        assert disabled["reason"] == "subagents_disabled"
    finally:
        cleanup(root)


def gc_6_flags_off_legacy_context() -> None:
    root = make_repo(compaction=False)
    try:
        ctx = context(root)
        assert ctx.context_sources == ()
        assert ctx.turn_summaries == ()
        assert ctx.assembled_context_tokens == 0
        assert context_policy(json.loads((root / "protocol.config.json").read_text(encoding="ascii")))["compaction_enabled"] is False
    finally:
        cleanup(root)


def gc_7_measurement_reports_delta() -> None:
    root = make_repo()
    try:
        result = measure(root)
        turn_context = result["turn_context"]
        assert turn_context["tasks"]
        assert turn_context["total_delta_tokens"] > 0
    finally:
        cleanup(root)


def gc_8_consolidation_trigger() -> None:
    root = make_repo()
    try:
        runlog = RunLog(root, "RUN-context-gc8")
        append_turn(runlog, 1, "first", tools=2)
        append_turn(runlog, 2, "second", tools=1)
        append_turn(runlog, 3, "third", tools=0)
        ctx = context(root, runlog)
        assert ctx.consolidation is not None
        assert ctx.consolidation["triggered"] is True
        assert "tool_results" in ctx.consolidation["triggered_by"]
        assert ctx.rolling_summary is not None
        assert ctx.rolling_summary["run_log"].endswith("RUN-context-gc8.jsonl")
    finally:
        cleanup(root)


def gc_9_warning_threshold_fallback() -> None:
    root = make_repo(warn_tokens=1)
    try:
        runlog = RunLog(root, "RUN-context-gc9")
        append_turn(runlog, 1, "first")
        append_turn(runlog, 2, "second")
        ctx = context(root, runlog)
        assert ctx.compaction_warning is True
        assert ctx.compaction_fallback is True
        assert ctx.assembled_context_tokens > 1
        assert ctx.turn_summaries == ()
        assert ctx.rolling_summary is not None
    finally:
        cleanup(root)


CASES: dict[str, Callable[[], None]] = {
    "GC-1": gc_1_compact_assembly_sources,
    "GC-2": gc_2_tool_result_clearing,
    "GC-3": gc_3_rolling_summary,
    "GC-4": gc_4_task_close_summary_gate,
    "GC-5": gc_5_subagent_isolated_and_capped,
    "GC-6": gc_6_flags_off_legacy_context,
    "GC-7": gc_7_measurement_reports_delta,
    "GC-8": gc_8_consolidation_trigger,
    "GC-9": gc_9_warning_threshold_fallback,
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Run context policy golden cases.")
    parser.add_argument("--golden-case", choices=sorted(CASES))
    args = parser.parse_args()
    selected = [args.golden_case] if args.golden_case else sorted(CASES)
    results = []
    for name in selected:
        try:
            CASES[name]()
            results.append({"case": name, "ok": True})
        except Exception as exc:  # noqa: BLE001 - compact golden failure reporting
            results.append({"case": name, "ok": False, "error": str(exc)})
    print(json.dumps({"passed": sum(1 for item in results if item["ok"]), "total": len(results), "results": results}, indent=2, sort_keys=True))
    return 0 if all(item["ok"] for item in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
