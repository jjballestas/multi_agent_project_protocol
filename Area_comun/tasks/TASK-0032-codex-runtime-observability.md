---
id: TASK-0032
owner: Codex
status: done
type: implementation
priority: normal
created_at: 2026-06-06
updated_at: 2026-06-06
depends_on: [TASK-0031]
relates_to: [TASK-0029]
phase: P2
spec_id: Area_comun/specs/SPEC-0031-runtime-observability.md
linked_decisions: [DECISION-0009, DECISION-0001]
execution_pipeline: [runtime/runlog.py enriquecido (trace/changed_paths/cost/duration_ms/collision_avoided), runtime/budget.py (max_iter+max_cost_tokens, exceeded => budget_exhausted), runtime/metrics.py summarize(run_log)->dict, orchestrator --run integra --budget-tokens + escribe RUN-<id>.summary.json, reloj/coste inyectables para determinismo, Golden examples/runtime_observability_cases]
acceptance_criteria: [run-log enriquecido con trace+changed_paths+cost+collision_avoided (golden excluye duration_ms), --budget-tokens agota => budget_exhausted + summary, --max-iter corta, RUN-<id>.summary.json con metricas exactas (turns_total/gates_green_pct/reverts/collisions_avoided/cost_total/cost_per_task), --plan sin regresion, enabled:false aborta --run, run-log basico de SPEC-0030 es subconjunto (back-compat)]
test_plan: [Golden replay sobre repo-fixture en examples/runtime_observability_cases: enriquecido, budget_exhausted, max-iter, summary exacto, --plan sin diffs, enabled:false; validador + scan verdes]
closure_criteria: [run-log enriquecido + budget.py + metrics.py + summary por run + --budget-tokens, golden deterministas verdes, --plan y off-by-default sin regresion, back-compat del run-log basico, handoff con evidencia, claim liberado]
---

# TASK-0032 — Runtime M2 (hito 1): observabilidad (métricas + budget + run-log enriquecido + trazas)

> `implementation` → SDD; implementar contra [SPEC-0031](../specs/SPEC-0031-runtime-observability.md) y
> [DISENO-runtime-m2.md](../artifacts/DISENO-runtime-m2.md) §4 bajo DECISION-0009. **Observabilidad
> primero** (dirección del operador): base auditable **antes** de los adapters reales y el loop autónomo.
> Aditivo y off-by-default. Depende de TASK-0031 (loop `--run` + run-log básico).

## Resumen
Enriquece el run-log por turno con **trazas por fase** (gate_pre→route→claim→adapter→validate→
human_gate→apply→gate_post→commit), `changed_paths`, `cost` (del turn report; `null` en replay) y
`collision_avoided`. Añade `runtime/budget.py` (techo duro de iteraciones/coste ⇒ `budget_exhausted`) y
`runtime/metrics.py` (`summarize` post-hoc del JSONL ⇒ `RUN-<id>.summary.json`). El orquestador integra
`--budget-tokens` y emite el resumen al cerrar. **Determinismo:** reloj/coste inyectables; el golden
asegura el esqueleto determinista y **excluye** `duration_ms` (misma lección que el `--run-id` de 0031).

## archivos objetivo (previstos)
- `runtime/runlog.py` (enriquecer, manteniendo el básico como subconjunto), `runtime/budget.py` (nuevo),
  `runtime/metrics.py` (nuevo)
- `runtime/orchestrator.py` (añadir `--budget-tokens` + escribir/imprimir `RUN-<id>.summary.json`)
- `examples/runtime_observability_cases/` (golden deterministas)

## Coordinación
- Reusa el tick y el `RunLog` de TASK-0031 sin reabrir el motor apply/gate/vcs (TASK-0030).
- `metrics.summarize` debe operar **post-hoc** sobre el JSONL (no acoplar métricas al loop).
- Antes de codificar el reloj/summary, si dudas del mecanismo determinista, **pregunta por mailbox**
  (como con el `--run-id`): el golden no puede aserir wallclock.
- Handoff autocontenido con comandos golden + validador/scan.

## No-alcance (siguiente hito de M2)
- Adapters LLM reales (Claude/Codex tras `AgentAdapter`) = **hito 2** (límites claros + replay comparativo
  + sin activar autonomía). Loop autónomo y mailbox automation = hitos posteriores. No tocar aquí.
