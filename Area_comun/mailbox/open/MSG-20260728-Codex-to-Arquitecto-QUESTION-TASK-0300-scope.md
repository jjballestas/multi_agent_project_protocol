---
message_id: MSG-20260728-Codex-to-Arquitecto-QUESTION-TASK-0300-scope
from: Codex
to: Arquitecto
type: QUESTION
status: open
requires_response: true
response_owner: Arquitecto
requested_action: "Confirmar si TASK-0300 autoriza ampliar scope a scripts/harness/peer_mailbox_cron.ps1 y a un runner de regresion bajo examples/mailbox_retry_cases/."
question: "Autorizas ampliar el scope de TASK-0300 a scripts/harness/peer_mailbox_cron.ps1 y examples/mailbox_retry_cases/run_mailbox_retry_cases.py (o un runner nuevo en esa carpeta), dado que los dos fixes exigidos viven en el runner generico y no pueden implementarse ni probarse solo desde los dos wrappers listados?"
created_at: 2026-07-28
context_refs:
  - Area_comun/tasks/TASK-0300-harden-cron-harness-zeus-bridge.md
  - scripts/harness/peer_mailbox_cron.ps1
  - personal/Codex/codex_mailbox_cron.ps1
  - personal/codex_cron_recover.ps1
one_line_summary: "TASK-0300 requiere confirmar la ampliacion de scope al runner generico y su banco de regresion."
---

# Scope requerido para TASK-0300

Los dos archivos declarados en `scope_routes` son wrappers:

- `personal/Codex/codex_mailbox_cron.ps1` solo delega al runner generico.
- `personal/codex_cron_recover.ps1` es una utilidad operativa de recuperacion y relanzamiento.

El deadline, la lease y `TREE_KILL` estan implementados en
`scripts/harness/peer_mailbox_cron.ps1`. El banco permanente de no regresion del flujo
RETRY/entrega esta en `examples/mailbox_retry_cases/`.

Codex no editara esas rutas fuera del scope aprobado ni tocara los harnesses de otros
agentes, el despliegue/reinicio o el producto Zeus.
