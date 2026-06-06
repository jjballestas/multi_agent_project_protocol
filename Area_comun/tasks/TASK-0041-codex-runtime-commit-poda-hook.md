---
id: TASK-0041
owner: Codex
status: done
type: implementation
priority: high
created_at: 2026-06-06
updated_at: 2026-06-06
depends_on: [TASK-0036]
relates_to: [TASK-0040, TASK-0034]
phase: P2
spec_id: Area_comun/specs/SPEC-0037-runtime-commit-poda-hook.md
linked_decisions: [DECISION-0009, DECISION-0014, DECISION-0001]
execution_pipeline: [commit_turn con verify=False (git commit --no-verify) en la ruta del runtime conservando validacion de policy-paths, auto-mantenimiento de poda en el orquestador (prune --check al cierre del run; si due prune --apply + commit de mantenimiento separado), atomicidad ante fallo de commit (VcsError => discard_worktree_changes + block_task sin propagar), golden con hook instalado en fixture]
acceptance_criteria: [un turno que cierra tarea con poda due COMMITEA igual (hook no bloquea al runtime), tras cruzar umbral el runtime se auto-poda y el repo queda prune not-due, fallo de commit => worktree restaurado + tarea blocked sin estado a medio aplicar, commits manuales siguen gateados por el hook, default replay + golden existentes intactos]
test_plan: [golden en examples (o extender runtime_loop_cases) en fixture temporal con el pre-commit hook + scripts instalados; estado que al cerrar cruza released_count>4; verificar commit del turno + auto-poda not-due + caso commit-fail (worktree limpio + blocked); sin red; .ps1 n/a]
closure_criteria: [commit_turn --no-verify (runtime) + auto-mantenimiento de poda + atomicidad ante fallo de commit, golden verdes, camino manual + default replay sin regresion, handoff autocontenido, claim liberado al pasar a in_review]
---

# TASK-0041 - Runtime commit robusto frente al pre-commit hook de poda

> `implementation` -> SDD; implementar contra [SPEC-0037](../specs/SPEC-0037-runtime-commit-poda-hook.md).
> **Follow-up priorizado por el operador.** Defecto hallado en la PRIMERA CORRIDA REAL sobre el repo vivo
> (TASK-0040).

## Resumen
`runtime/vcs.py` `commit_turn` commitea SIN `--no-verify`, asi que el commit del propio runtime dispara el
pre-commit hook de poda (`prune --check`). Cerrar una tarea libera un claim y puede cruzar
`released_count>4` => el hook **bloquea el commit del runtime** dejando el worktree a medio aplicar (apply
ya muto el estado antes del commit). Arreglo: (1) el runtime commitea con `--no-verify` (es escritor unico
con su propio `run_gate`: validador + neutralidad por turno; el hook es para commits manuales); (2) el
runtime se **auto-poda** (DECISION-0014 maintenance turn) al cierre del run si esta due, en un commit de
mantenimiento separado; (3) **atomicidad**: si el commit falla, `discard_worktree_changes` + `block_task`
(como el camino de gate rojo), nunca medio-aplicado.

## Evidencia (TASK-0040, 2026-06-06)
En la corrida real hubo que archivar 1 claim released a mano para que el commit del runtime no cruzara
`released_count>4` y el hook no lo bloqueara. Sin ese workaround, el turno habria quedado a medio aplicar.

## archivos objetivo (previstos)
- `runtime/vcs.py` (`commit_turn` con `verify`)
- `runtime/orchestrator.py` (auto-mantenimiento de poda + atomicidad ante fallo de commit en `run_loop`)
- `examples/` (golden con hook instalado en fixture)

## Dogfood
Liveness por turno + handoff-release (commitea WIP y libera claim al pasar a in_review). ASCII-only en
mailbox/state (DECISION-0012). Nota: si consideras `--no-verify` un cambio de politica, levanta la
pregunta (blocked + 1 pregunta) en vez de asumir; el arquitecto lo trata como extension de 0009/0014.
