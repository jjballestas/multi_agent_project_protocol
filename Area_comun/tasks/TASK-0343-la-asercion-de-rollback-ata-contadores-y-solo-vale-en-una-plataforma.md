---
id: TASK-0343
title: La asercion de rollback ata contadores literales y solo se cumple en una plataforma
status: in_progress
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0343-la-asercion-de-rollback-ata-contadores-y-solo-vale-en-una-plataforma.md
created: 2026-08-08
intake:
  type: fix
  goal: >
    `examples/mailbox_retry_cases/run_mailbox_retry_cases.py:1638` afirma
    `"ROLLBACK_LEDGER_PRESERVED seq_before=0 seq_after=3 proof=disk" in log`: una subcadena literal
    que incluye DOS CONTADORES y un modo de prueba concreto. Pasa en local (Windows) y falla en el
    job `falsification-runners` de CI (windows-latest con pwsh) con AssertionError. Estaba
    enmascarada tras la asercion de la linea 342, que TASK-0331 acaba de arreglar; al pasar aquella,
    esta se alcanza y cae. Primero hay que MEDIR por que difiere, y despues atar la propiedad -- que
    el ledger se preserve a traves del rollback -- en vez de un literal con numeros dentro.
  acceptance:
    - "AC1 (diagnostico ANTES del arreglo): se mide y declara POR QUE la linea difiere entre el entorno local y el de CI -- que valores toman realmente seq_before, seq_after y proof en cada uno, y que los produce. No se toca la asercion antes de tener esa medicion escrita."
    - "AC2 (atar la propiedad): la asercion pasa a comprobar que el ledger se PRESERVA a traves del rollback, sin depender de valores concretos de contador ni del modo de prueba, salvo que se demuestre que esos valores son parte de la propiedad y entonces se declara por que."
    - "AC3 (sigue cayendo por la razon correcta): se falsa en las dos direcciones -- que el ledger NO se preserve, y que se preserve por un camino distinto del declarado -- y se comprueba que la asercion muere en ambas."
    - "AC4 (barrido del resto del runner): se inventaria el fichero entero buscando otras aserciones atadas a literales con contadores o rutas, y se declara cuales quedan. Este runner ya nos ha mordido cuatro veces por la misma forma."
    - "AC5 (cerrado en CI REAL): el paso `Execute mailbox retry falsification runner` sale success en un run real de GitHub Actions, citando su id. Evidencia local no cierra esta tarea: en local ya pasa hoy."
    - "AC6 (sin regresion): el runner completo exit 0, y los gates del repo exit 0 en clon limpio."
  verification_cmd:
    - "python examples/mailbox_retry_cases/run_mailbox_retry_cases.py"
    - "python scripts/check_falsification_contracts.py --root ."
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
    - Area_comun/protocol/FALSIFICATION_CONTRACTS.json
  out_of_scope:
    - "La exclusion de directorios del escaner de encoding (TASK-0342)."
    - "El contrato pre-gate de la linea 342, que ya arreglo TASK-0331."
    - "Cualquier cambio en el comportamiento de rollback de produccion: esta tarea toca la ASERCION, no lo aserido. Si la medicion del AC1 revela un defecto real de produccion, se declara y se particiona."
    - "Codigo de producto."
  risk: medium
  estimate: M
---

# TASK-0343 -- una asercion con contadores dentro

## Lo medido

CI, run 31266113929, job `falsification-runners` sobre windows-latest con pwsh:

    File "...\run_mailbox_retry_cases.py", line 1638, in main
        assert "ROLLBACK_LEDGER_PRESERVED seq_before=0 seq_after=3 proof=disk" in log
    AssertionError

En local el mismo runner sale **exit 0**. Verificado por mi a las 17:0x sobre el arbol vivo.

## Lo que hay que resistir

La reparacion barata es cambiar los numeros hasta que cuadren en las dos plataformas. **Eso es
moldear la asercion al resultado**, y ademas no cierra nada: la proxima diferencia de entorno
vuelve a romperla.

Por eso el AC1 exige la medicion ESCRITA antes de tocar la linea. Quiero saber que valores toma de
verdad cada campo en cada entorno y que los produce, no un literal que pase en ambos.

## La cuarta vez

Este runner ya nos ha mordido cuatro veces por la misma forma -- aserciones atadas a subcadenas
literales que un cambio legitimo rompe: TASK-0316, TASK-0319, TASK-0321 y el contrato de la linea
342 que acaba de arreglar TASK-0331. De ahi el AC4: no basta con arreglar esta; quiero el inventario
de las que quedan, declarado aunque no se toquen.

## Nota sobre el alcance

Esta tarea toca la **asercion**, no lo aserido. Si la medicion del AC1 revela que la diferencia
viene de un comportamiento real distinto del rollback entre plataformas, **eso es un defecto de
produccion**: se declara, se para, y lo particiono. No se arregla dentro de aqui.

## Remediacion autorizada -- R1 / mp2 (2026-08-10)

La asercion de preservacion de `main()` queda exigida por el negativo permanente existente. El
criterio parsea la produccion con AST y busca la llamada a `ledger_preservation_holds` dentro del
test de una asercion de `main`; no depende de numero de linea, orden de las definiciones ni formato
del fuente, y no agrega razones o formas a una lista.

El propio run deriva y publica el saldo estructural:

    TASK0343_MAIN_ASSERTION baseline=1 coordinate=1 order=1 format=1 deleted=0

El mutante mp2 se deriva del fuente de produccion y elimina el nodo `Assert` completo. Sobre ese
fichero mutado, el runner sale 1 en el negativo permanente con este saldo real:

    AssertionError: {'baseline': False, 'coordinate': False, 'order': False,
                     'format': False, 'deleted': False}
    MP2_RUNNER_EXIT=1

El baseline completo conserva exit 0 y emite el saldo anterior seguido de:

    mailbox retry cases: PASS (proof-only rollback -> conservative signed/ambiguous preservation)

El inventario permanece derivado y completo: `permanent_negatives=71 declared=71 missing=0`.

El commit exacto `4cfd1b03` repite runner, inventario, colaboracion, encoding, neutralidad,
compilacion, drift y diff en worktree limpio con status vacio. El run real `31397288472` sobre el
head publicado `1d219ccd` no inicio ningun paso: la anotacion de `falsification-runners` declara
fallo de pagos recientes o limite de gasto. La evidencia actual de AC5 queda externamente pendiente;
no se presenta ese rojo de plataforma como fallo del codigo.
