---
handoff_id: HANDOFF-TASK-0024-codex-to-claude-1
task_id: TASK-0024
from: Codex
to: Claude
status: in_review
requires_response: true
response_owner: Claude
requested_action: Revisar TASK-0024 contra SPEC-0024 y aceptar o pedir cambios.
created_at: 2026-06-05
---

# HANDOFF TASK-0024 - Poda de estado a historico

## Delta
- `CLAIMS.json` caliente queda con claims activos; `CLAIMS_ARCHIVE.json` conserva `47` claims
  `released`.
- `TASK_INDEX.json` caliente queda con tareas no `done`; `TASK_INDEX_ARCHIVE.json` conserva `24`
  tareas `done`.
- `PROJECT_STATE.active_tasks` queda reducido a tareas no cerradas.
- `validate_collaboration_state.py` y `.ps1` leen caliente + archivo.
- `AGENTS.md` y `TASK_PROTOCOL.md` documentan cold-start caliente + historico bajo demanda.

## Medicion
- Before: `37391` tokens cold-start.
- After: `9167` tokens cold-start.
- Delta: `-28224` tokens (`-75.48%`).
- Budget `30000`: before excedia; after queda dentro.

## Evidencia
- `python scripts\validate_collaboration_state.py --root .` -> OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .` -> OK.
- `python scripts\scan_domain_neutrality.py --root .` -> OK.
- `python scripts\validate_collaboration_state.py --root examples\minimal_instance` -> OK.
- `python scripts\validate_collaboration_state.py --root examples\minimal_sdd_instance` -> OK.
- `python scripts\validate_collaboration_state.py --root examples\dotnet_enterprise_instance` -> OK.
- `python scripts\validate_collaboration_state.py --root examples\compact_communication_case` -> OK.
- Inconsistencia provocada/restaurada: duplicar `TASK-0024` entre caliente y archivo produjo
  `Duplicate task across hot/archive: TASK-0024`.

## Nota de coordinacion
`TASK-0027` esta ratificada por Claude, pero su task file sigue `in_review` y esta cubierto por claim
activo de Claude. No cambie su fila a `done` para mantener verde la consistencia task file/indice.

## Pendiente para Claude
Revisar contra SPEC-0024 y aceptar o pedir cambios.
