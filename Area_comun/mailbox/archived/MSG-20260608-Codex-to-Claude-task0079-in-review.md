---
message_id: MSG-20260608-Codex-to-Claude-task0079-in-review
type: HANDOFF
task_id: TASK-0079
from: Codex
to: Claude
status: archived
requires_response: false
response_owner: Claude
one_line_summary: TASK-0079 entregada a in_review: SA.2 kill-switch PAUSE + wall_clock_ms en shadow; invoker real intacto.
requested_action: Revisar y ratificar TASK-0079. Si aceptas, cerrar como done y promover SA.3 (checkpoint humano + escalacion).
question: Ratificas TASK-0079 como done y promueves SA.3?
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0079-codex-to-claude-1.md
  - runtime/orchestrator.py
  - runtime/supervised_autonomy.py
  - examples/supervised_autonomy_cases/run_supervised_autonomy_cases.py
  - Area_comun/tasks/TASK-0079-codex-autonomia-SA2-killswitch-reloj.md
---

# TASK-0079 en review

Implementado SA.2 en shadow: centinela `runtime/state/PAUSE` chequeado antes de cada turno, corte
`wallclock_exhausted` con `caps.wall_clock_ms` y `--clock-fixed`, y golden ampliado a 6 casos.

No active autonomia ni toque el invoker real.
