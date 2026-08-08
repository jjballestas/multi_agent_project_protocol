---
id: TASK-0346
title: Treinta y cinco runners cableados en CI no estan en la puerta de aceptacion de ninguna tarea
status: ready
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0346-treinta-y-cinco-runners-de-CI-fuera-de-toda-puerta-de-aceptacion.md
created: 2026-08-08
intake:
  type: fix
  goal: >
    Medido el 2026-08-08: de 66 runners de `examples/` cableados en `.github/workflows/validate.yml`,
    **35 no aparecen en el `verification_cmd` de ninguna tarea**. Nadie los ejecuta al entregar, asi
    que envejecen en silencio hasta que CI llega a ellos. Con CI en rojo desde el 2026-08-02, ninguno
    ha corrido en seis dias. Dos ya se han encontrado rotos por esta via -- el de status de mailbox
    (TASK-0344) y el de propiedades de runtime, que falla AHORA en local y en CI porque produccion
    exige un bloque `obstacles` que su generador no produce. Hay que arreglar el roto conocido,
    MEDIR cuantos mas lo estan, y cerrar el hueco estructural.
  acceptance:
    - "AC1 (el roto conocido, diagnostico primero): se mide y declara por escrito si el fallo de `run_runtime_property_cases.py` -- 'delivery turn is missing the obstacles block' con expected_valid true -- es defecto de produccion o generador obsoleto, y QUE cambio y en QUE tarea lo dejo obsoleto. No se toca nada antes de esa conclusion."
    - "AC2 (el censo real): se ejecutan LOS 66 runners y se declara, uno a uno, cuales pasan y cuales fallan. Esto convierte una rotura desconocida en una lista medida. Es el entregable principal."
    - "AC3 (se arregla el roto de AC1 y se declaran los demas): los fallos que aparezcan en el censo NO se arreglan aqui salvo el de AC1; se declaran con su sintoma para que el Arquitecto los particione."
    - "AC4 (el hueco estructural): se propone -- sin implementarlo unilateralmente -- como se garantiza que un runner cableado en CI quede alcanzable desde alguna puerta de aceptacion, o declarado explicitamente como de nivel protocolo con dueno. La propuesta se razona; la eleccion es del Arquitecto."
    - "AC5 (contrato): negativo permanente que muera si se anade a CI un runner que no queda cubierto por el mecanismo elegido en AC4, verificado por MUTACION. Si AC4 no se resuelve en esta tarea, este AC se declara diferido con su motivo."
    - "AC6 (cerrado en CI REAL): el paso `Run runtime property invariant cases` sale success en un run real de Actions, citando su id."
  verification_cmd:
    - "python examples/runtime_property_cases/run_runtime_property_cases.py"
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/check_falsification_contracts.py --root ."
  scope_routes:
    - examples/runtime_property_cases/
    - runtime/turn_validate.py
    - Area_comun/protocol/FALSIFICATION_CONTRACTS.json
  out_of_scope:
    - "Arreglar los demas runners que el censo del AC2 revele rotos: se declaran y los particiona el Arquitecto."
    - "Implementar por tu cuenta el mecanismo del AC4: se propone y lo decide el Arquitecto."
    - "Codigo de producto."
  risk: high
  estimate: L
---

# TASK-0346 -- mas de la mitad de los verificadores no los ejecuta nadie al entregar

## Lo medido

    runners de examples/ cableados en validate.yml            66
    que NO aparecen en el verification_cmd de ninguna tarea    35

Y con CI en rojo desde el 2026-08-02, **ninguno de los 66 ha corrido en seis dias**.

## El roto conocido

`examples/runtime_property_cases/run_runtime_property_cases.py` -> **exit 1 en local y en CI**:

    errors: "semantic: delivery turn is missing the obstacles block; use [] when there was no friction"
    expected_valid: true
    error: "turn_validate returned unexpected validity"

El generador produce un parte de entrega que considera valido y `turn_validate` lo rechaza por
faltarle un bloque que produccion exige. Mismo patron que TASK-0344: produccion avanzo y el
generador se quedo atras.

## Por que el AC2 es el entregable principal

Hoy no sabemos cuantos de los 35 estan rotos. **El censo convierte una rotura desconocida en una
lista medida**, y eso vale mas que arreglar el que hoy nos molesta. Si salen ocho rotos, quiero los
ocho declarados con su sintoma, no ocho sorpresas repartidas por las proximas semanas.

## La relacion con TASK-0330

Es su tesis un nivel mas arriba. Alli eran 23 contratos declarados cuyo runner CI no ejecutaba;
aqui son 35 runners que CI si ejecuta y que **ningun maker corre al entregar**. En los dos casos, el
mecanismo existe y no actua sobre la decision de nadie hasta que es tarde.
