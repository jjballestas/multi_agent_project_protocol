---
handoff_id: HANDOFF-TASK-0068-codex-to-claude-1
task_id: TASK-0068
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-07
---

# TASK-0068 - Fase B.3 drift hard-fail

## Resumen

Implementada B.3 de SPEC-0054: el drift del estado de protocolo pasa de warning a hard-fail solo bajo
`event_state.enabled && event_state.enforce && adoption_tier=runtime && runtime/state con contenido`.

La instancia viva queda con `event_state.enforce=false` en `protocol.config.json` y
`protocol.config.template.json`.

## Cambios principales

- `runtime/protocol_replay.py`
  - `event_state_enforce_enabled`, `protocol_state_enforcement_enabled`.
  - `ProtocolStateDriftError`, `drift_paths`, `enforce_protocol_state_drift`.
  - `protocol_state_drift` ahora reporta `enforced`.
  - `intent.applied` puede replayar un `task` completo para cubrir mutaciones internas como `original_author`.
- `scripts/validate_collaboration_state.py`
  - Con enforce activo y drift: `validation.fail(...)` hard-fail B.3 con paths y sugerencia de reconciliacion.
  - Con enforce off: mantiene warning-only B.1.
- `scripts/validate_collaboration_state.ps1`
  - Paridad con Python usando `drift.enforced`.
- `runtime/apply.py`
  - Despues de `apply_turn` + eventlog + materializacion opt-in, corre `enforce_protocol_state_drift` antes de
    `run_gate` y antes del commit.
  - Si hay drift enforceado: `discard_worktree_changes`, restaura `runtime/state`, bloquea la tarea y no commitea.
  - `intent.applied` incluye el task hot completo cuando existe `TASK_INDEX.json`; si no existe, conserva el
    comportamiento de fixtures N-agent/observabilidad.
- `.github/workflows/validate.yml`
  - Agregada suite `runtime_protocol_enforce_cases`.

## Golden nuevo

`examples/runtime_protocol_enforce_cases/run_runtime_protocol_enforce_cases.py` cubre:

1. `enforce=true` + drift => validador py/ps hard-fail con paths.
2. `enforce=true` + estado coherente => validador pasa.
3. `enforce=false`, sin `runtime/state`, o tier no runtime => warning-only/no hard-fail.
4. `apply` aborta commit ante drift enforceado, restaura runtime log y bloquea la tarea.
5. `apply` commitea cuando el estado enforceado es coherente.
6. Tier `coordination` no fuerza enforce.
7. Regresion B.1/B.2.

## Verificacion ejecutada

- `python examples/runtime_protocol_enforce_cases/run_runtime_protocol_enforce_cases.py`
- `python examples/runtime_protocol_replay_cases/run_runtime_protocol_replay_cases.py`
- `python examples/runtime_protocol_materialize_cases/run_runtime_protocol_materialize_cases.py`
- `python examples/runtime_eventlog_gate_cases/run_runtime_eventlog_gate_cases.py`
- `python examples/runtime_apply_cases/run_runtime_apply_cases.py`
- `python examples/runtime_loop_cases/run_runtime_loop_cases.py`
- Todas las suites `examples/runtime_*_cases` con runner Python: OK.
- `python scripts/validate_collaboration_state.py --root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_collaboration_state.ps1 -Root .`
- `python scripts/scan_encoding.py --root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_encoding.ps1 -Root .`
- `python scripts/scan_domain_neutrality.py --root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_domain_neutrality.ps1 -Root .`
- `python scripts/prune_state.py --root . --check`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/prune_state.ps1 -Root . -Check`
- `python -m compileall runtime examples/runtime_protocol_enforce_cases`
- `git diff --check`

## Fuera de alcance respetado

- No se prohibe ni migra la edicion manual del estado (B.4 sigue pendiente).
- No se enciende `event_state.enforce` en la instancia viva.
- No se cambia el contrato del turn schema.
