---
task_id: TASK-0336
file: Area_comun/tasks/TASK-0336-gate-de-cableado-por-los-cuatro-factores.md
title: "El gate de cableado emite una certificacion afirmativa FALSA bajo nueve escapes: ata dos de los cuatro factores que hacen que el fallo de un runner llegue al veredicto del job"
status: in_progress
type: infra
owner: Codex
reviewer: Analista
priority: high
project: multi_agent_project_protocol
relates_to:
  - TASK-0330
  - TASK-0335
created_at: 2026-08-07
intake:
  type: fix
  goal: >
    Particion del punto 3 de la iteracion 2 de TASK-0330, escalado por el checker al agotar sus dos
    iteraciones. El nucleo de 0330 esta entregado y verificado en el CI real -- los tres runners
    dormidos ejecutan y su fallo rompe el job -- y esto es una propiedad DEL GATE sobre si mismo.
    La propiedad a atar no es del COMANDO sino de **la contribucion del paso al veredicto del job**, y
    se descompone en cuatro factores independientes:
    (a) el paso llega a ejecutarse -- `if:` de paso y de job, `needs:`, `on:` del workflow;
    (b) el runner se invoca de verdad -- no `echo`, no `--help`, no una ruta solo mencionada;
    (c) el fallo del runner cae al paso -- semantica del shell y adornos que traguen el codigo;
    (d) el fallo del paso cae al job -- `continue-on-error` en cualquiera de sus grafias.
    El gate de hoy cubre (b) parcialmente y (d) parcialmente. **(a) y (c) no los mira en absoluto.**
    Lo grave no es el hueco: es que el gate emite una CERTIFICACION AFIRMATIVA --
    `FALSIFICATION_EXECUTION runners=8/8 contracts=48/48` -- que es falsa bajo **nueve vectores**
    medidos por el checker. Un verde con numero es peor que un silencio.
  acceptance:
    - "AC1 (falsacion previa): se reproducen los nueve escapes del veredicto r2 de 0330 y se demuestra que el gate los certifica como cableados. Evidencia por comportamiento."
    - "AC2 (los cuatro factores): step_gates_runner ata (a), (b), (c) y (d). Para (c) la regla es INVOCACION UNICA Y SIN ADORNOS -- tras quitar comentarios y lineas en blanco queda exactamente una linea y esa linea invoca el runner sin adornos que traguen el codigo -- salvo que el shell efectivo garantice el aborto al primer fallo. Para (a), `if:` y `needs:` de paso y job. Para (d), continue-on-error truthy en cualquier grafia. El regex de (b) ancla por los dos extremos."
    - "AC3 (la regla debe ser CIERTA, no comoda): 'un comando por paso' no es necesario -- GitHub invoca `shell: bash` como `bash --noprofile --norc -eo pipefail {0}`, asi que un bloque de tres comandos en bash SI gatea -- ni suficiente, porque hay vectores de una sola linea que no gatean. Se declara la regla implementada y por que es cierta por los dos lados."
    - "AC4 (contrato falsable, no una foto de si mismo): los TRECE mutantes del veredicto r2 de 0330 pasan a ser boundaries de NEG-FALSIFICATION-RUNNER-WIRING. Un gate cuyo contrato declara exactamente los escapes que ya mueren no es falsable."
    - "AC5 (la certificacion, honesta): mientras existan escapes vivos, el gate no emite un recuento afirmativo de ejecucion, o lo emite acotado a lo que de verdad garantiza. Se declara que garantiza."
    - "AC6 (sin regresion): el cableado del job falsification-runners NO se toca -- un paso por runner con if: always() en los dos siguientes es la forma correcta, probada en CI real, y la regla de invocacion unica la acepta sin cambios. Gates del repo exit 0 en clon limpio."
  verification_cmd:
    - "python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory"
    - "python scripts/test_falsification_contracts.py"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_domain_neutrality.py --root ."
  scope_routes:
    - scripts/check_falsification_contracts.py
    - scripts/test_falsification_contracts.py
  out_of_scope: >
    No se toca `.github/workflows/validate.yml`: su cableado actual es correcto y esta probado en el
    CI real. No se reabre TASK-0330, que cierra con su nucleo. No entra el inventario de rojos de la
    suite de retry, que es TASK-0335.
  risk: medium
  estimate: M
---

# TASK-0336 -- atar la contribucion del paso al veredicto, no el comando

## De donde sale, y por que se particiona

Punto 3 de la iteracion 2 de TASK-0330. El checker agoto sus dos iteraciones y escalo. La decision
de particionar es del Arquitecto y sigue el mismo criterio que se aplico al sexto rojo de 0330: el
valor de aquella tarea era **que los contratos dormidos dejaran de ser invisibles**, y eso esta
entregado y verificado en el CI real. Esto es una propiedad distinta -- la solidez de la
certificacion que el propio gate emite -- y merece alcance propio con criterio de aceptacion propio.

## El error de encuadre que el checker corrigio

El Arquitecto pregunto: "basta con un comando por paso, o hay que razonar sobre el shell efectivo?"
Respuesta: **ninguna de las dos, y ambas comparten el mismo error** -- miran el COMANDO, y la
propiedad es de la CONTRIBUCION DEL PASO AL VEREDICTO DEL JOB.

    (a) el paso llega a ejecutarse        if: de paso, if: de job, needs:, on:
    (b) el runner se invoca de verdad     no echo, no --help, no ruta mencionada
    (c) el fallo del runner cae al paso   semantica del shell / adornos
    (d) el fallo del paso cae al job      continue-on-error en cualquier grafia

    gate de hoy:  (b) parcial, (d) parcial.  (a) y (c) NO se miran.

Ninguna cantidad de razonamiento sobre el shell arregla (a): **`if: false` no es una cuestion de
shell.**

## Remediacion 1 - contrato de shell efectivo y certificacion acotada

La excepcion multilinea acepta solo un shell bash efectivo (declarado en el paso, en
`defaults.run.shell` del job o del workflow, o implicito en un runner Unix) y un bloque cuya unica
linea no inerte es la invocacion directa. Las demas lineas admitidas son `echo` simples: no pueden
desactivar `errexit`, instalar un `trap ERR`, evaluar codigo ni ocultar el estado de salida. Esta
regla conserva el bloque bueno `echo / runner / echo` y rechaza por construccion `set +e`,
`set +o errexit`, `trap`, `source`, `eval`, funciones y operadores de control.

La salida ya no afirma ejecucion garantizada. `FALSIFICATION_STATIC_WIRING` certifica solo las
claves de trigger requeridas, condiciones de job/paso, invocacion directa, propagacion al paso y
propagacion al job. Declara tres residuales fuera de esa afirmacion: filtros internos de triggers,
`working-directory` y la resolucion de escalares YAML 1.1. El `needs` defensivo a nivel de paso se
mantiene como guarda inerte conocida.

## La condicion dura heredada

Mientras los nueve escapes sigan vivos, **`FALSIFICATION_EXECUTION runners=8/8 contracts=48/48` no
se cita como prueba de ejecucion** en ningun handoff ni reporte. Es la misma disciplina que se
aplico al "47" y que el maker respeto en el AC5 de 0330.
