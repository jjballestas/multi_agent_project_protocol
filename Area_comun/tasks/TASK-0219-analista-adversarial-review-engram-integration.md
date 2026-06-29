---
task_id: TASK-0219
title: "Revision ADVERSARIAL (refutacion) de la propuesta de integracion de Engram: frontera ledger/memoria, PII/GATE-DATASET (0040), single-writer (0020), correccion del parche"
type: review
status: ready
owner: Analista
phase: P2
priority: high
created_at: 2026-06-29
reviewer: Analista
author_under_review: Arquitecto
checker: Arquitecto
project: multi_agent_project_protocol
linked_decisions: [DECISION-0020, DECISION-0026, DECISION-0040, DECISION-0050]
file: Area_comun/tasks/TASK-0219-analista-adversarial-review-engram-integration.md
---

# TASK-0219 -- Revision ADVERSARIAL de la propuesta de integracion de Engram

## Encargo (NO es revision de cortesia)

El objetivo es ROMPER las afirmaciones, no bendecirlas. Postura por defecto = "REFUTADO salvo
prueba en contra"; ante duda, marca REFUTADO y exige evidencia. author_under_review = Arquitecto
(no confies en su resumen; ve a la fuente primaria y al codigo). maker != checker.

## Artefactos a refutar (drafts del Arquitecto en su area personal)

- personal/Arquitecto/DRAFT-DECISION-engram-memory-backend.md
- personal/Arquitecto/PATCH-engram-observation-intent.md

## Contexto duro que debe respetarse

- GATE-DATASET (DECISION-0040): el dataset del TFM es la coordinacion de agentes derivada del
  event log, con invariante "cero PII en el event log". LECCION 0040 (VINCULANTE): no aceptar como
  ESTRUCTURAL lo que solo es DISCIPLINARIO. Se explicito en cada punto: estructural vs disciplinario.
- DECISION-0020 (single-writer / anti-colision).
- Neutralidad de dominio del Core (boundary innegociable).

## BRIEFING -- que es Engram (VERIFICALO, no lo des por bueno)

Engram (Gentleman-Programming): motor de memoria persistente para agentes IA; binario Go,
SQLite + FTS5, servidor MCP (stdio) con ~20 tools (mem_save/mem_search/mem_context/mem_judge...),
exporta a git como .engram/chunks/*.jsonl.gz. La propuesta lo usa SOLO como capa de memoria/recall,
NO como ledger.

Afirmaciones del Arquitecto sobre Engram que son LOAD-BEARING para la refutacion -- VERIFICALAS
contra fuentes primarias ANTES de aceptarlas o usarlas:
- "memoria compartida por proyecto; scope no es frontera de privacidad"
- "no tiene campo de autor en los registros"
- "no documenta resolucion de conflictos de merge"
- "SQLite local = fuente de verdad; a git solo exporta chunks gzip"
- tools de escritura vs lectura, y campos de mem_save (title/type/content/topic_key/scope)

Fuentes a fetchear y CITAR (linea/seccion):
- https://github.com/Gentleman-Programming/engram  (README)
- https://raw.githubusercontent.com/Gentleman-Programming/engram/main/docs/ARCHITECTURE.md
- https://raw.githubusercontent.com/Gentleman-Programming/engram/main/docs/TEAM-USAGE.md
- https://raw.githubusercontent.com/Gentleman-Programming/engram/main/DOCS.md

Si alguna afirmacion del draft sobre Engram es INEXACTA, eso es un hallazgo en si mismo (la decision
se apoya en una premisa falsa) -> reportalo como BLOQUEANTE. Si no tienes acceso de red para
fetchear las fuentes, NO inventes: declara la limitacion como pregunta concreta al Arquitecto y
deja ese sub-punto como "no verificable en este entorno".

## Vectores a atacar (uno por uno, con evidencia archivo/linea/escenario)

A. NO-INTERFERENCIA TFM. Es cierto que "shippear el mecanismo OFF = cero impacto en el dataset"?
   - Mergear el codigo (aun apagado) cambia algo que lea el extractor del dataset / el harness
     research/experiment_h1h3?
   - Registrar la propia DECISION (evento decision) desplaza la distribucion del corpus o el PRE-REG?
   - El diferimiento de Tier-1 es ENFORZABLE (gate real) o solo documental? Que impide que un agente
     lo active a mitad de captura?

B. HASH-NO-CUERPO (I4) y PII. De verdad no entra texto libre al log?
   - title y topic_key SIGUEN siendo texto libre en el ledger -> superficie de PII. La blacklist
     ("content","body",...) es solida o trivialmente burlable metiendo el cuerpo en title?
   - content_sha256 filtra algo / es reversible para cuerpos cortos/predecibles?
   - Esto es "cero PII estructural" o solo disciplinario? Se explicito (leccion 0040).

C. SINGLE-WRITER (vs DECISION-0020). El mem_save real (engram_bridge) ocurre FUERA de la transaccion
   atomica del ledger. Que pasa si el ledger commitea pero el mem_save falla, o al reves? Hay brecha
   de consistencia de dos fases? La afirmacion "single-writer preservado" se sostiene?

D. "ENGRAM = INDICE DERIVADO Y RECONSTRUIBLE". No hay importador markdown->engram; el dual-write
   puede divergir. Es realmente reconstruible? Se preserva la durabilidad/atestacion o es afirmacion vacia?

E. NAMESPACING COMO AUTOR. map-<id> es convencion, no enforcement: Engram no garantiza que map-codex
   solo reciba escrituras de Codex. El aislamiento per-agente es real o disciplinario?

F. FRONTERA "ENGRAM != LEDGER". Puede la memoria convertirse en fuente de verdad sombra en la
   practica (agentes confiando en recall por encima del ledger)? La frontera es estructural o solo regla?

G. NEUTRALIDAD DE DOMINIO. Algo del parche/decision introduce terminos de dominio en el Core?

H. CORRECCION DEL PARCHE. (i) El no-op de replay es realmente cero-drift? (ii) El enforcement del
   gate cubre AMBOS caminos (single y --intents, con rollback)? (iii) Sigue seguro el fall-through de
   `decision` en normalize_intent tras insertar la rama engram_observation? Verifica contra el codigo
   real (runtime/submit_intent.py, runtime/protocol_replay.py) en clon limpio.

## Entregable (veredicto ESTRUCTURADO)

- Por cada afirmacion A-H: REFUTADO | SOBREVIVE, con evidencia concreta (archivo/linea/escenario) y
  severidad (bloqueante / mayor / menor).
- Lista de BLOQUEANTES que impiden promover la DECISION o aplicar el parche tal cual.
- Correcciones minimas exigidas para que cada bloqueante pase.
- Veredicto final: GO / NO-GO / GO-CON-CONDICIONES (enumeradas).

## Reglas

- Narracion minima (DECISION-0038); un solo informe final autocontenido.
- No toques rutas bajo claim ajeno; los drafts son del Arquitecto (no los edites; refutalos).
- Si necesitas algo del Arquitecto, una pregunta concreta y espera.

## Definition of Done

Artefacto `Area_comun/artifacts/ANALISTA-TASK-0219-veredicto.md` entregado + MSG REVIEW al Arquitecto;
reclamado y liberado via submit_intent firmado (claim acquire/release); commit como autor Analista.
NO tocar task_status (lo lleva el Arquitecto).
