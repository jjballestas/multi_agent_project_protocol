---
handoff_id: HANDOFF-TASK-0017-codex-to-claude-1
task_id: TASK-0017
spec_id: Area_comun/specs/SPEC-0017-ci-completo-scan-neutralidad.md
from: Codex
to: Claude
date: 2026-06-05
status: for_review
requires_response: no
response_owner: Claude
acceptance_criteria_verified: yes
tests_run:
  - python scripts\validate_collaboration_state.py --root .
  - python scripts\validate_collaboration_state.py --root examples\minimal_instance
  - powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .
  - powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root examples\minimal_instance
  - powershell -NoProfile -ExecutionPolicy Bypass -File examples\sdd_validation_cases\run_sdd_cases.ps1
  - powershell -NoProfile -ExecutionPolicy Bypass -File examples\compact_comms_validation_cases\run_compact_comms_cases.ps1
  - powershell -NoProfile -ExecutionPolicy Bypass -File examples\neutrality_scan_cases\run_neutrality_scan_cases.ps1
  - python scripts\scan_domain_neutrality.py --root .
  - powershell -NoProfile -ExecutionPolicy Bypass -File scripts\scan_domain_neutrality.ps1 -Root .
spec_deviations:
  - none
decisions_referenced:
  - DECISION-0006
  - DECISION-0001
---

# Handoff: TASK-0017 CI completo y scan de neutralidad

## 1. Minimal Context
Implementacion de `SPEC-0017`: CI ahora cubre validadores Python/PowerShell, harness SDD, harness de comunicacion compacta y scan de neutralidad. Se anade scan configurable `.py/.ps1` con golden cases y paridad.

## 2. What Was Done
- `.github/workflows/validate.yml`: agrega validador `.ps1` para dogfood y `minimal_instance`, ambos harness existentes, harness de neutralidad y scan `.py/.ps1`.
- `scripts/scan_domain_neutrality.py`: scan configurable por `domain_neutrality`.
- `scripts/scan_domain_neutrality.ps1`: espejo con mismos mensajes/exits.
- `protocol.config.json`: activa scan dogfood con denylist del piloto y superficie neutral.
- `protocol.config.template.json`: agrega bloque configurable con denylist vacia.
- `examples/neutrality_scan_cases/`: fixture limpio, fixture con hallazgo y harness de paridad.

## 3. What Was Not Done
No se cambio la logica de `validate_collaboration_state.*`. No se escanean perfiles concretos, ejemplos ni area viva dogfood fuera de la superficie neutral definida.

## 4. Acceptance Criteria Verified
| Criterion | Evidence | Status |
|-----------|----------|--------|
| CI ejecuta validate.py x2, validate.ps1 x2, harness SDD, harness compacto y scan | `.github/workflows/validate.yml` contiene todos los pasos | met |
| Scan falla ante termino de denylist y pasa sobre repo actual | `run_neutrality_scan_cases.ps1` OK; scans directos sobre repo exit 0 | met |
| Paridad `.py`/`.ps1` del scan | Harness compara exit y salida normalizada para fixtures limpio y con hallazgo | met |
| Configurable y aditivo | `domain_neutrality` en configs; pruebas con config ausente y `enabled:false` salen 0 | met |
| Core neutral intacto | `scan_domain_neutrality.py --root .` y `.ps1 -Root .` salen 0 | met |

## 5. Tests Run
Ver `tests_run` en frontmatter. Adicionalmente:
- Config ausente en temp dir: scan `.py/.ps1` exit 0.
- `enabled:false` con termino denylisted en temp dir: scan `.py/.ps1` exit 0.

## 6. Spec Deviations
none

## 7. Requested Action
Claude: revisar contra `SPEC-0017` y aceptar/cerrar `TASK-0017` si la cobertura CI + scan es suficiente.

## 8. Risks and Assumptions
El workflow no se ejecuto en GitHub Actions desde esta sesion; se verificaron localmente los mismos comandos. En CI se usa `shell: pwsh` para los pasos PowerShell.

## 9. Open Questions / BLOCKED
Ninguna.

## 10. Pointers
- Task: `Area_comun/tasks/TASK-0017-codex-ci-completo-scan-neutralidad.md`
- Spec: `Area_comun/specs/SPEC-0017-ci-completo-scan-neutralidad.md`
- Deliverables: `.github/workflows/validate.yml`, `scripts/scan_domain_neutrality.py`, `scripts/scan_domain_neutrality.ps1`, `protocol.config*.json`, `examples/neutrality_scan_cases/`
