#!/usr/bin/env python3
"""Behavioral cases for governed mailbox REPORTE validation."""

from __future__ import annotations

import shutil
import subprocess
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "scripts" / "validate_collaboration_state.py"
MINIMAL = ROOT / "examples" / "minimal_instance"


def report(*, date: str, friction: str | None, obstacles: str | None) -> str:
    fields = [
        "---",
        "type: REPORTE",
        "status: archived",
        "requires_response: false",
        f"date: {date}",
        "task_id: TASK-0261",
    ]
    if friction is not None:
        fields.append(f"friction_count: {friction}")
    fields.extend(["---", "", "Governed TASK-0261 delivery."])
    if obstacles is not None:
        fields.extend(["", f"obstacles: {obstacles}"])
    return "\n".join(fields) + "\n"


NONEMPTY = """\n- what: A retry was required.
  root_cause: The first input was incomplete.
  resolution: The input was corrected and rerun.
  recurrence_risk: low"""


def run_case(name: str, content: str, expected: int, needle: str | None = None) -> None:
    with tempfile.TemporaryDirectory(prefix=f"mailbox-report-{name}-") as temp:
        fixture = Path(temp)
        shutil.copytree(MINIMAL, fixture, dirs_exist_ok=True)
        for state in ("open", "answered", "archived"):
            folder = fixture / "Area_comun" / "mailbox" / state
            folder.mkdir(parents=True, exist_ok=True)
            for stale in folder.glob("MSG-*.md"):
                stale.unlink()
        target = fixture / "Area_comun" / "mailbox" / "archived" / f"MSG-{name}.md"
        target.write_text(content, encoding="utf-8")
        result = subprocess.run(
            ["python", str(VALIDATOR), "--root", str(fixture)],
            text=True,
            capture_output=True,
            check=False,
        )
        assert result.returncode == expected, result.stdout + result.stderr
        if needle:
            assert needle in result.stdout, result.stdout


def main() -> int:
    run_case("zero-empty", report(date="2026-07-22", friction="0", obstacles="[]"), 0)
    run_case("zero-nonempty", report(date="2026-07-22", friction="0", obstacles=NONEMPTY), 0)
    run_case("positive-nonempty", report(date="2026-07-22", friction="2", obstacles=NONEMPTY), 0)
    run_case(
        "positive-empty",
        report(date="2026-07-22", friction="2", obstacles="[]"),
        1,
        "friction_count > 0 but obstacles is empty",
    )
    run_case("grandfathered", report(date="2026-07-21", friction=None, obstacles=None), 0)
    run_case(
        "missing-counter",
        report(date="2026-07-22", friction=None, obstacles="[]"),
        1,
        "requires friction_count as a non-negative integer",
    )
    run_case(
        "malformed-obstacle",
        report(date="2026-07-22", friction="1", obstacles="\n- what: incomplete"),
        1,
        "must contain exactly",
    )
    print("OK: governed mailbox report cases passed (7).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
