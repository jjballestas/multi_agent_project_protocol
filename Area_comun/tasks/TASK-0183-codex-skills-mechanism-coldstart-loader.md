---
task_id: TASK-0183
title: "FLOOR skills Fase 1 pieza 1: mecanismo de skills (registro fuera del config pinned + loader cold-start READ-ONLY), neutral, off-by-default (SPEC-0096)"
type: product
status: done
owner: Codex
phase: P2
priority: normal
spec_id: SPEC-0096
created_at: 2026-06-26
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/multi_agent_project_protocol
origin: FLOOR skills Fase 1 (GO operador 2026-06-26)
reuses: []
linked_decisions: [DECISION-0061, DECISION-0047, DECISION-0040, DECISION-0048]
file: Area_comun/tasks/TASK-0183-codex-skills-mechanism-coldstart-loader.md
---

# TASK-0183 - Mecanismo de skills (registro + loader cold-start read-only)

> maker=Codex / checker=Arquitecto. Repo = PROTOCOLO (capa neutral `skills/`, espejo de `connectors/`).
> FLOOR skills Fase 1 **pieza 1 = el MECANISMO** (las 3 skills neutrales = pieza 2, GO posterior). Off-by-default.
> NO toca `protocol.config.json`/genesis/#4. Una skill es TEXTO inerte; el loader es solo lectura.

## Alcance (SPEC-0096 AC1-AC6)
- **Capa `skills/`** neutral: framework + loader + registro. Domain-neutral (sin terminos de dominio).
- **`skills/skills.config.json`** FUERA del config pinned, `schema_version:"skills.config.v1"`, cada skill con
  `id`/`title`/`profile` (o `neutral_core`)/`path`/`version`/`enabled:false` + `trust_boundary`
  (`read_only:true`,`grants_no_authority:true`,`persists_outputs:false`).
- **Skill = doc gobernado:** frontmatter (`skill_id`,`title`,`profile`,`version`,`neutral_core`) + body (procedimiento).
- **Loader cold-start** DETERMINISTA y READ-ONLY: resuelve enabled, valida trust_boundary + ubicacion, devuelve
  indice/contenido en memoria; sin escritura de estado/ledger/event-log.
- **Golden `examples/skills_loader_cases/`** con registro + skills de ejemplo NEUTRALES (del mecanismo, no dominio).
- **CI** cubre el golden; `scan_domain_neutrality` cubre `skills/`.

## DoD (criterios de aceptacion = SPEC-0096 AC1-AC6)
- AC1 registro fuera del config pinned, default disabled, #4/genesis intacto, drift 0.
- AC2 loader read-only determinista (enabled->procedimientos; todo disabled->vacio; sin escritura).
- AC3 no concede autoridad: loader NO importa escritores ledger/event-log (test de imports); contenido inerte.
- AC4 neutralidad del mecanismo + skill de dominio ubicada en el core = RECHAZADA (fail-closed).
- AC5 off-by-default fail-closed: registro ausente/disabled -> vacio sin error; entrada malformada rechazada.
- AC6 gates: validate exit 0 (con/sin secretos) clon limpio, drift 0, scan_encoding/neutrality exit 0, golden
  verde, CI cubre el golden, Co-Authored-By Codex.

## Fuera de alcance
- Las 3 skills de contenido (pieza 2): convenciones DDL / regla-negocio-vs-legacy / verificacion-migracion en
  `profiles/financiero_presupuesto/skills/` (GO posterior tras cerrar esta).
- Capacidad ejecutable via skills; inyeccion en tareas/handoffs; superficie en el front; tocar genesis/#4/config.

## Notas
- Espeja el patron de `connectors/` (capa separada, registro fuera del config, off-by-default, fail-closed,
  no importa escritores). Diferencia: una skill es texto inerte (sin "uso vivo" riesgoso), por eso no requiere s9+GO.
