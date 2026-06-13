---
decision_id: DECISION-0031
title: "Ajustes a SPEC-0078 basados en evaluación SOTA (junio 2026)"
status: proposed
date_created: 2026-06-13
date_updated: 2026-06-13
authored_by: Claude (arquitecto de análisis)
relates_to: [DECISION-0030, SPEC-0078, TASK-0106]
blocks: []
blocked_by: []
---

# DECISION-0031 - Ajustes a SPEC-0078 basados en evaluación SOTA (Junio 2026)

## Resumen Ejecutivo

**Se aprueba SPEC-0078 con 5 deltas concretos derivados de verificación SOTA (14 claims validados).** 

SPEC-0078 es sólida arquitectónicamente pero incompleta en especificación respecto a estado del arte actual. Se incorporan:
1. Umbrales de degradación para compaction >100k tokens
2. Trigger explícito para consolidación (volumen + temporal)
3. Reserva para edición atómica (futuro TASK-0107)
4. Revisión de límites de summary
5. Golden cases GC-8 y GC-9 adicionales

**Veredicto:** SPEC-0078 sigue off-by-default, neutral de dominio, single-writer. Implementation TASK-0106 procede con deltas integrados.

---

## Antecedentes y Justificación

### Contexto

SPEC-0078 propone compaction / tool-result clearing / sub-agentes para evitar context rot en sesiones del arquitecto multi-agente. La especificación fue completada el 2026-06-13 y está lista para TASK-0106 (implementación, Codex).

Antes de GO operacional, se realizó evaluación SOTA (junio 2026) comparando:
- 22 papers académicos + 8 herramientas (MemGPT/Letta, code-review-graph, Mem0, etc.)
- 5 ángulos de investigación (SOTA foundational, técnicas cuantificadas, produção implementations, sub-agent patterns, limitaciones)
- 109 claims extraídos, 25 verificados, 14 confirmados (3-0 vote), 11 refutados (0-3 vote)

**Resultado:** SPEC-0078 es accionable y alineada con SOTA, pero 5 gaps específicos identificados.

### Documento de Análisis

Reporte completo: [ESTUDIO-GESTION-CONTEXTO-ARQUITECTO-2026.md](../ESTUDIO-GESTION-CONTEXTO-ARQUITECTO-2026.md)

---

## Decisión y Deltas

### Core Decision

**Se aprueba SPEC-0078 con los 5 deltas siguientes integrados antes de TASK-0106 implementation.**

Deltas son refinamientos menores (no redesign). Preservan:
- ✅ Off-by-default (`runtime.context_policy.*` false)
- ✅ Neutral de dominio (sin términos de negocio)
- ✅ Single-writer (runtime = autoridad, DECISION-0022)
- ✅ Event-sourced (evidencia en runlog, DECISION-0017)

### Delta-1: Umbrales de Degradación (Sección 2.1-bis)

**Problema SOTA:** Attention Matching (ICML 2026, arXiv:2602.16284) reporta 50x-100x compaction en 5-8k tokens pero no cuantifica degradación >100k.

**Solución:** Agregar a SPEC-0078 sección 2.1-bis especificando:

```markdown
### 2.1-bis Umbrales de Degradación (Compaction)

Con `compaction_enabled`, el ensamblador garantiza:
- Contexto ≤ 100k tokens: Compaction 50x-100x, F1 degradation < 5%
- Contexto 100k-500k tokens: Compaction 20x-50x, F1 degradation < 15%
- Contexto > 500k tokens: Fallback a rolling summary manual

En sesiones > 500k tokens, flag `compaction_warning: true` en turn_report.
```

**Acceptance Criterion nuevo (AC7):**
- Con `compaction_enabled` y contexto ≤100k tokens, degradación F1 < 5% (GC-1 verifica esto)
- Con contexto > 500k, fallback a rolling summary y alerta emitida

**Referencia:** arXiv:2602.16284 (Attention Matching, ICML 2026)

### Delta-2: Trigger de Consolidación Explícito (Sección 2.2-bis)

**Problema SOTA:** Focus (arXiv:2601.07190, Jan 2026) logra 22.7% reducción con consolidación cada 10-15 tool calls, pero SPEC-0078 solo dice "rolling summary" sin trigger.

**Solución:** Agregar sección 2.2-bis especificando:

```markdown
### 2.2-bis Politica de Consolidación (Trigger)

Tool-result clearing ocurre según:
- Temporal: Cada `consolidation_interval_minutes` (default 30)
- Volumen: Cada `consolidation_tool_call_count` llamadas a tools (default 10)
  - Whichever comes first

Config default:
```json
"runtime": {
  "context_policy": {
    "consolidation_trigger": "min(time_based, volume_based)",
    "consolidation_interval_minutes": 30,
    "consolidation_tool_call_count": 10
  }
}
```

Consolidación actúa:
- Colapsa resumenes más antiguos que `recent_turn_summaries` (default 3)
- Sintetiza últimas N acciones en rolling_summary acotado
- Valida anti-drift: cambios resumidos reflejados en CLAIMS/TASK_INDEX
```

**Acceptance Criterion nuevo (AC8):**
- Con 12 tool calls y `consolidation_tool_call_count: 10`, consolidación dispara (GC-8 valida)
- Rolling summary persistido en runlog
- Siguiente turno no reinyecta resumenes viejos (solo rolling summary)

**Referencia:** arXiv:2601.07190 (Focus, Jan 2026)

### Delta-3: Primitivo de Edición Atómica (Sección 2.6, para TASK-0107)

**Problema SOTA:** MemMA (arXiv:2603.18718, Mar 2026) logra +4.82 F1 con edición atómica ADD/UPDATE/DELETE, pero SPEC-0078 no menciona operaciones estructuradas sobre memoria de protocolo.

**Solución:** Agregar sección 2.6 como **Future Work**, documentando que:

```markdown
### 2.6 Edición Atómica de Memoria de Protocolo (Futuro, TASK-0107)

Cuando delegación a sub-agentes sea common, el runtime podrá soportar:

```python
def protocol_state_edit(
    operation: "ADD" | "UPDATE" | "DELETE",
    entity_type: "claim" | "task" | "decision",
    entity_id: str,
    changes: dict
) -> edit_result
```

Operaciones respetan `drift_checker` y requieren justificación en turn_report.

Habilitación: `subagents_enabled=false` por defecto. GO explícito requerido.
```

**Status:** Documentado pero NO en scope TASK-0106. TASK-0107 (post-0106) lo implementa si sub-agentes complejos lo requieren.

**Referencia:** arXiv:2603.18718 (MemMA, Mar 2026)

### Delta-4: Revisión de Límites de Summary

**Problema SOTA:** SPEC-0078 default `task_close_summary_max_tokens: 2000` sin justificación. Memory in LLM Era (arXiv:2604.01707, Apr 2026) sugiere 450-1200 tokens SOTA.

**Solución:** Antes de AC6 pass (TASK-0106), arquitecto revisa y justifica:
- ¿2000 tokens es correcto o reducir a 1200?
- ¿Casos de uso que requieren 2000?
- Idem para `subagent_summary_max_tokens: 2000`

**Recomendación:** Default 1200 tokens; si sub-agentes complejos requieren 2000, documentar caso de uso explícitamente.

**Referencia:** arXiv:2604.01707 (Memory in LLM Era, Apr 2026)

### Delta-5: Golden Cases Adicionales (GC-8, GC-9)

**Problema SOTA:** SPEC-0078 GC-1..GC-7 no cubren consolidation trigger ni degradation thresholds.

**Solución:** Agregar a sección 6 test_plan:

```markdown
**GC-8 (Consolidation Trigger):** 
Dado un turno que ejecuta 12 tool calls, `consolidation_tool_call_count: 10` debe 
disparar consolidación del historial previo en un rolling_summary persistido. 
Asertos:
- Resumenes previos a rolling_summary salen del contexto del siguiente turno
- Rolling_summary se reinyecta como una entrada
- Validador drift-checker pasa (cambios en rolling_summary reflejados en CLAIMS)

**GC-9 (Degradation Threshold):** 
Contexto acumulado > 100k tokens con `compaction_enabled=true` genera 
`compaction_warning=true` y fallback a rolling summary manual. Asertos:
- Flag emitido en turn_report
- Siguiente turno NO aplica dynamic compaction
- Usa rolling summary almacenado
```

**Test harness:** `examples/context_policy_cases/run_tests.py --golden-case GC-8|GC-9`

---

## Matriz de Deltas vs TASK-0106 Scope

| Delta | Implementar en TASK-0106 | Scope | Complejidad | Prioridad |
|-------|--------------------------|-------|-------------|-----------|
| DELTA-1: Thresholds | ✅ SÍ | Sección 2.1-bis + AC7 | BAJA | **ALTA** |
| DELTA-2: Consolidation trigger | ✅ SÍ | Sección 2.2-bis + AC8 + config | MEDIA | **ALTA** |
| DELTA-3: Atomic edits | ⚠️ Documentar solo | Sección 2.6 (Future Work) | — | MEDIA |
| DELTA-4: Límites | ⚠️ Revisar antes AC6 | Sección 2.5 justificación | BAJA | MEDIA |
| DELTA-5: GC-8, GC-9 | ✅ SÍ | Sección 6 + run_tests.py | BAJA | **ALTA** |

**Timeline:** DELTA-1, 2, 5 en TASK-0106. DELTA-3 postergar a TASK-0107. DELTA-4 revisar antes de cierre.

---

## Implicaciones Arquitectónicas

### Compatibilidad Hacia Atrás

✅ **Preservada:** Con `context_policy.*` deshabilitados (default), comportamiento es idéntico a hoy.

### Neutralidad de Dominio

✅ **Preservada:** Deltas son técnicos, sin términos de negocio. `runtime.context_policy` es genérico.

### Single-Writer (DECISION-0022)

✅ **Preservada:** Consolidation y edición atómica respetan autoridad del runtime.

### Event-Sourced (DECISION-0017)

✅ **Preservada:** Evidencia (stdout, tool results) queda en runlog. Contexto del turno usa solo resumenes.

---

## Riesgos y Mitigaciones

| Riesgo | Probabilidad | Impacto | Mitigación |
|--------|-------------|--------|-----------|
| Consolidation trigger (10 tool calls) es agresivo | BAJA | MEDIA | Tuneable via config; medir latency post-0106 |
| Degradation threshold >100k es conservador | BAJA | BAJA | Baseline con Attention Matching (ICML 2026 verified) |
| Edición atómica (DELTA-3) no está en TASK-0106 | NO | NO | Documentada como Future Work, no bloqueador |
| Límites de summary mal calibrados | BAJA | MEDIA | Revisar Delta-4 antes de AC6 pass |

---

## Aprobación y Siguiente Paso

### GO para TASK-0106

Con esta decisión, TASK-0106 (Codex) tiene:
1. SPEC-0078 base + 5 deltas integrados
2. Aceptance criteria extendidos (AC7, AC8)
3. Golden cases completos (GC-1..GC-9)
4. Config tunable y documentado
5. Roadmap para TASK-0107 (edición atómica, futuro)

**Handoff:** Documento separado en `Area_comun/handoffs/HANDOFF-TASK-0106-deltassota.md`

### Cierre de DECISION-0031

- [ ] Operador revisa y aprueba (o solicita ajustes)
- [ ] SPEC-0078 actualizado con deltas (CLAUDE redacta)
- [ ] TASK-0106 reclasificado a `ready` (operador GO)
- [ ] DECISION-0031 reclasificado a `accepted`

---

## Referencias

**Fuentes SOTA verificadas (3-0 vote):**
1. arXiv:2602.16284 (Attention Matching, ICML 2026)
2. arXiv:2603.18718 (MemMA, Mar 2026)
3. arXiv:2601.07190 (Focus, Jan 2026)
4. arXiv:2606.00610 (MemGraphRAG, KDD 2026)
5. arXiv:2604.01707 (Memory in LLM Era, Apr 2026)

**Documento de análisis:**
- ESTUDIO-GESTION-CONTEXTO-ARQUITECTO-2026.md (full report)

---

## Preguntas Abiertas (para Arquitecto / Operador)

1. **Consolidation trigger cadencia:** ¿10 tool calls es correcto o ajustar?
2. **Límites de summary:** ¿Bajar a 1200 tokens (SOTA) o mantener 2000?
3. **Edición atómica (DELTA-3):** ¿Habilitar en TASK-0106 o postergar a TASK-0107?
4. **Rolling summary persistencia:** ¿En runlog, NOTES-<task>.md, o handoffs/?
5. **Roadmap futuro:** ¿Prioritizar TASK-0107 (edición atómica) o TASK-0108 (A-Mem dynamic linking)?

---

**DECISION-0031 propuesta por:** Claude (Arquitecto de Análisis)  
**Fecha:** 13 de junio de 2026  
**Status:** PROPOSED (en espera de operador GO)
