#!/usr/bin/env python3
"""Behavioral cases for objective post-gate obstacle enforcement."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from runtime.runlog import RunLog, turn_entry  # noqa: E402

FALSIFICATION_CONTRACTS = (
    {
        "id": "NEG-POST-GATE-RED-OBSTACLES",
        "negative": "The real run-log append entrypoint rejects an objective red gate with empty obstacles.",
        "mutation": 'mutant = source.replace("        validate_post_gate_obstacles(entry)\\n", "")',
        "boundaries": (
            'assert "gate_green:false" in message and "non-empty obstacles" in message, message',
            'assert accepted[0]["gate_green"] is False',
        ),
        "exercised_by": "main",
    },
)


def entry(*, gate_green: bool, obstacles: object = None, include_obstacles: bool = True) -> dict[str, object]:
    report: dict[str, object] = {"task_id": "TASK-SCRATCH", "agent": "Codex", "outcome": "ok"}
    if include_obstacles:
        report["obstacles"] = obstacles
    return turn_entry(turn=1, trace=["apply", "gate_post"], report=report, gate_green=gate_green)


def append_with(run_log_type: type[RunLog], payload: dict[str, object]) -> list[dict[str, object]]:
    with tempfile.TemporaryDirectory(prefix="post-gate-runlog-") as temp:
        log = run_log_type(Path(temp), "RUN-POST-GATE")
        log.append(payload)
        return log.entries()


def main() -> int:
    """PERMANENT_NEGATIVE: NEG-POST-GATE-RED-OBSTACLES"""
    for payload in (entry(gate_green=False, obstacles=[]), entry(gate_green=False, include_obstacles=False)):
        try:
            append_with(RunLog, payload)
        except ValueError as exc:
            message = str(exc)
            assert "gate_green:false" in message and "non-empty obstacles" in message, message
        else:
            raise AssertionError("red gate with empty or absent obstacles was accepted")

    populated = [{"category": "gate", "description": "quality gate failed"}]
    assert append_with(RunLog, entry(gate_green=False, obstacles=populated))[0]["obstacles"] == populated
    assert append_with(RunLog, entry(gate_green=True, include_obstacles=False))[0]["gate_green"] is True

    source = (ROOT / "runtime" / "runlog.py").read_text(encoding="utf-8")
    mutant = source.replace("        validate_post_gate_obstacles(entry)\n", "")
    assert mutant != source, "mutation did not remove the post-gate enforcement call"
    with tempfile.TemporaryDirectory(prefix="post-gate-mutant-") as temp:
        module_path = Path(temp) / "runlog_mutant.py"
        module_path.write_text(mutant, encoding="utf-8")
        spec = importlib.util.spec_from_file_location("runlog_mutant", module_path)
        assert spec and spec.loader
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        accepted = append_with(module.RunLog, entry(gate_green=False, obstacles=[]))
        assert accepted[0]["gate_green"] is False
    print("OK: real run-log append rejects red-gate empty obstacles; green gate stays narration-free; mutant is killed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
