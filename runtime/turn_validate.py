#!/usr/bin/env python3
"""Validate a runtime turn report against schema and state invariants."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

import jsonschema

ROW_SCOPED_LEDGER_PATHS = {
    "Area_comun/state/TASK_INDEX.json",
    "Area_comun/state/PROJECT_STATE.json",
}


try:
    from .context import active_claims, enabled_agents, has_capability, load_agent_registry, load_state, tasks_by_id
    from .eventlog import EventWriter
    from .guardrails import contain_untrusted, sources_from_turn_report
    from .review_qa import (
        author_of_record,
        checks_with_signatures,
        expected_event,
        has_consecutive_failure,
        max_qa_cycles,
        qa_attempts_after_failure,
    )
except ImportError:  # pragma: no cover - direct script execution
    from context import active_claims, enabled_agents, has_capability, load_agent_registry, load_state, tasks_by_id
    from eventlog import EventWriter
    from guardrails import contain_untrusted, sources_from_turn_report
    from review_qa import (
        author_of_record,
        checks_with_signatures,
        expected_event,
        has_consecutive_failure,
        max_qa_cycles,
        qa_attempts_after_failure,
    )


def load_report(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def normalize_scope(scope: str) -> str:
    return scope.replace("\\", "/").strip()


def split_scope(scope: str) -> tuple[str, str | None]:
    path, separator, selector = normalize_scope(scope).partition("#")
    return path, selector if separator else None


def scope_covers(scope_entry: str, required_entry: str) -> bool:
    scope_path, scope_selector = split_scope(scope_entry)
    required_path, required_selector = split_scope(required_entry)
    if scope_path != required_path:
        if scope_selector is not None or required_selector is not None:
            return False
        return required_path.startswith(scope_path) if scope_path.endswith("/") else required_path == scope_path
    if scope_path in ROW_SCOPED_LEDGER_PATHS:
        if scope_selector is None:
            return True
        return required_selector is not None and scope_selector == required_selector
    if scope_selector is None and required_selector is None:
        return True
    return scope_selector == required_selector


def derive_transition_scopes(report: dict[str, Any]) -> list[str]:
    required: list[str] = []
    transitions = report.get("transitions") or {}
    if isinstance(transitions.get("task_status"), dict) and report.get("task_id"):
        task_id = str(report["task_id"])
        required.append(f"Area_comun/state/TASK_INDEX.json#{task_id}")
        required.append(f"Area_comun/state/PROJECT_STATE.json#active_tasks/{task_id}")
    if transitions.get("claims"):
        required.append("Area_comun/state/CLAIMS.json")
    for mailbox_transition in transitions.get("mailbox") or []:
        if isinstance(mailbox_transition, dict) and mailbox_transition.get("message_id"):
            message_id = str(mailbox_transition["message_id"])
            for folder in ("open", "answered", "archived"):
                required.append(f"Area_comun/mailbox/{folder}/{message_id}.md")
    handoff = transitions.get("handoff")
    if isinstance(handoff, str) and handoff:
        required.append(handoff)
    return required


def required_capability_for_report(report: dict[str, Any]) -> str | None:
    transition = (report.get("transitions") or {}).get("task_status")
    if isinstance(transition, dict):
        from_status = transition.get("from")
        to_status = transition.get("to")
        if from_status == "in_review" and to_status in {"changes_requested", "review_approved", "qa_pending"}:
            return "reviewer"
        if from_status == "in_review" and to_status == "done":
            return "reviewer"
        if from_status == "qa_pending" and to_status in {"qa_failed", "architect_review", "done"}:
            return "qa"
        if from_status in {"qa_failed", "changes_requested"} and to_status == "claimed":
            return "orchestrator"
        if to_status in {"in_review", "done", "blocked"}:
            return "implementer"
        if to_status in {"ready", "claimed", "in_progress"}:
            return "orchestrator"
    if report.get("changed_paths"):
        return "implementer"
    return None


def validate_agent_semantics(report: dict[str, Any], root: Path) -> list[str]:
    errors: list[str] = []
    agent_id = str(report.get("agent") or "")
    registry = load_agent_registry(root)
    agents = {str(agent.get("id")): agent for agent in registry.get("agents") or [] if isinstance(agent, dict)}
    agent = agents.get(agent_id)
    if not agent:
        return [f"semantic: agent not registered: {agent_id}"]
    if agent.get("enabled") is not True:
        errors.append(f"semantic: agent disabled: {agent_id}")
    required = required_capability_for_report(report)
    if required and not has_capability(registry, agent_id, required):
        errors.append(f"semantic: agent {agent_id} lacks required capability: {required}")
    if agent_id not in {str(agent.get("id")) for agent in enabled_agents(registry)}:
        errors.append(f"semantic: agent not enabled: {agent_id}")
    return errors


def validate_concurrency_semantics(report: dict[str, Any], root: Path) -> list[str]:
    errors: list[str] = []
    task_id = str(report.get("task_id") or "")
    if not task_id or task_id == "none":
        return errors
    state = EventWriter(root).state()
    current_version = int(state.get("aggregate_versions", {}).get(task_id) or 0)
    current_fencing = int(state.get("fencing_tokens", {}).get(task_id) or 0)
    if "aggregate_version" in report and int(report["aggregate_version"]) != current_version:
        errors.append(
            "semantic: stale aggregate_version "
            f"for {task_id}: expected {current_version}, found {report['aggregate_version']}"
        )
    if "fencing_token" in report and int(report["fencing_token"]) < current_fencing:
        errors.append(
            "semantic: stale fencing_token "
            f"for {task_id}: expected >= {current_fencing}, found {report['fencing_token']}"
        )
    return errors


def validate_review_qa_semantics(report: dict[str, Any], state: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    transitions = report.get("transitions") or {}
    transition = transitions.get("task_status")
    if not isinstance(transition, dict):
        return errors

    from_status = str(transition.get("from") or "")
    to_status = str(transition.get("to") or "")
    expected = expected_event(from_status, to_status)
    payload = transitions.get("review_qa")
    if expected is None:
        if from_status == "qa_pending" and to_status == "done":
            errors.append("semantic: pass_qa requires Review/QA payload and evidence")
        return errors
    if not isinstance(payload, dict):
        return [f"semantic: Review/QA transition {from_status}->{to_status} requires transitions.review_qa"]
    if payload.get("event") != expected:
        errors.append(
            "semantic: Review/QA event mismatch "
            f"for {from_status}->{to_status}: expected {expected}, found {payload.get('event')}"
        )

    task = tasks_by_id(state).get(report.get("task_id")) or {}
    actor = str(report.get("agent") or "")
    author = author_of_record(task)
    checks = [item for item in payload.get("checks_failed") or [] if isinstance(item, dict)]
    signed_checks = checks_with_signatures(checks)

    if expected in {"reject_review", "approve_review"}:
        reviewer = str(payload.get("reviewer") or actor)
        if reviewer != actor:
            errors.append(f"semantic: reviewer payload must match report agent: {reviewer} != {actor}")
        if actor == author:
            errors.append("semantic: reviewer actor is task author")
    if expected in {"fail_qa", "pass_qa"}:
        qa = str(payload.get("qa") or actor)
        if qa != actor:
            errors.append(f"semantic: qa payload must match report agent: {qa} != {actor}")
        if actor == author:
            errors.append("semantic: qa actor is task author")

    if expected in {"reject_review", "fail_qa"} and not signed_checks:
        errors.append(f"semantic: {expected} requires checks_failed")
    if expected == "pass_qa" and not [item for item in payload.get("evidence") or [] if str(item).strip()]:
        errors.append("semantic: pass_qa requires evidence")

    if expected == "fail_qa" and signed_checks:
        attempts_after = qa_attempts_after_failure(task)
        cycle_limit = max_qa_cycles(state.get("config") or {})
        loop_cut = has_consecutive_failure(task, signed_checks)
        must_escalate = loop_cut or attempts_after > cycle_limit
        if must_escalate and to_status != "architect_review":
            reason = "loop cut" if loop_cut else "max_qa_cycles"
            errors.append(f"semantic: fail_qa must transition to architect_review after {reason}")
        if not must_escalate and to_status == "architect_review":
            errors.append("semantic: architect_review requires loop cut or max_qa_cycles exhaustion")

    return errors


def validate_guardrail_semantics(report: dict[str, Any], root: Path, state: dict[str, Any]) -> list[str]:
    guardrail_result = contain_untrusted(
        report,
        state,
        state.get("agent_registry") or {},
        sources=sources_from_turn_report(report, root),
    )
    return [f"semantic: {error}" for error in guardrail_result.get("errors") or []]


def validate_turn(report: dict[str, Any], root: Path) -> list[str]:
    errors: list[str] = []
    schema = json.loads((root / "runtime" / "turn_schema.json").read_text(encoding="utf-8-sig"))
    try:
        jsonschema.Draft7Validator.check_schema(schema)
        jsonschema.Draft7Validator(schema).validate(report)
    except jsonschema.ValidationError as exc:
        errors.append(f"schema: {exc.message}")
        return errors

    state = load_state(root)
    errors.extend(validate_guardrail_semantics(report, root, state))
    errors.extend(validate_agent_semantics(report, root))
    errors.extend(validate_concurrency_semantics(report, root))
    errors.extend(validate_review_qa_semantics(report, state))
    claims = [
        claim
        for claim in active_claims(state)
        if claim.get("task_id") == report.get("task_id") and claim.get("owner") == report.get("agent")
    ]
    if not claims:
        errors.append("semantic: no active claim for report task_id and agent")
    else:
        claim = claims[0]
        scope = [str(item) for item in claim.get("scope") or []]
        required_entries = [str(item) for item in report.get("changed_paths") or []]
        required_entries.extend(derive_transition_scopes(report))
        for required_entry in required_entries:
            if not any(scope_covers(scope_entry, required_entry) for scope_entry in scope):
                errors.append(f"semantic: write outside active claim scope: {required_entry}")

    transition = (report.get("transitions") or {}).get("task_status")
    if isinstance(transition, dict):
        task = tasks_by_id(state).get(report.get("task_id"))
        current = task.get("status") if task else None
        if transition.get("from") != current:
            errors.append(
                "semantic: stale task_status.from "
                f"for {report.get('task_id')}: expected {current}, found {transition.get('from')}"
            )

    if report.get("outcome") in {"decision_required", "human_required"}:
        gate = report.get("gate") or {}
        if gate.get("human_required") is not True:
            errors.append("semantic: human gate outcome must set gate.human_required=true")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a runtime turn report.")
    parser.add_argument("report", help="Path to a turn report JSON file")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    args = parser.parse_args()
    errors = validate_turn(load_report(Path(args.report)), Path(args.root).resolve())
    if errors:
        print("ERRORS:")
        for error in errors:
            print(f"- {error}")
        return 1
    print("OK: turn report is valid.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
