---
spec_id: SPEC-0097
task_id: TASK-0184
type: feature
status: accepted
linked_decisions:
  - DECISION-0061
  - DECISION-0047
  - DECISION-0040
created_at: 2026-06-26
updated_at: 2026-06-26
author: Arquitecto
---

# SPEC-0097 - skills Fase 1 pieza 2: 3 skills de CONTENIDO en el perfil (sobre el mecanismo TASK-0183)

## Context

DECISION-0061 (skills gobernadas) + mecanismo entregado en TASK-0183/SPEC-0096 (registro fuera del config
pinned + loader cold-start read-only). FLOOR skills **Fase 1 pieza 2 = las 3 skills NEUTRALES de contenido**
declaradas en DECISION-0061: convenciones DDL / regla-negocio-vs-legacy / verificacion-migracion. El
**contenido vive en el PERFIL** (`profiles/financiero_presupuesto/skills/`), NO en el core (regla de
neutralidad). Como el perfil aun no existe, esta pieza crea un **shell MINIMO** del perfil suficiente para
hospedar las skills, SIN politica/logica de dominio (eso es la fase "perfil financiero" posterior, fuera de
alcance). maker=Codex, checker=Arquitecto. Repo = PROTOCOLO.

## Scope

- **Shell minimo `profiles/financiero_presupuesto/`:** `profile.manifest.json` (schema del template, profile_id
  `financiero_presupuesto`, `requires_protocol_version` compatible con 1.x, descripcion neutra) + carpeta
  `skills/`. SIN docs de dominio, SIN prompts/templates de negocio. Solo lo necesario para alojar las skills.
- **3 skill-docs** en `profiles/financiero_presupuesto/skills/`, cada uno con el formato del mecanismo
  (frontmatter `skill_id`/`title`/`profile: financiero_presupuesto`/`version`/`neutral_core: false` + body =
  PROCEDIMIENTO en texto, generico/neutral, sin PII ni secretos):
  1. `ddl-conventions.skill.md` -- convenciones para escribir DDL (naming, tipos, constraints, idempotencia).
  2. `business-rule-vs-legacy.skill.md` -- como distinguir una regla de negocio intencional de comportamiento
     legacy accidental al tocar codigo heredado.
  3. `migration-verification.skill.md` -- como verificar una migracion (conteos/reconciliacion, idempotencia,
     pre/post-checks, rollback).
- **Registro:** 3 entradas en `skills/skills.config.json` (`profile: financiero_presupuesto`, `path` al doc,
  `version`, `enabled:false` por defecto, `trust_boundary` read_only/grants_no_authority/persists_outputs). El
  registro (core) se mantiene NEUTRAL (id/title sin terminos de dominio).
- **Golden:** extender `examples/skills_loader_cases` (o golden hermano) para cargar las 3 skills de perfil
  habilitadas y verificar conformidad + resolucion via el loader.

## Acceptance Criteria

- **AC1 (shell de perfil minimo):** existe `profiles/financiero_presupuesto/profile.manifest.json` valido +
  `skills/`; SIN docs/prompts/templates de dominio. No introduce politica de negocio.
- **AC2 (3 skill-docs conformes):** los 3 docs existen en `profiles/financiero_presupuesto/skills/`, cada uno
  con frontmatter completo (`neutral_core:false`, `profile: financiero_presupuesto`) + body de procedimiento;
  contenido generico (sin PII/secretos).
- **AC3 (registradas, registry neutral):** 3 entradas en `skills/skills.config.json` con `profile`/`path`
  correctos, `enabled:false` por defecto, trust_boundary completo; el registro NO contiene terminos de dominio.
- **AC4 (cargan via el mecanismo):** behavior-test/golden que con las 3 habilitadas el loader (TASK-0183) las
  resuelve y devuelve sus procedimientos, valida su contencion de ruta (bajo `profiles/financiero_presupuesto/
  skills/`) y su conformidad; corrida repetida = misma salida; sin escritura de estado.
- **AC5 (neutralidad + encoding):** `scan_domain_neutrality` exit 0 (core + `skills/**` registry neutral) y
  `scan_encoding` exit 0.
- **AC6 (gates):** clon limpio `validate_collaboration_state.py` exit 0 (con y sin secretos), drift 0, golden
  verde, CI cubre el golden; `protocol.config.json`/genesis intactos; Co-Authored-By Codex.

## Out of scope

- Politica/logica de dominio del perfil financiero (docs de negocio, presupuesto, seguridad de dominio): fase
  posterior, fuera de esta pieza.
- Habilitar las skills por defecto (siguen off-by-default); cualquier capacidad ejecutable via skills.
- Tocar genesis/#4/config pinned.

## Notes

- Las 3 skills son procedimientos genericos de ingenieria; viven en el perfil por la regla de neutralidad del
  core (DECISION-0061), no porque sean de dominio. El shell de perfil es el minimo para hospedarlas.
