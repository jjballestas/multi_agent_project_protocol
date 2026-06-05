# Session report - Versionado del protocolo y arquitectura de perfiles

- Date: 2026-06-05
- Phase: P0 (con apertura de la línea P1)
- Process status: closed
- Ratification: draft (pendiente de ratificación por Codex y por el operador humano)

## 1. In One Sentence
Cerré TASK-0003 (política de versionado SemVer + CHANGELOG + mecanismo `protocol_version`) y dejé
formalizada la arquitectura **core / profiles / examples** (DECISION-0002) con su backlog.

## 2. What Was Done
- **Versionado (TASK-0003 → done):** se creó `CHANGELOG.md` y la decisión `DECISION-0001` que
  define SemVer para un protocolo de archivos con ejemplos concretos de qué es MAJOR (incompatible),
  MINOR (capacidad aditiva) y PATCH (fix), cómo se publican releases (tag `vX.Y.Z`) y que los
  cambios MAJOR requieren aprobación humana.
- **`protocol_version`:** cada instancia ya puede declarar qué versión del protocolo sigue, en su
  `protocol.config.json`. Se añadió a la plantilla, a la config viva de este repo y al ejemplo.
- **Arquitectura de perfiles (DECISION-0002):** el protocolo se separa en core neutral, perfiles
  profesionales opcionales (`profiles/`) y ejemplos. Lo específico del repo `entorno_open_cloude`
  (.NET, SQL Server, Azure DevOps, Dev Containers, Docker, ADRs, branching, seguridad, pipelines)
  entrará como perfil `dotnet_enterprise`, **nunca** dentro del core neutral.
- **Backlog nuevo (fase P1, target v0.3.0):** TASK-0005 (arquitectura de perfiles, Claude),
  TASK-0006 (perfil `dotnet_enterprise`, Codex), TASK-0007 (soporte de perfiles en estado y
  validador, Codex).

## 3. Decisions
- **DECISION-0001 — Versionado:** SemVer + CHANGELOG + `protocol_version`; MAJOR requiere
  aprobación humana. Consecuencia práctica: las instancias pueden fijar y comprobar compatibilidad.
- **DECISION-0002 — Core/profiles/examples:** el core se mantiene neutral; las buenas prácticas por
  stack viven en perfiles opcionales y componibles. Consecuencia: se reutiliza conocimiento
  profesional sin acoplar el protocolo a ningún stack.

## 4. Current Project State
- v0.1.0 publicado. La línea P0 (enriquecimiento) está casi completa: validador multiplataforma +
  CI (done), versionado (done). **Falta TASK-0004 (scaffolding, Codex) para cerrar v0.2.0.**
- Validador en verde sobre raíz y `examples/minimal_instance`.

## 5. Next Steps
1. Codex: ejecutar TASK-0004 (scaffolding) rellenando `protocol_version`. Cierra v0.2.0.
2. Publicar v0.2.0 (tag + mover Unreleased en el CHANGELOG) — release MINOR, sin aprobación humana
   obligatoria, pero con validador verde.
3. Arrancar P1: TASK-0005 (Claude) define `profiles/`; luego TASK-0006 y TASK-0007 (Codex).

## 6. What We Need From The Human Owner
- **Ratificar** las dos decisiones (DECISION-0001 y DECISION-0002).
- Confirmar que el primer perfil sea `dotnet_enterprise` desde `entorno_open_cloude`.
- Nota: la futura `v1.0.0` (estabilización del contrato) y cualquier cambio MAJOR sí requerirán tu
  aprobación explícita.

## 7. Things To Watch
- **Fuga de dominio al core:** el riesgo principal de la línea de perfiles. La revisión de frontera
  la hago yo (arquitecto) en cada handoff de perfil.
- **Drift del validador** al añadir soporte de perfiles (TASK-0007): debe mantenerse la paridad
  `.py` ↔ `.ps1` con golden tests.

## 8. Details
- `CHANGELOG.md`
- `Area_comun/decisions/DECISION-0001-versionado.md`
- `Area_comun/decisions/DECISION-0002-core-perfiles-profesionales.md`
- `Area_comun/handoffs/HANDOFF-TASK-0004-claude-to-codex-1.md`
- `Area_comun/tasks/TASK-0005-*`, `TASK-0006-*`, `TASK-0007-*`
- `Area_comun/artifacts/ROADMAP-v0.2.0.md`
