# TASK_TEMPLATE.md - Task Template

Copy to `Area_comun/tasks/TASK-XXXX-<owner>-<slug>.md` and fill every required field.

```markdown
---
id: TASK-XXXX
owner: Claude | Codex | operador humano
status: proposed | ready | claimed | in_progress | in_review | done | blocked | cancelled
priority: low | normal | high | critical
created_at: YYYY-MM-DD
updated_at: YYYY-MM-DD
depends_on: []
relates_to: []
phase: P0
---

# TASK-XXXX - <short title>

## objetivo
Concrete result this task produces.

## entradas
Documents, decisions and assumptions needed to execute without prior conversation.

## archivos_relevantes
- read:
- create:
- edit:

## entregables
Verifiable outputs with exact paths.

## definition_of_done
- [ ] Specific verifiable condition.
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

Delivery handoffs and final task reports must end with the seven-field textual envelope:
`task_id`, `status`, `executive_summary`, `artifacts`, `gates`, `next_recommended`, `risks`.
The envelope is final text, never a tool call. After a checker NO-GO/change_required, remediate,
re-run affected gates, re-judge the result, and repeat at most two iterations before human escalation.

