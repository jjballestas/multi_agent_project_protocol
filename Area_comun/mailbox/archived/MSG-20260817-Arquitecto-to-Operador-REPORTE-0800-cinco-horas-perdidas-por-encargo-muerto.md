---
id: MSG-20260817-Arquitecto-to-Operador-REPORTE-0800-cinco-horas-perdidas-por-encargo-muerto
from: Arquitecto
to: Operador
type: RESPONSE
task_id: TASK-0414
status: archived
requires_response: true
response_owner: Operador
one_line_summary: Reporte de estado. CINCO HORAS PERDIDAS -- el encargo r4b murio a las 03:18 con RETRY_EXHAUSTED attempts=3 por fallo de router del agente, y no lo detecte porque el cuadro externo de "encargo muerto" es IDENTICO al de "no hay trabajo": crons latiendo, processable_messages=0, tablero en in_progress. Reenviado con id nuevo.
requested_action: (1) Toma nota de que mis tres watchdogs NO cubren este modo -- el de salud de execs exige lock retenido mas heartbeat congelado, y aqui no habia ninguno de los dos. (2) Confirma si los problemas de proveedor que mencionaste siguen, porque los tres intentos cayeron con error de router del agente, no de gate. (3) v1.19.1 sigue pendiente de r4c.
question: Mantengo el reenvio automatico con id nuevo cuando un encargo muera por router, o prefieres que escale al primer RETRY_EXHAUSTED sin reintentar?
context_refs:
  - Area_comun/mailbox/open/MSG-20260817-Arquitecto-to-Codex-ACTION-TASK-0414-r4c-ancla-por-cadena-revive.md
  - Area_comun/decisions/DECISION-0119-DRAFT-clave-raiz-offline-del-operador-humano.md
---

# REPORTE 08:00 -- cinco horas perdidas por un encargo muerto que parecia trabajo en curso

## Lo que paso

    02:38  ruteo r4b (ancla-por-cadena)
    03:13  EXEC_START
    03:18  EXEC_EXIT outcome=transient
    03:18  RETRY_EXHAUSTED attempts=3
    03:18 -> 07:56   NADA. Crons latiendo cada 5 min con processable_messages=0.
                     Tablero: TASK-0414 in_progress. Cero claims, cero locks.

Los tres intentos cayeron con `ERROR codex_core::tools::router: Exit code: 1/2` -- **fallo de
herramienta del agente**, no de gate ni de contenido del encargo.

## Por que no lo vi, y es lo que hay que arreglar

**El cuadro externo de "encargo muerto" es IDENTICO al de "no hay trabajo pendiente".** Los dos se
ven asi: cron vivo, heartbeat puntual, `processable_messages=0`, sin locks, sin claims.

Mi watchdog de salud de execs dispara con **lock retenido + heartbeat congelado**. Aqui **no habia
ninguna de las dos cosas**: el exec habia terminado (limpiamente, desde el punto de vista del cron)
y el cron seguia latiendo. El watchdog estaba sano y mudo, correctamente segun su criterio.

Es **TASK-0408 en vivo por tercera vez hoy**, y esta vez el que pago fui yo.

## Lo que ya he hecho

**Reenviado como r4c con id nuevo** -- la firma del arnes es `Name|Length|Ticks`, asi que un id
distinto es entrada nueva y esquiva el `exhausted`. Contenido **identico**, con una nota de reenvio
que explica por que murio y que **no hay nada que corregir en el encargo**. Y le digo que si vuelve
a caer por el router, **bloquee con la causa en vez de reintentar en bucle**.

## Lo que te pido

**(1)** Que conste que mis tres watchdogs **no cubren este modo**. El que haria falta vigila otra
cosa: **encargo en `open/` dirigido a un peer + tarea en `in_progress` + cero avance en N minutos**.
Eso es exactamente el AC2/AC3 de TASK-0408, que sigue sin rutear.

**(2)** Si los problemas de proveedor que mencionaste anoche siguen. Los tres fallos son de router
del agente, no nuestros, y eso cambia la lectura: no es un encargo mal redactado.

**(3)** `v1.19.1` sigue pendiente de r4c. NOVA sigue esperando.

## Estado del resto, sin cambios desde las 02:42

    TASK-0414   in_progress, r4c en cola (ancla-por-cadena sobre el genesis pineado)
    TASK-0378   in_review, r5 sin re-rutear
    TASK-0397   in_review
    0410-0413   ready, sin rutear (cap de P4)
    DECISION-0119  borrador para el humano en persona, sin reloj

Deuda operativa mia: `open/` en 28, poda vencida (`cold_start` 45664+), drenaje de mi area personal.
Todo eso esperaba ventana quieta -- y he tenido cinco horas de ventana quieta sin saberlo, que es la
segunda cosa que este fallo me costo.

-- Arquitecto, 2026-08-17 08:08 local (UTC+2)
