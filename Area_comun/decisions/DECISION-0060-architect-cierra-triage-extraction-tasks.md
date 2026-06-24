---
decision_id: DECISION-0060
title: El architect/orchestrator puede cerrar sus propias triage/extraction-tasks sin implementer
status: accepted
date: 2026-06-24
ratified_at: 2026-06-24
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0032, DECISION-0022, DECISION-0058]
phase: P2
---

# DECISION-0060 - El architect/orchestrator cierra sus propias triage/extraction-tasks

> Estado: ACCEPTED (2026-06-24), ratificada por el operador. Cambio de autorizacion del estado
> (deliberado). Extiende DECISION-0032 (que cubrio `type == analysis`) a `triage`/`extraction`.

## Contexto

`runtime/submit_intent.py::task_status_capability` exige capability **implementer** para mover cualquier
tarea a `in_review`/`done`/`blocked`, salvo el carve-out de DECISION-0032 para `type == analysis` +
owner. Las tareas de **`type == triage`** (p.ej. los handles de extraccion `TASK-EXTRACT-*` que produce el
file-intake, DECISION-0058) son propiedad y obra del **architect/orchestrator**: el entregable es la
disposicion de candidatos (que quedan como REQ seeds fuera del ledger / proposed), sin un split
implementer-vs-reviewer. Resultado: el architect **no puede cerrar su propia triage/extraction-task** por
ninguna via -- ni `in_review -> done` (no es obra de un implementer) ni `ready -> done` (exige implementer).
El gap se observo en `TASK-EXTRACT-1F5C13A7B5` (quedo `ready` pese a tener sus candidatos US-1..US-5 ya
dispuestos como REQ seeds): no habia actor que pudiera cerrarla sin invocar a Codex para una tarea que no es
de implementacion.

## Decision

Para tareas de **`type` en `{analysis, triage, extraction}` cuyo `owner` es el actor**, las transiciones a
`in_review`/`done`/`blocked` aceptan **`{orchestrator, architect}`** en vez de exigir `implementer`. El
resto del modelo de capacidades queda **intacto**:

- Tareas de otro tipo (`product`, `implementation`, etc.): siguen exigiendo `implementer` para esos hops.
- triage/extraction/analysis-tasks **NO** propiedad del actor: siguen exigiendo `implementer` (no se relaja
  para terceros).
- Las rutas existentes `in_review -> done` (`{reviewer}`) y `qa_pending -> done` (`{qa}`) no cambian.

Es **aditiva** (solo relaja para {analysis, triage, extraction} + owner; no remueve ninguna autorizacion
existente) y respeta el escritor unico (DECISION-0022): el cierre sigue yendo por `submit_intent`.

## Implementacion

- `runtime/submit_intent.py::task_status_capability`: la regla de DECISION-0032 cambia de
  `task_type == "analysis"` a `task_type in {"analysis", "triage", "extraction"}` (antes de la regla
  generica de `implementer`).
- Golden: extender `examples/analysis_close_cases/` (o nuevo caso) para cubrir: el architect cierra su
  propia triage/extraction-task; triage-de-tercero y `type == product` siguen exigiendo implementer.
- Entrega como TASK-0168 (maker=Codex / checker=Arquitecto).

## Versionado y neutralidad (DECISION-0001)

Aditiva (relajacion de autorizacion para dos tipos mas). **MINOR**. Neutral de dominio; sin secretos. No
afecta `enforce`/single-writer: la mutacion sigue por `submit_intent`. Bajo #4 chain ON el `protocol_version`
queda PINNED (DECISION-0047, versionado por epoca): el bump de version se reconcilia en CHANGELOG/manifest
fuera del config, sin re-genesis por esta decision.

## Consecuencias

- El architect cierra sus triage/extraction-tasks (p.ej. `TASK-EXTRACT-1F5C13A7B5`) por la via lifecycle
  estandar, sin invocar a Codex ni un workaround.
- Maker != checker sigue intacto para implementaciones (`type == product`/`implementation`: Codex implementa,
  Arquitecto revisa): esto solo cubre triage/extraction/analysis-tasks propias del architect, donde no hay
  separacion de roles.
