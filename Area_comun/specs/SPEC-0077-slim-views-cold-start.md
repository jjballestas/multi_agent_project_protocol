---
spec_id: SPEC-0077
title: "Slim-views del estado y politica de cold-start just-in-time (DECISION-0030)"
status: draft
date_created: 2026-06-13
date_updated: 2026-06-13
authored_by: Claude (architect)
task_id: TASK-0105
related_decisions: [DECISION-0030, DECISION-0008, DECISION-0014, DECISION-0017, DECISION-0022]
---

# SPEC-0077 - Slim-views del estado y politica de cold-start just-in-time

**Resumen ejecutivo:** Materializar vistas compactas derivadas del estado autoritativo
(`TASK_INDEX.slim.json`, `PROJECT_STATE.slim.json`, `CLAIMS.slim.json`) en el mismo ciclo atomico que
las vistas full, y apuntar el cold-start a ellas, dejando los archivos full y el event log fuera del
arranque. Las slim-views son derivadas, regenerables y sin perdida; un verificador de drift garantiza que
nunca diverjan del snapshot. Todo bajo flag `event_state.slim_views_enabled` (off-by-default). El cambio
de `coldstart_globs` se promueve solo si la medicion before/after confirma el delta (objetivo <10k).

---

## 1. Contexto y justificacion

Ver DECISION-0030. DECISION-0008 acoto el crecimiento archivando `done`/`released` y DECISION-0014 hizo la
poda sistematica por umbral; ambas reducen el **peso muerto**. Persiste que el cold-start carga los
archivos calientes **completos** (`PROTOCOL_STATE_PATHS` en `runtime/protocol_replay.py`) con todos los
campos por entrada; medicion de DECISION-0014: re-acumulacion a ~19.5k tokens tras poda. El costo dominante
es **cuanto del peso vivo se vuelca al contexto**, no el peso muerto.

Esta SPEC introduce proyecciones compactas para el arranque y deja el detalle para recuperacion
just-in-time (el agente lee el `TASK-XXXX.md` / `DECISION-XXXX.md` / handoff concreto cuando lo necesita).

---

## 2. Diseno tecnico

### 2.1 Estados "calientes" (incluidos en slim)

Un task entra en las slim-views si su `status` NO es terminal. Terminal = `{done, cancelled}`.
Calientes = `{proposed, ready, claimed, in_progress, in_review, changes_requested, qa_pending,
qa_failed, architect_review, blocked}` (subconjunto de `VALID_TASK_STATUSES` de `submit_intent.py`).

### 2.2 Esquema de cada slim-view

**`Area_comun/state/TASK_INDEX.slim.json`** (derivada de `task_index`):
```json
{
  "schema_version": "1.0",
  "view": "task_index.slim",
  "tasks": [
    {"id": "TASK-0102", "status": "ready", "owner": "Codex", "phase": "P2",
     "priority": "high", "title": "...", "blocked_by_questions": []}
  ]
}
```
Solo tareas en estados calientes. Campos por tarea: `{id, status, owner, phase, priority, title}` y
`blocked_by_questions` solo si no esta vacio. Se omiten `deliverables`, `relevant_files`, `relates_to`,
`linked_decisions`, `depends_on`, `created_at`, `updated_at`, `file` (todos recuperables del `TASK-XXXX.md`
o del full bajo demanda).

**`Area_comun/state/PROJECT_STATE.slim.json`** (derivada de `project_state`):
```json
{
  "view": "project_state.slim",
  "status": "active",
  "active_tasks": [{"id": "TASK-0102", "status": "ready", "owner": "Codex", "title": "..."}],
  "next_actions": ["...ultimas recent_next_actions..."],
  "risks": ["...recortado..."],
  "open_questions": ["...recortado..."]
}
```
`active_tasks` reducido a `{id, status, owner, title}` y filtrado a estados calientes. Narrativa
(`next_actions`, `risks`, `open_questions`) truncada a las ventanas `recent_*` ya definidas en
`maintenance` (p.ej. `recent_next_actions`). `decisions` NO se incluye en el cold-start (lista larga;
recuperable on-demand).

**`Area_comun/state/CLAIMS.slim.json`** (derivada de `claims`):
```json
{
  "schema_version": "1.0",
  "view": "claims.slim",
  "claims": [{"claim_id": "CLAIM-...", "task_id": "TASK-0102", "owner": "Codex", "scope": ["..."]}]
}
```
Solo claims con `status == "active"`. Campos: `{claim_id, task_id, owner, scope}`.

### 2.3 Reglas duras (innegociables)

1. **Derivadas, no fuente de verdad.** Las slim-views se generan desde el snapshot canonico
   (`canonicalize_protocol_state`). El full + archive + event log siguen siendo autoritativos.
2. **No editables / no reclamables.** No se editan a mano ni participan en scopes de claims ni en
   `required_scopes` (`submit_intent.py`). Materializar slim-views no exige claim del agente: las produce
   el escritor unico (runtime), no un intent de agente.
3. **Deterministas y canonicas.** Mismo orden y forma que las full (ordenadas por `id`/`claim_id`,
   `ensure_ascii=True`, `indent=4`, `sort_keys=True`, newline `\n`), via `write_text_ascii` /
   `canonical_json_text`.
4. **Atomicas con las full.** Se escriben en el MISMO lote stage/backup/replace de `materialize_to_disk`
   (mismo `temp_root`), de modo que full y slim se actualizan o se revierten juntas.

### 2.4 Cambios de codigo (runtime)

**`runtime/protocol_replay.py`:**
- `SLIM_VIEW_PATHS = {"task_index_slim": Path("Area_comun/state/TASK_INDEX.slim.json"), ...}`.
- `HOT_TASK_STATUSES: set[str]` y helper `is_hot_status(status) -> bool`.
- `build_slim_views(snapshot_or_state, config) -> dict[str, dict]`: deriva las 3 slim del estado canonico.
  Lee las ventanas `recent_*` desde `config["maintenance"]`.
- `slim_views_enabled(config) -> bool`: `event_state.slim_views_enabled is True`.
- `materialize_to_disk(...)`: si `slim_views_enabled(config)`, ampliar `materialized` con las
  `SLIM_VIEW_PATHS` (mismas etapas de staging/backup/replace; mismas garantias de rollback y
  `fail_after_writes`). Si el flag esta off, no se escribe ninguna slim (comportamiento legacy intacto).
- `slim_view_drift(root) -> dict`: lee las slim de disco y las compara (por `canonical_hash`) contra
  `build_slim_views(current_protocol_snapshot(root), config)`. `has_drift=True` si difieren o faltan
  estando el flag on.
- `protocol_state_drift(root)`: si `slim_views_enabled`, incorpora las entradas de `slim_view_drift` al
  reporte (mismas claves `path/hot_hash/replay_hash`), de modo que el gate de drift existente en
  `submit_intent`/`submit_intents` aborte y revierta si una slim quedo inconsistente.

**`protocol.config.json` y `protocol.config.template.json`:**
- Nuevo flag en `event_state`: `"slim_views_enabled": false` (default).

**`coldstart_globs` (token_cost) - cambio gated, paso 2:**
- Reemplazar los tres full por sus `*.slim.json` SOLO tras confirmar el delta con
  `measure_context_cost`. Se publica tambien en `protocol.config.template.json`.

**Templates de estado:**
- Anadir `Area_comun/state/TASK_INDEX.slim.template.json`, `PROJECT_STATE.slim.template.json`,
  `CLAIMS.slim.template.json` (masters, neutral de dominio).

**`scripts/measure_context_cost.py` (+ `.ps1`, paridad):**
- Reportar cold-start con full-views vs slim-views (before/after) y el delta; objetivo de referencia
  cold-start <10k (vs ~19.5k).

---

## 3. Out of scope

- Compaction / tool-result clearing y sub-agentes (DECISION-0030 secciones 4-5): se especifican en una
  onda aparte; esta SPEC cubre slim-views + politica de cold-start.
- Cambios al replay/materializacion de las vistas full (sin cambios de semantica).
- Rotacion/segmentado de `events.jsonl` (se trata como item separado; aqui solo se garantiza que el log
  NO entra a `coldstart_globs`).

---

## 4. execution_pipeline

1. Anadir `slim_views_enabled` (default false) a `protocol.config(.template).json > event_state`.
2. Implementar `build_slim_views`, `SLIM_VIEW_PATHS`, `HOT_TASK_STATUSES` en `protocol_replay.py`.
3. Ampliar `materialize_to_disk` para escribir slim en el mismo lote atomico bajo el flag.
4. Implementar `slim_view_drift` e integrarlo en `protocol_state_drift`.
5. Crear templates `*.slim.template.json`.
6. Extender `measure_context_cost` con reporte before/after.
7. Golden cases (seccion 6).
8. Medir; si delta confirmado, promover `coldstart_globs` a las `*.slim.json` (paso 2, gated).

---

## 5. acceptance_criteria

**AC1 - Flag off-by-default, legacy intacto:**
- [ ] `event_state.slim_views_enabled` existe, default false.
- [ ] Con flag off no se materializa ninguna slim; estado full y drift sin cambios.

**AC2 - Slim derivadas correctas:**
- [ ] `build_slim_views` produce las 3 vistas con los campos y filtros de la seccion 2.2.
- [ ] Solo estados calientes; `done`/`cancelled` excluidos; claims no-`active` excluidos.
- [ ] Narrativa truncada a ventanas `recent_*` de `maintenance`.

**AC3 - Atomicidad y rollback:**
- [ ] Slim y full se escriben/revierten juntas (mismo `materialize_to_disk`).
- [ ] `fail_after_writes` deja full+slim consistentes (todo revertido).

**AC4 - Anti-drift:**
- [ ] `slim_view_drift` detecta slim manipulada o faltante (flag on).
- [ ] El gate de drift de `submit_intent(s)` aborta y revierte ante slim inconsistente.

**AC5 - Cold-start y log fuera del arranque:**
- [ ] Con `coldstart_globs` promovido, el cold-start usa `*.slim.json`; NO incluye full ni
      `runtime/state/events.jsonl`.
- [ ] `measure_context_cost` reporta before/after; delta documentado en el handoff.

**AC6 - Validador, neutralidad, encoding:**
- [ ] Validador de protocolo verde; `domain_neutrality` limpio; ASCII en canal / UTF-8 en datos.
- [ ] Sin secretos. Templates `*.slim.template.json` neutrales.

---

## 6. test_plan y golden cases

Directorio: `examples/slim_view_cases/` (cada caso autocontenido, inputs deterministas).

- **GC-1 (derivacion happy path):** estado con tareas/claims mixtos -> las 3 slim coinciden con el
  expected. Sin falsos positivos en drift.
- **GC-2 (filtro de estados):** estado con `done`/`cancelled` y claims `released` -> excluidos de slim.
- **GC-3 (anti-drift):** manipular `TASK_INDEX.slim.json` en disco -> `slim_view_drift.has_drift=True` y
  el submit aborta con rollback.
- **GC-4 (atomicidad):** `fail_after_writes` a mitad del lote -> full y slim quedan en estado previo.
- **GC-5 (flag off):** `slim_views_enabled=false` -> no se escriben slim; drift y estado full intactos.
- **GC-6 (medicion):** `measure_context_cost` reporta cold-start full vs slim; el caso fija un estado de
  referencia y asevera delta > 0 (objetivo <10k con slim).
- **GC-7 (log fuera del arranque):** asercion de que `events.jsonl` no esta en `coldstart_globs` tras la
  promocion.

Ejecucion: `python examples/slim_view_cases/run_tests.py [--golden-case GC-1|...]`, exit 0/1, reporte JSON
reproducible (timestamps fijos).

---

## 7. closure_criteria

- Slim-views materializadas bajo flag off-by-default, derivadas y atomicas con las full.
- `slim_view_drift` integrado y los golden cases (GC-1..GC-7) verdes.
- Medicion before/after adjunta; `coldstart_globs` promovido solo si delta confirmado.
- Validador/neutralidad/encoding verdes; handoff autocontenido.
- TASK-0105 cierra en `done`.

## 8. Risks

- **Drift silencioso de slim:** mitigado por `slim_view_drift` en el mismo gate que el drift de las full
  (escritor unico, DECISION-0022).
- **Perdida de informacion necesaria en arranque:** mitigado por recuperacion just-in-time + medicion;
  si un agente requiere un campo omitido, lo lee del full/`TASK-XXXX.md`.
- **Desincronizacion master/instancia:** templates `*.slim.template.json` se publican junto al codigo
  (regla 5 de CLAUDE.md).

## 9. linked_decisions

- `DECISION-0030`: define slim-views + politica de cold-start y las garantias anti-drift.
- `DECISION-0008` / `DECISION-0014`: medicion before/after y poda; esta SPEC reduce el peso vivo cargado.
- `DECISION-0017` / `DECISION-0022`: event log y escritor unico; las slim las produce el runtime.

## 10. Traceability

| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| Slim-views derivadas correctas | TASK-0105 | GC-1, GC-2 | AC2 |
| Atomicidad y rollback | TASK-0105 | GC-4 | AC3 |
| Anti-drift | TASK-0105 | GC-3 | AC4 |
| Flag off-by-default | TASK-0105 | GC-5 | AC1 |
| Cold-start <10k + log fuera | TASK-0105 | GC-6, GC-7 | AC5 |
| Validador/neutralidad/encoding | TASK-0105 | run_tests + validador | AC6 |
