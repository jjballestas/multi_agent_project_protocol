---
id: TASK-0387
title: El filtro que existe para NO serializar produce la serializacion maxima -- scope vacio se lee como ilegible y bloquea todo
status: ready
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0387-el-filtro-que-evita-serializar-produce-la-serializacion-maxima.md
created: 2026-08-14
reviewer: Analista
intake:
  type: fix
  goal: >
    Causa raiz, por fin identificada, del bloqueo cruzado de peones que arrastramos semanas (el
    sintoma vivia en TASK-0337 sin causa). `ConvertTo-ComparableRoute`
    (`scripts/harness/peer_mailbox_cron.ps1:1019`) DESCARTA a proposito toda ruta bajo
    `Area_comun/state` o `runtime/state`, y su propio comentario dice por que: "Treating their common
    container as material task overlap would serialize every peer". Pero si TODAS las rutas del claim
    caen ahi, `ConvertTo-ComparableScope` se queda con `$routes.Count -eq 0` y devuelve `$null`; y la
    linea 1116 trata ese `$null` como ILEGIBLE -- `if ($null -eq $claimScope) { return
    "active_external_claim" }` -- bloqueando TODO mensaje del peon, sin mirar solape. O sea: cuanto
    mas ESTRECHO y mas correcto es el claim del coordinador, MAS bloquea; el caso limite del filtro
    anti-serializacion es la serializacion total. Vacio significa "no queda ninguna ruta material que
    pueda solapar", que es exactamente lo contrario de "no se". Coste medido el 2026-08-14: un claim
    de coordinacion de cinco rutas, todas de ledger, dejo al peon difiriendo hasta que la remediacion
    de TASK-0378 agoto sus 7200 s y MURIO (`RETRY_EXHAUSTED defers=23 outcome=defer_terminal`), mas
    otras 7 h de parada. Clase: **fail-closed aplicado a la ausencia de evidencia en un punto donde
    la ausencia ES la evidencia.**
  acceptance:
    - "AC1 (la distincion que falta): el guard distingue `scope ILEGIBLE` -- no es array, entrada no
      string, comodines -- de `scope que no deja ninguna ruta material tras el filtro`. El primero
      sigue bloqueando (fail-closed correcto); el segundo NO bloquea. Se acredita con los DOS casos
      por comportamiento del cron, no por test unitario del helper."
    - "AC2 (prueba de que sigue RECHAZANDO donde debe): un claim externo con solape REAL sobre las
      `scope_routes` del mensaje sigue difiriendo, con su salida y exit code. Un arreglo que abre la
      puerta a todos no es arreglo. Este es el control historico obligatorio."
    - "AC3 (el caso que ocurrio, reproducido): claim externo cuyo scope es SOLO rutas de
      `Area_comun/state` y `runtime/state`, y un mensaje cuyo `scope_routes` no las toca -> el peon
      ARRANCA. Medido por `EXEC_START` en el log, no por inspeccion del helper."
    - "AC4 (el diagnostico nombra la causa): cuando el guard difiere por claim externo, el log dice
      QUE ruta del claim solapa con QUE ruta del mensaje. Hoy dice solo `active_external_claim`, y por
      eso costo semanas: el sintoma no distingue 'solapa de verdad' de 'no supe leer el scope'."
    - "AC5 (no se cambia de sitio el bloqueo): un claim con scope MIXTO -- ledger mas una ruta
      material que SI solapa -- sigue difiriendo. Medido."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory"
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - scripts/harness/peer_mailbox_cron.ps1
  out_of_scope:
    - "El rodeo aplicado el 2026-08-14 (anadir un ancla no-ledger `personal/Arquitecto/.ledger-commit-anchor`
      al scope del claim de coordinacion para que normalice no-vacio). Es un parche del llamante, no del
      guard, y se retira cuando esta tarea cierre. Queda declarado aqui para que no se confunda con el
      arreglo."
    - "TASK-0337 (el residue guard que veta sin mirar scope): es el hermano, mismo fichero, otra
      funcion. No se mezclan en una entrega."
    - "El gate de claim de producto (TASK-0378/0386): otra familia, otro fichero."
  risk: high
  estimate: S
---

# TASK-0387 -- el filtro anti-serializacion, en su caso limite, serializa

## El codigo, en tres lineas

    l.1019   if ($normalized -match '^(?i:Area_comun/state|runtime/state)(?:/|$)') { return $null }
             # comentario propio: "would serialize every peer"

    l.1032   if ($routes.Count -eq 0) { return $null }        # todas descartadas -> null

    l.1116   if ($null -eq $claimScope) { return "active_external_claim" }   # null -> BLOQUEA

Las dos primeras lineas existen para no bloquear. La tercera convierte su resultado en el bloqueo
mas fuerte que el guard sabe emitir.

## Lo medido el 2026-08-14

    claim de coordinacion, 5 rutas, TODAS de ledger
      -> Codex: RETRY_DEFER x23 reason=active_external_claim
      -> 18:10  RETRY_EXHAUSTED elapsed_seconds=7269 timeout_seconds=7200 outcome=defer_terminal
      -> el mensaje de remediacion de TASK-0378 MUERTO, y 7 h de parada

    mismo claim + UNA ruta no-ledger que no solapa con nadie
      -> 23:26:52 EXEC_START   (el peon arranca en la primera ronda)

El par discrimina: lo unico que cambio fue la presencia de una ruta que el filtro no descarta.

## Por que se declara de riesgo alto

Porque su forma es la de un fallo silencioso y caro: no rompe nada, no enrojece ninguna puerta, y su
unico sintoma -- `active_external_claim` -- es indistinguible de un bloqueo legitimo. Por eso se
diagnostico como "los peones se serializan" durante semanas en vez de como un bug de una linea.
