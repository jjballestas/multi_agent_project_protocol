---
handoff_id: HANDOFF-TASK-0064-codex-to-claude-1
task_id: TASK-0064
from: Codex
to: Claude
status: in_review
created_at: 2026-06-07
context_refs:
  - Area_comun/specs/SPEC-0050-d2.4-versionado-paquete.md
  - Area_comun/protocol/PACKAGE_VERSIONING.md
  - README_INSTANCIACION.md
---

# Handoff TASK-0064 - Versionado del paquete

## Resumen

Entrego D2.4 como documentacion solamente. No cambie runtime, scripts, schema, CHANGELOG, version
del protocolo ni tag de release.

## Cambios

- `Area_comun/protocol/PACKAGE_VERSIONING.md`: nuevo documento para adoptantes con:
  - fuentes autoritativas;
  - los 4 ejes de version (`protocol_version`, `runtime_version`, `schema_version`,
    `profile_version`);
  - SemVer desde la perspectiva de una instancia adoptante;
  - compatibilidad por tier `coordination`/`runtime`;
  - migracion dentro del mismo tier y `coordination -> runtime`;
  - notas sobre wrapper real, perfiles y cambios incompatibles.
- `README_INSTANCIACION.md`: enlace breve al nuevo documento desde la seccion de upgrade, sin
  duplicar reglas.
- `Area_comun/mailbox/archived/MSG-20260607-Claude-to-Codex-task0064-GO-versionado.md`: GO
  archivado tras claim.

## Validacion

- `python scripts\validate_collaboration_state.py --root .` -> OK, con warning FYI preexistente:
  `MSG-20260607-Claude-to-Codex-task0063-accepted.md`.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .`
  -> OK, mismo warning.
- `python scripts\validate_collaboration_state.py --root examples\minimal_instance` -> OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root examples\minimal_instance`
  -> OK.
- `python scripts\scan_encoding.py --root .` -> OK.
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\scan_encoding.ps1 -Root .` -> OK.
- `python scripts\scan_domain_neutrality.py --root .` -> OK (exit 0).
- `powershell -NoProfile -ExecutionPolicy Bypass -File scripts\scan_domain_neutrality.ps1 -Root .`
  -> OK (exit 0).
- `python scripts\prune_state.py --root . --check` -> OK.
- `git diff --check` -> OK, solo warnings CRLF de Git.
- Check de destinos enlazados principales -> OK.

## Fuera de alcance confirmado

- No hice el release v1.0.
- No hice bump de `protocol_version` ni `runtime_version`.
- No movi contenido de `CHANGELOG.md`.
- No toque DECISION-0020 ni el follow-up de prune.
