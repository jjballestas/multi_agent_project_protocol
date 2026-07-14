---
message_id: MSG-20260714-Operador-to-Arquitecto-FIRMA-decision-0097-gate1
from: Operador
to: Arquitecto
type: RESP
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-14
context_refs:
  - Area_comun/decisions/DECISION-0097-gate1-activacion-memoria-hibrida-nova-payroll.md
  - Area_comun/mailbox/open/MSG-20260714-Arquitecto-to-Operador-RESP-draft-gate1-para-firma.md
one_line_summary: "FIRMA del operador: apruebo DECISION-0097 (Gate-1, activacion scopeada de la memoria hibrida SOLO en Nova-Payroll). Sella via submit_intent y arranca la ceremonia de nacimiento. Fase A build sigue pendiente de su GO (freno Contabilidad-gana)."
requested_action: "Sella DECISION-0097 en el ledger del hub (submit_intent intent decision) y arranca la ceremonia de nacimiento de Nova-Payroll en NOVA-Suite/Nova-Payroll con el roster firmado (Julian firmante desde el genesis). NO arranques el build de Fase A: queda pendiente de su GO especifico (clausula 4)."
question: "Confirmas sellado + ceremonia de nacimiento iniciada, y reportas?"
---

# FIRMA - DECISION-0097 (Gate-1 activacion scopeada memoria hibrida)

FIRMO y apruebo la DECISION-0097 tal como esta redactada (draft hub c1f9606). Las 7 clausulas
quedan aceptadas sin cambios:

1. Activacion scopeada SOLO en Nova-Payroll, Fase A de la SPEC; F3+ fuera (exigen su propia DECISION).
2. Memoria OFF estructural Y vinculante en hub y en las instancias medidas (NOVA/Contabilidad/Budget)
   durante la ventana.
3. Firewall anti-HARKing: nada del probe es evidencia ni entra al corpus citable; solo indicios
   cualitativos para mi decision de adopcion.
4. Freno "Contabilidad gana": la Fase A solo arranca tras el sello de Etapa 2 o con ventana ociosa que
   yo declare; ante conflicto de recursos, Contabilidad prevalece. Esta clausula se copia al GO de Fase A.
5. Un solo DDL master (port del memdb via export born-operational).
6. Vehiculo/roster confirmados: Nova-Payroll aislada, roster Arquitecto/Codex/Analista + jball +
   Julian (jheredia) FIRMANTE DESDE EL GENESIS; guardrail PII de nomina desde el nacimiento.
7. Frontera dos-trios (DECISION-0095).

## Efecto que autorizo con esta firma
1. Sella DECISION-0097 en el ledger del hub (submit_intent intent decision).
2. Arranca la ceremonia de nacimiento de Nova-Payroll (papel/ceremonia; no compite con E2).
3. La Fase A queda pendiente de su GO especifico (no la arranques con esta firma).

El fondo pineado NO se toca (hub 2E35F26E / epoch 1.14.0 / dataset N=500 / sellos intactos).
Repo confirmado: NOVA-Suite/Nova-Payroll.
