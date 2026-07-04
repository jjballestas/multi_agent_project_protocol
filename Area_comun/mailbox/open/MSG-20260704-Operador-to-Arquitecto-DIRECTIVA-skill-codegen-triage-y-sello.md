---
message_id: MSG-20260704-Operador-to-Arquitecto-DIRECTIVA-skill-codegen-triage-y-sello
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - personal/asesor/DRAFT-skill-codegen-triage.md (diseno de referencia del Asesor; requisitos abajo, no copiar verbatim)
  - Area_comun/decisions/DECISION-0078-medicion-peones-ab-c-sandbox.md (peon = capa aparte; esta skill decide codegen-vs-frontera)
  - TASK-0245 (patron neutral+instancia skill) + CLAUDE.md regla 1 (neutralidad del core)
one_line_summary: "Dos acciones aprobadas por el Operador: (1) CREAR la skill gobernada codegen-triage (capa NEUTRAL: decidir cuando una tarea es mecanico-total -> codegen vs frontera; + recetas de INSTANCIA Nova aparte, fuera del core neutral); Codex-maker / Analista-checker; la usa Codex durante el desarrollo. (2) SELLAR en la definicion del brazo baseline la clarificacion codegen != peon: el codegen determinista es practica de dev competente, presente en AMBOS brazos (incl GOAL-P1), simetrico por par, NO es el tratamiento; cero peones en brazos medidos se mantiene. Antes del 08-jul."
requested_action: "[DIRECTIVA] Dos acciones aprobadas por el Operador (2026-07-04). ACCION 1 -- CREAR SKILL codegen-triage como tarea gobernada (owner Codex-maker / checker Analista; NO owner Analista). Requisitos (self-contained; el diseno completo esta en personal/asesor/DRAFT-skill-codegen-triage.md como referencia, no lo copies verbatim, extrae requisitos): (a) CAPA NEUTRAL (sin dominio, apta para exportar): dada una tarea de desarrollo, clasifica el camino de generacion -- 1) fuente determinista + funcion mecanica-y-total (esquema/entidad/contrato) con test 'por cada X emite N archivos rellenando huecos' -> CODEGEN; 2) requisito duro: correctitud comprobable por GATE determinista (build/test/arch-test/paridad), no por criterio; 3) banderas rojas que descalifican 'mecanico' y mandan al FIRMANTE FRONTERA: compone >1 mutacion, llama procs en secuencia, cruza frontera de modulo, toca contexto de sesion/tenant o saldos/cuadres, depende de vista/artefacto con brecha, o implica logica de negocio/seguridad/migracion con trazabilidad; 4) quien decide = el firmante responsable de la tarea, que define el gate. El peon queda FUERA del alcance inicial (capa aparte, DECISION-0078). (b) CAPA DE INSTANCIA NOVA (recetas, FUERA del core neutral, regla 1 CLAUDE.md): dotnet new template-pack del slice CRUD, EF Core scaffold, Roslyn SG, NSwag/openapi-generator, y el gate de instancia (dotnet build/test + architecture-tests + paridad EXEC-vs-endpoint + format + scan ASCII + guard sin-logica-de-negocio). (c) La USA Codex durante el desarrollo de Nova; aplica DESDE GOAL-P1/P2 (scaffolding sln/proyectos, EF scaffold de tablas de parametros, cliente OpenAPI). ACCION 2 -- SELLAR clarificacion de integridad del estudio en la definicion del brazo baseline (antes del 08-jul): 'codegen/scaffolding DETERMINISTA = practica de dev competente de un solo dev; NO anade agentes (respeta el mono-orquestador), NO produce tokens, NO es el tratamiento; es LEGITIMO en AMBOS brazos incluido GOAL-P1, con uso SIMETRICO por par (el patron-congelado P4.1 + aislamiento-intra-par ya lo fuerzan; hacerlo explicito evita un confound de asimetria de tooling)'. CERO PEONES en brazos medidos se MANTIENE intacto (esto no lo toca). RESPONDE con: (a) id de la tarea de la skill registrada en el hub; (b) confirmacion de que la clarificacion codegen!=peon queda capturada para el sello del brazo baseline."
question: ""
---

# DIRECTIVA - Skill codegen-triage (crear) + sellar la regla codegen != peon

El Operador acepto: no peones en la ventana medida, PERO Codex debe analizar cuando una tarea es
mecanico-total y usar CODEGEN -- hay mucho del build de Nova que aplica. Dos acciones:

## Accion 1 - Crear la skill gobernada `codegen-triage`
Tarea gobernada, owner Codex-maker / checker Analista. Diseno de referencia (no verbatim) en
personal/asesor/DRAFT-skill-codegen-triage.md. En dos capas:
- **Neutral** (exportable, sin dominio): decide codegen-vs-frontera con el test mecanico-total, el
  requisito de gate determinista, y las banderas rojas (composicion / cruce de modulo / sesion-tenant /
  saldos / brecha / logica-seguridad-migracion). El peon queda fuera (capa aparte, DECISION-0078).
- **Instancia Nova** (recetas, fuera del core neutral por regla 1): dotnet new / EF scaffold / Roslyn SG /
  NSwag + el gate de instancia.
La usa Codex durante el desarrollo; aplica desde GOAL-P1/P2.

## Accion 2 - Sellar codegen != peon en la definicion del brazo baseline (antes del 08-jul)
Clarificacion: el codegen determinista es practica de dev competente de UN dev (no anade agentes, cero
tokens, NO es el tratamiento); es legitimo en AMBOS brazos incluido GOAL-P1, con uso SIMETRICO por par.
Cero peones en brazos medidos se mantiene intacto.

Responde con: id de la tarea de la skill + confirmacion de la clarificacion sellada.
