---
id: TASK-0420
title: Vehiculo de review para TASK-0408 -- alcance por lo que la review ESCRIBE
status: ready
owner: Analista
type: research
file: Area_comun/tasks/TASK-0420-vehiculo-de-review-para-task-0408.md
created: 2026-08-18
reviewer: Arquitecto
intake:
  type: research
  goal: >
    Permitir que el juicio independiente de TASK-0408 se ejecute aunque el maker tenga claim
    activo sobre scripts/. Una review ruteada contra el task_id de la tarea auditada hereda sus
    scope_routes de CODIGO y queda bloqueada por el claim del maker. El 18-ago murieron TRES
    encargos del checker por active_external_claim con RETRY_EXHAUSTED outcome=defer_terminal
    (21:20:07, 21:20:09 y 23:27) sin haber ejecutado ni una sola vez, tras 21 diferimientos.
    Esta tarea declara como alcance lo que la review realmente ESCRIBE.
  acceptance:
    - "AC1: el veredicto sobre TASK-0408 (commit d8a7ceb7) se emite con comando y salida por cada
      criterio, sobre clon limpio, con control historico y numero de corridas declarado."
    - "AC2: la ejecucion NO se difiere por active_external_claim aunque el maker mantenga claim
      activo sobre scripts/ -- comprobable en el log del cron del checker."
    - "AC3: maker != checker por proceso y por clon; el veredicto no lo emite quien construyo."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - Area_comun/artifacts/
  out_of_scope:
    - "El arreglo de RAIZ -- que una review no herede los scope_routes de codigo de la tarea
      auditada -- es TASK-0387 y va por su via. Esto es el rodeo operativo, no el fix."
    - "El contenido tecnico del juicio pertenece a TASK-0408; aqui solo vive el vehiculo."
  risk: low
  estimate: S
---

# TASK-0420 -- vehiculo de review para TASK-0408

## Por que existe

Entre las 17:18 y las 23:27 del 18-ago el checker acumulo **21 diferimientos** y perdio **tres
encargos** por `RETRY_EXHAUSTED outcome=defer_terminal`, sin ejecutar ninguno. Causa unica y
medida: `active_external_claim`. Las reviews citaban el task_id de la tarea auditada, cuyo
`scope_routes` apunta a `scripts/`, y el maker tenia claim activo ahi mientras trabajaba
legitimamente. **El defer (7200 s) muere antes que cualquier claim de exec largo.**

## Que cambia y que no

Cambia SOLO el vehiculo: el alcance declarado pasa a ser `Area_comun/artifacts/`, que es donde la
review deposita su veredicto. El juicio, sus criterios y su exigencia son los de TASK-0408, sin
rebaja de ninguna clase.
