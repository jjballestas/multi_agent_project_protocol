---
id: TASK-0341
title: El certificador de contratos es ciego a la frontera muerta y fragil al reformateo
status: proposed
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0341-el-certificador-de-contratos-es-ciego-a-la-frontera-muerta.md
created: 2026-08-08
intake:
  type: fix
  goal: >
    Medido por el checker en el juicio del borrador DECISION-0105. `check_falsification_contracts.py`
    decide si una frontera declarada existe con `boundary not in source`, es decir un
    `assert <literal> in source`. Consecuencia doble y simetrica: (a) una frontera presente byte a
    byte pero INALCANZABLE -- envuelta en `if False:` -- se certifica como declarada, cableada y
    verde, con el paso de CI en exit 0 y el inventario en 58/58 missing=0; (b) un simple salto de
    linea PEP8 sobre esa misma asercion, de semantica identica y con el test en exit 0, pone el
    certificador en exit 1. El gate es a la vez ciego a la frontera muerta y fragil al reformateo.
    Re-medido en el re-juicio del 2026-08-09: la inalcanzabilidad NO es una forma, es una FAMILIA de
    al menos seis (`if False:`, `return` antes del cuerpo, `@unittest.skip`, `raise SkipTest`, guarda
    por variable de entorno, `while False:`), y las SEIS dejan certificador, guardian y runner en
    exit 0 con las fronteras presentes byte a byte. Dos de ellas son peores: el runner ya reporta
    `skipped=1` y nadie lo consume. Por eso el criterio de esta tarea no es detectar formas.
  acceptance:
    - "AC1 (falsacion previa, las dos direcciones): se reproduce que envolver una frontera declarada en `if False:` deja el certificador y el paso de CI en exit 0 con missing=0, y que un salto de linea PEP8 sobre la misma asercion lo pone en exit 1 con el test en verde. Evidencia por comportamiento."
    - "AC2 (el criterio es POR PROPIEDAD, no por forma): el certificador enrojece cuando una frontera declarada NO SE EJECUTO durante la corrida del runner que su contrato declara como `exercised_by`. El predicado es la ejecucion, no la sintaxis: no se detectan formas, se observa si la linea corrio. Se verifica ejecutando mutantes, NO comprobando que se anadio una comprobacion."
    - "AC2b (los seis vectores, declarados NO exhaustivos): U1 `if False:`, U2 `return` antes del cuerpo, U3 `@unittest.skip`, U4 `raise SkipTest`, U5 guarda por variable de entorno, U6 `while False:` deben poner el certificador en ROJO -- las seis. Se declaran vectores obligatorios y NO exhaustivos: si el criterio necesita crecer para cubrir un U7, es que se implemento una enumeracion y el AC2 no esta cumplido."
    - "AC3 (deja de ser fragil al formato): un cambio de formato que preserve la semantica de la asercion -- saltos de linea, espaciado, parentesis -- no puede poner rojo al certificador. Se falsa con al menos tres reformateos distintos."
    - "AC4 (el criterio no vuelve a ser una subcadena): la decision de si una frontera esta viva no puede apoyarse en `<literal> in source` ni en ninguna otra inspeccion del TEXTO. Se declara el criterio elegido y se acredita que sobrevive a cambios de coordenada, de orden y de formato."
    - "AC4b (sin falso rojo en el baseline): U0 -- el arbol real, sin mutar -- debe seguir en VERDE, y ninguna frontera legitima viva puede marcarse. Un criterio que enrojece con todo no distingue nada."
    - "AC4c (el fallo dice cual): cuando el certificador enrojece, su salida identifica QUE frontera no se ejercio y de que contrato. Un gate que falla con diagnostico vacio no es un gate: esta misma jornada un `assert` sin mensaje hizo que siete fallos de la misma causa se clasificaran como independientes."
    - "AC5 (contrato): negativo permanente que muera si el certificador vuelve a aceptar una frontera inalcanzable, verificado por MUTACION. Redactado como negativo por COMPORTAMIENTO, nunca como afirmacion de que la comprobacion existe."
    - "AC6 (sin regresion y sin falsos rojos): el inventario completo sigue verde sobre el arbol real, y ninguna de las fronteras legitimas vivas pasa a marcarse. Se declara el recuento antes y despues."
  verification_cmd:
    - "python scripts/check_falsification_contracts.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - scripts/check_falsification_contracts.py
    - Area_comun/protocol/FALSIFICATION_CONTRACTS.json
    - examples/
  out_of_scope:
    - "El crash del validador por dependencia ausente (TASK-0340)."
    - "El contrato de subcadenas de run_mailbox_retry_cases.py y la resolucion de la primera escritura alcanzable sobre $LockPath (frente C3): su dueno es TASK-0348. Esta linea corrige una remision mutua con TASK-0331 que dejo C3 huerfano."
    - "Codigo de producto."
  risk: high
  estimate: M
---

# TASK-0341 -- el certificador certifica fronteras que no asiertan nada

## Lo medido por el checker

Dejo las dos fronteras declaradas de `NEG-NEUTRALITY-NESTED-IDENTITY` presentes **byte a byte** y
las hizo inalcanzables con `if False:`. Resultado:

    paso de CI verbatim (validate.yml:45-49, los tres comandos)   exit 0
    inventario                      permanent_negatives=58 declared=58 missing=0
    guardian                        "OK: guardian rejects relaxed boundaries"

Un negativo permanente que **no asierta nada** queda certificado como declarado, cableado y verde.

En sentido contrario, un salto de linea PEP8 sobre esa misma asercion -- semantica identica, test en
exit 0 -- pone el certificador en **exit 1**.

## Por que importa mas de lo que parece

Este certificador es el mecanismo del que depende la regla R2 del borrador DECISION-0105
("todo contrato declarado debe ser ejecutado Y exigido"). El checker lo resume asi: **"declarado,
ejecutado, exigido" no implica ASERTADO**. Falta la cuarta palabra -- *ejercido* -- y su predicado.

Y el criterio que usa, `boundary not in source`, es exactamente el `assert <literal> in source` que
el propio borrador cataloga como anti-patron. Es la tercera aparicion del mismo defecto **dentro del
artefacto que existe para impedirlo**.

## El predicado, medido (tabla del re-juicio del 2026-08-09)

En las siete variantes las dos fronteras declaradas siguen presentes byte a byte dentro de la
funcion que el contrato declara como `exercised_by`.

| Variante | Forma | Presentes | Ejecutadas | Criterio por forma (`if False:`) | Criterio por propiedad |
|---|---|---|---|---|---|
| U0 | baseline | SI | SI | -- | EJERCIDA (verde) |
| U1 | `if False:` | SI | NO | detecta | NO EJERCIDA (rojo) |
| U2 | `return` antes del cuerpo | SI | NO | no detecta | NO EJERCIDA (rojo) |
| U3 | `@unittest.skip` | SI | NO | no detecta | NO EJERCIDA (rojo) |
| U4 | `raise SkipTest` | SI | NO | no detecta | NO EJERCIDA (rojo) |
| U5 | guarda por variable de entorno | SI | NO | no detecta | NO EJERCIDA (rojo) |
| U6 | `while False:` | SI | NO | no detecta | NO EJERCIDA (rojo) |

Uno de seis frente a siete de siete. El criterio cabe en un trazador de lineas o en `coverage` con
el runner ya cableado: no es caro, es distinto.

**U3 y U4 son las peores**, y niegan la version anterior de este contrato: el runner **ya** reporta
`skipped=1`. La informacion existe y nadie la consume. El predicado tiene que nombrar al
**consumidor**, no al emisor.

## Nota de redaccion, que viene del checker y la hago mia

El AC2 y el AC5 estan escritos a proposito como **comportamiento observable**, no como existencia de
codigo. "Se anadio la comprobacion" no cierra esta tarea; que el certificador **enrojezca** ante un
`if False:` alrededor de una frontera declarada, si.
