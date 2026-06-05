---
id: TASK-0031
owner: Codex
status: ready
type: implementation
priority: normal
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0030]
relates_to: [TASK-0029]
phase: P2
spec_id: Area_comun/specs/SPEC-0030-adapter-replay-loop.md
linked_decisions: [DECISION-0009, DECISION-0001]
execution_pipeline: [runtime/adapters/base.py AgentAdapter + tipos, runtime/adapters/replay.py report desde fichero, orchestrator --run/--once/--max-iter (tick del DISENO) con --plan intacto, runtime/runlog.py RUN-<id>.jsonl, Golden replay deterministas (once=1 commit / secuencia max-iter / parada human_required / enabled:false aborta --run)]
acceptance_criteria: [--run --once aplica 1 turno + 1 commit, secuencia determinista y --max-iter corta en N, human_required para el loop, --plan sigue sin mutar, runtime.enabled:false => --run no opera, misma interfaz replay vs real]
test_plan: [Golden replay sobre repo-fixture: once, secuencia/max-iter, parada humana, --plan sin diffs, enabled:false]
closure_criteria: [Interfaz + replay + --run/--max-iter + run-log, golden deterministas verdes, --plan sin regresion, off-by-default respetado, handoff con evidencia, claim liberado]
---

# TASK-0031 — Runtime M1: AgentAdapter + replay + loop `--run`

> `implementation` → SDD; implementar contra [SPEC-0030](../specs/SPEC-0030-adapter-replay-loop.md) y
> [DISENO-runtime-m1.md](../artifacts/DISENO-runtime-m1.md) bajo DECISION-0009. Cierra el loop de forma
> **determinista** con un replay adapter (sin LLM). Depende de TASK-0030 (apply+gate+vcs).

## Resumen
Define la interfaz vendor-neutral `AgentAdapter` y un **replay adapter** (devuelve un report pre-escrito),
y extiende el orquestador con `--run`/`--once`/`--max-iter` ejecutando el tick completo (router →
adapter → validate_turn → apply → gate → commit/revert) con run-log. **`enabled:false`** sigue limitando
a `--plan`. El adapter de LLM real entra en M2 sin tocar el loop.

## archivos objetivo (previstos)
- `runtime/adapters/base.py`, `runtime/adapters/replay.py`, `runtime/runlog.py`
- `runtime/orchestrator.py` (añadir `--run`/`--once`/`--max-iter`)
- `examples/runtime_loop_cases/` (golden replay deterministas)
