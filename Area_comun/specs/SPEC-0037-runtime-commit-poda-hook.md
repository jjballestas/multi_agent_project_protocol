---
spec_id: SPEC-0037-runtime-commit-poda-hook
task_id: TASK-0041
type: implementation
status: ready
linked_decisions: [DECISION-0009, DECISION-0014, DECISION-0001]
created_at: 2026-06-06
author: Claude
---

# SPEC-0037 - Runtime commit robusto frente al pre-commit hook de poda

> Estado: READY. Follow-up priorizado por el operador. Defecto real detectado durante la PRIMERA CORRIDA
> REAL sobre el repo vivo (TASK-0040, 2026-06-06). Aditivo; no cambia el contrato de turno.

## Contexto
`runtime/vcs.py` `commit_turn` hace `git add` + `git commit` **sin `--no-verify`**, asi que el commit del
PROPIO runtime dispara el pre-commit hook (`scripts/prune_state.py --check`). Cerrar una tarea en un turno
**libera un claim** (y suma un done), lo que puede cruzar el umbral `released_count > 4` (o `done_ratio`,
`cold_start`) **en el momento del commit del runtime y bloquearlo**. Como `apply_turn` ya muto el estado
ANTES de `commit_turn`, un commit bloqueado deja el worktree **a medio aplicar** (no commiteado, sin
revert). En la corrida real de TASK-0040 se evito archivando 1 released a mano (post-turno = 4); hay que
arreglarlo de raiz.

El hook de poda es el guardian del camino MANUAL/humano (DECISION-0014). El runtime es el **escritor unico
automatizado** con su **propio gate** (`run_gate`: validador + scan de neutralidad, ya por turno,
DECISION-0009). Por tanto el runtime no debe quedar bloqueado por el hook humano; debe gestionar la
higiene de poda por si mismo.

## Alcance
1. **Runtime commit no bloqueado por el hook humano:** `commit_turn` commitea con `--no-verify` (param
   explicito, p.ej. `verify=False` por defecto en la ruta del runtime). Justificacion: `run_gate` ya
   ejecuta los MISMOS chequeos que protege el hook manual (validador + neutralidad) por turno; lo unico que
   el hook anade es la poda, que pasa a gestionarse en (2). No se pierde seguridad.
2. **Auto-mantenimiento de poda (DECISION-0014 "maintenance turn"):** como el runtime ya no pasa por el
   hook, debe mantener el cold-start el mismo: al terminar el run (o cuando `prune_state` este due), el
   orquestador ejecuta `prune_state --apply` y lo commitea como un **commit de mantenimiento dedicado**
   (separado del turno; tambien `--no-verify`, pero ya queda not-due). Solo actua cuando esta due.
3. **Atomicidad ante fallo de commit:** si `commit_turn` falla por cualquier motivo, el orquestador
   **descarta el worktree** (`discard_worktree_changes`) y marca la tarea `blocked` (igual que el camino de
   gate rojo) -> nunca deja estado a medio aplicar.

## No-alcance
- NO cambia el contrato de turno, el router, el motor apply/gate ni los umbrales de poda.
- NO toca el hook manual: los commits humanos siguen gateados por `prune --check`.
- NO automatiza autonomia adicional; sigue todo off-by-default y gateado.

## execution_pipeline
1. `commit_turn(..., verify: bool = False)` -> `git commit --no-verify` cuando lo invoca el runtime;
   conservar la validacion de policy-paths existente.
2. Orquestador: tras el loop (o por turno si due), correr `prune_state --check`; si due, `prune --apply`
   + commit de mantenimiento (`--no-verify`) con mensaje claro (p.ej. `chore(runtime): prune state`).
3. `run_loop`: envolver `apply_gate_and_commit`; si el commit lanza `VcsError`, `discard_worktree_changes`
   + `block_task` + outcome `blocked`/`stopped` en el run-log (sin propagar excepcion cruda).

## acceptance_criteria
- Un turno del runtime que cierra una tarea **con la poda en estado due** COMMITEA igualmente (el hook no
  bloquea al runtime); 1 commit del turno.
- Tras un run que cruza el umbral de poda, el runtime **se auto-poda** (commit de mantenimiento) y el repo
  queda `prune --check` not-due.
- Fallo simulado de `commit_turn` => worktree restaurado (sin cambios colgando) + tarea `blocked`; sin
  estado a medio aplicar.
- Commits MANUALES siguen gateados por el hook (sin cambios). Default replay + golden existentes intactos.

## linked_decisions
- `DECISION-0009` (runtime = escritor unico con su propio gate), `DECISION-0014` (poda; "maintenance
  turn"), `DECISION-0001` (aditivo => MINOR/PATCH). Nota: si la revision considera `--no-verify` un cambio
  de politica de gating, elevar a decision; el arquitecto lo trata como extension de 0009/0014.

## test_plan
- Golden en `examples/` (o extender runtime_loop_cases) que en un fixture temporal: instala el pre-commit
  hook de poda + scripts; arma estado que al cerrar la tarea cruza `released_count>4`; corre el
  orquestador; verifica (a) el commit del turno ocurre, (b) el repo queda not-due (auto-poda), (c) un caso
  de fallo de commit deja worktree limpio + tarea blocked. Sin red. `.ps1` n/a (vcs.py python; hook sh).

## closure_criteria
- `commit_turn` con `--no-verify` (runtime) + auto-mantenimiento de poda + atomicidad ante fallo de commit;
  golden verdes; camino manual + default replay sin regresion; revision del arquitecto OK; claim liberado
  al pasar a in_review (handoff-release).

## Risks
- **`--no-verify` salta TODOS los hooks**, no solo poda. Mitigacion: el runtime ya corre `run_gate`
  (validador + neutralidad) por turno; documentar que solo el runtime (escritor automatizado de confianza)
  bypassa, y SOLO el; el camino humano sigue gateado.
- **Auto-poda mezclada con el turno.** Mitigacion: commit de mantenimiento SEPARADO del commit del turno
  (no re-stagear dentro del turno; DECISION-0014).
- **Crecimiento de cold-start si la auto-poda no corre.** Mitigacion: correr `prune --check` al cierre del
  run y podar si due; CI sigue con su hard-fail como backstop.

## Traceability
| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| Runtime commit no bloqueado por hook | TASK-0041 | golden hook+due | turno commitea con poda due |
| Auto-mantenimiento de poda | TASK-0041 | golden post-run not-due | repo queda not-due |
| Atomicidad ante fallo de commit | TASK-0041 | golden commit-fail | worktree limpio + blocked |
| Camino manual/default sin regresion | TASK-0041 | golden existentes | hook manual gatea; replay intacto |
