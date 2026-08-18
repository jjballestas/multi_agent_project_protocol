---
task_id: TASK-0330
file: Area_comun/tasks/TASK-0330-contratos-declarados-que-ci-nunca-ejecuta.md
title: "23 de 37 contratos de falsacion tienen un runner que CI nunca ejecuta, y uno de esos runners lleva roto desde TASK-0316: la cobertura declarada no es cobertura verificada"
status: proposed
type: infra
owner: Codex
reviewer: Analista
priority: high
project: multi_agent_project_protocol
relates_to:
  - TASK-0316
  - TASK-0319
  - TASK-0321
  - TASK-0324
created_at: 2026-08-07
intake:
  type: fix
  goal: >
    El registro declara 37 contratos de falsacion sobre 8 runners (recuento 2026-08-07 09:20; eran 32
    al detectarlo, y los 5 anadidos esa noche SI estan cableados). CI ejecuta
    `check_falsification_contracts.py --inventory`, que verifica que cada contrato este DECLARADO y
    tenga fichero duenno -- pero NO ejecuta los runners. Y el workflow lista los runners uno a uno
    como pasos explicitos, asi que un runner que no aparece, no corre.
    Tres no aparecen: `run_mailbox_retry_cases.py` (16 contratos), `run_runtime_turn_obstacle_cases.py`
    (6) y `run_post_gate_obstacle_cases.py` (1). Total: **23 de 37 contratos, 47 fronteras, sin
    ejecutar en ningun gate automatizado**. Ningun hook, harness ni script local los invoca; solo
    aparecen corridos a mano en veredictos antiguos del Analista.
    Y no es teorico: `run_mailbox_retry_cases.py` esta **ROJO en clon limpio sobre HEAD**. Causa
    identificada: `52d0a380 fix(TASK-0316)` hizo `-CoordinatorId` obligatorio en
    `peer_mailbox_cron.ps1`, y la suite lo invoca **0 veces** con ese parametro. Sus fixtures
    quedaron obsoletos ese dia y nadie lo vio porque nada los corre.
    Los 16 contratos que esa suite sostiene son justamente los del mecanismo de reintento y
    diferimiento (`retry-terminal-defer`, `retry-preexec-untracked-exit-gate`, `retry-expired-claim`,
    `retry-dirty-forensics`...), el subsistema que TASK-0319, 0321 y 0324 estan modificando ahora
    mismo. Se esta trabajando sobre esa maquinaria con sus contratos sin verificar.
  acceptance:
    - "AC1 (falsacion previa): se reproduce en clon limpio que la suite de retry falla, y se declara la causa con el commit que la rompio. Se declara tambien, por medicion, que ningun gate automatizado ejecuta los tres runners."
    - "AC2 (la suite vuelve a verde por la razon correcta): se actualizan los fixtures para pasar -CoordinatorId, SIN relajar ninguna asercion ni marcar casos como skip. Si algun caso resulta obsoleto de verdad, se borra con razon escrita, no se silencia."
    - "AC3 (el agujero se cierra de raiz): los tres runners entran en CI. Y el mecanismo deja de depender de que alguien acuerde anadir el paso: check_falsification_contracts.py gana un modo que FALLA si un contrato declarado tiene un runner que el workflow no ejecuta. Un contrato que nadie corre pasa a ser un error, no una linea de inventario."
    - "AC4 (contrato sobre el propio mecanismo): negativo permanente que caiga si se declara un contrato cuyo runner no esta cableado, verificado por MUTACION -- anadir un contrato huerfano debe poner el gate en rojo."
    - "AC5 (recuento honesto): el handoff declara cuantos contratos y fronteras pasan de declarados a EJECUTADOS, y si al encender las tres suites aparece alguna otra asercion en rojo, se reporta antes de arreglarla."
    - "AC6 (sin regresion): validate, scan_encoding, neutralidad, contratos y las suites del repo exit 0 en clon limpio."
  verification_cmd: "python examples/mailbox_retry_cases/run_mailbox_retry_cases.py && python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py && python examples/runtime_turn_cases/run_post_gate_obstacle_cases.py && python scripts/check_falsification_contracts.py --root . && python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
    - examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py
    - examples/runtime_turn_cases/run_post_gate_obstacle_cases.py
    - scripts/check_falsification_contracts.py
    - scripts/test_falsification_contracts.py
    - .github/workflows/validate.yml
    - Area_comun/protocol/FALSIFICATION_CONTRACTS.json
  out_of_scope: >
    No se toca `peer_mailbox_cron.ps1` -- el harness esta bien y el parametro obligatorio es el fix
    correcto de TASK-0316; lo que esta obsoleto son los fixtures. No se tocan las tareas en vuelo
    (0320, 0322, 0324, 0325, 0326) ni sus contratos.
  risk: >
    Encender tres suites dormidas puede destapar mas rojos que el ya identificado. Ese es el punto
    de la tarea, pero conviene que el AC5 obligue a REPORTAR el inventario de rojos antes de
    arreglarlos, para no confundir "lo arregle todo" con "lo silencie todo". Riesgo secundario: si
    alguna suite es lenta, alarga CI; medir y declarar el coste.
  estimate: M
---

# TASK-0330 -- la cobertura declarada no es cobertura verificada

## Lo medido (2026-08-07, clon limpio en HEAD 0eb060ee)

    contratos declarados                             32  ->  37  (remedido 09:20)
    runners distintos                                 8  ->   8
    runners que CI ejecuta                            5  ->   5
    contratos cuyo runner NUNCA se ejecuta           23  ->  23   (47 fronteras)

El total subio porque las tareas de la noche (0324, 0325, 0326) anadieron contratos, y TODOS los
suyos SI estan cableados. El conjunto huerfano no se movio ni un contrato: son los mismos tres
suites historicos. El trabajo nuevo no agrava el problema, pero el problema no se corrige solo.

    run_mailbox_retry_cases.py         16 contratos   NO en CI   y ADEMAS rojo
    run_runtime_turn_obstacle_cases.py  6 contratos   NO en CI   verde
    run_post_gate_obstacle_cases.py     1 contrato    NO en CI   verde

## La cadena causal del rojo

`52d0a380 fix(TASK-0316): restore nested identity enforcement` puso
`[Parameter(Mandatory = $true)][string]$CoordinatorId` en `peer_mailbox_cron.ps1`. La suite de retry
invoca ese script en cada fixture y no le pasa `-CoordinatorId` **ni una sola vez**. Desde ese
commit la suite muere en el primer caso que lanza el harness de verdad.

Es exactamente el tipo de dano colateral que un gate existe para cazar, cometido por una tarea que
cerramos como done, invisible porque el gate que lo habria cazado no se ejecuta.

## Por que esto es mas grave que los otros residuales de la noche

Los demas hallazgos son guardas que fallan abiertas. Este es distinto: es una **medida de
cobertura que miente**. `--inventory` corre en CI y pasa, el registro dice 37 contratos, y el
numero se ha citado como evidencia de rigor en este mismo hilo. Casi dos tercios de ese numero no
prueban nada hoy.

Y el subconjunto afectado no es aleatorio: son los 16 contratos del mecanismo de reintento y
diferimiento, la maquinaria que 0319 y 0321 acaban de cambiar y que 0324 va a cambiar a
continuacion. Es el peor sitio posible para tener contratos dormidos.

## AC3 es lo que evita que vuelva a pasar

Anadir los tres pasos al workflow arregla el caso de hoy y deja el mecanismo igual de fragil: el
siguiente contrato que alguien declare sin cablear volvera a contarse como cobertura. Por eso el
gate tiene que fallar solo cuando un contrato declarado no tenga ejecucion, en vez de confiar en
que nadie se olvide.
