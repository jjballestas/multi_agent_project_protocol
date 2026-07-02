# Session report - Release v0.2.0 y apertura de la fase P1

- **Updated:** 2026-06-29T12:34:56Z
- **Dataset actualizado:** 465/500 elegibles (seq>=2221 AND intent.applied AND ed25519; Analista: 46, Arquitecto: 236, Codex: 183).

- Phase: P0 (cerrada) → P1 (abierta)
- Process status: closed
- Ratification: draft (pendiente de ratificación por Codex y por el operador humano)

## 1. In One Sentence
Revisé y acepté TASK-0004 (scaffolding), **publiqué v0.2.0** cerrando la fase P0, y dejé lista la
línea P1 (perfiles) para Codex.

## 2. What Was Done
- **TASK-0004 (scaffolding) revisada y cerrada (`done`).** Verificación independiente: el validador
  pasa en `examples/generated_minimal_instance` y no quedan placeholders `{{...}}`. El script
  `scripts/new_instance.py` (solo stdlib) renderiza los masters `*.template.*`, puebla
  `protocol_version`, falla si queda algún placeholder y no arrastra el historial de dogfooding.
- **Release v0.2.0 publicada (MINOR, sin aprobación humana obligatoria por DECISION-0001 §4):**
  - `CHANGELOG.md`: sección `[0.2.0]` con validador Python+CI, versionado/CHANGELOG/`protocol_version`
    y scaffolding; nuevo `Unreleased` apuntando a v0.3.0 (perfiles).
  - `protocol.config.json` (live) → `protocol_version: 0.2.0`.
  - `AGENTS.md`: "Released version: v0.2.0" y §2 actualizada a fase P1.
  - `PROJECT_STATE.json`: `version` 0.2.0, `released_versions` += v0.2.0, fase P1 con P0 marcada
    como completada.
- **Fase P1 abierta y coordinada:** TASK-0006 y TASK-0007 pasadas a `ready` (su dependencia
  TASK-0005 está `done`). Quedan asignadas a Codex; no las implementé (límite de rol).

## 3. Decisions
- No se tomaron decisiones nuevas. Se **aplicó** DECISION-0001 (procedimiento de release, v0.2.0 =
  MINOR) y se respetó DECISION-0002 (core neutral; perfiles aún por construir en P1).

## 4. Current Project State
- **v0.2.0 publicada** (pendiente solo el commit + tag en git, que acompaña a este reporte).
- Validadores en verde: raíz, `examples/minimal_instance`, `examples/generated_minimal_instance`.
- Fase P1 activa; backlog `ready`: TASK-0006 (perfil `dotnet_enterprise`), TASK-0007
  (`adopted_profiles` + validador).

## 5. Next Steps
1. Codex: reclamar y ejecutar **TASK-0006** (construir `profiles/dotnet_enterprise/` desde
   `entorno_open_cloude`) y **TASK-0007** (soporte de perfiles, aditivo). Ver
   HANDOFF-TASK-0005-claude-to-codex-1.
2. Claude: revisar la frontera de neutralidad en los handoffs de cierre de Codex.
3. Al cerrar P1: publicar **v0.3.0** (MINOR; mover Unreleased + tag).

## 6. What We Need From The Human Owner
- **Ratificar** este release v0.2.0 y las decisiones DECISION-0001/0002 (si no se hizo aún).
- Confirmar prioridad de P1 (perfil `dotnet_enterprise` primero).
- Recordatorio: una futura `v1.0.0` o cualquier cambio MAJOR sí requerirá aprobación humana
  explícita.

## 7. Things To Watch
- **Fuga de dominio al core** durante P1: riesgo principal; revisión de frontera por el arquitecto.
- **Paridad `.py` ↔ `.ps1`** del validador al añadir soporte de perfiles (TASK-0007).
- El validador PowerShell no se pudo ejecutar en esta sesión (política de entorno); la paridad ya
  estaba verificada en TASK-0002 y los cambios de esta sesión son de datos/estado, no de lógica
  del validador.

## 8. Details
- `CHANGELOG.md`
- `Area_comun/decisions/DECISION-0001-versionado.md`, `DECISION-0002-core-perfiles-profesionales.md`
- `Area_comun/handoffs/HANDOFF-TASK-0004-claude-to-codex-1.md`, `HANDOFF-TASK-0005-claude-to-codex-1.md`
- `Area_comun/tasks/TASK-0004-*` (done), `TASK-0005-*` (done), `TASK-0006-*` / `TASK-0007-*` (ready)
- `scripts/new_instance.py`, `examples/generated_minimal_instance/`
- `profiles/` (README + PROFILE_TEMPLATE), `Area_comun/artifacts/ARQUITECTURA-core-profiles.md`
