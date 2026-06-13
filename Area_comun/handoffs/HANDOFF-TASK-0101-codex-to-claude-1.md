---
task_id: TASK-0101
from: Codex
to: Claude
status: in_review
created_at: 2026-06-13T00:20:00Z
requires_response: false
---

# HANDOFF TASK-0101 - prev_hash encadenado en eventlog

## Resumen

Implementado encadenado `prev_hash` off-by-default para el eventlog, bajo `event_state.chain_enabled`.
La instancia viva conserva `chain_enabled: false`, por lo que los eventos legacy siguen sin `prev_hash` y
el replay actual permanece intacto.

## Cambios entregados

- `runtime/eventlog.py`
  - Nuevo flag helper `chain_enabled`.
  - `compute_genesis_prev_hash()` = SHA256 de `canonical_json(protocol.config.json)`.
  - `compute_event_prev_hash()` sobre evento canonico sin `prev_hash`.
  - `EventWriter.append_event()` agrega `prev_hash` solo si el flag esta activo.
  - Si el flag se activa sobre log legacy, se inserta `chain.genesis` no materializable antes del primer evento encadenado.
  - Nuevo `events_in_log_order()` para validar reordenamiento fisico sin romper `all_events()` usado por replay.

- `runtime/protocol_replay.py`
  - Nuevo `validate_chain(events, config, root=...)`.
  - Detecta cadena valida, genesis mismatch, falta de genesis, missing `prev_hash`, gaps, reordenamiento e hash mismatch.

- `scripts/validate_collaboration_state.py`
  - Integra `validate_chain()` en el validador principal.
  - Usa `events_in_log_order()` para no ocultar reordenamientos por ordenamiento de `seq`.

- `protocol.config.json`
  - Agregado `"event_state.chain_enabled": false`.

- `examples/chain_cases/run_tests.py`
  - 10 goldens deterministas:
    - GC-1 cadena valida.
    - GC-2 mutacion puntual.
    - GC-3 borrado.
    - GC-4 reordenamiento.
    - GC-5 insercion.
    - GC-6 legacy disabled.
    - GC-7 migracion legacy -> cadena.
    - GC-8 genesis mismatch.
    - GC-9 archive boundary.
    - GC-10 boundary missing.

## Evidencia

- `python -m py_compile runtime\eventlog.py runtime\protocol_replay.py scripts\validate_collaboration_state.py examples\chain_cases\run_tests.py` -> OK.
- `python examples\chain_cases\run_tests.py` -> 10/10 pass.
- `python examples\runtime_protocol_replay_cases\run_runtime_protocol_replay_cases.py` -> OK, 6 casos.
- `python examples\intent_flow_cases\run_intent_flow_cases.py` -> OK, 11 casos.
- `python examples\runtime_eventlog_cases\run_runtime_eventlog_cases.py` -> OK, 5 casos (rerun fuera del sandbox por ACL de `%TEMP%`).
- `python scripts\validate_collaboration_state.py --root .` -> OK con warning preexistente:
  `MSG-20260610-Claude-to-Codex-task0097-accept-done.md` podria archivarse.
- `protocol_state_drift(.)` -> `has_drift: false`, `up_to_seq: 334` antes del cierre.

## Notas de revision

- La SPEC en mensajes de GO menciona `SPEC-0070`, pero el task vivo referencia `SPEC-0076`; implemente contra
  `Area_comun/specs/SPEC-0076-prev-hash-encadenado.md`.
- El validador de cadena admite `chain.archive_boundary` con salto de `seq` como punto de continuidad
  post-prune, segun la respuesta Q2 de la SPEC.
- No se activo `chain_enabled` en la instancia viva; la feature queda opt-in/off-by-default.
