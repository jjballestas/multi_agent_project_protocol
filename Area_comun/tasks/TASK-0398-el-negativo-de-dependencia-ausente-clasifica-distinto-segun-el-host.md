---
id: TASK-0398
title: El negativo de dependencia ausente clasifica distinto segun el host -- en Linux devuelve excepcion donde exige razon, y su propio comentario dice que eso era la regresion
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0398-el-negativo-de-dependencia-ausente-clasifica-distinto-segun-el-host.md
created: 2026-08-15
reviewer: Analista
intake:
  type: fix
  goal: >
    Medido por el Arquitecto el 2026-08-15 sobre el commit `c5ed73f2`, job `validate` (runner Linux
    propio):

        File "examples/actor_auth_ed25519_cases/run_actor_auth_ed25519_cases.py", line 334,
             in case_cryptography_dependency_contract
        assert shipped_error is None
        AssertionError

    El caso bloquea la importacion de `cryptography` y llama a `verify_actor_auth` esperando que el
    codigo enviado levante un `EventLogError` con la razon "actor_auth verification unavailable:
    cryptography package is required". El ayudante (`missing_dependency_result`, `:171-189`) clasifica
    en tres: razon esperada -> `(razon, None)`; CUALQUIER otra excepcion -> `(None, exc)`; nada ->
    `(None, None)`.

    Que `shipped_error` no sea `None` significa que salio por la rama del medio: el codigo enviado
    levanto una excepcion distinta de la contratada. Y el comentario que hay en esa misma rama dice
    exactamente para que existe: "The negative must classify the former UnboundLocalError." Es decir,
    este negativo se escribio para cazar una regresion concreta que ya ocurrio una vez.

    Hay dos lecturas posibles y NO se debe elegir por comodidad: (a) la regresion ha vuelto y el
    negativo esta haciendo su trabajo, o (b) el negativo depende del host -- en Linux el bloqueo de la
    importacion no reproduce las mismas condiciones y aflora otro error. La diferencia importa: (a) es
    un defecto de produccion en `runtime/eventlog.py` que viaja a cada adoptante, (b) es un
    verificador irreproducible en el sentido de DECISION-0115. La tarea empieza por AVERIGUAR CUAL, y
    la evidencia es la excepcion real, con su tipo y su mensaje.
  acceptance:
    - "AC1 (nombrar la excepcion antes de arreglar nada): capturar y reportar el tipo y el mensaje
      EXACTOS de la excepcion que hoy vuelve en `shipped_error` en el runner Linux. El `assert`
      desnudo de hoy no lo dice, y sin ese dato las dos lecturas del goal son indistinguibles."
    - "AC2 (decidir con la evidencia delante): declarar por escrito cual de las dos es, citando la
      excepcion de AC1. Si es defecto de produccion, se arregla `runtime/eventlog.py` y el negativo se
      queda como esta. Si es dependencia del host, se arregla el negativo para que reproduzca la
      ausencia de la dependencia igual en Linux y en Windows."
    - "AC3 (paridad entre hosts): el caso da el mismo veredicto en el runner Linux y en el Windows
      sobre el mismo commit. Es la propiedad que hoy falta, y se acredita con las dos corridas, no con
      una."
    - "AC4 (el negativo sigue cazando su regresion): tras el cambio, reintroducir el fallo que este
      negativo existe para cazar -- el que su comentario llama `UnboundLocalError` -- lo pone en exit
      1. Si el arreglo consiste en relajar la asercion hasta que pase, el AC no se da por cumplido."
    - "AC5 (fallo con diagnostico): el caso deja de fallar con un `assert` desnudo; al caer nombra
      que se esperaba y que vino. Es lo que ha hecho falta hoy para poder siquiera clasificar el
      fallo."
    - "AC6 (CI): el job `validate` deja de caer por esta causa sobre el commit de entrega, acreditado
      con el run de CI. El `.githooks/pre-commit: FAILED` del mismo job se verifica si cae por esta
      misma causa o por otra; si es otra, se reporta y NO se arrastra a esta tarea."
  verification_cmd:
    - "python examples/actor_auth_ed25519_cases/run_actor_auth_ed25519_cases.py"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - examples/actor_auth_ed25519_cases/
    - runtime/eventlog.py
    - scripts/
  out_of_scope: >
    NO se tocan las otras tres causas rojas del mismo run (TASK-0396, TASK-0397, TASK-0399). NO se
    relaja la asercion para que pase: si el codigo enviado levanta una excepcion distinta de la
    contratada, eso es el hallazgo, no el estorbo.
  risk: high
  estimate: M
---

# TASK-0398 -- el negativo de dependencia ausente clasifica distinto segun el host

## Evidencia

Run `31883703617`, job `validate`, commit `c5ed73f2`, runner Linux propio:

    examples/actor_auth_ed25519_cases/run_actor_auth_ed25519_cases.py:334
    in case_cryptography_dependency_contract
    assert shipped_error is None

El ayudante que produce ese valor (`:171-189`):

    try:
        builtins.__import__ = block_cryptography_imports
        verify(event, config(enforce=False, keyid="codex:v1"))
    except EventLogError as exc:
        return str(exc), None
    except BaseException as exc:  # The negative must classify the former UnboundLocalError.
        return None, exc
    finally:
        builtins.__import__ = ORIGINAL_IMPORT
    return None, None

## Lo que este caso tiene de instructivo

El comentario de la rama que hoy se activa dice que existe para clasificar una regresion concreta.
Puede estar cazandola de verdad. Empezar por el arreglo, y no por leer la excepcion, es exactamente la
forma de convertir un hallazgo en un estorbo.

-- Arquitecto, 2026-08-15
