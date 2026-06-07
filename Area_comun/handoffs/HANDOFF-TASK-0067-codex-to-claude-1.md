---
handoff_id: HANDOFF-TASK-0067-codex-to-claude-1
task_id: TASK-0067
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-07
---

# TASK-0067 - Fase B.2 materializacion opt-in

## Resumen

Implementada B.2 de SPEC-0053: el runtime puede materializar los tres `*.json` de estado de protocolo desde
`replay(log)` de forma opt-in, doble-gated por `event_state.enabled` + `event_state.materialize`, y solo con
`adoption_tier=runtime`.

La instancia viva queda con `event_state.materialize=false` en `protocol.config.json` y en
`protocol.config.template.json`.

## Cambios principales

- `runtime/protocol_replay.py`
  - `event_state_materialize_enabled`, `protocol_materialization_enabled`.
  - `write_genesis(root)`: emite un evento `protocol.genesis` idempotente desde el estado vivo y actualiza el
    snapshot runtime.
  - `materialize_to_disk(root, snapshot)`: escribe `TASK_INDEX.json`, `PROJECT_STATE.json` y `CLAIMS.json`
    canonicos, ASCII/sin BOM, con rollback ante fallo a mitad.
  - `materialize_from_event_log_if_enabled(root)`: materializa solo si `enabled && materialize && runtime`;
    si falta genesis con materializacion encendida, bloquea de forma segura en el runtime.
- `runtime/eventlog.py`
  - `EventWriter.acquire_claim(...)` acepta `claim_id` opcional para que el replay pueda reconciliar el claim
    real de protocolo y no crear uno sintetico.
- `runtime/apply.py`
  - El payload `intent.applied` incluye `transitions` completas del turn report.
  - Tras `apply_turn` + event log, invoca materializacion solo si el gate B.2 esta activo.
  - Los paths materializados se suman al commit del turno.
- `.github/workflows/validate.yml`
  - Agregada suite `runtime_protocol_materialize_cases`.

## Golden nuevo

`examples/runtime_protocol_materialize_cases/run_runtime_protocol_materialize_cases.py` cubre:

1. Escritura canonica ASCII/sin BOM de los tres state JSON.
2. Round-trip `write_genesis -> replay -> materialize` idempotente.
3. Rollback todo-o-nada ante fallo simulado a mitad.
4. Gating off byte-equivalente (`enabled=false`, `materialize=false`, tier no runtime).
5. Runtime con materializacion on: sin drift cuando el log es coherente y WARNING cuando se introduce divergencia.
6. Regresion B.1 (`runtime_protocol_replay_cases`).

## Verificacion ejecutada

- `python examples/runtime_protocol_materialize_cases/run_runtime_protocol_materialize_cases.py`
- Todas las suites `examples/runtime_*_cases` con runner Python: OK.
- `python scripts/validate_collaboration_state.py --root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_collaboration_state.ps1 -Root .`
- `python scripts/scan_encoding.py --root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_encoding.ps1 -Root .`
- `python scripts/scan_domain_neutrality.py --root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_domain_neutrality.ps1 -Root .`
- `python scripts/prune_state.py --root . --check`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/prune_state.ps1 -Root . -Check`
- `python -m compileall runtime examples/runtime_protocol_materialize_cases`
- `git diff --check`

## Fuera de alcance respetado

- No se convierte drift en hard-fail global (B.3 sigue pendiente).
- No se prohibe ni migra la edicion manual del estado (B.4 sigue pendiente).
- No se enciende `event_state.materialize` en la instancia viva.
- No se cambia el contrato del turn schema.
