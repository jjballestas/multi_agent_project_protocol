#!/usr/bin/env python3
"""Runtime budget helpers."""

from __future__ import annotations


class Budget:
    def __init__(self, *, max_iter: int | None = None, max_cost_tokens: int | None = None) -> None:
        self.max_iter = max_iter
        self.max_cost_tokens = max_cost_tokens
        self.turns = 0
        self.cost_tokens = 0
        self.reason: str | None = None

    def consume(self, *, cost_tokens: int | None = None) -> None:
        self.turns += 1
        if cost_tokens is not None:
            self.cost_tokens += cost_tokens

    def exceeded(self) -> bool:
        if self.max_iter is not None and self.turns >= self.max_iter:
            self.reason = "max_iter"
            return True
        if self.max_cost_tokens is not None and self.cost_tokens >= self.max_cost_tokens:
            self.reason = "max_cost_tokens"
            return True
        return False
