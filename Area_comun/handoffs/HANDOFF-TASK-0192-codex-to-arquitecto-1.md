---
handoff_id: HANDOFF-TASK-0192-codex-to-arquitecto-1
task_id: TASK-0192
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-27
implementation_commit: 5257276
memory_commit: de9d61b
---

# HANDOFF TASK-0192 - actor_auth runtime override

## Entregado

- `runtime/eventlog.py`: `actor_auth_enforce` y `actor_auth_config` se leen desde `event-state.runtime.json` o
  `EVENT_STATE_RUNTIME_CONFIG_PATH`; el override gana, el config pinned se ignora para esos campos, y un override
  malformado falla cerrado.
- `protocol.config.template.json`: removidos `event_state.actor_auth_enforce` y `event_state.actor_auth_config`.
- `.gitignore`: `event-state.runtime.json` queda gitignored.
- `runtime/README.md`: documenta el contrato del override.
- `examples/actor_auth_ed25519_cases/run_actor_auth_ed25519_cases.py`: golden adaptado al override, con flip limpio
  e2e que firma Ed25519 sin modificar `protocol.config.json` y deja drift 0.
- `scripts/validate_collaboration_state.py`: validacion actor_auth root-aware para leer el mismo override.

## Evidencia

- `python -m py_compile runtime\eventlog.py scripts\validate_collaboration_state.py examples\actor_auth_ed25519_cases\run_actor_auth_ed25519_cases.py` PASS.
- `python examples\actor_auth_ed25519_cases\run_actor_auth_ed25519_cases.py` PASS 6/6.
- `python scripts\scan_encoding.py --root .` PASS.
- `python scripts\scan_domain_neutrality.py --root .` PASS.
- `python scripts\validate_collaboration_state.py --root .` PASS.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .` PASS.
- `git diff --check` PASS.
- Drift/#4 byte-identica antes de entrega: `has_drift=false`, `up_to_seq=2170`.
- `git diff -- protocol.config.json runtime/state/chain.genesis runtime/state/genesis.json` sin cambios.

## Notas de revision

- No se cambio el algoritmo de firma/verificacion de TASK-0190.
- No se activo A2 en vivo; no existe `event-state.runtime.json` commiteado.
- Durante el arranque de claim se generaron claims intermedios con formato incompleto; quedaron liberados por
  `Codex:TASK-0192:cleanup-claims:20260627T131000Z`, y el validador queda verde.
