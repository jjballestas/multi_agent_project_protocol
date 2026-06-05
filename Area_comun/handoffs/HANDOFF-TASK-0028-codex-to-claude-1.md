---
handoff_id: HANDOFF-TASK-0028-codex-to-claude-1
task_id: TASK-0028
from: Codex
to: Claude
status: in_review
requires_response: true
response_owner: Claude
requested_action: Revisar TASK-0028 contra SPEC-0028 y aceptar o pedir cambios.
created_at: 2026-06-05
---

# HANDOFF TASK-0028 - Claims por fila

## Delta
- `validate_collaboration_state.py` y `.ps1` parsean scopes `ruta#selector`.
- Para `TASK_INDEX.json` y `PROJECT_STATE.json`, el solape es por fila:
  - filas distintas no se solapan;
  - misma fila se solapa;
  - ruta desnuda conserva significado de archivo completo.
- Selectores mal formados fallan.
- `runtime/turn_validate.py` valida allowlist por fila y deriva filas tocadas por `task_status`.
- `runtime/context.py` lee hot + archive para que el router resuelva dependencias archivadas tras
  `TASK-0024`.

## Evidencia
- `python examples\row_scoped_claim_cases\run_row_scoped_claim_cases.py` -> OK, 5 casos con paridad PowerShell.
- `python examples\runtime_turn_cases\run_runtime_turn_semantic_cases.py` -> OK.
- `python examples\runtime_router_cases\run_runtime_router_cases.py` -> OK.
- `python runtime\orchestrator.py --plan --root .` -> selecciona `TASK-0025`.
- `python scripts\validate_collaboration_state.py --root .` -> OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .` -> OK.
- `python scripts\scan_domain_neutrality.py --root .` -> OK.
- Regresion Python verde en `examples/minimal_instance`, `minimal_sdd_instance`,
  `dotnet_enterprise_instance`, `compact_communication_case`.

## Pendiente para Claude
Revisar contra SPEC-0028 y aceptar o pedir cambios.
