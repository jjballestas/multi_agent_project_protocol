#!/usr/bin/env python3
"""Local behavioral probes for TASK-0343 remediation 1."""

from __future__ import annotations

import importlib.util
import shutil
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
RUNNER_CASES = ROOT / "examples/mailbox_retry_cases/run_mailbox_retry_cases.py"
PRODUCTION_RUNNER = ROOT / "scripts/harness/peer_mailbox_cron.ps1"
SCRATCH_PARENT = Path("D:/Aegis_Scratch/multi_agent_project_protocol")


def load_module(source: str, name: str):
    namespace = {
        "__file__": str(RUNNER_CASES),
        "__name__": name,
        "__package__": None,
    }
    exec(compile(source, str(RUNNER_CASES), "exec"), namespace)
    return namespace


def expect_property_mutant_to_die(label: str, source: str) -> None:
    namespace = load_module(source, f"task0343_{label}")
    try:
        namespace["run_rollback_ledger_preservation_property"]()
    except AssertionError:
        print(f"{label}: exit 1 (expected)")
        return
    raise AssertionError(f"{label}: mutant survived")


def main() -> int:
    source = RUNNER_CASES.read_text(encoding="utf-8")
    mp4 = source.replace(" and after_claims == before_claims", "", 1)
    assert mp4 != source, "mp4 mutation did not apply"
    expect_property_mutant_to_die("mp4_claims_ignored", mp4)

    original_return = (
        "return bool(before_events) and after_events == before_events "
        "and after_claims == before_claims"
    )
    mp5 = source.replace(
        original_return,
        "return after_events == before_events and after_claims == before_claims",
        1,
    )
    assert mp5 != source, "mp5 mutation did not apply"
    expect_property_mutant_to_die("mp5_empty_accepted", mp5)

    spec = importlib.util.spec_from_file_location("task0343_mp6", RUNNER_CASES)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    production = PRODUCTION_RUNNER.read_text(encoding="utf-8-sig")
    mp6 = production.replace(
        "reason=ledger_unreadable_after_exec",
        "reason=ledger_head_unreadable_after_exec",
        1,
    )
    assert mp6 != production, "mp6 mutation did not apply"
    SCRATCH_PARENT.mkdir(parents=True, exist_ok=True)
    fixture = Path(tempfile.mkdtemp(prefix="task0343-mp6-", dir=SCRATCH_PARENT))
    try:
        mutant_runner = fixture / "peer_mailbox_cron.ps1"
        mutant_runner.write_text(mp6, encoding="utf-8")
        module.RUNNER = mutant_runner
        result = module.main()
        assert result == 0, f"mp6 returned {result}"
        print("mp6_reason_renamed: exit 0 (expected)")
    finally:
        shutil.rmtree(fixture, ignore_errors=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
