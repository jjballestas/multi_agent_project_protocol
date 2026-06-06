---
spec_id: SPEC-0031-runtime-observability
task_id: TASK-0032
type: implementation
status: ready
linked_decisions: [DECISION-0009, DECISION-0001]
created_at: 2026-06-06
author: Claude
---

# SPEC-0031 — Runtime observability: métricas + budget + run-log enriquecido + trazas

## Contexto
Runtime M2, **hito 1 (observabilidad primero**, dirección del operador 2026-06-06): antes de los
adapters LLM reales y el loop autónomo, el runtime necesita ser **auditable**. Hoy `runtime/runlog.py`
emite una línea JSONL básica por turno (`turn`, `unit`, `agent`, `outcome`, `transition`, `gate_green`,
`commit`, `reverted`). Esta spec lo **enriquece** con trazas por fase y coste/duración, añade un **budget**
(techo duro de iteraciones/coste) y un **resumen de métricas** por run. Ver
[DISENO-runtime-m2.md](../artifacts/DISENO-runtime-m2.md) §4. Bajo DECISION-0009 (aditivo, off-by-default).

## Alcance
- `runtime/runlog.py` (extender): cada entrada de turno añade `trace` (lista ordenada de fases),
  `changed_paths` (lista declarada por el turn report), `cost` (tokens declarados por el report; `null`
  en replay si no los declara), `duration_ms` (medido) y `collision_avoided` (bool/contador). Mantiene
  `run_id`, `sort_keys` y una línea por turno.
- `runtime/budget.py` (nuevo): `Budget(max_iter, max_cost_tokens)` con `consume(...)`/`exceeded()`;
  cuando se agota, el loop **para** con `outcome:"budget_exhausted"` y escribe el resumen.
- `runtime/metrics.py` (nuevo): `summarize(run_log_path) -> dict` deriva `turns_total`, `turns_per_task`,
  `gates_green_pct`, `reverts`, `collisions_avoided`, `cost_total`, `cost_per_task`. (La duración total
  se reporta pero **se excluye** de las aserciones golden por no ser determinista.)
- `runtime/orchestrator.py` (extender `--run`): integra `--budget-tokens N` (junto al `--max-iter`
  existente); al cerrar el run escribe `runtime/runs/RUN-<id>.summary.json` y lo imprime.
- **Determinismo inyectable** (lección de SPEC-0030 `--run-id`): un reloj inyectable (`--clock-fixed`
  o callable por defecto fijo en tests) y el `cost` tomado del report ⇒ el golden asegura el **esqueleto
  determinista** (trace, outcome, transición, gate, commit, changed_paths, métricas de conteo/coste) y
  **excluye** los campos de reloj (`duration_ms`).

## No-alcance
- **NO** implementa adapters LLM reales (`claude_adapter`/`codex_adapter`) ni el loop autónomo
  Claude↔Codex ni mailbox automation (hitos posteriores de M2). No cambia el router (SPEC-0027), el
  validador de turno (SPEC-0026), ni el motor apply/gate/vcs (SPEC-0029). No toca `--plan`.

## execution_pipeline
1. **runlog enriquecido:** la entrada por turno crece con `trace`/`changed_paths`/`cost`/`duration_ms`/
   `collision_avoided`; el orquestador rellena `trace` con las fases ya existentes del tick (gate_pre →
   route → claim → adapter → validate → human_gate → apply → gate_post → commit).
2. **budget:** `Budget` se consulta antes de cada turno y consume `cost` tras cada turno; al exceder
   `max_iter` o `max_cost_tokens` ⇒ para con `outcome:"budget_exhausted"`.
3. **summary:** al cerrar el run, `metrics.summarize` lee el JSONL y escribe `RUN-<id>.summary.json`.
4. **off-by-default:** sin `runtime.enabled:true`, `--run` sigue abortando; `--plan` intacto.

## acceptance_criteria
- Un replay run produce run-log enriquecido: cada línea tiene `trace` (fases ordenadas), `changed_paths`,
  `cost` y `collision_avoided`; el golden asegura esos campos deterministas y **excluye** `duration_ms`.
- `--budget-tokens N` con reports cuyo `cost` declarado supera N ⇒ el loop para con
  `outcome:"budget_exhausted"` + summary; `--max-iter N` sigue cortando en N.
- `RUN-<id>.summary.json` con métricas exactas: `turns_total`, `gates_green_pct`, `reverts`,
  `collisions_avoided`, `cost_total`, `cost_per_task` (aserción golden).
- Determinismo preservado (RUN-id + reloj inyectado ⇒ golden estable); `--plan` sin regresión;
  `runtime.enabled:false` ⇒ `--run` aborta (intacto).
- Run-log básico de SPEC-0030 sigue siendo un **subconjunto** (back-compat: campos nuevos aditivos).

## linked_decisions
- `DECISION-0009` (runtime, observabilidad/ROI §4 del diseño M2); `DECISION-0001` (aditivo,
  off-by-default ⇒ MINOR).

## test_plan
- Golden replay sobre repo-fixture en `examples/runtime_observability_cases/`: (1) run-log enriquecido
  con trace+changed_paths+cost (excluye duración); (2) `--budget-tokens` agota ⇒ `budget_exhausted` +
  summary; (3) `--max-iter` corta; (4) `RUN-<id>.summary.json` con métricas exactas; (5) `--plan` sin
  diffs; (6) `enabled:false` ⇒ `--run` aborta. Validador + scan de neutralidad verdes (runtime/** neutral).

## closure_criteria
- run-log enriquecido + `budget.py` + `metrics.py` + summary por run + `--budget-tokens`; golden
  deterministas verdes; `--plan` y off-by-default sin regresión; back-compat del run-log básico;
  revisión del arquitecto OK; claim liberado.

## Risks
- **No determinismo por reloj/coste.** Mitigación: reloj inyectable + `cost` desde el report; golden
  excluye `duration_ms`. (Misma lección que el `--run-id` de SPEC-0030.)
- **Acoplar métricas al loop.** Mitigación: `metrics.summarize` opera **post-hoc** sobre el JSONL; el
  loop solo emite líneas. Cambiar métricas no toca el loop.
- **Coste en replay = `null`.** Mitigación: las métricas de coste toleran `null` (no rompen el summary);
  el coste real llega con los adapters reales (hito siguiente de M2) sin cambiar el contrato del run-log.

## Traceability
| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| Run-log enriquecido (trace/cost/changed_paths) | TASK-0032 | golden enriched | campos deterministas asertados |
| Budget como techo duro | TASK-0032 | golden budget_exhausted | loop para + summary |
| Resumen de métricas por run | TASK-0032 | golden summary | RUN-<id>.summary.json exacto |
| Determinismo + off-by-default intactos | TASK-0032 | golden plan/enabled-false | sin regresión |
