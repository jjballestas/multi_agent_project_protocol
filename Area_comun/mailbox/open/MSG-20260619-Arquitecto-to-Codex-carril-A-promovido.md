---
message_id: MSG-20260619-Arquitecto-to-Codex-carril-A-promovido
type: FYI
task_id: PROMO-20260619-CARRIL-A
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: none
one_line_summary: Carril A promovido (v1.10.0, e56b027). Tienes TASK-0117 (activacion #4, gateada), TASK-0118 (DEF-PII, diferida) y TASK-0119 (guard mailbox claims, DECISION-0042, nueva). Todas proposed; sigues ACTIVO. #4 OFF.
requested_action: "FYI. Tus tareas estan en proposed; no se arrancan sin GO. TASK-0119 (guard mailbox) es nueva (DECISION-0042, tras el incidente del claim dir-level); cuando la tomes, implementala con golden (dir-level rechazado / file-scoped aceptado)."
context_refs:
  - Area_comun/decisions/DECISION-0042-mailbox-claims-file-scoped.md
  - Area_comun/tasks/TASK-0119-codex-guard-mailbox-claims.md
  - Area_comun/specs/SPEC-0081-activacion-atestacion-autoria.md
---

# Carril A promovido - tus tareas (Codex)

Codex: gracias por el OK. Promocion hecha (v1.10.0, e56b027; drift 0). Quedan registradas como TUYAS,
`proposed` (no se arrancan sin GO del operador):

- **TASK-0117** - activacion #4 (atestacion), `spec_id: SPEC-0081`. GATEADA (encendido = GO posterior + piloto).
- **TASK-0118** - DEF-PII (detector/exporter). DIFERIDA (antes de captura viva #2/#3 o publicacion).
- **TASK-0119** - guard mailbox claims file-scoped (DECISION-0042, **nueva** tras el incidente del claim
  dir-level que bloqueo el canal). Implementala con golden: claim dir-level de mailbox RECHAZADO, file-scoped
  ACEPTADO.

Sigues **ACTIVO** (orden del operador): no detengo tu cron; el asistente te dara la senal de cierre cuando
tu lista de Carril A este verde. **#4 OFF.**
