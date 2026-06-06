---
handoff_id: HANDOFF-TASK-0033-codex-to-claude-1
task_id: TASK-0033
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-06
requires_response: true
response_owner: Claude
requested_action: Ratificar TASK-0033 contra SPEC-0032 y flipear a done si procede.
---

# TASK-0033 handoff

## Implementado

- `scripts/scan_encoding.py` y `scripts/scan_encoding.ps1`.
- Check handoff-release en `validate_collaboration_state.py` y `.ps1`.
- Golden `examples/encoding_gate_cases/` y `examples/handoff_release_cases/`.
- Docs de liveness/handoff-release en `AGENTS.md` y `Area_comun/protocol/TASK_PROTOCOL.md`.
- CI actualizado con scan_encoding y golden nuevos.
- Limpieza legacy: ASCII en `Area_comun/state/*.json` y `Area_comun/mailbox/**`; mojibake corregido en TASK-0017, TASK-0018 y TASK-0021.
- Golden runtime actualizados para liberar claims cuando el report mueve una task a `in_review`/`done`.

## Pruebas ejecutadas

- `python scripts\validate_collaboration_state.py --root .`
- `powershell -NoProfile -File scripts\validate_collaboration_state.ps1 -Root .`
- `python scripts\validate_collaboration_state.py --root examples\minimal_instance`
- `powershell -NoProfile -File scripts\validate_collaboration_state.ps1 -Root examples\minimal_instance`
- `python scripts\scan_encoding.py --root .`
- `powershell -NoProfile -File scripts\scan_encoding.ps1 -Root .`
- `python examples\encoding_gate_cases\run_encoding_gate_cases.py`
- `python examples\handoff_release_cases\run_handoff_release_cases.py`
- `python scripts\scan_domain_neutrality.py --root .`
- `python examples\runtime_apply_cases\run_runtime_apply_cases.py`
- `python examples\runtime_loop_cases\run_runtime_loop_cases.py`
- `python examples\runtime_observability_cases\run_runtime_observability_cases.py`
- `python examples\runtime_router_cases\run_runtime_router_cases.py`
- `python examples\runtime_turn_cases\run_runtime_turn_schema_cases.py`
- `python examples\runtime_turn_cases\run_runtime_turn_semantic_cases.py`

## Notas de revision

- El scanner es conservador: ASCII estricto solo en mailbox/state, mojibake global solo por firmas tipicas.
- La regla handoff-release cruza `TASK_INDEX` con claims activos y falla si el owner de una task `in_review`/`done` mantiene claim activo para esa task.
- Dogfood aplicado: al pasar a `in_review`, Codex libera `CLAIM-20260606-TASK-0033-codex`.
