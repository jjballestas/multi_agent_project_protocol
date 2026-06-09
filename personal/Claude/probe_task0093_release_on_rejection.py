#!/usr/bin/env python3
"""Adversarial probe for TASK-0093 ratification: release-on-rejection.

Reuses the runtime_loop golden fixture helpers. Drives the orchestrator so it
ACQUIRES the routed owner claim (no pre-claim) and THEN the turn is rejected at
the `validate` step (report touches a path outside the acquired claim scope).

Hypothesis (open finding): the freshly-acquired claim is NOT released on the
rejection path -> orphan active claim left in the ledger, breaking the
cero-footprint property the pilot relied on.

This probe runs entirely on tempdir fixtures; it never touches the live ledger.
It is a verdict-evidence probe, NOT a committed golden (a committed golden for the
FIX would assert the claim is released).
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

CASES_DIR = Path(__file__).resolve().parents[2] / "examples" / "runtime_loop_cases"
sys.path.insert(0, str(CASES_DIR))

import run_runtime_loop_cases as g  # type: ignore
import tempfile


def probe_acquired_claim_orphaned_on_validate_rejection() -> dict:
    with tempfile.TemporaryDirectory(prefix="probe-rel-on-rej-") as temp:
        fixture = Path(temp)
        # No pre-claim for TASK-9000 -> orchestrator must ACQUIRE it.
        g.build_fixture(fixture, omit_claims=["TASK-9000"])
        # Report touches AGENTS.md, which is OUTSIDE the acquired claim scope
        # (task_claim_scope does not include AGENTS.md for this fixture task).
        report = g.policy_path_report("TASK-9000")
        report_dir = g.write_reports(fixture, [report])
        before = g.git_count(fixture)
        completed = g.run_orchestrator(
            fixture,
            ["--run", "--once", "--run-id", "RUN-probe-rel-on-rej", "--replay-report", str(report_dir)],
            check=False,
        )
        result = json.loads(completed.stdout)
        turn = result["turns"][0] if result.get("turns") else {}
        claims = json.loads(
            (fixture / "Area_comun/state/CLAIMS.json").read_text(encoding="utf-8-sig")
        )["claims"]
        acquired_rows = [
            c for c in claims if c.get("task_id") == "TASK-9000" and c.get("owner") == "Codex"
        ]
        events_path = fixture / "runtime/state/events.jsonl"
        events = events_path.read_text(encoding="utf-8-sig") if events_path.exists() else ""
        acquire_logged = "orchestrator:claim-acquire:TASK-9000:codex" in events
        return {
            "ok": result.get("ok"),
            "no_commit": g.git_count(fixture) == before,
            "turn_trace": turn.get("trace"),
            "turn_outcome": turn.get("outcome"),
            "turn_errors": turn.get("errors"),
            "acquire_logged": acquire_logged,
            "acquired_claim_rows": acquired_rows,
            "orphan_active": any(c.get("status") == "active" for c in acquired_rows),
        }


def main() -> int:
    out = probe_acquired_claim_orphaned_on_validate_rejection()
    print(json.dumps(out, indent=2))
    print("\n=== VERDICT EVIDENCE ===")
    if out["acquire_logged"] and out["orphan_active"]:
        print("CONFIRMED: orchestrator acquired the claim, turn was rejected, "
              "and the claim was LEFT ACTIVE (orphan).")
    elif out["acquire_logged"] and not out["orphan_active"]:
        print("REFUTED: claim was acquired AND released on rejection (no orphan).")
    else:
        print("INCONCLUSIVE: acquire not logged; rejection happened before acquire. "
              "trace=%s" % out["turn_trace"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
