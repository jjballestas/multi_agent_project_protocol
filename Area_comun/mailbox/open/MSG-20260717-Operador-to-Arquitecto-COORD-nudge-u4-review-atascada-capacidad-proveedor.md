---
message_id: MSG-20260717-Operador-to-Arquitecto-COORD-nudge-u4-review-atascada-capacidad-proveedor
from: Operador
to: Arquitecto
type: COORD
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-17
context_refs:
  - Area_comun/mailbox/open/MSG-20260717-Operador-to-Arquitecto-DIRECTIVA-decision-c-mover-checker-formal-otro-proveedor.md
one_line_summary: "NUDGE de coordinacion: la review FORMAL de U4 (ultima de Fase A) esta atascada ~24 min. Diagnostico del Asesor sobre el cron del Analista: 2 execs exit 1 por 'model at capacity' del proveedor (NO el classifier esta vez), y el cron marco el mensaje seen -> processable=0, no reintenta solo. Sugerencia: fallback informal checker Claude fuerte (ya cerro U3, sortea classifier Y capacidad OpenAI, cumple 0099 r3, checker_formal=0) o re-seen cuando haya capacidad. Refuerza tu (c) ya ruteada."
requested_action: "Destraba U4: usa el fallback informal (checker Claude fuerte, patron de U3) para cerrar Fase A ya, o re-seen del REVIEW para reintentar el formal cuando el proveedor tenga capacidad. NO degrades los probes. Reporta cuando U4 cierre."
question: "Cierras U4 con el fallback informal (rapido) o esperas capacidad del formal? El re-juicio formal se puede correr despues (o directamente en el nuevo proveedor de tu (c))."
---

# COORD - Nudge: U4 (ultima de Fase A) atascada en el gate formal

## Diagnostico del Asesor (cron del Analista, Nova-Payroll)
La review formal de TASK-0004 fallo 2 veces con `EXEC_EXIT code=1`; el err.log del ultimo run:
`ERROR: Selected model is at capacity. Please try a different model.` Es **capacidad del
proveedor** (OpenAI), NO el classifier cyber de U3. Tras los 2 fallos el cron marco el mensaje
`seen` -> los heartbeats posteriores dan `processable_messages=0`, asi que **NO reintenta solo**.
U4 lleva ~24 min sin cerrar; el resto de Fase A (U1-U3) esta done.

## Sugerencia (destrabe)
- **Rapido:** fallback informal = checker Claude fuerte (el mismo patron que cerro U3), que sortea
  TANTO el classifier COMO la capacidad de OpenAI. Cumple DECISION-0099 regla 3; marca
  `checker_formal=0` (honestidad de clase; Fase A = demostracion, no citable). El re-juicio formal
  se corre despues -- idealmente ya en el proveedor de tu **(c)** (directiva ruteada 96e5401).
- **Alternativa:** re-seen del REVIEW para reintentar el formal cuando OpenAI tenga capacidad.

## Lectura
Dos modos de fallo distintos del checker formal OpenAI en un mismo dia (classifier + capacidad)
**refuerzan la (c)**: mover el checker formal a un proveedor que autorice trabajo de seguridad Y sea
mas estable. No urge decidir el destino ahora; urge cerrar U4.

Guardrails intactos (PII fuera del store, fondo 2E35F26E/1.14.0/N=500, firewall, 0081). No degrades
los probes para pasar el filtro/capacidad.

-- Operador (via Asesor).
