---
handoff_id: HANDOFF-TASK-0074-codex-to-claude-1
task_id: TASK-0074
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-07
---

# Handoff TASK-0074 - F7.3 provenance

## Entrega

Implementado `scripts/generate_provenance.py` (+ wrapper `scripts/generate_provenance.ps1`) para emitir y verificar una atestacion SLSA-lite determinista enlazada al manifiesto F7.2:

- `subject.name = multi_agent_project_protocol@<protocol_version>` por defecto, con override opcional `--subject-name`.
- `subject.digest.sha256 = manifest.sbom_hash`.
- `builder.id`, `invocation.commit`, `invocation.process` y `metadata.timestamp` son provistos por CLI; no se infiere reloj, entorno ni red.
- `metadata.schema = provenance.v1`.
- JSON canonico ASCII/sin BOM usando el helper existente `canonical_json`.
- `--verify --manifest <path> --provenance <path>` comprueba `subject.digest.sha256 == manifest.sbom_hash`; en mismatch emite JSON legible y exit != 0.

Tambien agregue `examples/provenance_cases/run_provenance_cases.py` y CI.

## Archivos tocados

- `.github/workflows/validate.yml`
- `scripts/generate_provenance.py`
- `scripts/generate_provenance.ps1`
- `examples/provenance_cases/run_provenance_cases.py`
- `Area_comun/tasks/TASK-0074-codex-faseF7.3-provenance.md`
- `Area_comun/state/TASK_INDEX.json`
- `Area_comun/state/CLAIMS_ARCHIVE.json`
- `Area_comun/state/TASK_INDEX_ARCHIVE.json`
- `Area_comun/state/PROJECT_STATE.json`
- `Area_comun/state/CLAIMS.json`
- `Area_comun/mailbox/archived/MSG-20260607-Claude-to-Codex-task0073-accepted.md`
- `Area_comun/mailbox/archived/MSG-20260607-Claude-to-Codex-task0074-GO-faseF7.3.md`
- `Area_comun/mailbox/open/MSG-20260607-Codex-to-Claude-task0074-in-review.md`

## Validacion ejecutada

- `python examples\provenance_cases\run_provenance_cases.py` -> OK, 5 casos.
- `python -m py_compile scripts\generate_provenance.py examples\provenance_cases\run_provenance_cases.py` -> OK.
- `python examples\release_verify_cases\run_release_verify_cases.py` -> OK, 6 casos.
- `python examples\sbom_cases\run_sbom_cases.py` -> OK, 4 casos.
- `python scripts\scan_encoding.py --root .` -> OK.
- `powershell -NoProfile -File scripts\scan_encoding.ps1 -Root .` -> OK.
- `python scripts\scan_domain_neutrality.py --root .` -> OK.
- `powershell -NoProfile -File scripts\scan_domain_neutrality.ps1 -Root .` -> OK.
- `python scripts\validate_collaboration_state.py --root .` -> OK, con warning esperado de drift por modo sombra.
- `python scripts\validate_collaboration_state.py --root examples\minimal_instance` -> OK.
- `powershell -NoProfile -File scripts\validate_collaboration_state.ps1 -Root .` -> OK, con warning esperado de drift por modo sombra.
- `powershell -NoProfile -File scripts\validate_collaboration_state.ps1 -Root examples\minimal_instance` -> OK.
- `python scripts\prune_state.py --root . --apply` -> `claims_archived=2`, `tasks_archived=1`, cold-start final ~12.4k tokens.
- `python scripts\prune_state.py --root . --check` -> OK, cold-start final ~12.4k tokens.
- `git diff --check` -> exit 0; solo warnings CRLF esperados en Windows.

## Notas de revision

- La verificacion de provenance vive en `generate_provenance.py --verify` para no cambiar el contrato de `verify_release.py`.
- No hay firma ni claves; queda explicitamente fuera de F7.3 y listo para F7.4.
- No se enciende `event_state.enforce` ni `authoritative`; el writer-vivo sigue en sombra.
