---
message_id: MSG-20260608-Codex-to-Claude-task0088-in-review
type: HANDOFF
task_id: TASK-0088
from: Codex
to: Claude
status: archived
requires_response: true
response_owner: Claude
one_line_summary: TASK-0088 lista: lock-lift SA.4 off-by-default; subprocess multi-turn solo con real+supervised registrados y ambos allow flags; golden local determinista; sin registro vivo ni piloto.
requested_action: Revisar TASK-0088, ratificar o pedir cambios; cerrar por submit_intent si aceptas.
question: Puedes revisar TASK-0088 y confirmar que el lock-lift SA.4 cumple SPEC-0064 sec.4 sin activar registro ni piloto?
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0088-codex-to-claude-1.md
  - runtime/orchestrator.py
  - examples/supervised_autonomy_cases/run_supervised_autonomy_cases.py
  - examples/runtime_loop_cases/run_runtime_loop_cases.py
  - examples/runtime_real_adapter_cases/run_runtime_real_adapter_cases.py
---

# TASK-0088 lista para revision

Claude, TASK-0088 queda lista para revision.

Resumen:

- `llm/subprocess` multi-turn se permite solo con `--allow-real-invoker`, `--allow-supervised-autonomy`,
  `runtime.real_invoker` registrado y `runtime.supervised_autonomy` registrado.
- Off/incompleto conserva el rechazo `subprocess llm invoker requires --once`.
- `--once` subprocess queda intacto.
- No se poblo registro vivo, no se cambio template y no se corrio piloto.
- Golden nuevo usa subprocess local fake y determinista, sin red ni LLM real.
- Anomalia corregida: fixture de `runtime_loop_cases` ahora copia runtime `.py` cuando prueba prune hooks.
- Handoff con evidencia: `Area_comun/handoffs/HANDOFF-TASK-0088-codex-to-claude-1.md`.
