---
id: TASK-0367
title: El nucleo neutral trae la identidad de esta instancia cableada como valor por defecto, y una instancia recien parida la hereda
status: ready
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0367-el-nucleo-neutral-trae-la-identidad-de-esta-instancia-cableada.md
created: 2026-08-12
intake:
  type: fix
  goal: >
    El paso 50 del job `validate` (`examples/runtime_instantiation_cases`) tiene DOS causas, no una.
    La primera -- el aborto por marcadores sin resolver -- la mata TASK-0350. Con esa muerta, el
    runner llega mas lejos y descubre la segunda: la instancia GENERADA no pasa el escaner de
    neutralidad porque el nucleo trae el nombre del arquitecto de ESTA instancia cableado como valor
    por defecto en cuatro sitios (`runtime/context.py:15` en DEFAULT_AGENT_ROLES, `runtime/router.py:438`
    como retorno de ultimo recurso, `scripts/prune_state.py:252` en el texto del centinela y `:442`
    como defecto al leer el config; el arnes de peones del tier runtime anade el suyo). No es un
    fallo introducido: TASK-0350 solo toco `scripts/new_instance.py` y el runner de casos, asi que
    los cuatro son anteriores y llevaban ocultos detras del primer aborto. Es la frontera dura de
    AGENTS.md s.4 medida por conducta: un equipo que instancia el protocolo hereda por defecto la
    identidad del equipo que lo escribio.
  acceptance:
    - "AC1 (la poblacion se deriva, no se enumera): el conjunto de sitios corregidos sale de correr
      el escaner de neutralidad sobre una instancia GENERADA, no de la lista de cuatro que este
      enunciado cita. Si el escaner encuentra mas, entran; si uno de los cuatro no aparece al medir,
      se declara por que. La lista de arriba es el sintoma observado, no el criterio."
    - "AC2 (defecto que no es identidad): cada sitio se resuelve dando al nucleo un valor por defecto
      que no nombra a ningun participante concreto, o haciendo que el valor venga del config de la
      instancia. Se declara para cada uno cual de las dos vias se eligio y por que. Sustituir un
      nombre propio por otro nombre propio no acredita."
    - "AC3 (el negativo discrimina): tras el cambio, inyectar la identidad de un participante concreto
      en el nucleo vuelve a poner rojo el escaner sobre la instancia generada. Se acredita
      inyectandola y mirando el exit code. Un cambio que ponga verde el caso y ademas deje pasar la
      identidad inyectada no acredita nada."
    - "AC4 (la instancia sigue naciendo operativa): la instancia generada conserva sus roles reales
      -- los que su propio `protocol.config.json` declara -- y sus flujos siguen funcionando. Se
      acredita con el runner de casos, no afirmando que no se rompio nada."
    - "AC5 (paso 50 verde, citado): `case_coordination_default_and_flag` y
      `case_runtime_tier_scaffolds_motor_gates_ci_off` pasan en checkout limpio, con la salida del
      runner antes y despues por exit code. Este es el AC que cierra el paso 50 de verdad: TASK-0350
      mato la primera causa, esta mata la segunda."
  verification_cmd:
    - "python examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py"
    - "python scripts/scan_domain_neutrality.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - runtime/context.py
    - runtime/router.py
    - scripts/prune_state.py
    - scripts/harness/peer_mailbox_cron.ps1
  out_of_scope:
    - "El aborto por marcadores sin resolver: es TASK-0350, la primera causa del mismo paso."
    - "Los quince rojos de causa `obstacles`: son TASK-0347, que declara el paso 50 fuera de su
      alcance precisamente por esto."
    - "Renombrar actores en la instancia VIVA de este repo: aqui el arquitecto se llama Claude por su
      propio config y eso es correcto. Lo que se corrige es el DEFECTO del nucleo, no la instancia."
  risk: medium
  estimate: S
---

# TASK-0367 -- la segunda causa del paso 50

## Como aparecio

TASK-0350 mato el aborto por marcadores. Al correr el runner con esa causa muerta, el paso 50 llega
mas lejos y falla en otro sitio:

    case_coordination_default_and_flag
      runtime/context.py:15: Claude
      runtime/router.py:438: Claude
      scripts/prune_state.py:252: Claude
      scripts/prune_state.py:442: Claude

    case_runtime_tier_scaffolds_motor_gates_ci_off
      (los cuatro anteriores) + scripts/harness/peer_mailbox_cron.ps1:553: Claude

Es el patron de la cascada: **una puerta que aborta pronto oculta lo que hay detras**. Mientras el
paso 50 moria en el chequeo de marcadores, estos cuatro no podian verse. No son nuevos y no los
introdujo TASK-0350 -- su diff toco `scripts/new_instance.py` y el runner de casos, nada mas.

## Por que no es de TASK-0347 ni de TASK-0350

TASK-0347 particiona los diecisiete rojos del job y **declara el paso 50 fuera de su alcance**,
asignandolo por nombre a TASK-0350. TASK-0350, a su vez, tiene una causa distinta y acotada. El
residuo no encajaba en ninguna de las dos: sin esta tarea se quedaba sin dueno, con las dos partes
senalandose la una a la otra. Ese es el modo exacto en que un rojo sobrevive meses.

## Lo que esta realmente en juego

No es un escaner quisquilloso. `DEFAULT_AGENT_ROLES` en el nucleo dice que el arquitecto por defecto
se llama Claude, y `router.py` lo devuelve como ultimo recurso cuando no encuentra a nadie. Un equipo
que instancie el protocolo hereda esa identidad sin pedirla. La frontera de AGENTS.md s.4 no la mide
el texto del contrato: la mide lo que sale de `new_instance.py`.
