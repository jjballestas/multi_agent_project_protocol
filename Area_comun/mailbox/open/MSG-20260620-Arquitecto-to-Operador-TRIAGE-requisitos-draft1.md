---
message_id: MSG-20260620-Arquitecto-to-Operador-TRIAGE-requisitos-draft1
task_id: none
type: DECISION
from: Arquitecto
to: Operador
status: open
requires_response: false
response_owner: Operador
one_line_summary: "Triage de los 4 requisitos del intake + DRAFT #1 (REQ-DCC3BC1A = reset del formulario + confirmacion id/seq tras EXECUTE). #1 es UX read-only -> extension de SPEC-0086 (AC21), SIN DECISION. Roadmap: #2 Help read-only (ext, sin DECISION); #3 mailbox-archive TOCA escritura (extiende DECISION-0052, accion acotada + prueba negativa); #4 auto commit+push = nueva superficie de TRANSPORTE -> requiere DECISION (regla 2). Autoro de a una; aqui va el #1."
context_refs:
  - personal/Arquitecto/carril_A/DRAFT-SPEC-0086-ext3-intake-reset-confirm.md
  - personal/Arquitecto/carril_A/DRAFT-TASK-0135-intake-reset-confirm.md
deadline_or_blocking_level: normal
---

# TRIAGE de los 4 requisitos + DRAFT #1 para ratificacion

Recupere el contenido de los 4 (seeds en el ledger, no en archivo). Triage por sensibilidad (tu secuencia):

| # | REQ | Que es | Superficie | DECISION? | SPEC |
|---|-----|--------|-----------|-----------|------|
| 1 | DCC3BC1A | reset form + confirmacion id/seq tras EXECUTE | UX read-only | NO | ext SPEC-0086 (AC21) [DRAFT AHORA] |
| 2 | FB27AF72 | vista Help (manual metodologia) | UX read-only | NO | ext SPEC-0086 (reusa docs/MANUAL-operador.md) |
| 3 | B65E7802 | archivar mailbox con 1 click | ESCRITURA (relay) | extiende DECISION-0052 (accion acotada nueva) | ext SPEC-0086 + prueba negativa impersonacion |
| 4 | 444E0DE5 | auto commit+push del intake | TRANSPORTE nuevo (git push + credenciales) | SI - DECISION (regla 2) | DECISION + ext SPEC-0086 |

Notas de triage:
- **#2 FB27AF72:** su TITULO esta mangleado ("arrancamos con nova.budget:") por el bug del #1; su NARRATIVA es
  clara (vista Help detallada, read-only, reusa docs/MANUAL-operador.md, honesta = lo que la app HACE hoy). Al
  autorarlo re-derivo el intent de la narrativa (no del titulo stale). Tras cerrar el #1, el reenvio dejara de
  manglearse.
- **#3 B65E7802:** TOCA el relay -> NO reabrir el 403 ni la impersonacion. Lo modelo como EXTENSION del
  conjunto acotado de DECISION-0052: nueva accion `mailbox-archive` con builder SERVER-SIDE, forma estricta,
  emite open->archived via submit_intent (nunca edita el mailbox directo), con PRUEBA NEGATIVA permanente
  (AC18/19/20). Evaluo si basta extender 0052 o amerita su propia DECISION; te lo digo en su draft.
- **#4 444E0DE5:** EL MAS SENSIBLE. Nueva superficie de TRANSPORTE (la app hace git push -> credenciales del
  remote). Por regla 2 va **DECISION primero** (commit ACOTADO a outputs de submit_intent, nunca working tree
  arbitrario; prueba negativa: un sucio ajeno no entra; push fallido = error NO verde, AC11; resultado atomico
  "enviado + aterrizado HEAD/seq"). Lo autoro al final, tras tu ratificacion de los previos.

## DRAFT #1 - REQ-DCC3BC1A (reset + confirmacion)
- **ext SPEC-0086 (AC21):** tras EXECUTE exitoso (applied+seq reales) el wizard muestra id (REQ-xxxx)+seq y
  RESETEA el formulario (campos vacios, paso 1, borrador, piiAck=false); si el execute FALLA -> NO reset, NO
  verde, error real, borrador conservado (honestidad AC11). Test de comportamiento permanente.
- **TASK-0135** (ready/Codex; UX read-only; codigo Zeus-protocol). SIN cambio de superficie de escritura;
  #4 byte-identica; carry AC11/12/13.
- Drafts: personal/Arquitecto/carril_A/DRAFT-SPEC-0086-ext3-intake-reset-confirm.md + DRAFT-TASK-0135-...md.

Ratifica el #1 para promover (ext SPEC-0086 -> GO TASK-0135 a Codex). Voy de a una; al cerrar #1 sigo con #2.
#4 epoca 1.14.0 byte-identica. Etapa 5 roster diferida.
