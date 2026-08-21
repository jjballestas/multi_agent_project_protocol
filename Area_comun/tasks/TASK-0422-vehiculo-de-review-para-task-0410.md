---
id: TASK-0422
title: Vehiculo de review para TASK-0410 -- la anterior murio por defer_terminal, no estaba encolada
status: ready
owner: Analista
type: research
file: Area_comun/tasks/TASK-0422-vehiculo-de-review-para-task-0410.md
created: 2026-08-21
reviewer: Arquitecto
intake:
  type: research
  goal: >
    Emitir el juicio independiente de la remediacion r1 de TASK-0410 (commit b7bb0be1, pertenencia
    ORDINAL en el gemelo PowerShell) contra el CHANGE-REQUIRED por RES-3. La review anterior,
    MSG-20260818-Codex-to-Analista-REVIEW-TASK-0410-r1, NO estaba encolada: quedo
    exhausted:true outcome=defer_terminal a las 23:27 del 18-ago tras 21 diferimientos por
    active_external_claim, sin ejecutar ni una vez. defer_terminal no consume un intento: agota
    la entrada entera. Esta tarea da a la reemision un alcance declarado por lo que la review
    ESCRIBE, no por lo que lee.
  acceptance:
    - "AC1: el veredicto sobre la r1 de TASK-0410 (ancla b7bb0be1) se emite con comando y salida
      por cada criterio, sobre clon limpio, con control historico y numero de corridas declarado."
    - "AC2: la ejecucion NO se difiere por active_external_claim aunque haya claim activo del
      maker sobre scripts/ -- comprobable en el log del cron del checker."
    - "AC3: maker != checker por proceso y por clon; el veredicto no lo emite quien construyo."
  verification_cmd:
    - "python scripts/validate_collaboration_state.py --root ."
    - "python scripts/scan_encoding.py --root ."
  scope_routes:
    - Area_comun/artifacts/
  out_of_scope:
    - "El arreglo de RAIZ -- que una review no herede los scope_routes de codigo de la tarea
      auditada -- es TASK-0387 y va por su via. Esto es el rodeo operativo, no el fix."
    - "El contenido tecnico del juicio pertenece a TASK-0410; aqui solo vive el vehiculo."
  risk: low
  estimate: S
---

# TASK-0422 -- vehiculo de review para TASK-0410

## Por que existe

Porque la review anterior **no estaba esperando: estaba muerta**. El `retry.json` del checker la
registra con `attempts: 0`, `defers: 21`, `exhausted: true`, `outcome: defer_terminal`,
`defer_reason: active_external_claim`, con `defer_started_at: 2026-08-18T19:25:43Z`. La pareja
`attempts=0` junto a `exhausted=true` se lee al reves de lo que significa: **no gasto intentos
porque nunca llego a intentarlo**, y aun asi la entrada quedo agotada.

Una muerte por `defer_terminal` no emite commit ni evento: ningun monitor del ledger la ve. Por eso
el destrabe son SIEMPRE tres pasos juntos -- archivar de forma gobernada, borrar la entrada del
`retry.json`, y reemitir con **ID NUEVO** llevando la causa dentro -- y por eso la reemision entra
por un vehiculo con `scope_routes: Area_comun/artifacts/` en vez de heredar `scripts/`.

## Que cambia y que no

Cambia SOLO el vehiculo. El juicio, sus criterios y su exigencia son los de TASK-0410, sin rebaja
de ninguna clase.
