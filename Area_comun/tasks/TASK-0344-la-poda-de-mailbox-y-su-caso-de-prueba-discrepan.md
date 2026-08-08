---
id: TASK-0344
title: La poda de mailbox y su caso de prueba discrepan, y el runner lleva roto sin que nadie lo corra
status: in_review
owner: Codex
type: implementation
file: Area_comun/tasks/TASK-0344-la-poda-de-mailbox-y-su-caso-de-prueba-discrepan.md
created: 2026-08-08
intake:
  type: fix
  goal: >
    `examples/mailbox_status_cases/run_mailbox_status_cases.py` falla en
    `case_prune_normalizes_archived_status` con `assert archived.exists()`, y falla TANTO en CI como
    en local. El fixture crea dos mensajes en `answered/` con `mailbox_keep_recent: 1` y espera que
    el mas viejo acabe en `archived/`. `prune_mailbox` (`scripts/prune_state.py:286`) desvia primero
    a `open/` todo mensaje que `requires_unresolved_response`, y solo lo que sobrevive entra en
    `eligible`; si los dos mensajes del fixture caen por esa rama, `eligible` queda vacio y no se
    archiva nada. Hay que MEDIR cual de los dos tiene razon -- produccion o el caso de prueba -- y
    arreglar el que este mal, no el que sea mas facil.
  acceptance:
    - "AC1 (diagnostico ANTES del arreglo): se mide y declara por que rama pasa cada mensaje del fixture y por que, y se determina si el comportamiento actual de prune_mailbox es el correcto o si es el fixture el que quedo obsoleto. La conclusion se escribe antes de tocar nada."
    - "AC2 (se arregla el lado que esta mal): si produccion esta mal, se corrige prune_mailbox; si el caso de prueba quedo obsoleto, se corrige el caso y se declara que cambio de comportamiento lo dejo obsoleto y en que tarea. NO se ajusta el fixture solo para que pase."
    - "AC3 (el runner vuelve a ser portante): tras el arreglo el runner sale exit 0, y se falsa que sigue cayendo si prune deja de archivar lo que debe archivar."
    - "AC4 (por que nadie lo corria): se declara que este runner esta cableado en CI y no aparece en el verification_cmd de ninguna tarea, y se propone donde deberia estar. Es la razon por la que llevaba roto sin que se notara."
    - "AC5 (cerrado en CI REAL): el paso `Run mailbox status validation cases` sale success en un run real de GitHub Actions, citando su id."
    - "AC6 (sin regresion): la poda real sigue funcionando sobre el arbol vivo -- prune --check exit 0 -- y los gates del repo exit 0 en clon limpio."
  verification_cmd:
    - "python examples/mailbox_status_cases/run_mailbox_status_cases.py"
    - "python scripts/prune_state.py --root . --check"
    - "python scripts/validate_collaboration_state.py --root ."
  scope_routes:
    - examples/mailbox_status_cases/run_mailbox_status_cases.py
    - scripts/prune_state.py
    - Area_comun/protocol/FALSIFICATION_CONTRACTS.json
  out_of_scope:
    - "La asercion de rollback del runner de retry (TASK-0343)."
    - "La exclusion del escaner de encoding (TASK-0342)."
    - "Codigo de producto."
  risk: high
  estimate: M
---

# TASK-0344 -- produccion y su caso de prueba discrepan

## Lo medido

CI, run 31266732042, job `validate`, paso `Run mailbox status validation cases`:

    case_prune_normalizes_archived_status()
      assert archived.exists()
    AssertionError

**Y falla igual en local**: `python examples/mailbox_status_cases/run_mailbox_status_cases.py`
-> exit 1. No es un problema de entorno; esta roto en todas partes.

## La discrepancia

    fixture:   answered/MSG-001-old.md, answered/MSG-002-new.md, mailbox_keep_recent: 1
               espera MSG-001-old en archived/

    prune:     if requires_unresolved_response(path):  -> a open/, continue
               eligible.append(path)
               move = eligible[:-keep_recent]

Si los dos mensajes del fixture entran por la primera rama, `eligible` queda vacio y no se archiva
nada.

## Lo que NO quiero

Que se ajuste el fixture hasta que pase. **Una de las dos partes esta mal y hay que decir cual.**
Si `requires_unresolved_response` es correcto y el fixture quedo obsoleto tras un cambio de
comportamiento, hay que decir **que cambio** lo dejo obsoleto y **en que tarea** -- porque eso
significa que aquella tarea rompio un runner y nadie lo vio.

## Por que nadie lo vio

El runner esta cableado en CI y **no aparece en el `verification_cmd` de ninguna tarea**. Nadie lo
corre al entregar. Llevaba roto detras de tres fallos anteriores del mismo job, que caian primero.
El AC4 pide declararlo y proponer donde deberia estar.
