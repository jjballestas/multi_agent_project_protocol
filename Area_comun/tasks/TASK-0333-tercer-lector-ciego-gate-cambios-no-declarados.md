---
task_id: TASK-0333
file: Area_comun/tasks/TASK-0333-tercer-lector-ciego-gate-cambios-no-declarados.md
title: "Hay un TERCER lector de git status sin --untracked-files=all, y alimenta el gate que rechaza turnos con cambios no declarados: declarar un directorio esconde el subarbol entero"
status: ready
type: infra
owner: Codex
reviewer: Analista
priority: high
project: multi_agent_project_protocol
relates_to:
  - TASK-0326
  - TASK-0323
created_at: 2026-08-07
intake:
  type: fix
  goal: >
    Residual R1 del veredicto de TASK-0326, medido por el checker. TASK-0326 convergio los dos
    lectores conocidos; hay un TERCERO que sigue ciego: `runtime/orchestrator.py:680
    dirty_worktree_paths` interroga con `["git","status","--porcelain=v1","-z"]`, **sin**
    `--untracked-files=all`.
    No es un consumidor cualquiera: alimenta `unreported_dirty_paths`, que en
    `orchestrator.py:1033` **RECHAZA un turno cuando aparece un cambio no declarado**. Es una puerta
    de gobernanza, y se puede atravesar declarando un unico directorio.
    Falsacion medida por el checker:
    un turno crea `work/declared_note.md`, `work/hidden/backdoor.py` y `work/hidden/deep/more.py`, y
    declara `changed_paths = ["work/"]`. El orquestador ve `['work/']`; convergido veria las tres
    rutas. No-declarados marcados: **CERO**. El turno PASA, y quedan ocultos al gate
    `work/hidden/backdoor.py` y `work/hidden/deep/more.py`.
    La causa es la misma que 0326 cerro en los otros dos: sin la opcion, git colapsa el directorio
    sin rastrear en un unico registro, y `normalize_report_path("work/")` da `"work"`, que casa con
    el registro colapsado. Direccion ABIERTA.
  acceptance:
    - "AC1 (falsacion previa): se reproduce con git real que declarar un directorio esconde su subarbol del gate de cambios no declarados, y que el turno pasa. Evidencia por comportamiento con las rutas concretas."
    - "AC2 (el tercer lector converge): dirty_worktree_paths pasa a interrogar con el MISMO juego de opciones que los otros dos. Se declara en el handoff el inventario COMPLETO de lectores de git status del repo y las opciones de cada uno, para que no aparezca un cuarto."
    - "AC3 (lo que NO se toca, declarado): dirty_tracked_worktree_paths:689 usa --untracked-files=no A PROPOSITO y para su fin es correcto. Se deja intacto y se declara por que, para que un futuro barrido de convergencia no lo 'arregle' por simetria."
    - "AC4 (direccion del ensanche): ver mas ficheros hace que el gate RECHACE mas turnos. Se verifica que eso no rompe flujos legitimos -- en particular que un turno que declara correctamente sus rutas sigue pasando -- y se mide cuantos turnos del corpus real pasarian a rechazarse."
    - "AC5 (contrato POR COMPORTAMIENTO): negativo permanente que reproduzca el turno con subarbol oculto y exija que el gate lo RECHACE. Verificado por mutacion, incluida la forma de CODIGO MUERTO (opcion presente en el fuente pero inalcanzable), que es la que se escapo en TASK-0324. Cableado en CI."
    - "AC6 (sin regresion): suites del runtime y gates del repo exit 0 en clon limpio."
  verification_cmd:
    - "python scripts/test_exec_lease_harness.py"
    - "python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py"
    - "python scripts/check_falsification_contracts.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - runtime/orchestrator.py
    - examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py
    - Area_comun/protocol/FALSIFICATION_CONTRACTS.json
  out_of_scope: >
    No se toca `dirty_tracked_worktree_paths` (AC3). No se reabre TASK-0326, que cerro bien su
    alcance. No entra el caso del repo git EMBEBIDO: ninguna opcion de git status lo alcanza y va en
    su propia tarea.
  risk: medium
  estimate: M
---

# TASK-0333 -- el tercer lector deja pasar un subarbol por la puerta de gobernanza

## Por que esta separada de 0326 y por que es mas grave

0326 arreglo los dos lectores que deciden **a quien no matar** (barredor de zombis y guard de
residuo). Este decide **que turno se acepta**. El primero, al fallar, mata trabajo bueno -- molesto y
visible. Este, al fallar, **acepta trabajo no declarado** -- silencioso y exactamente lo contrario de
lo que el gate existe para impedir.

    turno declara:        ["work/"]
    orquestador ve:       ['work/']
    convergido veria:     ['work/declared_note.md','work/hidden/backdoor.py','work/hidden/deep/more.py']
    no-declarados:        []            <-- el turno PASA
    ocultos al gate:      work/hidden/backdoor.py, work/hidden/deep/more.py

## El AC2 es el que evita la cuarta vez

Esta es la TERCERA aparicion de la misma raiz: 0323 la encontro en el parseo, 0326 en las opciones de
dos lectores, y aqui esta en un tercero que nadie habia inventariado. Por eso el AC2 no pide arreglar
este lector: pide **el inventario completo de lectores de git status del repo con las opciones de
cada uno**. Arreglar el tercero y descubrir el cuarto dentro de dos semanas seria repetir el ciclo
por cuarta vez.

## Y el AC5 pide el mutante que ya se nos escapo una vez

El negativo tiene que morir tambien ante la forma de **codigo muerto** -- opcion presente en el
fuente pero inalcanzable -- porque es exactamente la que sobrevivio al contrato de TASK-0324 y la
que el contrato de 0326 si mata. Ya sabemos que esa forma existe y que un `assert linea in source`
no la ve.

## Riesgo declarado (medium)

El gate pasa a rechazar mas turnos. Si algun flujo declaraba rutas a nivel de directorio
confiando en el colapso, dejara de pasar -- y eso es el fix funcionando, pero hay que medirlo y
declararlo antes, no descubrirlo como ruido. Riesgo secundario: el runner de la suite de turnos
es uno de los que CI NO ejecuta hoy; si el contrato se cablea ahi sin mas, nacera dormido.
