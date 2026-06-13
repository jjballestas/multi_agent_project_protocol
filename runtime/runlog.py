#!/usr/bin/env python3
"""JSONL run log helpers for runtime orchestrator runs."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def deterministic_run_id(parts: list[str]) -> str:
    digest = hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()[:12]
    return f"RUN-{digest}"


class RunLog:
    def __init__(self, root: Path, run_id: str | None = None) -> None:
        self.root = root.resolve()
        self.run_id = run_id or deterministic_run_id(["default"])
        self.path = self.root / "runtime" / "runs" / f"{self.run_id}.jsonl"
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def append(self, entry: dict[str, Any]) -> None:
        payload = {"run_id": self.run_id, **entry}
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n")

    def entries(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        entries: list[dict[str, Any]] = []
        for line in self.path.read_text(encoding="utf-8-sig").splitlines():
            if not line.strip():
                continue
            entries.append(json.loads(line))
        return entries

    def task_entries(self, task_id: str) -> list[dict[str, Any]]:
        return [entry for entry in self.entries() if str(entry.get("task_id") or "") == task_id]

    def compacted_context(
        self,
        *,
        task_id: str,
        recent_limit: int,
        consolidation_tool_call_count: int | None = None,
        accumulated_token_limit: int | None = None,
    ) -> dict[str, Any]:
        entries = self.task_entries(task_id)
        summaries = [distilled_turn_summary(entry) for entry in entries if distilled_turn_summary(entry).get("summary")]
        old = summaries[:-recent_limit] if recent_limit > 0 else summaries
        recent = summaries[-recent_limit:] if recent_limit > 0 else []
        tool_result_count = sum(int(entry.get("tool_result_count") or 0) for entry in entries)
        accumulated_tokens = sum(int(entry.get("summary_tokens") or 0) for entry in entries)
        triggered_by: list[str] = []
        if old:
            triggered_by.append("recent_turn_summaries")
        if consolidation_tool_call_count is not None and tool_result_count >= consolidation_tool_call_count:
            triggered_by.append("tool_results")
        if accumulated_token_limit is not None and accumulated_tokens >= accumulated_token_limit:
            triggered_by.append("tokens")
        rolling = rolling_summary_for(task_id=task_id, summaries=old, run_log=str(self.path)) if old or triggered_by else None
        return {
            "recent": recent,
            "rolling_summary": rolling,
            "triggered": bool(triggered_by),
            "triggered_by": triggered_by,
            "tool_result_count": tool_result_count,
            "accumulated_tokens": accumulated_tokens,
            "run_log": str(self.path),
        }


def summary_token_count(text: str, divisor: int = 4) -> int:
    return len(str(text or "")) // max(int(divisor or 4), 1)


def distilled_turn_summary(entry: dict[str, Any]) -> dict[str, Any]:
    summary = str(entry.get("summary") or "").strip()
    if not summary:
        return {}
    return {
        "turn": entry.get("turn"),
        "summary": summary,
        "changed_paths": list(entry.get("changed_paths") or []),
        "run_log": entry.get("run_id"),
    }


def rolling_summary_for(*, task_id: str, summaries: list[dict[str, Any]], run_log: str) -> dict[str, Any]:
    text = " ".join(str(item.get("summary") or "").strip() for item in summaries if item.get("summary")).strip()
    paths: list[str] = []
    for item in summaries:
        for path in item.get("changed_paths") or []:
            text_path = str(path or "").strip()
            if text_path and text_path not in paths:
                paths.append(text_path)
    return {
        "task_id": task_id,
        "summary": text,
        "changed_paths": paths,
        "source_turns": [item.get("turn") for item in summaries if item.get("turn") is not None],
        "run_log": run_log,
    }


def turn_entry(
    *,
    turn: int,
    trace: list[str],
    unit: dict[str, Any] | None = None,
    report: dict[str, Any] | None = None,
    outcome: str | None = None,
    transition: dict[str, Any] | None = None,
    gate_green: bool | None = None,
    commit: str | None = None,
    reverted: bool = False,
    reason: str | None = None,
    errors: list[str] | None = None,
    duration_ms: int = 0,
    collision_avoided: int | bool = 0,
) -> dict[str, Any]:
    report = report or {}
    cost = report.get("cost")
    if isinstance(cost, int):
        cost = {"tokens": cost}
    summary = str(report.get("summary") or "")
    tools = report.get("tools") if isinstance(report.get("tools"), list) else []
    return {
        "turn": turn,
        "unit": unit,
        "agent": report.get("agent"),
        "task_id": report.get("task_id") or (unit or {}).get("task_id") or "none",
        "outcome": outcome or report.get("outcome"),
        "transition": transition,
        "gate_green": gate_green,
        "commit": commit,
        "reverted": reverted,
        "reason": reason,
        "errors": errors or [],
        "trace": trace,
        "changed_paths": list(report.get("changed_paths") or []),
        "summary": summary or None,
        "summary_tokens": summary_token_count(summary),
        "tool_result_count": len(tools),
        "cost": cost,
        "duration_ms": duration_ms,
        "collision_avoided": collision_avoided,
    }
