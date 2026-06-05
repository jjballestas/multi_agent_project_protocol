---
handoff_id: HANDOFF-TASK-0030-codex-to-claude-1
task_id: TASK-0030
from: Codex
to: Claude
status: in_review
requires_response: true
response_owner: Claude
requested_action: Revisar TASK-0030 contra SPEC-0029 y aceptar o pedir cambios.
created_at: 2026-06-05
---

# HANDOFF TASK-0030 - Runtime M1 apply/gate

## Delta
- `runtime/vcs.py`: commit/revert helpers + write-allowlist de politica.
- `runtime/gate.py`: wrapper de validator + neutrality scan.
- `runtime/apply.py`: apply_turn validado + apply/gate/commit-or-revert.
- `examples/runtime_apply_cases/run_runtime_apply_cases.py`: golden con repo git temporal.

## Evidencia
- `python examples\runtime_apply_cases\run_runtime_apply_cases.py` -> OK, 4 casos.
- `python -m py_compile runtime\vcs.py runtime\gate.py runtime\apply.py examples\runtime_apply_cases\run_runtime_apply_cases.py` -> OK.
- `python scripts\validate_collaboration_state.py --root .` -> OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .` -> OK.
- `python scripts\scan_domain_neutrality.py --root .` -> OK.
- Runtime M0 regressions (`schema`, `semantic`, `router`) -> OK.
- Regresion Python verde en `examples/minimal_instance`, `minimal_sdd_instance`,
  `dotnet_enterprise_instance`, `compact_communication_case`.

## Nota
M1 sigue sin invocar agentes. El golden rojo revierte cambios del turno y marca la tarea `blocked`
despues del rollback.

## Pendiente para Claude
Revisar contra SPEC-0029 y aceptar o pedir cambios.
