#!/usr/bin/env python3
"""Golden checks for the read-only agent metrics aggregator."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import agent_metrics


def run(cmd: list[str], *, cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True, check=False)


def assert_equal(actual: object, expected: object, label: str) -> None:
    if actual != expected:
        raise AssertionError(f"{label}: expected {expected!r}, got {actual!r}")


def test_fixture(repo: Path) -> None:
    root = repo / "examples" / "agent_metrics_cases"
    result = agent_metrics.aggregate(
        root,
        root / "events.jsonl",
        root / "runtime" / "runs",
        include_hashes=False,
    )
    assert_equal(set(result), {"por_agente", "por_peon", "por_tarea", "fuentes", "read_only"}, "top-level keys")
    assert_equal(result["por_tarea"]["TASK-A"]["lead_time_seconds"], 21600, "TASK-A lead")
    assert_equal(result["por_tarea"]["TASK-A"]["cycle_time_seconds"], 18000, "TASK-A cycle")
    assert_equal(result["por_tarea"]["TASK-A"]["review_cycles"], 1, "TASK-A review cycles")
    assert_equal(result["por_agente"]["agent-a"]["calidad"]["done"], 1, "agent-a done")
    assert_equal(result["por_agente"]["agent-a"]["calidad"]["tasa_aceptacion"], 1.0, "agent-a acceptance")
    assert_equal(result["por_tarea"]["TASK-A"]["tokens_coste"]["revision"], 25, "TASK-A review tokens")
    assert_equal(result["por_agente"]["agent-a"]["tokens_coste"]["autoria"], 100, "agent-a author tokens")
    assert_equal(result["por_agente"]["reviewer-a"]["tokens_coste"]["revision"], 25, "reviewer tokens")
    assert_equal(result["por_agente"]["agent-b"]["calidad"]["rechazadas"], 1, "agent-b rejected")
    assert_equal(result["por_agente"]["agent-b"]["calidad"]["tasa_aceptacion"], 0.0, "agent-b acceptance")
    assert_equal(result["por_peon"]["worker-a"]["modelo"], "model-a", "worker model")
    assert_equal(result["por_peon"]["worker-a"]["tokens_coste"]["autoria"], 100, "worker tokens")


def test_cli_json(repo: Path) -> None:
    root = repo / "examples" / "agent_metrics_cases"
    completed = run(
        [
            sys.executable,
            str(repo / "scripts" / "agent_metrics.py"),
            "--root",
            str(root),
            "--events",
            str(root / "events.jsonl"),
            "--runlogs",
            str(root / "runtime" / "runs"),
        ],
        cwd=repo,
    )
    if completed.returncode != 0:
        raise AssertionError(completed.stderr or completed.stdout)
    payload = json.loads(completed.stdout)
    assert_equal(payload["por_tarea"]["TASK-B"]["tokens_coste"]["total"], 40, "TASK-B cli tokens")


def test_readonly_guard(repo: Path) -> None:
    before = agent_metrics.pinned_hashes(repo)
    completed = run(
        [sys.executable, str(repo / "scripts" / "agent_metrics.py"), "--root", str(repo), "--check-readonly"],
        cwd=repo,
    )
    if completed.returncode != 0:
        raise AssertionError(completed.stderr or completed.stdout)
    payload = json.loads(completed.stdout)
    after = agent_metrics.pinned_hashes(repo)
    assert_equal(before, after, "pinned hashes stable")
    assert_equal(payload["read_only"]["byte_identical"], True, "reported read-only")
    assert_equal(payload["read_only"]["sha256_before"], payload["read_only"]["sha256_after"], "reported hashes")


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    try:
        test_fixture(repo)
        test_cli_json(repo)
        test_readonly_guard(repo)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    print("OK: agent metrics golden checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
