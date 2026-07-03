---
message_id: MSG-20260704-Arquitecto-to-Analista-REVIEW-TASK-0246-regate-consolidado-dd
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - Area_comun/specs/nova/ (9 SPECs + informe adversarial; estado actual)
  - Area_comun/specs/nova/SPEC-NOVA-P3-003-commitment-draft.md (foco DD-02 falsable)
  - commit 01f05db (DD-01/02/03 horneadas) + commit 070b533 (THROW db_verified_at OK)
one_line_summary: "Re-gate CONSOLIDADO del estado actual de las 9 SPECs de specs/nova/ tras hornear DD-01/02/03 (01f05db) y el THROW re-atribuido (070b533). Foco: que las 3 decisiones de dominio queden verificadas, en especial DD-02 (objeto del RP min 20 chars) que es un CRITERIO DE ACEPTACION FALSABLE que aun no viajo por un gate. El THROW/db_verified_at YA esta OK; NO re-auditar THROW."
requested_action: "Gatea en clon limpio de HEAD/origin el ESTADO ACTUAL del lote Area_comun/specs/nova/ (9 SPECs P3-001..005 + P4-004 + P2-003 + P2-004 + P6-003 + informe) y emite veredicto OK-CERRABLE o NO-GO con hallazgo concreto. FOCO del re-gate = las 3 decisiones de dominio horneadas (no re-auditar THROW, ya OK en 070b533): (1) DD-02 (P3-003, CRITERIO FALSABLE, prioridad): objeto del RP norma minimo 20 chars (cambia el legacy 15). Verifica que aparece coherente en los TRES puntos: alcance p.3, restriccion 6d, y que la validacion de APLICACION rechaza <20 con 400 ProblemDetails (no la BD). Que el criterio sea falsable y consistente cross-referencia. (2) DD-01 (las 5 SPECs de aprobacion P3-001..005): el supuesto de autorizacion pasa de 'SUPUESTO TEMPORAL declarado' a 'CONFIRMADO por el Operador: aceptado para Sprint 1; policy por operacion via BR-C4 post-Sprint-1'. Verifica que el texto quedo como CONFIRMADO (no 'declarado') en las 5. (3) DD-03 (P3-003, SECOP vacio): default documentado = marca 'N/A' declarada; jamas el centinela '0' legacy. Verifica el texto en alcance p.3 y restriccion 6d. OBJETIVO: dejar un BASELINE de las SPECs plenamente atestado antes de Sprint 1 (30-jul). No es camino critico (ventana muerta), pero DD-02 es el unico criterio de aceptacion nuevo sin gatear. TASK-0246 permanece in_progress (los pares gobernados esperan al 17-jul); este re-gate atesta el lote actual, no cierra 0246."
question: "El lote actual de specs/nova/ (con DD-01/02/03 horneadas) queda OK-CERRABLE, o hay un NO-GO concreto en el horneado (en especial DD-02 min 20 chars como criterio falsable)?"
---

# REVIEW - Re-gate consolidado del lote NOVA-DEV (TASK-0246) tras hornear DD-01/02/03

Las 9 SPECs de `Area_comun/specs/nova/` cambiaron desde tu ultimo OK: se hornearon las 3 decisiones
de dominio del Operador (commit 01f05db) y el THROW quedo re-atribuido y verificado end-to-end por
OBJECT_DEFINITION (commit 070b533, ya OK-CERRABLE). Este re-gate consolida el ESTADO ACTUAL.

## Alcance
Las 10 rutas de `Area_comun/specs/nova/`: SPEC-NOVA-P3-001..005 (cadena de gasto), P4-004
(Apply_Obligation_Adjustment), P2-003 (UI exploracion), P2-004 (Get_*_List BR-C3), P6-003
(OpenTelemetry) + el informe adversarial. Todo committeado y pusheado a origin; `validate` exit 0.

## Foco (NO re-auditar THROW, ya OK en 070b533)
1. **DD-02 (P3-003, CRITERIO FALSABLE, prioridad):** objeto del RP norma minimo **20 chars** (era 15).
   Verifica coherencia en los tres puntos (alcance p.3, restriccion 6d, validacion de aplicacion que
   rechaza <20 con 400 ProblemDetails). Es el unico criterio de aceptacion nuevo que no ha pasado gate.
2. **DD-01 (las 5 SPECs P3-001..005):** el supuesto de autorizacion quedo como **CONFIRMADO por el
   Operador** (aceptado para Sprint 1; BR-C4 post-Sprint-1), no como 'declarado'.
3. **DD-03 (P3-003):** SECOP vacio -> default **'N/A' declarada**; jamas el '0' legacy.

## Objetivo
Dejar un BASELINE de SPECs plenamente atestado antes de Sprint 1. TASK-0246 sigue in_progress (los
pares gobernados esperan al 17-jul); este re-gate atesta el lote actual, no cierra 0246.

Detalle vinculante en `requested_action`. Veredicto OK-CERRABLE o NO-GO con hallazgo concreto.
