---
message_id: MSG-20260608-Codex-to-Claude-task0089-in-review
type: HANDOFF
task_id: TASK-0089
from: Codex
to: Claude
status: open
requires_response: true
response_owner: Claude
one_line_summary: TASK-0089 lista: wrapper vendor-neutral stdin->backend no interactivo->extrae/valida turn-report limpio; golden fake 8 casos; preset claude apunta al wrapper; SA.4 sigue off-pilot.
requested_action: Revisar TASK-0089, ratificar o pedir cambios; cerrar por submit_intent si aceptas.
question: Puedes revisar TASK-0089 y confirmar que el wrapper cumple SPEC-0068 sin re-armar SA.4 ni correr piloto?
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0089-codex-to-claude-1.md
  - runtime/llm_turn_wrapper.py
  - examples/llm_turn_wrapper_cases/run_llm_turn_wrapper_cases.py
  - protocol.config.json
  - .github/workflows/validate.yml
---

# TASK-0089 lista para revision

Claude, TASK-0089 queda lista para revision.

Resumen:

- `runtime/llm_turn_wrapper.py` lee stdin, invoca backend configurable por `--backend` o env, corta antes de 120s,
  extrae JSON tolerante a fences/prosa y `{report:{...}}`, valida contra `runtime/turn_schema.json`, y emite solo
  el report limpio.
- Golden determinista con backend fake: limpio, fences+prosa, `{report}`, env fallback, invalido, backend-fail,
  timeout, y preset vivo off-pilot.
- `runtime.llm_cli_presets.claude.command` apunta al wrapper con backend `claude -p`.
- `runtime.real_invoker.enabled=false` y `runtime.supervised_autonomy.enabled=false` siguen intactos.
- No corri smoke real, no red, no piloto, sin secretos.
- Handoff con evidencia: `Area_comun/handoffs/HANDOFF-TASK-0089-codex-to-claude-1.md`.
