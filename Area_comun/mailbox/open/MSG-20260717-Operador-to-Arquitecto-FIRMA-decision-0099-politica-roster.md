---
message_id: MSG-20260717-Operador-to-Arquitecto-FIRMA-decision-0099-politica-roster
from: Operador
to: Arquitecto
type: FIRMA
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-17
context_refs:
  - Area_comun/decisions/DECISION-0099-politica-roster-peones-maker-only-checker-fuerte.md
  - Area_comun/mailbox/open/MSG-20260717-Arquitecto-to-Operador-RESP-politica-roster-decision-0099-draft.md
one_line_summary: "FIRMA del operador: aprueba DECISION-0099 (roster: peon maker-only + intake explicito + checker en modelo fuerte, capa HUB con espejo export 0096). Autoriza el sello via submit_intent decision (patron 0091); status draft-pendiente-firma -> active. Guardrails intactos."
question: "Sellas DECISION-0099 y confirmas por mailbox?"
requested_action: "Sella DECISION-0099 con submit_intent decision (patron DECISION-0091): status -> active con la referencia de la firma, approved_by = operador. Cablea el espejo en el export born-operational (DECISION-0096) como tarea de mantenimiento del template (no bloqueante)."
---

# FIRMA - DECISION-0099 (politica de roster)

El operador APRUEBA y FIRMA **DECISION-0099** tal como esta redactada (draft del Arquitecto,
b3ab81a). Las 3 reglas quedan aceptadas:

1. Peon = maker-only (nunca checker/orquestador/firmante de ratificacion).
2. Intake explicito obligatorio (DoR completo + contrato sin ambiguedad; tarea abierta no va a
   un peon).
3. El checker permanece en modelo fuerte (maker!=checker por CAPACIDAD ademas de por llave).

Aplicacion confirmada: **capa HUB (metodologia)**, aplica a toda instancia presente y futura, con
**espejo en el export born-operational (DECISION-0096)**. El trio actual de Nova-Payroll ya cumple;
la politica gatea la incorporacion futura de peones locales.

## Autorizacion del sello
Ejecuta `submit_intent decision` (patron DECISION-0091): status de la cabecera pasa a **active** con
la referencia de la firma y `approved_by: operador`. Guardrails intactos: fondo (2E35F26E / epoch
1.14.0 / N=500), firewall anti-HARKing, DECISION-0081, PII de nomina fuera del store. No altera
DECISION-0060.

Esto CIERRA el requires_response del RESP-draft-0099. Adelante con el sello.

-- Operador (via Asesor). Firma relevada: el operador aprobo en chat ("firmala"); el Asesor solo
   transmite, no firma por el.
