#!/usr/bin/env python3
"""Golden cases for DECISION-0032/0060: architect/orchestrator closes own lightweight tasks.

The architect (orchestrator) must be able to advance/close ITS OWN type in
{analysis, triage, extraction} tasks to in_review/done/blocked WITHOUT an implementer/qa capability.
Every other task type, and lightweight tasks NOT owned by the actor, keep requiring implementer.
Deterministic, no I/O.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.submit_intent import task_status_capability  # noqa: E402


def state(task_type: str, owner: str) -> dict:
    return {"task_index": {"tasks": [{"id": "TASK-X", "owner": owner, "type": task_type, "status": "in_progress"}]}}


def cap(frm: str, to: str, st: dict, actor: str) -> set:
    return task_status_capability({"task_id": "TASK-X", "from": frm, "to": to}, st, actor)


def gc_1_architect_advances_own_analysis_to_in_review() -> None:
    # in_progress -> in_review on own analysis-task: orchestrator/architect, NOT implementer.
    c = cap("in_progress", "in_review", state("analysis", "Claude"), "Claude")
    assert "orchestrator" in c and "architect" in c
    assert "implementer" not in c


def gc_2_architect_closes_own_analysis_to_done() -> None:
    # Direct in_progress -> done on own analysis-task: orchestrator/architect, NOT implementer.
    c = cap("in_progress", "done", state("analysis", "Claude"), "Claude")
    assert "orchestrator" in c and "implementer" not in c
    # And the standard in_review -> done path stays {reviewer} (unchanged).
    assert cap("in_review", "done", state("analysis", "Claude"), "Claude") == {"reviewer"}


def gc_3_non_analysis_still_requires_implementer() -> None:
    # Implementation task in_progress -> in_review still requires implementer (unchanged).
    assert cap("in_progress", "in_review", state("implementation", "Codex"), "Codex") == {"implementer"}
    assert cap("in_progress", "done", state("implementation", "Codex"), "Codex") == {"implementer"}


def gc_4_analysis_not_owner_still_requires_implementer() -> None:
    # Analysis task NOT owned by the actor: no relaxation, still implementer.
    assert cap("in_progress", "in_review", state("analysis", "Claude"), "Codex") == {"implementer"}


def gc_5_architect_closes_own_triage_and_extraction_to_done() -> None:
    # DECISION-0060: own triage/extraction tasks get the same lightweight close rule as analysis.
    assert cap("in_progress", "done", state("triage", "Arquitecto"), "Arquitecto") == {"orchestrator", "architect"}
    assert cap("in_progress", "done", state("extraction", "Arquitecto"), "Arquitecto") == {"orchestrator", "architect"}


def gc_6_triage_not_owner_still_requires_implementer() -> None:
    # Triage task NOT owned by the actor: no relaxation, still implementer.
    assert cap("in_progress", "done", state("triage", "Arquitecto"), "Codex") == {"implementer"}


def gc_7_product_owned_by_actor_still_requires_implementer() -> None:
    # Product task owned by the actor: no relaxation by ownership alone.
    assert cap("in_progress", "done", state("product", "Arquitecto"), "Arquitecto") == {"implementer"}


def gc_8_reviewer_and_qa_paths_stay_unchanged() -> None:
    assert cap("in_review", "done", state("triage", "Arquitecto"), "Arquitecto") == {"reviewer"}
    assert cap("qa_pending", "done", state("extraction", "Arquitecto"), "Arquitecto") == {"qa"}


CASES = {
    "GC-1": gc_1_architect_advances_own_analysis_to_in_review,
    "GC-2": gc_2_architect_closes_own_analysis_to_done,
    "GC-3": gc_3_non_analysis_still_requires_implementer,
    "GC-4": gc_4_analysis_not_owner_still_requires_implementer,
    "GC-5": gc_5_architect_closes_own_triage_and_extraction_to_done,
    "GC-6": gc_6_triage_not_owner_still_requires_implementer,
    "GC-7": gc_7_product_owned_by_actor_still_requires_implementer,
    "GC-8": gc_8_reviewer_and_qa_paths_stay_unchanged,
}


def main() -> int:
    results = []
    for name in sorted(CASES):
        try:
            CASES[name]()
            results.append({"case": name, "ok": True})
        except Exception as exc:  # noqa: BLE001
            results.append({"case": name, "ok": False, "error": str(exc)})
    print(json.dumps({"passed": sum(1 for r in results if r["ok"]), "total": len(results), "results": results}, indent=2, sort_keys=True))
    return 0 if all(r["ok"] for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
