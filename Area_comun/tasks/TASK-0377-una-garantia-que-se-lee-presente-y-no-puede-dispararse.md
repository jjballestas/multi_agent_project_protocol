---
id: TASK-0377
title: Una garantia que se lee presente y no puede dispararse -- el casefold del estado de politica es inalcanzable bajo la politica viva
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0377-una-garantia-que-se-lee-presente-y-no-puede-dispararse.md
created: 2026-08-14
reviewer: Analista
intake:
  type: fix
  goal: >
    Residual R3 del veredicto r1 de TASK-0368, declarado por el checker como NO perteneciente a esa
    tarea. `decision_policy_state` aplica `.casefold()` al estado antes de compararlo, lo que se lee
    como la garantia de que `Superseded`, `SUPERSEDED` o `Rejected` se reconocen igual que su
    minuscula. Medido: es INALCANZABLE. Toda variante de mayusculas muere antes en el allowlist de
    metadata, que filtra el valor contra el conjunto de estados conocidos y descarta la clave. El
    `.casefold()` nunca ve una entrada que necesite normalizar. No es un fallo de comportamiento --
    hoy nada se clasifica mal por esto -- sino una garantia aparente: quien lee el codigo concluye
    que la comparacion es insensible a mayusculas, y no lo es donde importa.
  acceptance:
    - "AC1 (decidir cual de las dos, con razon declarada): o la normalizacion se mueve donde SI puede
      actuar -- antes del filtro que hoy la deja sin entradas -- o se retira y se declara que el
      contrato es sensible a mayusculas. Las dos son respuestas legitimas; lo que no lo es es dejar
      una linea que promete algo que no puede cumplir."
    - "AC2 (acreditado por conducta, no por lectura): se acredita con una decision cuyo `status`
      lleve mayusculas. Si se elige normalizar, tiene que clasificarse como su equivalente en
      minuscula; si se elige retirar, tiene que quedar declarado que se descarta y por que. En ambos
      casos el resultado se observa, no se argumenta."
    - "AC3 (el barrido de la clase): se reporta si hay MAS normalizaciones o validaciones que queden
      detras de un filtro que las deja sin entradas posibles. La busqueda se deriva de la propiedad
      `codigo defensivo colocado despues de la puerta que lo haria necesario`, no de esta linea."
  verification_cmd:
    - "python scripts/memory/test_memory_db.py"
    - "python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory"
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - scripts/memory/build_memory_db.py
    - scripts/memory/test_memory_db.py
  out_of_scope:
    - "El literal cableado de `agent_memory.is_current`: es TASK-0376."
    - "Las fronteras de vigencia de decisiones: TASK-0368, en remediacion."
  risk: low
  estimate: S
---

# TASK-0377 -- codigo defensivo detras de la puerta que lo haria falta

## El hallazgo

`decision_policy_state` normaliza con `.casefold()`. Parece cubrir `Superseded`, `SUPERSEDED`,
`Rejected`, `Proposed`. No cubre ninguno: el allowlist de metadata filtra el valor **antes**, contra
el conjunto de estados conocidos, y una variante con mayusculas no esta en el. La clave se descarta y
la normalizacion nunca recibe la entrada que justifica su existencia.

## Por que importa aunque hoy no rompa nada

Porque una garantia que no puede dispararse es peor que su ausencia: quien lee el codigo cuenta con
ella. Es la misma familia que llevamos toda la jornada persiguiendo -- una forma que se lee como una
propiedad y no la tiene --, solo que aqui el sintoma es benigno y el habito no.

El AC3 es el que da valor a la tarea: buscar la CLASE, que es *codigo defensivo colocado despues de
la puerta que lo haria necesario*. Si esta es la unica, se dice y se cierra barato.
