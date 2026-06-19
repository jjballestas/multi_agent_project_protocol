# HANDOFF TASK-0120 - Codex to Arquitecto

## Estado

TASK-0120 implementado y listo para revision maker!=checker. #4 permanece OFF.

## Cambios

- `runtime/eventlog.py`
  - Agrega resolucion de secreto HMAC `event_auth` por `secret_file` y `secret_env`.
  - Mantiene precedencia legacy: `secret` / `hmac_secret` / `signing_secret` / `key` -> `secret_file` -> `secret_env`.
  - Propaga `root` explicitamente en firma, verificacion, replay y snapshot.
  - Fail-closed: referencias irresolubles levantan `unresolved_key` antes de escribir eventos; verificacion devuelve `reason: unresolved_key`.
  - Path-safety: `secret_file` relativo, sin traversal, dentro de `secrets/` o `.protocol-secrets/`.
- `scripts/validate_collaboration_state.py`
  - Gate AC4 dedicado: rechaza secretos literales de `event_auth` para actores vivos en config commiteado.
- `examples/event_auth_secret_resolution_cases/`
  - Goldens AC1-AC7: keyfile, env, file/env missing, gate literal, secreto fuera del hash, path-safety, precedencia literal.
- `.github/workflows/validate.yml`
  - CI ejecuta `event_auth_secret_resolution_cases`.
- `CHANGELOG.md` y `protocol.config.json`
  - Registra la implementacion como `1.13.0` en config/changelog. No se pudo reconciliar `PROJECT_STATE.version`
    con Codex porque `project_narrative` requiere capability de orchestrator.

## Evidencia

- `python examples\event_auth_secret_resolution_cases\run_event_auth_secret_resolution_cases.py` - OK
- `python examples\runtime_event_auth_cases\run_runtime_event_auth_cases.py` - OK
- `python examples\chain_auth_combined_cases\run_chain_auth_combined_cases.py` - OK
- `python examples\attestation_health_cases\run_attestation_health_cases.py` - OK
- `python examples\agent_signature_cases\run_agent_signature_cases.py` - OK
- `python examples\runtime_protocol_replay_cases\run_runtime_protocol_replay_cases.py` - OK
- `python examples\runtime_protocol_materialize_cases\run_runtime_protocol_materialize_cases.py` - OK after cleaning repo-local temp leftovers from prior runs
- `python examples\intent_flow_cases\run_intent_flow_cases.py` - OK
- `python examples\intent_tx_cases\run_intent_tx_cases.py` - OK
- `python examples\runtime_apply_cases\run_runtime_apply_cases.py` - OK
- `python scripts\validate_collaboration_state.py --root .` - OK
- `python scripts\scan_encoding.py --root .` - OK
- `python scripts\scan_domain_neutrality.py --root .` - OK

## Flags finales

- `event_auth.enabled=false`
- `event_state.chain_enabled=false`
- `event_state.agent_signatures_enabled=false`
- `event_state.anchor_enabled=false`

## Nota para cierre

Arquitecto debe reproducir y, si acepta el bump `1.13.0`, reconciliar `PROJECT_STATE.version` via flujo de
orchestrator o ajustar la version de cierre segun su criterio.
