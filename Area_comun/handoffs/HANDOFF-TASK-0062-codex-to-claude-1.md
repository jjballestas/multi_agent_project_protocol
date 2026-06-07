---
handoff_id: HANDOFF-TASK-0062-codex-to-claude-1
task_id: TASK-0062
from: Codex
to: Claude
status: in_review
created_at: 2026-06-07
context_refs:
  - Area_comun/specs/SPEC-0048-wrapper-llm-real.md
  - Area_comun/decisions/DECISION-0021-activacion-wrapper-llm.md
  - runtime/adapters/llm_adapter.py
  - runtime/orchestrator.py
  - examples/runtime_real_adapter_cases/run_runtime_real_adapter_cases.py
---

# Handoff TASK-0062 - Wrapper LLM real

## Resumen

Implementado el delta del wrapper LLM real sobre los adapters existentes. No rehice
`RecordedInvoker`, `SubprocessInvoker` ni `LLMAdapter`.

## Cambios principales

- `runtime/adapters/llm_adapter.py`: agrega resolucion vendor-neutral de comandos (`--llm-command`
  o preset config-driven), parser de `runtime.llm_cli_presets`, y validacion de registro
  `runtime.real_invoker`.
- `runtime/orchestrator.py`: agrega `--llm-preset`; para `llm/subprocess` exige
  `--allow-real-invoker`, `--once` (preexistente), comando/preset y registro local
  `runtime.real_invoker.enabled:true` con decision, aprobador y fecha.
- `protocol.config.json` y `protocol.config.template.json`: dejan `real_invoker.enabled:false` y
  presets de ejemplo `claude`/`codex` configurables.
- `examples/runtime_real_adapter_cases/`: golden nuevo con 4 casos deterministas, sin red ni
  credenciales: gates de activacion, replay comparativo, limites via RecordedInvoker, presets.
- `examples/llm_adapter_cases/`: el caso de subproceso local ahora registra activacion en el
  fixture antes de esperar exito.
- `.github/workflows/validate.yml`: agrega el runner `runtime_real_adapter_cases`.
- `runtime/README.md` y `README_INSTANCIACION.md`: docs minimas de operacion real segura.

## Invariantes

- Off-by-default: la instancia viva y el template tienen `runtime.real_invoker.enabled:false`.
- Sin secretos: no se agregan credenciales; CI usa RecordedInvoker o scripts locales centinela.
- Vendor-neutral: los presets se leen de config; `claude` y `codex` son ejemplos, no una ruta unica.
- Sin autonomia: `subprocess` sigue requiriendo `--once`; no se habilita loop multi-turno real.
- Limites: la ruta real sigue pasando por gate_pre, validate (guardrails/tool-policy), budget y
  apply/gate/commit.

## Validacion ejecutada

- `python -m py_compile runtime\adapters\llm_adapter.py runtime\orchestrator.py examples\llm_adapter_cases\run_llm_adapter_cases.py examples\runtime_real_adapter_cases\run_runtime_real_adapter_cases.py`
- `python examples\llm_adapter_cases\run_llm_adapter_cases.py` -> 6/6
- `python examples\runtime_real_adapter_cases\run_runtime_real_adapter_cases.py` -> 4/4
- Suite runtime completa (router, N-agent, property, concurrency, guardrails, tool-policy, eventlog,
  event auth, instantiation, upgrade, eventlog gate, review/QA, registry, turn schema/semantic,
  apply, loop, observability, budget, N-agent observability, LLM adapter, real adapter) -> verde.
- Distribucion/gates: runtime instantiation 5 + parity, runtime upgrade 4/4, encoding py/ps,
  neutrality py/ps, validators py/ps, prune --check, git diff --check.
- Casos no-runtime del workflow: encoding_gate, handoff_release, mailbox_status, SDD, compact
  comms, neutrality scan, minimal_instance py/ps -> verde.

Warnings conocidos: los validadores avisan por FYI abiertos `MSG-20260607-Claude-to-Codex-task0060-accepted.md`
y `MSG-20260607-Claude-to-Codex-task0061-accepted.md`; no requieren respuesta y no son de esta entrega.

## Pendiente para revision

Ratificacion adversarial de Claude sobre W1-W4 de SPEC-0048, especialmente que no exista camino de
subproceso real sin registro local y que el default recorded/replay conserve comportamiento.
