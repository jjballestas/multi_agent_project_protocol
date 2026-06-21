# DRAFT - Extension 10 de SPEC-0086: carga por archivo v2 (extraccion=agente, revision, selector de modo) [AC40..AC43]

> DRAFT en personal/Arquitecto; NO promovido. Triage del REQ-D642E4D8 (#1 operador). Bajo DECISION-0056 (OPCION 4).
> SUPERSEDE el flujo de REQ-31100EAF v1. maker=Codex / checker=Arquitecto + Analista. Codigo en Zeus. OFF-by-default.
> Dimensionado en FASES (pieza grande = el loop de extraccion); se promueven de a una.

## Origen (REQ-D642E4D8, author=Operador)
Subir archivo libre -> el sistema extrae historias/casos -> candidatos -> panel de revision (validar/editar) ->
solo aprobados al intake gobernado -> SPEC. + selector de modo (digitado vs archivo) validando obligatorios en
ambos. Guardas de ingestion intactas. Mecanismo = OPCION 4 (server no-egress; extraccion = trabajo de agente).

## AC40 - Upload gobernado server-NO-EGRESS: ruta acotada + PII-gate-en-ingest + emite tarea de extraccion [PERMANENTE; DECISION-0056]
El upload es accion gobernada server-side: (a) **PII-gate en el INGEST** -- screening estructural por patrones +
ASCII ANTES de guardar/antes de que un agente lo toque (honesto: best-effort, NO PII-free garantizado; DEF-PII
sigue gate); (b) guarda el archivo en RUTA ACOTADA server-derived (`Area_comun/intake/uploads/<id>/<saneado>`),
GITIGNORED/efimera, FUERA del dataset atestado; nombre saneado (sin traversal), allowlist tipo + limite tamano
(hereda AC37/AC38); contenido INERTE; (c) emite una **TAREA de extraccion** via el camino gobernado. **El server
NO llama a ningun modelo/LLM (NO-EGRESS)** -- el evento atestado solo registra "archivo subido (hash) + extraccion
pedida". #4 byte-identica. Test de comportamiento + PRUEBA NEGATIVA: el server no hace ninguna llamada saliente a
un modelo; tipo/tamano/traversal -> rechazado; PII-gate corre antes de persistir.

## AC41 - Extraccion = trabajo de AGENTE -> candidatos FUERA del backlog -> solo aprobados al intake [PERMANENTE; DECISION-0056]
La extraccion (archivo -> historias candidatas) la hace un **AGENTE** que toma la tarea (no el server). Las
candidatas viven en estado **`candidate`** como artefacto FUERA de PROPOSED/TASK_INDEX (no ensucian el backlog).
El operador las revisa/edita/aprueba en un **panel de revision**. Solo las **APROBADAS** pasan por el
`requirement-intake` EXISTENTE (execute gobernado, determinista, atestado) con la validacion honesta **AC39**
(no vacios/placeholder; proyecto explicito). Nada entra al dataset sin aprobacion del operador. El no-determinismo
del LLM queda FUERA de #4. Test: una candidata aprobada -> requirement real (id+seq) por el intake; una candidata
sin aprobar -> NO esta en el backlog ni atestada.

## AC42 - Selector de modo (digitado vs archivo) con validacion de obligatorios en ambos [PERMANENTE; REQ-D642E4D8]
Antes de crear, el operador elige el MODO: (a) "Nueva historia digitada" -> campos actuales; (b) "Por carga de
archivo" -> flujo de upload+extraccion. En AMBOS modos se validan los **obligatorios** antes de EXECUTE (carry
AC39: sin vacios/placeholder; proyecto explicito). Conforme al design-system (AC13). Test: cada modo expone su
flujo; ninguno permite EXECUTE con obligatorios vacios/placeholder.

## AC43 - Anti-abuso de la ingestion v2 (prueba negativa PERMANENTE) [CRITICO; DECISION-0056]
Tests permanentes (no reabrir): el server **NO hace egress** (no llama a ningun modelo) -- falsable; ruta de
uploads acotada/saneada, sin traversal, gitignored, FUERA del dataset; contenido INERTE (nunca ejecutado);
candidatas `candidate` NO entran a PROPOSED/atestado sin aprobacion; el cliente NO inyecta actor/rutas; PII-gate
corre en el ingest antes del agente; #4 byte-identica (config/genesis/keys sin cambio). OFF-by-default.

## FASES propuestas (promover de a una; cada una su TASK)
- **Fase A (plumbing determinista):** AC40 (upload gobernado: PII-gate + ruta acotada + emit extraction-task,
  no-egress) + AC42 (selector de modo + validacion). Entrega ya, sin depender del agente.
- **Fase B (candidatos + revision):** AC41 estado `candidate` + panel de revision + aprobar -> intake gobernado.
- **Fase C (loop de extraccion):** atar la tarea de extraccion a un agente que produce candidatas (define el
  contrato de la tarea de extraccion; el agente es el de siempre, LLM-backed). 

## test_plan
- Server (Zeus): upload -> PII-gate -> ruta acotada + extraction-task emit; PRUEBA NEGATIVA no-egress (ninguna
  llamada saliente a modelo); negativos tipo/tamano/traversal; #4 byte-identica.
- Front: selector de modo; panel de revision (candidate -> editar/aprobar); aprobar -> intake AC39 -> requirement
  real; candidatas no-aprobadas no estan en backlog.
- Gates: validate con/sin secretos exit 0; drift 0; npm test verde EN CLON LIMPIO; neutralidad/encoding 0.

## Carry permanentes
AC11 / AC13 / AC17 / AC19 / AC22 / AC37 / AC38 / AC39. #4 epoca 1.14.0 byte-identica. OFF by default; uso vivo =
env; pasada del Analista (ingest/egress/PII) antes de cerrar.
