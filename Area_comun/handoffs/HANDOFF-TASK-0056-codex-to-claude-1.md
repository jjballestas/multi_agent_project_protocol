---
handoff_id: HANDOFF-TASK-0056-codex-to-claude-1
task_id: TASK-0056
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-07
context_refs:
  - Area_comun/tasks/TASK-0056-codex-tool-policy.md
  - Area_comun/specs/SPEC-0042-fase5.2-tool-policy.md
  - protocol.config.json
  - protocol.config.template.json
  - runtime/tool_policy.py
  - runtime/turn_validate.py
  - runtime/turn_schema.json
  - Area_comun/protocol/SCHEMA_VERSIONING.md
  - runtime/orchestrator.py
  - examples/runtime_tool_policy_cases/run_runtime_tool_policy_cases.py
  - .github/workflows/validate.yml
---

# Handoff TASK-0056 - Tool policy deny-by-default

## Entrega

- `protocol.config.json` y `protocol.config.template.json` declaran `tool_policy` enabled + default deny, con reglas por herramienta, capacidad y scope para arquitecto/implementador.
- `runtime/tool_policy.py` agrega:
  - `is_tool_allowed(agent, tool, task_scope, registry, config)`;
  - `classify_action(action)`;
  - `gate_for_action(tipo)`.
- `runtime/turn_schema.json` sube a `schema_version: 1.2.0` con campos opcionales `tools`, `actions` y `decision_refs`; `Area_comun/protocol/SCHEMA_VERSIONING.md` documenta el MINOR.
- `runtime/turn_validate.py` cablea la politica:
  - tool no permitida => error semantico `security.tool_denied`;
  - `contract_change` sin `decision_refs` => error;
  - `external`/`sensitive` sin `gate.human_required=true` => error;
  - `local_write` exige `changed_paths`.
- `runtime/orchestrator.py` conserva esos campos al limpiar el report antes de validar.
- Nuevo golden `examples/runtime_tool_policy_cases/run_runtime_tool_policy_cases.py` con 6 casos y step de CI.

## Validacion ejecutada

- `python examples/runtime_tool_policy_cases/run_runtime_tool_policy_cases.py` -> 6/6.
- `python examples/runtime_turn_cases/run_runtime_turn_schema_cases.py` -> 5/5.
- `python examples/runtime_turn_cases/run_runtime_turn_semantic_cases.py` -> 5/5.
- Bloque runtime completo ejecutado: router, N-agent, property, concurrency, guardrail, tool-policy, eventlog, eventlog-gate, review/QA, registry, turn schema/semantic, apply, loop, observability, llm adapter y prune.
- `python scripts/validate_collaboration_state.py --root .` verde con warnings FYI no bloqueantes.
- `./scripts/validate_collaboration_state.ps1 -Root .` verde con los mismos warnings.
- `python scripts/scan_encoding.py --root .` verde.
- `./scripts/scan_encoding.ps1 -Root .` verde.
- `python scripts/scan_domain_neutrality.py --root .` verde.
- `./scripts/scan_domain_neutrality.ps1 -Root .` verde.
- `python scripts/prune_state.py --root . --check` verde.
- `./scripts/prune_state.ps1 -Root . -Check` verde.
- Tras liberar el claim, `python scripts/prune_state.py --root . --apply` archivo 2 claims; `--check` final queda verde.

## Limites respetados

- Aditivo y reversible: sin `tool_policy` declarado, `is_tool_allowed` conserva el comportamiento legacy.
- La politica solo se activa sobre herramientas/acciones declaradas; reportes antiguos sin esos campos siguen pasando.
- Sin red, sin secretos, domain-neutral.
- No toque 5.3, Fase B ni Fase 6/7.
- Release atomico aplicado: `TASK-0056` pasa a `in_review`, el claim de Codex queda liberado y la poda de mantenimiento queda al dia.
