---
spec_id: SPEC-0045-fase6.1-observabilidad-nagente
task_id: TASK-0059
type: implementation
status: accepted
created_at: 2026-06-07
author: Claude (arquitecto)
linked_decisions: [DECISION-0015, DECISION-0009, DECISION-0018]
relates_to: [SPEC-0031, SPEC-0038]
---

> SPEC de la Fase 6.1 (observabilidad N-agente) - cierra parte de D0 (motor). Es el DELTA sobre la
> observabilidad del M2 (TASK-0032: metrics.py/runlog.py/budget.py ya existen), NO rehacerlo. Aditiva,
> config-gated, fallback N=2 byte-equivalente. NO requiere DECISION nueva. Fase 6.2 (A10 budget) va aparte.

# SPEC-0045 - Fase 6.1: observabilidad N-agente (trace_id/spans + metricas)

## 1. Linea base (M2, NO rehacer)

- `runtime/runlog.py`: `turn_entry` con campo `trace` (lista por turno) + run_id determinista.
- `runtime/metrics.py`: `summarize()` post-hoc de 1 run-log: turns, gates_green_pct, reverts,
  collisions_avoided, cost_total/per_task, duration. SIN metricas N-agente.
- `runtime/eventlog.py`, `router.py`, `review_qa.py`: SIN trace_id/span.

## 2. Alcance (TASK-0059) = DELTA N-agente

1. **trace_id por evento** en `runtime/eventlog.py` (aditivo): id **DETERMINISTA** derivado de
   run_id+task+attempt+seq (sin reloj/random) => preserva replay y negative-replay (A6). El trace_id NO
   debe alterar el hash canonico del snapshot de forma no-determinista (o se excluye del hash, o se incluye
   de forma determinista).
2. **span por transicion** (aditivo): el router (decision) y la maquina review/qa (event) anotan un span
   `{trace_id, parent, name, attrs}` en el run-log/evento. Sin observabilidad activa => byte-equivalente.
3. **metricas N-agente** en `runtime/metrics.py` (extender, aditivo): `summarize_nagent()` que computa
   desde el event log + run log: distribucion de routing por agente (+ fairness), ciclos QA por tarea,
   conflictos/rechazos de fencing, escalados (architect_review/blocked), exclusiones de autor (I1/I2).
   Post-hoc, determinista.

## 3. Invariantes

- **O1:** trace_id por evento determinista; `replay(log)` reproduce el mismo hash canonico; negative-replay
  (A6) intacto (sin invocar red/reloj).
- **O2:** metricas N-agente derivadas SOLO de logs (post-hoc), deterministas, sin red/reloj.
- **O4:** aditivo/config-gated; sin observabilidad activa => byte-equivalente; fallback N=2 intacto.

## 4. Tests (golden examples/runtime_observability_nagent_cases, determinista)

1. trace_id presente y determinista (mismo event-log => mismos trace_id; dos corridas mismo hash).
2. span por transicion (router decision + review/qa event) anotado.
3. `summarize_nagent()` correcto sobre un event-log sintetico (routing/QA/conflictos/escalados/exclusiones).
4. replay con trace_id reproduce el mismo hash canonico de snapshot (negative-replay safe).
5. sin observabilidad activa => byte-equivalente (suite existente verde, fallback N=2). + CI.

## 5. Fuera de alcance

- OTel/exporters externos (A12: trace_id/run_id + run-logs estructurados en el nucleo; el resto de OTel
  diferido). Fase 6.2 (A10 budget/deadline). Fase B, Fase 7. Activar el runtime (gateado).
- Cambio incompatible de contrato => blocked + DECISION.

## 6. SemVer: MINOR (observabilidad aditiva, config-gated, default off => comportamiento actual).
