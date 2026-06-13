---
id: TASK-0105
owner: Codex
status: done
type: implementation
priority: high
created_at: 2026-06-13
updated_at: 2026-06-13
depends_on: []
relates_to: [DECISION-0030, DECISION-0008, DECISION-0014, DECISION-0022]
phase: P2
spec_id: SPEC-0077
linked_decisions: [DECISION-0030, DECISION-0008, DECISION-0014, DECISION-0017, DECISION-0022]
deliverables:
  - runtime/protocol_replay.py (build_slim_views, SLIM_VIEW_PATHS, slim_view_drift, materialize_to_disk ampliado, off-by-default)
  - protocol.config.json + protocol.config.template.json (flag event_state.slim_views_enabled, default false)
  - Area_comun/state/*.slim.template.json (masters neutrales)
  - scripts/measure_context_cost.py (+ .ps1) reporte cold-start full vs slim (before/after)
  - examples/slim_view_cases (GC-1..GC-7 deterministas)
relevant_files:
  - runtime/protocol_replay.py
  - protocol.config.json
  - protocol.config.template.json
  - Area_comun/state/TASK_INDEX.template.json
  - Area_comun/state/PROJECT_STATE.template.json
  - Area_comun/state/CLAIMS.template.json
  - scripts/measure_context_cost.py
blocked_by_questions: []
objective: (DECISION-0030) Materializar slim-views derivadas (TASK_INDEX/PROJECT_STATE/CLAIMS .slim.json) en el mismo ciclo atomico que las vistas full y dejar el cold-start apuntando a ellas, con el event log y los full fuera del arranque. Reducir el peso vivo cargado (objetivo cold-start <10k vs ~19.5k) sin perder trazabilidad.
expected_output: (1) Flag event_state.slim_views_enabled off-by-default. (2) build_slim_views + SLIM_VIEW_PATHS + filtro de estados calientes; las 3 slim con los campos de SPEC-0077 s.2.2. (3) materialize_to_disk escribe slim en el mismo lote stage/backup/replace (rollback y fail_after_writes cubren slim). (4) slim_view_drift integrado en protocol_state_drift; el gate de submit aborta y revierte ante slim inconsistente. (5) Templates *.slim.template.json. (6) measure_context_cost before/after. (7) coldstart_globs promovido a *.slim.json SOLO tras confirmar delta. (8) Golden cases GC-1..GC-7 verdes; validador/neutralidad/encoding verdes; sin secretos.
question_to_resolve: Ninguna abierta; SPEC-0077 fija contrato, estados calientes, esquema y garantias anti-drift. Si surge ambiguedad en la implementacion, handoff blocked + pregunta concreta.
closure_criterion: slim-views derivadas y atomicas con las full bajo flag off-by-default; slim_view_drift y GC-1..GC-7 verdes; medicion before/after adjunta; coldstart_globs promovido solo con delta confirmado; handoff autocontenido con evidencia.
sdd_required: true
---

# TASK-0105 - Slim-views del estado y politica de cold-start (DECISION-0030)

> PROPOSED (Claude 2026-06-13, habilitada por DECISION-0030 aprobada por el operador). Implementa
> SPEC-0077. Promover a ready+GO cuando el operador lo indique. Implementacion y registro de estado se
> ejecutan desde VS Code (el escritor unico/runtime), no desde la sesion Cowork.

## Contexto

Ver DECISION-0030 y SPEC-0077. DECISION-0008/0014 acotaron el peso muerto; persiste que el cold-start
carga los archivos calientes completos (`PROTOCOL_STATE_PATHS`). Esta tarea materializa proyecciones
compactas derivadas (slim-views) y mueve el arranque hacia ellas, dejando el detalle para recuperacion
just-in-time. Las slim son derivadas/regenerables; el full + archive + event log siguen autoritativos.

## Entrada

SPEC-0077 cerrada (acceptance_criteria + test_plan + golden cases). Codex implementa contra la SPEC y
entrega handoff autocontenido con evidencia (medicion before/after, golden cases reproducibles).
