---
decision_id: DECISION-0032
title: El architect/orchestrator puede cerrar sus propias analysis-tasks sin implementer/qa
status: accepted
date: 2026-06-13
ratified_at: 2026-06-13
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0004, DECISION-0015, DECISION-0022]
phase: P2
---

# DECISION-0032 - El architect/orchestrator cierra sus propias analysis-tasks

> Estado: ACCEPTED (2026-06-13), ratificada por el operador. Cambio de autorizacion del estado
> (deliberado, no de pasajero). Va separada de DECISION-0005 (narracion minima).

## Contexto

`runtime/submit_intent.py::task_status_capability` exigia capability **implementer** para mover cualquier
tarea a `in_review`/`done`/`blocked`. Una tarea de tipo **analysis** es propiedad y obra del
architect/orchestrator (Claude = [architect, orchestrator, qa, reviewer], SIN implementer): el entregable
es el propio analisis, sin un split implementer-vs-reviewer. Resultado: el architect **no podia cerrar su
propia analysis-task** por la via lifecycle `in_progress -> in_review -> done` (el hop `in_progress ->
in_review` exigia implementer). El gap se observo en TASK-0109 (quedo `in_progress`) y TASK-0110 (cerrada
con un workaround `in_progress -> qa_pending -> done`).

## Decision

Para tareas de **`type == analysis` cuyo `owner` es el actor**, las transiciones a
`in_review`/`done`/`blocked` aceptan **`{orchestrator, architect}`** en vez de exigir `implementer`. El
resto del modelo de capacidades queda **intacto**:

- Tareas de otro tipo (`implementation`, etc.): siguen exigiendo `implementer` para esos hops.
- Analysis-tasks **NO** propiedad del actor: siguen exigiendo `implementer` (no se relaja para terceros).
- Las rutas existentes `in_review -> done` (`{reviewer}`) y `qa_pending -> done` (`{qa}`) no cambian.

Es **aditiva** (solo relaja para analysis+owner; no remueve ninguna autorizacion existente) y respeta el
escritor unico (DECISION-0022): el cierre sigue yendo por `submit_intent`.

## Implementacion

- `runtime/submit_intent.py::task_status_capability`: regla nueva para `analysis` + `actor_owns_task`
  antes de la regla generica de `implementer`.
- Golden: `examples/analysis_close_cases/run_tests.py` (GC-1..GC-4): el architect avanza/cierra su propia
  analysis-task; otro tipo y analysis-de-tercero siguen exigiendo implementer.

## Versionado y neutralidad (DECISION-0001)

Aditiva (relajacion de autorizacion para un caso). **MINOR** (publicado en v1.5.0). Neutral de dominio;
sin secretos. No afecta `enforce`/single-writer: la mutacion sigue por `submit_intent`.

## Consecuencias

- El architect cierra sus analysis-tasks (p.ej. TASK-0109, TASK-0110) por la via lifecycle estandar, sin
  el workaround `qa_pending`.
- Maker != checker sigue intacto para implementaciones (Codex implementa, Claude revisa): esto solo cubre
  analysis-tasks propias del architect, donde no hay separacion de roles.
