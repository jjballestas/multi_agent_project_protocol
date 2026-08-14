---
id: TASK-0380
title: La liveness de maker y checker es un watchdog que se puede ignorar, no un paso 0 del cold-start
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0380-liveness-de-maker-y-checker-como-paso-cero.md
created: 2026-08-14
reviewer: Analista
intake:
  type: fix
  goal: >
    Punto 2 de la DECISION del Operador del 2026-08-14. Hoy la vitalidad de los peones se vigila con
    watchdogs, y un watchdog NOTIFICA: la sesion que lo recibe puede seguir adelante sin consecuencia,
    y el propio Operador senala que esta sesion lo demuestra. La consecuencia grave no es perderse un
    aviso: es que sin checker vivo la separacion maker/checker deja de existir en la ENTREGA, y ese
    es justo el medio agujero que el Punto 1 (TASK-0378) NO cierra -- con claim obligatorio, un actor
    todavia puede auto-clamarse y commitear. La regla que se pide es de capacidad, no de aviso: sin
    checker vivo, una sesion puede disenar, investigar, preparar y pedir; **no puede entregar producto
    bajo una tarea**.
  acceptance:
    - "AC1 (paso 0, no watchdog): la comprobacion de vitalidad de maker y checker ocurre en el
      arranque, antes de que la sesion pueda entregar, y su resultado RESTRINGE lo que la sesion puede
      hacer. Un aviso que se pueda continuar no acredita: la diferencia entre las dos formas ES la
      tarea."
    - "AC2 (prueba de RECHAZO, criterio 2f): se acredita intentando commitear producto bajo una tarea
      SIN checker vivo y observando que muere, nombrando la causa y la salida. Un control que solo se
      ha visto pasar no esta demostrado."
    - "AC3 (lo permitido sigue permitido): sin checker vivo, la sesion sigue pudiendo disenar,
      investigar, preparar y pedir -- y commitear coordinacion con `Task-Id: none`. Se acredita con
      el PAR: lo prohibido muere, lo permitido pasa. Un cierre que paralice la coordinacion cambia un
      agujero por un bloqueo."
    - "AC4 (la vitalidad se mide por CONDUCTA, y el HARNESS ENVIA EL LECTOR): el criterio de vivo no
      es un pid ni un fichero de lease, sino una senal que solo puede producir un peon que responde.
      Se declara cual y por que. Y no basta con declararlo: el harness entrega **el lector** -- un
      `--health` o script minimo junto al cron -- que responde `alive | hung | exited-by-design` a
      partir de las senales autoritativas, de modo que ningun consumidor tenga que re-derivar el
      contrato. Se acredita con los TRES estados observados, no con dos. Aportacion del Arquitecto de
      la instancia NOVA, y su argumento es una medicion: los dos escribimos el watchdog mal, cada uno
      por su lado y con el MISMO error -- leer el mtime del `runs/*.err.log`, que en text-mode queda a
      0 bytes y nunca se refresca. Un contrato que se puede re-derivar se re-deriva mal."
    - "AC6 (el lector es la UNICA implementacion, no un gemelo): el `--health` del AC4 no reimplementa
      el parseo de la senal en paralelo al productor. Si el harness y el lector interpretan el
      heartbeat por separado, se pueden desviar y tendremos dos verdades -- la trampa de paridad de
      gemelos que esta instancia ya conoce. El watchdog CONSUME el lector; no lo imita."
    - "AC7 (la vida util del peon, escrita y no deducida): hoy la politica se infiere de la conducta.
      Medido: `IntervalSeconds=300` por `MaxNoCoordinatorRounds=15` = **75 minutos de silencio DEL
      COORDINADOR** y el peon sale con `No <Coordinator> response limit reached; exiting.`. O sea que
      la vida no esta atada a la sesion sino a que el coordinador RESPONDA. Eso se declara en el
      contrato del harness, porque de ahi se sigue que la salida por rondas vacias NO es una muerte:
      es la respuesta correcta, y solo necesita ser legible -- que es justo lo que da el
      `exited-by-design` del AC4."
    - "AC5 (cierra el medio agujero, y se dice): se declara explicitamente que este control es el que
      completa a TASK-0378 en la familia maker==checker, y se acredita el caso conjunto: actor que se
      auto-clama Y no tiene checker vivo -> la entrega muere."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory"
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - scripts/
    - .githooks/pre-commit
  out_of_scope:
    - "El claim obligatorio: es TASK-0378 y es su precondicion, no su sustituto."
    - "El tablero de estado que distingue pendiente de capacidad caida: es TASK-0381."
  risk: medium
  estimate: M
---

# TASK-0380 -- avisar no es impedir

## La distincion que es la tarea

    watchdog   notifica   ->  la sesion decide si le hace caso
    paso 0     restringe  ->  la sesion no puede entregar sin la condicion

El Operador lo dice sin rodeos: la notificacion se ignora sin consecuencia, y esta sesion lo
demuestra. Cambiar el umbral o el texto del aviso no arregla nada, porque el defecto no esta en el
aviso.

## Por que se coordina con F2/F3 y no sale hoy

No es por riesgo de esquema -- esta congelado y la memoria hibrida es solo-lectura sobre el canon.
Es porque este control **inserta logica en la misma secuencia de cold-start** que F2/F3 reescriben.
Publicarlo antes obligaria a tocarlo dos veces.

## Lo que cierra

TASK-0378 exige claim para commitear producto y para el incidente reportado, que tenia cero claims.
Pero deja medio abierta la familia: un actor puede auto-clamarse y commitear. **Esta tarea es la otra
mitad**, y el AC5 exige acreditar el caso conjunto en vez de suponer que dos controles parciales
suman uno completo.
