---
spec_id: SPEC-0096
task_id: TASK-0183
type: security
status: accepted
linked_decisions:
  - DECISION-0061
  - DECISION-0047
  - DECISION-0040
  - DECISION-0048
created_at: 2026-06-26
updated_at: 2026-06-26
author: Arquitecto
---

# SPEC-0096 - Mecanismo de skills: registro fuera del config pinned + loader cold-start READ-ONLY

## Context

DECISION-0061: skills gobernadas, mecanismo NEUTRAL, registro fuera del config pinned, loader cold-start
read-only, off-by-default, no concede autoridad, no toca #4. FLOOR skills **Fase 1 pieza 1 = el MECANISMO**
(las 3 skills neutrales son la pieza 2, GO posterior). Patron = capa `connectors/` (DECISION-0044/0048).
maker=Codex, checker=Arquitecto. Fixtures-only.

## Scope

- **`skills/` (capa neutral en el protocolo):** framework + loader + registro, domain-neutral (sin terminos
  de dominio). Espeja `connectors/`.
- **Registro `skills/skills.config.json`** (FUERA de `protocol.config.json`), `schema_version:"skills.config.v1"`,
  lista de skills cada una con `id`, `title`, `profile` (o `neutral_core:true` solo para skills del mecanismo
  de ejemplo), `path` (al doc de la skill), `version`, `enabled:false` por defecto, y `trust_boundary`
  (`read_only:true`, `grants_no_authority:true`, `persists_outputs:false`).
- **Skill = documento gobernado:** frontmatter (`skill_id`, `title`, `profile`, `version`, `neutral_core`) +
  body (el PROCEDIMIENTO en texto). Las skills de DOMINIO viven SOLO en `profiles/<perfil>/skills/`.
- **Loader cold-start (`skills/loader.py` o equivalente):** funcion DETERMINISTA y READ-ONLY que, dado el
  registro, resuelve las skills `enabled:true`, valida cada una contra su trust_boundary + ubicacion, y
  devuelve un indice/contenido en memoria para que un agente lo lea en arranque. SIN escritura de estado.
- **Golden fixtures `examples/skills_loader_cases/`:** registro de ejemplo + skills de ejemplo NEUTRALES
  (mecanismo, no dominio) que ejercitan: resolucion de enabled, skip de disabled, rechazo de skill mal
  declarada, rechazo de contenido de dominio en el core.

## Acceptance Criteria

- **AC1 (registro fuera del config pinned):** existe `skills/skills.config.json` con schema versionado,
  default por skill `enabled:false`. `protocol.config.json` NO cambia; `chain.genesis` intacto; drift 0.
- **AC2 (loader read-only determinista):** el loader resuelve skills enabled y produce el indice/contenido en
  memoria; corrida repetida = misma salida. Behavior-test: con N skills enabled devuelve sus procedimientos;
  con todas disabled devuelve vacio. NO escribe ningun archivo de estado/ledger/event-log.
- **AC3 (no concede autoridad / frontera de datos):** el modulo del loader NO importa escritores del
  ledger/event-log (test de imports, espejo AC4 connectors). El contenido cargado es texto inerte; no hay
  ruta de ejecucion ni mutacion de estado del protocolo a traves de una skill.
- **AC4 (neutralidad del mecanismo + ubicacion del contenido):** `scan_domain_neutrality` cubre `skills/` y
  pasa (el mecanismo no contiene terminos de dominio). Behavior-test: una skill declarada con contenido de
  dominio pero ubicada en el core (no en `profiles/`) es RECHAZADA por el loader (fail-closed).
- **AC5 (off-by-default fail-closed):** con el registro ausente o todo disabled, el loader devuelve vacio sin
  error; una entrada malformada (falta `path`, trust_boundary incompleta, `path` fuera de las rutas
  permitidas) es rechazada antes de leer contenido.
- **AC6 (gates):** clon limpio valida `python scripts/validate_collaboration_state.py` exit 0 (con y sin
  secretos), drift 0, `scan_encoding`/`scan_domain_neutrality` exit 0; golden `examples/skills_loader_cases`
  verde; CI cubre el golden. Co-Authored-By Codex en el commit de producto.

## Out of scope

- Las 3 skills neutrales de contenido (pieza 2, GO posterior): convenciones DDL / regla-negocio-vs-legacy /
  verificacion-migracion, en `profiles/financiero_presupuesto/skills/`.
- Cualquier capacidad ejecutable/accion via skills; inyeccion de skills en tareas/handoffs; superficie en el
  front. Tocar genesis/#4/config pinned.

## Notes

- Una skill es TEXTO inerte: no hay "uso vivo" riesgoso como en connectors; por eso no requiere s9+GO para
  leerse. Aun asi off-by-default y SDD por pieza.
- El loader es solo lectura; la "digestion" es que el agente LEE el procedimiento en cold-start, no que el
  mecanismo actue.
