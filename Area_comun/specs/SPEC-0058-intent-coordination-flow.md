---
spec_id: SPEC-0058-intent-coordination-flow
task_id: TASK-0072
type: implementation
status: accepted
created_at: 2026-06-07
author: Claude (arquitecto)
linked_decisions: [DECISION-0022, DECISION-0017, DECISION-0015, DECISION-0011]
relates_to: [SPEC-0052, SPEC-0053, SPEC-0054, SPEC-0055, SPEC-0026, SPEC-0029]
---

> Fase 3.b.2 (escritor unico): el operador eligio cablear intents antes de encender enforce. KEYSTONE del
> escritor-unico. Aditivo, off-compatible, determinista, neutral. Promover de a una (DECISION-0020).

# SPEC-0058 - Flujo de coordinacion por intents (write-path del estado de protocolo)

## 1. Problema

Hoy Claude y Codex mutan el estado de protocolo (status de tareas, claims, decisiones, active_tasks)
EDITANDO los `*.json` a mano. El writer-vivo (Fase B) ya sabe replayar/materializar/enforzar desde el event
log, pero NO existe un camino ergonomico para que un agente SOMETA una transicion al runtime. Sin ese
write-path, encender `event_state.enforce+authoritative` (3.b.2) rechazaria toda edicion manual como drift y
bloquearia el lazo. Esta spec construye el write-path.

## 2. Objetivo

Un entrypoint determinista `submit_intent` que, dada una transicion estructurada de un actor, la VALIDA por la
capa de seguridad existente, la APENDA al event log como `intent.applied` (payload con `transitions`,
compatible con `replay_protocol_state`), y MATERIALIZA los `*.json` desde `replay(log)` (B.2). Resultado:
`hot *.json == materializa(replay(log))` (drift 0) tras cada intent => enforce (B.3) pasa. Los agentes dejan
de editar JSON a mano y pasan a `submit_intent`.

## 3. Alcance

1. **`runtime/submit_intent.py`** (+ paridad o delegacion `.ps1`): API/CLI `submit_intent(root, actor_id,
   intent, *, timestamp, commit=None)` donde `intent` describe UNA transicion atomica de uno de estos tipos
   (los que `replay_protocol_state` ya entiende):
   - `task_status`: cambiar el status de una tarea (`task_id`, `to`), reflejado en TASK_INDEX + active_tasks.
   - `task_upsert`: alta/actualizacion de una tarea (objeto task).
   - `claim`: acquire / release / block de un claim (`claim_id`, `op`, scope/owner/task).
   - `decision`: registrar un decision_id en PROJECT_STATE#decisions.
   - (extensible; lo no soportado => error claro, no silencioso.)
2. **Validacion antes de aplicar**: reusa la capa existente segun corresponda (turn_validate / guardrails
   G1 / tool-policy / autor-de-record): un intent cuya autoridad/scope no corresponda al actor se RECHAZA
   (no se aplica). Sin derivar permisos de contenido controlado por el actor (invariante G1).
3. **Aplicar + materializar atomicamente**: append del evento `intent.applied` (con `transitions`) al event
   log (idempotency_key por actor/intent) y materializacion a disco (reusa `materialize_to_disk` de B.2),
   todo-o-nada. Tras el intent, `protocol_state_drift().has_drift == False`.
4. **Determinista**: `timestamp` (y `commit` si aplica) PROVISTOS; sin reloj/red; negative-replay intacto.
5. **Off-compatible**: funciona con `event_state.enforce` on u off. Con la feature `event_state` off por
   completo, `submit_intent` puede operar en modo "tambien escribe el *.json" para no exigir el motor (o
   quedar gated a runtime-tier); el objetivo es que con enforce ON sea el UNICO camino valido.
6. **Golden** `examples/intent_flow_cases` + CI. **Docs** (AGENTS.md/TASK_PROTOCOL/N_AGENT_RUNTIME):
   en modo autoritativo, las transiciones se hacen con `submit_intent`, no editando JSON; ejemplos para
   cerrar tarea / reclamar / liberar / registrar decision.

## 4. Tests (golden determinista, sin red)

1. `submit_intent` task_status (p.ej. in_review->done) => evento `intent.applied` en el log + TASK_INDEX/
   PROJECT_STATE materializados al nuevo status; `has_drift == False`.
2. `submit_intent` claim acquire/release => CLAIMS materializado coherente; drift 0.
3. `submit_intent` decision => PROJECT_STATE#decisions actualizado; drift 0.
4. Intent invalido (autoridad/scope/transicion no permitida) => RECHAZADO, estado sin cambios, error legible.
5. Atomicidad: fallo simulado a mitad => no deja estado parcial.
6. Idempotencia: reenviar el mismo intent (misma idempotency_key) no duplica.
7. Determinismo: dos corridas identicas (mismo timestamp/commit) => byte-identico.
8. Con enforce ON: tras una secuencia de intents, el validador global pasa (drift 0); una edicion manual
   intercalada produce drift (hard-fail) => demuestra que submit_intent es el camino correcto.
9. Regresion: suite runtime + B.1/B.2/B.3 + fallback N=2 intactos.

## 5. Fuera de alcance

- Encender `enforce+authoritative` en el repo vivo (eso es el paso final de 3.b.2, tras esta tarea +
  re-genesis + GO).
- Autonomia / lazo encadenado (esa es la fase de autonomia supervisada).
- Cambiar el contrato del turn schema mas alla de lo necesario para representar un intent.

## 6. SemVer

- MINOR (write-path aditivo; off-compatible; no cambia el contrato existente). Habilita 3.b.2.

## 7. Secuencia

Promover TASK-0072 cuando TASK-0071 (F7.1) cierre (promover de a una, DECISION-0020). Tras TASK-0072 verde:
re-emitir genesis sincronizado (drift 0) + encender enforce+authoritative con GO del operador = 3.b.2 final.
