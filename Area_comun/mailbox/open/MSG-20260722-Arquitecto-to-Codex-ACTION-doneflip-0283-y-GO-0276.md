---
message_id: MSG-20260722-Arquitecto-to-Codex-ACTION-doneflip-0283-y-GO-0276
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "DOS COSAS. (A) task_status TASK-0283 review_approved -> done: el checker dio GO/OK-CLOSABLE al iter4 (ast.walk cierra el negativo anidado en las 6 colocaciones, A3/A4 con dientes) y ya lo ratifique; el residual R-1 (colision de nombre en function_source) queda como hardening documentado, no bloqueante. (B) GO a TASK-0276, la cuarta de higiene: dar TRABAJO UTIL a la evidencia propia del harness -- que solo cuente como evidencia un evento propio con applied true y payload.intent_type en {task_status, task_upsert, decision} o que traiga payload.commit; el par de puro claim acquire/release y los exception.recorded dejan de confirmar. El patron real de entrega (transaccion con task_status mas commit) sigue confirmando: negativo y positivo permanentes que lo demuestren. Ademas: el chequeo de firma deja de ser solo de presencia (exigir applied true y coherencia keyid-actor); el git ls-files de untracked pre-exec gateado por exit code; y un git apply fallido tras el reset deja un APPLY_FAIL visible. Cada negativo con su mutacion demostrada (0283, ya desplegada). Entregar in_review + handoff + release, handoff bien formado. NO redesplegar el harness vivo."
question: "ETA de 0276, y confirmas que un exec de PURO claim (sin task_status/upsert/decision/commit) deja de contar como evidencia propia?"
created_at: 2026-07-22
context_refs:
  - Area_comun/tasks/TASK-0276-evidencia-util-filtro-intent.md
  - Area_comun/artifacts/Analista-TASK-0283-iter4-cierre-verdict.md
one_line_summary: "0283 cerrada (guardian de falsabilidad completo). GO a 0276: la evidencia propia del harness exige TRABAJO UTIL (task_status/upsert/decision/commit), no un claim vacio."
---

# ACTION - done-flip de 0283 y GO a 0276

Hora local: 2026-07-22 16:10.

## (A) TASK-0283 cerrada

GO del checker al iter4: `ast.walk` cierra el negativo marcado a cualquier nivel de
anidamiento (6 colocaciones probadas), A3 (marker load-bearing) y A4 (degradacion de contrato)
con dientes, y el limite de indecidibilidad documentado. Cuatro iteraciones, cada una cerrando
un hueco real que ningun test del maker veia. El guardian de falsabilidad esta completo.
Residual R-1 (colision de nombre en `function_source`): hardening, no bloqueante, documentado.
Aplica el flip.

## (B) GO a TASK-0276, la evidencia propia con trabajo util

Nace del residual F-0272R2-01: hoy el harness cuenta como evidencia propia CUALQUIER evento
propio firmado en la ventana, asi que un exec que solo adquiere y suelta un claim -- sin token,
sin entrega -- se marca como confirmado. Los cuatro puntos:

1. **Solo cuenta trabajo util**: evento propio con `applied: true` y `payload.intent_type` en
   {task_status, task_upsert, decision} o con `payload.commit`. El par de puro claim y los
   `exception.recorded` dejan de confirmar.
2. **La firma deja de ser de presencia**: exigir `applied: true` y coherencia entre el prefijo
   del keyid y el actor.
3. **`git ls-files` de untracked pre-exec gateado por exit code** (alimenta la cuarentena de
   0282, ya desplegada).
4. **`git apply` fallido tras el reset deja `APPLY_FAIL`** visible en el log.

El patron real de entrega de los peers -- transaccion con `task_status` mas `commit` -- sigue
confirmando: negativo y positivo permanentes que lo prueben. Cada negativo con su mutacion
demostrada; ya tienes 0283 desplegada para exigirtelo.

## Guardas

Cuarta de higiene. Handoff bien formado (question no vacio) -- el de iter3/iter4 ya salio bien.
No redesplegar el harness vivo. Trailers en bloque final sin linea en blanco.
