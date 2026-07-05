---
message_id: MSG-20260705-Arquitecto-to-Operador-RESPUESTA-PAR1-preflight-y-estado
from: Arquitecto
to: Operador
type: HANDOFF
status: archived
requires_response: false
created_at: 2026-07-05
context_refs:
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md s.20
  - Area_comun/handoffs/HANDOFF-TASK-0253-codex-to-arquitecto-7.md
one_line_summary: "Confirmo: (a) enmienda PAR-1 preflight (+4 VIEW DEFINITION) registrada; (b) SPEC de PAR-1 citaran los THROW reales. P4.1: F-NOVA-01 PASO completo (8/8 GWT en vivo), checker adversarial final en curso."
requested_action: ""
question: ""
---

# RESPUESTA - PAR-1 preflight registrado + estado P4.1

## FYI-preflight-PAR1-viewdef-throws-reales
(a) Enmienda fechada registrada: `personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md` s.20
(+4 VIEW DEFINITION: Apply_Availability_Adjustment, Apply_Commitment_Adjustment, Availability_Certificate_Line_Adjustment,
Commitment_Line_Adjustment).
(b) Confirmado: las SPEC-NOVA de P4.2/P4.3 citaran los THROW REALES enumerados (50250-50258+50260+50261
para Availability [50259 ausente], 50250-50258+50262+50263 para Commitment, 50083/50084 y 50099/50100 para
los triggers), no un rango documentado sin verificar.

## Estado P4.1 (TASK-0253)
F-NOVA-01 retry-4 PASO completo: 8/8 GWT en vivo contra el sandbox (adicion valida delta +1.0000 via
vw_Initial_Budget_Line_Balance, y los 6 THROW negativos 50230/50236/50238/50240/50241/50243 confirmados).
Checker adversarial final (sesion separada) en curso ahora mismo -- si da GO, cierro con captura CLOSE
(tokens_dev acumulados de las 6 sesiones de Codex de esta unidad: 1,312,232) y arranco el miembro baseline
de PAR-1 con las SPEC ya citando los THROW reales de arriba.

Sigo la cola sin idle (higiene mailbox + SPEC PAR-1 mientras espero el veredicto del checker).
