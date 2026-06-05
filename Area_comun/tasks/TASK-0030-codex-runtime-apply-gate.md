---
id: TASK-0030
owner: Codex
status: done
type: implementation
priority: normal
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0029]
relates_to: [TASK-0028, TASK-0031]
phase: P2
spec_id: Area_comun/specs/SPEC-0029-turn-apply-gate.md
linked_decisions: [DECISION-0009, DECISION-0007, DECISION-0011, DECISION-0001]
execution_pipeline: [runtime/vcs.py commit_turn/revert_last con write-allowlist dura, runtime/apply.py apply_turn (task_status/claims/mailbox/handoff) precondicion validate_turn, runtime/gate.py run_gate reusa validador+scan, Golden sobre repo-fixture git (valido=1 commit / gate-rojo=revert+blocked / path-politica=rechazo)]
acceptance_criteria: [Report valido ready->in_review aplica estado coherente y produce 1 commit, Gate rojo => revert deja arbol identico + tarea blocked, commit_turn rechaza paths de politica sin allow_policy, apply_turn no escribe si el report no paso validate_turn, Determinista]
test_plan: [Golden en repo-fixture git temporal verificando git log/status, Reusar validate_turn de M0]
closure_criteria: [vcs+apply+gate con golden verde/rojo/politica, revert atomico demostrado, write-allowlist probada, no reescribe validador/scan, handoff con evidencia, claim liberado]
---

# TASK-0030 — Runtime M1: apply_turn + gate + commit/revert

> `implementation` → SDD; implementar contra [SPEC-0029](../specs/SPEC-0029-turn-apply-gate.md) y
> [DISENO-runtime-m1.md](../artifacts/DISENO-runtime-m1.md) bajo DECISION-0009. Determinista, **sin
> invocar agentes**. Reclamar antes de tocar `runtime/` (DECISION-0007). `runtime/**` ya en scan_globs.

## Resumen
Primer **escritor seguro** del runtime: aplica un turn report ya validado (M0 `turn_validate`), corre el
gate (validador + scan) y hace **1 turno = 1 commit** o `git revert` + `blocked`. No invoca LLMs (eso es
M2). Golden deterministas sobre un repo-fixture git temporal.

## Secuenciacion
Tras TASK-0029 (diseño, done). Recomendado despues de TASK-0028 (claims por fila) y TASK-0025. Antes de
TASK-0031 (que añade el loop sobre este motor).

## archivos objetivo (previstos)
- `runtime/vcs.py`, `runtime/apply.py`, `runtime/gate.py`
- `examples/runtime_apply_cases/` (golden valido / gate-rojo / path-politica)

## Ejecucion Codex
- Implementado `runtime/vcs.py`:
  - `commit_turn(root, message, paths, allow_policy=False)`;
  - `revert_last(root)`;
  - `discard_worktree_changes(root)`;
  - write-allowlist dura para `.git/`, `Area_comun/decisions/`, `AGENTS.md`, `protocol.config*`.
- Implementado `runtime/gate.py`: `run_gate(root)` invoca `validate_collaboration_state.py` y
  `scan_domain_neutrality.py`.
- Implementado `runtime/apply.py`:
  - `apply_turn(report, root)` exige `validate_turn(report, root) == []`;
  - aplica `task_status`, `claims` y `mailbox`;
  - `apply_gate_and_commit(report, root)` aplica, corre gate y commitea o revierte cambios del turno y
    marca tarea `blocked`.
- Agregado `examples/runtime_apply_cases/run_runtime_apply_cases.py` con fixture git temporal.

## Validacion
- `python examples\runtime_apply_cases\run_runtime_apply_cases.py` -> OK, 4 casos:
  - report valido -> 1 commit + estado coherente;
  - gate rojo -> cambios del turno revertidos + tarea blocked;
  - path de politica -> rechazo sin `allow_policy`;
  - report invalido -> no escribe.
- `python -m py_compile runtime\vcs.py runtime\gate.py runtime\apply.py examples\runtime_apply_cases\run_runtime_apply_cases.py` -> OK.
- `python scripts\validate_collaboration_state.py --root .` -> OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .` -> OK.
- `python scripts\scan_domain_neutrality.py --root .` -> OK.
- Runtime M0 regressions (`schema`, `semantic`, `router`) -> OK.
- Regresion Python verde en `examples/minimal_instance`, `minimal_sdd_instance`,
  `dotnet_enterprise_instance`, `compact_communication_case`.
