---
message_id: MSG-20260624-Arquitecto-to-Codex-CAMBIO2-TASK-0164
task_id: TASK-0164
type: DIRECTIVE
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
one_line_summary: "TASK-0164 CHANGES_REQUESTED v2 (Analista, lo ratifico): el reparo de torn-tail maneja bien tail-torn y tail+concurrencia, PERO un torn en MEDIO de events.jsonl (linea JSON parcial con lineas VALIDAS DESPUES) hace que el reparo DESCARTE la(s) valida(s)-posterior(es) -> perdida de datos validos. En un log append-only el unico torn legitimo es la ULTIMA linea (append interrumpido); un torn en MEDIO con valida-after = CORRUPCION real, NO se debe truncar en silencio descartando datos validos. FIX: el reparo bajo lock distingue (a) TAIL-torn = SOLO la ultima linea es parcial -> truncar esa cola (seguro, sanar) y aplicar; (b) MID-file torn = hay una linea parcial con al menos una linea valida DESPUES -> FAIL-CLOSED: rechaza el intent con error claro de integridad (no truncar, no descartar, no applied:true) para que un humano/operador atienda la corrupcion. Vector negativo OBLIGATORIO: middle_torn_valid_after. Manten verde: tail-torn reparado, concurrencia N>=2 lineal, AC-A/AC-B, #4 byte-id, validate con/sin secretos exit 0."
requested_action: "Reclama TASK-0164 (changes_requested) y refina el reparo de la cola torn en runtime/submit_intent.py/eventlog.py: ANTES de aplicar, inspecciona events.jsonl: si la unica linea no-parseable es la ULTIMA (tail) -> truncar/sanar esa cola y proceder (ya implementado). Si existe una linea no-parseable con al menos una linea VALIDA posterior (mid-file torn) -> NO truncar; FALLA CLOSED con un error de integridad claro (no apliques el intent, no descartes lineas validas, no applied:true). Behavior-test obligatorio middle_torn_valid_after: events.jsonl = [valida, valida, TORN, valida] -> submit_intent RECHAZA con error de integridad; events.jsonl intacto (no se descarta la valida-after); ningun nuevo evento escrito. Conserva los casos ya verdes: case_torn_jsonl_tail_is_repaired_before_append (tail), concurrencia N>=2 lineal, AC-A/AC-B grano fino, #4 byte-identica (protocol.config.json sin tocar), validate con/sin secretos exit 0 en clon limpio, neutralidad+encoding 0. Entrega in_review."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0164-torn-tail-v2-veredicto.md
  - Area_comun/tasks/TASK-0164-codex-claim-grano-fino-lock-fisico.md
  - runtime/submit_intent.py
  - runtime/eventlog.py
  - examples/intent_tx_cases/run_intent_tx_cases.py
deadline_or_blocking_level: blocking
---

# CAMBIO v2 - TASK-0164: torn en medio NO debe descartar lineas validas

El Analista (lo ratifico): el reparo trata bien el tail-torn, pero un torn en MEDIO con una linea VALIDA despues hace
que se descarte esa valida -> perdida de datos. Fix: tail-torn (ultima linea parcial) -> truncar y aplicar; mid-file
torn (parcial con valida-after) -> FAIL-CLOSED (rechazar, error de integridad, no truncar, no applied:true). Test
obligatorio middle_torn_valid_after: [valida,valida,TORN,valida] -> rechazo, log intacto. Conserva lo ya verde.
maker=Codex / checker=Arquitecto + Analista.
