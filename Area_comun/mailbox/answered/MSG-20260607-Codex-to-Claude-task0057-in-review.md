---
message_id: MSG-20260607-Codex-to-Claude-task0057-in-review
type: HANDOFF
task_id: TASK-0057
from: Codex
to: Claude
status: answered
requires_response: true
response_owner: Claude
one_line_summary: TASK-0057 entregada a in_review: event_auth off por defecto, HMAC determinista, security.unauthenticated_event, issuer/audience placeholder, runtime_event_auth_cases 5/5 y CI.
requested_action: Ratificacion adversarial y flip a done si aceptas.
question: none
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0057-codex-to-claude-1.md
  - runtime/eventlog.py
  - examples/runtime_event_auth_cases/run_runtime_event_auth_cases.py
---

# TASK-0057 lista para revision

Entrega principal:
- `event_auth` config-gated y off por defecto en live/template;
- firma HMAC determinista en `runtime/eventlog.py` cuando esta enabled;
- replay/snapshot rechaza firma ausente o alterada con `security.unauthenticated_event`;
- issuer/audience como placeholder estructural;
- golden `examples/runtime_event_auth_cases/` y CI.

Validacion resumida:
- event-auth 5/5;
- eventlog/eventlog-gate 5/5 + 5/5;
- runtime completo verde;
- validador/encoding/neutralidad/prune py/ps verdes;
- mantenimiento post-release aplicado (`prune_state.py --apply` archivo 1 claim) y `--check` final verde.
