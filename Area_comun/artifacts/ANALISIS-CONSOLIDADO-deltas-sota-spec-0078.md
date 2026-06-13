# ANÁLISIS CONSOLIDADO — Deltas SOTA para SPEC-0078 (TASK-0109)

**Consolidador:** Claude (arquitecto). **NO es una voz**: reconcilia las 3 voces independientes.
**Fecha:** 2026-06-13 · **Tarea:** TASK-0109 (analysis) · **Deliverable.**
**Insumos (3 voces, maker≠checker, ninguna leyó a las otras durante la producción):**
- `VOZ-OPERADOR-revision-deltas-sota.md` (valor/riesgo)
- `ANALISTA-deltas-sota-spec-0078.md` (fuentes/SOTA)
- `VOZ-CODEX-factibilidad-deltas-sota.md` (factibilidad)
- Base: `PROPUESTA-deltas-sota-spec-0078.md` (= borrador DECISION-0031), `ESTUDIO-...`, `SPEC-0078`.

> **Estado:** este artefacto es el deliverable de TASK-0109. La actualización de SPEC-0078, la reemisión
> limpia de DECISION-0031 y el handoff a TASK-0106 **NO** se ejecutan aquí: esperan GO del operador.
> TASK-0106 / SPEC-0078 siguen **GATED**.

---

## 0. Veredicto consolidado (5 líneas)

1. SPEC-0078 base es **sólida** (neutral, single-writer, event-sourced, off-by-default): **no requiere redesign**.
2. El problema es de **trazabilidad de fuentes**, no de diseño: **DELTA-1 y DELTA-2 citan mal sus papers**
   (números/heurísticas que el paper no contiene). Confirmado **independientemente** por las 2 voces analíticas.
3. **Principio rector (DECISION-0008):** umbrales y cadencias salen de **`measure_context_cost` baseline propio**,
   no de citas. Se **BLOQUEA el freeze** de umbrales/cadencias hasta correr ese baseline.
4. **Alcance TASK-0106 = mínimo seguro:** medición + límites + tool-result clearing + trigger determinista
   provisional + goldens estructurales. DELTA-3 difiere a TASK-0107 (Future Work).
5. **GO condicional:** DELTA-3 y DELTA-5 directos; DELTA-1/2/4 condicionados a medición propia + corrección de
   procedencia. Rechazar toda deriva a Neo4j/LlamaIndex/servicio de memoria persistente.

---

## 1. Las 3 voces y su convergencia

| Delta | Operador (valor/riesgo) | Analista (fuentes/SOTA) | Codex (factibilidad) | Consolidado |
|-------|-------------------------|--------------------------|----------------------|-------------|
| DELTA-1 | Descartar como está; umbral = límite medido | Reformular; 2602.16284 KV-cache no aplica a CLI | Reformular; medir `assembled_context_tokens` en `build_turn_context` | **REFORMULAR** |
| DELTA-2 | Reformular; cadencia de nuestra medición, no de Focus | Reformular; "10 calls" no es de Focus (autónomo) | Reformular; trigger determinista; overhead `<5%` medido | **REFORMULAR** |
| DELTA-3 | Fuera de 0106; futuro; solo `submit_intent` | Mantener Future Work; patrón MemMA (sin coord. 4-agentes) | Diferir; choca con escritor único si no pasa por `submit_intent` | **DIFERIR (TASK-0107)** |
| DELTA-4 | Mantener (idea), por medición propia | Decidir+justificar; 2604.01707 no-verificable | Reformular; límite por baseline propio | **REFORMULAR (medir)** |
| DELTA-5 | Mantener; sin números inventados | Mantener; GC-9 sobre umbral medido | Implementable; asertos estructurales + umbrales medidos | **MANTENER** |

**Convergencia 3-0 en dirección.** Las dos voces analíticas (Analista, Codex) llegaron al mismo veredicto
por delta **sin leerse durante la producción** (cross-check post-entrega). Alineación plena con el
meta-criterio del operador.

---

## 2. SET DE DELTAS CORREGIDO

### DELTA-1 — Umbrales de degradación → **REFORMULAR**

- **Procedencia corregida:** quitar la atribución a **arXiv:2602.16284** (Attention Matching). Es
  compactación de **KV-cache en espacio latente** (capa de inferencia/atención): el runtime arma contexto
  **plano** para stdin del CLI y **no controla** la atención del backend. Los cortes ">100k" y "F1 <5%/<15%"
  **no están en el paper**; son interpolación del ESTUDIO. No presentarlos como "verificados desde SOTA".
- **Mecanismo (se conserva):** warning + fallback por umbral de tamaño del contexto **ensamblado**.
- **Refinamiento de Codex (integrado):** el equivalente real y medible es instrumentar
  **`assembled_context_tokens`** (o proxy) en **`build_turn_context`** y disparar warning/fallback por un
  **umbral propio configurable**. Es el punto de control que el runtime sí posee (antes de la llamada CLI).
- **Valores:** **derivados de `measure_context_cost` baseline (DECISION-0008)**, no de citas. **Bloqueado** el
  freeze hasta correr el baseline.
- **AC (reformulado):** "Con el límite activo, si `assembled_context_tokens` supera el umbral **medido**, se
  emite `compaction_warning` y se aplica fallback; los cortes provienen del baseline propio, no de papers."
- **Coste/factibilidad (Codex):** BAJA-MEDIA. **En scope 0106.**

### DELTA-2 — Trigger de consolidación → **REFORMULAR**

- **Procedencia corregida:** quitar la atribución a **arXiv:2601.07190** (Focus). Focus es un mecanismo
  **agente-autónomo** (decide cuándo consolidar por atención propia); **no** especifica "cada 10-15 tool calls",
  y el 22.7% **no** se deriva de esa cadencia. La heurística es adición del ESTUDIO.
- **Patrón (se conserva):** trigger **determinista** del runtime (por N tool-results / T minutos / tokens
  acumulados desde la última consolidación) — correcto para single-writer; encaja en `orchestrator`/`runlog`.
- **"10 tool calls" = PROVISIONAL/tuneable**, NO baseline de Focus.
- **Refinamiento de Codex (integrado):** el objetivo **`overhead <5%`** es un **gate MEDIDO** (construcción +
  consolidación vs wall-time del turno y delta de tokens enviados), **no un supuesto**. Además: **preferir
  consolidación barata y FUERA del hot path** — evitar una **llamada a LLM en caliente** para resumir, porque
  ese coste puede **superar** el margen del 5%.
- **AC (reformulado):** "Cadencia inicial **provisional**; se ajusta tras medición. Objetivo **overhead <5%**
  validado contra baseline propio; la consolidación no debe invocar un LLM en el hot path del turno."
- **Coste/factibilidad (Codex):** MEDIA. **En scope 0106** (trigger provisional + clearing).

### DELTA-3 — Edición atómica de memoria de protocolo → **DIFERIR (Future Work, TASK-0107)**

- **Fuente:** **arXiv:2603.18718** (MemMA) **CONFIRMADO como patrón** (ops ADD/UPDATE/DELETE). **Caveat:** el
  paper asume **4 agentes** (Meta-Thinker + Memory Manager); se adopta el **patrón**, no la coordinación
  multi-agente.
- **Regla del operador (integrada, innegociable):** si algún día entra, **EXCLUSIVAMENTE vía `submit_intent`**
  (transacción con rollback/idempotencia/drift-gate). **Nunca** edición directa de CLAIMS/TASK_INDEX/PROJECT_STATE
  — editar estado fuera del flujo es justo lo que causó el drift reparado con re-genesis esta sesión.
- **Alcance:** **FUERA de TASK-0106.** Solo se documenta como §2.6 Future Work, off-by-default. Implementación =
  TASK-0107 (si la delegación a sub-agentes lo requiere).

### DELTA-4 — Límites de summary → **REFORMULAR (decidir por medición)**

- **Fuente:** **arXiv:2604.01707** **NO-VERIFICABLE** (verificado solo 2-1 en el propio ESTUDIO; sin acceso a
  cifras). El rango **450-1200 es GUÍA, no ley**.
- **Acción:** **no** bajar a 1200 "porque el paper". Decidir 2000 vs 1200 (e idéntico para
  `subagent_summary_max_tokens`) según **medición propia** del tamaño real de resúmenes; **justificar en
  SPEC-0078 §2.5**. 2000 conservador es defendible si se justifica.
- **Coste/factibilidad (Codex):** BAJA. **Revisión antes del cierre de 0106** (no congela número heredado).

### DELTA-5 — Golden cases GC-8 / GC-9 → **MANTENER (asertos estructurales)**

- **Sin paper requerido** (cobertura de test).
- **Corrección:** los asertos NO se construyen sobre números heredados (F1, KV-cache, cifras de papers). Deben
  verificar **comportamiento estructural** + **umbral MEDIDO**:
  - **GC-8 (trigger/clearing):** tras > N tool-results, el siguiente contexto **no** incluye cuerpos antiguos;
    el `runlog` conserva **referencia recuperable**; el drift-checker pasa.
  - **GC-9 (umbral de degradación):** si `assembled_context_tokens` > umbral **medido**, se emite
    `compaction_warning` + fallback; el siguiente turno usa el resumen almacenado, no recompacta.
- **Coste/factibilidad (Codex):** BAJA-MEDIA. **En scope 0106.**

---

## 3. Trazabilidad de fuentes (reclasificación de votos del ESTUDIO)

| arXiv | Pieza | Estado consolidado |
|-------|-------|--------------------|
| 2603.18718 (MemMA) | edición atómica (patrón) | ✅ **Verified 3-0** (patrón; descartar coord. 4-agentes) |
| 2502.12110 (A-Mem) | dynamic linking / consolidación post-sesión | ✅ **Verified 3-0** (patrón; timing offline ≠ hot path) |
| 2603.09619 (taxonomía memoria) | Working/Episodic/Semantic/Procedural | ✅ **Verified 3-0** (fundacional conceptual) |
| 2602.16284 (Attention Matching) | umbrales ">100k", "F1 <5%" | ⚠️ **Baja a "patrón confirmado / cifra NO atribuible"** (KV-cache, no aplica a CLI) |
| 2601.07190 (Focus) | "cada 10 tool calls", 22.7% | ⚠️ **Baja a "patrón confirmado / cifra NO atribuible"** (autónomo; heurística no es del paper) |
| 2604.01707 (Memory in LLM Era) | "sub-450 tokens" | ❓ **NO-VERIFICABLE** (2-1; guía, no ley) |
| 2603.10062 (Multi-Agent Memory) | "mayoría usa hybrid" | ❓ **NO-VERIFICABLE** (claim genérico) |
| 2606.00610 (MemGraphRAG) | "8x-49x", ontología 3-capas | ❓ **NO-VERIFICABLE / vago** (asume graph DB; rechazado) |

**Contradicción interna del ESTUDIO (a corregir):** §6.3 exige `measure_context_cost --baseline` ANTES de
TASK-0106, pero DELTA-1/2 fijan umbrales/cadencias como si vinieran de SOTA. La reformulación la resuelve: los
deltas describen el **mecanismo**; los **valores** salen de la medición.

---

## 4. Gate de medición (BLOQUEANTE)

- **Bloquear el freeze** de cualquier umbral/cadencia en SPEC/AC/golden hasta ejecutar
  `scripts/measure_context_cost` baseline (coherente con DECISION-0008 y con §6 del propio ESTUDIO, que ya
  prevé `baseline-2026-06-13.json`).
- **Ningún número no verificado entra a SPEC/AC/golden.** Los goldens aseveran comportamiento + umbral medido.

---

## 5. Alcance TASK-0106 = mínimo seguro (orden de implementación, voz Codex)

1. **Baseline de medición** del contexto ensamblado (`assembled_context_tokens` en `build_turn_context`) y del
   overhead del turno.
2. **Límites configurables** off-by-default / conservadores.
3. **Tool-result clearing** de resultados antiguos **preservando referencias en `runlog`** (auditable) +
   fallback explícito.
4. **Trigger determinista provisional** (N/T/tokens), consolidación **barata y fuera del hot path** (sin LLM en
   caliente).
5. **GC-8 / GC-9** con asertos estructurales + umbrales derivados de medición propia.

**Riesgos (voz Codex) y mitigaciones:**
- Pérdida de contexto útil por clearing agresivo → referencias auditables en `runlog` + fallback explícito.
- Coste oculto si la consolidación llama LLM en caliente → medir overhead; `<5%` como **gate**, no supuesto.
- Drift/doble-escritura si DELTA-3 se implementa fuera del runtime → exigir `submit_intent`.
- Specs/goldens frágiles si congelan números no medidos → `measure_context_cost` baseline antes del freeze.

---

## 6. Rechazos explícitos (neutralidad + single-writer)

- **Neo4j / Memgraph / graph DB** como prescripción (MemGraphRAG): tecnología pesada, acopla, rompe neutralidad.
- **LlamaIndex PropertyGraphIndex** como prescripción: ídem; backend agnóstico (SQLite default) si acaso, separado.
- **Servicio de memoria persistente externo** (Mem0/Letta) en el core: rompería single-writer; separable, off-by-default.
- **"Agente de fondo" de consolidación** (vago): sustituido por trigger determinista medido.

---

## 7. Próximos pasos (GATED — solo con GO del operador)

1. **Actualizar SPEC-0078** con los deltas corregidos: §2.1-bis (DELTA-1 reformulado, `assembled_context_tokens`),
   §2.2-bis (DELTA-2 reformulado, gate `<5%` medido + fuera del hot path), §2.5 (DELTA-4 justificado por medición),
   §2.6 (DELTA-3 Future Work + regla `submit_intent`), §6 (GC-8/GC-9 estructurales), traceability de fuentes
   reclasificada.
2. **Reemitir DECISION-0031 LIMPIA** con el esquema real del repo (`decision_id`, `status`, `date`,
   `ratified_at`, `deciders`, `supersedes`, `superseded_by`, `relates_to`, `phase`), ratificada por el operador,
   reservando bien el número (hoy el borrador vive en `artifacts/`, no en el ledger).
3. **Handoff a Codex para TASK-0106** (subconjunto mínimo seguro: medición + límites + tool-result clearing +
   trigger provisional + GC-8/GC-9), con el gate de medición como bloqueante previo al freeze.

---

*Consolidación de TASK-0109. Sin código, sin mutación de estado autoritativo. Reportado al operador antes de
tocar SPEC-0078 / DECISION-0031 / handoff.*
