---
task_id: TASK-0046
from: Codex
to: Claude
status: submitted
created_at: 2026-06-06
spec_id: Area_comun/specs/SPEC-0038-n-agent-registry.md
linked_decisions: [DECISION-0015, DECISION-0001]
---

# HANDOFF TASK-0046 - N-agent Phase 4 Review/QA

## Summary

Implemented the Phase 4 Review/QA state machine additively, keeping legacy runtime cases green.

Delivered:

- `runtime/review_qa.py`
  - canonical `failure_signature = check_id + normalized error class + normalized artifact path`;
  - superficial log/timestamp/id differences do not affect signatures;
  - consecutive same-signature QA failure detection;
  - `max_qa_cycles` helper from config.
- `runtime/turn_schema.json`
  - additive Review/QA statuses: `changes_requested`, `review_approved`, `qa_pending`,
    `qa_failed`, `architect_review`;
  - optional `transitions.review_qa` payload for review/QA events.
- `runtime/turn_validate.py`
  - reviewer/QA capability checks for new transitions;
  - reviewer/QA author exclusion;
  - defect checks required for `reject_review` and `fail_qa`;
  - evidence required for `pass_qa`;
  - `architect_review` required when loop cut or `max_qa_cycles` is exceeded.
- `runtime/apply.py`
  - persists `review_attempts`, `qa_attempts`, `defect_log`, `qa_evidence`,
    `review_approved_by`, `qa_passed_by`, `assigned_to`, and quality escalation reason.
- `runtime/router.py`
  - routes `changes_requested`/`qa_failed` as `assign_fix`;
  - prefers original author when still eligible, otherwise falls back to weighted least-loaded.
- `scripts/validate_collaboration_state.py` and `.ps1`
  - allow the new Review/QA statuses in SDD validation;
  - treat `review_approved`, `qa_pending`, and `architect_review` as reviewed/release-like
    states for deliverable and handoff-release checks.
- `protocol.config.json` and `.template.json`
  - added `quality_policy.max_qa_cycles` and related flags.
- `examples/runtime_review_qa_cases/`
  - 9 golden cases covering QA failure, loop cut, distinct signatures, superficial log normalization,
    max-cycle escalation, self-QA/self-review rejection, evidence gate and fix routing.

## Compatibility

- Existing runtime router/apply/turn/eventlog/loop/observability/LLM adapter cases remain green.
- Existing legacy N=2 paths are not migrated or rewritten.
- New schema fields are optional; old turn reports remain valid.
- No network access used.

## Verification

Green:

- `python examples/runtime_review_qa_cases/run_runtime_review_qa_cases.py` -> 9/9
- `python examples/runtime_turn_cases/run_runtime_turn_schema_cases.py` -> 5/5
- `python examples/runtime_turn_cases/run_runtime_turn_semantic_cases.py` -> 5/5
- `python examples/runtime_apply_cases/run_runtime_apply_cases.py` -> 4/4
- `python examples/runtime_router_cases/run_runtime_router_cases.py` -> 10/10
- `python examples/runtime_eventlog_cases/run_runtime_eventlog_cases.py` -> 5/5
- `python examples/agent_registry_cases/run_agent_registry_cases.py` -> 4/4
- `python examples/runtime_loop_cases/run_runtime_loop_cases.py` -> 8/8
- `python examples/runtime_observability_cases/run_runtime_observability_cases.py` -> 5/5
- `python examples/llm_adapter_cases/run_llm_adapter_cases.py` -> 6/6
- `python scripts/validate_collaboration_state.py` -> OK
- `python scripts/scan_encoding.py` -> OK
- `python scripts/scan_domain_neutrality.py` -> OK
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_collaboration_state.ps1` -> OK
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_encoding.ps1` -> OK
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_domain_neutrality.ps1` -> OK

## Notes for review

- `architect_review` is used as the non-human quality escalation state requested by TASK-0046.
- Human escalation remains outside this implementation unless an architect later marks
  `requires_human_decision`.
- `.claude/scheduled_tasks.lock` was present as an unrelated untracked file and was not touched.
