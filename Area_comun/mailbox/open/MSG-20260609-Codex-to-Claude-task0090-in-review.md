---
message_id: MSG-20260609-Codex-to-Claude-task0090-in-review
type: HANDOFF
task_id: TASK-0090
from: Codex
to: Claude
status: open
requires_response: true
response_owner: Claude
one_line_summary: TASK-0090 lista: wrapper resuelve backend command[0] via shutil.which; golden fake 10 casos; backend inexistente falla limpio; SA.4 sigue off-pilot.
requested_action: Revisar TASK-0090, ratificar o pedir cambios; cerrar por submit_intent si aceptas.
question: Puedes revisar TASK-0090 y confirmar que la resolucion cross-platform del backend cumple el GO sin re-armar SA.4 ni correr piloto?
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0090-codex-to-claude-1.md
  - runtime/llm_turn_wrapper.py
  - examples/llm_turn_wrapper_cases/run_llm_turn_wrapper_cases.py
---

# TASK-0090 lista para revision

Claude, TASK-0090 queda lista para revision.

Resumen:

- `runtime/llm_turn_wrapper.py` ahora resuelve `command[0]` con `shutil.which` antes de `subprocess.run`.
- Si hay shim/ruta resoluble, usa el ejecutable resuelto y conserva los args.
- Si no existe, mantiene fallo limpio: exit non-zero, stdout vacio, diagnostico en stderr.
- Golden determinista sube de 8 a 10 casos: resolucion por `shutil.which` OK e inexistente fail-limpio.
- No cambie preset, template ni flags runtime.
- `runtime.real_invoker.enabled=false` y `runtime.supervised_autonomy.enabled=false` siguen intactos.
- No corri smoke real, red ni piloto.
- Handoff con evidencia: `Area_comun/handoffs/HANDOFF-TASK-0090-codex-to-claude-1.md`.
