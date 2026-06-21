# DRAFT - DECISION-0056: Carga por archivo v2 - extraccion = trabajo de AGENTE (server no-egress) (OPCION 4)

> DRAFT en personal/Arquitecto; NO promovido. Espera ratificacion. Origen: REQ-D642E4D8 (intake del operador, #1).
> SUPERSEDE el mecanismo de REQ-31100EAF v1 (solo adjuntaba). Mecanismo elegido por el operador: OPCION 4.
> maker=Codex / checker=Arquitecto + PASADA DEL ANALISTA (ingest/egress/PII) al cierre. OFF-by-default.

## status
proposed

## Contexto
REQ-D642E4D8 (v2): el operador quiere subir un archivo libre (sin formato), que el sistema EXTRAIGA historias/
casos de uso y genere requisitos CANDIDATOS, revisarlos/editarlos en un panel, y que solo los APROBADOS pasen al
intake gobernado -> SPEC. La v1 (REQ-31100EAF) solo adjuntaba y obligaba a teclear todo (acceptanceIntent vacio
-> 400). La pieza grande es la EXTRACCION (archivo libre -> candidatos).

## Trilema y su disolucion (OPCION 4 del operador)
El riesgo: si el SERVER extrae con un LLM, eso es EGRESS del contenido (rompe la guarda "sin egress" + el dataset
PII-free + el determinismo #4). OPCION 4 lo disuelve: **el server NO extrae nada.**

## Decision (OPCION 4)
1. **Subir = accion gobernada, server NO-EGRESS, determinista, #4-limpia.** El upload: (a) **PII-gate en el
   INGEST** (screening estructural por patrones + ASCII ANTES de guardar / antes de que un agente lo toque; el
   archivo es contenido EXTERNO nuevo, puede traer PII de terceros; honesto: NO se afirma PII-free garantizado --
   best-effort por patrones, DEF-PII/TASK-0118 sigue siendo el gate); (b) guarda el archivo en una **RUTA ACOTADA
   server-derived** (p.ej. `Area_comun/intake/uploads/<id>/<archivo-saneado>`) GITIGNORED/efimera, FUERA del
   dataset atestado; (c) emite una **TAREA de extraccion** ("leer archivo X, extraer historias/casos, generar
   candidatas"). El evento atestado solo registra "archivo subido (hash/ruta) + extraccion pedida": determinista,
   sin egress, #4-byte-identica.
2. **Extraccion = trabajo de AGENTE (no superficie del server).** Un agente (Codex u otro, ya LLM-backed) toma la
   tarea y extrae -> historias candidatas. El LLM vive DONDE YA VIVE (los agentes procesando el dataset); NO es
   un egress nuevo del server. El no-determinismo del LLM queda FUERA de #4 (mismo patron que los SPECs: el agente
   genera no-deterministicamente, el write gobernado es determinista y gateado por humano/checker).
3. **Estado `candidate` FUERA del backlog.** Las candidatas viven como artefacto `candidate` (NO en PROPOSED,
   no ensucian el backlog ni el TASK_INDEX). El operador las consulta/revisa/edita/aprueba en un **panel de
   revision**.
4. **Solo APROBADAS -> intake gobernado actual.** Una candidata aprobada pasa por el `requirement-intake` EXISTENTE
   (execute gobernado, determinista, atestado), con la validacion honesta AC39 (no vacios/placeholder; proyecto
   explicito). Nada entra al dataset sin aprobacion del operador.
5. **OFF BY DEFAULT, reversible por flag** (registro fuera del config pinned, patron DECISION-0054/0055). Uso vivo
   por entorno; la extraccion ata a que un agente este en el loop (no es instantaneo).

## Por que respeta las fronteras
- Server **no-egress / determinista / #4-limpio**: tu guard intacto. Lo atestado solo es lo que el operador
  aprueba, por el intake determinista. PII-free preservado por el gate-en-ingest + redaccion + intake guards.
- El LLM no es una superficie nueva: es trabajo de agente, ya aceptado por la metodologia.

## Threat model (resumen)
PII de terceros en el archivo -> screening estructural + ASCII en el INGEST (antes del agente); raw upload
gitignored/efimero, fuera del dataset; honesto (no PII-free garantizado). Nombre/ruta -> saneado, acotado,
sin traversal. Contenido -> dato INERTE (nunca ejecutado por el server). Candidatas no-aprobadas -> NO entran al
dataset (fuera de PROPOSED). Egress del server -> NO existe (el server no llama a ningun modelo). Fantasma/
placeholder al aprobar -> AC39 (intake honesto). Encendido sin querer -> off-by-default.

## Alcance / limites
- El server NO llama a ningun LLM (descartada la opcion "server hace egress"). 
- Solo .md/.txt, allowlist + limite de tamano (hereda AC37/AC38). 
- Retencion/limpieza de la ruta de uploads: definir (efimera; purga tras aprobar/descartar).

## Consecuencias
Nueva accion de producto (upload + emit extraction-task) + estado candidate + panel de revision en Zeus; una
tarea de extraccion para un agente. Supersede el flujo v1. El core sigue neutral. Activacion viva = env;
pasada del Analista (ingest/egress/PII) al cierre.

## Condiciones de cierre (innegociables)
(a) server NO-EGRESS (no llama a ningun modelo; prueba negativa permanente); (b) PII-gate en el INGEST antes de
guardar/antes del agente (test); (c) ruta de uploads acotada, saneada, gitignored, fuera del dataset; (d) estado
candidate FUERA de PROPOSED; solo aprobadas -> intake gobernado AC39; (e) #4 byte-identica (el upload solo registra
"subido + extraccion pedida"); (f) off-by-default, reversible por flag; (g) validate con/sin secretos exit 0,
drift 0, npm test verde EN CLON LIMPIO; (h) PASADA DEL ANALISTA (ingest/egress/PII) ANTES de cerrar.
