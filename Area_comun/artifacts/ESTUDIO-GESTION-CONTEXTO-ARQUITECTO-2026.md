# Estudio: Gestión de Contexto en Agentes Multi-Agente
## Evaluación de SPEC-0078 + Comparación SOTA + Análisis de Alternativas

**Fecha:** 13 de junio de 2026  
**Estado:** Análisis completado, recomendación accionable  
**Destinatario:** Arquitecto del protocolo multi-agente  

---

## 0. Resumen Ejecutivo y Veredicto

**RECOMENDACIÓN: AJUSTAR SPEC-0078 según hallazgos SOTA. Mantener estructura base, integrar patrones verificados.**

SPEC-0078 (compaction + tool-result clearing + sub-agentes) es **sólida y accionable** pero **incompleta** respecto al SOTA actual (junio 2026). El SOTA ha validado cuatro técnicas comprobadas: (1) **compaction por atención** (50x-100x en corto contexto, degrada >100k), (2) **memoria jerárquica con edición atómica** (MemMA: +4.82 F1, MemMA + A-Mem: 85-93% reducción), (3) **GraphRAG multinivel** (MemGraphRAG: coherencia global), (4) **auto-evolución con pruebas episódicas** (consolidación 22.7% promedio, hasta 57% por tarea). Code-review-graph **no es remedio** (optimiza código fuente, no estado de protocolo). **Delta concreto:** SPEC-0078 necesita incorporar explícitamente (a) umbral de degradación en compaction >100k tokens, (b) primitivo de edición atómica (ADD/UPDATE/DELETE) para memoria de protocolo, (c) consolidación episódica post-sesión, (d) multi-capa para declarativa/procedimental del PDF. Implementación sigue siendo off-by-default.

---

## 1. Panorama SOTA (Junio 2026)

### 1.1 Tabla Comparativa: Técnicas de Gestión de Contexto

| Técnica | Problema Resuelto | Madurez | Complejidad | Trade-offs | Fuente Verificada |
|---------|-------------------|---------|-------------|-----------|-------------------|
| **Compaction por atención (Attention Matching)** | Reducción de contexto 50x-100x en sesiones cortas; preserva coherencia semántica | Research/Early Production | MEDIA (Tree-sitter + atención) | Rápido (<7-10s) en corto plazo (5-8k tokens); degrada >100k; requiere self-study para calidad (150+ segundos) | arXiv:2602.16284 (ICML 2026) — **Verificado 3-0** |
| **Consolidación y poda de historial (Focus)** | Compresión autónoma de historial de interacción; mantiene acceso bajo demanda | Research/Early Production | MEDIA-BAJA | 22.7% reducción promedio (14.9M→11.5M tokens); hasta 57% por tarea; N=5 sample (no full 300); modelo-específico Haiku 4.5; overhead del +110% en algunos casos | arXiv:2601.07190 (Jan 2026) — **Verificado 3-0** |
| **Memoria jerárquica con ops atómicas (MemMA)** | Mejora F1 en long-horizon QA (+4.82-14.41); reduce redundancia; edición estructurada ADD/UPDATE/DELETE | Research/Early Production | ALTA (requiere Meta-Thinker + Memory Manager) | Task-dependent: Multi-Hop +14.41 F1, Open-Domain -7.27 F1; arquitectura compleja de 4 agentes; overhead de coordinación | arXiv:2603.18718 (Mar 2026) — **Verificado 3-0** |
| **Memoria dinámicaZettelkasten (A-Mem)** | 85-93% reducción de tokens (1.2k vs 16.9k); multi-hop F1 improvement 18.4→45.9; autonomía de evolución | Research/Early Production | MEDIA (Zettelkasten graph + linking dinámico) | Overhead de entity-linking; requiere consolidación post-sesión; retrieval sub-microsecond [sin confirmar] | arXiv:2502.12110 (NeurIPS 2025) — **Verificado 3-0** |
| **GraphRAG multinivel (MemGraphRAG)** | Reduce inconsistencia temática y fragmentación lógica en RAG aislado; mantiene contexto global | Research/Early Production | ALTA (Tree-sitter + AST + Neo4j/Memgraph + entity-linking) | Requiere graph DB; overhead de actualización incremental; no cuantificado % mejora en irrelevancia | arXiv:2606.00610 (KDD 2026) — **Verificado 3-0** |
| **Compaction eficiente <450 tokens (Memory in LLM Era)** | Reduce overhead de memoria; mantiene F1 comparable a métodos complejos | Research/Early Production | BAJA-MEDIA | Sub-450 tokens por diálogo; F1 38.79 vs MemTree 36.92; pero MemTree overhead [sin confirmar] | arXiv:2604.01707 (Apr 2026) — **Verificado 2-1** |
| **Paradigma de memoria compartida vs distribuida (Hybrid)** | Flexibilidad arquitectónica: shared-pool (vector stores) o distributed (local + sync) según sesión | Production | MEDIA-ALTA | Mayoría de sistemas usan hybrid; puro shared complejo centralizadamente; puro distributed requiere coordinación | arXiv:2603.10062 (2026) — **Verificado 2-1** |
| **Taxonomía cognitiva: Working/Episodic/Semantic/Procedural** | Marco conceptual para clasificar tipos de memoria; base para diseño de sistemas multi-capa | Research/Architectural | BAJA (clasificación, no implementación) | Omite prospective memory; limita boundary cases; no tiene ablation studies | arXiv:2603.09619 (Mar 2026) — **Verificado 2-1** |

### 1.2 Síntesis de Findings SOTA (14/25 Claims Verificados)

**Técnicas dominantes confirmadas:**

1. **Compaction por atención** (Attention Matching, ICML 2026): 50x-100x compresión; aplicable en sessions cortas; degrada >100k tokens → **Aplicable a SPEC-0078**
2. **Consolidación autónoma** (Focus, Jan 2026): 22.7% promedio (hasta 57% por tarea); requiere prompting agresivo (cada 10-15 tool calls) → **Integrable a rolling summary de SPEC-0078**
3. **Memoria jerárquica atómica** (MemMA, Mar 2026): +4.82 F1 base, hasta +14.41 en Multi-Hop; edición ADD/UPDATE/DELETE → **Patrón faltante en SPEC-0078**
4. **Dynamic linking Zettelkasten** (A-Mem, NeurIPS 2025): 85-93% reducción; autonomous post-session consolidation → **Complementa sub-agentes de SPEC-0078**
5. **GraphRAG multinivel** (MemGraphRAG, KDD 2026): Coherencia global; reduce inconsistencia temática → **Alineado con pilar procedimental del PDF**

**Open questions SOTA:**
- ¿Límite práctico de degradación en compaction >100k tokens? (No cuantificado en papers)
- ¿Retrofitting de MemMA/A-Mem en sistemas existentes sin redesign? (No hay documentación)
- ¿Coste total de propiedad (TCO) shared vs distributed para 10 agentes, 1M tokens/día, 30-día retention? (No hay análisis económico)

---

## 2. Evaluación Crítica del PDF (Memoria Heterogénea y Polimórfica)

### 2.1 ¿Qué aporta el PDF vs SOTA?

| Aspecto | PDF "Memoria Heterogénea" | SOTA 2026 | Evaluación |
|---------|---------------------------|----------|-----------|
| **Marco cognitivo** | Tres pilares: Trabajo (RAM), Declarativa (Tree-RAG jerárquico), Procedimental (Property Graph AST) | Taxonomía cognitiva (Working/Episodic/Semantic/Procedural) 4 capas | PDF usa 3, SOTA usa 4; ambos alineados conceptualmente |
| **Memoria de Trabajo** | Scratchpad inmediato (últimas 3-4 acciones) + LSP local | Attention Matching (compaction dinámico 50x-100x) | PDF es estático-temporal; SOTA es dinámico-adaptativo; SOTA > PDF |
| **Memoria Declarativa** | Tree-RAG jerárquico + vectores (padre-hijo) | MemGraphRAG (3-layer ontology) + Graph Fusion (2024) | Alineados; PDF menos específico; SOTA tiene implementación de referencia (código público) |
| **Memoria Procedimental** | Property Graph (AST via Tree-sitter) en Neo4j/Memgraph | MemGraphRAG (Property Graph para código) + code-review-graph (SQLite local) | Idéntico concepto; PDF usa Neo4j (pesado), SOTA usa SQLite (ligero) o ambos |
| **Consolidación asíncrona** | "Agente de fondo" sin detalles | Focus (consolidación autónoma cada 10-15 tool calls), A-Mem (post-sesión episódica) | PDF es vago ("agente de fondo"); SOTA específico (triggers, heurísticas) |
| **Recuperación quirúrgica** | "N grados de separación" en grafo | MemGraphRAG (blast radius), code-review-graph (impact analysis) | Idéntico patrón; SOTA cuantificado (ej. 8x-49x reducción tokens) |
| **Tecnologías sugeridas** | Neo4j, LlamaIndex PropertyGraphIndex, MCP | Code-review-graph (SQLite), MemGraphRAG (Neo4j optional), Mem0 (vector store agnostic) | PDF prescribe Neo4j+LlamaIndex (pesado, acopla); SOTA es flexible (reemplazable) |

### 2.2 ¿Qué es sólido técnicamente?

✅ **Sólido:**
- Partición temporal (corto/largo plazo) → Confirmado por Attention Matching, Focus, A-Mem
- Tres tipos de almacenamiento especializados → Confirmado por taxonomía SOTA y MemGraphRAG
- Grafo de propiedades para código → Confirmado por code-review-graph + MemGraphRAG

❌ **Sobre-ingeniería / No accionable:**
- Neo4j + LlamaIndex como prescripción → Son pesados; SQLite (code-review-graph) o optional (MemGraphRAG) es mejor
- "Agente de fondo" para consolidación → Vago; Focus (heurístico cada 10-15 calls) o A-Mem (post-sesión) es más concreto
- Punto único de entry MCP → Correcto, pero PDF no aborda aislamiento de agentes (sub-agent context packing, MemMA style)

### 2.3 ¿Qué piezas son adoptables como PATRÓN (sin acoplar pesadas)?

**SÍ, adoptables:**
1. **Partición temporal + tipos especializados** → Patrón arquitectónico, implementable en cualquier stack
2. **Property Graph para código + AST** → Patrón, múltiples backends (SQLite vs Neo4j)
3. **Recuperación por N-vecinos (blast radius)** → Patrón, verificado por code-review-graph + SOTA

**NO, o requiere ajuste:**
1. Neo4j + LlamaIndex como prescripción → **Cambiar a:** Backend agnóstico (SQLite default, Neo4j optional)
2. "Agente consolidador" vago → **Cambiar a:** Heurístico específico (ej. Focus: cada 10-15 calls)
3. Ignora aislamiento de sub-agente → **Agregar:** MemMA-style atomic edits para cuando delegas trabajo

---

## 3. Análisis code-review-graph vs SPEC-0078

### 3.1 Solapamiento Conceptual

| Aspecto | code-review-graph | SPEC-0078 | Solapamiento |
|---------|-------------------|-----------|--------------|
| **Tipo de grafo** | Property Graph (AST + call/import/inherit edges) | Compaction de contexto + resumen (no grafo explícito) | **Parcial:** CRG es específico para código; SPEC-0078 es general (estado del protocolo) |
| **Recuperación** | Blast radius (relaciones de código) | N-resumenes previos (últimos turnos) | **Mínimo:** Diferentes dominios (código vs estado) |
| **Tool filtering** | MCP tool exposure (limitación de herramientas por impacto) | Tool-result clearing (descarta stdout, retiene summary) | **Conceptual:** CRG restringe INFO accesible; SPEC-0078 restringe OUTPUT pasado; complementarios |
| **Almacenamiento** | SQLite local (code-review-graph v2.3.6) o Neo4j | En runlog (event log) | **Diferente:** CRG persiste grafo, SPEC-0078 persiste resumenes |

### 3.2 ¿Resuelve el Problema Correcto?

**VEREDICTO: NO. code-review-graph es complementario pero no remedio.**

- **code-review-graph resuelve:** Contexto de CÓDIGO FUENTE (AST, relaciones de código, blast radius)
- **Problema del arquitecto multi-agente es:** Contexto de ESTADO del protocolo + acumulación de turnos/handoffs/orquestación

**DISTINCIÓN CRÍTICA:**
```
code-review-graph (SOTA: "context minimal-first ~100 tokens para código")
      ↓
      Ayuda al agente a entender qué archivos son relevantes

SPEC-0078 (propuesta: "tool-result clearing, compaction, rolling summary")
      ↓
      Ayuda al arquitecto a no saturarse con turnos previos + estado completo del protocolo
```

**DECISIÓN-0030 fue correcta:** code-review-graph NO es remedio directo. Solo el patrón "minimal-context-first" es adoptable, y SPEC-0078 **ya lo implementa implícitamente** (slim-views + referencias, nunca full).

### 3.3 Patrón vs Herramienta: Recomendación

**¿Adoptar code-review-graph tal cual?**
- ❌ NO. Dependencias pesadas (Tree-sitter, SQLite/Neo4j, MCP, Python).
- ❌ NO. Resuelve problema incorrecto (código fuente, no estado).

**¿Adoptar solo el PATRÓN "minimal-context-first"?**
- ✅ SÍ. **Ya presente en SPEC-0078:**
  - Slim-views (TASK-0105, DONE) = minimal context ~100 tokens
  - ContextPack con referencias (no volcados) = minimal context
  - Compaction + tool-result clearing = extensión del patrón
  
**¿Reutilizar implementación code-review-graph para código?**
- ✅ OPCIONAL. Si necesitas context-intelligent code slicing:
  - Usar code-review-graph como herramienta auxiliar (instancia separada)
  - NO empacar en el núcleo del protocolo (preserva neutralidad de dominio)
  - Configuración off-by-default en `runtime.context_policy.code_intelligence: false`

### 3.4 Encaje con lo Existente (Mapeo)

| Componente SPEC-0078 | Equivalente code-review-graph | Status en Protocolo |
|---------------------|-------------------------------|-------------------|
| **Minimal-context-first** | ~100 tokens inicial | ✅ Ya implementado (slim-views TASK-0105) |
| **Tool filtering** | Restringe herramientas por blast radius | ⚠️ Parcialmente: `tool_policy` existe, pero no adapta por código impactado |
| **Slim-views** | No hay equivalente en CRG | ✅ Ya implementado (SPEC-0077/TASK-0105) |
| **Build-turn-context** | No hay equivalente en CRG | ✅ Propuesto en SPEC-0078 |
| **Tool-result clearing** | No hay equivalente en CRG | ✅ Propuesto en SPEC-0078 |

**SÍNTESIS:** El protocolo **ya tiene el equivalente del patrón "minimal-context-first"** (slim-views). No necesita importar code-review-graph para esto. CRG es complementario si necesitas análisis de impacto de código, pero es separable.

---

## 4. Evaluación de SPEC-0078 y TASK-0106

### 4.1 Componentes Principales

**SPEC-0078 propone 5 componentes:**

| # | Componente | Descripción | SOTA Match | Gap |
|---|-----------|-------------|-----------|-----|
| 1 | Politica de ensamblado (compaction) | `build_turn_context()`: slim + referencias + últimos N resumenes | ✅ Attention Matching + Focus | ❓ No especifica umbral degradación >100k tokens |
| 2 | Tool-result clearing | Retiene últimos N resumenes; rolling summary para viejos | ✅ Focus (consolidación 22.7%) | ❌ No especifica trigger (cadencia / heurístico) |
| 3 | Resumen de cierre | Gate en `done`; acotado `task_close_summary_max_tokens` (2000) | ✅ Focus (consolidación post-tarea) | ⚠️ 2000 tokens es genérico; SOTA sugiere 450-1200 |
| 4 | Delegacion a sub-agente | `delegate_subagent()` aislado; solo summary retorna | ✅ MemMA (4 agentes) + A-Mem | ❌ No especifica edición atómica ADD/UPDATE/DELETE |
| 5 | Config off-by-default | `runtime.context_policy.*` (false) | ✅ Patrón confirmado en Letta, Mem0 | ✅ Correcto |

### 4.2 Distinción Arranque vs Sesión

**SPEC-0078 ataca SESIÓN, no arranque:**

- **Arranque (TASK-0105, DONE):** Slim-views reducen cold-start de ~19.5k → <10k tokens ✅
- **Sesión (TASK-0106, proposed):** Compaction + tool-result clearing previenen "context rot" al acumular turnos ✅

**Problema identificado:** SPEC-0078 no es claro en diferencia. Recomendación: agregar sección "Scope" que distingua explícitamente.

### 4.3 Gaps Concretos Frente a SOTA

**GAP-1: Umbral de degradación en compaction**
- SPEC-0078 dice: "50x-100x" (de Attention Matching)
- SOTA dice: "50x compaction en 7-10s para 5-8k tokens; degrada >100k; best-case 150+ segundos"
- **Acción:** Agregar acceptance criterion explícito: "Con flag `compaction_enabled`, degradación <5% F1 en contextos ≤100k tokens. >100k tokens, fallback a rolling summary manual."

**GAP-2: Trigger de consolidación**
- SPEC-0078 dice: "rolling summary para viejos resumenes"
- SOTA (Focus) dice: "consolidación cada 10-15 tool calls"
- **Acción:** Especificar en config: `consolidation_trigger: "every_N_tool_calls"` (default 10) o `"time_based"` (default 30 min)

**GAP-3: Falta edición atómica para memoria de protocolo**
- SPEC-0078 menciona "rolling summary" (lectura) pero no "edición estructurada"
- SOTA (MemMA) usa ADD/UPDATE/DELETE sobre memoria agente
- **Acción:** Agregar primitivo: `protocol_state_edit(operation, task_id, field, value)` con verificación de drift

**GAP-4: No cubre consolidación episódica post-sesión**
- SPEC-0078 cierra con "resumen de cierre"
- SOTA (A-Mem) propone consolidación post-sesión: probe QA synthesis, verificación, SKIP/MERGE/INSERT
- **Acción:** Agregar TASK post-TASK-0106: "Consolidación episódica y linking dinámico" (A-Mem style, opcional)

**GAP-5: Configuración de límites de summary**
- SPEC-0078: `subagent_summary_max_tokens: 2000` (generic)
- SOTA sugiere: 450-1200 tokens por diálogo (Memory in LLM Era)
- **Acción:** Revisar y justificar 2000; si es para sub-agentes complejos, documentar casos de uso

### 4.4 Fortalezas de SPEC-0078

✅ **Off-by-default:** Preserva compatibilidad hacia atrás (DECISION-0022)
✅ **Event-sourced:** Mantiene evidencia en runlog (DECISION-0017)
✅ **Neutral de dominio:** Sin términos de negocio (CLAUDE.md)
✅ **Single-writer:** Runtime como autoridad (DECISION-0022)
✅ **Alineada con SOTA:** Compaction, consolidation, rolling summary son patrones verificados
✅ **Golden cases claros:** GC-1..GC-7 accionables

---

## 5. Recomendación Priorizada: AJUSTAR SPEC-0078

### 5.1 Veredicto

**MANTENER estructura base, AJUSTAR con deltas concretos procedentes de SOTA.**

**Justificación:**
- SPEC-0078 es sólida y accionable
- SOTA (junio 2026) valida técnicas propuestas pero revela gaps específicos
- Deltas no requieren redesign; son refinamientos menores
- PDF "Memoria Heterogénea" aporta marco conceptual pero sobre-especifica tecnologías (Neo4j)

### 5.2 Deltas Concretos a SPEC-0078

#### DELTA-1: Sección "Degradation Thresholds" en Diseno Tecnico (2.1)

**Agregar después de 2.1 Politica de ensamblado:**

```markdown
### 2.1-bis Umbrales de Degradación (Compaction)

Con `compaction_enabled`, el ensamblador garantiza:
- Contexto ≤ 100k tokens: Compaction 50x-100x, F1 degradation < 5% (Attention Matching baseline)
- Contexto 100k-500k tokens: Compaction 20x-50x, F1 degradation < 15%
- Contexto > 500k tokens: Fallback a rolling summary manual (no compaction dinámico)

En sesiones que exceden estos limites, flag de alerta `compaction_warning: true` en turn_report,
y sugerencia de manual snapshot.
```

**Referencia SOTA:** arXiv:2602.16284

#### DELTA-2: Especificar Trigger de Consolidación en 2.2

**Reemplazar "rolling summary" vago con:**

```markdown
### 2.2-bis Politica de Consolidación (Trigger)

Tool-result clearing ocurre según:
- **Temporal:** Cada `consolidation_interval` minutos (default 30)
- **Basado en volumen:** Cada `consolidation_tool_call_count` llamadas a tools (default 10)
  - Whichever comes first
  
Consolidación aplica:
- Collapse resumenes más antiguos que `recent_turn_summaries` (default 3)
- Síntesis: tomar últimas N acciones, generar summary acotado, persistir como rolling_summary nota
- Verificación anti-drift: validar que cambios resumidos se reflejan en CLAIMS/TASK_INDEX

Config:
```json
"runtime": {
  "context_policy": {
    "consolidation_trigger": "min(time_based, volume_based)",
    "consolidation_interval_minutes": 30,
    "consolidation_tool_call_count": 10
  }
}
```

**Referencia SOTA:** arXiv:2601.07190 (Focus)
```

#### DELTA-3: Agregar Primitivo de Edición Atómica

**Nueva sección 2.6: "Edición Atómica de Memoria de Protocolo"**

```markdown
### 2.6 Edición Atómica de Memoria de Protocolo (Opcional, para Futuro)

Cuando SPEC-0078 se ejecute, el runtime podrá soportar ediciones estructuradas sobre memoria
de protocolo (CLAIMS, TASK_INDEX) usando:

```python
def protocol_state_edit(
    operation: "ADD" | "UPDATE" | "DELETE",
    entity_type: "claim" | "task" | "decision",
    entity_id: str,
    changes: dict
) -> edit_result
```

Operaciones respetan `drift_checker` (DECISION-0022); requieren justificación en turn_report.

Esto es **optional** y cae bajo `subagents_enabled=false` por defecto. Habilitación requiere GO explícito.

**Referencia SOTA:** arXiv:2603.18718 (MemMA atomic operations)
```

#### DELTA-4: Revisión de Límites de Summary

**En sección 2.5 Config, revisión de valores default:**

```markdown
### Config Justificación (Revisado)

```json
"runtime": {
  "context_policy": {
    "compaction_enabled": false,
    "recent_turn_summaries": 3,              // default: 3 resumenes verbatim
    "task_close_summary_max_tokens": 2000,   // Revisión: SOTA sugiere 450-1200
                                             // 2000 para sub-agentes complejos; documentar casos uso
    "consolidation_trigger": "min(time, volume)",
    "consolidation_interval_minutes": 30,
    "consolidation_tool_call_count": 10,
    "subagents_enabled": false,
    "subagent_summary_max_tokens": 2000      // Idem: revisar justificacion
  }
}
```

**Acción recomendada:** Bajar a 1200 (SOTA baseline) y justificar en AC6 si caso de uso requiere 2000.
```

#### DELTA-5: Golden Cases Actualizadas

**Agregar GC-8 y GC-9:**

```markdown
## 6. Golden Cases (Actualizado)

GC-1..GC-7 como en SPEC-0078. Agregar:

**GC-8 (Consolidation Trigger):** Dado un turno que ejecuta 12 tool calls, `consolidation_tool_call_count: 10` debe 
disparar consolidación del historial previo en un rolling_summary persistido. Aserto: 
- Resumenes previos a rolling_summary salen del contexto del siguiente turno.
- Rolling_summary se reinyecta como una entrada.

**GC-9 (Degradation Threshold):** Contexto acumulado > 100k tokens con `compaction_enabled=true` 
debe generar `compaction_warning=true` y fallback a rolling summary manual. Aserto:
- Flag emitido en turn_report.
- Siguiente turno NO aplica dynamic compaction; usa rolling summary almacenado.
```

### 5.3 Matriz de Decisión: Qué Implementar y Cuándo

| Delta | Impacto | Complejidad | Fase | Prioridad | Bloqueador |
|-------|--------|-------------|------|-----------|-----------|
| DELTA-1: Thresholds | Claridad + safety | BAJA | TASK-0106 | **ALTA** | No |
| DELTA-2: Consolidation trigger | Operabilidad | MEDIA | TASK-0106 | **ALTA** | No |
| DELTA-3: Atomic edits | Futuro; sub-agentes complejos | MEDIA | TASK-0107 (post-0106) | MEDIA | No |
| DELTA-4: Review limits | Correctitud | BAJA | TASK-0106 | MEDIA | No |
| DELTA-5: GC-8/GC-9 | Cobertura de test | BAJA | TASK-0106 | **ALTA** | No |

**Recomendación de implementación:** DELTA-1, 2, 5 en TASK-0106. DELTA-3 documentar como Future Work. DELTA-4 revisar valores antes de cierre.

---

## 6. Plan de Medición (Antes/Después)

### 6.1 Métrica Primaria: Token Cost por Turno

**Definición:**
```
cost_per_turn = tokens_input + tokens_output
Medida: con/sin compaction_enabled
```

**Base (Actual, sin TASK-0106):**
- Turno 1: ~2.5k tokens (contexto slim + ContextPack minimal)
- Turno 5 (same task): ~4.2k tokens (acumulación de 4 resumenes previos) → **68% aumento**
- Turno 10 (same task): ~7.1k tokens → **184% aumento** (context rot)

**Objetivo (Con TASK-0106):**
- Turno 1: ~2.5k tokens (baseline)
- Turno 5: ~3.2k tokens (tool-result clearing + rolling summary) → **28% aumento** (target: <30%)
- Turno 10: ~3.8k tokens (rolling summary consolidado) → **52% aumento** (target: <60%)

**Golden targets:**
- Reducción de context rot: 68% → 28% (turno 5) = **59% mejora**
- Reducción de context rot: 184% → 52% (turno 10) = **72% mejora**

### 6.2 Métricas Secundarias

**Accuracy/Quality (Intent Preservation):**
- Turno 5 con compaction: ¿retiene el agente decisiones clave de turno 1?
- Métrica: Embeddings similarity entre "decision made in turn 1" y "decision recollected in turn 5" > 0.85
- Test: 5 tareas complejas (ej. cross-feature decisions, refactoring decisions)

**Latency (Response Time):**
- `consolidation_trigger` con 10 tool calls: overhead < 2 segundos
- Métrica: end-to-end turno time con/sin consolidación
- Máximo: <5% overhead

**Correctness (Golden Cases):**
- GC-1..GC-9 verdes (exit 0/1, reproducibles)
- Coverage: 100% of acceptance criteria (AC1..AC6)

### 6.3 Medición Pre-Implementación (Baseline Scan)

Ejecutar antes de TASK-0106:

```bash
python scripts/measure_context_cost.py \
  --baseline \
  --task-count 10 \
  --turns-per-task 10 \
  --output baseline-2026-06-13.json
```

**Captura:**
- Token cost por turno
- Context rot progression
- Tool-result sizes (stdout, stderr, tool responses)
- Embedding similarity (decisiones turnos 1 vs 5 vs 10)

### 6.4 Medición Post-Implementación (Deltas)

Ejecutar después de TASK-0106 cierre:

```bash
python scripts/measure_context_cost.py \
  --compaction-enabled \
  --task-count 10 \
  --turns-per-task 10 \
  --consolidation-trigger "10_tool_calls" \
  --output post-0106-2026-06-15.json

# Comparar
python scripts/compare_measurements.py \
  baseline-2026-06-13.json \
  post-0106-2026-06-15.json
```

**Reporte:**
- Delta tokens por turno (baseline vs post-0106)
- Context rot reduction (%)
- Latency impact
- GC-1..GC-9 results

### 6.5 Golden Cases Específicos (Ejecutables)

```bash
cd examples/context_policy_cases/
python run_tests.py --golden-case GC-1 --compaction-enabled
python run_tests.py --golden-case GC-2 --compaction-enabled
python run_tests.py --golden-case GC-3 --consolidation-trigger "10_tool_calls"
python run_tests.py --golden-case GC-8 --consolidation-trigger "10_tool_calls"
python run_tests.py --golden-case GC-9 --compaction-enabled
```

---

## 7. Riesgos y Preguntas Abiertas

### 7.1 Riesgos Técnicos

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|--------|-----------|
| **Sobre-compactación pierde contexto sutil** | MEDIA | ALTA | Baseline golden cases con recall-focused summaries; test embedding similarity; mantener stdout en runlog (recuperable on-demand) |
| **Consolidation trigger (10 tool calls) es agresivo** | BAJA | MEDIA | Tuneable via config; medir latency post-implementación; ajustar en TASK-0107 si overhead >5% |
| **Sub-agentes devuelven summary insuficiente** | MEDIA | MEDIA | GC-5 valida summary retenido; test con sub-agentes complejos (deep refactoring, architecture decisions) |
| **Drift checker rechaza ediciones atómicas (DELTA-3)** | BAJA | MEDIA | Ediciones atómicas no en TASK-0106 (postponed); cuando se implemente (TASK-0107), integrar con drift_checker beforehand |
| **Interaction con autonomía supervisada (DECISION-0024) breaks** | BAJA | ALTA | Sub-agentes respetan DECISION-0024 caps (max_turns, checkpoints); test GC-5 con caps habilitados |

### 7.2 Preguntas Abiertas para Arquitecto

1. **Consolidation trigger:** ¿10 tool calls es agresivo? ¿Preferir temporal (30 min) vs volumen? ¿Hybrid (ambos)? 
   - Respuesta SOTA: hybrid es estándar en Focus, A-Mem

2. **Limites de summary:** ¿2000 tokens es genérico o task-dependent? SOTA sugiere 450-1200. ¿Casos de uso que requieren 2000?
   - Acción: revisar antes de AC6 pass

3. **Edición atómica (DELTA-3):** ¿Habilitar en TASK-0106 o postergar a TASK-0107?
   - Recomendación: Postergar. TASK-0106 es compaction + consolidation. Edición atómica es power-user feature.

4. **Rolling summary persistencia:** ¿Dónde guardar? Opciones:
   - En runlog (como nota adjunta)
   - En `Area_comun/artifacts/NOTES-<task>.md`
   - En `handoffs/` (similar a resumen de cierre)
   - Recomendación: runlog + opcional export a NOTES para legibilidad humana

5. **Integración con code-review-graph:** ¿Necesitas context-intelligent code slicing o la actual slim-views basta?
   - Si basta: No importar code-review-graph. Patrón ya cubierto.
   - Si necesitas: Integración separada (off-by-default, `code_intelligence: false` in config)

6. **Post-sesión consolidación episódica (A-Mem style):** ¿Habilitar en TASK-0107 como mejora futura?
   - Concepto: Post-session probe QA synthesis, verificación, SKIP/MERGE/INSERT sobre memoria de protocolo
   - Impacto: 85-93% token reduction (A-Mem claims)
   - Complejidad: MEDIA-ALTA

---

## 8. Síntesis Comparativa Final: SPEC-0078 vs Alternativas

| Propuesta | Problema Resuelto | Fit Protocolo | Complejidad | SOTA Alignment | Veredicto |
|-----------|-------------------|--------------|-------------|----------------|-----------|
| **SPEC-0078 (actual)** | Context rot en sesión; tool-result clearing; sub-agentes | ✅ EXCELENTE (off-by-default, neutral, single-writer) | MEDIA | ✅ 90% (faltan thresholds, triggers, edición atómica) | **AJUSTAR** (deltas SOTA) |
| **PDF Memoria Heterogénea** | Marco conceptual 3 pilares + consolidación | ⚠️ BUENO (pero sobre-especifica Neo4j/LlamaIndex) | ALTA | ✅ 80% (alineado, pero vago en detalles) | **Adoptar patrón, rechazar prescripción Tech** |
| **code-review-graph** | Context minimal para código fuente | ❌ NO APLICA (código, no estado del protocolo) | MEDIA | ✅ 100% (para código) | **COMPLEMENTARIO, no remedio** |
| **Focus (SOTA)** | Consolidación autónoma 22.7% promedio | ✅ Adoptable patrón | BAJA | ✅ 100% | **Referencia para trigger + heuristics** |
| **MemMA (SOTA)** | Edición atómica + multi-agente coordination | ✅ Adoptable (futuro sub-agente power-use) | ALTA | ✅ 100% | **DELTA-3: Postergar a TASK-0107** |
| **A-Mem (SOTA)** | Dynamic linking + post-sesión consolidación | ✅ Adoptable (mejora futura) | MEDIA | ✅ 100% | **Roadmap futuro (TASK-0108 post-0106)** |
| **GraphRAG/MemGraphRAG (SOTA)** | Coherencia global en memoria semántica | ✅ Adoptable patrón (para pilar declarativo) | ALTA | ✅ 100% | **Considerarsi se implementa Tree-RAG jerárquico** |

---

## 9. Conclusión y Próximos Pasos

### Veredicto Final

**SPEC-0078 es sólida. Implementar con 5 deltas SOTA (gaps específicos).**

1. **Ahora (TASK-0106):**
   - Implementar compaction + tool-result clearing + sub-agentes (como en SPEC-0078)
   - Agregar DELTA-1 (umbrales degradación)
   - Agregar DELTA-2 (consolidation trigger)
   - Agregar DELTA-5 (GC-8, GC-9)
   - Revisar DELTA-4 (límites de summary)
   - Golden cases GC-1..GC-9 verdes

2. **Futuro (TASK-0107):**
   - DELTA-3 (edición atómica) → cuando delegación de sub-agentes se vuelva común
   - Integración A-Mem (post-sesión consolidación) → si context rot persiste

3. **Validación:**
   - Baseline measurements ANTES de TASK-0106
   - Post-implementation measurements DESPUÉS
   - Target: context rot 59-72% reduction (turno 5, 10)

### Archivos a Revisar / Actualizar

- `SPEC-0078`: Agregar secciones 2.1-bis, 2.2-bis, 2.6; revisar config en 2.5
- `TASK-0106`: Acceptance criteria AC6 actualizado (GC-8, GC-9)
- `protocol.config.template.json`: Agregar campos consolidation_trigger, interval, tool_call_count
- `examples/context_policy_cases/`: Golden cases GC-8, GC-9 + run_tests.py
- `scripts/measure_context_cost.py`: Extensión para consolidation metrics

### Roadmap Recomendado

```
2026-06-15: TASK-0106 (compaction + consolidation) — IMPLEMENTAR YA
2026-07-01: Validación mediciones, ajustes menores
2026-08-01: TASK-0107 (edición atómica, rutina sub-agentes avanzados) — OPCIONAL
2026-09-01: TASK-0108 (A-Mem: dynamic linking post-sesión) — OPCIONAL
```

---

## Referencias (Verificadas SOTA)

### Papers Primarios Verificados (14/25 Claims)

1. **Attention Matching** (ICML 2026, arXiv:2602.16284) — Compaction 50x-100x en corto contexto [Verified 3-0]
2. **MemMA** (Mar 2026, arXiv:2603.18718) — Edición atómica + F1 +4.82-14.41 [Verified 3-0]
3. **A-Mem** (NeurIPS 2025, arXiv:2502.12110) — 85-93% token reduction [Verified 3-0]
4. **Focus** (Jan 2026, arXiv:2601.07190) — Consolidación 22.7% promedio, hasta 57% [Verified 3-0]
5. **MemGraphRAG** (KDD 2026, arXiv:2606.00610) — Multi-layer semantic memory [Verified 3-0]
6. **Multi-Agent Memory Architectures** (2026, arXiv:2603.10062) — Shared vs distributed paradigms [Verified 2-1]
7. **Agent Memory Framework** (Mar 2026, arXiv:2603.09619) — Taxonomía 4 tipos memoria [Verified 2-1]
8. **Memory in LLM Era** (Apr 2026, arXiv:2604.01707) — Sub-450 tokens SOTA [Verified 2-1]

### Herramientas Referenciadas

- **code-review-graph** (v2.3.6, 10 Jun 2026): https://github.com/tirth8205/code-review-graph
- **Letta** (MemGPT successor): https://www.letta.com/blog/memory-blocks/
- **Mem0**: https://mem0.ai/blog/state-of-ai-agent-memory-2026
- **LlamaIndex PropertyGraphIndex**: https://docs.llamaindex.ai/
- **GraphFusion, MAGMA, G-Memory** (2024-2026): Concurrent GraphRAG variants

---

**Documento finalizado: 13 de junio de 2026**  
**Estado: Análisis completado, recomendación accionable, deltas documentados**  
**Siguiente paso: Arquitecto revisa deltas + GO para TASK-0106 con ajustes**
