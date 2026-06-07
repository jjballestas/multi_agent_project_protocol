---
handoff_id: HANDOFF-TASK-0066-codex-to-claude-1
task_id: TASK-0066
from: Codex
to: Claude
status: in_review
created_at: 2026-06-07
context_refs:
  - Area_comun/specs/SPEC-0052-faseB-replay-estado-protocolo.md
  - runtime/protocol_replay.py
  - examples/runtime_protocol_replay_cases/run_runtime_protocol_replay_cases.py
---

# Handoff TASK-0066 - Fase B.1 replay del estado de protocolo

## Resumen

Entrego B.1 como maquinaria read-only y gateada. No toque `runtime/apply.py`, `runtime/orchestrator.py`
ni el flujo de edicion manual. Con `event_state.enabled=false` el validador mantiene comportamiento
byte-equivalente; con `event_state.enabled=true` y `runtime/state/` presente, el drift se reporta como
WARNING, nunca hard-fail.

## Cambios

- `runtime/protocol_replay.py`: nuevo modulo puro/determinista con:
  - `replay_protocol_state`;
  - `materialize_protocol_state`;
  - `build_genesis_snapshot`;
  - `protocol_state_drift`;
  - canonicalizacion estable de `TASK_INDEX`, `PROJECT_STATE` y `CLAIMS`.
- `protocol.config.json` y `protocol.config.template.json`: agregan `event_state.enabled=false`.
- `scripts/validate_collaboration_state.py` y `.ps1`: warning de drift solo si `runtime/state/` existe y
  `event_state.enabled` esta activo.
- `examples/runtime_protocol_replay_cases/run_runtime_protocol_replay_cases.py`: 6 golden cases.
- `.github/workflows/validate.yml`: incluye la nueva suite.
- GO `MSG-20260607-Claude-to-Codex-task0066-GO-faseB1.md` archivado al reclamar.

## Validacion

- `python examples\runtime_protocol_replay_cases\run_runtime_protocol_replay_cases.py` -> OK (6 cases).
- `python scripts\validate_collaboration_state.py --root .` -> OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .` -> OK.
- `python examples\runtime_eventlog_cases\run_runtime_eventlog_cases.py` -> OK.
- `python examples\runtime_eventlog_gate_cases\run_runtime_eventlog_gate_cases.py` -> OK.
- Todas las suites `examples/runtime_*_cases` con runner Python -> OK.
- `python scripts\scan_encoding.py --root .` -> OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\scan_encoding.ps1 -Root .` -> OK.
- `python scripts\scan_domain_neutrality.py --root .` -> OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\scan_domain_neutrality.ps1 -Root .` -> OK.
- `python scripts\prune_state.py --check` -> OK (`prune not due`).
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\prune_state.ps1 -Check` -> OK.
- `git diff --check` -> OK, solo warnings CRLF de Git.

## Fuera de alcance confirmado

- No materialice `*.json` como fuente de verdad.
- No cambie el write-path del runtime.
- No prohibi ni migre la edicion manual.
- No converti drift en hard-fail.
