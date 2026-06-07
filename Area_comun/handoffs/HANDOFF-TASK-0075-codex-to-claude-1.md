---
handoff_id: HANDOFF-TASK-0075-codex-to-claude-1
task_id: TASK-0075
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-07
---

# Handoff TASK-0075 - F7.4 firma de releases

## Entrega

Implementada F7.4 como extension aditiva/off-by-default:

- `scripts/sign_release.py` (+ `scripts/sign_release.ps1`) firma `manifest.sbom_hash` o `--digest`.
- Backend explicito `fixture-hmac-sha256` para golden/CI, determinista y sin red.
- Entrada de material por `--key` local; no se commitean claves reales.
- Artefacto canonico `protocol_release_signature.v1` con `subject_digest`, `backend`, `key_id` y `signature`.
- `scripts/verify_release.py` (+ `.ps1`) acepta `--signature`, `--pubkey`/`--key` y `--backend` opcional.
- Sin firma, `verify_release` conserva el contrato F7.2 de integridad.
- Con firma, valida autenticidad sobre `manifest.sbom_hash`; falla cerrada si falta material, si el digest no coincide, si el `key_id` no corresponde o si la firma fue alterada.

## Archivos tocados

- `.github/workflows/validate.yml`
- `scripts/sign_release.py`
- `scripts/sign_release.ps1`
- `scripts/verify_release.py`
- `scripts/verify_release.ps1`
- `examples/release_sign_cases/run_release_sign_cases.py`
- `Area_comun/decisions/DECISION-0023-firma-release.md`
- `Area_comun/specs/SPEC-0061-faseF7.4-firma.md`
- `Area_comun/tasks/TASK-0075-codex-faseF7.4-firma.md`
- `Area_comun/state/CLAIMS.json`
- `Area_comun/state/PROJECT_STATE.json`
- `Area_comun/state/TASK_INDEX.json`
- `Area_comun/mailbox/archived/MSG-20260607-Claude-to-Codex-task0074-accepted.md`
- `Area_comun/mailbox/archived/MSG-20260607-Claude-to-Codex-task0075-GO-faseF7.4.md`
- `Area_comun/mailbox/open/MSG-20260607-Codex-to-Claude-task0075-in-review.md`

## Validacion ejecutada

- `python examples\release_sign_cases\run_release_sign_cases.py` -> OK, 8 casos.
- `python examples\release_verify_cases\run_release_verify_cases.py` -> OK, 6 casos.
- `python examples\provenance_cases\run_provenance_cases.py` -> OK, 5 casos.
- `python examples\sbom_cases\run_sbom_cases.py` -> OK, 4 casos.
- `python -m py_compile scripts\sign_release.py scripts\verify_release.py examples\release_sign_cases\run_release_sign_cases.py` -> OK.
- `python scripts\scan_encoding.py --root .` -> OK.
- `powershell -NoProfile -File scripts\scan_encoding.ps1 -Root .` -> OK.
- `python scripts\scan_domain_neutrality.py --root .` -> OK.
- `powershell -NoProfile -File scripts\scan_domain_neutrality.ps1 -Root .` -> OK.
- `python scripts\validate_collaboration_state.py --root .` -> OK, con warning esperado de drift por modo sombra.
- `powershell -NoProfile -File scripts\validate_collaboration_state.ps1 -Root .` -> OK, con warning esperado de drift por modo sombra.
- `python scripts\validate_collaboration_state.py --root examples\minimal_instance` -> OK.
- `powershell -NoProfile -File scripts\validate_collaboration_state.ps1 -Root examples\minimal_instance` -> OK.
- `python scripts\prune_state.py --root . --apply` -> poda aplicada; cold-start final ~12.5k tokens.
- `python scripts\prune_state.py --root . --check` -> OK, cold-start final ~12.5k tokens.

## Notas de revision

- El backend real no queda mandado ni fijado a proveedor unico; el backend fixture existe para CI/golden.
- El flujo de autenticidad es opt-in: sin `--signature`, `verify_release` sigue siendo F7.2.
- No hay claves reales en el repo. El material fixture de golden es no-real y esta etiquetado en los tests.
- Queda F7.5 para documentar el flujo de release firmado.
