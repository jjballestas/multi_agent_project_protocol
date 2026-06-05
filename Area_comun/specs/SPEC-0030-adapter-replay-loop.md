---
spec_id: SPEC-0030-adapter-replay-loop
task_id: TASK-0031
type: implementation
status: ready
linked_decisions: [DECISION-0009, DECISION-0001]
created_at: 2026-06-05
author: Claude
---

# SPEC-0030 — Interfaz AgentAdapter + replay adapter + loop `--run`

## Contexto
Runtime M1 (DECISION-0009): cierra el loop de forma **determinista** sin invocar LLMs. Define la
interfaz vendor-neutral `AgentAdapter` y un **replay adapter** (report pre-escrito), y extiende el
orquestador con `--run`. Ver [DISENO-runtime-m1.md](../artifacts/DISENO-runtime-m1.md) §2-§3, §5-§6.
Depende de SPEC-0029 (apply+gate+vcs).

## Alcance
- `runtime/adapters/base.py`: `AgentAdapter` (Protocol) + tipos `ContextPack`/report.
- `runtime/adapters/replay.py`: `run_turn` devuelve el report desde `context.replay_report_path`.
- `runtime/orchestrator.py`: `--run` (aplica de verdad), `--once`, `--max-iter N`; `--plan` sin cambios.
- `runtime/runlog.py`: `RUN-<id>.jsonl`, una línea por turno.

## No-alcance
- No implementa adapters de LLM real (`claude_adapter`/`codex_adapter` = M2). No automatiza el ciclo
  multi-agente sin humano (M2). No cambia el router (SPEC-0027) ni el validador de turno (SPEC-0026).

## execution_pipeline
1. **base.py:** `AgentAdapter.run_turn(*, context, root) -> dict` (un turn report conforme a
   `turn_schema.json`). `ContextPack` mínimo (task, rutas de specs/decisions, `replay_report_path`).
2. **replay.py:** lee y devuelve el report del fichero; sin red; determinista.
3. **orchestrator `--run`:** ejecuta el `tick` del DISENO §2: gate_pre → router → (claim) → adapter →
   `validate_turn` → gates humanos → `apply_turn` → gate_post → commit/revert (SPEC-0029) → run-log.
   `--max-iter N` y parada por `none`/gate humano. `--plan` permanece read-only.
4. **off-by-default:** sin `runtime.enabled:true`, `--run` aborta con mensaje (solo `--plan`); con enabled,
   `--run` opera.
5. **run-log:** una línea JSON por turno (unit, agent, outcome, transición, gate, commit/skip).

## acceptance_criteria
- Replay de un report `ready→in_review` con `--run --once` ⇒ exactamente 1 turno aplicado + 1 commit.
- Replay de una secuencia ⇒ orden determinista; `--max-iter N` corta en N.
- Report `human_required` en la secuencia ⇒ el loop **para** antes de continuar (parada dura).
- `--plan` sigue sin mutar (regresión del comportamiento M0).
- `runtime.enabled:false` ⇒ `--run` no opera (comportamiento actual intacto).
- Misma interfaz para replay y (futuro) real: cambiar adapter no cambia el loop.

## linked_decisions
- `DECISION-0009` (loop, adapters vendor-neutral); `DECISION-0001` (aditivo, off-by-default ⇒ MINOR).

## test_plan
- Golden replay sobre repo-fixture: `--run --once` (1 commit), secuencia con `--max-iter`, parada por
  `human_required`, `--plan` sin diffs, `enabled:false` ⇒ `--run` aborta.

## closure_criteria
- Interfaz + replay + `--run`/`--max-iter` + run-log; golden deterministas verdes; `--plan` sin
  regresión; off-by-default respetado; revisión del arquitecto OK; claim liberado.

## Risks
- Acoplamiento accidental loop↔replay. Mitigación: el loop depende solo de `AgentAdapter`; replay es un
  adapter más (el real entra en M2 sin tocar el loop).

## Traceability
| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| Loop determinista vía replay | TASK-0031 | golden secuencia | orden estable |
| `--run --once` = 1 turno/commit | TASK-0031 | golden once | git log +1 |
| Parada por gate humano | TASK-0031 | golden human_required | loop se detiene |
| Off-by-default y `--plan` intactos | TASK-0031 | regresión | sin mutación |
