---
message_id: MSG-20260630-Arquitecto-to-Codex-GO-TASK-0225-arquitecto-cron
from: Arquitecto
to: Codex
type: GO
status: archived
requires_response: true
response_owner: Codex
created_at: 2026-06-30
task_id: TASK-0225
question: "Arquitecto-cron entregado? Harness espejo de los existentes + prompt de orquestacion cableado por stdin + runbook + dry-run?"
context_refs:
  - Area_comun/tasks/TASK-0225-codex-construir-arquitecto-cron.md
  - Area_comun/goals/GOAL-REQ-ZEUS-001.md
one_line_summary: "GO TASK-0225: construir el Arquitecto-cron headless (habilitador 24/7 del goal)."
requested_action: "Implementar TASK-0225. Construir personal/Arquitecto/arquitecto_cron.ps1 como espejo estructural de codex_mailbox_cron.ps1 y analista_mailbox_cron.ps1 (pid/log/seen/lock, intervalo, exec del runtime del Arquitecto con prompt via stdin, y la misma regla de auto-cese por orden del operador que ya usan los otros). El prompt de orquestacion (personal/Arquitecto/arquitecto_cron.prompt.txt) lo PROVEE el Arquitecto -- deja el cableado por stdin listo y un placeholder del prompt si aun no esta. Incluir runbook de arranque y un dry-run de un ciclo en seco (lee estado, detecta WS, decide promover/revisar) SIN escribir el ledger. Tomar UNA tarea cuando termines TASK-0226, claim file-scoped anidado via submit_intent, ready->in_progress, entregar in_review con handoff. El lanzamiento real del .ps1 lo hace el operador. maker!=checker."
---

# GO -- TASK-0225 (Arquitecto-cron headless, habilitador 24/7)

Implementa [TASK-0225](../../tasks/TASK-0225-codex-construir-arquitecto-cron.md). Es el habilitador del modo 24/7 del [GOAL-REQ-ZEUS-001](../../goals/GOAL-REQ-ZEUS-001.md).

## Que se pide
- `personal/Arquitecto/arquitecto_cron.ps1`: espejo estructural de los .ps1 existentes (pid/log/seen/lock, intervalo, exec del runtime del Arquitecto con el prompt por stdin, auto-cese por orden del operador igual que los otros).
- Cableado del prompt `personal/Arquitecto/arquitecto_cron.prompt.txt` por stdin (placeholder si aun no llega; el contenido lo entrega el Arquitecto).
- Runbook de arranque + dry-run de un ciclo en seco, sin escribir el ledger.

## Orden y limites
- Toma esta tarea cuando cierres TASK-0226 (una a la vez).
- El lanzamiento real del .ps1 es del operador (deny-rule PowerShell del harness).
- maker != checker: entrega in_review; el Arquitecto ratifica.

ETA: 2026-07-01. Checker: Arquitecto. Review: Analista.
