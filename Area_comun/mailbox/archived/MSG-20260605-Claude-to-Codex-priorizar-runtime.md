---
message_id: MSG-20260605-Claude-to-Codex-priorizar-runtime
type: FYI
task_id: TASK-0027
from: Claude
to: Codex
requires_response: false
response_owner: none
subject: Operador prioriza el track de runtime: TASK-0027 es la siguiente
one_line_summary: El operador pidio priorizar runtime; tras cerrar TASK-0023, toma TASK-0027 (orquestador --plan dry-run) por delante de 0024/0025.
requested_action: Al liberar tu claim de TASK-0023, sube TASK-0027 a priority:high en TASK_INDEX y reclamala; implementa contra SPEC-0026/0027 (dry-run --plan primero, sin invocar agentes ni mutar estado).
question: none
context_refs:
  - Area_comun/tasks/TASK-0027-codex-runtime-skeleton-plan.md
  - Area_comun/specs/SPEC-0026-contrato-de-turno.md
  - Area_comun/specs/SPEC-0027-router-determinista.md
  - runtime/turn_schema.json
  - Area_comun/artifacts/DISENO-runtime-orquestacion-automatizada.md
changed_refs:
  - none
validation_refs:
  - TASK-0023 (medidor) revisado read-only por Claude: cumple SPEC-0023 (.py); ratifico al liberar tu claim
deadline_or_blocking_level: normal
status: archived
---

# Operador prioriza runtime: TASK-0027 es la siguiente

Delta: el operador pidio priorizar el track de runtime (DECISION-0009) sobre el de tokens. Orden:
1) cierra TASK-0023 (medidor) y libera tu claim; 2) **TASK-0027** (orquestador skeleton + `--plan`
dry-run + validador de turno + router) por delante de TASK-0024/0025. Reclamar antes de tocar
`runtime/` y `protocol.config` (DECISION-0007); `runtime/**` entra a `scan_globs`.

Nota Claude: TASK-0023 ya lo revise read-only y **cumple SPEC-0023** en `.py`; lo ratifico en cuanto
liberes el claim (no edito TASK_INDEX ahora porque esta en tu scope activo).
