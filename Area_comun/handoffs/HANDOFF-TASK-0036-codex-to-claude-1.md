---
handoff_id: HANDOFF-TASK-0036-codex-to-claude-1
task_id: TASK-0036
from: Codex
to: Claude
status: in_review
created_at: 2026-06-06
---

# HANDOFF TASK-0036 - Adapter LLM real

## Resultado
Implementado SPEC-0035 sin disparar invoker real.

- `runtime/adapters/llm_adapter.py`: `LLMAdapter`, `RecordedInvoker`, `SubprocessInvoker` y builder de prompt desde `ContextPack`.
- `runtime/orchestrator.py`: `--adapter llm`, `--llm-invoker recorded|subprocess`, `--llm-command`, `--allow-real-invoker`; `recorded` usa `--replay-report` como transcript file/dir; `subprocess` exige `--once`.
- Limites: default `replay` intacto; CI sin red; subprocess real requiere flags explicitos; el orquestador rechaza cambios de worktree no declarados en `changed_paths`; budget pre-apply aborta si el coste declarado supera `--budget-tokens`.
- `examples/llm_adapter_cases/`: 5 golden (once recorded, replay comparativo, rechazo allowlist, abort budget, enabled:false).
- `runtime/README.md`: uso documentado de recorded y subprocess real gateado.

## Decision de implementacion
Formato de transcript propuesto para `RecordedInvoker`:

```json
{
  "format": "recorded_invoker.v1",
  "expected_prompt_contains": ["TASK-9000"],
  "report": { "turn_id": "...", "task_id": "TASK-9000" }
}
```

`expected_prompt_contains` es opcional y sirve para probar que el prompt incluye task/spec sin acoplar el golden a todo el texto. `report` es el turn report que se valida por el loop M1.

## Verificacion
- `python -m py_compile runtime/adapters/llm_adapter.py runtime/orchestrator.py examples/llm_adapter_cases/run_llm_adapter_cases.py`
- `python examples/llm_adapter_cases/run_llm_adapter_cases.py` -> 5 OK
- `python examples/runtime_loop_cases/run_runtime_loop_cases.py` -> 5 OK
- `python examples/runtime_observability_cases/run_runtime_observability_cases.py` -> 5 OK
- `python examples/runtime_apply_cases/run_runtime_apply_cases.py` -> 4 OK
- `python examples/runtime_turn_cases/run_runtime_turn_schema_cases.py` -> 4 OK
- `python examples/runtime_turn_cases/run_runtime_turn_semantic_cases.py` -> 3 OK
- `python examples/runtime_router_cases/run_runtime_router_cases.py` -> 5 OK
- `python scripts/validate_collaboration_state.py` -> OK
- `python scripts/scan_encoding.py` -> OK
- `python scripts/scan_domain_neutrality.py` -> OK

## Notas de seguridad
No se ejecuto `SubprocessInvoker` real. La primera corrida real sobre el repo vivo sigue pendiente de aprobacion puntual del operador cuando Claude avise.
