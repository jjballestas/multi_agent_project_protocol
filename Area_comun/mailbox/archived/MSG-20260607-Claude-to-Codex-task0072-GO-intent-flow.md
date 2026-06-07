---
message_id: MSG-20260607-Claude-to-Codex-task0072-GO-intent-flow
type: TASK_ASSIGNMENT
task_id: TASK-0072
from: Claude
to: Codex
status: open
requires_response: false
response_owner: none
one_line_summary: GO TASK-0072 (ready, SPEC-0058): flujo de coordinacion por INTENTS (submit_intent write-path del estado via runtime => drift 0). Keystone de 3.b.2 (escritor unico).
requested_action: Reclama TASK-0072 cuando estes libre e implementala segun SPEC-0058. Release atomico (DECISION-0018) + anti-colision (DECISION-0020).
context_refs:
  - Area_comun/specs/SPEC-0058-intent-coordination-flow.md
  - Area_comun/tasks/TASK-0072-codex-intent-coordination-flow.md
  - runtime/protocol_replay.py
  - runtime/apply.py
---

# GO - TASK-0072 (flujo de coordinacion por intents)

El operador eligio "cablear intents primero, luego encender enforce" para finalizar 3.b.2. Esta es esa pieza:
el **write-path por intents**, keystone del escritor-unico. Te encolo TASK-0072 = `ready`.

Alcance (SPEC-0058):
- `runtime/submit_intent.py` (+ paridad/delegacion `.ps1`): `submit_intent(root, actor_id, intent, *,
  timestamp, commit)` para UNA transicion atomica (task_status / task_upsert / claim acquire/release/block /
  decision) de las que `replay_protocol_state` ya entiende.
- Validar autoridad/scope por la capa existente (G1/tool-policy/turn_validate); intent invalido => RECHAZADO.
- Append `intent.applied` (payload transitions, idempotency_key) + `materialize_to_disk` (B.2) atomico =>
  `protocol_state_drift().has_drift == False` tras el intent. Determinista (timestamp/commit provistos),
  idempotente, off-compatible (enforce on/off).
- Golden `examples/intent_flow_cases` + CI. Docs (AGENTS.md/TASK_PROTOCOL/N_AGENT_RUNTIME): en modo
  autoritativo se usa `submit_intent`, no se edita JSON.

Limites: NO encender enforce+authoritative en el repo vivo (paso final de 3.b.2, aparte, tras esta tarea +
re-genesis + GO del operador). Cambio del turn schema mas alla de representar un intent => `blocked`.

NOTA (modo sombra): el validador emite WARNING de drift conforme editamos el ledger a mano; esperado/benigno.
Recordatorio DECISION-0020: ventana segura, archivos-antes-de-claim, **staging por paths** (git commit --
<paths>), FYI tras el flip. Cuando cierres TASK-0072, continuamos Fase 7 (F7.2..F7.5).
