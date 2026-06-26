---
handoff_id: HANDOFF-TASK-0190-codex-to-arquitecto-1
task_id: TASK-0190
from: Codex
to: Arquitecto
status: in_review
requires_response: false
created_at: 2026-06-27
changed_refs:
  - runtime/eventlog.py
  - scripts/validate_collaboration_state.py
  - examples/actor_auth_ed25519_cases/run_actor_auth_ed25519_cases.py
  - .github/workflows/validate.yml
  - protocol.config.template.json
  - Area_comun/tasks/TASK-0190-codex-actor-auth-ed25519-submit-intent.md
  - Area_comun/state/TASK_INDEX.json
  - Area_comun/state/CLAIMS.json
---

# HANDOFF TASK-0190 - Codex -> Arquitecto

## Resultado

TASK-0190 queda implementada y lista para review. Commit de implementacion:

- `d8bb869 feat(runtime): add actor auth ed25519`

El camino OFF conserva `actor_auth.method=not_enforced_phase2` y no modifica `protocol.config.json` ni genesis. El
flag nuevo queda documentado en `protocol.config.template.json` como `event_state.actor_auth_enforce: false`; si falta,
se interpreta como OFF.

## Cambios

- `runtime/eventlog.py`: agrega `actor_auth_enforce`, resolucion path-safe de privadas Ed25519 fuera del repo, firma
  fail-closed con la privada del actor, verificacion con publicas de `event_state.signature_config.public_keys`, y
  rechazo en replay de firma invalida / keyid no registrado / atribucion cruzada.
- `scripts/validate_collaboration_state.py`: valida `actor_auth` en el event log; acepta `not_enforced_phase2` y falla
  ante `ed25519` invalido.
- `examples/actor_auth_ed25519_cases/run_actor_auth_ed25519_cases.py`: golden permanente para AC1-AC4: firma ON,
  OFF byte-identico, atribucion cruzada rechazada, verificacion sin secretos y firma sin privada fail-closed.
- `.github/workflows/validate.yml`: ejecuta el golden nuevo en CI.

## Evidencia

- `python -m py_compile runtime/eventlog.py scripts/validate_collaboration_state.py examples/actor_auth_ed25519_cases/run_actor_auth_ed25519_cases.py` OK.
- `python examples/actor_auth_ed25519_cases/run_actor_auth_ed25519_cases.py` OK: 5/5.
- `python scripts/scan_encoding.py --root .` OK.
- `python scripts/scan_domain_neutrality.py --root .` OK.
- `python scripts/validate_collaboration_state.py --root .` OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_collaboration_state.ps1 -Root .` OK.
- Clean clone without repo secrets: `python scripts/validate_collaboration_state.py --root <clone>` OK.
- Clean clone golden: `python examples/actor_auth_ed25519_cases/run_actor_auth_ed25519_cases.py` OK.
- Drift before delivery: `has_drift=false`, `up_to_seq=2131`.
- After delivery claim: `has_drift=false`, `up_to_seq=2132`.

## Review foco

- Verificar que `actor_auth_message` cubre el evento sin `actor_auth/event_auth/prev_hash`, evitando circularidad con
  chain/HMAC y manteniendo actor/aggregate/payload/seq/timestamp firmados.
- Confirmar que la activacion viva queda fuera de alcance: `protocol.config.json` no fue modificado y no se enciende
  `actor_auth_enforce` en esta entrega.
