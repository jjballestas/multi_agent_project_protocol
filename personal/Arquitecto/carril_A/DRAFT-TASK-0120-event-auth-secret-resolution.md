---
id: TASK-0120
title: Cargador de secreto HMAC de event_auth fuera del repo (secret_file/secret_env) - precondicion de #4 (DECISION-0043 / SPEC-0082)
type: security
status: ready
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0082
linked_decisions: [DECISION-0043, DECISION-0039, DECISION-0029]
created_at: 2026-06-19
---

# TASK-0120 - Cargador de secreto HMAC de event_auth fuera del repo

## Objective

Implementar la resolucion del secreto HMAC de `event_auth` por REFERENCIA (keyfile gitignored
`secret_file` / env `secret_env`), no por literal commiteado, cerrando la precondicion de SPEC-0081 AC1
(capa HMAC) sin meter secretos al repo. Ver SPEC-0082 para acceptance_criteria + test_plan. La privada
Ed25519 ya es wrapper-side; esta tarea NO la toca.

## Alcance (SPEC-0082)

- `runtime/eventlog.py`: `agent_auth_config`/`signing_secret`/`verify_event_auth` aceptan
  `secret_file`/`secret_env` ademas del `secret` literal (precedencia literal -> file -> env). Resolutor
  `resolve_event_auth_secret(entry, root)` que NO altera el dict de `read_protocol_config`.
- **Thread explicito de `root`** hasta `verify_event_auth` y todos sus llamadores
  (`protocol_replay.replay_events`/`rebuild_snapshot`/`EventWriter.state()`/validadores); no depender del
  `cwd` (ajuste Codex feasibility).
- **Fail-closed**: referencia presente pero irresoluble -> `sign_event` lanza error de clase
  (`unresolved_key`) antes de `atomic_append_jsonl`; verificacion -> `reason: unresolved_key`.
- **AC4 - check DEDICADO** (en el validador o script de CI): rechaza `secret` literal de actor vivo en el
  config commiteado; permite `secret_file`/`secret_env`; literal solo en fixtures bajo `examples/`. NO se
  delega en `scan_encoding`/`scan_domain_neutrality`.
- **Path-safety**: `secret_file` relativo, allowlist `SECRET_DIRS = {"secrets", ".protocol-secrets"}`;
  rechazar absoluto/traversal antes de leer.
- Golden `examples/event_auth_secret_resolution_cases/`; cablear en CI.

## DoD

SPEC-0082 AC1-AC8 cumplidos; maker!=checker (Codex implementa, Arquitecto reproduce); SemVer MINOR +
CHANGELOG; memoria actualizada. **NO enciende #4** (habilita su provisioning). #4 sigue OFF.

## Verification

- `python examples\event_auth_secret_resolution_cases\run_event_auth_secret_resolution_cases.py`
- suites #4 existentes verdes (`attestation_health_cases`, `chain_auth_combined_cases`,
  `agent_signature_cases`) byte-identicas
- `python scripts\validate_collaboration_state.py --root .` (drift 0) + `scan_encoding.py` +
  `scan_domain_neutrality.py`
