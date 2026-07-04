---
message_id: MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-amplia-cola-pre-sello
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: false
created_at: 2026-07-04
context_refs:
  - MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-cola-pre-sello (items 2/3 en curso; este AMPLIA)
  - NOVA_ESTUDIO_Particion_Baseline_vs_Gobernado.md (familia de unidades + pool Q4 + PAR-2 condicional)
  - personal/operador/vision-nova/SELLO-ETAPA-1-nova-budget-DRAFT.md (placeholders a llenar)
one_line_summary: "AMPLIACION de la cola sin-idle (churneas rapido). Backlog profundo pre-sello, en orden: (2-ext) COMPLETA la familia de SPECs -- lista explicita: P3.1-P3.5, P4.2/P4.3/P4.4, PAR-2 condicional (Annul_* si hardening entrega <=15-jul) -- con las restricciones de estudio ya horneadas en P2/P4-001; (3) ENUMERA el pool Q4 nominalmente para el sello; (4) RUTEA las SPECs entregadas (P2-001..004, P4-001, + las nuevas) al ANALISTA para un GATE BASELINE de SPECs (deja el baseline atestado antes de Sprint 1; usa al Analista, caza omisiones tipo F-0246-01 ahora); (5) FINALIZA el SELLO draft (llena TODO lo llenable; deja solo sorteo-dia + estimates-operador); (6) PROGRAMA/RUTEA a Codex la deuda del harness de test del front de Nova-Budget (foundation-completion, EXCLUIDA, antes del front P2). Relleno paralelo: TASK-0245 (watchdogs->skills) + F1.6 (aprendizajes-externos) si hay holgura. Sello 08-jul manda; dev medido NO abre pre-sello."
requested_action: "[DIRECTIVA] Churneas rapido -> AMPLIO tu cola sin-idle con backlog profundo (trabaja en orden de prioridad; el sello 08-jul es el reloj; el dev MEDIDO no abre pre-sello -- todo esto es arq+docs/coordinacion). (2-EXTENDIDO) COMPLETA LA FAMILIA DE SPECs (bajo TASK-0246, mismas restricciones que horneaste en P2/P4-001: adversarial en sesion separada, checker_formal=0 baseline, deuda front, correlation+task_id, no reimplementar SQL en C#, db_verified_at contra proc desplegado, q4_membership explicita): familia P3 -> P3.1 Initial Budget Draft (primera_unidad, alcance congelado) + P3.2/P3.3/P3.4 Drafts (condicionadas a su DEC cerrada) + P3.5 Payment Draft (frontera Treasury, criticidad alta, fuera de Q4); mutadores restantes -> P4.2 Apply_Availability_Adjustment + P4.3 Apply_Commitment_Adjustment (miembros de PAR-1, heredan el patron congelado de P4.1) + P4.4 Apply_Obligation_Adjustment; PAR-2 CONDICIONAL -> Annul_Availability_Certificate / Annul_Commitment (SOLO superficie API sobre proc existente; condicion: nova-hardening entrega ambos procs verificados <=15-jul; si no, PAR-2 cae -- registra el trigger; el dev JAMAS crea los procs, regla 8). (3) ENUMERA EL POOL Q4 NOMINALMENTE para el sello (P4.4, P3.2/3/4, P2.3, P6.3, Get_*_List uno-a-uno con vista verificada contra el conector readonly). (4) RUTEA LAS SPECs ENTREGADAS AL ANALISTA PARA UN GATE BASELINE (P2-001..004, P4-001, y las nuevas segun las cierres): deja un baseline de SPECs ATESTADO antes de Sprint 1; el Analista verifica completitud/citas/q4_membership (caza las omisiones tipo F-0246-01 ANTES del dev, no durante). Es review de artefacto, pre-dev, no cuenta como checker_formal de ninguna tarea medida. (5) FINALIZA EL SELLO DRAFT: llena TODOS los placeholders [LLENAR-AL-SELLAR] que YA se pueden llenar (manifiesto+sha256 ya pre-armados, direccion de schema, hallazgos del piloto, familia de unidades, pool Q4 enumerado); deja SOLO pendientes el sorteo-del-dia (semilla NIST + T + sha256) y los estimates S/M/L del Operador. (6) PROGRAMA Y RUTEA A CODEX la deuda del harness de test del front de Nova-Budget (apps/nova-web): agregar el harness que corra VERDE en clon limpio (npm ci && npm test), como foundation-completion (EXCLUIDA del contraste, es cierre de GOAL-P1, NO dev medido de P2) -- debe estar antes de las unidades front P2. RELLENO PARALELO (si hay holgura, prioridad baja): TASK-0245 (portar watchdogs a la capa neutral skills/) y F1.6 (aprendizajes-externos, extraccion de reglas). NOTA: los estimates S/M/L y el sandbox de mutadores (<=14-jul, gatea P4.x) son del OPERADOR; no los generes. Cualquier bloqueo -> mailbox con pregunta concreta, no idle."
question: ""
---

# DIRECTIVA - Amplia la cola pre-sello (backlog profundo)

Churneas rapido; amplio tu cola. Trabaja en orden de prioridad; el sello 08-jul manda; dev medido NO abre pre-sello.

## 2-EXT - Completa la familia de SPECs (bajo TASK-0246, restricciones de P2/P4-001)
- **P3:** P3.1 Initial Budget Draft (primera_unidad) + P3.2/P3.3/P3.4 Drafts (cond. a DEC cerrada) + P3.5 Payment Draft (frontera Treasury, fuera Q4).
- **P4 restantes:** P4.2 Apply_Availability_Adjustment + P4.3 Apply_Commitment_Adjustment (PAR-1, heredan patron congelado de P4.1) + P4.4 Apply_Obligation_Adjustment.
- **PAR-2 condicional:** Annul_Availability_Certificate / Annul_Commitment (solo superficie API sobre proc EXISTENTE; cond: hardening entrega ambos procs <=15-jul; si no, PAR-2 cae; el dev NUNCA crea el proc, regla 8).

## 3 - Enumera el pool Q4 nominalmente (para el sello)
P4.4, P3.2/3/4, P2.3, P6.3, Get_*_List uno-a-uno con vista verificada contra el conector readonly.

## 4 - Rutea las SPECs al Analista para un GATE BASELINE
P2-001..004 + P4-001 + las nuevas: deja el baseline de SPECs atestado antes de Sprint 1; el Analista caza omisiones tipo F-0246-01 ANTES del dev. Review de artefacto, no cuenta como checker_formal.

## 5 - Finaliza el SELLO draft
Llena todo lo llenable (manifiesto+sha256, schema, hallazgos, familia, pool Q4); deja solo sorteo-del-dia + estimates-operador.

## 6 - Rutea a Codex la deuda del harness de test del front
apps/nova-web con `npm ci && npm test` verde en clon limpio (foundation-completion, EXCLUIDA, antes del front P2).

Relleno paralelo (holgura, baja prioridad): TASK-0245 (watchdogs->skills) + F1.6 (aprendizajes-externos).
NOTA: estimates S/M/L y sandbox de mutadores (<=14-jul) son del OPERADOR; no los generes. Bloqueo -> mailbox, no idle.
