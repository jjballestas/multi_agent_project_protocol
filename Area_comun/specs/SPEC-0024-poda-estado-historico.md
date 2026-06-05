---
spec_id: SPEC-0024-poda-estado-historico
task_id: TASK-0024
type: implementation
status: ready
linked_decisions: [DECISION-0008, DECISION-0001, DECISION-0007]
created_at: 2026-06-05
author: Claude
---

# SPEC-0024 — Poda de estado a histórico (sin pérdida)

## Contexto
DECISION-0008 §2: el 75% del cold-start es estado append-only (CLAIMS 100% `released`, TASK_INDEX 95%
`done`). Mover ese peso muerto a archivos históricos baja el cold-start ~74% sin perder trazabilidad.
Ver [DISENO-eficiencia-de-tokens.md](../artifacts/DISENO-eficiencia-de-tokens.md) §2. **Mayor impacto.**

## Alcance
- `Area_comun/state/CLAIMS_ARCHIVE.json` y `Area_comun/state/TASK_INDEX_ARCHIVE.json` (mismo schema).
- Lógica de poda/migración (script o paso) que mueve `released`/`done` a los archivos.
- `validate_collaboration_state.py`/`.ps1`: leer **caliente ∪ archivo** para chequeos.
- Docs: AGENTS §0 (cold-start lee lo caliente; histórico bajo demanda) + templates `*_ARCHIVE.template.json`.

## No-alcance
- **No borrar** historia. No cambiar el schema de claims/tareas. No tocar la lógica de validación
  más allá de unir las dos fuentes.

## execution_pipeline
1. Crear `CLAIMS_ARCHIVE.json` / `TASK_INDEX_ARCHIVE.json` (+ `.template.json`) con el mismo schema.
2. Migración inicial: mover claims `released` (conservando opcional ventana reciente) y tareas `done`
   a los archivos; dejar en caliente solo `active`/no-`done` (+ ventana).
3. Validador: cargar caliente ∪ archivo para consistencia índice↔task-file, `depends_on`/`relates_to`,
   duplicados, etc. (cobertura idéntica a hoy). Verde en root + ejemplos.
4. AGENTS §0 / TASK_PROTOCOL: cold-start lee los archivos calientes; histórico bajo demanda.
5. Medir before/after con `measure_context_cost` (SPEC-0023) y reportar el delta.

## acceptance_criteria
- Cold-start (medido) baja sustancialmente (objetivo ~−70%); reportado con before/after real.
- Trazabilidad intacta: toda entrada archivada es consultable; **nada se borra**.
- Validador verde en root + todos los ejemplos, con cobertura equivalente (lee caliente ∪ archivo).
- Caliente contiene solo `active`/no-`done` (+ ventana declarada); resto en archivo.
- Paridad `.py`↔`.ps1` del validador.

## linked_decisions
- `DECISION-0008` §2 (fuente); `DECISION-0007` (claim antes de mover estado compartido);
  `DECISION-0001` (aditivo ⇒ MINOR).

## test_plan
- `measure_context_cost` antes y después ⇒ delta documentado.
- Validador en root + minimal/sdd/dotnet/compact ⇒ verde; provocar una inconsistencia índice↔archivo
  ⇒ el validador la detecta (prueba de que lee ambos).

## closure_criteria
- Poda aplicada sin pérdida; validador verde con cobertura equivalente; delta medido en handoff;
  AGENTS §0 actualizado; revisión del arquitecto OK; claim liberado.

## Risks
- El validador podría dejar de ver entradas archivadas y romper referencias. Mitigación: union
  obligatoria caliente∪archivo, con test que lo demuestra (inconsistencia detectada).
- Ventana reciente mal definida ⇒ poda demasiado agresiva. Mitigación: empezar conservador
  (solo `released`/`done` con `expires_at` pasado o todos salvo ventana N).

## Traceability
| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| Cold-start baja ~70% medido | TASK-0024 | measure antes/después | delta en handoff |
| Sin pérdida de trazabilidad | TASK-0024 | archivo consultable; nada borrado | union verificada |
| Validador cobertura equivalente | TASK-0024 | inconsistencia detectada | verde + detecta cross-ref |
