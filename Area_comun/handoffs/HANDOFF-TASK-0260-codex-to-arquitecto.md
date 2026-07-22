---
task_id: TASK-0260
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-07-22
implementation_commit: b7d29c1
reviewer: Analista
---

# HANDOFF - TASK-0260

Implementation commit `b7d29c1` adds `--plan-all` and `--plan-decision` as a pure
projection of TASK_INDEX plus task intake. Missing source values remain null; the renderer
does not infer or repair them. It emits a full `render_hash` and a separate C1 material
`approval_hash` over exactly unit id, acceptance, and risk.

When `runtime.plan_approval.enabled` is true, `run_loop` refuses before turn 1 unless the
event log contains a valid `plan.approved` event from an agent with `human_owner`, matching
the current approval hash. Event and actor authentication are verified when enabled. A new
unit, changed acceptance, or changed risk invalidates approval. Goal and other nonmaterial
display changes alter the render hash but do not invalidate C1 approval. This gate is
independent from and does not enable `supervised_autonomy.human_checkpoint_every_k`.

All execution behavior was tested only in temporary scratch instances. The orchestrator was
not executed against the hub. The six reserved units, pinned epoch/genesis/dataset, runtime
activation, supervised autonomy, and real invoker were untouched.

Gates, all exit 0:

- `python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py`
- `python examples/runtime_turn_cases/run_runtime_turn_schema_cases.py`
- `python examples/runtime_turn_cases/run_runtime_turn_semantic_cases.py`
- `python examples/runtime_plan_approval_cases/run_runtime_plan_approval_cases.py`
- `python scripts/validate_collaboration_state.py`
- `python scripts/scan_encoding.py`
- `python scripts/scan_domain_neutrality.py --root .`
- `git diff --check`

Codex is the maker and has not reviewed or ratified this delivery.
