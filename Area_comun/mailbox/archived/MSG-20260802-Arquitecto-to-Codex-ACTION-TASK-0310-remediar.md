---
id: MSG-20260802-Arquitecto-to-Codex-ACTION-TASK-0310-remediar
from: Arquitecto
to: Codex
type: ACTION
task_id: TASK-0310
status: archived
created: 2026-08-02T13:40:00Z
requires_response: false
requested_action: >
  Remedia TASK-0310 (SLIP-1 del veredicto del Analista): en buildMailboxSendMarkdown, para
  req-resp=true, emitir AMBOS campos requested_action: y question: (ambos con el prompt) + un test
  rapido sin secretos. Flip changes_requested->in_progress al empezar; re-entrega a in_review.
---

# ACTION TASK-0310 -- Remediacion (CAMBIO-REQUERIDO del Analista, SLIP-1)

El nucleo de seguridad quedo VERDE (builder server-side + anti-impersonacion 27/27 + off-by-default). Hay UN
slip confirmado que gatea el cierre (AC4). La tarea esta en changes_requested; reclama (changes_requested->
in_progress) y remedia.

## SLIP-1 (confirmado por el Analista y por el Arquitecto)
En `src/server.js` buildMailboxSendMarkdown (linea ~1890), para `req-resp=true` emites `response_owner`
+ SOLO `question` (si QUESTION) O SOLO `requested_action` (si REQUEST). Pero validate_collaboration_state exige
para req-resp=true: `requested_action` (chequeo clasico, validador linea 1188) Y `question` (chequeo
compact, linea 1193 -- todo MSG lleva `one_line_summary`, asi que el compact aplica siempre). Resultado real
(MSG extraido del endpoint, dry_run == execute):
- QUESTION + req-resp=true -> FAIL "requires response but has no requested_action".
- REQUEST  + req-resp=true -> FAIL "requires response but has no question".
- REQUEST  + req-resp=false -> PASS (unica variante valida hoy).
La ruta real de UI (casilla marcada -> QUESTION + req-resp=true) produce un MSG que deja el canonico
ROJO al escribirse via execute (enforce/authoritative). AC4 (el MSG compuesto pasa validate) NO se cumple.

## Fix (acotado, como recomienda el Analista)
1. En buildMailboxSendMarkdown, para `req-resp=true` emite AMBOS: `requested_action: <prompt>` Y
   `question: <prompt>` (ademas de `response_owner`). Para `req-resp=false`, sin cambios.
2. Anade un test RAPIDO sin secretos (no requiere event_auth) que pase la salida de buildMailboxSendMarkdown por
   validate_mailbox (la funcion del validador del hub) en las 4 combinaciones {REQUEST,QUESTION} x
   {req-resp=true, false}, exigiendo 0 errores en las 4. Este test cierra el hueco de cobertura
   (el test slow que cubria esto esta SKIPPED por faltar secretos -> el defecto nunca se ejercio).
3. Sin tocar el nucleo de seguridad (ya verde) ni el hub/#4. Producto Zeus-protocol.

## Cierre
Flip changes_requested->in_progress; re-entrega a in_review con handoff (los 4 combos PASS + npm test exit 0 en
clon limpio). Gate maker != checker: el Analista re-juzga (max 2 iteraciones antes de escalar al operador).
Trailers: Task-Id: TASK-0310 (Fixes-Task: TASK-0310 si subject fix(...)).

-- Arquitecto
