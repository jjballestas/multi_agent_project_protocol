# TASK_TEMPLATE.md - Task Template

Copy to `Area_comun/tasks/TASK-XXXX-<owner>-<slug>.md` and fill every required field.

For implementable task types, the frontmatter SDD fields are canonical and must be complete before
the task moves to `ready`, `claimed` or `in_progress`.

```markdown
---
id: TASK-XXXX
owner: Claude | Codex | operador humano
status: proposed | ready | claimed | in_progress | in_review | done | blocked | cancelled
type: implementation | refactor | integration | migration | security | release | discovery | analysis | review | documentation | triage
priority: low | normal | high | critical
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
depends_on: []
relates_to: []
phase: P2

# Full SDD fields for implementation/refactor/integration/migration/security/release.
spec_id: Area_comun/specs/SPEC-XXXX-short-name.md | none
execution_pipeline:
  - Step 1.
acceptance_criteria:
  - Verifiable criterion.
linked_decisions:
  - DECISION-XXXX
test_plan:
  - Command or verification.
closure_criteria:
  - Objective condition for done.

# Lightweight SDD fields for discovery/analysis/review/documentation/triage.
objective: One sentence objective.
expected_output: Concrete output.
question_to_resolve: Concrete question.
closure_criterion: Objective closure condition.
---

# TASK-XXXX - <short title>

## objetivo
Concrete result this task produces.

## entradas
Documents, decisions, specs and assumptions needed to execute without prior conversation.

## archivos_relevantes
- read:
- create:
- edit:

## entregables
Verifiable outputs with exact paths.

## SDD
- `spec_id`:
- `execution_pipeline`:
- `acceptance_criteria`:
- `linked_decisions`:
- `test_plan`:
- `closure_criteria`:

For lightweight tasks:
- `objective`:
- `expected_output`:
- `question_to_resolve`:
- `closure_criterion`:

## communication_budget
- expected_messages:
- required_handoffs:
- escalation_owner:
- compact_refs:

## definition_of_done
- [ ] Specific verifiable condition.
- [ ] Acceptance criteria satisfied.
- [ ] Test plan executed and recorded.
- [ ] Handoff created if needed.
- [ ] TASK_INDEX.json updated.
- [ ] No secrets.
- [ ] No violation of `No secrets committed. Project-specific critical boundaries must be recorded here.`.

## riesgos
What may go wrong.

## preguntas_abiertas
Concrete questions. Use "none" if there are no blockers.

## notas_de_ejecucion
Short execution log from the owner.
```
