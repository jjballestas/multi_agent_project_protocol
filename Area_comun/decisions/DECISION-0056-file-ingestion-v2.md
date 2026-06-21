---
decision_id: DECISION-0056
title: Carga por archivo v2 - extraccion = trabajo de AGENTE (server no-MODELO-egress) + gate humano duro de PII + candidatas no-ledger (OPCION 4)
status: accepted
ratified_at: 2026-06-22
date: 2026-06-22
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
amends: [DECISION-0055]
relates_to: [DECISION-0055, DECISION-0051, DECISION-0052, DECISION-0040, DECISION-0049]
phase: P2
---

# DECISION-0056 - Carga por archivo v2 (OPCION 4): extraccion=agente, server no-MODELO-egress, PII gate humano duro

> ACCEPTED por el operador (2026-06-22). Origen: REQ-D642E4D8 (#1). SUPERSEDE el mecanismo de REQ-31100EAF v1.
> Mecanismo = OPCION 4 del operador + 2 decisiones (D-PII, D-ACTOR) tras red-team adversarial (38/40 confirmados,
> artefacto REDTEAM-ingestion-v2-OPCION4-veredicto.md). maker=Codex / checker=Arquitecto + PASADA DEL ANALISTA
> (ingest/egress/PII) al cierre. OFF-by-default; uso vivo por entorno.

## Contexto
v2: subir un archivo libre, EXTRAER historias/casos y generar requisitos CANDIDATOS, revisarlos/editarlos/
APROBARLOS en un panel, y que solo los APROBADOS pasen al intake gobernado -> SPEC. La v1 solo adjuntaba.

## Mecanismo (OPCION 4 del operador): el SERVER NO EXTRAE
1. **Upload = accion gobernada, server NO-MODELO-EGRESS, determinista, #4-limpia.** El server NO llama a ningun
   endpoint de MODELO/inferencia (sin sockets a hosts de LLM, sin SDK de modelo, sin API key de modelo). [NOTA:
   el server SI hace `git push` gobernado del intake -- eso es transporte existente DECISION-0054, no egress a un
   modelo; la garantia es ESTRECHA: "no llama a un modelo", NO "cero egress".]
   El upload: (a) corre un **screening de PII REAL best-effort** sobre el contenido (patrones de email, telefono,
   documento/cedula, NIT, razon social, SQL/schema, y nombres propios heuristicos) + ASCII; HONESTO: best-effort,
   **NO se afirma "PII-free garantizado" ni "ningun LLM ve PII"** (estructuralmente inalcanzable por patrones);
   (b) guarda el archivo en un **STORE FUERA DEL DATASET ATESTADO** (tmp del SO / area gitignored entregada con su
   linea `.gitignore` en el mismo commit y EXCLUIDA del git-status del indicador canonico), ruta server-derived
   acotada, nombre saneado (sin traversal), allowlist tipo (.md/.txt) + limite de tamano (hereda AC37/AC38),
   contenido INERTE; el **hash atestado** del archivo es **SHA-256 sobre los BYTES CRUDOS** (no FNV-32 ni sobre
   texto saneado); (c) emite una **TAREA de extraccion** con CONTRATO AUTOCONTENIDO (ruta del archivo, formato de
   salida de candidatas, criterio de done) via `task_upsert` con status YA VALIDO -- NO se crea ningun intent
   kind ni status nuevo (eso seria cambio de runtime, regla 2, fuera de alcance). El evento atestado solo registra
   "archivo subido (sha256) + extraccion pedida". **Idempotente** por (sha256-bytes + project): re-subir identico
   no emite nueva tarea.
2. **Extraccion = trabajo de AGENTE; su frontera de egress se ACOTA.** Un agente LLM-backed toma la tarea y
   extrae -> candidatas. RECONOCIDO HONESTAMENTE: el agente LEE el archivo externo (post best-effort screening);
   si el agente corre en un modelo hospedado, el contenido (con la PII que los patrones no atraparon) cruza al
   proveedor. Por eso: el upload **etiqueta/consiente** que el archivo sera leido por el agente extractor y lo
   registra; el operador asume esa ventana (mitigada por el screening best-effort + el gate humano del paso 4).
   El no-determinismo del LLM queda FUERA de #4.
3. **Candidatas en STORE NO-LEDGER, fuera del backlog.** Las candidatas viven en un store gitignored FUERA del
   dataset (mismo trato que uploads), con **ciclo de vida propio que NO es `task_status`** (el estado `candidate`
   NO existe en VALID_TASK_STATUSES y NO se agrega): el ledger atestado NUNCA ve `candidate`; no tocan
   TASK_INDEX/PROJECT_STATE; drift 0 con candidatas presentes.
4. **GATE HUMANO DURO de PII + aprobacion por candidata.** El operador revisa/edita CADA candidata en el panel y,
   para aprobarla, **DECLARA explicitamente que reviso PII** (atestacion humana por-candidata). Solo entonces la
   candidata pasa por el `requirement-intake` EXISTENTE (execute gobernado, determinista, atestado) con AC39
   (no vacios/placeholder; proyecto explicito) + **re-screening de PII** en la frontera candidate->intake. El
   **id/idempotency** del requirement aprobado deriva del **CONTENIDO EDITADO** (title+narrative+intent+project),
   NO del archivo (evita colision al aprobar N candidatas del mismo upload). El `narrative` aprobado se atesta en
   #4 (IRREVERSIBLE) -> por eso la declaracion humana de PII es el gate duro antes del write inmutable.
5. **Atribucion (D-ACTOR): RELAY HONESTO como Arquitecto.** El evento de upload/intake va con author=Operador /
   relayed_by=Arquitecto / endorsement=none (firmante=Arquitecto pinned), igual que el intake actual. NO se toca
   `agent_registry` ni keys -> **#4 epoca 1.14.0 BYTE-IDENTICA, sin re-genesis**.
6. **Trazabilidad de procedencia (PII-free, determinista).** El requirement aprobado lleva metadato de procedencia:
   sha256 del archivo origen + id de la extraction-task + hash del candidato PRE-edicion (evidencia de que hubo
   revision humana). Todo hashes/ids: sin egress, sin PII, #4-compatible.
7. **OFF BY DEFAULT, reversible por flag** (registro fuera del config pinned, patron DECISION-0054/0055; activacion
   por env). Uso vivo gateado.

## Decisiones del operador (tras red-team)
- **D-PII:** detector REAL best-effort (email/tel/doc/NIT/razon-social/SQL/nombres) + honestidad (no garantizado)
  + GATE HUMANO DURO (revision+aprobacion por candidata con declaracion de PII revisada). NO se afirma "ningun
  LLM ve PII".
- **D-ACTOR:** relay honesto como Arquitecto (sin tocar registry, sin re-genesis, #4 byte-identica).

## Threat model (resumen)
PII de terceros: screening real best-effort en ingest (reduce, NO elimina) + gate humano duro por-candidata antes
del atestado irreversible + re-screen candidate->intake. Egress: server NO llama a MODELO (prueba negativa
estatica: sin import de SDK de modelo, sin socket a host de LLM; + control positivo); el git-push es transporte
gobernado existente; el agente extractor lee el archivo (ventana reconocida, etiquetada/consentida). Raw store
FUERA del dataset, gitignored, purgado al estado terminal + TTL para huerfanos. Candidatas NO atestadas hasta
aprobar. Colision id N-candidatas: id del contenido editado. Hash atestado = SHA-256 de bytes crudos.
Estados de extraccion (0/basura/cap/failed/timeout/sin-agente) explicitos. Logs/errores no ecoan contenido crudo.

## Alcance / fases
A (plumbing determinista: upload no-MODELO-egress + screening + store-fuera-dataset + emit-task-con-contrato +
selector de modo) / B (candidatas store-no-ledger + panel de revision + gate-humano-PII + aprobar->intake) /
C (loop de extraccion: el agente atiende la tarea). La rama "por carga de archivo" del selector se GATEA detras
de B+C (no se ofrece vacia) o lleva un consumidor minimo no-LLM (archivo entero = 1 candidato editable).

## Condiciones de cierre (innegociables)
(a) server no llama a ningun MODELO (prueba negativa estatica + control positivo); (b) screening PII real
best-effort + ASCII en ingest, HONESTO (no garantizado); (c) store de uploads y de candidatas FUERA del dataset
atestado (gitignored entregado + git ls-files vacio + excluido del git-status del indicador); (d) candidatas NO
usan el ledger/task_status; ledger nunca ve `candidate`; drift 0 con candidatas; (e) GATE HUMANO DURO: aprobacion
por-candidata con declaracion de PII revisada antes del intake; re-screen candidate->intake; id del contenido
editado; (f) hash atestado = SHA-256 bytes crudos; procedencia PII-free determinista; (g) #4 epoca 1.14.0
BYTE-IDENTICA (relay honesto, sin registry/re-genesis); validate con/sin secretos exit 0; drift 0; npm test verde
EN CLON LIMPIO; neutralidad/encoding 0; (h) estados de extraccion + purga del raw + idempotencia de upload;
(i) PASADA DEL ANALISTA (ingest/egress/PII, incl. el salto LLM->intake) ANTES de cerrar; off-by-default.
