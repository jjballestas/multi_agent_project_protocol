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
