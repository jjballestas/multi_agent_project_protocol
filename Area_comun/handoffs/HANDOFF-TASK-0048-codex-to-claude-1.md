---
handoff_id: HANDOFF-TASK-0048-codex-to-claude-1
task_id: TASK-0048
from: Codex
to: Claude
status: in_review
created_at: 2026-06-06
requires_response: true
response_owner: Claude
requested_action: Revisar TASK-0048 contra SPEC-0039/DECISION-0017 y aceptar o devolver hallazgos concretos.
---

# TASK-0048 - Handoff de review

## Resumen

Implementada la Fase A de SPEC-0039 / DECISION-0017:

- `runtime/apply.py` ahora envuelve los turnos runtime con event log del control-plane:
  - preflight de `assert_snapshot_matches` si `runtime/state` existe;
  - emision de `EventWriter.acquire_claim` y `EventWriter.apply_intent`;
  - escritura de snapshot;
  - gate de snapshot antes de commitear;
  - inclusion de `runtime/state/` en el commit exitoso;
  - restauracion de `runtime/state` y bloqueo de tarea si hay mismatch/gate rojo/fallo de commit.
- `runtime/eventlog.py` expone `STATE_DIR` y `runtime_state_has_content`.
- `runtime/orchestrator.py` registra en el run log los eventos emitidos (`seq`, `type`, `aggregate_id`).
- `scripts/validate_collaboration_state.py` y `.ps1` ejecutan `assert_snapshot_matches` solo cuando
  `runtime/state/` existe y contiene archivos.
- Nuevo golden `examples/runtime_eventlog_gate_cases/run_runtime_eventlog_gate_cases.py` con 5 casos:
  commit con eventlog/snapshot, run log del orquestador, mismatch que bloquea sin commit, fallback sin
  `runtime/state`, y deteccion py/ps1 de mismatch.
- `.github/workflows/validate.yml` incluye el runner nuevo.

No implementado: Fase B (replay/materializacion del estado de protocolo, genesis snapshot, warning->hard-fail).

## Validacion ejecutada

- Runtime suites: 66/66 verdes.
  - router 10/10
  - eventlog 5/5
  - eventlog gate 5/5
  - review_qa 9/9
  - agent_registry 4/4
  - turn schema 5/5
  - turn semantic 5/5
  - apply 4/4
  - loop 8/8
  - observability 5/5
  - llm adapter 6/6
- `python scripts/validate_collaboration_state.py --root .`
- `python scripts/validate_collaboration_state.py --root examples/minimal_instance`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_collaboration_state.ps1 -Root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/validate_collaboration_state.ps1 -Root examples/minimal_instance`
- `python scripts/scan_encoding.py --root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_encoding.ps1 -Root .`
- `python scripts/scan_domain_neutrality.py --root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts/scan_domain_neutrality.ps1 -Root .`
- `python examples/encoding_gate_cases/run_encoding_gate_cases.py`
- `python examples/handoff_release_cases/run_handoff_release_cases.py`
- `python examples/mailbox_status_cases/run_mailbox_status_cases.py`
- `python scripts/prune_state.py --root . --check`
- `powershell -NoProfile -ExecutionPolicy Bypass -File examples/sdd_validation_cases/run_sdd_cases.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File examples/compact_comms_validation_cases/run_compact_comms_cases.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File examples/neutrality_scan_cases/run_neutrality_scan_cases.ps1`
- `powershell -NoProfile -ExecutionPolicy Bypass -File examples/neutrality_scan_cases/run_neutrality_scan_cases.ps1`
- workflow YAML parse OK.
- `git diff --check` OK; solo warnings CRLF esperados.

## Notas de review

- El fallback se mantiene: si `runtime/state/` no existe o no contiene archivos, el validador global se
  comporta como antes.
- El gate no cura snapshots inconsistentes: si ya hay mismatch antes del turno, `apply_gate_and_commit`
  aborta antes de mutar el estado de protocolo y deja la tarea en `blocked`.
- El event log se restaura desde backup si el turno no llega a commit, evitando `runtime/state` a medias.
