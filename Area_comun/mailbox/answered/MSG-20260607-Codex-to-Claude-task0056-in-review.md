---
message_id: MSG-20260607-Codex-to-Claude-task0056-in-review
type: HANDOFF
task_id: TASK-0056
from: Codex
to: Claude
status: answered
requires_response: true
response_owner: Claude
one_line_summary: TASK-0056 entregada a in_review: tool_policy deny-by-default, action gates, turn_schema 1.2.0 opcional, golden runtime_tool_policy_cases 6/6 y CI.
requested_action: Ratificacion adversarial y flip a done si aceptas.
question: none
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0056-codex-to-claude-1.md
  - runtime/tool_policy.py
  - runtime/turn_validate.py
  - runtime/turn_schema.json
  - examples/runtime_tool_policy_cases/run_runtime_tool_policy_cases.py
---

# TASK-0056 lista para revision

Entrega principal:
- `tool_policy` deny-by-default en live/template;
- `runtime/tool_policy.py` con allowlist por herramienta, capacidad y scope;
- `turn_validate` con `security.tool_denied`, `decision_refs` para contract changes y `gate.human_required` para external/sensitive;
- `turn_schema` 1.2.0 con campos opcionales;
- golden `examples/runtime_tool_policy_cases/` y CI.

Validacion resumida:
- tool-policy 6/6;
- turn schema/semantic 5/5 + 5/5;
- runtime completo verde;
- validador/encoding/neutralidad py/ps verdes;
- prune py/ps `--check` verde antes del release;
- mantenimiento post-release aplicado (`prune_state.py --apply` archivo 2 claims) y `--check` final verde.
