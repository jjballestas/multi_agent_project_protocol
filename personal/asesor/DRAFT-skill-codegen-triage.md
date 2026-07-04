# DRAFT (diseno del Asesor) - skill codegen-triage + recetas de instancia Nova

> Diseno para que el Arquitecto lo rutee y Codex-maker/Analista-checker lo creen. El Asesor DISENA,
> no instala ni gobierna. Split en 2 capas para respetar la neutralidad del core (CLAUDE.md regla 1).
> Origen: pregunta del operador 2026-07-04 (Codex debe analizar cuando usar codegen; hay mucho del
> build que aplica). Runbook operativo de referencia: TEMP_Guia_Modelos_Peones_y_Medicion.md s.1/s.5
> (personal/ungobernado; esta skill es la version gobernada de su regla de decision, sin el peon).

## CAPA NEUTRAL - skill `codegen-triage` (metodologia, sin dominio)

PROPOSITO: dada una tarea de desarrollo, clasificar el CAMINO DE GENERACION antes de codificar, para
no gastar criterio (ni tokens) en trabajo que una fuente determinista + un gate resuelven.

TRIGGER WORDS: codegen, scaffold, plantilla, generar, boilerplate, CRUD, DTO, mapper, cliente OpenAPI,
mecanico, repetitivo, "por cada tabla", triage de generacion, delegar, que hago a mano.

PROCEDIMIENTO (el firmante responsable de la tarea lo aplica; el decide porque el firma):
1. FUENTE DETERMINISTA? La salida es funcion MECANICA y TOTAL de una fuente (esquema de tabla,
   entidad, contrato OpenAPI, DDL)? Test literal: "por cada X, emite estos N archivos rellenando
   estos huecos". Si SI -> candidato a CODEGEN (cero tokens, cero alucinacion, misma entrada=misma salida).
2. ORACULO DETERMINISTA? La correctitud se comprueba con un GATE automatico (build + tests + arch-tests
   + paridad + lint/format), NO con criterio humano? Requisito DURO para codegen y para CUALQUIER
   delegacion: "solo delega/genera lo que un gate verde puede comprobar, no lo que exige criterio".
   Si 1 y 2 = SI -> CODEGEN.
3. VARIACION PEQUENA que la plantilla no captura (renombrar a lenguaje de dominio, una validacion de
   rango) -> candidato a ASISTENCIA AUTORIZADA (peon) SOLO donde una DECISION lo permita (DECISION-0078)
   y NUNCA en brazos medidos del estudio; maker!=checker; gate verde + firma. (Fuera del alcance de
   esta skill en su version inicial: la skill decide codegen-vs-frontera; el peon es capa aparte.)
4. BANDERAS ROJAS -> lo hace el FIRMANTE FRONTERA (no codegen, no delegable). La tarea deja de ser
   "mecanica" si: compone >1 mutacion; llama procesos/servicios en SECUENCIA; CRUZA frontera de modulo;
   toca contexto de sesion/tenant o saldos/cuadres; depende de una vista/artefacto con brecha conocida;
   o implica logica de negocio, seguridad o migraciones con trazabilidad.

REGLA DE ORO: el ahorro solo existe si revisar/generar es mas barato que escribir con criterio. Una
"superficie" es mecanica SOLO si es 1-fuente/1-salida sin secuencia de mutaciones ni dependencia con brecha.

SALIDA de la skill: para la tarea -> {camino: codegen | frontera | (asistencia-autorizada si aplica),
razon, gate que la verifica, banderas rojas detectadas}.

## CAPA DE INSTANCIA NOVA - recetas (el "como"; NO va en el core neutral)

Vive en la instancia Nova (Aegis/ o tooling del producto), no en la skill neutral:
- `dotnet new` template-pack: slice CRUD (Controller + UseCase + DTO + test) instanciado por entidad/modulo.
- EF Core scaffold: entidades + DbContext desde la BD existente (tablas de parametros).
- Roslyn Source Generators: DTO mappers / codigo pegamento en tiempo de compilacion (cero runtime).
- NSwag / openapi-generator: cliente tipado + DTOs desde el contrato REST versionado.
- GATE de instancia: `dotnet build` + `dotnet test` (unit + golden del slice) + architecture-tests
  (no salta capas) + paridad EXEC-vs-endpoint + `dotnet format` + scan ASCII (si toca canales del protocolo)
  + guard "sin logica de negocio / sin dependencias nuevas" (grep de patrones prohibidos).

## Restriccion de integridad del estudio (para el sello)
- CODEGEN != PEON. El codegen es practica estandar de un solo dev competente: NO anade agentes (respeta
  el mono-orquestador), NO produce tokens, NO es el tratamiento. Es LEGITIMO en AMBOS brazos, incluido GOAL-P1.
- Constraint: uso SIMETRICO por par (mismo tooling de codegen disponible/aplicado en el miembro baseline y
  el gobernado de un mismo par). El patron-congelado (P4.1) + aislamiento-intra-par ya lo fuerzan; hacerlo
  explicito en la definicion del brazo evita un confound de asimetria de tooling.
- Cero peones en brazos medidos se mantiene (esto NO lo toca).
- A SELLAR: una linea en la definicion del brazo baseline: "codegen/scaffolding determinista = practica de
  dev competente, presente en ambos brazos, simetrica por par; no es el tratamiento".

## Carril / ownership
- USA: Codex durante el desarrollo. CREA: Codex-maker / VERIFICA: Analista-checker. GOBIERNA: Arquitecto.
- El Asesor DISENA (este draft) y RUTEA; no instala la skill ni la gobierna.
- Neutralidad: la capa neutral NO menciona .NET/Nova; las recetas .NET viven en la instancia (regla 1 CLAUDE.md).
