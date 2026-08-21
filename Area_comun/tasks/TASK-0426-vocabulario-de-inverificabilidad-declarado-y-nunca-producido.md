---
id: TASK-0426
title: El vocabulario de inverificabilidad esta declarado y nunca se produce, y su parametro es codigo muerto
status: ready
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0426-vocabulario-de-inverificabilidad-declarado-y-nunca-producido.md
created: 2026-08-22
reviewer: Analista
intake:
  type: fix
  goal: >
    Dos hallazgos gemelos en runtime/eventlog.py, reportados por la instancia NOVA y verificados
    aqui. (1) EVENT_AUTH_UNVERIFIABLE_REASONS (:32) declara tres motivos -- unresolved_key,
    missing_key y key_unavailable -- y "key_unavailable" NO LO PRODUCE NADIE: es su unica
    aparicion en todo runtime/ y scripts/. Todos los caminos reales devuelven "unresolved_key"
    (:585-621, :779, :783, :958), asi que la frontera solo sabe decir una cosa donde el vocabulario
    promete tres. (2) declared_unavailable_key_ids es PARAMETRO MUERTO de verify_event_auth: se
    declara (:745), replay_events lo CALCULA con attested_unavailable_event_auth_key_ids (:1061),
    se pasa desde dos llamantes (:819, :1070) -- y no se referencia ni una sola vez en el cuerpo de
    la funcion. El dato de que una clave estaba declarada como no disponible se computa, se
    transporta y se descarta en destino.
  acceptance:
    - "AC1: o key_unavailable tiene un productor real y acreditado, o sale del conjunto. Un
      vocabulario cuyos terminos no se pueden emitir miente sobre lo que la frontera distingue.
      La eleccion se declara con su razon; las dos son aceptables, la ambiguedad no."
    - "AC2: o declared_unavailable_key_ids se usa en el cuerpo de verify_event_auth con efecto
      OBSERVABLE, o se elimina junto con su computo y su transporte. Si se usa, acreditar con el
      par: una clave declarada no disponible produce un veredicto DISTINTO del que produce una
      clave simplemente irresoluble."
    - "AC3: si se elimina, acreditar que attested_unavailable_event_auth_key_ids no tiene otro
      consumidor vivo antes de borrar nada; si lo tiene, no se borra."
    - "AC4: el cambio no altera ningun veredicto de la cadena existente. Acreditar validate y
      verificacion de cadena sobre el ledger real, DOS corridas, antes y despues."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - runtime/eventlog.py
    - scripts/
  out_of_scope:
    - "NO se toca el enlace de firma ni el registro de claves: es TASK-0423."
    - "NO se cambia el criterio de validez de la cadena. Esto es limpieza de una frontera que
      declara mas de lo que sabe decir, no un cambio de politica criptografica."
  risk: medium
  estimate: S
---

# TASK-0426 -- lo que la frontera promete y lo que sabe decir

    runtime/eventlog.py:32    EVENT_AUTH_UNVERIFIABLE_REASONS = {"unresolved_key", "missing_key", "key_unavailable"}
                              ^ unica aparicion de key_unavailable en todo el arbol

    runtime/eventlog.py:745   declared_unavailable_key_ids: set[str] | None = None,   <- se declara
    runtime/eventlog.py:1061  declared_unavailable_key_ids = attested_unavailable_...  <- se calcula
    runtime/eventlog.py:819   declared_unavailable_key_ids=declared,                   <- se pasa
    runtime/eventlog.py:1070  declared_unavailable_key_ids=...,                        <- se pasa
                              ...y el cuerpo de verify_event_auth no lo lee jamas.

Ninguno de los dos rompe nada hoy, y por eso llevan aqui sin que nadie los vea. Lo que hacen es
peor a plazo: **el codigo dice que distingue casos que no distingue**. Quien lea el conjunto de
motivos creera que la frontera separa "clave no disponible" de "clave irresoluble", y no lo hace;
quien lea la firma de `verify_event_auth` creera que el veredicto tiene en cuenta las claves
declaradas no disponibles, y no las tiene.
