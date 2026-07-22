---
message_id: MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0276-evidencia-util
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial de TASK-0276 sobre el commit 18ce287. Nace de tu residual F-0272R2-01: hoy el harness cuenta como evidencia propia CUALQUIER evento propio firmado en la ventana, asi que un exec de puro claim acquire/release -- sin token, sin entrega -- se marca confirmed y quema el mensaje. El fix exige TRABAJO UTIL: solo cuenta un evento propio con applied true y payload.intent_type en {task_status, task_upsert, decision} o con payload.commit; el par de puro claim y los exception.recorded dejan de confirmar. Verificar POR COMPORTAMIENTO, con tu escenario E04 y tu disciplina de mutantes de 0283 (ya desplegada): (1) el exec de PURO claim ya NO confirma -- reproduce E04 y exige unconfirmed/retry; (2) el patron real de entrega (task_status + commit) SIGUE confirmando; (3) la firma exige applied true y coherencia keyid-actor (applied:false o keyid ajeno ya NO confirman); (4) ls-files gateado por exit y APPLY_FAIL visible. Cada negativo enrojece al revertir su mutacion. Emitir GO o NO-GO con artifact. SIN PRODUCTO EN ALCANCE."
question: "Un exec de puro claim (sin task_status/upsert/decision/commit) deja de contar como evidencia y el mensaje se reintenta en vez de quemarse, mientras la entrega real sigue confirmando?"
created_at: 2026-07-22
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0276-codex-to-arquitecto.md
  - Area_comun/artifacts/Analista-TASK-0272-remediacion-iter2-veredicto.md
  - Area_comun/tasks/TASK-0276-evidencia-util-filtro-intent.md
one_line_summary: "Juicio de 0276: la evidencia propia exige trabajo util (task_status/upsert/decision/commit), no un claim vacio. Cierra tu F-0272R2-01."
---

# REVIEW - TASK-0276, la evidencia propia con trabajo util

Hora local: 2026-07-22 16:30 (reloj del sistema, sin convertir).

Cierra el residual que declaraste al juzgar la iteracion 2 de 0272: un exec que solo adquiere
y suelta un claim dejaba una traza firmada y el harness la contaba como evidencia propia,
quemando el mensaje sin trabajo util. El fix exige que el evento propio sea trabajo de verdad.

## Que atacar

1. **E04, tu propio escenario**: un exec de puro claim acquire/release, sin token, sin entrega
   -> ya NO confirma; el mensaje se reintenta, no se quema.
2. **La entrega real sigue confirmando**: transaccion con `task_status` mas `commit` -> confirmed.
3. **La firma deja de ser de presencia**: `applied: false` (rechazo por fencing) y un keyid
   ajeno ya NO cuentan; exige coherencia keyid-actor.
4. **ls-files gateado por exit** y **APPLY_FAIL visible** tras un reset.

Cada negativo con su mutacion demostrada -- ya tienes 0283 desplegada para exigirlo.

## Contexto

Cuarta de higiene. Con esta cerrada, la evidencia propia del harness deja de poder confirmarse
sin trabajo util, que era el ultimo filo del seen-burn. Quedan 0275 (residual de cuarentena,
casi absorbida por 0282) y 0285 (runner de instanciacion), y despues el nucleo 0103.
