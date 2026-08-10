#!/usr/bin/env python3
"""Runtime orchestrator entry point.

--plan is read-only. --run is opt-in via protocol.config.json runtime.enabled
and executes deterministic replay turns in M1.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    from .budget import Budget, budget_settings, responsible
    from .context import active_claims, load_state, parse_frontmatter
    from .eventlog import read_jsonl_torn_safe, utc_now, verify_actor_auth, verify_event_auth
    from .metrics import summarize
    from .router import select_next
    from .adapters.base import ContextPack
    from .adapters.llm_adapter import (
        LLMAdapter,
        RecordedInvoker,
        SubprocessInvoker,
        real_invoker_activation_error,
        resolve_llm_command,
    )
    from .adapters.replay import ReplayAdapter, replay_paths
    from .apply import apply_gate_and_commit
    from .gate import run_gate
    from .runlog import RunLog, deterministic_run_id, turn_entry
    from .supervised_autonomy import (
        fix_cycle_checkpoint_reason,
        pause_sentinel_path,
        supervised_autonomy_activation_error,
        supervised_autonomy_payload,
        write_run_report,
    )
    from .submit_intent import IntentError, parse_frontmatter_mapping, submit_intent
    from .turn_validate import validate_turn
    from .vcs import VcsError, commit_turn, discard_worktree_changes
except ImportError:  # pragma: no cover - direct script execution
    from context import active_claims, load_state, parse_frontmatter
    from eventlog import read_jsonl_torn_safe, utc_now, verify_actor_auth, verify_event_auth
    from router import select_next
    from adapters.base import ContextPack
    from adapters.llm_adapter import (
        LLMAdapter,
        RecordedInvoker,
        SubprocessInvoker,
        real_invoker_activation_error,
        resolve_llm_command,
    )
    from adapters.replay import ReplayAdapter, replay_paths
    from apply import apply_gate_and_commit
    from gate import run_gate
    from runlog import RunLog, deterministic_run_id
    from turn_validate import validate_turn
    from budget import Budget, budget_settings, responsible
    from metrics import summarize
    from runlog import turn_entry
    from supervised_autonomy import fix_cycle_checkpoint_reason, pause_sentinel_path, supervised_autonomy_activation_error, supervised_autonomy_payload, write_run_report
    from submit_intent import IntentError, parse_frontmatter_mapping, submit_intent
    from vcs import VcsError, commit_turn, discard_worktree_changes


HUMAN_OUTCOMES = {"decision_required", "human_required"}

DEFAULT_CONTEXT_POLICY = {
    "compaction_enabled": False,
    "recent_turn_summaries": 3,
    "task_close_summary_max_tokens": 2000,
    "subagents_enabled": False,
    "subagent_summary_max_tokens": 2000,
    "assembled_context_warn_tokens": None,
    "consolidation_trigger": "min(time, volume, tokens)",
    "consolidation_interval_minutes": 30,
    "consolidation_tool_call_count": 10,
    "consolidation_overhead_budget_pct": 5,
}

FULL_STATE_CONTEXT_PATHS = {
    "Area_comun/state/CLAIMS.json",
    "Area_comun/state/PROJECT_STATE.json",
    "Area_comun/state/TASK_INDEX.json",
    "runtime/state/events.jsonl",
}
SLIM_CONTEXT_PATHS = (
    "AGENTS.md",
    "Area_comun/README.md",
    "Area_comun/protocol/TASK_PROTOCOL.md",
    "Area_comun/state/PROJECT_STATE.slim.json",
    "Area_comun/state/TASK_INDEX.slim.json",
    "Area_comun/state/CLAIMS.slim.json",
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def turn_schema_keys(root: Path) -> frozenset[str]:
    """Return the only keys that the turn validator can accept.

    The schema is the validator's first gate and rejects additional properties.
    Resolve it from the routed root, exactly as validate_turn does, so filtering and
    validation cannot silently use different schema artifacts.
    """
    schema_path = root / "runtime" / "turn_schema.json"
    schema = read_json(schema_path)
    if schema.get("additionalProperties") is not False:
        raise ValueError(
            f"{schema_path}: orchestrator filtering requires additionalProperties=false"
        )
    properties = schema.get("properties")
    if not isinstance(properties, dict):
        raise ValueError(f"{schema_path}: schema must define a properties mapping")
    return frozenset(str(key) for key in properties)


def token_count(text: str, divisor: int = 4) -> int:
    return len(str(text or "")) // max(int(divisor or 4), 1)


def runtime_config(config: dict[str, Any] | None) -> dict[str, Any]:
    runtime = (config or {}).get("runtime")
    return runtime if isinstance(runtime, dict) else {}


def context_policy(config: dict[str, Any] | None) -> dict[str, Any]:
    raw = runtime_config(config).get("context_policy")
    policy = dict(DEFAULT_CONTEXT_POLICY)
    if isinstance(raw, dict):
        policy.update(raw)
    return policy


def positive_int(value: Any, default: int | None = None) -> int | None:
    if value in (None, ""):
        return default
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default
    return parsed if parsed >= 0 else default


def compact_context_sources(config: dict[str, Any] | None) -> tuple[str, ...]:
    token_config = (config or {}).get("token_cost") if isinstance((config or {}).get("token_cost"), dict) else {}
    configured = token_config.get("coldstart_globs") if isinstance(token_config, dict) else None
    sources = list(configured or SLIM_CONTEXT_PATHS)
    clean: list[str] = []
    for source in sources:
        normalized = normalize_scope_path(source)
        if not normalized or normalized in FULL_STATE_CONTEXT_PATHS:
            continue
        if normalized not in clean:
            clean.append(normalized)
    return tuple(clean)


def read_text_if_exists(root: Path, relative: str) -> str:
    path = root / normalize_scope_path(relative)
    if not path.exists() or not path.is_file():
        return ""
    return path.read_text(encoding="utf-8-sig")


def runtime_enabled(root: Path) -> bool:
    config = read_json(root / "protocol.config.json")
    runtime = config.get("runtime") or {}
    return runtime.get("enabled") is True


PLAN_FIELDS = ("id", "goal", "acceptance", "verification_cmd", "required_capability", "risk", "estimate")
PLAN_MATERIAL_FIELDS = ("id", "acceptance", "risk")


def plan_approval_config(config: dict[str, Any] | None) -> dict[str, Any]:
    value = runtime_config(config).get("plan_approval")
    return value if isinstance(value, dict) else {}


def _task_file(root: Path, task: dict[str, Any]) -> Path | None:
    relative = str(task.get("file") or "").strip()
    if relative:
        path = root / relative
        return path if path.is_file() else None
    task_id = str(task.get("id") or "")
    matches = sorted((root / "Area_comun" / "tasks").glob(f"{task_id}-*.md"))
    return matches[0] if len(matches) == 1 else None


def render_plan(root: Path, *, decision_id: str | None = None) -> dict[str, Any]:
    """Project the governed task index and task intake without filling missing values."""
    state = load_state(root)
    units: list[dict[str, Any]] = []
    for task in state.get("task_index", {}).get("tasks") or []:
        path = _task_file(root, task)
        metadata = parse_frontmatter(path) if path else {}
        linked = task.get("linked_decisions") or metadata.get("linked_decisions") or []
        if decision_id and decision_id not in {str(item) for item in linked}:
            continue
        intake = parse_frontmatter_mapping(path, "intake") if path else None
        intake = intake if isinstance(intake, dict) else {}
        units.append(
            {
                "id": task.get("id"),
                "goal": intake.get("goal"),
                "acceptance": intake.get("acceptance"),
                "verification_cmd": intake.get("verification_cmd"),
                "required_capability": task.get("required_capability", metadata.get("required_capability")),
                "risk": intake.get("risk"),
                "estimate": intake.get("estimate"),
            }
        )
    units.sort(key=lambda item: str(item.get("id") or ""))
    material = [{key: unit.get(key) for key in PLAN_MATERIAL_FIELDS} for unit in units]
    encoded = json.dumps(units, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    material_encoded = json.dumps(material, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {
        "decision_id": decision_id,
        "fields": list(PLAN_FIELDS),
        "units": units,
        "render_hash": hashlib.sha256(encoded).hexdigest(),
        "approval_hash": hashlib.sha256(material_encoded).hexdigest(),
        "material_fields": list(PLAN_MATERIAL_FIELDS),
    }


def plan_approval_error(root: Path, config: dict[str, Any], plan: dict[str, Any]) -> str | None:
    """Require an authenticated human plan.approved event for the current material plan."""
    approval = plan_approval_config(config)
    if approval.get("enabled") is not True:
        return None
    expected = str(plan.get("approval_hash") or "")
    registry = load_state(root).get("agent_registry") or {}
    human_actors = {
        str(agent.get("id"))
        for agent in registry.get("agents") or []
        if "human_owner" in {str(cap) for cap in agent.get("capabilities") or []}
    }
    for event in reversed(read_jsonl_torn_safe(root / "runtime" / "state" / "events.jsonl")):
        payload = event.get("payload") if isinstance(event.get("payload"), dict) else {}
        if event.get("type") != "plan.approved" or payload.get("approval_hash") != expected:
            continue
        if str(event.get("actor") or "") not in human_actors:
            continue
        if verify_event_auth(event, config, root=root).get("valid") is not True:
            continue
        if (config.get("event_state") or {}).get("agent_signatures_enabled") is True:
            if verify_actor_auth(event, config, root).get("valid") is not True:
                continue
        return None
    return f"turn-zero plan approval required for approval_hash={expected}; material fields are id, acceptance, risk"


def task_for_unit(state: dict[str, Any], unit: dict[str, Any] | None) -> dict[str, Any] | None:
    if not unit:
        return None
    task_id = unit.get("task_id")
    for task in state.get("task_index", {}).get("tasks") or []:
        if task.get("id") == task_id:
            return task
    return None


def build_context(
    *,
    state: dict[str, Any],
    unit: dict[str, Any] | None,
    replay_report_path: Path | None,
    turn_index: int,
) -> ContextPack:
    task = task_for_unit(state, unit)
    spec_paths = tuple([str(task.get("spec_id"))] if task and task.get("spec_id") else [])
    decision_ids = tuple(task.get("linked_decisions") or []) if task else ()
    return ContextPack(
        unit=unit,
        task=task,
        spec_paths=spec_paths,
        decision_ids=decision_ids,
        replay_report_path=replay_report_path,
        turn_index=turn_index,
    )


def estimate_context_tokens(root: Path, context: ContextPack, *, divisor: int = 4) -> int:
    chunks = [
        json.dumps(context.unit or {}, ensure_ascii=False, sort_keys=True),
        json.dumps(context.task or {}, ensure_ascii=False, sort_keys=True),
        json.dumps(list(context.decision_ids), ensure_ascii=False),
        json.dumps(list(context.turn_summaries), ensure_ascii=False, sort_keys=True),
        json.dumps(context.rolling_summary or {}, ensure_ascii=False, sort_keys=True),
    ]
    for source in context.context_sources:
        chunks.append(read_text_if_exists(root, source))
    for spec_path in context.spec_paths:
        chunks.append(read_text_if_exists(root, spec_path))
    return token_count("\n".join(chunks), divisor)


def build_turn_context(
    *,
    root: Path,
    state: dict[str, Any],
    unit: dict[str, Any] | None,
    replay_report_path: Path | None,
    turn_index: int,
    config: dict[str, Any] | None = None,
    runlog: RunLog | None = None,
) -> ContextPack:
    base = build_context(state=state, unit=unit, replay_report_path=replay_report_path, turn_index=turn_index)
    policy = context_policy(config)
    if policy.get("compaction_enabled") is not True:
        return base

    task_id = str((base.task or {}).get("id") or (unit or {}).get("task_id") or "none")
    recent_limit = positive_int(policy.get("recent_turn_summaries"), 3) or 0
    token_config = (config or {}).get("token_cost") if isinstance((config or {}).get("token_cost"), dict) else {}
    divisor = positive_int((token_config or {}).get("chars_per_token"), 4) or 4
    compacted = (
        runlog.compacted_context(
            task_id=task_id,
            recent_limit=recent_limit,
            consolidation_tool_call_count=positive_int(policy.get("consolidation_tool_call_count")),
            accumulated_token_limit=positive_int(policy.get("assembled_context_warn_tokens")),
        )
        if runlog is not None
        else {"recent": [], "rolling_summary": None, "triggered": False, "triggered_by": []}
    )
    context = ContextPack(
        unit=base.unit,
        task=base.task,
        spec_paths=base.spec_paths,
        decision_ids=base.decision_ids,
        replay_report_path=base.replay_report_path,
        turn_index=base.turn_index,
        context_sources=compact_context_sources(config),
        turn_summaries=tuple(compacted.get("recent") or []),
        rolling_summary=compacted.get("rolling_summary"),
        context_policy=policy,
        consolidation={
            "triggered": bool(compacted.get("triggered")),
            "triggered_by": list(compacted.get("triggered_by") or []),
            "run_log": compacted.get("run_log"),
            "tool_result_count": compacted.get("tool_result_count", 0),
            "accumulated_tokens": compacted.get("accumulated_tokens", 0),
            "overhead_budget_pct": policy.get("consolidation_overhead_budget_pct"),
        },
    )
    assembled_tokens = estimate_context_tokens(root, context, divisor=divisor)
    warn_threshold = positive_int(policy.get("assembled_context_warn_tokens"))
    warning = warn_threshold is not None and assembled_tokens > warn_threshold
    if not warning:
        return ContextPack(**{**context.__dict__, "assembled_context_tokens": assembled_tokens})

    fallback_context = ContextPack(
        unit=context.unit,
        task=context.task,
        spec_paths=context.spec_paths,
        decision_ids=context.decision_ids,
        replay_report_path=context.replay_report_path,
        turn_index=context.turn_index,
        context_sources=context.context_sources,
        turn_summaries=(),
        rolling_summary=context.rolling_summary
        or {
            "task_id": task_id,
            "summary": "Fallback context: recent turn summaries omitted after assembled_context_tokens exceeded threshold.",
            "changed_paths": [],
            "source_turns": [],
        },
        context_policy=policy,
        consolidation={**(context.consolidation or {}), "fallback": True},
        compaction_warning=True,
        compaction_fallback=True,
    )
    return ContextPack(**{**fallback_context.__dict__, "assembled_context_tokens": estimate_context_tokens(root, fallback_context, divisor=divisor)})


def validate_task_close_summary(report: dict[str, Any], config: dict[str, Any] | None) -> list[str]:
    policy = context_policy(config)
    if policy.get("compaction_enabled") is not True:
        return []
    task_status = (report.get("transitions") or {}).get("task_status") or {}
    if task_status.get("to") != "done":
        return []
    summary = str(report.get("task_close_summary") or "").strip()
    if not summary:
        return ["context_policy: task_close_summary is required when moving a task to done"]
    max_tokens = positive_int(policy.get("task_close_summary_max_tokens"), 2000) or 2000
    if token_count(summary) > max_tokens:
        return [f"context_policy: task_close_summary exceeds {max_tokens} tokens"]
    return []


def delegate_subagent(
    *,
    subtask: dict[str, Any],
    context_pack: ContextPack,
    root: Path,
    config: dict[str, Any] | None,
    report: dict[str, Any] | None = None,
) -> dict[str, Any]:
    policy = context_policy(config)
    if policy.get("subagents_enabled") is not True:
        return {"ok": False, "reason": "subagents_disabled"}
    report = dict(report or {})
    max_tokens = positive_int(policy.get("subagent_summary_max_tokens"), 2000) or 2000
    divisor = positive_int(((config or {}).get("token_cost") or {}).get("chars_per_token"), 4) or 4
    summary = str(report.get("summary") or subtask.get("summary") or "").strip()
    limit_chars = max_tokens * divisor
    truncated = len(summary) > limit_chars
    if truncated:
        summary = summary[:limit_chars].rstrip()
    return {
        "ok": True,
        "summary": summary,
        "summary_tokens": token_count(summary, divisor),
        "truncated": truncated,
        "changed_paths": list(report.get("changed_paths") or []),
        "context": {
            "unit": subtask,
            "task": subtask,
            "spec_paths": list(context_pack.spec_paths),
            "decision_ids": list(context_pack.decision_ids),
            "context_sources": list(context_pack.context_sources),
        },
    }


def context_metadata(context: ContextPack) -> dict[str, Any]:
    if not context.context_policy:
        return {}
    return {
        "context_sources": list(context.context_sources),
        "assembled_context_tokens": context.assembled_context_tokens,
        "compaction_warning": context.compaction_warning,
        "compaction_fallback": context.compaction_fallback,
        "rolling_summary": context.rolling_summary,
        "recent_turn_summaries": list(context.turn_summaries),
        "consolidation": context.consolidation,
    }


def attach_context_metadata(entry: dict[str, Any], context: ContextPack) -> dict[str, Any]:
    metadata = context_metadata(context)
    if metadata:
        entry["context_policy"] = metadata
    return entry


def default_run_id(reports: list[Path | None], *, adapter_name: str = "replay") -> str:
    parts = [adapter_name]
    parts.extend(str(path.as_posix()) for path in reports if path is not None)
    for path in [item for item in reports if item is not None]:
        if path.exists() and path.is_file():
            parts.append(path.read_text(encoding="utf-8-sig"))
    return deterministic_run_id(parts)


def run_log_path(root: Path, run_id: str) -> Path:
    return root / "runtime" / "runs" / f"{run_id}.jsonl"


def real_invoker_run_id_error(root: Path, *, llm_invoker: str, run_id: str | None) -> str | None:
    if llm_invoker != "subprocess":
        return None
    if not str(run_id or "").strip():
        return "subprocess llm invoker requires --run-id"
    if run_log_path(root, str(run_id)).exists():
        return f"run_log already exists for run_id: {run_id}"
    return None


def schema_report(report: dict[str, Any], root: Path) -> dict[str, Any]:
    allowed_keys = turn_schema_keys(root)
    return {key: value for key, value in report.items() if key in allowed_keys}


def normalize_scope_path(path: Any) -> str:
    return str(path or "").replace("\\", "/").strip()


def owner_slug(owner: str) -> str:
    return "".join(char.lower() if char.isalnum() else "-" for char in owner).strip("-") or "agent"


def claim_id_for_unit(task_id: str, owner: str) -> str:
    return f"CLAIM-{task_id}-{owner_slug(owner)}-runtime"


def task_claim_scope(task: dict[str, Any], task_id: str) -> list[str]:
    scope: list[str] = [
        "Area_comun/state/CLAIMS.json",
        f"Area_comun/state/TASK_INDEX.json#{task_id}",
        f"Area_comun/state/PROJECT_STATE.json#active_tasks/{task_id}",
    ]
    for key in ("file", "task_file"):
        value = normalize_scope_path(task.get(key))
        if value:
            scope.append(value)
    for key in ("scope", "relevant_files", "deliverables"):
        values = task.get(key)
        if isinstance(values, (list, tuple)):
            for value in values:
                text = normalize_scope_path(value)
                if text and ("/" in text or "." in Path(text).name):
                    scope.append(text)
    return list(dict.fromkeys(scope))


def active_claim_for_unit(state: dict[str, Any], task_id: str, owner: str) -> dict[str, Any] | None:
    for claim in active_claims(state):
        if claim.get("task_id") == task_id and claim.get("owner") == owner:
            return dict(claim)
    return None


def acquire_routed_claim(root: Path, state: dict[str, Any], unit: dict[str, Any]) -> dict[str, Any]:
    task_id = str(unit.get("task_id") or "")
    owner = str(unit.get("owner") or "")
    task = task_for_unit(state, unit) or {}
    if not task_id or task_id == "none" or not owner:
        return {"acquired": False, "claim": None}

    existing = active_claim_for_unit(state, task_id, owner)
    if existing is not None:
        return {"acquired": False, "claim": existing, "reused": True}

    claim_id = claim_id_for_unit(task_id, owner)
    timestamp = utc_now()
    claim = {
        "claim_id": claim_id,
        "task_id": task_id,
        "owner": owner,
        "status": "active",
        "scope": task_claim_scope(task, task_id),
        "started_at": timestamp,
        "updated_at": timestamp,
        "expires_at": "2026-06-10",
        "notes": "Acquired by runtime orchestrator before routed turn.",
    }
    try:
        result = submit_intent(
            root,
            owner,
            {
                "claim": {
                    "op": "acquire",
                    "idempotency_key": f"orchestrator:claim-acquire:{task_id}:{owner_slug(owner)}",
                    "claim": claim,
                }
            },
            timestamp=timestamp,
        )
    except IntentError as exc:
        return {"acquired": False, "claim": None, "error": str(exc)}
    return {"acquired": True, "claim": claim, "result": result}


def release_acquired_routed_claim(root: Path, claim_result: dict[str, Any]) -> dict[str, Any]:
    if not claim_result.get("acquired"):
        return {"released": False}
    claim = claim_result.get("claim") if isinstance(claim_result.get("claim"), dict) else {}
    claim_id = str(claim.get("claim_id") or "").strip()
    owner = str(claim.get("owner") or "").strip()
    task_id = str(claim.get("task_id") or "").strip()
    if not claim_id or not owner:
        return {"released": False, "error": "claim cleanup missing claim_id or owner"}

    timestamp = utc_now()
    try:
        result = submit_intent(
            root,
            owner,
            {
                "claim": {
                    "op": "release",
                    "idempotency_key": f"orchestrator:claim-release:{task_id}:{owner_slug(owner)}",
                    "claim_id": claim_id,
                }
            },
            timestamp=timestamp,
        )
    except IntentError as exc:
        return {"released": False, "claim_id": claim_id, "error": str(exc)}
    return {"released": True, "claim_id": claim_id, "result": result}


def cleanup_event_summary(cleanup: dict[str, Any]) -> dict[str, Any]:
    summary = {
        "released": cleanup.get("released") is True,
        "claim_id": cleanup.get("claim_id"),
    }
    if cleanup.get("error"):
        summary["error"] = cleanup["error"]
    result = cleanup.get("result") if isinstance(cleanup.get("result"), dict) else {}
    events = result.get("events") if isinstance(result, dict) else []
    if events:
        summary["eventlog_events"] = [
            {"seq": event.get("seq"), "type": event.get("type"), "aggregate_id": event.get("aggregate_id")}
            for event in events
            if isinstance(event, dict)
        ]
    return {key: value for key, value in summary.items() if value not in (None, [], {})}


def with_pre_apply_claim_cleanup(root: Path, claim_result: dict[str, Any], entry: dict[str, Any]) -> dict[str, Any]:
    cleanup = release_acquired_routed_claim(root, claim_result)
    if cleanup.get("released") or cleanup.get("error"):
        entry["claim_cleanup"] = cleanup_event_summary(cleanup)
    if cleanup.get("error"):
        errors = entry.setdefault("errors", [])
        if isinstance(errors, list):
            errors.append(f"claim cleanup failed: {cleanup['error']}")
    return entry


def report_cost_tokens(report: dict[str, Any]) -> int | None:
    cost = report.get("cost")
    if isinstance(cost, int):
        return cost
    if isinstance(cost, dict) and isinstance(cost.get("tokens"), int):
        return cost["tokens"]
    return None


def budget_stop_entry(
    *,
    turn: int,
    trace: list[str],
    budget_event: dict[str, Any],
    unit: dict[str, Any] | None = None,
    report: dict[str, Any] | None = None,
    duration_ms: int = 0,
) -> dict[str, Any]:
    entry = turn_entry(
        turn=turn,
        trace=trace,
        unit=unit,
        report=report,
        outcome="budget_exhausted",
        reason=str(budget_event.get("reason") or "budget_exhausted"),
        duration_ms=duration_ms,
    )
    entry["budget_escalation"] = budget_event
    return entry


def normalize_report_path(path: str) -> str:
    return path.replace("\\", "/").split("#", 1)[0].strip("/")


def parse_porcelain_v1_z(raw: bytes) -> list[str]:
    records = raw.split(b"\0")
    paths: list[str] = []
    index = 0
    while index < len(records):
        record = records[index]
        index += 1
        if not record:
            continue
        if len(record) < 4 or record[2:3] != b" ":
            raise ValueError("malformed git status --porcelain=v1 -z record")
        status = record[:2]
        paths.append(record[3:].decode("utf-8", errors="surrogateescape").replace("\\", "/"))
        if b"R" in status or b"C" in status:
            if index >= len(records) or not records[index]:
                raise ValueError("missing source path in git status --porcelain=v1 -z pair")
            paths.append(records[index].decode("utf-8", errors="surrogateescape").replace("\\", "/"))
            index += 1
    return sorted(paths)


def dirty_worktree_paths(root: Path) -> list[str]:
    completed = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
        cwd=root,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return []
    return parse_porcelain_v1_z(completed.stdout)


def dirty_tracked_worktree_paths(root: Path) -> list[str]:
    completed = subprocess.run(
        ["git", "status", "--porcelain=v1", "-z", "--untracked-files=no"],
        cwd=root,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        return []
    return parse_porcelain_v1_z(completed.stdout)


def unreported_dirty_paths(root: Path, report: dict[str, Any], *, baseline_dirty: set[str]) -> list[str]:
    declared = {normalize_report_path(str(path)) for path in report.get("changed_paths") or []}
    current = set(dirty_worktree_paths(root))
    return [path for path in sorted(current - baseline_dirty) if normalize_report_path(path) not in declared]


def select_reports(*, adapter_name: str, replay_path: Path | None, llm_invoker: str) -> list[Path | None]:
    if adapter_name == "replay":
        if replay_path is None:
            raise ValueError("replay adapter requires --replay-report")
        return list(replay_paths(replay_path))
    if adapter_name == "llm" and llm_invoker == "recorded":
        if replay_path is None:
            raise ValueError("llm recorded invoker requires --replay-report transcript file or directory")
        return list(replay_paths(replay_path))
    return [None]


def subprocess_multiturn_allowed(
    *,
    config: dict[str, Any],
    allow_real_invoker: bool,
    allow_supervised_autonomy: bool,
) -> bool:
    return (
        allow_real_invoker
        and allow_supervised_autonomy
        and supervised_autonomy_activation_error(config) is None
        and real_invoker_activation_error(config) is None
    )


def adapter_for_turn(
    *,
    adapter_name: str,
    report_path: Path | None,
    llm_invoker: str,
    llm_command: str | None,
    llm_preset: str | None,
    allow_real_invoker: bool,
    config: dict[str, Any] | None,
) -> Any:
    if adapter_name == "replay":
        return ReplayAdapter()
    if adapter_name != "llm":
        raise ValueError(f"unsupported adapter: {adapter_name}")
    if llm_invoker == "recorded":
        if report_path is None:
            raise ValueError("recorded invoker requires a transcript path")
        return LLMAdapter(RecordedInvoker(report_path))
    if llm_invoker == "subprocess":
        if not allow_real_invoker:
            raise ValueError("subprocess invoker requires --allow-real-invoker")
        activation_error = real_invoker_activation_error(config)
        if activation_error:
            raise ValueError(f"subprocess invoker requires registered activation: {activation_error}")
        resolved = resolve_llm_command(config, command=llm_command, preset=llm_preset)
        if resolved is None:
            raise ValueError("subprocess invoker requires --llm-command or --llm-preset")
        return LLMAdapter(SubprocessInvoker.from_command(resolved.command, name=f"subprocess:{resolved.label}"))
    raise ValueError(f"unsupported llm invoker: {llm_invoker}")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True), encoding="utf-8")


def auto_prune_if_due(root: Path) -> dict[str, Any]:
    script = root / "scripts" / "prune_state.py"
    if not script.exists():
        return {"checked": False, "reason": "prune_state.py not found"}
    pre_dirty_all = set(dirty_worktree_paths(root))
    pre_dirty = dirty_tracked_worktree_paths(root)
    if pre_dirty:
        return {"checked": False, "reason": "worktree dirty before prune", "dirty_paths": pre_dirty}

    check = subprocess.run(
        [sys.executable, str(script), "--root", str(root), "--check"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if check.returncode == 0:
        return {"checked": True, "due": False, "stdout": check.stdout}
    if check.returncode != 1:
        return {"checked": True, "due": None, "returncode": check.returncode, "stdout": check.stdout, "stderr": check.stderr}

    apply = subprocess.run(
        [sys.executable, str(script), "--root", str(root), "--apply"],
        cwd=root,
        text=True,
        capture_output=True,
        check=False,
    )
    if apply.returncode != 0:
        return {"checked": True, "due": True, "applied": False, "returncode": apply.returncode, "stdout": apply.stdout, "stderr": apply.stderr}

    changed = sorted(set(dirty_worktree_paths(root)) - pre_dirty_all)
    if not changed:
        return {"checked": True, "due": True, "applied": True, "commit": None, "stdout": apply.stdout}
    try:
        commit = commit_turn(root, "chore(runtime): prune state", changed, verify=False)
        return {"checked": True, "due": True, "applied": True, "commit": commit, "changed_paths": changed, "stdout": apply.stdout}
    except VcsError as exc:
        discard_worktree_changes(root)
        return {"checked": True, "due": True, "applied": True, "commit": None, "error": str(exc)}


def run_loop(
    root: Path,
    replay_path: Path | None,
    *,
    adapter_name: str = "replay",
    llm_invoker: str = "recorded",
    llm_command: str | None = None,
    llm_preset: str | None = None,
    allow_real_invoker: bool = False,
    allow_supervised_autonomy: bool = False,
    once: bool = False,
    max_iter: int | None = None,
    run_id: str | None = None,
    budget_tokens: int | None = None,
    clock_fixed: int = 0,
) -> dict[str, Any]:
    root = root.resolve()
    if not runtime_enabled(root):
        return {"ok": False, "reason": "runtime.enabled is false; --run is disabled"}
    config = read_json(root / "protocol.config.json")
    approval_config = plan_approval_config(config)
    current_plan = render_plan(root, decision_id=str(approval_config.get("decision_id") or "") or None)
    approval_error = plan_approval_error(root, config, current_plan)
    if approval_error:
        return {
            "ok": False,
            "reason": approval_error,
            "plan_approval": {
                "approval_hash": current_plan["approval_hash"],
                "render_hash": current_plan["render_hash"],
                "material_fields": current_plan["material_fields"],
            },
        }
    supervision: dict[str, Any] | None = None
    subprocess_multiturn = adapter_name == "llm" and llm_invoker == "subprocess" and not once
    if allow_supervised_autonomy and not subprocess_multiturn:
        activation_error = supervised_autonomy_activation_error(config)
        if activation_error:
            return {"ok": False, "reason": f"supervised autonomy requires registered activation: {activation_error}"}
        supervision = supervised_autonomy_payload(config)
    elif allow_supervised_autonomy and supervised_autonomy_activation_error(config) is None:
        supervision = supervised_autonomy_payload(config)

    try:
        reports = select_reports(adapter_name=adapter_name, replay_path=replay_path, llm_invoker=llm_invoker)
    except ValueError as exc:
        return {"ok": False, "reason": str(exc)}
    if not reports:
        return {"ok": False, "reason": f"no replay reports found: {replay_path}"}
    if subprocess_multiturn and not subprocess_multiturn_allowed(
        config=config,
        allow_real_invoker=allow_real_invoker,
        allow_supervised_autonomy=allow_supervised_autonomy,
    ):
        return {"ok": False, "reason": "subprocess llm invoker requires --once"}
    run_id_error = real_invoker_run_id_error(root, llm_invoker=llm_invoker, run_id=run_id)
    if run_id_error:
        return {"ok": False, "reason": run_id_error}

    if once:
        requested_limit = 1
    elif subprocess_multiturn:
        requested_limit = max_iter if max_iter is not None else int((supervision or {}).get("caps", {}).get("max_turns", 1))
    else:
        requested_limit = max_iter if max_iter is not None else len(reports)
    limit = min(requested_limit, int((supervision or {}).get("caps", {}).get("max_turns", requested_limit)))
    if limit < 1:
        return {"ok": False, "reason": "--max-iter must be >= 1"}
    if subprocess_multiturn and len(reports) < limit:
        reports = [None for _ in range(limit)]

    runlog = RunLog(root, run_id=run_id or default_run_id(reports[:limit], adapter_name=adapter_name))
    budget = Budget(max_iter=limit, max_cost_tokens=budget_tokens, **budget_settings(config))
    turns: list[dict[str, Any]] = []
    baseline_dirty = set(dirty_worktree_paths(root))
    wall_clock_elapsed_ms = 0

    def finalize(maintenance: dict[str, Any]) -> dict[str, Any]:
        summary = summarize(runlog.path)
        summary_path = runlog.path.with_suffix(".summary.json")
        write_json(summary_path, summary)
        result = {
            "ok": True,
            "run_id": runlog.run_id,
            "run_log": str(runlog.path),
            "summary": str(summary_path),
            "metrics": summary,
            "maintenance": maintenance,
            "turns": turns,
        }
        if supervision is not None:
            run_report_path = runlog.path.with_suffix(".runreport.md")
            write_run_report(run_report_path, run_id=runlog.run_id, turns=turns, metrics=summary, supervision=supervision)
            result["run_report"] = str(run_report_path)
            result["supervised_autonomy"] = supervision
        return result

    queue_event = budget.queue_event(queue_length=len(reports), last_responsible=responsible())
    if queue_event:
        entry = budget_stop_entry(turn=1, trace=["budget"], budget_event=queue_event, duration_ms=clock_fixed)
        runlog.append(entry)
        turns.append(entry)
        maintenance = auto_prune_if_due(root)
        return finalize(maintenance)

    for index, report_path in enumerate(reports[:limit], start=1):
        if supervision is not None and pause_sentinel_path(root).exists():
            entry = turn_entry(
                turn=index,
                trace=["supervised_autonomy", "pause"],
                outcome="paused",
                reason="runtime/state/PAUSE",
                duration_ms=0,
            )
            entry["supervised_autonomy"] = {**supervision, "wall_clock_elapsed_ms": wall_clock_elapsed_ms}
            runlog.append(entry)
            turns.append(entry)
            break

        if supervision is not None:
            wall_clock_limit = int((supervision.get("caps") or {}).get("wall_clock_ms") or 0)
            if wall_clock_limit and wall_clock_elapsed_ms + clock_fixed > wall_clock_limit:
                entry = turn_entry(
                    turn=index,
                    trace=["supervised_autonomy", "wall_clock"],
                    outcome="wallclock_exhausted",
                    reason=f"caps.wall_clock_ms={wall_clock_limit}",
                    duration_ms=0,
                )
                entry["supervised_autonomy"] = {**supervision, "wall_clock_elapsed_ms": wall_clock_elapsed_ms}
                runlog.append(entry)
                turns.append(entry)
                break

        trace: list[str] = ["gate_pre"]
        gate_pre = run_gate(root)
        if not gate_pre["green"]:
            entry = turn_entry(turn=index, trace=trace, outcome="stopped", reason="pre-gate failed", duration_ms=clock_fixed)
            entry["gate"] = gate_pre
            runlog.append(entry)
            turns.append(entry)
            break

        state = load_state(root)
        trace.append("route")
        unit = select_next(state)
        if unit is None or unit.get("action") == "escalate":
            entry = turn_entry(
                turn=index,
                trace=trace,
                unit=unit,
                outcome="stopped",
                reason="no runnable unit or human gate",
                duration_ms=clock_fixed,
            )
            runlog.append(entry)
            turns.append(entry)
            break

        task_id = str(unit.get("task_id") or "none")
        deadline_event = budget.deadline_event(
            task_id=task_id,
            turn_index=index,
            last_responsible=responsible(str(unit.get("owner") or ""), task_id),
        )
        if deadline_event:
            entry = budget_stop_entry(
                turn=index,
                trace=[*trace, "budget"],
                unit=unit,
                budget_event=deadline_event,
                duration_ms=clock_fixed,
            )
            runlog.append(entry)
            turns.append(entry)
            break

        trace.append("claim")
        claim_result = acquire_routed_claim(root, state, unit)
        if claim_result.get("error"):
            entry = turn_entry(
                turn=index,
                trace=trace,
                unit=unit,
                outcome="rejected",
                errors=[f"claim acquire failed: {claim_result['error']}"],
                duration_ms=clock_fixed,
            )
            runlog.append(entry)
            turns.append(entry)
            break
        if claim_result.get("acquired"):
            baseline_dirty = set(dirty_worktree_paths(root))
            state = load_state(root)

        context = build_turn_context(
            root=root,
            state=state,
            unit=unit,
            replay_report_path=report_path,
            turn_index=index,
            config=config,
            runlog=runlog,
        )
        trace.append("adapter")
        try:
            adapter = adapter_for_turn(
                adapter_name=adapter_name,
                report_path=report_path,
                llm_invoker=llm_invoker,
                llm_command=llm_command,
                llm_preset=llm_preset,
                allow_real_invoker=allow_real_invoker,
                config=config,
            )
        except ValueError as exc:
            entry = turn_entry(turn=index, trace=trace, unit=unit, outcome="rejected", errors=[str(exc)], duration_ms=clock_fixed)
            entry = attach_context_metadata(entry, context)
            entry = with_pre_apply_claim_cleanup(root, claim_result, entry)
            runlog.append(entry)
            turns.append(entry)
            break
        report = adapter.run_turn(context=context, root=root)
        unreported = unreported_dirty_paths(root, report, baseline_dirty=baseline_dirty)
        if unreported:
            entry = turn_entry(
                turn=index,
                trace=trace,
                unit=unit,
                report=report,
                outcome="rejected",
                errors=[f"unreported worktree change: {path}" for path in unreported],
                duration_ms=clock_fixed,
            )
            entry = with_pre_apply_claim_cleanup(root, claim_result, entry)
            runlog.append(entry)
            turns.append(entry)
            break
        clean_report = schema_report(report, root)
        trace.append("validate")
        errors = validate_turn(clean_report, root)
        errors.extend(validate_task_close_summary(clean_report, config))
        if errors:
            entry = turn_entry(
                turn=index,
                trace=trace,
                unit=unit,
                report=report,
                outcome="rejected",
                errors=errors,
                duration_ms=clock_fixed,
            )
            entry = attach_context_metadata(entry, context)
            entry = with_pre_apply_claim_cleanup(root, claim_result, entry)
            runlog.append(entry)
            turns.append(entry)
            break

        trace.append("human_gate")
        human_gate = clean_report.get("outcome") in HUMAN_OUTCOMES or (clean_report.get("gate") or {}).get("human_required") is True
        if human_gate:
            entry = turn_entry(turn=index, trace=trace, unit=unit, report=report, duration_ms=clock_fixed)
            entry["human_required"] = True
            entry = attach_context_metadata(entry, context)
            entry = with_pre_apply_claim_cleanup(root, claim_result, entry)
            runlog.append(entry)
            turns.append(entry)
            break

        cost_tokens = report_cost_tokens(report)
        last_responsible = responsible(str(report.get("agent") or ""), str(report.get("task_id") or "none"))
        budget_warning = budget.soft_warning(cost_tokens=cost_tokens, last_responsible=last_responsible)
        hard_event = budget.hard_event(cost_tokens=cost_tokens, last_responsible=last_responsible)
        if hard_event:
            entry = budget_stop_entry(
                turn=index,
                trace=[*trace, "budget"],
                unit=unit,
                report=report,
                budget_event=hard_event,
                duration_ms=clock_fixed,
            )
            if budget_warning:
                entry["budget_warning"] = budget_warning
            entry = attach_context_metadata(entry, context)
            entry = with_pre_apply_claim_cleanup(root, claim_result, entry)
            runlog.append(entry)
            turns.append(entry)
            break
        if budget_tokens is not None and cost_tokens is not None and cost_tokens > budget_tokens:
            budget_event = budget.event(
                reason="max_cost_tokens",
                consumed={"cost_tokens": cost_tokens},
                limit={"cost_tokens": budget_tokens},
                last_responsible=last_responsible,
            )
            entry = budget_stop_entry(
                turn=index,
                trace=[*trace, "budget"],
                unit=unit,
                report=report,
                budget_event=budget_event,
                duration_ms=clock_fixed,
            )
            entry = with_pre_apply_claim_cleanup(root, claim_result, entry)
            entry = attach_context_metadata(entry, context)
            runlog.append(entry)
            turns.append(entry)
            break

        trace.append("apply")
        result = apply_gate_and_commit(clean_report, root)
        trace.extend(["gate_post", "commit"])
        entry = turn_entry(
            turn=index,
            trace=trace,
            unit=unit,
            report=report,
            transition=(clean_report.get("transitions") or {}).get("task_status"),
            gate_green=result.get("green"),
            commit=result.get("commit"),
            reverted=result.get("reverted", False),
            duration_ms=clock_fixed,
        )
        if result.get("eventlog_events"):
            entry["eventlog_events"] = [
                {"seq": event.get("seq"), "type": event.get("type"), "aggregate_id": event.get("aggregate_id")}
                for event in result["eventlog_events"]
            ]
        if budget_warning:
            entry["budget_warning"] = budget_warning
        entry = attach_context_metadata(entry, context)
        runlog.append(entry)
        turns.append(entry)
        budget.consume(cost_tokens=cost_tokens)
        wall_clock_elapsed_ms += clock_fixed
        baseline_dirty = set(dirty_worktree_paths(root))
        if supervision is not None and result.get("green"):
            checkpoint_reason = fix_cycle_checkpoint_reason(root, report, config)
            actual_adapter_turns = sum(1 for current in turns if "adapter" in (current.get("trace") or []))
            checkpoint_every = int((supervision.get("caps") or {}).get("human_checkpoint_every_k") or 0)
            if checkpoint_reason is None and checkpoint_every and actual_adapter_turns >= checkpoint_every and index < len(reports[:limit]):
                checkpoint_reason = f"caps.human_checkpoint_every_k={checkpoint_every}"
            if checkpoint_reason:
                checkpoint_entry = turn_entry(
                    turn=index + 1,
                    trace=["supervised_autonomy", "human_checkpoint"],
                    outcome="human_checkpoint",
                    reason=checkpoint_reason,
                    duration_ms=0,
                )
                checkpoint_entry["human_required"] = True
                checkpoint_entry["supervised_autonomy"] = {
                    **supervision,
                    "wall_clock_elapsed_ms": wall_clock_elapsed_ms,
                }
                runlog.append(checkpoint_entry)
                turns.append(checkpoint_entry)
                break
        if not result.get("green"):
            break
        if budget.exceeded(last_responsible=last_responsible) and index < len(reports[:limit]):
            budget_entry = budget_stop_entry(
                turn=index + 1,
                trace=["budget"],
                budget_event=budget.last_event or budget.event(
                    reason=budget.reason or "budget_exhausted",
                    consumed={"turns": budget.turns, "cost_tokens": budget.cost_tokens},
                    limit={},
                    last_responsible=last_responsible,
                ),
                duration_ms=clock_fixed,
            )
            runlog.append(budget_entry)
            turns.append(budget_entry)
            break

    if supervision is not None and len(reports) > limit:
        actual_adapter_turns = sum(1 for entry in turns if "adapter" in (entry.get("trace") or []))
        last = turns[-1] if turns else {}
        stopped_already = (
            bool(last.get("reason"))
            or bool(last.get("errors"))
            or last.get("human_required") is True
            or last.get("gate_green") is False
            or str(last.get("outcome") or "") in {"rejected", "budget_exhausted", "human_required", "decision_required", "human_checkpoint"}
        )
        if actual_adapter_turns >= limit and not stopped_already:
            entry = turn_entry(
                turn=limit + 1,
                trace=["supervised_autonomy"],
                outcome="max_turns_reached",
                reason=f"caps.max_turns={limit}",
                duration_ms=clock_fixed,
            )
            entry["supervised_autonomy"] = supervision
            runlog.append(entry)
            turns.append(entry)

    maintenance = auto_prune_if_due(root)
    return finalize(maintenance)


def main() -> int:
    parser = argparse.ArgumentParser(description="Protocol runtime orchestrator.")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument("--plan", action="store_true", help="Dry-run: print next action without mutating state")
    parser.add_argument("--plan-all", action="store_true", help="Render the governed unit set as a pure task-index/intake projection")
    parser.add_argument("--plan-decision", help="With --plan-all, include only tasks linked to this decision id")
    parser.add_argument("--run", action="store_true", help="Execute deterministic runtime turns")
    parser.add_argument("--once", action="store_true", help="Execute exactly one turn")
    parser.add_argument("--max-iter", type=int, default=None, help="Maximum turns to execute")
    parser.add_argument("--adapter", choices=["replay", "llm"], default="replay")
    parser.add_argument("--replay-report", help="Replay report JSON file or directory; for llm recorded, transcript file or directory")
    parser.add_argument("--llm-invoker", choices=["recorded", "subprocess"], default="recorded")
    parser.add_argument("--llm-command", help="Command for the explicit subprocess LLM invoker")
    parser.add_argument("--llm-preset", help="Named runtime.llm_cli_presets entry for the subprocess LLM invoker")
    parser.add_argument("--allow-real-invoker", action="store_true", help="Required to run the subprocess LLM invoker")
    parser.add_argument("--allow-supervised-autonomy", action="store_true", help="Enable registered supervised-autonomy caps")
    parser.add_argument("--run-id", help="Run-log id. Required for subprocess invoker; replay defaults to a replay-input hash")
    parser.add_argument("--budget-tokens", type=int, default=None, help="Maximum declared turn cost in tokens")
    parser.add_argument("--clock-fixed", type=int, default=0, help="Deterministic duration_ms value for tests")
    args = parser.parse_args()

    modes = sum(bool(value) for value in (args.plan, args.plan_all, args.run))
    if modes != 1:
        parser.error("choose exactly one of --plan, --plan-all, or --run")
    if args.plan_decision and not args.plan_all:
        parser.error("--plan-decision requires --plan-all")

    root = Path(args.root).resolve()

    if args.plan:
        result = select_next(load_state(root))
        print(json.dumps({"dry_run": True, "next": result}, indent=2, ensure_ascii=False))
        return 0
    if args.plan_all:
        print(json.dumps(render_plan(root, decision_id=args.plan_decision), indent=2, ensure_ascii=False))
        return 0

    if args.adapter == "replay" and not args.replay_report:
        parser.error("--run with replay requires --replay-report")
    if args.adapter == "llm" and args.llm_invoker == "recorded" and not args.replay_report:
        parser.error("--run with llm recorded requires --replay-report")

    result = run_loop(
        root,
        Path(args.replay_report) if args.replay_report else None,
        adapter_name=args.adapter,
        llm_invoker=args.llm_invoker,
        llm_command=args.llm_command,
        llm_preset=args.llm_preset,
        allow_real_invoker=args.allow_real_invoker,
        allow_supervised_autonomy=args.allow_supervised_autonomy,
        once=args.once,
        max_iter=args.max_iter,
        run_id=args.run_id,
        budget_tokens=args.budget_tokens,
        clock_fixed=args.clock_fixed,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
