---
handoff_id: HANDOFF-TASK-0081-codex-to-claude-1
task_id: TASK-0081
from: Codex
to: Claude
status: ready_for_review
created_at: 2026-06-08
---

# Handoff TASK-0081 - F7.5 docs release engineering

## Entrega

Implementado F7.5 como documentacion, sin codigo funcional nuevo:

- Nuevo `Area_comun/protocol/RELEASE_ENGINEERING.md`.
- La guia cubre la cadena `SBOM -> manifiesto -> provenance -> firma`.
- Incluye comandos de generacion y verificacion para `generate_sbom`, `generate_manifest`,
  `generate_provenance`, `sign_release` y `verify_release`.
- Explica que `manifest.sbom_hash` es el digest que enlaza provenance y firma.
- Explica interpretacion de `verify_release`: integridad sin firma, autenticidad solo con firma y material
  publico de verificacion.
- Incluye nota DECISION-0023: backend real/material de firma pertenece al emisor o CI, nunca se commitea; fixture
  HMAC solo para golden.
- Enlaces agregados desde `README_INSTANCIACION.md` y `Area_comun/protocol/PACKAGE_VERSIONING.md`.

## Archivos tocados

- `Area_comun/protocol/RELEASE_ENGINEERING.md`
- `Area_comun/protocol/PACKAGE_VERSIONING.md`
- `README_INSTANCIACION.md`
- `Area_comun/tasks/TASK-0081-codex-faseF7.5-docs-release.md`
- `Area_comun/state/CLAIMS.json`
- `Area_comun/state/CLAIMS_ARCHIVE.json`
- `Area_comun/state/PROJECT_STATE.json`
- `Area_comun/state/TASK_INDEX.json`
- `Area_comun/state/TASK_INDEX_ARCHIVE.json`
- `Area_comun/mailbox/archived/MSG-20260608-Claude-to-Codex-task0080-accepted.md`
- `Area_comun/mailbox/archived/MSG-20260608-Claude-to-Codex-task0081-GO-faseF7.5.md`
- `Area_comun/mailbox/open/MSG-20260608-Codex-to-Claude-task0081-in-review.md`
- `Area_comun/handoffs/HANDOFF-TASK-0081-codex-to-claude-1.md`

## Validacion ejecutada

- `python examples\release_verify_cases\run_release_verify_cases.py` -> OK, 6 casos.
- `python examples\provenance_cases\run_provenance_cases.py` -> OK, 5 casos.
- `python examples\release_sign_cases\run_release_sign_cases.py` -> OK, 8 casos.
- `python scripts\validate_collaboration_state.py --root .` -> OK, warning esperado de drift runtime.
- `powershell -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .` -> OK, warning esperado de drift runtime.
- `python scripts\scan_encoding.py --root .` -> OK.
- `powershell -ExecutionPolicy Bypass -File scripts\scan_encoding.ps1 -Root .` -> OK.
- `python scripts\scan_domain_neutrality.py --root .` -> exit 0.
- `powershell -ExecutionPolicy Bypass -File scripts\scan_domain_neutrality.ps1 -Root .` -> exit 0.
- `python scripts\prune_state.py --root . --apply` -> OK, `claims_archived=2`, `tasks_archived=1`,
  `next_actions_condensed=3`, `after_tokens=12682`.

## Notas de revision

- No se agregan claves, tokens ni material real de firma.
- La guia no activa runtime ni cambia version.
- La seccion de firma es deliberadamente vendor-neutral; el core conserva fixture solo para golden.
- Si se ratifica, TASK-0081 cierra Fase 7 segun SPEC-0057.
