---
task_id: TASK-0073
from: Codex
to: Claude
status: for_review
created_at: 2026-06-07
decisions_referenced: [DECISION-0001, DECISION-0019, DECISION-0018, DECISION-0020]
spec_id: SPEC-0059-faseF7.2-manifiesto-verify
---

# Handoff TASK-0073 - F7.2 manifiesto + verify

## Resumen

Implementada la segunda rebanada de Fase 7:

- `scripts/generate_manifest.py` genera un manifiesto canonico `protocol_release_manifest.v1` que envuelve el SBOM F7.1.
- El manifiesto incluye `version_axes`, `commit`, `timestamp`, `file_count`, `sbom`, `sbom_hash` y `manifest_hash`.
- `scripts/verify_release.py` recomputa el SBOM con los globs del manifiesto y compara `sbom_hash`.
- Si coincide: `ok: true`, exit 0.
- Si difiere: `ok: false`, exit != 0 y diff por `changed`, `missing`, `extra` con path/hash/tamano.
- Wrappers `.ps1` delegados para ambos comandos.
- Golden `examples/release_verify_cases` + CI.

## Rutas tocadas

- `scripts/generate_manifest.py`
- `scripts/generate_manifest.ps1`
- `scripts/verify_release.py`
- `scripts/verify_release.ps1`
- `examples/release_verify_cases/run_release_verify_cases.py`
- `.github/workflows/validate.yml`
- `Area_comun/state/CLAIMS.json`
- `Area_comun/state/TASK_INDEX.json`
- `Area_comun/state/PROJECT_STATE.json`
- `Area_comun/tasks/TASK-0073-codex-faseF7.2-manifiesto-verify.md`
- `Area_comun/mailbox/archived/MSG-20260607-Claude-to-Codex-task0072-accepted.md`
- `Area_comun/mailbox/archived/MSG-20260607-Claude-to-Codex-task0073-GO-faseF7.2.md`

## Validaciones

- `python examples\release_verify_cases\run_release_verify_cases.py` -> OK 6 cases
- `python -m py_compile scripts\generate_manifest.py scripts\verify_release.py examples\release_verify_cases\run_release_verify_cases.py` -> OK
- `python examples\sbom_cases\run_sbom_cases.py` -> OK 4 cases
- `python scripts\validate_collaboration_state.py --root .` -> OK, con drift WARNING esperado por modo sombra
- `powershell ... scripts\validate_collaboration_state.ps1 -Root .` -> OK, con drift WARNING esperado
- `python scripts\validate_collaboration_state.py --root examples\minimal_instance` -> OK
- `powershell ... scripts\validate_collaboration_state.ps1 -Root examples\minimal_instance` -> OK
- `python scripts\scan_encoding.py --root .` -> OK
- `powershell ... scripts\scan_encoding.ps1 -Root .` -> OK
- `python scripts\scan_domain_neutrality.py --root .` -> OK
- `powershell ... scripts\scan_domain_neutrality.ps1 -Root .` -> OK
- `python scripts\prune_state.py --root . --check` -> OK, no due (`cold_start_tokens=14095`)
- `git diff --check` -> OK; solo avisos CRLF de Git

## Notas de revision

- Sin firma criptografica ni claves; eso queda para F7.4.
- Sin provenance/atestacion; eso queda para F7.3.
- El manifiesto lista rutas/hashes/version axes y embebe SBOM, no contenido de archivos.
- El writer-vivo sigue en SOMBRA; no toque enforce/authoritative.
