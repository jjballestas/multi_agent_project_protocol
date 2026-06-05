---
handoff_id: HANDOFF-TASK-0020-codex-to-claude-1
task_id: TASK-0020
spec_id: none
from: Codex
to: Claude
date: 2026-06-05
status: for_review
requires_response: no
response_owner: Claude
acceptance_criteria_verified: yes
tests_run:
  - python scripts\validate_collaboration_state.py --root .
  - powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .
spec_deviations:
  - none
decisions_referenced:
  - DECISION-0007
  - DECISION-0005
---

# Handoff: TASK-0020 claim-before-shared-draft

## 1. Minimal Context
El operador humano pidio formalizar la regla detectada durante la coordinacion de TASK-0019:
claim activo antes de crear o editar cualquier borrador en rutas compartidas.

## 2. What Was Done
- `Area_comun/decisions/DECISION-0007-claim-before-shared-draft.md`: decision append-only.
- `AGENTS.md` y `AGENTS.template.md`: regla visible en el contrato principal.
- `Area_comun/README.md` y `Area_comun/README.template.md`: regla visible en la entrada compartida.
- `Area_comun/protocol/TASK_PROTOCOL.md`: regla operativa en Claiming Work.
- `Area_comun/protocol/COMMUNICATION_PROTOCOL.md`: regla y tratamiento de trabajo no reclamado.
- `Area_comun/tasks/TASK-0020-codex-claim-before-shared-draft.md`: microtarea auditable.

## 3. What Was Not Done
No se implemento enforcement automatico en validadores; queda como regla procedimental.

## 4. Acceptance Criteria Verified
| Criterion | Evidence | Status |
|-----------|----------|--------|
| Decision registrada | `DECISION-0007` creada | met |
| Regla visible para agentes entrando en frio | `AGENTS.md`, `Area_comun/README.md`, protocolos y templates actualizados | met |
| Estado valido | Validadores Python/PowerShell verdes | met |
| Sin cambio incompatible | Regla aditiva; no invalida historico | met |

## 5. Tests Run
- `python scripts\validate_collaboration_state.py --root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .`

## 6. Spec Deviations
none

## 7. Requested Action
Claude: revisar y aceptar/cerrar TASK-0020 si la regla queda suficientemente clara.

## 8. Risks and Assumptions
La regla depende de disciplina de agentes hasta que exista un validador de claims/rutas mas estricto.

## 9. Open Questions / BLOCKED
Ninguna.

## 10. Pointers
- Decision: `Area_comun/decisions/DECISION-0007-claim-before-shared-draft.md`
- Task: `Area_comun/tasks/TASK-0020-codex-claim-before-shared-draft.md`
