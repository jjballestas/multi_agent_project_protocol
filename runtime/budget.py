#!/usr/bin/env python3
"""Runtime budget helpers."""

from __future__ import annotations

from typing import Any

try:
    from .eventlog import (
        COST_ATTRIBUTION_DEFAULT_CONTEXT_UNIT,
        COST_ATTRIBUTION_DEFAULT_SCHEMA,
        COST_ATTRIBUTION_DEFAULT_UNIT,
        COST_ATTRIBUTION_DIMENSIONS,
        COST_ATTRIBUTION_SUBJECT_KEY,
        canonical_hash,
        cost_attribution_enabled,
    )
except ImportError:  # pragma: no cover - direct script execution
    from eventlog import (
        COST_ATTRIBUTION_DEFAULT_CONTEXT_UNIT,
        COST_ATTRIBUTION_DEFAULT_SCHEMA,
        COST_ATTRIBUTION_DEFAULT_UNIT,
        COST_ATTRIBUTION_DIMENSIONS,
        COST_ATTRIBUTION_SUBJECT_KEY,
        canonical_hash,
        cost_attribution_enabled,
    )


def positive_int(value: Any) -> int | None:
    if value in (None, ""):
        return None
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed >= 0 else None


def budget_settings(config: dict[str, Any] | None) -> dict[str, Any]:
    config = config or {}
    raw = config.get("budget")
    if not isinstance(raw, dict):
        runtime = config.get("runtime") if isinstance(config.get("runtime"), dict) else {}
        raw = runtime.get("budget") if isinstance(runtime.get("budget"), dict) else {}
    if not isinstance(raw, dict) or raw.get("enabled") is not True:
        return {}

    deadlines = raw.get("task_deadlines") if isinstance(raw.get("task_deadlines"), dict) else {}
    return {
        "soft_cost_tokens": positive_int(raw.get("soft_cost_tokens", raw.get("soft_tokens"))),
        "hard_cost_tokens": positive_int(raw.get("hard_cost_tokens", raw.get("hard_tokens"))),
        "task_deadlines": {str(task_id): value for task_id, value in deadlines.items()},
        "max_queue_length": positive_int(raw.get("max_queue_length", raw.get("queue_limit"))),
    }


def responsible(agent_id: str | None = None, task_id: str | None = None) -> dict[str, str]:
    return {
        "agent": str(agent_id or "runtime"),
        "task_id": str(task_id or "none"),
    }


def canonical_subject(dimension: str, subject_id: str) -> dict[str, str]:
    """Build the CANONICAL subject for a dimension from a single typed identifier.

    DECISION-0033 hardening (analista pasada-3 C1): the subject is exactly one structured id per
    dimension (handoff=`{handoff_id}`, decision=`{decision_id}`, agent=`{agent_id}`) -- no prose, no
    variable fields. This guarantees two logically-equal emissions hash identically, so H2's paired
    handoff matching (and the idempotency key) cannot silently break. The payload plane (the actual
    handoff/decision content) is NOT here; it is referenced only by the hash of this subject.
    """
    key = COST_ATTRIBUTION_SUBJECT_KEY.get(str(dimension or ""))
    if key is None:
        raise ValueError(f"invalid cost attribution dimension: {dimension}")
    text = str(subject_id or "").strip()
    if not text:
        raise ValueError(f"cost attribution subject_id is required for dimension {dimension}")
    return {key: text}


def cost_attribution_record(
    *,
    dimension: str,
    actor: str,
    subject_id: str,
    cost_tokens: int,
    cost_unit: str = COST_ATTRIBUTION_DEFAULT_UNIT,
    cost_schema: str = COST_ATTRIBUTION_DEFAULT_SCHEMA,
    context_tokens: int | None = None,
    context_unit: str = COST_ATTRIBUTION_DEFAULT_CONTEXT_UNIT,
    subject_seq: int | None = None,
    task_id: str | None = None,
    decision_id: str | None = None,
    agent_vocabulary: set[str] | None = None,
) -> dict[str, Any]:
    """Build the structured protocol-plane cost-attribution record (no free text).

    Only the metric, the unit/version tags and structured identifiers are kept; the subject is
    referenced by the hash of its CANONICAL form (DECISION-0033). Raises on an unknown dimension so
    callers cannot smuggle arbitrary content into the protocol plane. `cost_tokens` is the PRODUCER's
    total tokens (input context + output generation) spent by `actor` producing the subject;
    `cost_unit`/`cost_schema` make the immutable corpus self-describing (analista pasada-3 C2). If
    `agent_vocabulary` is given, `actor` is restricted to it (non-human agent ids; C3).
    """
    dimension = str(dimension or "")
    if dimension not in COST_ATTRIBUTION_DIMENSIONS:
        raise ValueError(f"invalid cost attribution dimension: {dimension}")
    tokens = positive_int(cost_tokens)
    if tokens is None:
        raise ValueError(f"cost_tokens must be a non-negative integer, got: {cost_tokens!r}")
    unit = str(cost_unit or "").strip()
    schema = str(cost_schema or "").strip()
    if not unit or not schema:
        raise ValueError("cost_unit and cost_schema are required and must be non-empty")
    actor_text = str(actor or "runtime")
    if agent_vocabulary is not None and actor_text not in agent_vocabulary:
        raise ValueError(f"actor outside agent vocabulary: {actor_text!r}")
    context: int | None = None
    if context_tokens is not None:
        context = positive_int(context_tokens)
        if context is None:
            raise ValueError(f"context_tokens must be a non-negative integer, got: {context_tokens!r}")
    record: dict[str, Any] = {
        "dimension": dimension,
        "actor": actor_text,
        "subject_hash": canonical_hash(canonical_subject(dimension, subject_id)),
        "subject_seq": int(subject_seq) if subject_seq is not None else None,
        "cost_tokens": tokens,
        "cost_unit": unit,
        "cost_schema": schema,
        "context_tokens": context,
        "context_unit": str(context_unit or "").strip() or COST_ATTRIBUTION_DEFAULT_CONTEXT_UNIT,
    }
    if task_id:
        record["task_id"] = str(task_id)
    if decision_id:
        record["decision_id"] = str(decision_id)
    return record


def cost_attribution_idempotency_key(record: dict[str, Any]) -> str:
    """Deterministic dedup key: same subject+dimension+actor+seq => one attribution."""
    return ":".join(
        [
            "cost",
            str(record.get("dimension") or ""),
            str(record.get("subject_hash") or ""),
            str(record.get("subject_seq")),
            str(record.get("actor") or ""),
        ]
    )


def attribute_cost(writer: Any, **kwargs: Any) -> dict[str, Any] | None:
    """Build the record and emit it via the event log writer (gated by the flag).

    Production-faithful emission point for the orchestrator/wrapper at turn close: it is called with
    the turn's measured `cost_tokens` and the typed `subject_id` it produced (handoff/decision/agent).
    Returns the emitted event, or None when `metrics.cost_attribution_enabled` is off
    (writer.append_cost_attribution no-ops).
    """
    record = cost_attribution_record(**kwargs)
    return writer.append_cost_attribution(
        dimension=record["dimension"],
        actor_id=record["actor"],
        subject_hash=record["subject_hash"],
        cost_tokens=record["cost_tokens"],
        cost_unit=record["cost_unit"],
        cost_schema=record["cost_schema"],
        context_tokens=record["context_tokens"],
        context_unit=record["context_unit"],
        subject_seq=record["subject_seq"],
        task_id=record.get("task_id"),
        decision_id=record.get("decision_id"),
        idempotency_key=cost_attribution_idempotency_key(record),
    )


class Budget:
    def __init__(
        self,
        *,
        max_iter: int | None = None,
        max_cost_tokens: int | None = None,
        soft_cost_tokens: int | None = None,
        hard_cost_tokens: int | None = None,
        task_deadlines: dict[str, Any] | None = None,
        max_queue_length: int | None = None,
    ) -> None:
        self.max_iter = max_iter
        self.max_cost_tokens = max_cost_tokens
        self.soft_cost_tokens = soft_cost_tokens
        self.hard_cost_tokens = hard_cost_tokens
        self.task_deadlines = {
            str(task_id): int(value)
            for task_id, value in (task_deadlines or {}).items()
            if positive_int(value) is not None
        }
        self.max_queue_length = max_queue_length
        self.turns = 0
        self.cost_tokens = 0
        self.reason: str | None = None
        self.last_event: dict[str, Any] | None = None

    def event(
        self,
        *,
        reason: str,
        consumed: dict[str, int],
        limit: dict[str, int],
        last_responsible: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        return {
            "reason": reason,
            "consumed": consumed,
            "limit": limit,
            "last_responsible": last_responsible or responsible(),
        }

    def soft_warning(self, *, cost_tokens: int | None = None, last_responsible: dict[str, str] | None = None) -> dict[str, Any] | None:
        if self.soft_cost_tokens is None or cost_tokens is None:
            return None
        projected = self.cost_tokens + cost_tokens
        if projected < self.soft_cost_tokens:
            return None
        return self.event(
            reason="soft_cost_tokens",
            consumed={"cost_tokens": projected},
            limit={"cost_tokens": self.soft_cost_tokens},
            last_responsible=last_responsible,
        )

    def hard_event(self, *, cost_tokens: int | None = None, last_responsible: dict[str, str] | None = None) -> dict[str, Any] | None:
        if self.hard_cost_tokens is None or cost_tokens is None:
            return None
        projected = self.cost_tokens + cost_tokens
        if projected < self.hard_cost_tokens:
            return None
        return self.event(
            reason="hard_cost_tokens",
            consumed={"cost_tokens": projected},
            limit={"cost_tokens": self.hard_cost_tokens},
            last_responsible=last_responsible,
        )

    def queue_event(self, *, queue_length: int, last_responsible: dict[str, str] | None = None) -> dict[str, Any] | None:
        if self.max_queue_length is None or queue_length <= self.max_queue_length:
            return None
        return self.event(
            reason="max_queue_length",
            consumed={"queue_length": queue_length},
            limit={"queue_length": self.max_queue_length},
            last_responsible=last_responsible,
        )

    def deadline_event(
        self,
        *,
        task_id: str,
        turn_index: int,
        last_responsible: dict[str, str] | None = None,
    ) -> dict[str, Any] | None:
        deadline = self.task_deadlines.get(str(task_id))
        if deadline is None or turn_index <= deadline:
            return None
        return self.event(
            reason="deadline_turn",
            consumed={"turn": turn_index},
            limit={"deadline_turn": deadline},
            last_responsible=last_responsible,
        )

    def consume(self, *, cost_tokens: int | None = None) -> None:
        self.turns += 1
        if cost_tokens is not None:
            self.cost_tokens += cost_tokens

    def exceeded(self, *, last_responsible: dict[str, str] | None = None) -> bool:
        if self.max_iter is not None and self.turns >= self.max_iter:
            self.reason = "max_iter"
            self.last_event = self.event(
                reason="max_iter",
                consumed={"turns": self.turns},
                limit={"turns": self.max_iter},
                last_responsible=last_responsible,
            )
            return True
        if self.max_cost_tokens is not None and self.cost_tokens >= self.max_cost_tokens:
            self.reason = "max_cost_tokens"
            self.last_event = self.event(
                reason="max_cost_tokens",
                consumed={"cost_tokens": self.cost_tokens},
                limit={"cost_tokens": self.max_cost_tokens},
                last_responsible=last_responsible,
            )
            return True
        return False
