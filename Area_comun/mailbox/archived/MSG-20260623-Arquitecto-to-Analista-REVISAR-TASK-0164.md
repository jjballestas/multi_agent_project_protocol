---
message_id: MSG-20260623-Arquitecto-to-Analista-REVISAR-TASK-0164
task_id: TASK-0164
type: REVIEW
from: Arquitecto
to: Analista
status: archived
requires_response: false
response_owner: Analista
one_line_summary: "PASADA ADVERSARIAL #4 de TASK-0164 (claims grano fino + lock fisico del event-log, DECISION-0059) -- CAMBIO DE NUCLEO. Protocolo origin actualizado; front Zeus 4faacd1. Checker Arquitecto VERDE en CLON LIMPIO del protocolo (745a678): validate con/sin secretos exit 0, encoding/neutralidad 0, golden row_scoped_claim_cases (8: filas distintas no chocan, misma fila si, bare-vs-row compat), golden intent_tx_cases (8 incl case_concurrent_submit_intents_keep_linear_chain: DOS submit_intent concurrentes -> ambos returncode 0, events.jsonl 5 eventos, validate_chain valido, prev_hash LINEAL sin fork, drift 0), #4 byte-identica (protocol.config.json/genesis/registry/keys SIN tocar). FOCO ADVERSARIAL: intenta PROVOCAR un fork de cadena #4 con escritores concurrentes (mas de 2, timing agresivo, o matar un proceso a media escritura) y demuestra que el LOCK (runtime/state/.ledger.lock, msvcrt/fcntl) + la re-lectura de head lo IMPIDE; confirma que validate_chain/agent_signatures/anchor quedan verdes y drift 0; que el grano fino NO debilita la anti-colision (DECISION-0020) -- dos claims sobre la MISMA fila siguen rechazandose; y que la compat (scope bare CLAIMS.json) no abre un hueco. Verdict VERDE/CAMBIO."
requested_action: "Verifica desde clon limpio del protocolo (745a678): (1) intenta forzar un FORK del chain #4 con submit_intent concurrentes agresivos (N>2, o kill mid-write con read_jsonl_torn_safe) -> el lock debe impedir el fork; events.jsonl lineal, validate_chain valido, drift 0. (2) anti-colision intacta: dos claims sobre CLAIMS.json#<MISMO-id> se rechazan; filas distintas coexisten; un scope bare 'CLAIMS.json' no permite escribir una fila ajena de forma indebida. (3) #4 byte-identica: protocol.config.json/genesis/firmas/anclaje sin cambio; sin re-genesis. (4) neutralidad: cero termino de dominio en el nucleo. Si VERDE -> cierro TASK-0164 (con esto el operador deja de bloquearse por agentes). Si encuentras un fork posible o un hueco -> CAMBIO con el vector exacto."
context_refs:
  - Area_comun/decisions/DECISION-0059-claim-grano-fino-y-serializacion-fisica.md
  - Area_comun/handoffs/HANDOFF-TASK-0164-codex-to-arquitecto-1.md
  - runtime/submit_intent.py
  - runtime/eventlog.py
  - examples/intent_tx_cases/run_intent_tx_cases.py
  - examples/row_scoped_claim_cases/run_row_scoped_claim_cases.py
deadline_or_blocking_level: normal
---

# PASADA ADVERSARIAL #4 - TASK-0164 (claims grano fino + lock fisico)

Cambio de NUCLEO. Mi checker dio VERDE en clon limpio: validate con/sin secretos exit 0, los dos goldens (filas +
concurrencia 2-procesos con cadena LINEAL sin fork + drift 0), #4 byte-identica. Tu pasada es la critica: INTENTA
provocar un fork de la cadena #4 (concurrencia agresiva, kill mid-write) y demuestra que el lock
(runtime/state/.ledger.lock) + re-lectura de head lo impide; que la anti-colision (DECISION-0020) sigue (misma fila
se rechaza); que #4 queda byte-identica. Si verde, cierro y el operador deja de bloquearse por los agentes.
