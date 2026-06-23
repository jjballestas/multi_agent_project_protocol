---
message_id: MSG-20260624-Arquitecto-to-Codex-CAMBIO-TASK-0164
task_id: TASK-0164
type: DIRECTIVE
from: Arquitecto
to: Codex
status: archived
requires_response: false
response_owner: Codex
one_line_summary: "TASK-0164 CHANGES_REQUESTED (Analista CAMBIO, lo ratifico): el lock evita forks (concurrencia N=8 lineal OK), PERO el append NO maneja una COLA JSON PARCIAL/cortada en events.jsonl. Si el ultimo registro quedo torn (write parcial por crash/kill mid-write), el siguiente submit_intent bajo lock ESCRIBE el nuevo evento DETRAS de la linea cortada -> queda INVISIBLE para read_jsonl_torn_safe (que para en la linea torn), pero submit_intent reporta applied:true y los gates validan sobre el PREFIJO -> integridad #4 rota silenciosamente. FIX: el append bajo lock debe, ANTES de aceptar un intent nuevo, DETECTAR una cola JSON parcial y TRUNCARLA (sanar) o RECHAZAR el intent (fail-closed) -- nunca aceptar applied:true dejando un evento invisible. Agrega caso al golden de concurrencia: events.jsonl con una ultima linea PARCIAL -> submit_intent o trunca la cola y aplica visiblemente, o falla; jamas applied:true con evento detras del torn; validate_chain/drift ven el evento real."
requested_action: "Reclama TASK-0164 (changes_requested) y corrige el append bajo lock (runtime/submit_intent.py + runtime/eventlog.py). ANTES de escribir el nuevo evento, dentro del lock, INSPECCIONA la cola de events.jsonl: si la ultima linea es JSON PARCIAL/torn (no parsea), o (a) TRUNCALA de forma segura (sanar la cola a la ultima linea valida) y registra el saneo, o (b) RECHAZA el intent fail-closed (error claro), segun lo que preserve mejor la integridad de la cadena; en ningun caso aceptes el intent dejando el nuevo evento DETRAS de una linea torn con applied:true. Behavior-test (extiende el golden de concurrencia/intent_tx): events.jsonl con ultima linea parcial -> el resultado es consistente (cola saneada + evento visible y encadenado, O rechazo), NUNCA applied:true con evento invisible; read_jsonl_torn_safe y validate_chain ven el mismo head real; drift 0. Manten lo ya verde: concurrencia N>=2 lineal, AC-A/AC-B (grano fino + compat), #4 byte-identica (protocol.config.json sin tocar), validate con/sin secretos exit 0 en clon limpio, neutralidad+encoding 0. Entrega in_review."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0164-lock-fisico-veredicto.md
  - Area_comun/tasks/TASK-0164-codex-claim-grano-fino-lock-fisico.md
  - runtime/submit_intent.py
  - runtime/eventlog.py
  - examples/intent_tx_cases/run_intent_tx_cases.py
deadline_or_blocking_level: blocking
---

# CAMBIO - TASK-0164: cola JSON parcial deja evento invisible (integridad #4)

El Analista (y lo ratifico) encontro un hueco real: el lock evita forks (N=8 lineal), pero si events.jsonl tiene una
ULTIMA LINEA PARCIAL/torn (write a medias por crash/kill), el siguiente submit_intent bajo lock escribe el nuevo
evento DETRAS de esa linea -> read_jsonl_torn_safe para en el torn y no lo ve, pero submit_intent dice applied:true y
los gates validan el PREFIJO. Fix: el append bajo lock DETECTA la cola parcial y la TRUNCA (sanar) o RECHAZA el
intent (fail-closed) antes de aceptar; nunca applied:true con evento invisible. Golden: ultima linea parcial -> cola
saneada+evento visible/encadenado o rechazo; jamas evento detras del torn. maker=Codex / checker=Arquitecto + Analista.
