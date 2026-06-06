---
handoff_id: HANDOFF-TASK-0034-codex-to-claude-1
task_id: TASK-0034
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-06
requires_response: true
response_owner: Claude
requested_action: Ratificar TASK-0034 contra SPEC-0033 y flipear a done si procede.
---

# TASK-0034 handoff

## Implementado

- `scripts/prune_state.py` con `--check` read-only y `--apply` idempotente.
- `scripts/prune_state.ps1` como wrapper con paridad de exit codes.
- Bloque `maintenance` en `protocol.config.json` y `protocol.config.template.json`.
- Hook bloqueante `.githooks/pre-commit` (no muta ni re-stagea).
- Paso CI `Check systematic state pruning`.
- Golden `examples/prune_state_cases/`.
- Poda real aplicada al repo vivo.

## Resultado de poda real

- Antes: `20701` cold-start tokens.
- Despues: `8881` cold-start tokens en la ejecucion inmediata de `--apply`.
- Recuperado: `11820` tokens.
- Tareas archivadas: `7`.
- Claims archivados: `20`.
- Entradas `PROJECT_STATE.active_tasks` removidas: `7`.
- Mensajes movidos `answered -> archived`: `40`.

Tras ajustar scope del claim, la medicion final quedo en `8959` tokens y `prune_state --check` queda verde.

## Pruebas ejecutadas

- `python examples\prune_state_cases\run_prune_state_cases.py`
- `python scripts\prune_state.py --root . --check`
- `powershell -NoProfile -File scripts\prune_state.ps1 -Root . -Check`
- `python scripts\validate_collaboration_state.py --root .`
- `powershell -NoProfile -File scripts\validate_collaboration_state.ps1 -Root .`
- `python scripts\scan_encoding.py --root .`
- `python scripts\scan_domain_neutrality.py --root .`
- `python examples\runtime_router_cases\run_runtime_router_cases.py`
- `python examples\runtime_apply_cases\run_runtime_apply_cases.py`

## Notas

- `--check` fallo antes de aplicar poda por: cold-start `20701 >= 20000`, done `90 >= 85`, released `96 >= 90`.
- `--check` pasa despues de aplicar poda: cold-start `8959`.
- Archive != delete: tareas/claims terminales se mueven a `*_ARCHIVE.json`; mailbox resuelto se mueve a `archived`.
- Dogfood: este WIP se commitea antes de liberar el claim; el cierre a `in_review` libera el claim.
