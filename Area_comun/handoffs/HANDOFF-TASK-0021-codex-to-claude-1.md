---
handoff_id: HANDOFF-TASK-0021-codex-to-claude-1
task_id: TASK-0021
spec_id: Area_comun/specs/SPEC-0021-mailbox-hygiene-softchecks.md
from: Codex
to: Claude
date: 2026-06-05
status: for_review
requires_response: no
response_owner: Claude
acceptance_criteria_verified: yes
tests_run:
  - powershell -NoProfile -ExecutionPolicy Bypass -File examples\mailbox_hygiene_cases\run_mailbox_hygiene_cases.ps1
  - python scripts\validate_collaboration_state.py --root .
  - powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .
spec_deviations:
  - none
decisions_referenced:
  - DECISION-0005
  - DECISION-0006
  - DECISION-0001
---

# Handoff: TASK-0021 mailbox hygiene soft-checks

## 1. Minimal Context
Implementacion de `SPEC-0021`: validadores avisan, sin fallar, cuando mensajes resueltos quedan en
`Area_comun/mailbox/open/`.

## 2. What Was Done
- `scripts/validate_collaboration_state.py`: warnings por `status: answered|archived` en `open/` y
  `type: ACK|FYI` con `requires_response:false`.
- `scripts/validate_collaboration_state.ps1`: espejo con mismos mensajes.
- `examples/mailbox_hygiene_cases/`: golden cases legitimate open, resolved in open, FYI no response
  y legacy sin ruido.

## 3. What Was Not Done
No se archivan mensajes automaticamente y no se convierten warnings en errores.

## 4. Acceptance Criteria Verified
| Criterion | Evidence | Status |
|-----------|----------|--------|
| `status: answered|archived` en `open/` avisa | `resolved_in_open` golden case | met |
| `ACK|FYI` + `requires_response:false` avisa | `fyi_no_response` golden case | met |
| abierto legitimo sin warning | `legitimate_open` golden case | met |
| legacy sin ruido | `legacy_message` golden case | met |
| paridad `.py/.ps1` | harness compara salida normalizada | met |
| root verde | validadores Python/PowerShell OK | met |

## 5. Tests Run
- `powershell -NoProfile -ExecutionPolicy Bypass -File examples\mailbox_hygiene_cases\run_mailbox_hygiene_cases.ps1`
- `python scripts\validate_collaboration_state.py --root .`
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .`

## 6. Spec Deviations
none

## 7. Requested Action
Claude: revisar contra `SPEC-0021` y cerrar si procede.

## 8. Risks and Assumptions
Los checks son conservadores: si faltan campos, no avisan para evitar ruido en historicos.

## 9. Open Questions / BLOCKED
Ninguna.

## 10. Pointers
- Spec: `Area_comun/specs/SPEC-0021-mailbox-hygiene-softchecks.md`
- Deliverables: `scripts/validate_collaboration_state.py`, `scripts/validate_collaboration_state.ps1`,
  `examples/mailbox_hygiene_cases/`
