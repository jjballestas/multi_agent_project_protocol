---
task_id: TASK-0184
title: "FLOOR skills Fase 1 pieza 2: 3 skills de CONTENIDO (DDL / regla-negocio-vs-legacy / verificacion-migracion) en profiles/financiero_presupuesto/skills/ (SPEC-0097)"
type: product
status: done
owner: Codex
phase: P2
priority: normal
spec_id: SPEC-0097
created_at: 2026-06-26
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/multi_agent_project_protocol
origin: FLOOR skills Fase 1 pieza 2 (GO operador 2026-06-26)
reuses: [TASK-0183]
linked_decisions: [DECISION-0061, DECISION-0047, DECISION-0040]
file: Area_comun/tasks/TASK-0184-codex-skills-fase1-pieza2-tres-skills.md
---

# TASK-0184 - 3 skills de contenido sobre el mecanismo (pieza 2)

> maker=Codex / checker=Arquitecto. Repo = PROTOCOLO. Usa el mecanismo de TASK-0183 (loader + registro). El
> CONTENIDO va al PERFIL (`profiles/financiero_presupuesto/skills/`), NO al core (neutralidad, DECISION-0061).
> Crea el shell MINIMO del perfil para hospedarlas (sin politica de dominio). Off-by-default. NO toca #4/config.

## Alcance (SPEC-0097 AC1-AC6)
- **Shell minimo `profiles/financiero_presupuesto/`:** `profile.manifest.json` (schema del template, profile_id
  financiero_presupuesto, requires_protocol_version compatible 1.x, descripcion neutra) + carpeta `skills/`.
  SIN docs/prompts/templates de negocio.
- **3 skill-docs** en `profiles/financiero_presupuesto/skills/` (frontmatter skill_id/title/profile/version/
  neutral_core:false + body procedimiento generico, sin PII/secretos):
  1. `ddl-conventions.skill.md` (naming, tipos, constraints, idempotencia).
  2. `business-rule-vs-legacy.skill.md` (regla intencional vs comportamiento legacy accidental).
  3. `migration-verification.skill.md` (conteos/reconciliacion, idempotencia, pre/post-checks, rollback).
- **Registro:** 3 entradas en `skills/skills.config.json` (profile/path/version/enabled:false/trust_boundary);
  registry (core) sigue NEUTRAL (id/title sin terminos de dominio).
- **Golden:** extender `examples/skills_loader_cases` para cargar las 3 (habilitadas) via el loader y validar
  conformidad + contencion de ruta; CI cubre.

## DoD (= SPEC-0097 AC1-AC6)
- AC1 shell de perfil minimo (manifest valido + skills/), sin politica de dominio.
- AC2 3 docs conformes (neutral_core:false, profile=financiero_presupuesto), contenido generico.
- AC3 3 entradas en el registro, enabled:false, trust_boundary completo, registry neutral.
- AC4 el loader las resuelve cuando enabled (golden/behavior), valida contencion de ruta, determinista, sin escritura.
- AC5 scan_domain_neutrality exit 0 + scan_encoding exit 0.
- AC6 validate exit 0 (con/sin secretos) clon limpio, drift 0, golden verde, CI, config pinned/genesis intactos, Co-Author.

## Fuera de alcance
- Politica/logica de dominio del perfil financiero (negocio/presupuesto/seguridad de dominio): fase posterior.
- Habilitar las skills por defecto; capacidad ejecutable via skills; tocar genesis/#4/config pinned.

## Notas
- Las 3 skills son procedimientos genericos de ingenieria; viven en el perfil por la regla de neutralidad del
  core, no por ser de dominio. Reusa el loader/registro de TASK-0183 (clon protocolo en Windows: usar
  `git -c core.longpaths=true`).
