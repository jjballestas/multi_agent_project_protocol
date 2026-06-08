---
message_id: MSG-20260608-Codex-to-Claude-task0082-in-review
type: HANDOFF
task_id: TASK-0082
from: Codex
to: Claude
status: archived
requires_response: true
response_owner: Claude
one_line_summary: TASK-0082 entregada a in_review: SA.5 docs supervised autonomy, sin activar SA.4 ni tocar invoker real.
requested_action: Revisar y ratificar TASK-0082 contra SPEC-0064; si aceptas, cerrar como done. No promover SA.4 sin GO operador + rollback.
question: Ratificas TASK-0082 como done?
context_refs:
  - Area_comun/tasks/TASK-0082-codex-autonomia-SA5-docs.md
  - Area_comun/specs/SPEC-0064-autonomia-supervisada.md
  - Area_comun/handoffs/HANDOFF-TASK-0082-codex-to-claude-1.md
changed_refs:
  - Area_comun/protocol/SUPERVISED_AUTONOMY.md
  - Area_comun/protocol/N_AGENT_RUNTIME.md
  - README_INSTANCIACION.md
validation_refs:
  - python scripts\scan_encoding.py --root .
  - python scripts\scan_domain_neutrality.py --root .
  - python scripts\validate_collaboration_state.py --root .
  - python scripts\prune_state.py --root . --check
---

# TASK-0082 in review - SA.5 docs supervised autonomy

Documente el sobre SA.1-SA.3 ya implementado: configuracion `runtime.supervised_autonomy`, caps, flag
`--allow-supervised-autonomy`, paradas duras, `runtime/state/PAUSE`, `*.runreport.md` y frontera SA.4.

No active autonomia, no cambie `protocol.config.json` y no toque el invoker real. SA.4 queda gateado por GO del
operador + rollback.
