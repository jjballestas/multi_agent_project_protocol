# VOZ ANALISTA SOTA — Revisión de Deltas (SPEC-0078)

**Rol:** Voz analista independiente (solidez SOTA + verificación de fuentes) en revisión adversarial multi-agente.
**Restricción:** maker≠checker. Análisis puro, sin código, sin mutar estado autoritativo. No consolida ni decide.
**Fecha:** 13 de junio de 2026
**Insumos verificados:**
- `Area_comun/artifacts/ESTUDIO-GESTION-CONTEXTO-ARQUITECTO-2026.md`
- `Area_comun/artifacts/PROPUESTA-deltas-sota-spec-0078.md` (= DECISION-0031)
- `Area_comun/specs/SPEC-0078-compaction-y-subagentes.md`

---

## 0. Veredicto en 5 líneas

1. SPEC-0078 base es **sólida**: neutral de dominio, single-writer, event-sourced, off-by-default. No requiere redesign.
2. **DELTA-1** (umbrales de degradación) → **REFORMULAR**: los umbrales >100k NO están en el paper citado (2602.16284); son interpolación del ESTUDIO. El paper es de KV-cache, arquitectura que tu runtime CLI **no tiene**.
3. **DELTA-2** (consolidation trigger "cada 10 tool calls") → **REFORMULAR**: la heurística "10 tool calls" **NO aparece en Focus** (2601.07190), que es un mecanismo AUTÓNOMO. Es adición del ESTUDIO.
4. **DELTA-3** (edición atómica, Future Work) y **DELTA-5** (GC-8/GC-9) → **MANTENER**: bien fundados, off-by-default, coverage correcta.
5. **Principio rector (DECISION-0008):** los umbrales se derivan de la MEDICIÓN PROPIA (`scripts/measure_context_cost`), no de papers. DELTA-1 y DELTA-2 violan esto. **GO condicional**: medir baseline ANTES de congelar umbrales/cadencias.

---

## 1. Tabla de Fuentes (claim → estado → enlace)

| Referencia | arXiv | Claim en ESTUDIO | Estado | Enlace | Nota crítica |
|-----------|-------|------------------|--------|--------|--------------|
| Attention Matching (ICML 2026) | 2602.16284 | 50x-100x compaction; "degrada >100k" | ⚠️ **MAL-ATRIBUIDO (parcial)** | https://arxiv.org/abs/2602.16284 | Es compactación de **KV-cache en espacio latente**. Los umbrales F1 (<5% ≤100k) y el corte >100k **no están en el paper**; son interpolación conservadora del ESTUDIO. NO aplica a runtime que invoca CLIs. |
| Focus / Active Context Compression (Jan 2026) | 2601.07190 | 22.7% reducción; "cada 10-15 tool calls" | ❌ **MAL-ATRIBUIDO** | https://arxiv.org/abs/2601.07190 | Mecanismo **AGENTE-AUTÓNOMO** (consolida según atención mínima propia). La heurística "cada 10 tool calls" es **adición del ESTUDIO**, no del paper. El 22.7% no se deriva de esa cadencia. |
| MemMA (Mar 2026) | 2603.18718 | +4.82 F1 base, +14.41 Multi-Hop; ADD/UPDATE/DELETE | ✅ **CONFIRMADO** (patrón) | https://arxiv.org/abs/2603.18718 | Edición atómica es pattern sólido. **Caveat:** asume **4 agentes (Meta-Thinker + Memory Manager)** — arquitectura distinta a single-writer. El patrón (ops atómicas) es adoptable; la coordinación multi-agente NO. |
| A-Mem / Zettelkasten (NeurIPS 2025) | 2502.12110 | 85-93% reducción; 18.4→45.9 F1 multi-hop | ✅ **CONFIRMADO** (patrón) | https://arxiv.org/abs/2502.12110 | Dynamic linking + consolidación post-sesión. Patrón sólido. **Caveat:** "retrieval sub-microsecond" marcado [sin confirmar] en el propio ESTUDIO. Timing offline ≠ hot path. |
| MemGraphRAG (KDD 2026) | 2606.00610 | "3-layer ontology", coherencia global, "8x-49x" | ⚠️ **NO-VERIFICABLE / vago** | https://arxiv.org/abs/2606.00610 | Asume **graph DB (Neo4j/Memgraph)**. El "% mejora en irrelevancia" el propio ESTUDIO lo marca "no cuantificado". Aserto vago. Tecnología pesada = NO aplica. |
| Memory in LLM Era (Apr 2026) | 2604.01707 | sub-450 tokens; F1 38.79 vs MemTree 36.92 | ❓ **NO-VERIFICABLE** | https://arxiv.org/abs/2604.01707 | Verificado solo **2-1** en el propio ESTUDIO. MemTree overhead marcado [sin confirmar]. Números específicos sin acceso a PDF. Usar rango 450-1200 como **guía**, no ley. |
| Multi-Agent Memory Architectures (2026) | 2603.10062 | "mayoría de sistemas usa hybrid" | ❓ **NO-VERIFICABLE** | https://arxiv.org/abs/2603.10062 | Verificado 2-1. Claim genérico ("mayoría"), sin cuantificación. Arquitectural, no prescriptivo. |
| Agent Memory Framework / Taxonomía (Mar 2026) | 2603.09619 | Working/Episodic/Semantic/Procedural | ✅ **CONFIRMADO** (fundacional) | https://arxiv.org/abs/2603.09619 | Taxonomía de Tulving adaptada; SOTA fundacional bien conocido. Verificado 2-1 pero conceptualmente robusto. Marco conceptual, no implementación. |

**Resumen de estados:**
- ✅ **CONFIRMADOS (uso seguro como patrón):** 2603.18718, 2502.12110, 2603.09619
- ⚠️ **MAL-ATRIBUIDOS (la cifra/heurística no está en el paper):** 2602.16284 (umbrales >100k), 2601.07190 (cadencia "10 calls")
- ❓ **NO-VERIFICABLES (sin acceso / claim genérico):** 2604.01707, 2603.10062, 2606.00610

> **Hallazgo de partida CONFIRMADO por mí:** las dos sospechas iniciales son correctas. DELTA-1 cita un paper de KV-cache cuyos umbrales no aparecen; DELTA-2 atribuye a Focus una heurística "cada 10 tool calls" que Focus no especifica (es autónomo).

---

## 2. Aplicabilidad por Arquitectura

Tu protocolo: **estado event-sourced, ESCRITOR ÚNICO (runtime), turnos LLM single-shot vía CLI** (`claude -p` / `codex exec`). El runtime NO controla el modelo backend ni su atención interna.

| Técnica SOTA | Arquitectura que asume | ¿Aplica a single-writer + CLI? | Por qué |
|--------------|------------------------|-------------------------------|---------|
| **Attention Matching** (2602.16284) | KV-cache en memoria del modelo; atención layer-wise | ❌ **NO (mecánica); ✅ patrón** | Tu runtime arma contexto **plano** para stdin del CLI. No hay KV-cache que compactar. Los 50x-100x dependen de atención interna que no controlas. Adoptable: el *principio* (retener relevante, descartar ruido). Inaplicable: los números. |
| **Focus** (2601.07190) | Agente con **decisión interna** de cuándo consolidar | ❌ **NO (autónomo); ✅ patrón periódico** | Single-shot CLI no decide "cuándo consolidar" por sí mismo. El trigger debe ser **determinista del runtime** (cada N calls / T min). Pero esa cadencia es tuya, no de Focus. |
| **MemMA** (2603.18718) | **Meta-Thinker + Memory Manager** (4 agentes) | ⚠️ **Patrón sí, coordinación NO** | Las ops ADD/UPDATE/DELETE son adoptables sobre CLAIMS/TASK_INDEX **con drift_checker**. La orquestación multi-agente del paper NO encaja en single-writer. Correctamente diferido a TASK-0107. |
| **A-Mem** (2502.12110) | Consolidación **post-sesión offline** | ⚠️ **Patrón sí, timing distinto** | "Fin de sesión" en tu protocolo = transición a `done` de UNA tarea, no fin global. Episódico asíncrono, fuera del hot path. TASK-0108 si acaso. |
| **MemGraphRAG** (2606.00610) | **Neo4j / Memgraph** (graph DB persistente) | ❌ **NO (tecnología pesada)** | Viola neutralidad de dominio y off-by-default si se acopla. El patrón "3 pilares" es adoptable; la prescripción graph-DB se rechaza. SPEC-0078 no la menciona — correcto. |
| **Servicio de memoria persistente** (Mem0/Letta, citados) | Servicio externo con vector store | ❌ **NO core; ✅ opcional separado** | El estado del protocolo vive en runlog event-sourced. Importar un servicio de memoria rompería single-writer. Separable, off-by-default. |

**Conclusión de aplicabilidad:** las cuatro técnicas más citadas (Attention Matching, Focus, MemMA, MemGraphRAG) asumen arquitecturas con control de atención interna, multi-agente, o graph DB. Tu protocolo CLI single-writer **adopta los PATRONES**, no los números ni las tecnologías. Esto refuerza DECISION-0008: **medir lo propio**.

---

## 3. Evaluación del PDF "Memoria Heterogénea y Polimórfica"

**Nota de alcance:** el PDF no está entre los 3 insumos. Lo evalúo según el resumen del ESTUDIO (sección 2). Si el operador quiere veredicto sobre el PDF original, pido el archivo.

| Pieza del PDF | ¿Adoptable como PATRÓN? | ¿Rechazar como prescripción? |
|---------------|-------------------------|------------------------------|
| **3 pilares** (Trabajo / Declarativa / Procedimental) | ✅ SÍ — marco conceptual sólido, implementable en cualquier stack | — |
| **Property Graph para código (AST)** | ✅ SÍ — patrón, backend agnóstico (SQLite o Neo4j) | — |
| **Recuperación por N-vecinos (blast radius)** | ✅ SÍ — verificado por code-review-graph + SOTA | — |
| **Partición temporal corto/largo plazo** | ✅ SÍ | — |
| **Neo4j + LlamaIndex PropertyGraphIndex** | — | ❌ **RECHAZAR** — pesado, acopla, viola neutralidad. Usar backend agnóstico (SQLite default). |
| **"Agente de fondo" para consolidación** | — | ❌ **RECHAZAR (por vago)** — sustituir por trigger determinista medido. |

**Adoptable:** patrón de 3 pilares + recuperación por vecindad.
**Rechazo tecnológico pesado:** Neo4j / LlamaIndex como prescripción. SPEC-0078 ya es agnóstico → correcto.

---

## 4. Juicio por Delta

| Delta | Veredicto | Fuente verificada | Acción concreta |
|-------|-----------|-------------------|-----------------|
| **DELTA-1** — Umbrales de degradación (≤100k / 100k-500k / >500k) | ⚠️ **REFORMULAR** | 2602.16284 **MAL-ATRIBUIDO**: paper KV-cache; umbrales no presentes | Reescribir: "Ejecutar `measure_context_cost` baseline ANTES de fijar umbrales. SOTA sugiere 50x-100x en corto plazo; los cortes concretos se derivan de la MEDICIÓN PROPIA (DECISION-0008)." Quitar la cifra "F1 <5%" como si viniera del paper. El **mecanismo de warning + fallback** sí es válido y se mantiene. |
| **DELTA-2** — Consolidation trigger (cada 10 tool calls) | ⚠️ **REFORMULAR** | 2601.07190 **MAL-ATRIBUIDO**: Focus es autónomo, no "cada N calls" | Mantener el patrón (trigger determinista periódico, correcto para single-writer). Marcar "10" como **provisional/tuneable**, no como baseline de Focus. AC8 debe decir "cadencia inicial provisional, ajustar tras medición; objetivo overhead <5%". |
| **DELTA-3** — Edición atómica ADD/UPDATE/DELETE (sec 2.6, TASK-0107) | ✅ **MANTENER** | 2603.18718 **CONFIRMADO** (patrón; descartar coordinación 4-agentes) | Sin cambios. Future Work, off-by-default, respeta drift_checker y single-writer. Correctamente fuera de scope TASK-0106. |
| **DELTA-4** — Revisión límites summary (2000 vs 1200) | ⚠️ **DECIDIR + JUSTIFICAR** | 2604.01707 **NO-VERIFICABLE** (rango 450-1200 como guía, no ley) | No bajar a 1200 "porque lo dice el paper". Decidir según **medición propia** del tamaño real de resúmenes; documentar la justificación en SPEC-0078 §2.5. 2000 conservador es defendible si se justifica. |
| **DELTA-5** — Golden Cases GC-8 / GC-9 | ✅ **MANTENER** | N/A (test coverage, no requiere paper) | Sin cambios. Coverage correcta y determinista. **Sugerencia:** GC-9 debe asertar sobre la **medición propia** del umbral, no sobre un número heredado. |

---

## 5. Recomendación al Arquitecto (no vinculante — soy una voz)

1. **Aprobar la estructura** de SPEC-0078 y los 5 deltas como dirección, pero **corregir la procedencia** de DELTA-1 y DELTA-2: no presentarlos como "verificados 3-0 desde el paper" cuando las cifras/heurísticas son interpolaciones. Esto es un problema de **trazabilidad de fuentes**, no de diseño.
2. **Reclasificar los "Verified 3-0"** del ESTUDIO: 2602.16284 y 2601.07190 deben bajar a "patrón confirmado / cifra no atribuible". Mantener el voto solo para 2603.18718, 2502.12110, 2603.09619.
3. **Bloquear el freeze de umbrales/cadencias** hasta correr `scripts/measure_context_cost` baseline. Es coherente con DECISION-0008 y con el propio Plan de Medición (§6 del ESTUDIO), que ya prevé baseline-2026-06-13.json. El ESTUDIO se contradice: pide medición propia en §6 pero hereda números de papers en los deltas.
4. **Rechazar** cualquier deriva hacia Neo4j/LlamaIndex/servicio de memoria persistente: rompen neutralidad y single-writer.
5. **GO condicional para TASK-0106:** DELTA-3 y DELTA-5 directos; DELTA-1, 2, 4 condicionados a medición + reescritura de procedencia.

---

## Anexo — Contradicción interna detectada en el ESTUDIO

El ESTUDIO afirma en §6.3 que se debe ejecutar `measure_context_cost --baseline` ANTES de TASK-0106 para capturar umbrales reales, pero en DELTA-1/DELTA-2 **fija** umbrales (≤100k, 5% F1) y cadencias (10 tool calls) como si ya estuvieran derivados de SOTA. Esto es incoherente con DECISION-0008 ("umbrales de medición propia, no de papers"). La reformulación propuesta en §4 resuelve la contradicción: los deltas describen el **mecanismo**; los **valores** salen de la medición.

---

*Voz Analista SOTA. Entregable de revisión, no consolidación. Recogido por el arquitecto vía TASK-0109. Sin código, sin mutación de estado autoritativo.*
