---
message_id: MSG-20260624-Arquitecto-to-Codex-TASK-0172-changes2
task_id: TASK-0172
type: REVIEW
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
requested_action: "Corregir 4 defectos de layout/UX del rediseno Intake (feedback del operador en prueba), todos en public/app.js (+ CSS): (1) ELIMINAR la seccion inline intake-extraction-standalone del panel principal -- la carga por archivo queda SOLO via el modal intake-file-modal (ya se abre desde el radio Archivo); (2) el boton Cancelar del modal de archivo ademas de cerrar debe RESETEAR el file input + el file-extraction-status; (3) en tarjetas de candidata con status != pending (approved/discarded) NO renderizar el bloque de accion (checkbox PII revisada + botones Aprobar/Usar tarjeta/Descartar) -- solo en status pending; (4) los textarea de Narrativa e Intencion de aceptacion (modal revision, tarjeta y modal manual) deben tener rows>=6 (idealmente 8, SPEC-0090 AC7) o min-height, full-width (estaban sin rows -> apinados). Behavior-test por cada uno. El fix de PII (round 2) y las AC1-AC6/fronteras siguen verdes. Reentregar a in_review."
question: "Confirmas las 4 correcciones de layout (quitar uploader inline / reset al cancelar / sin bloque-accion en aprobadas / textareas rows>=6) con behavior-test, sin romper PII fix ni fronteras?"
one_line_summary: "TASK-0172 round 3 (layout, feedback prueba operador): quitar uploader inline, reset Cancelar, sin bloque-accion en aprobadas, textareas rows>=6."
answered_at: 2026-06-24T17:50:00Z
answer_ref: Area_comun/handoffs/HANDOFF-TASK-0172-codex-to-arquitecto-3.md
context_refs:
  - Area_comun/tasks/TASK-0172-codex-front-intake-redesign.md
  - Area_comun/specs/SPEC-0092-front-intake-redesign-cluster.md
---

# TASK-0172 round 3 -- 4 correcciones de layout (feedback del operador en prueba)

Respondido por Codex en `Area_comun/handoffs/HANDOFF-TASK-0172-codex-to-arquitecto-3.md`.

Producto: `95af6ed fix(intake): clean round three layout`.
