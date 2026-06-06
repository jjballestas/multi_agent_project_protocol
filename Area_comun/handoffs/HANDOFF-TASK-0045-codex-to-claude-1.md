---
task_id: TASK-0045
from: Codex
to: Claude
status: submitted
created_at: 2026-06-06
spec_id: Area_comun/specs/SPEC-0038-n-agent-registry.md
linked_decisions: [DECISION-0015, DECISION-0001]
---

# HANDOFF TASK-0045 - N-agent Phase 3 router

## Summary

Implemented the Phase 3 router as an additive, deterministic N-agent path while keeping the
legacy N=2 behavior intact when tasks do not declare `required_capability`.

Delivered:

- `runtime/router.py`
  - capability-based `select_agent` for ready tasks with `required_capability`;
  - inferred reviewer/QA capability routing for `in_review` and `qa_pending`;
  - author exclusion for review/QA, including multi-capability authors;
  - no hidden self-review: no eligible distinct reviewer/QA returns `action: escalate` with candidate/filter explanation;
  - `max_active_claims` filtering;
  - load score from `routing_weights` in config;
  - deterministic score tuple: `(load_score, stable_hash(task|transition|agent|routing_epoch), agent_id)`;
  - `routing_decision.explanation` with candidate agents, eligible candidates, filtered reasons, weights and selected agent;
  - `evaluate_fairness` gate helper over eligible assignments, with weighted expected-vs-observed checks,
    anti-starvation and denominator-zero guard.
- `runtime/context.py`
  - `load_state` now includes `config` and resolved `agent_registry`.
- `protocol.config.json` and `protocol.config.template.json`
  - added `routing_epoch` and `routing_weights`.
- `examples/runtime_router_cases/run_runtime_router_cases.py`
  - preserved the 5 original router cases;
  - added capability/load, max-active-claims, review author exclusion, no-self-review escalation,
    QA author exclusion, deterministic replay and fairness/anti-starvation/weighted/zero-denominator checks.

## Compatibility

- Ready tasks without `required_capability` still route to their declared `owner`.
- Existing fallback cases remain green:
  - human gate -> `operador humano`;
  - pending mailbox before review;
  - review -> `Claude` in the legacy fallback case;
  - ready task priority/dependency ordering;
  - claimed-by-other skip.
- No network access used.

## Verification

Green:

- `python examples/runtime_eventlog_cases/run_runtime_eventlog_cases.py` -> 5/5
- `python examples/agent_registry_cases/run_agent_registry_cases.py` -> 4/4
- `python examples/runtime_turn_cases/run_runtime_turn_schema_cases.py` -> 5/5
- `python examples/runtime_turn_cases/run_runtime_turn_semantic_cases.py` -> 5/5
- `python examples/runtime_router_cases/run_runtime_router_cases.py` -> 10/10 plus fairness sub-gates
- `python examples/runtime_apply_cases/run_runtime_apply_cases.py` -> 4/4
- `python examples/runtime_loop_cases/run_runtime_loop_cases.py` -> 8/8
- `python examples/runtime_observability_cases/run_runtime_observability_cases.py` -> 5/5
- `python examples/llm_adapter_cases/run_llm_adapter_cases.py` -> 6/6
- `python scripts/validate_collaboration_state.py` -> OK, warning only for existing FYI TASK-0044 mailbox
- `python scripts/scan_encoding.py` -> OK
- `python scripts/scan_domain_neutrality.py` -> OK
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_collaboration_state.ps1` -> OK, same warning
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_encoding.ps1` -> OK
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_domain_neutrality.ps1` -> OK

## Review focus

- Confirm `required_capability` absent still preserving owner routing is the intended legacy behavior.
- Confirm escalation owner for no eligible reviewer/QA is acceptable when only the author is also the
  architect/orchestrator; the returned action is escalation, never review/QA.
- Confirm `routing_weights` top-level config shape is acceptable for future calibration.
