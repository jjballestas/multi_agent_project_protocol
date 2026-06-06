---
handoff_id: HANDOFF-TASK-0039-codex-to-claude-1
task_id: TASK-0039
from: Codex
to: Claude
status: in_review
created_at: 2026-06-06
---

# HANDOFF TASK-0039 - SubprocessInvoker Windows-safe

## Resultado
Implementado SPEC-0036 sin disparar corrida real sobre el repo vivo.

- `runtime/adapters/llm_adapter.py`: `SubprocessInvoker.from_command` usa `CommandLineToArgvW` en Windows y conserva `shlex.split` POSIX en otros SO.
- `examples/llm_adapter_cases/run_llm_adapter_cases.py`: nuevo golden `case_subprocess_native_command_commits`, que construye un comando con `sys.executable` + script temporal usando separador nativo del host y verifica 1 commit verde.
- El caso cubre prompt por stdin, stdout con turn report JSON, ruta de script con espacios y separador nativo.

## Verificacion
- `python -m py_compile runtime/adapters/llm_adapter.py examples/llm_adapter_cases/run_llm_adapter_cases.py`
- `python examples/llm_adapter_cases/run_llm_adapter_cases.py` -> 6 OK
- `python examples/runtime_loop_cases/run_runtime_loop_cases.py` -> 5 OK
- `python examples/runtime_observability_cases/run_runtime_observability_cases.py` -> 5 OK
- `python examples/runtime_apply_cases/run_runtime_apply_cases.py` -> 4 OK
- `python examples/runtime_router_cases/run_runtime_router_cases.py` -> 5 OK
- `python examples/runtime_turn_cases/run_runtime_turn_schema_cases.py` -> 4 OK
- `python examples/runtime_turn_cases/run_runtime_turn_semantic_cases.py` -> 3 OK
- `python scripts/validate_collaboration_state.py` -> OK
- `python scripts/scan_encoding.py` -> OK
- `python scripts/scan_domain_neutrality.py` -> OK

## Notas
No se ejecuto ninguna corrida real sobre el repo vivo. El fix corrige la tokenizacion local del comando para que el invoker real pueda usar rutas nativas de Windows sin el workaround de `/`.
