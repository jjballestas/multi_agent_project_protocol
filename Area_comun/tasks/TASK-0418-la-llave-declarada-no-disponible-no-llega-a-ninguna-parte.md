---
id: TASK-0418
title: La llave declarada no disponible se calcula, se pasa y no la lee nadie -- y la razon que deberia producir es inalcanzable
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0418-la-llave-declarada-no-disponible-no-llega-a-ninguna-parte.md
created: 2026-08-18
reviewer: Analista
intake:
  type: infra
  goal: >
    Reportado por la instancia NOVA tras medir v1.19.1 en copia fiel de su arbol, y verificado en el
    hub. Se reporto como DOS defectos; medido, es UNO: una funcion cableada por los dos extremos y
    desconectada por el medio.
    Extremo A -- `key_unavailable` esta declarado en `EVENT_AUTH_UNVERIFIABLE_REASONS`
    (`runtime/eventlog.py:32`) y **ningun camino lo devuelve**: es su UNICA aparicion en todo
    `runtime/`. Las razones que `verify_event_auth` si produce son trece, y esa no esta.
    Extremo B -- `declared_unavailable_key_ids` se **calcula**
    (`attested_unavailable_event_auth_key_ids`, `:1062`), se **pasa** (`:1071`, `:820`) y se
    **acepta** en la firma (`:746`), pero **el cuerpo no lo lee ni una vez**.
    Los dos extremos son la misma pieza: el parametro muerto es exactamente el que produciria la
    razon inalcanzable. Hoy una llave **atestada como no disponible** es indistinguible de una que
    simplemente no resuelve.
    Por que importa y no es cosmetico: esa distincion es la que desbloqueo a NOVA. Su medicion sobre
    1009 eventos da `unresolved_key` con 0 acusados -- el efecto es CORRECTO y v1.19.1 no se
    retracta -- pero el diagnostico que la instancia lee no nombra la causa real. Un fallo sin
    diagnostico hace que N causas parezcan una, que es la leccion que este repo lleva semanas
    pagando.
  acceptance:
    - "AC1 (decidir y ejecutar, no dejarlo a medias): o se CABLEA -- el parametro se lee y produce
      `key_unavailable` cuando la llave esta atestada como no disponible -- o se PODA entero: el
      parametro sale de la firma, de las dos llamadas y del calculo, y el nombre sale del set de
      razones. Las dos salidas son validas; lo que no vale es dejar el canal colgando."
    - "AC2 (si se cablea, la razon debe ser ALCANZABLE por conducta): existe una entrada que produce
      `key_unavailable` y no `unresolved_key`. Se acredita ejecutando esa entrada, no leyendo el
      codigo. Si tras el cambio ninguna entrada la produce, el arreglo no cerro nada."
    - "AC3 (si se poda, no queda rastro): `grep -rn` de `key_unavailable` y de
      `declared_unavailable_key_ids` en `runtime/` devuelve CERO. Un nombre que sobrevive en un set
      es una promesa que alguien leera como contrato."
    - "AC4 (el negativo, por MUTACION): sea cual sea la salida elegida, existe un mutante de
      produccion que MUERE. Si se cablea: quitar la lectura del parametro debe enrojecer. Si se poda:
      reintroducir el nombre en el set sin productor debe enrojecer. Sin esto, el defecto vuelve en
      el siguiente refactor y nadie se entera."
    - "AC5 (no se toca el efecto que ya funciona): la medicion de NOVA sobre su poblacion sigue dando
      CERO acusados con el registro puesto. Se acredita por censo diferencial antes/despues: el
      numero de eventos acusados no cambia."
  verification_cmd:
    - "python examples/replay_secret_independent_cases/run_replay_secret_independent_cases.py"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - runtime/eventlog.py
    - examples/replay_secret_independent_cases/run_replay_secret_independent_cases.py
  out_of_scope:
    - "Por COMPORTAMIENTO: queda fuera cambiar QUE eventos se acusan. Esta tarea cambia como se
      NOMBRA una causa, no el veredicto. Si al medir el censo diferencial de AC5 cambia el numero de
      acusados, el cambio se ha pasado de alcance y hay que parar."
    - "El agujero de la COLA de la cadena (TASK-0416) es otra tarea, aunque toque el mismo fichero."
  risk: medium
  estimate: M
---

# TASK-0418 -- una tuberia que calcula, pasa, acepta y no desemboca

## Origen

Intel de la instancia **NOVA** tras medir v1.19.1 en copia fiel de su arbol con secretos, la misma
cuenta tres veces sobre sus 1009 eventos. Lo reportaron como dos defectos; al verificarlo en el hub
resulta ser uno.

    v1.19.0 (su codigo actual)              1009 invalid_signature   ACUSADOS 1009
    v1.19.1 SIN registro de claves          1009 unknown_key_id      ACUSADOS 1009
    v1.19.1 CON registro (v1 retired@1009)  1009 unresolved_key      ACUSADOS 0

**El corte funciona.** Esta tarea no lo retracta: el veredicto es correcto y nadie queda acusado.
Lo que falla es que la instancia lee `unresolved_key` donde el diseno tenia previsto
`key_unavailable`, y esa distincion --llave atestada como no disponible frente a llave que no
resuelve-- es justo la que separa "te falta la llave" de "alguien manipulo esto", que es el problema
que abrio la saga entera de TASK-0414.

## Lo medido en el hub

    key_unavailable                 runtime/eventlog.py:32   <- UNICA aparicion en runtime/
    declared_unavailable_key_ids    :1062 se calcula
                                    :1071 se pasa
                                    : 820 se pasa
                                    : 746 se acepta en la firma
                                    cuerpo: leido 0 veces

Razones que `verify_event_auth` si devuelve: `active_key_has_boundary`, `event_auth_disabled`,
`invalid_key_status`, `invalid_signature`, `key_actor_mismatch`, `key_outside_validity`,
`missing_key`, `missing_key_id`, `missing_signature`, `retired_key_missing_boundary`,
`unknown_key_id`, `unresolved_key`, `valid`. **Trece, y `key_unavailable` no esta.**

## Por que una sola tarea y no dos

Porque el arreglo es una sola decision: **cablear o podar**. Partirlo en dos invita a cablear un
extremo y dejar el otro, que es exactamente el estado actual.
