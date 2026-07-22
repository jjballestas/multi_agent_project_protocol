#!/usr/bin/env python3
from __future__ import annotations

import json
import tempfile
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from runtime.improvement_offers import (  # noqa: E402
    Obstacle, evaluate, proposal_id, read_mailbox, record_offers, record_response,
)


def obstacle(delivery: str, root: str, risk: str = "low") -> Obstacle:
    return Obstacle("runtime:RUN.jsonl", delivery, "gate retry", root, "run bounded validation", risk)


def main() -> int:
    empty = {"schema_version": "1.0", "offers": []}

    high = evaluate([obstacle("TURN-1", "Missing bounded gate", "high")], empty)
    assert len(high) == 1 and high[0]["trigger"] == ["recurrence_risk_high"]
    assert "MUST" in high[0]["draft_change"] and high[0]["citations"]

    repeated = evaluate([
        obstacle("TURN-1", "  SAME\tCause "), obstacle("TURN-2", "same cause")
    ], empty)
    assert len(repeated) == 1 and "root_cause_repeated_across_deliveries" in repeated[0]["trigger"]

    registry = {"schema_version": "1.0", "offers": []}
    record_offers(registry, repeated)
    pid = repeated[0]["proposal_id"]
    record_response(registry, pid, "rejected", "MSG-human-reject")
    assert evaluate([obstacle("TURN-1", "same cause"), obstacle("TURN-2", "same cause")], registry) == []
    newer = [obstacle("TURN-1", "same cause"), obstacle("TURN-2", "same cause"), obstacle("TURN-3", "same cause")]
    assert evaluate(newer, registry) == []
    assert len(evaluate(newer, registry, {pid})) == 1

    accepted_registry = {"schema_version": "1.0", "offers": []}
    record_offers(accepted_registry, high)
    record_response(accepted_registry, high[0]["proposal_id"], "accepted", "MSG-human-accept")
    assert accepted_registry["offers"][0]["status"] == "accepted"
    assert evaluate([obstacle("TURN-9", "Missing bounded gate", "high")], accepted_registry) == []

    assert evaluate([obstacle("TURN-1", "isolated low risk")], empty) == []

    with tempfile.TemporaryDirectory() as tmp:
        report = Path(tmp) / "MSG-report.md"
        report.write_text("""---
message_id: MSG-report
task_id: TASK-0001
type: REPORTE
---
obstacles:
  - what: mailbox retry
    root_cause: Shared Cause
    resolution: serialize the write
    recurrence_risk: high
""", encoding="utf-8")
        mailbox_items = read_mailbox(report)
        assert len(mailbox_items) == 1 and mailbox_items[0].source.startswith("mailbox:")
        combined = evaluate([obstacle("TURN-2", "shared cause"), *mailbox_items], empty)
        assert len(combined) == 1 and len(combined[0]["citations"]) == 2

    assert proposal_id("same cause") == pid
    print(json.dumps({"ok": True, "cases": 6, "auto_apply_routes": 0}))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
