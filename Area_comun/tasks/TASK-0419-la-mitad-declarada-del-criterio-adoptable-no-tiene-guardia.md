---
id: TASK-0419
title: La mitad declarada del criterio adoptable se autocertifica -- y el ensanche estructural estrecho la raiz y .github
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0419-la-mitad-declarada-del-criterio-adoptable-no-tiene-guardia.md
created: 2026-08-18
reviewer: Analista
intake:
  type: infra
  goal: >
    Residuos RES-1 y RES-2 declarados por el checker al cerrar TASK-0394 r2. Van juntos porque son
    la misma frontera vista por sus dos lados, y el propio checker dijo que no se arreglan con
    codigo urgente sino con una DECISION DE ALCANCE.
    RES-2 -- el criterio del conjunto adoptable tiene DOS mitades: cuatro raices recursivas (que r2
    puso bajo control estructural) y **nueve globs de master declarados a mano, que no tienen
    guardia ninguno**. Medido por el checker: retirar `.github/workflows/validate.yml`,
    `profiles/PROFILE_TEMPLATE`, `Area_comun/protocol` o `AGENTS.template.md` de
    `ADOPTABLE_MASTER_FILES` deja los dos gemelos en **exit 0**. La mitad que el AC3 de 0394 dejo
    cubierta enrojece; esta se autocertifica.
    RES-1 -- **el ensanche tambien estrecho**. Dos celdas que en r1 el checker midio ROJAS hoy salen
    VERDES en los dos gemelos: `exportable.py` en la RAIZ del master, y `.github/scripts/gate.py`.
    Es la regla de la casa incumplida --al ensanchar un patron hay que medir lo ganado Y lo
    perdido-- y ocurrio dentro del arreglo que ensanchaba.
  acceptance:
    - "AC1 (la mitad declarada deja de autocertificarse): retirar CUALQUIERA de los globs de
      `ADOPTABLE_MASTER_FILES` debe ENROJECER los dos gemelos. Se acredita retirando al menos tres
      distintos, uno a uno, y comprobando exit 1 en `.py` y en `.ps1`. Hoy los cuatro medidos dan 0."
    - "AC2 (recuperar lo perdido): `exportable.py` en la raiz del master y `.github/scripts/gate.py`
      vuelven a enrojecer, como hacian en r1. Se acredita con las dos celdas exactas del checker,
      ejecutadas, no descritas."
    - "AC3 (no se re-estrecha por el otro lado): las celdas que r2 gano siguen ganadas. Censo
      diferencial antes/despues sobre el conjunto completo, sin perdidas."
    - "AC4 (el criterio, no la lista): si la solucion es declarar mas globs a mano, no cierra --
      seria la enumeracion que TASK-0394 AC2 prohibe. Debe declararse QUE hace adoptable a un master
      declarado, o dejar por escrito que no hay criterio derivable y por que."
  verification_cmd:
    - "python scripts/upgrade_instance.py --help"
    - "python scripts/test_upgrade_instance_contract.py"
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - scripts/upgrade_instance.py
    - scripts/upgrade_instance.ps1
    - scripts/test_upgrade_instance_contract.py
  out_of_scope:
    - "Por COMPORTAMIENTO: RES-3 (la lista negra espejada en contenido pero no en comportamiento --
      ContainsKey de PowerShell es insensible a mayusculas y el set de Python no) NO entra aqui: va
      a TASK-0410, que es la tarea de paridad de gemelos, para no crear un tercer dueno sobre los
      mismos ficheros."
    - "RES-4 no es defecto: es el precio del fail-loud y los dos gemelos coinciden."
  risk: medium
  estimate: M
---

# TASK-0419 -- la mitad que enrojece y la mitad que se autocertifica

## Origen

Residuos **RES-1** y **RES-2** del veredicto **OK-CLOSABLE de TASK-0394 r2**. La tarea cerro porque
su efecto esta acreditado por mutacion de produccion; estos dos residuos son lo que quedo declarado.

## Por que juntos y no en dos tareas

Son **la misma frontera por sus dos lados**: una mitad del criterio quedo bajo control estructural
y la otra no, y al ensanchar la primera se estrecho la cobertura de la segunda. Separarlos invita a
arreglar una mitad y dejar la otra, que es exactamente el estado que produjo este residuo.

## La trampa, dicha de antemano

**Declarar mas globs a mano satisface la letra y repite el defecto.** El AC2 de TASK-0394 existe
para prohibir esa salida. Si al medirlo resulta que no hay criterio derivable para la mitad
declarada, la respuesta correcta es **decirlo por escrito**, no simular uno.
