---
spec_id: SPEC-0027-router-determinista
task_id: TASK-0027
type: implementation
status: ready
linked_decisions: [DECISION-0009, DECISION-0007, DECISION-0001]
created_at: 2026-06-05
author: Claude
---

# SPEC-0027 — Router determinista

## Contexto
DECISION-0009: el runtime decide **qué unidad de trabajo toca y a qué agente** con un router
**determinista** (mismo estado ⇒ misma decisión). Ver
[DISENO-runtime-orquestacion-automatizada.md](../artifacts/DISENO-runtime-orquestacion-automatizada.md) §3.

## Alcance
- Función pura `select_next(state) -> {action, task_id, owner, reason} | none`, leyendo
  `PROJECT_STATE`, `TASK_INDEX`, `CLAIMS`, `mailbox/open`.
- Golden cases de selección.

## No-alcance
- No invoca agentes (eso es el orquestador/adapters). No muta estado (solo decide).

## execution_pipeline (orden de prioridad determinista)
1. **Gate humano:** si hay tarea `blocked` con `DECISION_REQUIRED`/`HUMAN_REQUIRED` o mensaje
   `human_required` en `open/` ⇒ `action=escalate`, parar.
2. **Desbloquear pares:** mensaje en `mailbox/open` con `requires_response:true` y `response_owner`
   = un agente disponible ⇒ `action=answer_mailbox` (ese owner).
3. **Ratificación:** tarea `in_review` cuyo revisor es el arquitecto ⇒ `action=review` (Claude).
4. **Trabajo nuevo:** la tarea `ready` con `depends_on` todas `done`, **no** cubierta por claim
   activo de otro owner, de mayor prioridad ⇒ `action=execute` (owner de la tarea). Desempate
   determinista: (`priority` desc, `id` asc).
5. Si nada aplica ⇒ `none` (el loop para por "sin trabajo").
- **Respeta claims:** nunca selecciona una ruta/tarea bajo claim activo de otro (DECISION-0007).
- **Determinismo:** sin azar; mismo estado ⇒ misma salida; desempates por id.

## acceptance_criteria
- Selección determinista y estable para un estado dado (mismo input ⇒ mismo output).
- Respeta el orden de prioridad (gate humano > mailbox > review > ready).
- No selecciona tareas con `depends_on` no satisfechas ni bajo claim de otro owner.
- Desempate por (priority, id) reproducible.

## linked_decisions
- `DECISION-0009` (router determinista); `DECISION-0007` (respeta claims); `DECISION-0001` (aditivo).

## test_plan
- Golden de estados → selección esperada: gate humano presente; mailbox pendiente; in_review;
  varias ready con dependencias/claims; estado sin trabajo (none).

## closure_criteria
- Router puro y determinista; golden de selección pasan; respeta claims/dependencias; revisión del
  arquitecto OK; claim liberado.

## Risks
- Prioridad mal ordenada ⇒ inanición de tareas. Mitigación: orden explícito + golden que cubre cada
  rama; desempate por id evita ciclos.

## Traceability
| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| Selección determinista | TASK-0027 | golden mismo estado | salida estable |
| Orden de prioridad | TASK-0027 | golden por rama | rama correcta elegida |
| Respeta claims/deps | TASK-0027 | golden claim/dep | no selecciona bloqueadas |
