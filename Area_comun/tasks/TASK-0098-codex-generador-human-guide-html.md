---
id: TASK-0098
owner: Codex
status: ready
type: implementation
priority: normal
created_at: 2026-06-10
updated_at: 2026-06-10
depends_on: [TASK-0037]
relates_to: [TASK-0037, SPEC-0072]
phase: P2
spec_id: Area_comun/specs/SPEC-0072-guia-humana-operativa-generador-html.md
linked_decisions: [DECISION-0004, DECISION-0019, DECISION-0001, DECISION-0006]
objective: (IMPLEMENTADOR, bajo SPEC-0072 sec.5/8/9) Construir el generador determinista .md -> .html de la guia humana operativa + su validador integrado (--check) + golden + cableado a gates, sobre la plantilla master que ya redacto el arquitecto (Area_comun/protocol/HUMAN_GUIDE.template.md, 21 secciones). Aditivo, MINOR, off-by-default; NO toca runtime ni defaults del template.
expected_output: (1) scripts/generate_human_guide.py (+ scripts/generate_human_guide.ps1 paridad, wrapper que delega como generate_*): stdlib-only, determinista (mismo MD -> HTML byte-identico), SIN red, SIN JS/CDN, SIN timestamp embebido salvo el del frontmatter. Parsea frontmatter (nombre/estado/protocol_version/runtime_version/adoption_tier/perfiles/idioma) + las 21 secciones + lineas de metadatos `<!-- origen: ... | tier: ... | campo: ... -->` + checklists `- [ ]` + callouts `> [SEGURIDAD]` + placeholders `<...>`. (2) Render HTML autocontenido estilo casa (como Area_comun/reports/*.html si existe, o REPORT-style): <!DOCTYPE> + <style> INLINE, header de identidad, bloque panorama arriba, indice navegable por anclas en CSS puro, badges obligatorio/opcional/no-aplica, checklists, callouts de seguridad, layout imprimible, banner "GENERADO - NO EDITAR". (3) Modo --check: regenera en memoria y compara byte a byte -> exit!=0 si drift. (4) VALIDACION DE ESQUEMA integrada: seccion obligatoria ausente / placeholder `<...>` en guia *live* (no en plantilla/ejemplo) / tier que exige seccion ausente -> exit!=0 con diagnostico; tier-aware (lee adoption_tier del frontmatter o protocol.config.json -> secciones solo-runtime = no-aplica en coordination). (5) Golden determinista en examples/human_guide_cases/ (render byte-identico, --check detecta drift, validacion: obligatoria-ausente fail / placeholder-en-live fail / tier-coordination no-aplica, plantilla/ejemplo con placeholders pass, paridad .py/.ps1). (6) Cablear --check en .github/workflows/validate.yml (CI) y .githooks/pre-commit (local). validador/neutralidad/encoding verdes; determinista en CI; sin secretos; cross-platform.
question_to_resolve: Q1 estilo HTML: reusar el CSS/estructura de los reportes HTML de la casa si existe un patron, o definir uno minimo inline coherente. Q2 fuente del adoption_tier para el tier-awareness (frontmatter de la guia vs protocol.config.json) y precedencia. Si la plantilla necesita un ajuste de estructura para ser parseable de forma robusta -> blocked + nota al arquitecto (NO cambiar el esquema de 21 secciones ni la neutralidad).
closure_criterion: generate_human_guide.py + .ps1 + golden examples/human_guide_cases/ 100% verde; --check verde (drift detectado); determinismo confirmado (byte-identico); validacion de esquema correcta (obligatoria/placeholder-live/tier); cableado en CI + githook; neutralidad 0 sobre los *.template.* (incluido el HTML de la plantilla generado); encoding limpio; stdlib-only; paridad .py/.ps1; sin secretos; handoff con evidencia. El ejemplo (examples/human_guide_instance/HUMAN_GUIDE.example.{md,html}) y la guia dogfooding de la raiz se generan via el generador (paso de cierre, lo coordina el arquitecto). NO re-armar SA.4 ni piloto.
sdd_required: true
---

# TASK-0098 - Generador determinista de la guia humana operativa (.md -> .html)

> READY+GO (Claude 2026-06-10, bajo SPEC-0072, GO del operador). Aditivo MINOR off-by-default.
> El arquitecto ya redacto la plantilla master Area_comun/protocol/HUMAN_GUIDE.template.md (21 secciones,
> neutral, con lineas de metadatos parseables) + neutrality globs + README. Tu construyes el generador.
> NEUTRAL innegociable; *.template.* son masters (regla 5); sin secretos; claim + staging por paths.
> enforce/authoritative intactos; SA.4/Capa C OFF.

## Alcance (SPEC-0072 sec.5, 8, 9)

generate_human_guide.py (+ .ps1) stdlib-only determinista, --check (drift + validacion de esquema),
golden en examples/human_guide_cases/, cableado en CI + githook. Ver el frontmatter de esta task y SPEC
para el detalle.

## Restricciones (duras)

- Fuente de verdad = el .md; HTML = artefacto generado, NUNCA editado a mano (banner). Determinista,
  stdlib-only, sin red/JS/CDN. Paridad .py/.ps1. Neutral. Off-by-default, aditivo, reversible. enforce+
  authoritative ON: todo cambio de estado por submit_intent. 1 commit/turno con rutas explicitas. NO
  cambiar el esquema de 21 secciones ni los defaults del template; si la plantilla no es parseable de
  forma robusta -> blocked + nota al arquitecto.
