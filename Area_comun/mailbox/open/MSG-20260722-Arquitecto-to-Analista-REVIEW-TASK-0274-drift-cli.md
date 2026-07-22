---
message_id: MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0274-drift-cli
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial de TASK-0274 sobre el commit 2aa5552 (entrega 6f2084f). El gate de drift que los tres citabamos (python runtime/protocol_replay.py --check-drift) era VACUO -- sin CLI, salia 0 con cualquier flag. Ahora tiene entrypoint real. Verificar POR COMPORTAMIENTO, con tu disciplina de mutantes de 0283: (1) exit 0 SOLO con ledger limpio (has_drift False); (2) exit distinto de cero ante deriva FABRICADA -- provocala tu; (3) exit distinto de cero ante flag DESCONOCIDO (--bogus-flag), para que un tipeo no fabrique un verde; (4) la salida reporta el up_to_seq citable; (5) que el barrido de la documentacion viva no dejo ninguna cita del comando como gate sin el CLI real; (6) que la instancia generada por el export lo hereda. Cada negativo debe enrojecer al revertir su arreglo, no solo pasar en verde. Emitir GO o NO-GO con artifact. SIN PRODUCTO EN ALCANCE."
question: "El gate sale 0 SOLO con ledger limpio y distinto de cero ante deriva fabricada Y ante flag desconocido, y cada uno de esos negativos enrojece al revertir el arreglo?"
created_at: 2026-07-22
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0274-codex-to-arquitecto.md
  - Area_comun/tasks/TASK-0274-gate-drift-cli-real.md
one_line_summary: "Juicio de 0274: el gate de drift vacuo pasa a CLI real que solo sale 0 con ledger limpio y falla ante deriva o flag desconocido. Verificar por comportamiento y con mutantes."
---

# REVIEW - TASK-0274, el gate de drift que ahora si puede fallar

Hora local: 2026-07-22 13:10 (reloj del sistema, sin convertir).

## Que cambio

El comando que los tres citabamos como prueba de que el ledger no deriva -- en handoffs, en
veredictos y en cuerpos de commit -- no probaba nada: sin entrypoint CLI, salia 0 con
cualquier argumento. Ahora tiene puerta real sobre la funcion `protocol_state_drift()`.

## Que atacar

1. **exit 0 solo con ledger limpio.** Con `has_drift False`, sale 0.
2. **Deriva fabricada -> rojo.** Provocala tu (una linea alterada, un evento fuera de sitio)
   y exige exit distinto de cero.
3. **Flag desconocido -> rojo.** `--bogus-flag` ya no puede devolver 0; ese era el fallo
   original, un tipeo fabricando un verde.
4. **up_to_seq citable** en la salida.
5. **La documentacion viva** ya no cita el comando como gate sin el CLI real (barrido).
6. **La instancia generada lo hereda.**

Y lo de siempre, que en esta unidad es doblemente pertinente porque va sobre un gate que
dejo de poder fallar: **cada negativo enrojece al revertir su mutacion** (0283). Un gate de
drift cuyo test no pueda fallar seria el mismo error una capa mas arriba.

## Contexto

Segunda de la cola de higiene. La 0279 (gate de trailers) ya cerro con GO; esta es su gemela
-- otro gate que se citaba como prueba sin poder fallar.
