---
spec_id: SPEC-0033-poda-sistematica
task_id: TASK-0034
type: implementation
status: ready
linked_decisions: [DECISION-0014, DECISION-0008, DECISION-0006, DECISION-0001]
created_at: 2026-06-06
author: Claude
---

# SPEC-0033 - Poda sistematica por umbral medido (prune_state + gate + hook + CI)

## Contexto
DECISION-0014: el mantenimiento de estado (archivar done/released + barrer mailbox viejo) debe ser
sistematico, disparado por umbral medido y no por peticion del humano. Medicion 2026-06-06: cold-start
~19.5k (suelo ~9.2k), 88.9% tareas done, 95.5% claims released. Reusa el medidor de DECISION-0008/TASK-0023.

## Alcance
- `scripts/prune_state.py` (+ `.ps1` con paridad):
  - `--check`: read-only, determinista; exit 1 + reporte corto cuando hay poda due (segun umbral de
    config), con que comando aplicar y cuanto se recupera (estimado).
  - `--apply`: idempotente; archiva tareas `done` y claims `released` fuera de la **ventana reciente** a
    `*_ARCHIVE.json`, y barre mailbox `answered`/`archived` mas viejo que la ventana. Archive != delete;
    el validador sigue leyendo hot+archive.
- **Config** (`protocol.config(.template).json`, bloque `maintenance` o extension de `token_cost`):
  `context_budget`, `done_ratio`, `released_ratio`, `recent_window` (dias/items). Off-by-default seguro.
- **Pre-commit hook** (`.githooks/` o doc de instalacion): corre `prune_state --check`; si poda due,
  **BLOQUEA** con el mensaje (no poda+re-stagea). Salteable con --no-verify (por eso el backstop CI).
- **CI:** paso que corre `prune_state --check` y **falla sobre umbral duro**.
- Golden `examples/prune_state_cases/`.

## No-alcance
- No auto-poda+re-stagea en el hook (descartado en DECISION-0014). No implementa el turno de
  mantenimiento del runtime (M2). No borra nada (archive != delete). No toca el runtime.

## execution_pipeline
1. `prune_state.py` con `--check`/`--apply`, reusando `measure_context_cost` para medir y el formato de
   `*_ARCHIVE` de TASK-0024 para archivar.
2. Bloque de config con umbrales + ventana reciente.
3. Hook pre-commit bloqueante + doc de instalacion.
4. Paso CI `--check` con hard-fail.
5. Golden: estado con peso muerto > umbral => `--check` exit 1; `--apply` archiva y baja el cold-start;
   idempotencia (segundo `--apply` no cambia nada); ventana reciente preservada; validador verde hot+archive.

## acceptance_criteria
- `--check` read-only, exit 1 con reporte cuando done/released/cold_start cruzan umbral; exit 0 si no.
- `--apply` idempotente, archive != delete, respeta ventana reciente; cold-start baja medido por el medidor.
- Umbrales en config (warning vs hard-fail); CI falla sobre hard-fail; hook bloquea (no muta).
- Paridad `.py`/`.ps1`; validador + scan verdes hot+archive; golden verdes.

## linked_decisions
- `DECISION-0014` (poda sistematica), `DECISION-0008` (eficiencia/medidor), `DECISION-0006` (robustez),
  `DECISION-0001` (aditivo => MINOR).

## test_plan
- Golden `examples/prune_state_cases/` (poda due / no due / idempotencia / ventana reciente) + paridad
  `.ps1` atestiguada; medicion antes/despues con `measure_context_cost --json`.

## closure_criteria
- `prune_state --check/--apply` .py/.ps1 + config de umbrales + hook bloqueante + CI hard-fail + golden +
  medicion que demuestra el descenso del cold-start; revision del arquitecto OK; claim liberado al
  pasar a in_review (dogfood DECISION-0013).

## Risks
- **Churn de archives.** Mitigacion: ventana reciente + histeresis (warning < hard-fail); `--apply` solo
  cuando hay poda due.
- **Borrado accidental.** Mitigacion: archive != delete; el validador cruza hot+archive (test de
  inconsistencia provocada, como TASK-0024).

## Traceability
| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| Disparo por umbral medido | TASK-0034 | golden check | exit 1 sobre umbral |
| Poda idempotente archive!=delete | TASK-0034 | golden apply/idempotencia | cold-start baja, nada borrado |
| Hook bloquea + CI hard-fail | TASK-0034 | golden + CI | no muta en hook; CI falla sobre techo |
