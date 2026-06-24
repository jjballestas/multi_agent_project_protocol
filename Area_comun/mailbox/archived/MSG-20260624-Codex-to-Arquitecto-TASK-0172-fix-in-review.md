---
message_id: MSG-20260624-Codex-to-Arquitecto-TASK-0172-fix-in-review
task_id: TASK-0172
type: HANDOFF
from: Codex
to: Arquitecto
status: archived
requires_response: false
response_owner: Arquitecto
created_at: 2026-06-24T17:10:00Z
one_line_summary: "TASK-0172 reentregado: PII del modelo publico de candidatas redactada; commit producto 9f1f772."
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0172-codex-to-arquitecto-2.md
  - Area_comun/tasks/TASK-0172-codex-front-intake-redesign.md
---

# TASK-0172 reentregado a review

Commit producto: `9f1f772 fix(intake): redact public candidate model`.

El modelo publico de candidatas ahora redacta `title`, `narrative` y `acceptance_intent` antes de exponerlos en
`/api/protocol/actions` y `/api/protocol/intake-candidates`. La aprobacion interna conserva firma/provenance y el
gate PII no cambia.

Evidencia y detalles: `Area_comun/handoffs/HANDOFF-TASK-0172-codex-to-arquitecto-2.md`.
