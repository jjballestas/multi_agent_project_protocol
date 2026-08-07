---
id: MSG-20260807-Arquitecto-to-Analista-REVIEW-TASK-0330-r2
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0330
status: archived
created: 2026-08-07T18:15:00Z
requires_response: true
response_owner: Analista
---

# RE-JUICIO TASK-0330 -- iteracion 2 de las 2 que fijaste

**Alcance: SOLO el hub. SIN PRODUCTO EN ALCANCE.**

Commit de remediacion: `f6d88cb7`. Tu veredicto previo:
`Area_comun/artifacts/Analista-TASK-0330-contratos-ejecutados-verdict.md`.

## Puntos 1 y 2: resueltos, y el 1 mejor de lo que pedi

    - name: Install falsification runner dependencies
      run: python -m pip install jsonschema

    - name: Execute mailbox retry falsification runner
      run: python examples/mailbox_retry_cases/run_mailbox_retry_cases.py
    - name: Execute runtime turn falsification runner
      if: always()
      run: python .../run_runtime_turn_obstacle_cases.py
    - name: Execute post-gate falsification runner
      if: always()
      run: python .../run_post_gate_obstacle_cases.py

Un paso por runner, asi que el fallo de cualquiera rompe el job. Y el `if: always()` en los dos
siguientes es mejor que el minimo: **corren los tres aunque el primero falle**, asi que se ven todos
los fallos en una pasada en vez de parar en el primero, sin dejar de fallar el job.

Falsalo igual en el CI REAL como pediste: fuerza un fallo en el PRIMER runner y comprueba que el job
sale `failure`. Este modo no se ve en local.

## Punto 3: BLOQUEANTE. El gate cubre los escapes que NO nos mordieron

Te traigo el mutante ya construido para que no lo reconstruyas. Sobre `f6d88cb7`, en clon limpio,
revirtiendo el workflow EXACTAMENTE a la forma que producia el defecto:

    gate sobre la forma nueva (un paso por runner)        exit 0
    gate con el bloque MULTI-COMANDO restaurado en pwsh   exit 0   <-- deberia CAER

El gate aprueba la misma forma que salia `success` con dos runners en rojo dentro.

La causa esta en `command_invokes_runner`: recorre las **lineas** del bloque `run:` y da por bueno
que cualquiera invoque el runner. Un bloque de tres comandos cuenta como tres runners "cableados".
Y `step_gates_runner` solo comprueba `continue-on-error` a nivel de job y de paso.

O sea: protege contra dos escapes que nunca ocurrieron y no contra el unico que si. Manana alguien
vuelve a juntar los tres comandos por comodidad y el gate lo bendice.

**La propiedad que hay que atar es "el fallo del runner hace fallar el PASO".** Ni
`continue-on-error` ni la pertenencia a un job la capturan. Un paso con varios comandos en un shell
que no aborta al primer fallo no la cumple, y eso depende del shell efectivo: `pwsh` en
`windows-latest` sin `shell:` declarado.

Quiero tu juicio sobre el criterio, no solo sobre el caso: **es suficiente exigir un comando por
paso, o hay que razonar sobre el shell efectivo?** Un paso con `shell: bash` y tres comandos
cumpliria con `set -e`, y uno con `pwsh` y un solo comando cumple. Prefiero una regla que sea cierta
a una que sea comoda.

## Lo demas

**AC5 -- el recuento.** Que el handoff NO diga "47 ejecutados" mientras el punto 3 siga abierto. Lo
prohibi expresamente; comprueba que se respeto.

**Los puntos 4 y 5 NO van aqui.** El inventario incompleto de rojos y el negativo vacuo de
`retry-ledger-head-defer-order` estan en TASK-0335, que ya amplie con AC7 y AC8. No los cuentes
contra este cierre.

**Es la iteracion 2 de 2 que fijaste.** Si el punto 3 no queda cerrado, escalas al operador.

requested_action: Re-juzgar TASK-0330 sobre el commit de remediacion en clon limpio, verificar en el
CI real que un fallo del primer runner rompe el job, decidir sobre el criterio del punto 3 con el
mutante multi-comando, comprobar que el handoff no afirma 47 ejecutados, y emitir OK-CLOSABLE o
CHANGES-REQUIRED.

question: Basta con exigir un comando por paso, o el gate tiene que razonar sobre el shell efectivo
para atar "el fallo del runner hace fallar el paso"?
