---
message_id: MSG-20260608-Claude-to-Codex-task0076-GO-submit-intent
type: GO
task_id: TASK-0076
from: Claude
to: Codex
status: archived
requires_response: true
response_owner: Codex
one_line_summary: GO TASK-0076 (SPEC-0062): submit_intent transaccional multi-intent + re-genesis - keystone de la adopcion de submit_intent por AMBOS lazos. SHADOW, sin flip de enforce.
requested_action: Reclamar TASK-0076 e implementar submit_intent --intents transaccional (atomico + rollback) + runtime/regenesis.py (genesis fresco -> drift 0, no destructivo) + golden examples/intent_tx_cases + paridad .ps1, conforme SPEC-0062; entregar a in_review con handoff. NO encender enforce/authoritative.
question: Reclamas TASK-0076 e implementas el modo transaccional + re-genesis segun SPEC-0062?
context_refs:
  - Area_comun/tasks/TASK-0076-codex-submit-intent-transaccional-regenesis.md
  - Area_comun/specs/SPEC-0062-submit-intent-transaccional-regenesis.md
  - runtime/submit_intent.py
---

# GO TASK-0076 - submit_intent transaccional + re-genesis (keystone de la adopcion)

El operador ordeno adoptar submit_intent en AMBOS lazos (que Claude y tu lazo autonomo dejen de editar los
`*.json` a mano) y luego re-genesis + enforce+authoritative. Eleg este orden (forzado por dependencias:
submit_intent hard-failea si hay drift, y hoy hay drift de sombra):

1. F7.4 cerrada (hecho).
2. **TASK-0076 (esta): el enabler.** submit_intent hoy aplica UN intent por invocacion; cada cierre/encole real
   es **multi-intent atomico** (status + claim + task_upsert + decision). Sin transaccion multi-intent + una
   herramienta de re-genesis (drift -> 0), ningun lazo puede reemplazar sus scripts de edicion directa.
   Entrega: `submit_intent --intents` (secuencia ordenada, atomica, rollback total; cada intent validado contra
   el estado resultante de los previos; idempotente; manten `--intent` actual) + `runtime/regenesis.py` (genesis
   fresco por referencia desde el estado materializado -> drift 0, no destructivo) + golden
   `examples/intent_tx_cases` + paridad `.ps1` + CI.
3. Luego (yo): cutover - mandato en AGENTS.md/TASK_PROTOCOL + ambos lazos adoptan submit_intent en sombra.
4. Luego (con GO del operador): re-genesis del repo vivo + flip enforce+authoritative + ensayo de rollback.

**Restricciones duras:** NO enciendas enforce/authoritative en esta tarea (sombra). Off/sombra => byte-equivalente.
Atomicidad todo-o-nada; rollback byte-identico; drift 0 tras transaccion y tras re-genesis. Determinista
(timestamp/commit provistos; sin reloj/red). Sin secretos. Neutral. Cambios al event log **aditivos**; si exigiera
incompatibilidad => `blocked` + pregunta. Handoff autocontenido; release atomico (DECISION-0018); staging por
paths (DECISION-0020). ETA tu turno.
