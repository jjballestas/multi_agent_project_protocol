---
id: TASK-0347
title: Ocho runners de CI fallan por la misma raiz -- sus fixtures de entrega no traen el bloque obstacles
status: ready
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0347-ocho-runners-sin-el-bloque-obstacles.md
created: 2026-08-09
intake:
  type: fix
  goal: >
    Del censo de TASK-0346, NUEVE de los diecisiete runners rotos comparten una sola causa: sus
    fixtures de entrega no incluyen el bloque `obstacles` que `turn_validate` empezo a exigir. El
    numero 18 (`runtime_property_cases`) ya se arreglo bajo el AC1 de 0346; quedan OCHO. Un cambio
    correcto de produccion dejo obsoletos ocho verificadores a la vez y nadie lo vio porque ninguno
    esta en la puerta de aceptacion de ninguna tarea. Se arreglan juntos por compartir raiz, no por
    comodidad.
  acceptance:
    - "AC1 (diagnostico comun declarado): se identifica y declara QUE cambio introdujo el requisito de `obstacles` y en que tarea, y se confirma por medicion que los ocho fallan por esa misma causa y no por causas distintas que se le parecen."
    - "AC2 (los ocho pasan): los ocho runners salen exit 0. Se listan uno a uno con su resultado."
    - "AC3 (se arregla el lado correcto): si en alguno el defecto resulta ser de PRODUCCION y no del fixture, se declara, se para en ese, y se particiona. No se ajusta un fixture para tapar un fallo real."
    - "AC4 (contrato por la clase, no por los ocho): negativo permanente que muera si un fixture de entrega vuelve a omitir el bloque obligatorio, atado por PROPIEDAD -- no enumerando los ocho ficheros -- y verificado por MUTACION."
    - "AC5 (cerrado en CI REAL): los pasos correspondientes salen success en un run real de GitHub Actions, citando su id."
    - "AC6 (sin regresion): el resto del censo no empeora; se declara el saldo PASS/FAIL antes y despues."
  verification_cmd:
    - "python examples/runtime_concurrency_cases/run_runtime_concurrency_cases.py"
    - "python examples/runtime_guardrail_cases/run_runtime_guardrail_cases.py"
    - "python scripts/check_falsification_contracts.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - examples/
    - Area_comun/protocol/FALSIFICATION_CONTRACTS.json
  out_of_scope:
    - "Los otros ocho fallos del censo, que son de causas independientes."
    - "El mecanismo de cobertura del AC4 de TASK-0346, pendiente de decision del operador."
    - "Codigo de produccion, salvo que el AC3 revele un defecto real, y entonces se para y se declara."
  risk: medium
  estimate: M
---

# TASK-0347 -- ocho verificadores, una sola raiz

## Los ocho

Del censo reproducido de TASK-0346 (49 PASS / 17 FAIL, verificado dos veces por el checker):

    19  runtime_concurrency_cases          24  runtime_protocol_materialize_cases
    20  runtime_guardrail_cases            29  runtime_protocol_enforce_cases
    30  runtime_protocol_genesis_ref_cases 42  runtime_eventlog_gate_cases
    52  runtime_budget_cases               63  runtime_real_adapter_cases

El numero 18 ya se arreglo bajo el AC1 de 0346.

## Por que juntos

Comparten **una sola causa**: produccion empezo a exigir un bloque que sus fixtures no producen.
Partirlos en ocho multiplicaria la revision sin anadir informacion, y arreglar uno solo dejaria la
clase abierta -- que es exactamente el patron que esta jornada ha demostrado ocho veces.

Por eso el AC4 pide el contrato **por la clase**: un negativo que muera si un fixture de entrega
vuelve a omitir el bloque obligatorio, sin enumerar los ocho ficheros. Si enumera, manana hay un
noveno.

## Por que existe esta tarea ahora

TASK-0340 no puede cerrar hasta que uno de estos fallos -- el numero 19 -- este contratado: el
criterio de AC6 que dicte exige que todo fallo restante del job este atribuido **por id a una tarea
CONTRATADA**. Aplace contratarlos esperando una decision de alcance del operador, y esa demora
bloqueo a 0340. La demora es mia.
