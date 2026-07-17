---
message_id: MSG-20260717-Operador-to-Arquitecto-FIRMA-decisions-0100-0101
from: Operador
to: Arquitecto
type: FIRMA
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-17
context_refs:
  - Area_comun/decisions/DECISION-0100-adopcion-memoria-hibrida.md
  - Area_comun/decisions/DECISION-0101-checker-formal-proveedor-diverso.md
one_line_summary: "FIRMA del operador de DOS decisiones tal cual: DECISION-0100 (adopcion de la memoria hibrida, promocion al master hub Fase 3+ post-ventana) + DECISION-0101 (checker formal migra a Claude/Anthropic; maker!=checker por capacidad+llave+PROVEEDOR; capa hub + espejo 0096; re-juicios diferidos al nuevo proveedor). Autoriza sellar ambas via submit_intent decision. El probe de coste NO se ejecuta: pendiente de revision del operador + modelo + GO post-0005."
requested_action: "Sella DECISION-0100 y DECISION-0101 con submit_intent decision (patron 0091/0099): status -> active, approved_by: operador. NO ejecutes el probe de coste (el operador lo revisara aparte y elegira modelo local + dara GO post-cierre de TASK-0005)."
question: "Confirmas por mailbox el sello de 0100 y 0101 (tx seq) tras firmarlas?"
---

# FIRMA - DECISION-0100 (adopcion memoria hibrida) + DECISION-0101 (checker a proveedor diverso)

El operador APRUEBA y FIRMA ambas decisiones TAL CUAL (drafts del Arquitecto):

- **DECISION-0100** - la metodologia ADOPTA la memoria hibrida (por demostracion; nada citable).
  Promocion al master hub via export 0096 AGENDADA a Fase 3+ POST-ventana-medida (no toca scripts/
  del hub durante la ventana). Re-juicio formal U3/U4 via 0101. Runbook cierra normal. F2 minimo NO.
- **DECISION-0101** - el checker formal migra a Claude/Anthropic CLI; maker!=checker se sostiene por
  CAPACIDAD + POSESION DE LLAVE + PROVEEDOR (el checker no corre en el proveedor del maker). Capa
  HUB + espejo export 0096. Re-juicios diferidos (U3/U4) al nuevo proveedor. Los probes NO se
  degradan: se cambia el proveedor, no el mandato.

## Autorizacion del sello
Ejecuta submit_intent decision para AMBAS (patron 0091/0099): status -> active, approved_by:
operador. Guardrails intactos (fondo 2E35F26E / epoch 1.14.0 / N=500; firewall anti-HARKing; PII de
nomina fuera del store; DECISION-0081 intacta; estudio medido gated post-30-jul sin tocarse).

## Nota: el probe de coste NO se dispara aun
El operador quiere REVISAR el diseno del probe el mismo y elegir el modelo local; el GO de ejecucion
es post-cierre de TASK-0005/Fase A. NO lo arranques hasta su OK explicito.

Cierra los requires_response de los drafts 0100/0101. Adelante con los dos sellos.

-- Operador (via Asesor). Firma relevada: el operador aprobo en chat ("firmo 0100 y 0101"); el
   Asesor solo transmite, no firma por el.
