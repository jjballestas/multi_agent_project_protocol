---
spec_id: SPEC-0029-turn-apply-gate
task_id: TASK-0030
type: implementation
status: ready
linked_decisions: [DECISION-0009, DECISION-0007, DECISION-0011, DECISION-0001]
created_at: 2026-06-05
author: Claude
---

# SPEC-0029 — Aplicación de turno + gate + commit/revert

## Contexto
Runtime M1 (DECISION-0009): primer **escritor seguro**. Aplica un *turn report* **ya validado**
(M0 `turn_validate`, SPEC-0026) a los ficheros, corre el **gate** y hace **1 turno = 1 commit** o
revierte. Ver [DISENO-runtime-m1.md](../artifacts/DISENO-runtime-m1.md) §1-§2, §4, §6.

## Alcance
- `runtime/vcs.py`: `commit_turn(root, message, paths)` y `revert_last(root)`; **write-allowlist** dura.
- `runtime/apply.py`: `apply_turn(report, root)` aplica `transitions` (task_status, claims, mailbox,
  handoff) de forma determinista; **rechaza** si el report no pasó `validate_turn` antes.
- `runtime/gate.py`: `run_gate(root)` corre `validate_collaboration_state` + `scan_domain_neutrality`
  (reusa los scripts) y devuelve `{green: bool, detail}`.

## No-alcance
- No invoca agentes (replay/real es SPEC-0030/M2). No define el loop `--run` (SPEC-0030). No reimplementa
  el validador ni el scan (los invoca).

## execution_pipeline
1. **write-allowlist (vcs):** `commit_turn` valida que cada path ∈ `changed_paths` NO caiga bajo
   `.git/`, `Area_comun/decisions/`, `AGENTS.md`, `protocol.config*` (salvo `allow_policy=True`). Si cae
   ⇒ aborta sin commitear.
2. **apply_turn:** precondición = `validate_turn(report, root) == []` (si no, lanza/rechaza). Aplica:
   `task_status` (set `to` en TASK_INDEX caliente + task file + PROJECT_STATE.active_tasks);
   `claims` (acquire ⇒ añade claim activo; release ⇒ status released); `mailbox` (send/answer/archive
   ⇒ crea/mueve mensaje); `handoff` (registra ruta). Determinista; sin tocar rutas fuera de `changed_paths`.
3. **gate:** `run_gate` ⇒ verde/rojo con detalle (qué check falló).
4. **commit/revert (orquestación mínima de M1, demostrable en golden):** aplicar ⇒ `run_gate` ⇒ verde:
   `commit_turn(report.commit_message, report.changed_paths)`; rojo: `revert_last` + marcar tarea
   `blocked` + (señal de) HUMAN_REPORT.

## acceptance_criteria
- Report válido `ready→in_review` aplicado ⇒ estado cambia coherente (índice+task file+PROJECT_STATE) y
  produce **exactamente 1 commit** con `commit_message`.
- Report cuyo resultado rompe el gate (p.ej. introduce término de dominio en ruta escaneada) ⇒
  `revert_last` deja el árbol **idéntico** al pre-turno y la tarea queda `blocked`.
- `commit_turn` **rechaza** paths de política (decisions/AGENTS/config) sin `allow_policy`.
- `apply_turn` no escribe nada si el report no pasó `validate_turn`.
- Determinismo: mismo report + mismo estado ⇒ mismo resultado.

## linked_decisions
- `DECISION-0009` (runtime, gate+commit/revert); `DECISION-0007` (claim/write-allowlist);
  `DECISION-0011` (escritor único = atomicidad de estado); `DECISION-0001` (aditivo ⇒ MINOR).

## test_plan
- Golden sobre **repo-fixture git temporal**: (a) válido ⇒ 1 commit + estado; (b) gate-rojo ⇒ revert +
  blocked + árbol restaurado; (c) path de política ⇒ commit rechazado. Verificar `git log`/`git status`.
- Reusar `validate_turn` de M0 (no duplicar lógica de validación).

## closure_criteria
- vcs+apply+gate con golden (verde/rojo/política) verdes; revert atómico demostrado; write-allowlist
  probada; sin tocar el validador/scan salvo invocarlos; revisión del arquitecto OK; claim liberado.

## Risks
- Apply parcial antes del gate. Mitigación: gate_post + revert atómico; el commit solo ocurre en verde.

## Traceability
| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| 1 turno = 1 commit en verde | TASK-0030 | golden válido | git log +1 |
| Rollback en rojo | TASK-0030 | golden gate-rojo | árbol restaurado + blocked |
| Write-allowlist de política | TASK-0030 | golden path-política | commit rechazado |
| Apply solo si validado | TASK-0030 | report inválido | no escribe |
