---
id: HANDOFF-TASK-0106-codex-to-claude-1
task_id: TASK-0106
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-13
requires_response: true
response_owner: Claude
requested_action: review TASK-0106 implementation and close as done if accepted
---

# HANDOFF TASK-0106 - Codex to Claude

TASK-0106 queda implementada para revision. El alcance aplicado es el minimo seguro de SPEC-0078/DECISION-0031: compaction off-by-default, tool-result clearing, limites medidos y primitivo de subagente off-by-default. DELTA-3 queda fuera de 0106.

## Cambios principales

- `runtime/orchestrator.py`: agrega `runtime.context_policy`, `build_turn_context`, medicion `assembled_context_tokens`, warning/fallback por umbral, gate de `task_close_summary` al cerrar en `done`, metadata de contexto en runlog y `delegate_subagent` off-by-default.
- `runtime/runlog.py`: agrega resumenes destilados por turno, conteo de resultados de herramientas, ventana reciente y rolling summary determinista.
- `runtime/adapters/base.py` y `runtime/adapters/llm_adapter.py`: extienden `ContextPack` y exponen contexto compacto al prompt solo si `compaction_enabled=true`.
- `protocol.config.json` y `protocol.config.template.json`: incorporan defaults off-by-default para `runtime.context_policy`.
- `scripts/measure_context_cost.py` y `.ps1`: miden contexto por turno con/sin compaction y soportan baseline JSON.
- `examples/context_policy_cases/run_tests.py`: cubre GC-1..GC-9.
- `Area_comun/specs/SPEC-0078-compaction-y-subagentes.md`: documenta baseline TASK-0106 en sec. 2.5.
- `Area_comun/artifacts/baseline-context-20260613.json`: baseline medido.

## Baseline medido

Artefacto: `Area_comun/artifacts/baseline-context-20260613.json`.

- Cold-start slim: 9346 tokens.
- Cold-start full: 19676 tokens.
- Delta cold-start: 10330 tokens.
- Turn-context con compaction: 22092 tokens.
- Turn-context legacy/full: 42752 tokens.
- Delta turn-context: 20660 tokens.
- TASK-0106: 13598 con compaction vs 23928 legacy.
- TASK-0109: 8494 con compaction vs 18824 legacy.

## Evidencia ejecutada

- `python -m py_compile runtime\orchestrator.py runtime\runlog.py runtime\adapters\base.py runtime\adapters\llm_adapter.py scripts\measure_context_cost.py examples\context_policy_cases\run_tests.py` -> OK.
- `python examples\context_policy_cases\run_tests.py` -> OK, 9/9.
- `powershell -NoProfile -ExecutionPolicy Bypass -File examples\context_cost_cases\run_context_cost_cases.ps1 -Root .` -> OK.
- `python examples\runtime_loop_cases\run_runtime_loop_cases.py` -> OK, 15/15.
- `python examples\runtime_budget_cases\run_runtime_budget_cases.py` -> OK, 5/5 tras ejecutar con permiso elevado por ACL temporal del sandbox.
- `python examples\llm_adapter_cases\run_llm_adapter_cases.py` -> OK, 6/6 tras ejecutar con permiso elevado por ACL temporal del sandbox.
- `python scripts\scan_domain_neutrality.py --root .` -> OK.
- `python scripts\validate_collaboration_state.py --root .` -> OK antes del handoff-release.
- `protocol_state_drift(Path('.'))` -> sin drift antes del handoff-release.

## Nota de riesgo

`python scripts\scan_encoding.py --root .` sigue fallando por mensajes historicos con bytes no ASCII en mailbox (`answered`, `archived` y un mensaje abierto del operador). No son rutas creadas ni modificadas por TASK-0106.

## Solicitud de revision

Revisar consistencia de SPEC-0078, AC/GC-8/GC-9 y el contrato off-by-default. Si aceptas, puedes cerrar TASK-0106 como done.
