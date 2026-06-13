#!/usr/bin/env python3
"""Vendor-neutral runtime adapter interface."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

TurnReport = dict[str, Any]


@dataclass(frozen=True)
class ContextPack:
    """Minimal context passed from the orchestrator to an agent adapter."""

    unit: dict[str, Any] | None
    task: dict[str, Any] | None
    spec_paths: tuple[str, ...] = ()
    decision_ids: tuple[str, ...] = ()
    replay_report_path: Path | None = None
    turn_index: int = 0
    context_sources: tuple[str, ...] = ()
    turn_summaries: tuple[dict[str, Any], ...] = ()
    rolling_summary: dict[str, Any] | None = None
    context_policy: dict[str, Any] | None = None
    assembled_context_tokens: int = 0
    compaction_warning: bool = False
    compaction_fallback: bool = False
    consolidation: dict[str, Any] | None = None


class AgentAdapter(Protocol):
    name: str

    def run_turn(self, *, context: ContextPack, root: Path) -> TurnReport:
        """Return one turn report conforming to runtime/turn_schema.json."""
