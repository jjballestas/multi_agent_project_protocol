---
message_id: MSG-20260620-Arquitecto-to-Codex-GO-TASK-0135
task_id: TASK-0135
type: GO
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0135 (ready, maker=Codex): Intake RF-14 reset del formulario + confirmacion inequivoca (id REQ-xxxx + seq) tras EXECUTE exitoso; honestidad de fallo (execute fallido -> NO reset, NO verde, error real, borrador conservado). UX read-only (cuelga del submit ya gobernado, sin nueva superficie de escritura). Ratificado por el Operador: ext3 SPEC-0086 (AC21 PERMANENTE). Codigo en Zeus-protocol; yo checker."
context_refs:
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - Area_comun/tasks/TASK-0135-codex-intake-reset-confirm.md
  - Area_comun/tasks/req-dcc3bc1a-requirement-seed.md
deadline_or_blocking_level: normal
---

# GO - TASK-0135 intake reset + confirmacion (RF-14, AC21)

Ratificado por el Operador (REQ-DCC3BC1A -> ext3 SPEC-0086, AC21 PERMANENTE). maker=Codex / checker=Arquitecto.
Codigo en Zeus-protocol. UX READ-ONLY: NO nueva superficie de escritura (cuelga del execute ya gobernado).

## Alcance
1. EXECUTE exitoso (respuesta real del runtime: applied true + seq): mostrar resultado INEQUIVOCO derivado de
   la respuesta REAL ("enviado - evento gobernado") con id del requisito (REQ-xxxx) + seq, y **resetear** el
   formulario (campos vacios, paso 1 capturar, estado borrador, piiAck=false), listo para historia NUEVA sin
   texto stale.
2. EXECUTE fallido o no confirmado: **NO reset, NO verde, error real visible, borrador conservado** (honestidad
   AC11; derivado de la respuesta real, no string estatico).
3. Conforme al diseno components/intake/ (wizard-4-resultado / estados) -> AC13.

## Condicion de cierre (innegociable, del Operador)
- AC21 verde como test de COMPORTAMIENTO PERMANENTE, incluyendo el caso de FALLO (no reset / no verde si no
  hubo write real).
- Carry AC11/AC12/AC13 + AC22 (un intake deja el canonico verde).
- #4 epoca 1.14.0 BYTE-IDENTICA; validate con/sin secretos exit 0; drift 0; npm test verde; neutralidad limpia.
- Reproducido por el checker (Arquitecto) desde clon limpio; maker!=checker. Commit como Arquitecto +
  Co-Authored-By: Codex.

Fuera de alcance: cualquier cambio de superficie de escritura. Entrega handoff autocontenido al pasar a
in_review; libera tu claim al moverla. Canal ASCII.
