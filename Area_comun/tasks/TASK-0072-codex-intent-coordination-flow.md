---
id: TASK-0072
owner: Codex
status: done
type: implementation
priority: high
created_at: 2026-06-07
updated_at: 2026-06-07
depends_on: [TASK-0066, TASK-0067, TASK-0068, TASK-0069]
relates_to: [TASK-0038]
phase: P2
spec_id: Area_comun/specs/SPEC-0058-intent-coordination-flow.md
linked_decisions: [DECISION-0022, DECISION-0017, DECISION-0015]
execution_pipeline: [runtime/submit_intent.py (+ paridad/delegacion .ps1): API/CLI submit_intent(root, actor_id, intent, *, timestamp, commit) para UNA transicion atomica (task_status, task_upsert, claim acquire/release/block, decision) de las que replay_protocol_state ya entiende; validar autoridad/scope por la capa existente (turn_validate/guardrails G1/tool-policy/autor-de-record) sin derivar permisos de contenido del actor; apendar evento intent.applied (payload transitions, idempotency_key) + materializar a disco (materialize_to_disk de B.2) atomicamente => has_drift==False tras el intent; determinista (timestamp/commit provistos); off-compatible (enforce on u off); golden examples/intent_flow_cases + CI; docs AGENTS.md/TASK_PROTOCOL/N_AGENT_RUNTIME (en modo autoritativo se usa submit_intent, no se edita JSON)]
acceptance_criteria: [submit_intent aplica task_status/claim/decision => evento intent.applied + *.json materializados coherentes + has_drift==False; intent invalido (autoridad/scope/transicion) RECHAZADO sin cambiar estado; atomico (sin estado parcial ante fallo); idempotente (misma key no duplica); determinista (timestamp/commit provistos => byte-identico); con enforce ON una secuencia de intents pasa el validador (drift 0) y una edicion manual intercalada produce drift/hard-fail; suite runtime + B.1/B.2/B.3 + fallback N=2 sin regresion; paridad/delegacion .ps1; gates py/ps verdes; neutral, sin secretos]
expected_output: write-path por intents (runtime/submit_intent.py + .ps1) que muta el estado de protocolo via event log + materializacion dejando drift 0, validado por la capa de seguridad + golden examples/intent_flow_cases + docs; gates verdes. Habilita 3.b.2 (escritor unico).
test_plan: [golden intent_flow: task_status, claim acquire/release, decision => log+materializado+drift0; intent invalido rechazado; atomicidad; idempotencia; determinismo; enforce-ON secuencia pasa / edicion manual intercalada hard-failea; regresion B.1/B.2/B.3 + N=2; paridad py/ps]
question_to_resolve: ninguna (alcance acotado en SPEC-0058). Encender enforce+authoritative en el repo vivo NO entra (paso final de 3.b.2 tras esta tarea + re-genesis + GO). Si exige cambiar el contrato del turn schema mas alla de representar un intent => blocked + pregunta.
closure_criterion: submit_intent (task_status/claim/decision) valida+apende+materializa atomico dejando drift 0, off-compatible, determinista + golden + docs + paridad .ps1; gates verdes; handoff autocontenido; release atomico (DECISION-0018).
closure_criteria: [runtime/submit_intent.py (+ .ps1) para task_status/task_upsert/claim/decision; validacion de autoridad/scope (G1) que rechaza intents invalidos; append intent.applied + materialize atomico => has_drift False; idempotente; determinista (timestamp/commit provistos); off-compatible; golden examples/intent_flow_cases + CI; docs AGENTS.md/TASK_PROTOCOL/N_AGENT_RUNTIME; suite runtime + B.1/B.2/B.3 + N=2 sin regresion; paridad/delegacion .ps1; gates py/ps verdes; handoff autocontenido; release atomico (DECISION-0018)]
---

# TASK-0072 - Flujo de coordinacion por intents (write-path del estado)

> KEYSTONE de 3.b.2 (escritor unico). Promovida a ready tras cerrar TASK-0071 (F7.1). Ver SPEC-0058. Tras
> esta tarea verde: re-genesis (drift 0) + encender enforce+authoritative con GO del operador = 3.b.2 final.

## Contexto

Hoy los agentes mutan el estado editando los `*.json`. Para encender `enforce+authoritative` sin bloquear el
lazo hace falta un write-path por INTENTS: que una transicion se SOMETA al runtime (validar -> event log ->
materializar) dejando `hot == replay(log)` (drift 0). Ver SPEC-0058.

## Alcance (ver SPEC-0058 sec.3)

1. `runtime/submit_intent.py` (+ paridad/delegacion `.ps1`): `submit_intent(root, actor_id, intent, *,
   timestamp, commit)` para task_status / task_upsert / claim / decision.
2. Validar autoridad/scope por la capa existente (G1/tool-policy/turn_validate); intent invalido => rechazado.
3. Append `intent.applied` + `materialize_to_disk` atomico => `has_drift==False`. Determinista, idempotente.
4. Off-compatible (enforce on/off). Golden `examples/intent_flow_cases` + docs.

## Restricciones

- **Aditivo, off-compatible, determinista** (timestamp/commit provistos; sin reloj/red). **Neutral, sin
  secretos**, ASCII (DECISION-0012). Fallback N=2 intacto. Invariante G1 (no derivar permisos de contenido).
- NO encender enforce+authoritative en el repo vivo (paso final de 3.b.2, aparte). Cambio del turn schema mas
  alla de representar un intent => `blocked`.
- **Handoff autocontenido**; **release atomico** (DECISION-0018); anti-colision (DECISION-0020).

## Nota

Keystone de 3.b.2. Tras esta: re-genesis sincronizado + encender enforce+authoritative (GO del operador) =
escritor unico real. Promovida de a una. Codex autonomo: tomala cuando `ready`; GO por mailbox.
