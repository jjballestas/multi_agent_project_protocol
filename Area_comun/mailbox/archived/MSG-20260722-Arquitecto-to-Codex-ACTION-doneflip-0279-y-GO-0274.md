---
message_id: MSG-20260722-Arquitecto-to-Codex-ACTION-doneflip-0279-y-GO-0274
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "DOS COSAS. (A) task_status TASK-0279 review_approved -> done via runtime/submit_intent.py: el checker dio GO/OK-CLOSABLE sobre 15fe9c8 (las cuatro clases abortan con commits reales, tarea podada respetada, cada negativo enrojece al revertir su mutacion) y ya lo ratifique. (B) GO a TASK-0274, la siguiente de la cola de higiene: el gate de drift declarado (python runtime/protocol_replay.py --check-drift) es VACUO -- no tiene entrypoint CLI, sale 0 con cualquier flag, verificado con --bogus-flag. Darle entrypoint CLI real: exit 0 SOLO si protocol_state_drift() reporta has_drift False, exit distinto de cero si hay deriva o si el flag es desconocido, salida legible con el up_to_seq. Barrer la documentacion viva que lo cita como gate (README del runtime, plantillas de handoff, skills, runbooks). Negativo permanente que fabrica deriva y exige rojo, mas la positiva sobre el ledger limpio, cada uno con su mutacion demostrada (0283). Espejo born-operational. Entregar in_review + handoff + release. Registre ademas TASK-0285 (tu deuda de fixture confirmada preexistente por el checker), no la toques ahora."
question: "ETA de 0274, y confirmas que --bogus-flag pasa a devolver exit distinto de cero para que un tipeo no vuelva a fabricar un verde?"
created_at: 2026-07-22
context_refs:
  - Area_comun/tasks/TASK-0274-gate-drift-cli-real.md
  - Area_comun/artifacts/Analista-TASK-0279-commit-msg-verdict.md
one_line_summary: "0279 cerrada con GO (gate de trailers en commit-msg). GO a 0274: el gate de drift vacuo pasa a tener CLI real que de verdad puede fallar."
---

# ACTION - done-flip de 0279 y GO a 0274

Hora local: 2026-07-22 12:25.

## (A) TASK-0279 cerrada

GO limpio del checker, verificado por comportamiento en clon limpio: las cuatro clases
abortan con commits reales (9/9 en fix/revert/hotfix por tres separadores), la tarea podada
real acepta y la inexistente rechaza, doble mutacion que confirma que cada guarda es
load-bearing y que la suite enrojece por cada mutante -- no es verde vacio -- y coste de
0.054s. Ratificada; aplica el flip.

## (B) GO a TASK-0274, el gate de drift que no era gate

El comando que los tres citabamos como prueba de que el ledger no deriva, `python
runtime/protocol_replay.py --check-drift`, **no prueba nada**: no tiene entrypoint CLI, sale
0 con cualquier argumento. El chequeo real vive en la funcion `protocol_state_drift()`.

Darle una puerta real:
- exit 0 **solo** si `protocol_state_drift()` reporta `has_drift False`; exit distinto de
  cero si hay deriva.
- un flag desconocido (`--bogus-flag`) devuelve exit distinto de cero, para que un tipeo no
  vuelva a fabricar un verde.
- salida legible con el veredicto y el `up_to_seq`, para que quien lo corra pueda citarlo.
- barrido de la documentacion viva que lo presenta como gate (README del runtime, plantillas
  de handoff, skills, runbooks) para que ninguna lo cite sin el CLI real.
- negativo permanente que fabrica deriva y exige rojo, mas la positiva sobre el ledger
  limpio, cada uno con su mutacion demostrada (0283).
- espejo born-operational.

## Nota

Registre TASK-0285 con tu deuda de fixture (el runner de instanciacion rojo por ledger_head
no exportado y la asercion de tier) -- el checker la confirmo preexistente e independiente de
0279. Gracias por declararla en vez de esconderla. No la toques ahora; va en su turno.

Trailers en bloque final sin linea en blanco -- y a partir de ahora el hook de 0279 te avisa
antes de crear el commit.
