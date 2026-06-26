---
message_id: MSG-20260626-Arquitecto-to-Codex-GO-TASK-0183
task_id: TASK-0183
type: GO
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
requested_action: "GO a TASK-0183 (FLOOR skills Fase 1 PIEZA 1 = el MECANISMO; ready). Reclamala -> in_progress y entrega a in_review cuando este verde. Repo = PROTOCOLO (capa neutral `skills/`, espejo de `connectors/`). Construir: registro `skills/skills.config.json` FUERA del config pinned (off-by-default) + skill=doc gobernado + loader cold-start DETERMINISTA y READ-ONLY + golden `examples/skills_loader_cases` + cobertura neutralidad + CI. DoD = SPEC-0096 AC1-AC6. NO tocar protocol.config.json/genesis/#4. Las 3 skills de contenido son la PIEZA 2 (GO posterior); esta tarea es SOLO el mecanismo. maker=Codex / checker=Arquitecto. rr=false."
one_line_summary: "GO TASK-0183: mecanismo de skills (registro fuera del config + loader cold-start read-only), neutral, off-by-default; pieza 1 de skills Fase 1."
context_refs:
  - Area_comun/decisions/DECISION-0061-skills-registry-coldstart-loader.md
  - Area_comun/specs/SPEC-0096-skills-mechanism-coldstart-loader.md
  - Area_comun/tasks/TASK-0183-codex-skills-mechanism-coldstart-loader.md
---

# GO -- TASK-0183 (FLOOR skills Fase 1, pieza 1 = mecanismo)

El operador dio **GO a skills Fase 1** (modelo de digestion elegido = **loader cold-start READ-ONLY**).
Esta tarea es la **pieza 1 = el MECANISMO** (las 3 skills de contenido son la pieza 2, GO posterior).

Anclaje: DECISION-0061 + SPEC-0096. Repo = **protocolo**, capa neutral `skills/` (espejo de `connectors/`).

Construir (SPEC-0096 AC1-AC6):
- **Registro** `skills/skills.config.json` FUERA de `protocol.config.json`, `schema_version:"skills.config.v1"`,
  cada skill con `id`/`title`/`profile` (o `neutral_core`)/`path`/`version`/`enabled:false` + `trust_boundary`
  (`read_only`/`grants_no_authority`/`persists_outputs`).
- **Skill = doc gobernado** (frontmatter + body = procedimiento). Contenido de dominio SOLO en `profiles/<perfil>/skills/`.
- **Loader cold-start** DETERMINISTA + READ-ONLY: resuelve enabled, valida trust_boundary + ubicacion, devuelve
  indice/contenido en memoria; SIN escribir estado/ledger/event-log; NO importa escritores (test de imports).
- **Golden** `examples/skills_loader_cases` (registro + skills de ejemplo NEUTRALES del mecanismo): enabled
  resuelto, disabled skip, skill malformada rechazada, contenido de dominio en el core RECHAZADO (fail-closed).
- **Neutralidad:** `scan_domain_neutrality` cubre `skills/` y pasa. **CI** cubre el golden.

Gates de cierre: validate exit 0 (con/sin secretos) clon limpio, drift 0, scan_encoding/neutrality exit 0,
golden verde, CI, Co-Authored-By. #4/genesis/config pinned intactos. Entrega a in_review; yo re-checo clon limpio. rr=false.
