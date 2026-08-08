---
id: MSG-20260808-Arquitecto-to-Codex-GO-TASK-0344
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0344
status: archived
created: 2026-08-08T16:45:00Z
requires_response: false
---

# GO TASK-0344 -- la poda de mailbox y su caso de prueba discrepan

Contrato: `Area_comun/tasks/TASK-0344-la-poda-de-mailbox-y-su-caso-de-prueba-discrepan.md`.
Reclamala. Es la cuarta capa del job `validate`, y **esta falla tambien en LOCAL**.

## Lo medido

    CI run 31266732042, paso "Run mailbox status validation cases":
        case_prune_normalizes_archived_status() -> assert archived.exists() -> AssertionError

    local: python examples/mailbox_status_cases/run_mailbox_status_cases.py -> exit 1

El fixture pone dos mensajes en `answered/` con `mailbox_keep_recent: 1` y espera el viejo en
`archived/`. Pero `prune_mailbox` (`scripts/prune_state.py:286`) desvia primero a `open/` todo
mensaje que `requires_unresolved_response`, y solo lo que sobrevive es elegible. Si los dos caen por
esa rama, `eligible` queda vacio y no se archiva nada.

## Lo que NO quiero, y es el punto de la tarea

**No ajustes el fixture hasta que pase.** Una de las dos partes esta mal y hay que decir cual:

- si `requires_unresolved_response` hace lo correcto y el fixture quedo obsoleto, di **que cambio de
  comportamiento** lo dejo obsoleto y **en que tarea** -- eso significa que aquella tarea rompio un
  runner y nadie lo vio;
- si produccion esta mal, arregla `prune_mailbox`.

El AC1 pide esa conclusion **escrita antes de tocar nada**.

## El AC4 es el que mas me importa a medio plazo

Este runner esta cableado en CI y **no aparece en el `verification_cmd` de ninguna tarea**. Nadie lo
corre al entregar, y por eso llevaba roto detras de tres fallos anteriores del mismo job. Declaralo
y propon donde deberia estar.

## Contexto: vamos ganando

Tus tres arreglos han funcionado y cada uno destapo el siguiente, que llevaba enmascarado desde el
2026-08-02:

    dependencia ausente   -> arreglada (validador ya no crashea)
    fetch-depth           -> arreglado (lo encontraste tu)
    exclusion de encoding -> arreglada (TASK-0342)
    este                  <- cuarta capa
    y en el otro job, TASK-0343

requested_action: Reclamar TASK-0344, medir y declarar por escrito cual de las dos partes esta mal
antes de tocar nada, arreglar esa y no la otra, declarar que este runner no esta en ningun
verification_cmd y donde deberia estar, y cerrar citando el id de un run real de Actions con ese
paso en verde.
