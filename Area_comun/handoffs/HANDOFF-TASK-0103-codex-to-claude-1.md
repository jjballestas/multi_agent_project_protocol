---
task_id: TASK-0103
from: Codex
to: Claude
status: in_review
created_at: 2026-06-13T01:25:00Z
requires_response: false
---

# HANDOFF TASK-0103 - Anclaje externo periodico

## Resumen

Implementado anclaje de cabeza de cadena off-by-default bajo `event_state.anchor_enabled`. El backend
`git-remote` queda soportado para una ruta local de auditoria determinista; los remotos reales fallan
cerrado si requieren credenciales externas no configuradas, sin crear eventos `chain.anchor` parciales.

## Cambios entregados

- `runtime/eventlog.py`
  - `anchor_enabled()`, `anchor_config()`.
  - `event_head_digest()`.
  - `anchor_to_git_remote()` para destino local tipo repo/directorio de auditoria (`HEAD` + `anchors.log`).
  - `anchor_due()` con `interval_seconds=0` como “siempre vencido”.
  - `EventWriter.periodic_anchor_if_due(...)` que crea eventos `chain.anchor` no materializables.

- `runtime/protocol_replay.py`
  - `verify_anchor_monotonicity(events, config)`.
  - Validacion de schema minima de `chain.anchor`.
  - Deteccion de reordenamiento, duplicados y campos faltantes.

- `scripts/validate_collaboration_state.py`
  - Integra `verify_anchor_monotonicity`; con flag apagado es no-op.

- `protocol.config.json` y `protocol.config.template.json`
  - Agregados `anchor_enabled: false` y `anchor_config` sin secretos ni destino accidental.

- `examples/anchor_cases/run_anchor_cases.py`
  - 10 golden cases deterministas.

## Evidencia

- `python examples\anchor_cases\run_anchor_cases.py` -> 10/10 pass.
- `python examples\agent_signature_cases\run_agent_signature_cases.py` -> 10/10 pass.
- `python examples\chain_cases\run_tests.py` -> 10/10 pass.
- `python examples\runtime_protocol_replay_cases\run_runtime_protocol_replay_cases.py` -> OK, 6 casos.
- `python examples\runtime_eventlog_cases\run_runtime_eventlog_cases.py` -> OK, 5 casos.
- `python examples\llm_turn_wrapper_cases\run_llm_turn_wrapper_cases.py` -> OK, 10 casos.
- `python scripts\validate_collaboration_state.py --root .` -> OK con warning preexistente de mailbox:
  `MSG-20260613-Claude-TASK0101-ratificado-done.md` podria archivarse.
- `protocol_state_drift(.)` -> `has_drift: false`, `up_to_seq: 355` antes del cierre.

## Notas de revision

- No se agregan secretos. `remote_url` queda vacio en config live/template.
- En tests, el backend `git-remote` usa una ruta local bajo `.protocol-tmp` para simular el medio externo
  de auditoria sin red ni credenciales.
- Un remoto `https://...` en esta implementacion falla cerrado con `EventLogError`; la maquina operadora
  debera proveer credenciales/destino fuera del repo antes de activar un backend remoto real.
- `chain.anchor` convive con `prev_hash` y `agent.attestation`; GC-6 valida las tres piezas juntas.
