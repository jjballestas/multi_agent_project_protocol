---
decision_id: DECISION-0070
title: Modulo de estadisticas por agente y por peon (read-only) -- calidad (aceptada/rechazada), tokens (autoria vs revision), tiempo y coste por tarea, derivado del ledger + runlogs + provenance
status: accepted
ratified_at: 2026-06-29
date: 2026-06-29
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0069, DECISION-0064, DECISION-0050, DECISION-0022]
phase: P2
---

# DECISION-0070 - Modulo de estadisticas por agente y por peon

> ACCEPTED (operador ratifico por adelantado 2026-06-29: "encola modulo de estadisticas queda aprobado y
> ratificado desde ahora"). READ-ONLY, DOMAIN-NEUTRAL, no contamina el TFM (analisis, no escritura del ledger).

## Contexto

El operador quiere medir el desempeno del pool por niveles (jefes/peones de DECISION-0069): tarea bien ejecutada
vs rechazada, gasto de tokens por revision, tiempo consumido por tarea, coste. Base existente: `runtime/metrics.py`
(cost_per_task/tokens post-hoc) + `measure_context_cost.py`; Hermes ya muestra tokens/coste por SESION (reusable).
Falta la dimension POR AGENTE y POR PEON con calidad (accept/reject) y desglose autoria-vs-revision.

## Decision

1. **Agregador READ-ONLY** (script NUEVO, neutral) que deriva metricas del LEDGER + runlogs + provenance, SIN
   escribir el ledger ni tocar pineados del hub:
   - **Calidad por agente/peon:** tareas done vs changes_requested/rechazadas (de las transiciones `task_status`),
     tasa de aceptacion, nro de ciclos de revision.
   - **Tiempo por tarea:** de los timestamps de los eventos (ready->in_progress->in_review->done) -> lead/cycle time.
   - **Tokens y coste:** de los runlogs (`runtime/metrics.py` cost_per_task), desglosado AUTORIA (maker/peon) vs
     REVISION (checker/jefe) usando la provenance de DECISION-0069 (autor real + modelo) y el rol del que firma.
   - **Por peon:** una vez exista la provenance (DECISION-0069/TASK-0213), atribuye autoria a cada peon y su
     tasa aceptada/rechazada + tokens/revision; antes de eso, la dimension agente ya funciona desde el ledger.
2. **Exposicion:** salida JSON del agregador + una VISTA en el panel Zeus-Aegis (read-only, reusa el patron de
   `/api/governance/*`). El panel reusa lo de Hermes para tokens/coste de sesion; la metodologia aporta la
   dimension por-agente/peon + calidad.
3. **Dependencia:** la dimension POR PEON depende de la provenance de TASK-0213; por eso el agregador
   (TASK-0214) se construye primero (dimension agente desde el ledger) y la atribucion por-peon se completa cuando
   0213 cierre. La vista del panel es trabajo de PRODUCTO (Zeus-Aegis), SDD/tarea aparte.
4. **GUARDRAIL TFM (igual que 0069):** todo es READ-ONLY y se construye FUERA del core pineado del hub; cero
   deltas en `eventlog.py`/validador/`protocol.config.json`/override/pre-registro hasta cerrar los 500. El
   agregador solo LEE.
5. **Neutralidad:** agregador y vista son DOMAIN-NEUTRAL; nada de dominio (NOVA/PII) en el core.

## Consecuencias

- SDD: SPEC-0109 + TASK-0214 (agregador read-only, maker=Codex/checker=Arquitecto) ahora; la vista del panel
  (producto Zeus-Aegis) como tarea siguiente tras el agregador. El agregador suma eventos gobernados al dataset.
- Rollback: borrar el script/vista nuevos; nada del core tocado.
