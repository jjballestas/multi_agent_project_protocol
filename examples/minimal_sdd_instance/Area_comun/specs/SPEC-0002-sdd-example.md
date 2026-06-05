---
spec_id: SPEC-0002-sdd-example
task_id: TASK-0002
type: implementation
status: ready
linked_decisions: [DECISION-0004]
created_at: 2026-06-05
author: architect_agent
---

# SPEC-0002 - SDD Example Task

## Context
This neutral example demonstrates how an instance can enable SDD and require a task to declare a
resolvable spec, execution pipeline, acceptance criteria, linked decisions, test plan and closure
criteria before implementation.

## Scope
Create one simple protocol artifact and validate the instance with both validators.

## Non-Scope
No project domain, stack profile or business policy is introduced.

## execution_pipeline
- Create this spec.
- Create `TASK-0002-implementer-sdd-example.md` with the six SDD fields.
- Create a handoff.
- Run both validators.

## acceptance_criteria
- `protocol.config.json` has `sdd.enabled:true`.
- `TASK-0002` references this spec.
- Both validators pass.

## linked_decisions
- DECISION-0004

## test_plan
- `python scripts/validate_collaboration_state.py --root examples/minimal_sdd_instance`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_collaboration_state.ps1 -Root examples/minimal_sdd_instance`

## closure_criteria
- The example validates green.
- The task has a handoff for review.

## Risks
- The example should stay domain-neutral and minimal.
