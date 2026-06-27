---
handoff_id: HANDOFF-TASK-0195-codex-to-arquitecto-1
task_id: TASK-0195
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-27
implementation_commit: affb5cd
memory_commit: e15020b
---

# HANDOFF TASK-0195 - event_auth runtime override

## Entregado

- `runtime/eventlog.py`: el lector de override ahora es `event_state` y conserva el contrato
  `EVENT_STATE_RUNTIME_CONFIG_PATH` / `event-state.runtime.json`.
- El override sigue admitiendo `actor_auth_enforce` y `actor_auth_config`, y ahora admite solo
  `event_auth.keys`; cualquier otra subclave de `event_auth` falla cerrado.
- `agent_auth_config` / `signing_secret` mergean `event_auth.keys` del override sobre el config pinned por actor.
  El override gana, sin tocar `protocol.config.json`, `protocol.config.template.json`, genesis ni algoritmo HMAC.
- `runtime/README.md`: documenta el contrato combinado de override para actor_auth y altas locales de
  `event_auth.keys`.
- `.github/workflows/validate.yml`: anade el golden permanente
  `examples/event_auth_runtime_override_cases/run_event_auth_runtime_override_cases.py`.

## Evidencia

- `python -m py_compile runtime\eventlog.py examples\event_auth_runtime_override_cases\run_event_auth_runtime_override_cases.py` PASS.
- `python examples\event_auth_runtime_override_cases\run_event_auth_runtime_override_cases.py` PASS 6/6.
- `python examples\runtime_event_auth_cases\run_runtime_event_auth_cases.py` PASS 5/5.
- `python examples\actor_auth_ed25519_cases\run_actor_auth_ed25519_cases.py` PASS 6/6.
- `python examples\event_auth_secret_resolution_cases\run_event_auth_secret_resolution_cases.py` PASS 8/8.
- `python examples\replay_secret_independent_cases\run_replay_secret_independent_cases.py` PASS 3/3.
- `python scripts\scan_encoding.py --root .` PASS.
- `python scripts\scan_domain_neutrality.py --root .` PASS.
- `python scripts\validate_collaboration_state.py --root .` PASS con warning preexistente de context_refs en
  `MSG-20260627-Codex-to-Arquitecto-TASK-0193-in-review.md`.
- `powershell -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1` PASS con el mismo warning.
- `git diff --check` PASS.
- Drift/#4 byte-identica antes de entrega: `has_drift=false`, `up_to_seq=2203`.
- `git diff -- protocol.config.json protocol.config.template.json runtime\state\chain.genesis.json runtime\state\genesis.json` sin cambios.

## Notas de revision

- No se commiteo `event-state.runtime.json` ni ningun secreto; `.gitignore` ya cubre `event-state.runtime.json` y
  `secrets/`.
- El golden cubre alta de Analista por override con `event_auth` HMAC + `actor_auth` Ed25519, rollback quitando la
  entrada `event_auth.keys.Analista`, replay sin secretos y fail-closed de override malformado.
