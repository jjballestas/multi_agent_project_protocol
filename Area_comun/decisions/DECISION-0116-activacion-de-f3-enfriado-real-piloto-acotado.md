---
decision_id: DECISION-0116
title: Activacion de F3 -- enfriado real en lote piloto ACOTADO, con stub-espejo obligatorio y rehidratacion probada
status: accepted
date: 2026-08-15
author: Arquitecto
approved_by: operador humano
supersedes: []
superseded_by: []
related:
  - SPEC-MEMORIA-HIBRIDA (REQ s.0.4, s.5.3, AC10)
  - TASK-0373
  - TASK-0389
  - Area_comun/protocol/MEMORY_HOT_COLD_RULES.json
---

# DECISION-0116 -- se activa F3, en piloto acotado

## Autorizacion

El operador humano pre-aprobo esta DECISION el 2026-08-14 condicionandola a que **F2 estuviera
acreditada**, y dio el GO explicito de activacion el 2026-08-15 tras el cierre de F2. Esta DECISION
es el instrumento que el REQ s.0.4 exige para mover historia canonica: **sin ella, ningun `git mv`
de artefactos esta autorizado.**

## Que se activa, y que NO

**SE ACTIVA:** el movimiento fisico hot->cold descrito en SPEC s.5.3, sobre un **LOTE PILOTO
ACOTADO**, ejecutado como tarea gobernada con claim.

**NO se activa:** el enfriado de la poblacion completa. La regla habilitada
`RULE-TASK-DONE-COLD-PROPOSAL` propone hoy **273 candidatos**; enfriar los 273 en la primera
ejecucion real convertiria el estreno del mecanismo en el cambio mas grande que ha hecho nunca. El
piloto se acota, se mide, y ensanchar es una decision posterior con la medicion delante.

## El lote piloto: acotado Y representativo

**Tope duro: 20 artefactos.**

Y la parte que importa mas que el numero -- **el lote DEBE ejercitar el camino peligroso**, no el
comodo. Obligatorio que incluya:

1. Al menos **una tarea referenciada por `file`** en el indice fusionado.
2. Al menos **una tarea `done` con `deliverables`** (hoy hay 92 archivadas con ellos).
3. Al menos **una tarea `id > TASK-0238`** (con intake, stub que lo conserva) **y una `id <= 0238`**
   (sin intake, stub sin el) -- las dos caras de la frontera que cerro F2.

Un piloto que solo enfrie artefactos sin punteros no prueba nada: la REGLA DE ORO anti-B1 existe
precisamente para los que si los tienen.

## Condiciones de ejecucion (vinculantes)

1. **Stub-espejo obligatorio** en la RUTA ORIGINAL EXACTA para todo lo referenciado por `file` o
   `deliverables`, con `status` espejo y puntero verificable (`cold_path` + `sha256` +
   `rehydration_command`). Es la regla de oro de s.5.3 y el bloqueante B1 de la review formal.
2. **Rehidratacion probada de ida y vuelta**: al menos un artefacto del lote se rehidrata y se
   comprueba que vuelve **byte a byte identico** al original (sha256), no "equivalente".
3. **`validate_collaboration_state.py` VERDE en CLON LIMPIO** tras el movimiento, y
   `check_memory_db_drift` verde. En clon limpio, no en el arbol caliente.
4. **AC10 medido**: baseline del HOT MAP REAL de s.2.1 **antes** y **despues**. Si el baseline previo
   no existe, se computa ANTES de mover -- una medicion posterior sin punto de partida no es un
   delta, es un numero.
5. **Reversibilidad probada antes de necesitarla**: se documenta y se EJECUTA el camino de vuelta
   (rehidratar el lote entero y dejar el arbol como estaba) en el clon de prueba, antes de aplicar
   sobre el arbol real.
6. Ejecucion como **tarea gobernada con claim** sobre rutas origen y destino, commit con pathspec
   explicito.

## Frontera de riesgo

Esta es la primera operacion del sistema que **borra informacion de donde estaba**. Todo lo anterior
-- F1, F2 -- anadia o derivaba. Por eso las condiciones 2 y 5 no son ceremonia: son la diferencia
entre un movimiento y una perdida.

Los residuales de TASK-0389 (la frontera de intake duplicada, el negativo vacio de `shlex.quote`) NO
bloquean el piloto -- hoy las dos copias coinciden -- pero **se cierran antes de ensanchar el lote**,
porque a partir de ahi la divergencia silenciosa empieza a mover ficheros de verdad.

## Ejecutor y revision

Arquitecto decide el lote; **Codex ejecuta; Analista revisa** con su gate adversarial habitual.
El done-flip no se ratifica sin veredicto del checker sobre clon limpio.

## Anexo

`Area_comun/protocol/MEMORY_HOT_COLD_RULES.json`, regla `RULE-TASK-DONE-COLD-PROPOSAL`
(`enabled: true`, `requires_stub: true`, `selector: status=done`, `window_count: 100`).
El `created_by_decision` de la regla queda actualizado a esta DECISION cuando el piloto cierre;
hasta entonces la regla sigue rigiendo solo la PROPUESTA en seco, que es lo que F2 acredito.
