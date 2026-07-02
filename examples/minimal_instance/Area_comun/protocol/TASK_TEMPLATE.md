# TASK_TEMPLATE.md

Minimal task template placeholder.

```markdown
---
id: TASK-XXXX
status: proposed
intake:
  type: feature | fix | infra | doc | research
  goal: One-line outcome.
  acceptance:
    - Verifiable criterion.
  verification_cmd:
    - Exact command or gate.
  scope_routes:
    - Relative path or route.
  out_of_scope:
    - Explicit non-goal.
  risk: low | medium | high
  estimate: S | M | L
---
```

Delivery handoffs and final task reports must end with the seven-field textual envelope:
`task_id`, `status`, `executive_summary`, `artifacts`, `gates`, `next_recommended`, `risks`.
The envelope is final text, never a tool call. After a checker NO-GO/change_required, remediate,
re-run affected gates, re-judge the result, and repeat at most two iterations before human escalation.
