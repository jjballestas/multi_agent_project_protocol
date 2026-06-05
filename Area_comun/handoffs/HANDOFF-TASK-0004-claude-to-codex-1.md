---
handoff_id: HANDOFF-TASK-0004-claude-to-codex-1
task_id: TASK-0004
from: Claude
to: Codex
date: 2026-06-05
status: for_implementation
requires_response: yes
response_owner: Codex
requested_action: Confirmar recepcion; en TASK-0004 rellenar protocol_version en el scaffolding; no arrancar TASK-0006/0007 hasta cerrar TASK-0005.
---

# Handoff: versionado cerrado (TASK-0003) → impacto en scaffolding y nuevo backlog de perfiles

## 1. Minimal Context
Cerré **TASK-0003** (política de versionado). Ahora hay SemVer formal
([DECISION-0001](../decisions/DECISION-0001-versionado.md)), `CHANGELOG.md` y un campo nuevo
**`protocol_version`** que toda instancia declara en `protocol.config.json`. Esto afecta
directamente a tu **TASK-0004** (scaffolding). Además quedó formalizada la arquitectura de
perfiles ([DECISION-0002](../decisions/DECISION-0002-core-perfiles-profesionales.md)) con backlog
nuevo (TASK-0005/0006/0007).

## 2. What Was Done
- `CHANGELOG.md` (raíz): formato Keep a Changelog + SemVer; v0.1.0 y sección Unreleased→v0.2.0.
- `DECISION-0001-versionado.md`: SemVer con ejemplos concretos (MAJOR/MINOR/PATCH), regla "ante la
  duda, MAJOR", mecanismo `protocol_version`, procedimiento de release y aprobación humana de MAJOR.
- `protocol_version` añadido como campo aditivo (cambio MINOR) en:
  - `protocol.config.template.json` (placeholder `{{PROTOCOL_VERSION}}`),
  - `protocol.config.json` (live, `0.1.0`),
  - `examples/minimal_instance/protocol.config.json` (`0.1.0`),
  - documentado en `README_INSTANCIACION.md` (paso 8).
- `DECISION-0002` + tareas TASK-0005/0006/0007 en `TASK_INDEX.json` (fase P1, target v0.3.0).

## 3. What Was Not Done
- No toqué `scripts/` ni `new_instance.*` (es tu claim/scope en TASK-0004).
- No creé `profiles/` todavía: lo define TASK-0005 (Claude) antes de TASK-0006/0007.

## 4. How To Verify
- `python scripts/validate_collaboration_state.py` → OK (raíz).
- `python scripts/validate_collaboration_state.py --root examples/minimal_instance` → OK.
- Revisar que `protocol.config.json` (raíz, ejemplo) tiene `protocol_version`.

## 5. Requested Action
1. **TASK-0004 (scaffolding):** el script `new_instance.*` debe pedir/rellenar
   `{{PROTOCOL_VERSION}}` (por defecto, la versión publicada vigente del protocolo) y NO dejar el
   placeholder sin resolver. Cuéntalo en tu handoff de cierre de TASK-0004.
2. **Backlog P1:** TASK-0006 y TASK-0007 dependen de **TASK-0005** (Claude). No los arranques hasta
   que cierre TASK-0005 y te entregue el contrato `profile.manifest` y la estructura `profiles/`.
3. Confirma recepción y si ves un problema con `protocol_version` en el scaffolding, responde aquí
   o abre un MSG en `mailbox/open/`.

## 6. Risks and Assumptions
- Asumo Python para el scaffolding (recomendado por portabilidad), pero la decisión final del
  lenguaje es tuya en TASK-0004.
- `protocol_version` es opcional para el validador hoy; no rompe instancias existentes.

## 7. Open Questions / BLOCKED
- Ninguna bloqueante. (Pregunta abierta no bloqueante en TASK-0005 sobre `adopted_profiles`.)

## 8. Pointers
- Decisiones: `Area_comun/decisions/DECISION-0001-versionado.md`, `DECISION-0002-core-perfiles-profesionales.md`.
- Tareas: `Area_comun/tasks/TASK-0004-*`, `TASK-0005-*`, `TASK-0006-*`, `TASK-0007-*`.
- Roadmap: `Area_comun/artifacts/ROADMAP-v0.2.0.md` (sección post-v0.2.0).
- CHANGELOG: `CHANGELOG.md`.
