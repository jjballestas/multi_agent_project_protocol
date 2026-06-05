---
id: TASK-0028
owner: Codex
status: done
type: implementation
priority: high
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0027]
relates_to: [TASK-0024]
phase: P2
spec_id: Area_comun/specs/SPEC-0028-claims-por-fila.md
linked_decisions: [DECISION-0011, DECISION-0007, DECISION-0009, DECISION-0001]
execution_pipeline: [Parser de scope ruta#fila (sin # = archivo completo), Solape por fila en validate_collaboration_state.py para TASK_INDEX/PROJECT_STATE, Paridad .ps1, Golden examples/row_scoped_claim_cases, Alinear write-allowlist runtime]
acceptance_criteria: [Filas distintas de distinto owner no se solapan, Misma fila se solapa, Ruta desnuda + selector falla, Claims historicos sin cambio, Paridad .py/.ps1, Selector mal formado da error claro]
test_plan: [Golden row_scoped_claim_cases en .py y .ps1, Regresion root + minimal_instance + minimal_sdd_instance]
closure_criteria: [Parser + solape por fila con paridad, golden verdes/rojos, sin regresion, write-allowlist runtime alineada, handoff con evidencia, claim liberado]
---

# TASK-0028 - Claims por fila para ledgers de estado

> `implementation` -> SDD; implementar contra [SPEC-0028](../specs/SPEC-0028-claims-por-fila.md) y
> [DECISION-0011](../decisions/DECISION-0011-claims-por-fila-estado.md). Aditivo y back-compat:
> el selector `ruta#fila` es opt-in; la ruta desnuda conserva su significado de archivo completo.

## Resumen
Resuelve el cuello de botella de coordinacion: el chequeo de solape trataba `TASK_INDEX.json` y
`PROJECT_STATE.json` como archivo completo. Se adopta scope por fila (`ruta#TASK-ID` o
`PROJECT_STATE.json#active_tasks/TASK-ID`) manteniendo `CLAIMS.json`/`mailbox/**` exentos.

## Ejecucion Codex
- Implementado parser `ruta#selector` en `validate_collaboration_state.py` y `.ps1`.
- `TASK_INDEX.json` y `PROJECT_STATE.json` soportan solape por fila:
  - filas distintas: OK;
  - misma fila: conflicto;
  - ruta desnuda + selector: conflicto conservador;
  - ruta desnuda + ruta desnuda: comportamiento legacy (conflicto).
- Selector invalido falla con error claro.
- `runtime/turn_validate.py` entiende scopes por fila y deriva writes de `transitions.task_status` a:
  - `Area_comun/state/TASK_INDEX.json#<TASK-ID>`;
  - `Area_comun/state/PROJECT_STATE.json#active_tasks/<TASK-ID>`.
- `runtime/context.py` ahora carga `TASK_INDEX_ARCHIVE.json`/`CLAIMS_ARCHIVE.json` si existen, para que
  el router vea dependencias archivadas. Esto corrige el plan post-poda: vuelve a seleccionar `TASK-0025`
  antes de `TASK-0030`.
- Agregado runner `examples/row_scoped_claim_cases/run_row_scoped_claim_cases.py`.

## Validacion
- `python examples\row_scoped_claim_cases\run_row_scoped_claim_cases.py` -> OK, 5 casos con paridad PowerShell.
- `python examples\runtime_turn_cases\run_runtime_turn_semantic_cases.py` -> OK.
- `python examples\runtime_router_cases\run_runtime_router_cases.py` -> OK.
- `python runtime\orchestrator.py --plan --root .` -> `TASK-0025`.
- `python scripts\validate_collaboration_state.py --root .` -> OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .` -> OK.
- `python scripts\scan_domain_neutrality.py --root .` -> OK.
- Regresion Python verde en `examples/minimal_instance`, `minimal_sdd_instance`,
  `dotnet_enterprise_instance`, `compact_communication_case`.

## Ratificacion Claude (arquitecto)
ACEPTADA contra SPEC-0028. Verificacion independiente:
- Validador (`validate_collaboration_state.py` 258-286): `split_scope` parte en `#`; `scopes_conflict`
  ⇒ mismo path con (algun selector None ⇒ archivo completo ⇒ conflicto) o (selectores iguales);
  selectores distintos ⇒ sin conflicto. `validate_claim_scope_selector` rechaza selector en ruta no
  soportada y selector mal formado. `CLAIMS.json`/`mailbox/**` siguen exentos. Exactamente DECISION-0011.
- `turn_validate` deriva las filas tocadas por `task_status` y valida la allowlist por fila (alinea M0).
- `context.py` lee hot+archive ⇒ el router resuelve dependencias archivadas tras la poda (corrige el
  plan post-TASK-0024). Bonus correcto.
- Golden **5/5 con paridad PowerShell**; runtime M0 verde; regresion verde en los 4 ejemplos.
**Aditivo/back-compat** (ruta desnuda intacta) ⇒ MINOR. Cierra el cuello de botella que colisiono 3
veces en la sesion. Flip a `done` aplicado por Claude (estado libre). Parte del checkpoint commiteado.
