---
id: TASK-0024
owner: Codex
status: done
type: implementation
priority: high
created_at: 2026-06-05
updated_at: 2026-06-05
depends_on: [TASK-0023]
relates_to: [TASK-0025]
phase: P2
spec_id: Area_comun/specs/SPEC-0024-poda-estado-historico.md
linked_decisions: [DECISION-0008, DECISION-0001, DECISION-0007]
execution_pipeline: [Crear CLAIMS_ARCHIVE/TASK_INDEX_ARCHIVE (+template), Migrar released/done a archivo (ventana conservadora), Validador lee caliente union archivo, AGENTS seccion 0 cold-start a calientes + historico bajo demanda, Medir before/after con measure_context_cost]
acceptance_criteria: [Cold-start medido baja ~70% con before/after real, Trazabilidad intacta (nada borrado y consultable), Validador verde con cobertura equivalente (lee caliente union archivo), Caliente solo active/no-done + ventana, paridad .py/.ps1]
test_plan: [measure_context_cost antes/despues, validador en root + ejemplos, inconsistencia indice-archivo detectada]
closure_criteria: [Poda sin perdida, validador verde con cobertura equivalente, delta medido en handoff, AGENTS seccion 0 actualizado, claim liberado]
---

# TASK-0024 - Poda de estado a historico (mayor impacto)

> `implementation` -> SDD; implementar contra [SPEC-0024](../specs/SPEC-0024-poda-estado-historico.md)
> y DECISION-0008. Mayor ahorro del lote. Sin perdida: archivar no es borrar.
> Depende de TASK-0023 (medir el delta). Reclamar antes de mover estado (DECISION-0007).

## Ejecucion Codex
- Creado `Area_comun/state/CLAIMS_ARCHIVE.json` y `TASK_INDEX_ARCHIVE.json`.
- Creadas plantillas `CLAIMS_ARCHIVE.template.json` y `TASK_INDEX_ARCHIVE.template.json`.
- Migrados a historico:
  - `47` claims `released`.
  - `24` tareas `done`.
- Estado caliente tras poda:
  - `CLAIMS.json`: solo claims activos.
  - `TASK_INDEX.json`: `TASK-0024`, `TASK-0025`, `TASK-0027`, `TASK-0028`.
  - `PROJECT_STATE.active_tasks`: solo tareas no cerradas.
- `validate_collaboration_state.py` y `.ps1` leen caliente + archivo y detectan duplicados entre ambos.
- Documentado cold-start caliente + historico bajo demanda en `AGENTS.md` y `TASK_PROTOCOL.md`.

## Medicion
- Before: `37391` tokens cold-start.
- After: `9167` tokens cold-start.
- Delta: `-28224` tokens (`-75.48%`).

## Validacion
- `python scripts\validate_collaboration_state.py --root .` -> OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .` -> OK.
- `python scripts\scan_domain_neutrality.py --root .` -> OK.
- Regresion Python verde en `examples/minimal_instance`, `minimal_sdd_instance`,
  `dotnet_enterprise_instance`, `compact_communication_case`.
- Prueba de inconsistencia: duplicar temporalmente `TASK-0024` en `TASK_INDEX_ARCHIVE.json` produjo
  `Duplicate task across hot/archive: TASK-0024`; archivo restaurado.

## Nota de coordinacion
`TASK-0027` esta ratificada por Claude, pero su task file sigue `in_review` bajo claim activo de Claude.
No se cambio su fila a `done` para no romper la regla de estado task-file/indice.

## Ratificacion Claude (arquitecto)
ACEPTADA contra SPEC-0024. Verificacion independiente (`.py`) por Claude sobre root:
- Poda **sin perdida**: 24 tareas done + 47 claims released en `*_ARCHIVE.json`; union `caliente∪archivo`
  en el validador (`merge_by_array_field`) con deteccion de duplicados (test de inconsistencia provocada
  reproducido: `Duplicate task across hot/archive`).
- Caliente solo no-`done` + ventana reciente (permitida por la spec: `active/no-done + ventana`).
- Cold-start medido `37391 -> ~9.2k` tok (~`-75%`), dentro de budget 30000.
- Integridad: hot∪archivo = 28 tareas unicas (TASK-0001..0028), nada borrado.
- Paridad `.ps1` atestiguada por Codex/CI (deny-rule PowerShell en sesion arquitecto).
Cierra el mayor ahorro del track de eficiencia de tokens (DECISION-0008). Flips a `done` de 0024 y 0027
aplicados por Claude tras liberarse el estado.
