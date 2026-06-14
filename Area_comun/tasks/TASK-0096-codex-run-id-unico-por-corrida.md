---
id: TASK-0096
owner: Codex
status: in_review
type: implementation
priority: normal
created_at: 2026-06-10
updated_at: 2026-06-10
depends_on: []
relates_to: [TASK-0091, DECISION-0013]
phase: P2
spec_id: none
linked_decisions: [DECISION-0013]
objective: (OFF-PILOT, follow-up del re-pilot SA.4) run_id UNICO por corrida del orquestador, para evitar el ruido de agregacion de metricas. Hoy el run_id por defecto es deterministico por hash del replay-input; en corridas con invoker real (sin replay) colisiona entre corridas (visto en el re-pilot: run_id RUN-487b91042c7c igual que el smoke), y el run_log RUN-XXXX.jsonl se ACUMULA -> metrics.turns_total/cost agregan entradas de corridas previas (el smoke + TASK-0040/0092 viejos) y dan numeros engañosos. El registro autoritativo de la corrida (turns array) era correcto, pero las metricas no.
expected_output: run_id unico por corrida cuando no hay replay-input deterministico (invoker real): derivarlo de un componente unico por corrida pasado por el caller (p.ej. un run-id explicito requerido para invoker real, o un contador/sufijo determinista por corrida que NO colisione). NUNCA usar Date.now()/random en codigo que deba ser determinista en goldens -> el caller (orquestador CLI) inyecta el componente unico; los goldens siguen pasando run-id explicito fijo. El run_log de una corrida NO debe agregar entradas de corridas previas (archivo por run_id unico, o no reusar un .jsonl existente). Golden/regresion que asevere que dos corridas reales consecutivas NO comparten run_log ni agregan metricas cruzadas. validador/neutralidad/encoding verdes; drift 0; determinista en CI.
question_to_resolve: Q1 fuente del componente unico sin romper determinismo de goldens (run-id explicito requerido para invoker real, vs sufijo por corrida inyectado por el caller). Q2 confirmar por golden que el run_log no se reusa/acumula entre corridas reales y que las metricas no agregan cruzado.
closure_criterion: run_id unico por corrida real (sin colision); run_log por corrida sin acumulacion; metricas no agregan entre corridas; goldens deterministas siguen pasando con run-id explicito; validador/neutralidad/encoding verdes; drift 0; handoff con evidencia. OFF-PILOT: SA.4 de-armado, NO re-armar ni piloto.
sdd_required: true
---

# TASK-0096 - run_id unico por corrida (evita ruido de agregacion de metricas)

> PROPOSED (Claude 2026-06-10, follow-up #2 del re-pilot SA.4). OFF-PILOT. Pequena. SA.4 DE-ARMADO.

## Contexto

En el re-pilot SA.4 el run_id RUN-487b91042c7c colisiono con el del smoke; el run_log se acumulo y las
metricas (turns_total=6, cost_total=5 de TASK-0040) agregaron entradas viejas. El registro autoritativo
(turns array) era correcto, pero las metricas eran ruido. run_id debe ser unico por corrida real.

## Alcance

- runtime/orchestrator.py (generacion de run_id) + runtime/metrics.py / runlog: run_id unico por corrida
  cuando no hay replay deterministico; run_log no reusado/acumulado. Determinismo de goldens preservado
  (run-id explicito). Sin Date.now()/random en rutas que deban ser deterministas.
- Golden/regresion que asevere no-colision/no-agregacion entre corridas reales.

## Restricciones

- OFF-PILOT: SA.4 de-armado, NO re-armar ni piloto. enforce+authoritative ON. ASCII, sin secretos,
  determinista en CI. Template intacto. 1 commit/turno con rutas explicitas.
