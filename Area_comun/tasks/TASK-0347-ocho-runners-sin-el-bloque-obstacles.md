---
id: TASK-0347
title: El job validate no esta verde desde el 5 de junio -- una regla endurecida dejo obsoletas las fixtures de quince runners a la vez
status: ready
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0347-ocho-runners-sin-el-bloque-obstacles.md
created: 2026-08-09
intake:
  type: fix
  goal: >
    El job `validate` de GitHub Actions no sale verde desde el 2026-06-05 (run 27017313818, sha
    fb0d0f07), cuando ejecutaba DOS gates reales. Hoy declara 77 pasos `run:`. Como un paso rojo
    aborta el job, ningun runner cableado en estos dos meses ha sido observado nunca pasar en CI.
    Replicado el job entero a HEAD en un checkout limpio: 55 verdes, 17 rojos. QUINCE de esos
    diecisiete comparten una causa unica -- `c725e9bd fix(TASK-0259)` empezo a exigir el bloque
    `obstacles` en los turnos de entrega y las fixtures no lo producen. Siete lo dicen; ocho lo
    ocultan tras un `assert` sin mensaje, que reporta `"error": ""`. El encargo anterior de esta
    tarea enumeraba ocho y declaraba los otros de causas independientes: esa afirmacion queda
    FALSADA por medicion y es mia. Esta version no enumera: deriva la poblacion de la condicion
    que el motor evalua.
  acceptance:
    - "AC1 (la poblacion se deriva, no se enumera): existe un replicador local que LEE `.github/workflows/validate.yml` y ejecuta cada paso `run:` del job `validate` en orden, reportando exit code por paso. Nadie escribe la lista a mano: si manana se anade un paso al workflow, el replicador lo corre sin tocarlo. Declara que pasos no puede ejecutar en el host y por que."
    - "AC2 (el criterio de pertenencia, medido): se declara por medicion cuantos runners del job construyen turnos de entrega, cuantos de ellos satisfacen el contrato de `obstacles` y cuantos no, y se acredita la correlacion con el rojo. La particion se justifica por la condicion evaluada, no por el sintoma observado."
    - "AC3 (el fallo silencioso deja de serlo): ningun caso puede reportarse fallido con diagnostico vacio. Se acredita ejecutando un fallo real y mostrando que el mensaje identifica la causa. Un `assert` sin mensaje que reporta `error: \"\"` no es una puerta: oculto siete de estas quince causas al censo anterior."
    - "AC4 (los quince pasan, y se dice el saldo): el replicador de AC1 baja de 17 rojos a como mucho 2 (los dos de causa ajena, ver alcance). Se reporta el saldo PASS/FAIL antes y despues, paso a paso."
    - "AC5 (se arregla el lado correcto): si en alguno el defecto resulta ser de PRODUCCION y no del fixture, se declara, se para en ese, y se particiona. No se ajusta un fixture para tapar un fallo real."
    - "AC6 (contrato por la clase, verificado por mutacion): negativo permanente que muera si un fixture de entrega vuelve a omitir el bloque obligatorio, atado por PROPIEDAD -- no enumerando ficheros -- y verificado matando un mutante de PRODUCCION. Debe sobrevivir a cambio de coordenada, de orden y de formato."
    - "AC7 (cerrado en CI REAL): los pasos correspondientes salen success en un run real de GitHub Actions, citando la terna run_id + job + head_sha. Este AC esta hoy BLOQUEADO por la facturacion de Actions: la tarea puede entregarse y revisarse sin el, pero no cierra sin el."
  verification_cmd:
    - "python scripts/replay_validate_job.py --root ."
    - "python scripts/check_falsification_contracts.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - examples/
    - scripts/replay_validate_job.py
    - Area_comun/protocol/FALSIFICATION_CONTRACTS.json
  out_of_scope:
    - "El paso 43 (`event auth runtime override cases`), que falla por `unsupported keys: method` -- causa distinta, tarea aparte."
    - "El paso 50 (`runtime instantiation cases`), que falla por marcadores sin resolver en el port del motor de memoria -- causa distinta, tarea aparte."
    - "El mecanismo de cobertura del AC4 de TASK-0346, pendiente de decision del operador."
    - "Codigo de produccion, salvo que el AC5 revele un defecto real, y entonces se para y se declara."
  risk: medium
  estimate: L
---

# TASK-0347 -- quince verificadores, una sola raiz, y dos meses sin verde

## Lo que se midio

Ultimo verde de Actions: **2026-06-05, run 27017313818, sha fb0d0f07**. Su job `validate` tenia
**ocho pasos**, de los cuales dos eran gates reales:

    Validate repository dogfood instance
    Validate minimal example instance

El job de hoy tiene **77 pasos `run:`**. Los otros 75 se anadieron despues, y el job no ha vuelto a
salir verde ni una vez. Un paso rojo aborta el job, asi que **ninguno de esos 75 ha sido observado
pasar en CI**. Existen, estan cableados y los citamos en criterios de aceptacion. No estan
ejercitados.

Replica local del job a HEAD, checkout limpio, 72 pasos ejecutables: **55 OK / 17 FAIL**.

## La causa, derivada

`c725e9bd fix(TASK-0259): gate obstacles on objective friction` (2026-07-22) empezo a exigir:

    semantic: delivery turn is missing the obstacles block; use [] when there was no friction

De los runners del job que construyen turnos de entrega:

    26 construyen turnos
       4 mencionan obstacles  ->   0 en rojo
      22 no lo mencionan      ->  15 en rojo

Los 15 rojos caen dentro de los 22. Ninguno de los 4 falla. La correlacion no es una hipotesis:
es el recuento.

## Por que el censo anterior dijo "ocho, y el resto independientes"

Porque ocho de ellos fallan asi:

    {"case": "case_explicit_registry", "error": ""}

Un `assert` sin mensaje produce `AssertionError()` vacio, y el runner reporta `str(exc)` -- cadena
vacia. El sintoma parecia distinto, asi que se clasificaron como causas independientes. Medido caso
a caso, la linea que revienta es:

    assert validate_turn(turn_report("Builder"), root) == []
    -> ['semantic: delivery turn is missing the obstacles block; ...']

Es la misma causa, con el diagnostico apagado. De ahi el AC3: **una puerta que puede fallar sin
decir por que no es una puerta**, y su silencio ya nos costo una particion equivocada del censo.

## Por que la poblacion se deriva

El encargo anterior enumeraba ocho ficheros. El maker habria arreglado ocho y manana habria un
noveno -- es el patron que esta jornada ha demostrado repetidamente. Por eso AC1 no pide arreglar
una lista: pide un replicador que **lea el workflow** y ejecute lo que haya. La lista deja de
existir como artefacto editable a mano.
