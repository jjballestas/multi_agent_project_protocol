---
spec_id: SPEC-0028-claims-por-fila
task_id: TASK-0028
type: implementation
status: ready
linked_decisions: [DECISION-0011, DECISION-0007, DECISION-0009, DECISION-0001]
created_at: 2026-06-05
author: Claude
---

# SPEC-0028 — Claims por fila para ledgers de estado

## Contexto
DECISION-0011: el chequeo de solape trata `TASK_INDEX.json`/`PROJECT_STATE.json` como archivo completo
y serializa el trabajo paralelo. Se adopta **scope por fila** (selector `ruta#fila`), aditivo y
back-compat. Ver [DECISION-0011](../decisions/DECISION-0011-claims-por-fila-estado.md).

## Alcance
- Gramática de `scope`: aceptar `Area_comun/state/TASK_INDEX.json#<TASK-ID>` y
  `Area_comun/state/PROJECT_STATE.json#active_tasks/<TASK-ID>` y `PROJECT_STATE.json#<campo>`.
- Chequeo de solape **por fila** en `validate_collaboration_state.py` y `.ps1` (paridad) para esos dos
  ledgers; `CLAIMS.json` y `mailbox/**` siguen exentos.
- Golden cases en `examples/row_scoped_claim_cases/` (verdes y rojos).
- (Alineación) extender la *write-allowlist* del runtime (`runtime/turn_validate.py`, SPEC-0026) para
  mapear `transitions` → selector de fila y validar contra el scope.

## No-alcance
- No cambia `CLAIMS.json`/mailbox (siguen exentos). No implementa atomicidad física (eso es el
  single-writer del orquestador, DECISION-0009). No migra claims históricos (ruta desnuda sigue válida).

## execution_pipeline
1. **Parser de scope:** dividir cada entrada en `(path, selector|None)` por el primer `#`. Sin `#` ⇒
   selector `None` (= archivo completo, comportamiento actual).
2. **Solape por fila:** en el doble bucle de claims activos de distinto owner, para `TASK_INDEX.json` y
   `PROJECT_STATE.json`:
   - mismo path **y** (alguno con selector `None`) ⇒ **conflicto** (ruta desnuda ⊇ cualquier fila).
   - mismo path **y** ambos con selector ⇒ conflicto **solo si** `selector_izq == selector_der`.
   - paths distintos ⇒ sin conflicto. Mantener exención de `CLAIMS.json` y `mailbox/**`.
3. **Paridad `.ps1`:** misma lógica, misma salida/exit. Harness tolerante a runtime (DECISION-0006).
4. **Golden:** ver test_plan. Incluir caso de regresión (ruta desnuda + ruta desnuda ⇒ sigue fallando).
5. **Runtime:** en `turn_validate`, derivar de `transitions.task_status`/`claims`/`mailbox` el conjunto de
   filas tocadas y verificar `⊆ scope` del claim (selectores incluidos).

## acceptance_criteria
- Dos claims activos de distinto owner sobre `TASK_INDEX.json#TASK-A` y `#TASK-B` ⇒ **válido** (sin solape).
- Los mismos sobre `#TASK-A` y `#TASK-A` ⇒ **falla** (overlapping row).
- Ruta desnuda + cualquier selector del otro owner sobre el mismo archivo ⇒ **falla** (conservador).
- Claims históricos (ruta desnuda) conservan su significado; ejemplos existentes siguen verdes.
- Paridad `.py`↔`.ps1`. Selector inválido/mal formado ⇒ error claro (no silencioso).

## linked_decisions
- `DECISION-0011` (modelo por fila); `DECISION-0007` (claim-as-lock que se afina);
  `DECISION-0009` (single-writer = atomicidad); `DECISION-0001` (aditivo ⇒ MINOR).

## test_plan
- Golden `examples/row_scoped_claim_cases/`: `distinct_rows_ok`, `same_row_conflict`,
  `bare_vs_row_conflict`, `legacy_bare_unchanged`; correr `.py` y `.ps1`.
- Regresión: validador verde en root + `examples/minimal_instance` + `minimal_sdd_instance`.

## closure_criteria
- Parser + solape por fila con paridad; golden verdes/rojos con exit esperado; sin regresión;
  write-allowlist del runtime alineada; revisión del arquitecto OK; claim liberado.

## Risks
- Selector ambiguo en `PROJECT_STATE` (escalares compartidos). Mitigación: selectores `#campo`
  explícitos + single-writer para escalares contendidos; documentar en la convención.

## Traceability
| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| Filas distintas no se solapan | TASK-0028 | distinct_rows_ok | válido |
| Misma fila se solapa | TASK-0028 | same_row_conflict | falla |
| Ruta desnuda conservadora | TASK-0028 | bare_vs_row_conflict + legacy_bare_unchanged | falla / sin cambio |
| Paridad .py/.ps1 | TASK-0028 | golden en ambos | misma salida |
