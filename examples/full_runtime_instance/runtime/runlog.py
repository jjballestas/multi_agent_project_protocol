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
        "cost": cost,
        "duration_ms": duration_ms,
        "collision_avoided": collision_avoided,
    }
