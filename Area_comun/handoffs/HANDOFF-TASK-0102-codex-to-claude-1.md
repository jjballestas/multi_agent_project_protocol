---
task_id: TASK-0102
from: Codex
to: Claude
status: in_review
created_at: 2026-06-13T01:05:00Z
requires_response: false
---

# HANDOFF TASK-0102 - Firma por agente

## Resumen

Implementada atestacion de autoria por agente off-by-default bajo
`event_state.agent_signatures_enabled`. El runtime puede almacenar eventos `agent.attestation`, pero la
firma se produce fuera del runtime: `runtime/llm_turn_wrapper.py` expone `sign_turn_report()` para firmar
con una clave privada Ed25519 externa al repo. El replay valida firmas con claves publicas configuradas.

## Cambios entregados

- `runtime/eventlog.py`
  - `agent_signatures_enabled()`
  - `attestation_signing_payload(subject_digest, predicate)`
  - `EventWriter.append_agent_attestation(...)` como evento no materializable (`applied=False`).

- `runtime/protocol_replay.py`
  - `validate_agent_signatures(events, config)`
  - Validacion de schema minima de `agent.attestation`.
  - Verificacion Ed25519 real con `cryptography` cuando el backend `local-ed25519` esta activo.
  - Deteccion de agente desconocido, clave publica faltante, backend no soportado, firma invalida y predicado incompleto.

- `runtime/llm_turn_wrapper.py`
  - `sign_turn_report(...)` firma un turn-report con clave privada externa.
  - No cambia el comportamiento por defecto ni el schema del turn-report.

- `protocol.config.json` y `protocol.config.template.json`
  - Agregados `agent_signatures_enabled: false`, `signature_backend: local-ed25519` y
    `signature_config.public_keys: {}`.

- `scripts/validate_collaboration_state.py`
  - Integra `validate_agent_signatures` en el gate principal. Con flag apagado es no-op.

- `examples/agent_signature_cases/run_agent_signature_cases.py`
  - 10 golden cases deterministas con clave Ed25519 de test generada desde seed fijo en memoria.

## Evidencia

- `python examples\agent_signature_cases\run_agent_signature_cases.py` -> 10/10 pass.
- `python examples\chain_cases\run_tests.py` -> 10/10 pass.
- `python examples\runtime_protocol_replay_cases\run_runtime_protocol_replay_cases.py` -> OK, 6 casos.
- `python examples\llm_turn_wrapper_cases\run_llm_turn_wrapper_cases.py` -> OK, 10 casos.
- `python examples\runtime_eventlog_cases\run_runtime_eventlog_cases.py` -> OK, 5 casos.
- `python scripts\validate_collaboration_state.py --root .` -> OK con warning preexistente de mailbox:
  `MSG-20260613-Claude-TASK0101-ratificado-done.md` podria archivarse.
- `protocol_state_drift(.)` -> `has_drift: false`, `up_to_seq: 348` antes del cierre.

## Overhead medido

- Firma Ed25519: 64 bytes binarios, 88 caracteres base64.
- Atestacion golden completa: aproximadamente 850-1100 bytes JSON por evento, segun predicado.
- Tokens: no se agregan al turn-report por defecto; `sign_turn_report()` devuelve una atestacion separada.

## Notas de revision

- No se guardan claves privadas en el repo. Los goldens usan una clave de test generada en memoria desde
  seed fijo; config solo contiene clave publica.
- Si `cryptography` no esta instalado y el flag se activa con `local-ed25519`, el validador reporta
  `backend_unavailable` en vez de romper imports globales.
- La validacion acepta logs legacy con `agent_signatures_enabled=true` y cero eventos `agent.attestation`;
  no es error, para compatibilidad post-hoc.
