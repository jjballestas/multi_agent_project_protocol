#!/usr/bin/env python3
"""Deterministic replay adapter for runtime tests and dogfooding."""

from __future__ import annotations

import json
from pathlib import Path

try:
    from .base import ContextPack, TurnReport
except ImportError:  # pragma: no cover - direct script execution
    from base import ContextPack, TurnReport


class ReplayAdapter:
    name = "replay"

    def run_turn(self, *, context: ContextPack, root: Path) -> TurnReport:
        if context.replay_report_path is None:
            raise ValueError("replay adapter requires context.replay_report_path")
        path = context.replay_report_path
        if not path.is_absolute():
            path = root / path
        return json.loads(path.read_text(encoding="utf-8-sig"))


def replay_paths(path: Path) -> list[Path]:
    """Return deterministic replay report paths from a file or directory."""

    if path.is_dir():
        return sorted(candidate for candidate in path.glob("*.json") if candidate.is_file())
    return [path]
