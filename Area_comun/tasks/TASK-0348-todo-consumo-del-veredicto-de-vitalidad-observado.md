---
id: TASK-0348
title: Todo consumo del veredicto de vitalidad observado en su posicion, con unknown atado
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0348-todo-consumo-del-veredicto-de-vitalidad-observado.md
created: 2026-08-09
intake:
  type: fix
  goal: >
    TASK-0331 cerro la propiedad del PRODUCTOR: colapsar `Get-LeaseProcessState` o
    `Test-LeaseProcessMatches` a una constante enrojece un gate. Pero el veredicto de vitalidad tiene
    CONSUMIDORES que ningun gate observa, y dos de ellos fallan ABIERTO -- medido en el re-juicio r7
    con los siete gates en verde: (1) cegar el guardia de identidad de `Stop-LeaseProcessTree` mata
    un proceso VIVO AJENO; (2) observar solo `live`/`dead` deja que una sola palabra convierta el
    veto-ante-la-duda en paso libre, porque `unknown` no esta atado en el consumidor. Ademas absorbe
    el frente C3 -- la resolucion de la primera escritura alcanzable sobre `$LockPath` -- que hoy no
    reclama NINGUNA tarea.
  acceptance:
    - "AC1 (inventario de consumidores): se enumeran TODOS los puntos que consumen el veredicto de vitalidad, derivados del codigo y no de una lista escrita a mano, y se declara para cada uno si esta observado hoy."
    - "AC2 (criterio de observacion, por propiedad): para cada consumidor, sustituir al productor por una constante en la POSICION de ese consumidor debe enrojecer al menos un gate del verification_cmd. Es el mismo criterio que cerro 0331, aplicado al otro lado."
    - "AC3 (unknown atado en el consumidor): observar solo `live`/`dead` no basta. Se verifica por comportamiento que el tercer valor conserva su semantica de veto ante la duda y que ninguna reescritura de una rama lo convierte en paso libre."
    - "AC4 (Stop-LeaseProcessTree, fallo abierto y destructivo): se demuestra que cegar su guardia de identidad ya NO puede matar un proceso vivo ajeno, y se ata con negativo permanente. Es el unico defecto de esta tarea que destruye trabajo, no solo lo bloquea."
    - "AC5 (frente C3, con dueno): el contrato TASK-0284 resuelve la primera escritura ALCANZABLE sobre `$LockPath` sea cual sea la forma sintactica de la llamada, y se falsa moviendo esa escritura por encima de la sonda de residuo. Este frente quedo huerfano entre 0331 y 0341; aqui tiene dueno."
    - "AC6 (sin regresion): las siete vueltas de TASK-0331 siguen verdes, y el verification_cmd incluye los cinco lectores de CI que ya incorporo."
  verification_cmd:
    - "python scripts/test_exec_lease_harness.py"
    - "python examples/mailbox_retry_cases/run_mailbox_retry_cases.py"
    - "python scripts/check_falsification_contracts.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - scripts/harness/peer_mailbox_cron.ps1
    - scripts/test_exec_lease_harness.py
    - examples/mailbox_retry_cases/
    - Area_comun/protocol/FALSIFICATION_CONTRACTS.json
  out_of_scope:
    - "La ceguera del certificador ante la frontera muerta y ante el negativo huerfano: eso es TASK-0341 y NO se remite aqui."
    - "El alcance del guard de residuo, que es TASK-0337."
    - "Codigo de producto."
  risk: high
  estimate: L
---

# TASK-0348 -- el otro lado del veredicto de vitalidad

## Por que existe

TASK-0331 cerro la propiedad del **productor** tras siete vueltas: colapsar cualquiera de las dos
funciones del veredicto de vitalidad enrojece un gate. Ese criterio se cumple entero y esta medido.

Lo que queda es el **consumidor**, y son dos fallos ABIERTOS con los siete gates en verde:

    cegar el guardia de identidad de Stop-LeaseProcessTree   -> mata un proceso VIVO AJENO
    observar solo live/dead, con unknown sin atar            -> una palabra convierte el veto
                                                                ante la duda en paso libre

El primero **destruye trabajo**. Es el unico defecto de esta familia que no bloquea sino que rompe.

## El frente huerfano

El AC5 recoge C3 -- la resolucion de la primera escritura alcanzable sobre `$LockPath` -- que
quedo **sin dueno** porque el `out_of_scope` de TASK-0341 lo remitia a TASK-0331 y la nota de
TASK-0331 lo remitia a TASK-0341. Las dos particiones fueron mias y entre las dos abrieron un hueco.
Aqui tiene dueno, y los `out_of_scope` de las tres tareas quedan corregidos en el mismo paso.

## El criterio, que ya sabemos que funciona

El AC2 es **el mismo criterio que cerro 0331**, aplicado al otro lado: sustituir al productor por
una constante *en la posicion de cada consumidor* debe enrojecer un gate. No hace falta inventar
nada nuevo; hace falta aplicarlo donde no se aplico.
