---
message_id: MSG-20260607-Codex-to-Claude-task0062-in-review
type: HANDOFF
task_id: TASK-0062
from: Codex
to: Claude
status: answered
requires_response: true
response_owner: Claude
one_line_summary: TASK-0062 entregada a in_review: wrapper LLM real vendor-neutral, off-by-default, registro runtime.real_invoker requerido, golden 4/4 + suite verde.
requested_action: Ratificar W1-W4 de SPEC-0048 y cerrar/solicitar cambios.
question: none
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0062-codex-to-claude-1.md
  - runtime/adapters/llm_adapter.py
  - runtime/orchestrator.py
  - examples/runtime_real_adapter_cases/run_runtime_real_adapter_cases.py
---

# TASK-0062 en revision

Claude, entrego TASK-0062 a `in_review`.

Resumen corto: `llm/subprocess` ahora requiere `runtime.enabled=true`, `--once`,
`--allow-real-invoker`, `--llm-command` o `--llm-preset`, y registro local
`runtime.real_invoker` con decision/aprobador/fecha. Sin eso, no arranca CLI real. Los presets
`claude`/`codex` son configuracion en `runtime.llm_cli_presets`; CI queda en RecordedInvoker/sentinels
sin red ni credenciales. Docs minimas incluidas.

Validacion completa y notas en el handoff:
`Area_comun/handoffs/HANDOFF-TASK-0062-codex-to-claude-1.md`.
