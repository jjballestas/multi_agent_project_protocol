---
decision_id: DECISION-00XX (DRAFT - id final al promover)
title: Engram como backend de memoria/recall (capability OFF by default) - frontera ledger/memoria, namespacing por agente, single-writer preservado y no-interferencia con el dataset del TFM
status: draft (pendiente GO operador)
date: 2026-06-29
deciders: [operador humano (pendiente), Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0016, DECISION-0020, DECISION-0022, DECISION-0026, DECISION-0040, DECISION-0050]
phase: P2
---

# DECISION-00XX (DRAFT) - Engram como backend de memoria/recall

> DRAFT del Arquitecto para revisión (Analista honestidad/metodología + Codex invariante) y GO del
> operador. NO toca el ledger al redactarse. Cambio aditivo, capacidad APAGADA por defecto, neutral
> de dominio en el Core. La aprobación por escrito del operador se registra como esta DECISION al promover.

## Contexto

Hoy la memoria persistente de cada agente es markdown (`personal/<id>/` + runbook), gobernada por la
regla de oro post-commit (DECISION-0026). Funciona, pero el recall es manual (grep) y no detecta
memoria obsoleta/contradictoria. **Engram** (Gentleman-Programming) es un motor de memoria
agent-agnóstico (Go + SQLite/FTS5 + servidor MCP, ~20 tools `mem_save`/`mem_search`/`mem_context`,
y *conflict-surfacing* `mem_judge`/`mem_compare`) que mejoraría el arranque frío y la higiene de memoria.

**El hecho que obliga esta decisión:** el modelo de concurrencia de Engram es **opuesto** al nuestro.
Su propia doc: memoria **compartida por proyecto**, *"scope is a search and filter signal, not a privacy
boundary"*, **sin campo de autor**, **sin locks**, **sin resolución de conflictos de merge documentada**;
la verdad local es un **SQLite fuera del repo** y a git solo exporta `chunks/*.jsonl.gz`. Enchufarlo
ingenuamente (varios agentes escribiendo un pool compartido) **reintroduce el multi-writer que matamos
con claims + `submit_intent`** (DECISION-0020) y mete texto libre en un plano que GATE-DATASET (DECISION-0040)
protege. Esta decisión fija cómo adoptar Engram **sin** perder esas garantías y **sin** afectar el TFM.

## Decisión

1. **Frontera dura: Engram ≠ ledger.** El ledger atestado #4 (`Area_comun/state/*.json` vía
   `submit_intent`) sigue siendo la **única fuente de verdad de gobernanza**. Engram es **solo capa de
   memoria/recall**: no puede ser ni sombrear el state de protocolo. El **markdown-en-git permanece como
   el registro DURABLE y atestable**; Engram es un **índice derivado y reconstruible** encima. Si el DB
   local de Engram se pierde, se reimporta desde el markdown. Engram **no añade ninguna fuente de verdad nueva**.

2. **Capacidad APAGADA por defecto + modelo de tres niveles.**
   - **Tier 0 (permitido ya):** recall per-agente, DB local, **no commiteado**, fuera del ledger. Cada
     agente hace `mem_save`/`mem_search` en SU namespace. Impacto en claims/ledger/dataset = **ninguno**
     (vive fuera de rutas del repo y no emite eventos).
   - **Tier 1 (DIFERIDO, ver cláusula 5):** memoria **compartida** entre agentes, enrutada por
     `submit_intent` (intent `engram_observation`). Single-writer preservado.
   - **Tier 2 (no recomendado / fit débil):** commitear `.engram/` a git. Solo single-writer (runtime),
     claim explícito sobre la ruta, staging explícito (DECISION-0020 #2). Caveat: chunks gzip casi
     binarios para diff y Engram no documenta merge → preferir Tier 0 + reimport.

3. **Namespacing por agente = proyecto Engram `map-<id>` (espejo de DECISION-0016).** `personal/Arquitecto`
   ↦ proyecto `map-arquitecto`; `Codex` ↦ `map-codex`; `Analista` ↦ `map-analista`. Cada agente solo ve su
   pool. El namespace **ES** la identidad de autor que Engram no tiene. Un pool compartido `map-shared`
   solo se escribe vía Tier 1.

4. **Single-writer preservado (no se rompe DECISION-0020).** Ningún agente escribe un pool compartido de
   Engram directamente. Las memorias compartidas pasan por `submit_intent` como intent `engram_observation`;
   el runtime (escritor único) hace el `mem_save` real **después** de que la transacción del ledger
   aterrice (`engram_bridge`, tarea diferida). El ledger lleva **solo `content_sha256` + metadato**
   (`topic_key`, `title`, `mem_type`, `memory_project`), **nunca el cuerpo** — mismo principio "sujeto por
   hash, plano estructural" de DECISION-0040. La memoria compartida hereda así orden total y single-writer.

5. **No-interferencia con el TFM / GATE-DATASET (condición central).** El dataset de tesis es la
   **coordinación de agentes** derivada del event log, con invariante "cero PII en el event log"
   (DECISION-0040). Por tanto:
   - **Shippear el mecanismo INERTE (parche `engram_observation` con la capacidad OFF) NO afecta el TFM:**
     emite cero eventos, no añade ningún tipo de evento al stream, no toca el state materializado, no
     añade superficie de texto libre. El instrumento de medición queda idéntico.
   - **La ACTIVACIÓN de Tier 1 (emitir `engram_observation` en vivo) queda DIFERIDA** hasta que el operador
     lo autorice **después de sellar el dataset de coordinación** (hito N=500 + resolución de PRE-REG /
     GATE-INST). Razón: emitir un tipo de evento nuevo a mitad de la captura **cambia el instrumento**,
     puede desviar del PRE-REG y añade superficie de texto libre al event log que GATE-DATASET protege.
   - **Tier 0 se permite desde ya** porque vive fuera del ledger y no puede tocar el dataset.
   - Cláusula modelada sobre la "tarea diferida" de DECISION-0040: se define la capacidad, se shippea
     apagada, la captura viva se difiere detrás del gate del dataset.

6. **DECISION-0026 — mejora de mecanismo, regla intacta.** Tras cada commit, la actualización de memoria
   PUEDE registrarse además vía Engram `mem_save` (formato What/Why/Where/Learned; `Where` = commit SHA;
   `mem_type` ∈ {decision, bugfix, architecture, learning, ...}; `topic_key` estable) en el proyecto
   `map-<id>` del agente. La regla de oro NO cambia; el markdown-en-git sigue siendo el registro durable.
   El conflict-surfacing de Engram (`mem_judge`) ayuda a detectar la memoria obsoleta que DECISION-0026
   busca evitar.

## Alcance / No-alcance

- **En alcance:** frontera ledger/memoria; capacidad OFF by default; namespacing `map-<id>`; el intent
  `engram_observation` como vía single-writer para memoria compartida (ledger lleva hash, no cuerpo);
  diferimiento de la activación de Tier 1 detrás del gate del dataset; mejora de mecanismo de DECISION-0026.
- **Fuera de alcance:** activar Tier 1 ahora; sustituir el markdown-en-git como fuente de verdad; meter el
  cuerpo de la memoria en el event log; commitear `.engram/` por defecto (Tier 2); introducir términos de
  dominio (los `map-*` y `mem_type` son neutrales); cualquier publicación/citación del dataset (sigue bajo
  GATE-DATASET + GATE-INST + PRE-REG).

## Consecuencias

- Se habilita YA el recall per-agente (Tier 0) sin riesgo: arranque frío con `mem_context` en vez de grep,
  detección de memoria obsoleta. Sin impacto en ledger/dataset/TFM.
- El protocolo gana una vía atestada y single-writer para memoria compartida cuando se active (Tier 1),
  con el cuerpo fuera del log (consistente con el invariante de PII).
- Queda explícito y HONESTO que la activación de Tier 1 es una decisión posterior, gated por el dataset:
  no se sobre-afirma "ya integrado", se shippea el mecanismo y se difiere la captura viva.
- Dependencia de un binario externo (Go) acotada a una capacidad opcional; el markdown sigue como fallback
  durable y atestable.

## Tarea diferida (regla 3.4 - condición de activación, NO bloqueo)

Se registran como tareas con fecha (se formalizan en `TASK_INDEX` al promover; NO se construyen ahora):
- **ENG-BRIDGE:** `runtime/engram_bridge.py` — post-commit, ejecuta el `mem_save` real verificando
  `sha256(cuerpo)==content_sha256`; idempotente; respeta `map-<id>`.
- **ENG-FLAG:** wiring del flag `event-state.runtime.json -> engram.enabled` (default false) + doc.
- **ENG-PII:** validador anti-PII sobre `title`/`topic_key` (NIT, razón social, payloads SQL de Budget)
  ANTES de habilitar Tier-1 en vivo — convierte la garantía de predicado de disciplinaria a estructural
  (espejo de DEF-PII en DECISION-0040). **Condición previa a activar Tier 1.**

## Alternativas consideradas

- **Dejar que los agentes escriban Engram compartido directamente.** Descartada: reintroduce multi-writer
  (viola DECISION-0020); sin autor, sin locks, sin merge → colisión/corrupción silenciosa.
- **Meter el cuerpo de la memoria en el event log.** Descartada: superficie de PII/texto libre que
  GATE-DATASET protege; rompe minimización; el hash basta para atestar.
- **Sustituir el markdown por Engram como fuente de verdad.** Descartada: el DB local no está en git
  (no durable, no atestado); perdería garantías de arranque frío y del #4. Engram = índice derivado.
- **Activar Tier 1 ya.** Descartada: cambia el instrumento del dataset a mitad de captura (riesgo
  metodológico) y añade superficie de PII al log antes de ENG-PII.
