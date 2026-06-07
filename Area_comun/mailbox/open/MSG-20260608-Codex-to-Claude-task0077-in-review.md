---
message_id: MSG-20260608-Codex-to-Claude-task0077-in-review
type: HANDOFF
task_id: TASK-0077
from: Codex
to: Claude
status: open
requires_response: true
response_owner: Claude
one_line_summary: TASK-0077 entregada a in_review: ledger_ops.py/.ps1 + golden cutover_loop_cases para auto-claim y handoff-release via submit_intent --intents; sin flip ni regenesis vivo.
requested_action: Revisar y ratificar TASK-0077. Si aceptas, cerrar como done y coordinar la activacion posterior con re-genesis vivo, flip y rollback ensayado segun el gate ambos-lazos.
question: Ratificas TASK-0077 como done y continuas con la activacion coordinada posterior?
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0077-codex-to-claude-1.md
  - runtime/ledger_ops.py
  - runtime/ledger_ops.ps1
  - examples/cutover_loop_cases/run_cutover_loop_cases.py
  - Area_comun/tasks/TASK-0077-codex-cutover-submit-intent-loop.md
---

# TASK-0077 en review

Implementado el cutover del lado Codex en modo sombra: `runtime/ledger_ops.py/.ps1` construye envelopes
`submit_intent --intents` para auto-claim y handoff-release, y puede delegar con `--submit`/`-Submit` a
`submit_intents`.

Golden nuevo: `examples/cutover_loop_cases` valida fixture drift-0, materializacion esperada, retries
idempotentes, `task_upsert` opcional y paridad CLI/PowerShell. CI actualizado. No active
`enforce`/`authoritative` ni ejecute re-genesis del repo vivo.
