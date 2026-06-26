---
message_id: MSG-20260626-Arquitecto-to-Codex-GO-TASK-0184
task_id: TASK-0184
type: GO
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
requested_action: "GO a TASK-0184 (FLOOR skills Fase 1 PIEZA 2 = 3 skills de CONTENIDO; ready). Reclamala -> in_progress y entrega a in_review cuando este verde. Repo = PROTOCOLO. Usa el mecanismo de TASK-0183 (loader + registro). CONTENIDO al PERFIL (profiles/financiero_presupuesto/skills/), NO al core. Crea el shell MINIMO del perfil (manifest + skills/) SIN politica de dominio. 3 skills: ddl-conventions, business-rule-vs-legacy, migration-verification (procedimientos genericos). Registralas en skills/skills.config.json (profile/path, enabled:false, trust_boundary). Golden: cargar las 3 via el loader. DoD = SPEC-0097 AC1-AC6. NO tocar protocol.config.json/genesis/#4. maker=Codex / checker=Arquitecto. rr=false."
one_line_summary: "GO TASK-0184: 3 skills de contenido (DDL/regla-vs-legacy/migracion) en el perfil, sobre el mecanismo TASK-0183; shell minimo de perfil; off-by-default."
context_refs:
  - Area_comun/specs/SPEC-0097-skills-fase1-pieza2-tres-skills-contenido.md
  - Area_comun/tasks/TASK-0184-codex-skills-fase1-pieza2-tres-skills.md
  - Area_comun/decisions/DECISION-0061-skills-registry-coldstart-loader.md
---

# GO -- TASK-0184 (FLOOR skills Fase 1, pieza 2 = 3 skills de contenido)

El operador dio **GO a la pieza 2**. Construir sobre el mecanismo ya cerrado (TASK-0183/SPEC-0096).
Gobernada por DECISION-0061 (sin decision nueva). Anclaje: SPEC-0097. Repo = **protocolo**.

Construir (SPEC-0097 AC1-AC6):
- **Shell MINIMO** `profiles/financiero_presupuesto/`: `profile.manifest.json` (schema del template, profile_id
  financiero_presupuesto, requires_protocol_version compatible 1.x, descripcion neutra) + carpeta `skills/`.
  **SIN** docs/prompts/templates de negocio (la politica de dominio es fase posterior, fuera de alcance).
- **3 skill-docs** en `profiles/financiero_presupuesto/skills/` (frontmatter skill_id/title/`profile:
  financiero_presupuesto`/version/`neutral_core:false` + body = procedimiento generico, sin PII/secretos):
  `ddl-conventions.skill.md`, `business-rule-vs-legacy.skill.md`, `migration-verification.skill.md`.
- **Registro:** 3 entradas en `skills/skills.config.json` (profile/path/version/`enabled:false`/trust_boundary).
  El registro (core) sigue NEUTRAL: id/title sin terminos de dominio.
- **Golden:** extender `examples/skills_loader_cases` para cargar las 3 (habilitadas) via el loader y validar
  conformidad + contencion de ruta (bajo el perfil). CI cubre.

Gates de cierre: validate exit 0 (con/sin secretos) clon limpio, drift 0, scan_encoding/neutrality exit 0,
golden verde, CI, config pinned/genesis intactos, Co-Authored-By. Entrega a in_review; yo re-checo clon limpio
(usa `git -c core.longpaths=true` al clonar el protocolo en Windows). rr=false.
