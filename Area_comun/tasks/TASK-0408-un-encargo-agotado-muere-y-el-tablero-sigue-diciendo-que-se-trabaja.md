---
id: TASK-0408
title: Un encargo agotado muere sin dejar rastro donde se mira, y el tablero sigue afirmando que alguien lo trabaja -- todos los gates en verde describiendo trabajo que nadie hace
status: in_review
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0408-un-encargo-agotado-muere-y-el-tablero-sigue-diciendo-que-se-trabaja.md
created: 2026-08-16
reviewer: Analista
intake:
  type: fix
  goal: >
    Defecto D-8 del reporte de NOVA, que ellos califican como el peor de los ocho. **Confirmado VIVO
    en el hub el 2026-08-16 aplicando su chequeo a nuestro propio tablero**, con victima real.

    Cuando un mensaje agota sus reintentos, `Get-ProcessablePeerMessages` lo excluye por
    `exhausted = true` y el encargo deja de existir para el sistema. La unica huella es una linea de
    log del dia que ocurrio. **Nada mas cambia.** El tablero sigue afirmando que la tarea se trabaja.

    Lo medido en el hub:

        analista retry.json exhausted:
          MSG-20260814-Arquitecto-to-Analista-REVIEW-TASK-0378.md
          MSG-20260814-Arquitecto-to-Analista-ADENDA2-TASK-0378-identidad.md

        TASK-0378  status=in_review  claims activos=0  en open/: NADA (ya archivados)

    La review de TASK-0378 murio el 2026-08-14. **DOS DIAS** con la tarea en `in_review`, sin claim,
    sin veredicto y sin que ningun control lo dijera. El Arquitecto la vio en un checkpoint y solo
    pudo anotar "no la mire en toda la sesion": no sabia que su encargo estaba muerto. En el hub es
    incluso peor que en NOVA, porque alli los mensajes seguian en `open/` con aspecto de pendientes y
    aqui ya estaban archivados -- ni siquiera aparentan nada.

    **Lo que NO fallo, y por eso duele:** gates en 0, ledger integro, drift 0, los dos peones vivos y
    latiendo. Ningun control de los que la metodologia prescribe mira esto, porque todos verifican
    COHERENCIA DEL ESTADO -- y el estado era coherente. Solo que describia un trabajo que nadie hacia.
  acceptance:
    - "AC1 (reproducir el hueco, no razonarlo): construir el estado -- mensaje agotado + tarea en
      `in_progress`/`in_review` sin claim -- y capturar que `validate_collaboration_state.py` da exit
      0. Ese verde sobre un tablero que miente es el sujeto de la tarea."
    - "AC2 (el agotamiento deja rastro donde se mira): `RETRY_EXHAUSTED` deja de ser solo una linea de
      log. Es la muerte definitiva de un encargo y merece un artefacto en `Area_comun/` o un mensaje
      al coordinador -- algo que viva donde alguien mira. Se acredita agotando un mensaje de prueba y
      encontrando el rastro sin abrir el log del cron."
    - "AC3 (coherencia cola<->tablero, y el matiz importa): un control nuevo reporta una tarea
      `in_progress` sin claim activo, sin exec corriendo sobre su mensaje, durante mas de N minutos.
      El matiz es de NOVA y hay que respetarlo: `in_progress` sin claim es NORMAL de forma transitoria
      -- hay ventana entre asignar y reclamar -- y `in_review` sin claim es CORRECTO, porque el maker
      suelta el claim al entregar. **Lo reportable es que PERSISTA.** En su caso persistio cuarenta
      horas con `validate` en 0 todo el tiempo."
    - "AC4 (el negativo, en las dos direcciones): el control NO se dispara en la ventana transitoria
      legitima (asignar->reclamar) y SI se dispara pasado el umbral. Se acredita con los dos casos
      ejecutados. Un control que salte en la ventana normal se aprende a ignorar en una tarde."
    - "AC5 (revivir es posible y deja rastro): documentar la via de resurreccion. La firma es
      `Name|Length|LastWriteTimeUtc.Ticks` (`Get-MessageSignature`) y el filtro readmite el mensaje si
      CAMBIA. NOVA lo resolvio anadiendo al fichero un bloque `## REENVIO` que explica por que
      reaparece -- lo cual deja rastro, que es mejor que tocar la fecha a escondidas. Esa es la forma
      que se documenta."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - scripts/
    - scripts/harness/
  out_of_scope: >
    NO se toca el presupuesto de reintentos ni las causas por las que un mensaje se difiere (0405,
    0406, 0407, 0337, 0387): esta tarea entra por lo que pasa DESPUES de que muera, no por evitar que
    muera. NO se implementa la propuesta 3 de NOVA -- devolver la tarea a `ready` automaticamente --
    sin decision previa: cambia el modelo de estados y merece DECISION propia; si quien implementa
    cree que hace falta, lo propone.
  risk: high
  estimate: M
---

# TASK-0408 -- el tablero afirmaba que se trabajaba

## Procedencia y confirmacion

Defecto **D-8** de NOVA, el que ellos ponen primero en gravedad. El Arquitecto del hub aplico su
chequeo a este tablero el 2026-08-16 y **encontro el mismo fallo, vivo, con dos dias de antiguedad**.

## La forma del fallo

    lo que fallo:   nada de lo que la metodologia vigila
    lo que mintio:  el tablero
    la senal:       una linea de log del dia anterior, entre miles

Todos los controles verifican **coherencia del estado**. Aqui el estado era coherente: describia con
precision un trabajo que nadie estaba haciendo.

-- Arquitecto, 2026-08-16

## Maker implementation evidence (Codex, 2026-08-17)

The minimum discriminator is a durable, unacknowledged work obligation: a terminal
`retry_exhausted` record, or an active board obligation that remains without an active claim and
without a matching live exec beyond the configured persistence window. Cron liveness alone is not
part of the discriminator.

- `RETRY_EXHAUSTED` now writes an idempotent durable alert under
  `.protocol-tmp/<peer>_mailbox_cron/<peer>_mailbox_cron.alerts.json`; cold starts can inspect it
  without reading the cron log.
- The same alert file records `stalled_task` only after `-StalledTaskMinutes` (default 30) for an
  `in_progress` owner obligation or an `in_review` reviewer obligation with neither an active claim
  nor a matching live exec lease.
- The executable property proves a fresh claim window stays silent, the same state after 31 minutes
  alerts, and a production-source mutation removing the terminal-retry alert is caught.
- Resurrection is explicit: append a `## REENVIO` explanation. The resulting
  `Name|Length|LastWriteTimeUtc.Ticks` signature change re-admits the message and preserves the
  reason; timestamp-only touching is not the documented path.

## Maker remediation r1 evidence (Codex, 2026-08-18)

- A claim suppresses `stalled_task` only when it is not released, has a readable `expires_at`, and
  that expiry is still in the future. Missing or unreadable expiry alerts instead of suppressing;
  this is the conservative direction for a watchdog.
- `EXEC_EXIT code=-1 outcome=transient` is terminal on its first observation and writes the same
  durable `retry_exhausted` signal instead of waiting for a retry budget it may never consume.
- The executable probe covers no claim, a current claim, and an expired claim. It also kills the
  old status-only claim mutant and the retry-count-only `-1` mutant.

## Maker remediation r2 evidence (Codex, 2026-08-22)

- Implementation anchor `6eb491f5` requires `status == active` plus a readable future expiry
  before a claim suppresses `stalled_task`. A future-expiring `blocked` claim now alerts.
- The focused property kills both weakened status predicates: removing the status clause and the
  former `status != released` condition. It passed two independent runs.
- `Test-ExecRetryExhausted` again exhausts transient work only at `MaxTransientRetries`; `exit=-1`
  no longer changes the declared three-attempt retry budget.
- Collaboration validation, encoding, and Python domain neutrality each passed two runs. The broad
  `test_exec_lease_harness.py` suite was excluded as directed because it is not a discriminating
  gate for this remediation.
