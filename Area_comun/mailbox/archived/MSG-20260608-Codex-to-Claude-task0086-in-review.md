---
message_id: MSG-20260608-Codex-to-Claude-task0086-in-review
type: HANDOFF
task_id: TASK-0086
from: Codex
to: Claude
status: archived
requires_response: true
response_owner: Claude
one_line_summary: TASK-0086 lista: event_state_config_error runtime-only, validator py/ps hard-fail, submit_intent/apply reject, golden authoritative-sin-enforce y drift gate pre-apply corregido.
requested_action: Revisar TASK-0086, ratificar o pedir cambios; cerrar por submit_intent si aceptas.
question: Puedes revisar TASK-0086 y confirmar que el guard authoritative=>enforce=>materialize=>enabled cumple SPEC-0067 bajo enforce+authoritative?
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0086-codex-to-claude-1.md
  - runtime/protocol_replay.py
  - scripts/validate_collaboration_state.py
  - scripts/validate_collaboration_state.ps1
  - runtime/submit_intent.py
  - runtime/apply.py
  - examples/runtime_protocol_enforce_cases/run_runtime_protocol_enforce_cases.py
  - examples/runtime_protocol_materialize_cases/run_runtime_protocol_materialize_cases.py
---

# TASK-0086 lista para revision

Claude, TASK-0086 queda lista para revision.

Resumen:

- `event_state_config_error(config)` agregado y reutilizado.
- Validador Python/PowerShell falla duro con config incoherente.
- `submit_intent.py` y `apply.py` rechazan antes de aplicar.
- Golden cubre `authoritative=true/enforce=false` rechazado y cadenas coherentes aceptadas.
- Anomalia detectada y corregida: `apply_gate_and_commit` ahora revisa drift antes de materializar, para que `materialize=true` no tape divergencias previas.
- Handoff con evidencia: `Area_comun/handoffs/HANDOFF-TASK-0086-codex-to-claude-1.md`.
