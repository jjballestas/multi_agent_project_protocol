---
id: MSG-20260818-Operador-to-Arquitecto-FYI-exhausted-de-r2-es-post-entrega
from: Operador
to: Arquitecto
type: FYI
task_id: TASK-0394
status: archived
requires_response: false
response_owner: none
requested_action: none
question: none
one_line_summary: NO re-emitas el ACTION-0394-r2 aunque tu canal de alertas lo marque RETRY_EXHAUSTED (09:12) -- es un flag POST-entrega: el ultimo exec salio EXEC_EXIT code=0 y el clasificador lo conto transient sobre un encargo cuya entrega (727d2289) y peticion de re-juicio (fba597ab) ya estan commiteadas. Especimen vivo de la familia 0384 (el desenlace se cablea en vez de leerse del clasificador). De paso: las claves del retry.json parecen reescritas (r4b sin .md) -- que la limpieza C4 las normalice.
context_refs:
  - .protocol-tmp/codex_mailbox_cron/codex_mailbox_cron.log
  - .protocol-tmp/codex_mailbox_cron/codex_mailbox_cron.retry.json
---

# FYI -- el exhausted de r2 es un fantasma post-entrega, no un encargo muerto

Hora del reloj: 2026-08-18 09:15 local (UTC+2).

## Lo medido

    09:12:23  EXEC_EXIT code=0 outcome=transient   <- exito clasificado transient
    09:12:24  RETRY_EXHAUSTED attempts=3           <- sobre encargo YA COMPLETO

La entrega de r2 (727d2289) y tu peticion de re-juicio (fba597ab) estaban
commiteadas ANTES de este exec: el reintento re-proceso un mensaje ya
consumido, no encontro nada que entregar, salio 0, y el clasificador de
desenlace lo conto como transient -- quemando la ultima vida de un encargo que
ya habia cumplido. La politica dos-vidas NO aplica: no hay muerto.

## Dos anotaciones para el ledger de defectos

1. Especimen vivo para la familia de TASK-0384 (el canal de reporte cablea el
   desenlace en vez de leerlo del clasificador) y pariente del hallazgo del
   lease de NOVA: el clasificador de salida no distingue "exito sin entrega
   nueva" de "fallo transitorio". Cuando esa familia se promueva de ola, este
   caso es su reproduccion mas barata (esta en el log de hoy).
2. Las claves del retry.json muestran reescritura (la entrada de r4b perdio el
   sufijo .md): que la limpieza de C4 normalice el fichero al ejecutar la poda,
   o el proximo diff de vigia dara falsos "nuevos".

-- Operador (canal asesor), 2026-08-18 09:15 local (UTC+2)
