#!/usr/bin/env python3
"""Post-hoc metrics for runtime JSONL logs."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def read_entries(run_log_path: Path) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    if not run_log_path.exists():
        return entries
    for line in run_log_path.read_text(encoding="utf-8-sig").splitlines():
        if line.strip():
            entries.append(json.loads(line))
    return entries


def summarize(run_log_path: Path) -> dict[str, Any]:
    entries = read_entries(run_log_path)
    turns_total = len(entries)
    turns_per_task: dict[str, int] = {}
    cost_per_task: dict[str, int] = {}
    green_count = 0
    gate_count = 0
    reverts = 0
    collisions_avoided = 0
    cost_total = 0

    for entry in entries:
        task_id = str(entry.get("task_id") or "none")
        turns_per_task[task_id] = turns_per_task.get(task_id, 0) + 1
        if entry.get("gate_green") is not None:
            gate_count += 1
            if entry.get("gate_green") is True:
                green_count += 1
        if entry.get("reverted") is True:
            reverts += 1
        collision_value = entry.get("collision_avoided") or 0
        collisions_avoided += int(collision_value) if isinstance(collision_value, int) else int(bool(collision_value))
        cost = entry.get("cost")
        if isinstance(cost, dict):
            tokens = cost.get("tokens")
        else:
            tokens = cost
        if isinstance(tokens, int):
            cost_total += tokens
            cost_per_task[task_id] = cost_per_task.get(task_id, 0) + tokens

    gates_green_pct = 100.0 if gate_count == 0 else round((green_count / gate_count) * 100, 2)
    return {
        "run_id": entries[0].get("run_id") if entries else None,
        "turns_total": turns_total,
        "turns_per_task": turns_per_task,
        "gates_green_pct": gates_green_pct,
        "reverts": reverts,
        "collisions_avoided": collisions_avoided,
        "cost_total": cost_total,
        "cost_per_task": cost_per_task,
        "duration_ms_total": sum(entry.get("duration_ms") or 0 for entry in entries),
    }
