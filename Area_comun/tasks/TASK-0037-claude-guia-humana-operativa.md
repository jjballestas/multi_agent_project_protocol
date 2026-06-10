---
id: TASK-0037
owner: Claude
status: done
type: documentation
priority: normal
created_at: 2026-06-06
updated_at: 2026-06-10
depends_on: []
relates_to: [TASK-0004, TASK-0013, SPEC-0072]
phase: P2
spec_id: Area_comun/specs/SPEC-0072-guia-humana-operativa-generador-html.md
linked_decisions: [DECISION-0004, DECISION-0019, DECISION-0001, DECISION-0020, DECISION-0006]
sdd_required: true
objective: Formalizar el contrato minimo de documentacion humana operativa, neutral de dominio y reusable por cualquier instancia: un esquema de 21 secciones fijas (SPEC-0072 sec.4) cuya fuente de verdad es un .md estructurado y cuyo HTML es un artefacto generado determinista (nunca editado a mano). Aditivo, MINOR, off-by-default; NO toca runtime ni defaults del template.
expected_output: (ARQUITECTO) plantilla master neutral Area_comun/protocol/HUMAN_GUIDE.template.md con las 21 secciones, marcadores obligatorio/opcional/no-aplica, [CORE]/[INSTANCIA], tier-awareness y placeholders <...>; *.template.* anadido a neutrality.scan_globs y las versiones llenas a exempt_globs; README_INSTANCIACION.md actualizado (SPEC sec.11). (IMPLEMENTADOR, tarea separada) scripts/generate_human_guide.py + .ps1 (stdlib-only, determinista, --check drift + validacion de esquema integrada), golden en examples/human_guide_cases/, cableado en CI + githook. (GENERACION) examples/human_guide_instance/HUMAN_GUIDE.example.{md,html} y la guia dogfooding HUMAN_GUIDE.{md,html} en la raiz, ambos via el generador.
question_to_resolve: RESUELTO (SPEC-0072 sec.13): (1) ubicacion = plantilla en Area_comun/protocol/, guia llena en RAIZ, ejemplo en examples/, sin arbol docs/; (2) idioma canonico = espanol, esquema agnostico de idioma; (3) validador integrado en el generador (--check).
closure_criterion: golden 100% verde; neutralidad 0 sobre los *.template.*; encoding limpio; --check verde (drift MD<->HTML detectado); determinismo confirmado (mismo MD -> HTML byte-identico); las 21 secciones presentes en la plantilla con sus tipos de campo; generador + .ps1 + golden + gates cableados; README actualizado; ejemplo lleno + guia dogfooding de esta instancia generada (via el generador, nunca HTML a mano); ratificado adversarialmente (neutralidad + determinismo + no-drift). TASK-0037 -> done con handoff + FYI.
---

# TASK-0037 - Guia humana operativa neutral + HTML

## Intencion
Dejar como trabajo futuro la ultima capa de documentacion para usuarios humanos: una guia que explique
como entender, construir, lanzar, probar y operar una aplicacion gestionada con esta metodologia.

## Alcance futuro
- Definir una plantilla neutral de dominio para la guia humana operativa.
- Incluir secciones esperadas:
  - arquitectura del proyecto/aplicacion;
  - como construir;
  - como ejecutar localmente;
  - como probar;
  - como desplegar/lanzar;
  - operacion diaria;
  - troubleshooting;
  - rutas/protocolos relevantes;
  - roles/capacidades configuradas en la instancia, sin atarlo a Claude/Codex.
- Proveer un formato HTML legible por humanos, ademas del formato markdown/source.
- Documentar en `README_INSTANCIACION.md` cuando y como debe completarse en una instancia.

## No-alcance
- No definir dominio de negocio.
- No introducir reglas especificas de stack en el core.
- No acoplar la guia a dos agentes concretos.

## Nota
El operador pidio dejarlo como futuro trabajo para evitar que esta capa quede desactualizada mientras
se termina la metodologia.
