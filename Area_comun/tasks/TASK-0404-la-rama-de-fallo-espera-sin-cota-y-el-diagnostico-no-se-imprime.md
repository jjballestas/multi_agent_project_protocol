---
id: TASK-0404
title: La rama de fallo del fixture espera sin cota a los descendientes, y por esa via el diagnostico que TASK-0396 acaba de construir no llega a imprimirse nunca
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0404-la-rama-de-fallo-espera-sin-cota-y-el-diagnostico-no-se-imprime.md
created: 2026-08-16
reviewer: Analista
intake:
  type: fix
  goal: >
    Residual R1 del veredicto del Analista sobre TASK-0396, declarado no bloqueante y recomendado con
    PRIORIDAD. Sale como tarea propia por decision del Arquitecto.

    En la rama de fallo del fixture de arbol de procesos, `terminate()` mata solo la RAIZ. Los
    descendientes heredaron los handles de sus pipes, asi que `communicate()` **sin `timeout=`** se
    queda esperando a que mueran solos. Control de variable unica del Analista, mismo fallo en los dos
    brazos:

        descendientes de 60s -> la rama de fallo tarda 60.5s
        descendientes de  3s -> la rama de fallo tarda 10.4s   (deadline del caso: 10s)

    Hoy queda acotado en ~60s porque los scripts del fixture se autoterminan. **Esa cota es una
    propiedad del fixture actual, no del codigo.** Si un descendiente futuro no se autoterminara, la
    espera no tiene cota: el job muere por timeout del runner y **el diagnostico que el AC4 de
    TASK-0396 acaba de construir no se imprime jamas**.

    Por eso esto no es una optimizacion. TASK-0396 existio para que un fixture que no arranca lo DIGA
    en vez de callarse. Esta rama devuelve exactamente esa clase de fallo por la puerta de atras: el
    runner muere sin llegar a hablar, y el sintoma externo vuelve a ser un job muerto sin causa.
    Arreglo de una linea segun el propio veredicto.
  acceptance:
    - "AC1 (reproducir la cota primero): reproducir el par del Analista -- mismo fallo con
      descendientes largos y cortos -- y capturar los dos tiempos de la rama de fallo. Sin ese par no
      esta demostrado que el tiempo dependa de los descendientes y no del fallo."
    - "AC2 (la espera tiene cota): la rama de fallo termina en un tiempo acotado que NO depende de
      cuanto vivan los descendientes. Se acredita repitiendo el par de AC1 y mostrando que los dos
      brazos convergen."
    - "AC3 (el diagnostico SI se imprime): con la cota puesta, el mensaje que AC4 de TASK-0396
      construye -- el que nombra la causa de que el arbol no se levante -- aparece en la salida. Es la
      razon de ser de esta tarea: se acredita leyendo el texto en el log, no por exit code."
    - "AC4 (no se mata el caso feliz): el camino normal del fixture, con el arbol levantandose y el
      negativo cazando su mutante, sigue en el mismo veredicto que antes. Un timeout demasiado corto
      convierte un negativo sano en flaky, que es peor que el defecto que arregla."
  verification_cmd:
    - "python examples/mailbox_retry_cases/run_mailbox_retry_cases.py"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - examples/mailbox_retry_cases/
  out_of_scope: >
    NO se toca el techo del GPO (residual R3 del mismo veredicto): eso es la via de no materializar
    `.ps1`, va en tarea propia y no bloquea esta. NO se reabre TASK-0396, cerrada `done`. NO se toca
    el estimulo de TASK-0343 (TASK-0395, cerrada) ni la asercion de `mid-log ambiguity` (TASK-0401).
  risk: medium
  estimate: S
---

# TASK-0404 -- la rama de fallo espera sin cota, y el diagnostico no llega a imprimirse

## Procedencia

Residual **R1** del veredicto `Analista-TASK-0396-el-fixture-que-vuelve-a-tener-sujeto-verdict.md`.
Declarado no bloqueante para 0396 y recomendado con prioridad. El Analista pregunto si abrirlo aparte
o dejarlo en cola; el Arquitecto decide **tarea propia**, porque lo que protege es la garantia que
acabamos de instalar.

## Por que sale ahora y no espera

TASK-0396 se cerro para que un fixture sin sujeto **lo diga**. R1 es el camino por el que ese aviso
puede volver a no emitirse: el runner muere por timeout antes de hablar. Dejarlo en cola es aceptar
que la garantia recien puesta se evapore en silencio la primera vez que un descendiente no se
autotermine.

-- Arquitecto, 2026-08-16
