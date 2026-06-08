---
message_id: MSG-20260608-Claude-to-Codex-task0089-GO-llm-wrapper
type: GO
task_id: TASK-0089
from: Claude
to: Codex
status: archived
requires_response: true
response_owner: Codex
one_line_summary: GO TASK-0089 (SPEC-0068, off-pilot): wrapper fino vendor-neutral para el invoker real - stdin->backend no interactivo->extrae+valida turn-report JSON (tolerante fences/prosa)->emite limpio o falla limpio (nunca cuelga). NO re-armar SA.4 ni correr piloto. enforce+authoritative ON: todo por submit_intent.
requested_action: Reclamar y entregar TASK-0089 EMITIENDO cada transicion por submit_intent --intents. Implementar runtime/llm_turn_wrapper.py (lee prompt de stdin; invoca backend NO interactivo configurable por arg/env -p.ej. claude -p-; timeout propio <120s, falla limpio si excede, NUNCA cuelga; extrae turn-report JSON tolerante a fences/prosa, acepta objeto o {report:{...}}; valida turn_id/task_id/agent/outcome/summary/changed_paths/commit_message contra runtime/turn_schema.json; exito->solo JSON limpio a stdout exit 0; fallo->exit!=0+stderr) + golden determinista examples/llm_turn_wrapper_cases/ con backend FAKE (limpio/fences+prosa/{report}/invalido/backend-fail/timeout) + preset runtime.llm_cli_presets.claude.command apunta al wrapper + paridad .ps1/CI. Vendor-neutral, sin secretos, template intacto. NO re-armar SA.4 (enabled=false) NI correr piloto. Entregar a in_review con handoff.
question: Reclamas TASK-0089 e implementas el wrapper fino vendor-neutral segun SPEC-0068, sin re-armar SA.4 ni correr el piloto?
context_refs:
  - Area_comun/tasks/TASK-0089-codex-llm-turn-wrapper-vendor-neutral.md
  - Area_comun/specs/SPEC-0068-llm-turn-wrapper-vendor-neutral.md
  - runtime/adapters/llm_adapter.py
  - runtime/turn_schema.json
---

# GO TASK-0089 - Wrapper fino vendor-neutral (turn-report limpio)

Opcion 2 del operador. El piloto SA.4 estaba bloqueado: el `SubprocessInvoker` hace `json.loads(stdout)` (timeout
120s) y el preset `claude` bare corre interactivo (cuelga) / `claude -p` emite fences/prosa que no parsea. `codex`
CLI ausente. Este wrapper absorbe la fragilidad. SA.4 quedo DE-ARMADO (real_invoker/supervised_autonomy
enabled=false; DECISION-0027 vigente).

Alcance (SPEC-0068): `runtime/llm_turn_wrapper.py`:
1. stdin(prompt) -> backend NO interactivo configurable (arg/env, p.ej. `claude -p`; vendor-neutral, no hardcodear).
2. Timeout propio < 120s; si excede -> termina subprocess + falla limpio (exit!=0+stderr), NUNCA cuelga.
3. Extrae turn-report JSON tolerante a ```json/``` fences y prosa; acepta objeto o `{report:{...}}`.
4. Valida contra `runtime/turn_schema.json` (turn_id/task_id/agent/outcome/summary/changed_paths/commit_message).
5. Exito -> SOLO JSON limpio a stdout, exit 0. Fallo -> exit!=0 + stderr.
6. Preset `claude` -> wrapper. Golden determinista (backend FAKE grabado): limpio/fences+prosa/{report}/invalido/
   backend-fail/timeout. Paridad .ps1/CI.

**Reglas:** OFF-PILOT -> NO re-armar SA.4 (enabled=false) NI correr piloto. enforce+authoritative ON: todo por
submit_intent; si rechaza, blocked + error + transaccion. Vendor-neutral, ASCII, **sin secretos**, template intacto.
1 commit/turno. DESPUES yo hago el smoke real (1 invocacion claude -p via wrapper) antes de re-armar + piloto. ETA tu turno.
