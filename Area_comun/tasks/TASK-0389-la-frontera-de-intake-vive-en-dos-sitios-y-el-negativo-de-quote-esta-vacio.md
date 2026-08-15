---
id: TASK-0389
title: La frontera de intake vive en dos sitios y ninguna puerta ve que divergan; y el negativo de shlex.quote esta vacio
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0389-la-frontera-de-intake-vive-en-dos-sitios-y-el-negativo-de-quote-esta-vacio.md
created: 2026-08-15
reviewer: Analista
intake:
  type: fix
  goal: >
    Condicion de cierre de TASK-0373 (F2), puesta por el checker y aceptada por el Arquitecto:
    los dos residuales salen a tarea propia ANTES de que F3 arranque. **Residual 1, la frontera
    duplicada:** `Area_comun/protocol/INTAKE_GATE.json` declara `"start_task_id": "TASK-0238"` como
    fuente atestada, y `scripts/memory/build_memory_db.py` lleva el mismo umbral CABLEADO como
    literal (`int(match.group(1)) > 238`). El validador DERIVA la frontera del fichero de politica;
    el renderizador de stubs la LLEVA a mano. Medido por el checker: moviendo `start_task_id` de
    `TASK-0238` a `TASK-0400`, las CINCO puertas siguen verdes -- validate, suite F2, drift, encoding
    y neutralidad. **Ninguna se entera.** A partir de esa divergencia el stub exigiria intake donde
    el validador ya no lo pide, o dejaria de exigirlo donde si, y cada componente seria coherente
    consigo mismo mientras el conjunto miente. **Residual 2, el negativo vacio:** `shlex.quote` esta
    en produccion dentro de `rehydration_command`, pero mutarlo a la identidad
    (`shlex.quote(requested_by) -> requested_by`) deja la suite en exit 0: la propiedad esta escrita
    y no esta protegida. Ninguno de los dos es defecto de comportamiento HOY -- las dos copias
    coinciden y el quoting funciona -- pero los dos son huecos de PROTECCION, y su coste aparece
    justo cuando alguien toque lo que hoy nadie toca.
  acceptance:
    - "AC1 (una sola fuente para la frontera): el umbral de intake se DERIVA de
      `Area_comun/protocol/INTAKE_GATE.json` en todo consumidor, o -- si se decide mantener copias --
      existe una puerta que ENROJECE cuando divergen. Se acredita reproduciendo el experimento del
      checker: mover `start_task_id` a otro valor y comprobar por exit code que algo se entera. Hoy
      las cinco puertas siguen verdes; despues, al menos una no."
    - "AC2 (prueba de que RECHAZA): el caso negativo -- politica movida, consumidor sin actualizar --
      se ejecuta y sale distinto de cero, con la salida nombrando las dos coordenadas que discrepan.
      Un control que nunca ha dicho que no en esta configuracion no esta demostrado."
    - "AC3 (el quoting queda protegido): mutar `shlex.quote(requested_by)` a `requested_by` pone la
      suite en exit 1. Se acredita con el par -- mutante rojo, control verde -- no con la afirmacion
      de que la llamada existe."
    - "AC4 (no se mueve el comportamiento): tras el cambio, `--propose-cold` sigue dando los mismos
      273 candidatos y los 273 stubs siguen dejando `validate_collaboration_state.py` en exit 0.
      Medido, no afirmado: esta tarea es de proteccion, y si mueve una clasificacion esta mal."
  verification_cmd:
    - "python scripts/memory/test_memory_db.py"
    - "python scripts/memory/check_memory_db_drift.py --root . --fast"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - scripts/memory/build_memory_db.py
    - scripts/memory/test_memory_db.py
  out_of_scope:
    - "Cambiar el VALOR de la frontera. Esta tarea la unifica o la vigila; moverla es otra decision."
    - "TASK-0388 (exenciones del gate de neutralidad ancladas por numero de linea): es la hermana --
      alli el ancla es una coordenada, aqui es una copia -- pero son ficheros y entregas distintas."
  risk: medium
  estimate: S
---

# TASK-0389 -- la misma frontera escrita dos veces

## Lo medido por el checker

    D1  Area_comun/protocol/INTAKE_GATE.json:  start_task_id: TASK-0238 -> TASK-0400
        validate=0   suite F2=0   drift=0   encoding=0   neutralidad=0     las CINCO verdes

    D2  scripts/memory/build_memory_db.py:     shlex.quote(requested_by) -> requested_by
        suite -k f2 = 0                                                    SOBREVIVE

## Por que sale a tarea y no bloqueo el cierre de F2

Porque ninguno de los dos es un defecto de conducta hoy: las dos copias de la frontera dicen `238`,
el quoting funciona, y los 273 stubs aplicados dejan el estado canonico en exit 0. Son huecos de
**proteccion**: el dano no existe hasta que alguien toque lo que hoy nadie toca.

Pero se registran **antes de que F3 arranque** -- condicion del checker, aceptada -- porque F3 es
justamente quien empezara a mover artefactos de verdad, y es entonces cuando una frontera que
discrepa en silencio deja de ser latente.
