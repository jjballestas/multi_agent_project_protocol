---
message_id: MSG-20260608-Codex-to-Claude-task0080-in-review
type: HANDOFF
task_id: TASK-0080
from: Codex
to: Claude
status: open
requires_response: false
response_owner: Claude
one_line_summary: TASK-0080 entregada a in_review: SA.3 checkpoint humano por K turnos y fix-cycles; invoker real intacto.
requested_action: Revisar y ratificar TASK-0080. Si aceptas, cerrar como done. No promover SA.4 sin GO del operador + rollback.
question: Ratificas TASK-0080 como done?
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0080-codex-to-claude-1.md
  - runtime/orchestrator.py
  - runtime/supervised_autonomy.py
  - examples/supervised_autonomy_cases/run_supervised_autonomy_cases.py
  - Area_comun/tasks/TASK-0080-codex-autonomia-SA3-checkpoint-humano.md
---

# TASK-0080 en review

Implementado SA.3 en shadow: `caps.human_checkpoint_every_k`, corte `human_checkpoint` con
`human_required=True`, escalacion por fix-cycles segun `quality_policy`, y runreport actualizado.

No active autonomia ni toque el invoker real. SA.4 queda bloqueada hasta GO explicito del operador con rollback.
