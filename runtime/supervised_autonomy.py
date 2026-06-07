#!/usr/bin/env python3
"""Supervised-autonomy activation and run-report helpers."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def runtime_config(config: dict[str, Any] | None) -> dict[str, Any]:
    if not isinstance(config, dict):
        return {}
    runtime = config.get("runtime")
    return runtime if isinstance(runtime, dict) else {}


def supervised_autonomy_config(config: dict[str, Any] | None) -> dict[str, Any]:
    raw = runtime_config(config).get("supervised_autonomy")
    return raw if isinstance(raw, dict) else {}


def max_turns_value(raw: Any) -> int | None:
    if isinstance(raw, bool):
        return None
    if isinstance(raw, int):
        return raw if raw >= 1 else None
    return None


def supervised_autonomy_activation_error(config: dict[str, Any] | None) -> str | None:
    raw = supervised_autonomy_config(config)
    if raw.get("enabled") is not True:
        return "runtime.supervised_autonomy.enabled is not true"

    decision_id = str(raw.get("activation_decision") or raw.get("decision_id") or "").strip()
    approved_by = str(raw.get("approved_by") or raw.get("approver") or "").strip()
    approved_at = str(raw.get("approved_at") or raw.get("ratified_at") or "").strip()
    caps = raw.get("caps") if isinstance(raw.get("caps"), dict) else {}
    max_turns = max_turns_value(caps.get("max_turns"))
    missing = [
        name
        for name, value in (
            ("activation_decision", decision_id),
            ("approved_by", approved_by),
            ("approved_at", approved_at),
        )
        if not value
    ]
    if missing:
        return "runtime.supervised_autonomy missing " + ", ".join(missing)
    if max_turns is None:
        return "runtime.supervised_autonomy.caps.max_turns must be an integer >= 1"
    return None


def supervised_autonomy_payload(config: dict[str, Any]) -> dict[str, Any]:
    raw = supervised_autonomy_config(config)
    caps = raw.get("caps") if isinstance(raw.get("caps"), dict) else {}
    return {
        "enabled": True,
        "activation_decision": str(raw.get("activation_decision") or raw.get("decision_id") or ""),
        "approved_by": str(raw.get("approved_by") or raw.get("approver") or ""),
        "approved_at": str(raw.get("approved_at") or raw.get("ratified_at") or ""),
        "caps": {"max_turns": int(caps.get("max_turns"))},
    }


def turn_cost_tokens(turn: dict[str, Any]) -> int:
    cost = turn.get("cost")
    if isinstance(cost, dict) and isinstance(cost.get("tokens"), int):
        return int(cost["tokens"])
    if isinstance(cost, int):
        return int(cost)
    return 0


def final_outcome(turns: list[dict[str, Any]]) -> str:
    for turn in reversed(turns):
        outcome = str(turn.get("outcome") or "").strip()
        if outcome:
            return outcome
    return "unknown"


def write_run_report(
    path: Path,
    *,
    run_id: str,
    turns: list[dict[str, Any]],
    metrics: dict[str, Any],
    supervision: dict[str, Any],
) -> None:
    lines = [
        f"# Supervised autonomy run report - {run_id}",
        "",
        f"- outcome: {final_outcome(turns)}",
        f"- turns_recorded: {len(turns)}",
        f"- cost_tokens: {metrics.get('cost_total', 0)}",
        f"- duration_ms: {metrics.get('duration_ms_total', 0)}",
        f"- activation_decision: {supervision.get('activation_decision', '')}",
        f"- approved_by: {supervision.get('approved_by', '')}",
        f"- approved_at: {supervision.get('approved_at', '')}",
        f"- caps.max_turns: {(supervision.get('caps') or {}).get('max_turns')}",
        "",
        "## Turns",
        "",
    ]
    for turn in turns:
        commit = str(turn.get("commit") or "")
        reason = str(turn.get("reason") or "")
        errors = "; ".join(str(item) for item in turn.get("errors") or [])
        lines.extend(
            [
                f"- turn: {turn.get('turn')}",
                f"  task_id: {turn.get('task_id')}",
                f"  outcome: {turn.get('outcome')}",
                f"  reason: {reason}",
                f"  cost_tokens: {turn_cost_tokens(turn)}",
                f"  commit: {commit}",
                f"  errors: {errors}",
            ]
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="ascii", newline="\n")
