---
id: HANDOFF-TASK-0113-codex-to-claude-1
task_id: TASK-0113
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-14
requires_response: true
response_owner: Claude
requested_action: Review TASK-0113 fix and close as done if accepted.
---

# HANDOFF TASK-0113 - Codex to Claude

TASK-0113 queda implementada para revision. El bug latente chain+event_auth queda corregido sacando `event_auth` del payload canonicalizado para la cadena: `event_without_chain_fields()` ahora elimina `prev_hash`, `event_auth` y `deduped`. La firma sigue cubriendo `prev_hash`, porque `signable_event()` conserva `prev_hash`.

## Cambios

- `runtime/eventlog.py`: `event_without_chain_fields()` excluye `event_auth`.
- `examples/chain_auth_combined_cases/run_chain_auth_combined_cases.py`: nuevo golden combinado:
  - positivo: `event_auth.enabled=true` + `event_state.chain_enabled=true` + `metrics.cost_attribution_enabled=true`, con `cost.attributed`, `verify_event_auth`, `validate_chain(valid:true)` y `protocol_state_drift(has_drift:false)`.
  - negativo: tampering del evento `cost.attributed` detectado por cadena y firma.

## Re-review TASK-0111

Con TASK-0113 aplicado, mi re-review de TASK-0111 endurecido PASA para el hop solicitado:

- `cost.attributed` sigue `applied:false`; `replay_protocol_state()` lo omite y no muta task/claim/decision.
- `append_cost_attribution()` sigue pasando por `append_event()`, por tanto respeta firma/cadena cuando esos flags se activen.
- El schema endurecido evita texto libre: subject canonico por dimension, `subject_hash` seudonimo, tags `cost_unit`/`cost_schema`, `context_tokens`, y `metrics.summarize_cost_attribution()` rechaza filas sin unidad/schema.
- No hay ruta de autoridad derivada de `cost.attributed`; un evento forjado afecta metricas, no permisos, scope, claims ni decisiones.
- Activacion live sigue fuera de este handoff: flag true + version + CHANGELOG + hot verification quedan para architect bajo GO del operador.

## Evidencia

- `python -m py_compile runtime\eventlog.py examples\chain_auth_combined_cases\run_chain_auth_combined_cases.py` -> OK.
- `python examples\chain_auth_combined_cases\run_chain_auth_combined_cases.py` -> OK, 2/2.
- `python examples\chain_cases\run_tests.py` -> OK, 10/10.
- `python examples\runtime_event_auth_cases\run_runtime_event_auth_cases.py` -> OK, 5/5.
- `python examples\runtime_cost_attribution_cases\run_runtime_cost_attribution_cases.py` -> OK, 11/11.
- `python examples\runtime_eventlog_cases\run_runtime_eventlog_cases.py` -> OK, 5/5.
- `python examples\intent_flow_cases\run_intent_flow_cases.py` -> OK, 11/11.
- `python examples\runtime_protocol_enforce_cases\run_runtime_protocol_enforce_cases.py` -> OK, 9/9.
- `python examples\agent_signature_cases\run_agent_signature_cases.py` -> OK, 10/10.

## Nota

No active chain/auth/cost flags were enabled in the live instance. This is a dormant machinery fix plus regression coverage.
