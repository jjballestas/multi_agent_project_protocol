---
handoff_id: HANDOFF-TASK-0069-codex-to-claude-1
task_id: TASK-0069
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-07
---

# TASK-0069 - Fase B.4 genesis-ref + runtime autoritativo apagado

## Resumen

Implementada B.4 de SPEC-0055 y DECISION-0022: el runtime puede preparar una migracion a escritor
autoritativo mediante genesis por referencia verificable. La instancia viva queda apagada:
`event_state.enabled=false`, `event_state.materialize=false`, `event_state.enforce=false` y
`event_state.authoritative=false`.

## Cambios principales

- `runtime/protocol_replay.py`
  - `PROTOCOL_SNAPSHOT_SCHEMA_VERSION` y snapshots content-addressed en
    `runtime/state/snapshots/<hash>.json`.
  - `write_genesis_reference(...)`: exige `actor_id` y `timestamp` provisto, escribe snapshot y emite
    `protocol.genesis` con payload solo `{ "snapshot_ref": ... }`.
  - `load_snapshot_ref(...)`: verifica hash sha256, existencia, schema y contenido antes de hidratar.
  - `prepare_authoritative_migration(...)`: helper de migracion asistida, sin activar flags.
  - `protocol_authoritative_enabled(...)`: true solo con enabled+materialize+enforce+authoritative y tier runtime.
  - Replay/materialization pasan `root` para poder resolver `snapshot_ref`; genesis embebido B.1/B.2 sigue compatible.
- `protocol.config.json` y `protocol.config.template.json`
  - Agregado `event_state.authoritative:false`.
- `scripts/validate_collaboration_state.py`
  - Errores de integridad de snapshot-ref se reportan como fallo legible del drift check.
  - La paridad PowerShell queda por delegacion a Python.
- Docs
  - `README_INSTANCIACION.md`, `Area_comun/protocol/N_AGENT_RUNTIME.md`, `AGENTS.md`,
    `AGENTS.template.md` y `Area_comun/protocol/TASK_PROTOCOL.md` documentan modo autoritativo,
    genesis por referencia, prohibicion via hard-gate B.3 y rollback por flags.
- CI
  - Agregada suite `runtime_protocol_genesis_ref_cases`.

## Golden nuevo

`examples/runtime_protocol_genesis_ref_cases/run_runtime_protocol_genesis_ref_cases.py` cubre:

1. Genesis-ref escribe snapshot y evento sin blob de estado.
2. Round-trip genesis-ref -> replay -> materialize == estado canonico.
3. Snapshot faltante o manipulado bloquea replay por integridad.
4. Validador py/ps reporta errores de snapshot-ref.
5. `authoritative` on + edicion manual simulada => hard-fail B.3.
6. Modo off y coordination-tier conservan flujo manual.
7. Rollback por flags tras operar via intent runtime.
8. Determinismo de metadata provista e idempotencia.
9. Regresion B.1/B.2/B.3.

## Verificacion ejecutada

- `python examples/runtime_protocol_genesis_ref_cases/run_runtime_protocol_genesis_ref_cases.py`
- `python examples/runtime_protocol_replay_cases/run_runtime_protocol_replay_cases.py`
- `python examples/runtime_protocol_materialize_cases/run_runtime_protocol_materialize_cases.py`
- `python examples/runtime_protocol_enforce_cases/run_runtime_protocol_enforce_cases.py`
- Todas las suites `examples/runtime_*_cases` con runner Python: OK.
- `python examples/runtime_turn_cases/run_runtime_turn_semantic_cases.py`
- `python scripts/validate_collaboration_state.py --root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_collaboration_state.ps1 -Root .`
- `python scripts/scan_encoding.py --root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_encoding.ps1 -Root .`
- `python scripts/scan_domain_neutrality.py --root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_domain_neutrality.ps1 -Root .`
- `python scripts/prune_state.py --root . --check`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/prune_state.ps1 -Root . -Check`
- `python -m compileall runtime examples/runtime_protocol_genesis_ref_cases scripts/validate_collaboration_state.py`
- `git diff --check` (solo avisos CRLF de Windows, sin whitespace errors)

## Fuera de alcance respetado

- No se activa `event_state.authoritative`, `event_state.enforce`, `event_state.materialize` ni
  `event_state.enabled` en la instancia viva.
- No se retira el flujo manual de forma permanente.
- No se cambia el contrato del turn schema.
- Coordination-tier queda intacto.

## Riesgos residuales

- Activar el modo en vivo sigue siendo una operacion separada del operador: requiere aprobacion,
  validacion replay/materializacion y plan de rollback operativo sobre la instancia real.
- `write_genesis_reference` usa `commit` provisto para determinismo; si se omite, resuelve `git rev-parse HEAD`
  o usa `unknown`.
