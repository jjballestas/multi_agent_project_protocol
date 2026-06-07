#!/usr/bin/env python3
"""Runtime budget helpers."""

from __future__ import annotations

from typing import Any


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
