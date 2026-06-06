#!/usr/bin/env python3
"""Golden cases for the N-agent Review/QA state machine."""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from runtime.apply import apply_turn  # noqa: E402
from runtime.review_qa import checks_with_signatures, failure_signature  # noqa: E402
from runtime.router import select_next  # noqa: E402
from runtime.turn_validate import validate_turn  # noqa: E402


TASK_ID = "TASK-9100"


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2), encoding="utf-8")


def agents() -> list[dict]:
    return [
        {"id": "Author", "capabilities": ["implementer", "reviewer", "qa"], "enabled": True},
        {"id": "Reviewer", "capabilities": ["reviewer"], "enabled": True},
        {"id": "QA", "capabilities": ["qa"], "enabled": True},
        {"id": "Architect", "capabilities": ["architect", "orchestrator", "reviewer"], "enabled": True},
    ]


def task(status: str, **extra) -> dict:
    payload = {
        "id": TASK_ID,
        "owner": "Author",
        "author": "Author",
        "status": status,
        "type": "implementation",
        "priority": "high",
        "phase": "P2",
        "file": f"Area_comun/tasks/{TASK_ID}.md",
        "depends_on": [],
        "deliverables": [],
    }
    payload.update(extra)
    return payload


def build_fixture(root: Path, task_payload: dict, actor: str, *, max_qa_cycles: int = 3) -> None:
    write_json(
        root / "protocol.config.json",
        {
            "schema_version": "1.0",
            "agent_registry": {
                "enabled": True,
                "routing_policy": "weighted_least_loaded_deterministic",
                "agents": agents(),
            },
            "routing_weights": {
                "active_claims": 10,
                "pending_reviews": 6,
                "pending_qa": 6,
                "open_fix_cycles": 4,
                "cooldown_penalty": 1,
                "capability_affinity": 1,
            },
            "quality_policy": {"max_qa_cycles": max_qa_cycles},
            "domain_neutrality": {"enabled": False},
            "state_invariants": [{"path": "status", "equals": "active"}],
        },
    )
    write_json(
        root / "Area_comun/state/PROJECT_STATE.json",
        {"status": "active", "active_tasks": [{"id": TASK_ID, "owner": "Author", "status": task_payload["status"]}]},
    )
    write_json(root / "Area_comun/state/TASK_INDEX.json", {"schema_version": "1.0", "tasks": [task_payload]})
    write_json(
        root / "Area_comun/state/CLAIMS.json",
        {
            "schema_version": "1.0",
            "claims": [
                {
                    "claim_id": f"CLAIM-{actor}",
                    "task_id": TASK_ID,
                    "owner": actor,
                    "status": "active",
                    "scope": [
                        f"Area_comun/state/TASK_INDEX.json#{TASK_ID}",
                        f"Area_comun/state/PROJECT_STATE.json#active_tasks/{TASK_ID}",
                    ],
                }
            ],
        },
    )
    task_path = root / "Area_comun/tasks" / f"{TASK_ID}.md"
    task_path.parent.mkdir(parents=True, exist_ok=True)
    task_path.write_text(f"---\nid: {TASK_ID}\nstatus: {task_payload['status']}\n---\n\n# Fixture\n", encoding="utf-8")
    (root / "runtime").mkdir(parents=True, exist_ok=True)
    (root / "runtime/turn_schema.json").write_text((ROOT / "runtime/turn_schema.json").read_text(encoding="utf-8-sig"), encoding="utf-8")
    for folder in ("open", "answered", "archived"):
        (root / "Area_comun/mailbox" / folder).mkdir(parents=True, exist_ok=True)


def check(check_id="unit", error_class="AssertionError", artifact_path="reports/result.txt", log="ts=2026-06-06 id=abc123") -> dict:
    return {
        "check_id": check_id,
        "error_class": error_class,
        "artifact_path": artifact_path,
        "log": log,
    }


def report(actor: str, from_status: str, to_status: str, review_qa: dict) -> dict:
    return {
        "turn_id": f"RUN-{actor}-{from_status}-{to_status}",
        "task_id": TASK_ID,
        "agent": actor,
        "outcome": "done" if to_status == "done" else "ok",
        "summary": "Exercise Review/QA transition.",
        "changed_paths": [],
        "transitions": {
            "task_status": {"from": from_status, "to": to_status},
            "review_qa": review_qa,
            "claims": [],
            "mailbox": [],
            "handoff": None,
        },
        "commit_message": "test(runtime): review qa transition",
        "gate": {"human_required": False},
        "next_hint": None,
    }


def read_task(root: Path) -> dict:
    return json.loads((root / "Area_comun/state/TASK_INDEX.json").read_text())["tasks"][0]


def assert_valid(report_payload: dict, root: Path) -> None:
    errors = validate_turn(report_payload, root)
    assert errors == [], errors


def assert_invalid(report_payload: dict, root: Path, expected: str) -> None:
    errors = validate_turn(report_payload, root)
    if not any(expected in error for error in errors):
        raise AssertionError({"expected": expected, "errors": errors})


def case_fail_qa_records_defect_and_attempt() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-review-qa-fail-") as temp:
        root = Path(temp)
        build_fixture(root, task("qa_pending"), "QA")
        payload = report("QA", "qa_pending", "qa_failed", {"event": "fail_qa", "qa": "QA", "checks_failed": [check()]})
        assert_valid(payload, root)
        apply_turn(payload, root)
        updated = read_task(root)
        assert updated["status"] == "qa_failed"
        assert updated["qa_attempts"] == 1
        assert updated["defect_log"][0]["checks_failed"][0]["failure_signature"]


def case_second_same_signature_goes_to_architect_review() -> None:
    previous = {"event": "fail_qa", "checks_failed": checks_with_signatures([check()])}
    with tempfile.TemporaryDirectory(prefix="runtime-review-qa-loop-") as temp:
        root = Path(temp)
        build_fixture(root, task("qa_pending", qa_attempts=1, defect_log=[previous]), "QA")
        payload = report("QA", "qa_pending", "architect_review", {"event": "fail_qa", "qa": "QA", "checks_failed": [check(log="ts=DIFFERENT id=ffffeeee")]})
        assert_valid(payload, root)
        apply_turn(payload, root)
        updated = read_task(root)
        assert updated["status"] == "architect_review"
        assert updated["quality_escalation_reason"] == "loop_cut"


def case_different_signature_does_not_cut_loop() -> None:
    previous = {"event": "fail_qa", "checks_failed": checks_with_signatures([check(artifact_path="reports/old.txt")])}
    with tempfile.TemporaryDirectory(prefix="runtime-review-qa-different-") as temp:
        root = Path(temp)
        build_fixture(root, task("qa_pending", qa_attempts=1, defect_log=[previous]), "QA")
        payload = report("QA", "qa_pending", "qa_failed", {"event": "fail_qa", "qa": "QA", "checks_failed": [check(artifact_path="reports/new.txt")]})
        assert_valid(payload, root)
        apply_turn(payload, root)
        assert read_task(root)["status"] == "qa_failed"


def case_superficial_log_does_not_change_signature() -> None:
    left = failure_signature(check(log="timestamp=2026-06-06T10:00:00Z trace=abcdef12"))
    right = failure_signature(check(log="timestamp=2026-06-06T11:00:00Z trace=99999999"))
    assert left == right


def case_max_qa_cycles_escalates_to_architect() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-review-qa-max-") as temp:
        root = Path(temp)
        build_fixture(root, task("qa_pending", qa_attempts=1), "QA", max_qa_cycles=1)
        payload = report("QA", "qa_pending", "architect_review", {"event": "fail_qa", "qa": "QA", "checks_failed": [check()]})
        assert_valid(payload, root)
        apply_turn(payload, root)
        updated = read_task(root)
        assert updated["status"] == "architect_review"
        assert updated["quality_escalation_reason"] == "max_qa_cycles"


def case_pass_qa_by_author_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-review-qa-selfqa-") as temp:
        root = Path(temp)
        build_fixture(root, task("qa_pending"), "Author")
        payload = report("Author", "qa_pending", "done", {"event": "pass_qa", "qa": "Author", "evidence": ["reports/qa.md"]})
        assert_invalid(payload, root, "qa actor is task author")


def case_reject_review_by_author_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-review-qa-selfreview-") as temp:
        root = Path(temp)
        build_fixture(root, task("in_review"), "Author")
        payload = report("Author", "in_review", "changes_requested", {"event": "reject_review", "reviewer": "Author", "checks_failed": [check()]})
        assert_invalid(payload, root, "reviewer actor is task author")


def case_done_without_evidence_rejected() -> None:
    with tempfile.TemporaryDirectory(prefix="runtime-review-qa-evidence-") as temp:
        root = Path(temp)
        build_fixture(root, task("qa_pending"), "QA")
        payload = report("QA", "qa_pending", "done", {"event": "pass_qa", "qa": "QA", "evidence": []})
        assert_invalid(payload, root, "pass_qa requires evidence")


def case_router_prefers_original_author_for_fix() -> None:
    state = {
        "task_index": {"tasks": [task("qa_failed", required_capability="implementer")]},
        "claims": {"claims": []},
        "mailbox_open": [],
        "config": {"routing_weights": {"active_claims": 10}},
        "agent_registry": {
            "enabled": True,
            "routing_policy": "weighted_least_loaded_deterministic",
            "agents": agents(),
        },
    }
    selected = select_next(state)
    assert selected["action"] == "assign_fix", selected
    assert selected["owner"] == "Author", selected


def main() -> int:
    cases = [
        case_fail_qa_records_defect_and_attempt,
        case_second_same_signature_goes_to_architect_review,
        case_different_signature_does_not_cut_loop,
        case_superficial_log_does_not_change_signature,
        case_max_qa_cycles_escalates_to_architect,
        case_pass_qa_by_author_rejected,
        case_reject_review_by_author_rejected,
        case_done_without_evidence_rejected,
        case_router_prefers_original_author_for_fix,
    ]
    failures = []
    for case in cases:
        try:
            case()
        except Exception as exc:
            failures.append({"case": case.__name__, "error": str(exc)})
    if failures:
        print(json.dumps({"status": "FAILED", "failures": failures}, indent=2))
        return 1
    print(f"OK: {len(cases)} Review/QA golden cases passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
