---
message_id: MSG-20260620-Operador-to-Arquitecto-GO-ratifica-TASK-0135-reset-confirm
task_id: TASK-0135
type: DECISION
from: Operador
to: Arquitecto
status: open
requires_response: false
response_owner: Arquitecto
one_line_summary: "RATIFICO el requisito #1 (REQ-DCC3BC1A): reset del formulario del intake + confirmacion id/seq tras EXECUTE. UX read-only, SIN cambio de superficie de escritura, sin DECISION. Promueve ext SPEC-0086 (AC21) -> GO TASK-0135 a Codex. CONDICION DE CIERRE: AC21 con AC11 honesto VERDE (execute fallido -> NO reset, NO verde, error real, borrador conservado) como test de comportamiento permanente. Sigue de a una; al cerrar, retoma el #2 (Help). Canonico ya VERDE (TASK-0136 cerrada)."
requested_action: "Promueve ext SPEC-0086 (AC21) y emite GO TASK-0135 a Codex (maker; codigo en Zeus-protocol; tu checker). Alcance: tras un EXECUTE exitoso (applied+seq reales) el wizard muestra id (REQ-...) + seq y RESETEA el formulario (campos vacios, paso 1, borrador, piiAck=false); si el execute FALLA -> NO reset, NO verde, error real, borrador conservado (honestidad AC11). CONDICION DE CIERRE: AC21 verde como TEST DE COMPORTAMIENTO permanente (incluye el caso de fallo: que NO resetee ni pinte verde si no hubo write real); carry AC11/12/13 + AC22 (un intake deja el canonico verde); #4 epoca 1.14.0 byte-identica; validate con/sin secretos exit 0; drift 0; npm test verde. SIN cambio de superficie de escritura (read-only salvo el submit ya gobernado). maker=Codex/checker=Arquitecto, reproduccion desde clon limpio. Reporta el cierre en canonico. Tras cerrar, sigue con el #2 (REQ-FB27AF72 Help; re-deriva el intent de la narrativa, titulo mangleado; reusa docs/MANUAL-operador.md)."
question: none
context_refs:
  - personal/Arquitecto/carril_A/DRAFT-SPEC-0086-ext3-intake-reset-confirm.md
  - personal/Arquitecto/carril_A/DRAFT-TASK-0135-intake-reset-confirm.md
  - Area_comun/tasks/req-dcc3bc1a-requirement-seed.md
deadline_or_blocking_level: normal
---

# GO - ratifico el #1 (REQ-DCC3BC1A): reset + confirmacion del intake

Ratifico. Es UX read-only, sin DECISION, y arregla el bug de campos stale que estaba mangleando requisitos
(p.ej. el titulo del #2). Canonico ya VERDE tras TASK-0136, asi que se puede promover.

**Promueve:** ext SPEC-0086 (AC21) -> GO TASK-0135 a Codex.

**Condicion de cierre (innegociable):** AC21 verde como test de COMPORTAMIENTO permanente, e incluye el
caso de FALLO: si el execute no produjo write real, el wizard **NO resetea y NO pinta verde** (error real,
borrador conservado, AC11). Carry AC11/12/13 + AC22; #4 byte-identica; validate con/sin secretos exit 0;
drift 0.

Voy de a una: al cerrar el #1, sigue con el #2 (Help). Verifico tu cierre en canonico. Canal ASCII.
