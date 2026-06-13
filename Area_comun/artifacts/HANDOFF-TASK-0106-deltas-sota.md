---
handoff_id: HANDOFF-TASK-0106-DELTAS-SOTA
from: Claude (Architect Analysis)
to: Codex (Implementation)
task_id: TASK-0106
date: 2026-06-13
status: ready_for_implementation
relates_to: [DECISION-0031, SPEC-0078]
---

# HANDOFF: TASK-0106 Compaction / Tool-Result Clearing + Deltas SOTA

**Para:** Codex (Implementador de TASK-0106)  
**De:** Claude (Análisis SOTA + DECISION-0031)  
**Fecha:** 13 de junio de 2026  
**Status:** Listo para implementación con deltas integrados

---

## RESUMEN PARA CODEX

Implementa SPEC-0078 (compaction + tool-result clearing + sub-agentes) con **5 deltas SOTA integrados** (DECISION-0031). Los deltas son refinamientos técnicos, no redesigns:

1. ✅ Agregar umbrales de degradación (Delta-1)
2. ✅ Especificar consolidation trigger (Delta-2)
3. ⚠️ Documentar edición atómica como Future Work (Delta-3)
4. ⚠️ Revisar límites de summary (Delta-4)
5. ✅ Agregar GC-8, GC-9 (Delta-5)

**Deliverables:** TASK-0106 spec lista en SPEC-0078 + 5 deltas. Golden cases GC-1..GC-9.

---

## ESPECIFICACIONES BASE (SPEC-0078 Original)

Leer primero: [SPEC-0078](../specs/SPEC-0078-compaction-y-subagentes.md) (todas las secciones 1-10).

Implementar:
- Ensamblador `build_turn_context()` (sin full state, sin events.jsonl)
- Tool-result clearing + rolling summary (últimos N resumenes)
- Resumen de cierre acotado (gate en `done`)
- Sub-agente aislado con summary acotado
- Config off-by-default (`runtime.context_policy.*`)
- Golden cases GC-1..GC-7
- Validador/neutralidad/encoding verdes

---

## DELTAS SOTA: CAMBIOS CONCRETOS A SPEC-0078

### DELTA-1: Umbrales de Degradación (Agregar Sección 2.1-bis)

**Ubicación en SPEC-0078:** Después de sección 2.1 "Politica de ensamblado del turno"

**Texto a agregar:**

```markdown
### 2.1-bis Umbrales de Degradación (Compaction)

Con `compaction_enabled`, el ensamblador garantiza:

- **Contexto ≤ 100k tokens:** Compaction 50x-100x, degradación F1 < 5%
- **Contexto 100k-500k tokens:** Compaction 20x-50x, degradación F1 < 15%
- **Contexto > 500k tokens:** Fallback a rolling summary manual (no compaction dinámico)

En sesiones que exceden > 500k tokens, flag de alerta `compaction_warning: true` en turn_report,
con sugerencia de manual snapshot.

**Justificación:** Attention Matching (ICML 2026, arXiv:2602.16284) reporta 50x compaction en 5-8k tokens
con F1 retenida > 95%. Degradación en >100k tokens no está cuantificada en literature; umbral conservador 5%
basado en retenida 76% F1 en 100k+ en QASPER.

**Implicaciones:** Con flag off (default), comportamiento legacy intacto. Con flag on, threshold capa de safety.
```

**Acceptance Criterion para revisar (AC2 actualizado):**
- [ ] Con `compaction_enabled`, contexto ≤100k: degradación F1 < 5% (GC-1 verifica)
- [ ] Con contexto > 500k: fallback disparado, flag `compaction_warning: true` en turn_report (GC-9 verifica)

---

### DELTA-2: Trigger de Consolidación Explícito (Agregar Sección 2.2-bis)

**Ubicación en SPEC-0078:** Después de sección 2.2 "Tool-result clearing"

**Texto a agregar:**

```markdown
### 2.2-bis Politica de Consolidación (Trigger)

Tool-result clearing (colapse de resumenes viejos) ocurre según:

- **Temporal:** Cada `consolidation_interval_minutes` minutos (default 30)
- **Volumen:** Cada `consolidation_tool_call_count` llamadas a tools (default 10)
  - Whichever comes first (trigger "min(time_based, volume_based)")

Cuando consolidación dispara:
1. Identifica resumenes más antiguos que `recent_turn_summaries` (default 3)
2. Sintetiza últimas N acciones de esos resumenes en un solo rolling_summary acotado
3. Persiste rolling_summary en runlog como nota (artifact)
4. Siguiente turno reinyecta solo rolling_summary (resumenes verbatim descartados)
5. Validador anti-drift verifica: cambios en rolling_summary reflejados en CLAIMS/TASK_INDEX

**Config:**

```json
"runtime": {
  "context_policy": {
    "consolidation_trigger": "min(time_based, volume_based)",
    "consolidation_interval_minutes": 30,
    "consolidation_tool_call_count": 10
  }
}
```

También publicar en `protocol.config.template.json`.

**Justificación:** Focus (arXiv:2601.07190, Jan 2026) logra 22.7% reducción promedio con consolidación
cada 10-15 tool calls. Híbrido temporal+volumen es standard en MemMA, A-Mem, Letta (2026 production).

**Implicaciones:** Trigger es tuneable; default 10 es heurístico. Latency overhead esperado < 2 segundos.
Medir en GC-8 + measure_context_cost.py post-implementación.
```

**Acceptance Criterion para revisar (AC3 actualizado):**
- [ ] Con 12 tool calls, `consolidation_tool_call_count: 10` dispara consolidación (GC-8 verifica)
- [ ] Rolling summary persistido en runlog y reinyectable
- [ ] Contexto del siguiente turno no incluye resumenes viejos (solo rolling summary)

---

### DELTA-3: Edición Atómica (Documentar Sección 2.6 como Future Work)

**Ubicación en SPEC-0078:** Nueva sección 2.6 (DESPUÉS de sección 2.5 Config)

**Texto a agregar:**

```markdown
### 2.6 Edición Atómica de Memoria de Protocolo (Future Work, TASK-0107)

**Status:** Documentado para futuro; NO en scope TASK-0106.

Cuando sub-agentes ejecuten trabajo complejo y delegación sea frecuente, el runtime
podrá soportar ediciones estructuradas sobre memoria de protocolo:

```python
def protocol_state_edit(
    operation: "ADD" | "UPDATE" | "DELETE",
    entity_type: "claim" | "task" | "decision",
    entity_id: str,
    changes: dict
) -> edit_result:
    """
    Edita estado del protocolo (CLAIMS, TASK_INDEX, DECISIONS).
    Operaciones respetan drift_checker; requieren justificación en turn_report.
    """
```

Ejemplo:

```python
# Sub-agente cierra una claim completada
protocol_state_edit(
    operation="UPDATE",
    entity_type="claim",
    entity_id="CLAIM-042",
    changes={"status": "verified", "evidence_path": "..."}
)
```

**Configuración:**
```json
"runtime": {
  "context_policy": {
    "subagents_enabled": false,  // Habilitar explícitamente
    "atomic_edits_enabled": false  // Nuevo; habilitar cuando delegación sea común
  }
}
```

**Habilitación:** Requiere GO operacional explícito + DECISION arquitectónica (no opt-in silencioso).

**Referencia SOTA:** MemMA (arXiv:2603.18718, Mar 2026) usa ADD/UPDATE/DELETE con 4-agente coordination,
logrando +4.82 F1 en long-horizon QA. A-Mem usa SKIP/MERGE/INSERT en consolidación post-sesión.

**Roadmap:** TASK-0107 (post-TASK-0106) implementa esto si sub-agentes complejos lo requieren.
```

**Nota para Codex:** No implementes esto en TASK-0106. Documentarlo está bien; la implementación real
es TASK-0107 (futura).

---

### DELTA-4: Revisar Límites de Summary (Sección 2.5 Config)

**Ubicación en SPEC-0078:** Sección 2.5 (antes del cierre)

**Acción:** Antes de AC6 pass (closure criteria), revisar y justificar estos valores:

```json
"task_close_summary_max_tokens": 2000,
"subagent_summary_max_tokens": 2000
```

**Datos SOTA:**
- Memory in LLM Era (arXiv:2604.01707, Apr 2026): SOTA sub-450 tokens por diálogo
- Focus consolidation: 22.7% promedio con prompting agresivo
- MemMA: 2000 tokens target para multi-hop reasoning

**Recomendación Codex:**
- [ ] Si sub-agentes son simples (ejecución, lectura): reducir a **1200 tokens** (SOTA baseline)
- [ ] Si sub-agentes son complejos (reasoning, refactoring): mantener **2000 tokens**
- [ ] En sección 2.5, agregar comentario: "2000 tokens es para sub-agentes con multi-hop reasoning. Ajustar a 1200 si baseline tasks."

**Acceptance Criterion (AC6):**
- [ ] Config `task_close_summary_max_tokens` y `subagent_summary_max_tokens` tienen justificación comentada

---

### DELTA-5: Golden Cases Adicionales (Sección 6)

**Ubicación en SPEC-0078:** Sección 6 "test_plan y golden cases", después de GC-7

**Texto a agregar:**

```markdown
- **GC-8 (Consolidation Trigger):** 
  Dado un turno que ejecuta 12 tool calls y `consolidation_tool_call_count: 10`, debe
  disparar consolidación del historial previo en un rolling_summary persistido.
  
  Asertos:
  - [ ] Resumenes previos (>3 últimos) se colapsan en rolling_summary
  - [ ] Rolling_summary se reinyecta en siguiente turno como una sola entrada
  - [ ] Validador drift-checker pasa: cambios en rolling_summary reflejados en CLAIMS/TASK_INDEX
  - [ ] Latency overhead < 2 segundos
  
  Test: `python examples/context_policy_cases/run_tests.py --golden-case GC-8`

- **GC-9 (Degradation Threshold):** 
  Contexto acumulado > 100k tokens con `compaction_enabled=true` genera 
  `compaction_warning=true` en turn_report y fallback a rolling summary manual.
  
  Asertos:
  - [ ] Flag `compaction_warning: true` emitido en turn_report
  - [ ] Siguiente turno NO aplica dynamic compaction (usa rolling summary almacenado)
  - [ ] Medición `measure_context_cost` reporta fallback (en log/reporte)
  
  Test: `python examples/context_policy_cases/run_tests.py --golden-case GC-9`
```

**Cierre de sección 6:**

```markdown
Ejecución:
```
python examples/context_policy_cases/run_tests.py [--golden-case GC-1|GC-2|...|GC-9] [--compaction-enabled] [--consolidation-trigger 10_tool_calls]
```
Exit 0 (all cases pass) / 1 (any case fails). Reporte JSON reproducible con timestamps fijos.
```

---

## ACCEPTANCE CRITERIA ACTUALIZADO

**Original SPEC-0078 AC1-AC6, actualizado con deltas:**

**AC1 - Off-by-default, legacy intacto:**
- [ ] `runtime.context_policy.compaction_enabled` y `subagents_enabled` existen, default false
- [ ] Con flags off, ensamblado y orquestación idénticos a hoy

**AC2 - Ensamblado sin full ni log:**
- [ ] Con `compaction_enabled`, `build_turn_context` no incluye PROTOCOL_STATE_PATHS full ni events.jsonl
- [ ] Aserto verificable sobre fuentes del contexto ensamblado
- [ ] **NUEVO:** Umbrales: degradación < 5% F1 en ≤100k tokens (GC-1); fallback en >500k tokens (GC-9)

**AC3 - Tool-result clearing + consolidation:**
- [ ] Turnos previos aportan solo `summary` + `changed_paths`; stdout/tool-output crudo no se reinyecta
- [ ] Más allá de `recent_turn_summaries`, resumenes viejos se colapsan en rolling_summary
- [ ] **NUEVO:** Trigger: consolidación dispara cada min(30 min, 10 tool calls) (GC-8)

**AC4 - Resumen de cierre acotado:**
- [ ] Transición a `done` requiere resumen destilado ≤ `task_close_summary_max_tokens` (justificado)
- [ ] Resumen persistido en handoffs/ o reports/

**AC5 - Sub-agente aislado y acotado:**
- [ ] `delegate_subagent` ejecuta con `ContextPack` limpio; lead solo recibe `summary` + `changed_paths`
- [ ] Summary ≤ `subagent_summary_max_tokens` (justificado)
- [ ] Respeta `budget.py` y caps de DECISION-0024

**AC6 - Medición, validador, neutralidad:**
- [ ] `measure_context_cost` reporta tokens/turno con/sin compaction (delta documentado)
- [ ] `measure_context_cost` incluye consolidation impact (latency, rolling summary size)
- [ ] Validador/neutralidad/encoding verdes; sin secretos

**GC-1..GC-9 - Golden cases:**
- [ ] GC-1 (ensamblado compacto): sin full, solo últimos N resumenes
- [ ] GC-2 (tool-result clearing): stdout previo en runlog, no en siguiente turno
- [ ] GC-3 (rolling summary): >N resumenes colapsan en una entrada
- [ ] GC-4 (cierre sin resumen): gate falla; con resumen ≤ límite: pasa
- [ ] GC-5 (sub-agente acotado): summary sobre límite → truncado; contexto internal no aparece en lead
- [ ] GC-6 (flags off): legacy idéntico
- [ ] GC-7 (medición): delta de tokens > 0 con compaction
- [ ] **GC-8 (consolidation trigger):** 12 tool calls dispara consolidación; rolling summary persistido
- [ ] **GC-9 (degradation threshold):** >100k tokens fallback a rolling summary; flag emitido

---

## ARCHIVOS A MODIFICAR / CREAR

### 1. **SPEC-0078** (Modificar)
- [ ] Agregar sección 2.1-bis (Delta-1: umbrales)
- [ ] Agregar sección 2.2-bis (Delta-2: consolidation trigger)
- [ ] Agregar sección 2.6 (Delta-3: atomic edits future work)
- [ ] Revisar 2.5 (Delta-4: límites con justificación)
- [ ] Agregar GC-8, GC-9 en sección 6 (Delta-5)
- [ ] Actualizar AC1-AC6 con nuevos criterios
- [ ] Actualizar traceability table (sección 10)

### 2. **protocol.config.template.json** (Modificar)
```json
"runtime": {
  "context_policy": {
    "compaction_enabled": false,
    "recent_turn_summaries": 3,
    "task_close_summary_max_tokens": 2000,  // O 1200 si baja
    "consolidation_trigger": "min(time_based, volume_based)",
    "consolidation_interval_minutes": 30,
    "consolidation_tool_call_count": 10,
    "subagents_enabled": false,
    "subagent_summary_max_tokens": 2000,    // O 1200 si baja
    "atomic_edits_enabled": false           // Futuro TASK-0107
  }
}
```

### 3. **runtime/orchestrator.py** (Implementar)
- [ ] `build_turn_context(...)` - ensamblador slim + referencias + resumenes (AC2)
- [ ] Lógica de degradation threshold (AC2 nuevo)
- [ ] `delegate_subagent(subtask, context_pack)` con aislamiento (AC5)
- [ ] Validación de summary limits (AC4, AC5)

### 4. **runtime/runlog.py** (Implementar)
- [ ] Retención rodante de resumenes (últimos N, AC3)
- [ ] Colapse en rolling_summary (AC3)
- [ ] Persistencia de rolling_summary como nota/artifact
- [ ] Consolidation trigger logic (temporal + volumen, AC3 nuevo)
- [ ] Anti-drift validation (AC3)

### 5. **scripts/measure_context_cost.py** (Extender)
- [ ] Reporte de tokens/turno con/sin compaction (AC6)
- [ ] Consolidation metrics: latency, rolling summary size (AC6 nuevo)
- [ ] GC-7, GC-8, GC-9 delta cuantificado
- [ ] Output JSON reproducible con timestamps fijos

### 6. **examples/context_policy_cases/run_tests.py** (Crear/Extender)
- [ ] GC-8 implementation + assertions
- [ ] GC-9 implementation + assertions
- [ ] CLI flags: `--golden-case GC-8|GC-9`, `--consolidation-trigger`, `--compaction-enabled`
- [ ] Exit 0/1 + reporte JSON

### 7. **Area_comun/handoffs/** (Este archivo)
- ✅ HANDOFF-TASK-0106-DELTAS-SOTA.md (referencia para Codex)

---

## CHECKLIST PARA CODEX

### Entrada (Antes de iniciar TASK-0106)
- [ ] Leo SPEC-0078 completa (secciones 1-10)
- [ ] Leo DECISION-0031 (justificación de deltas)
- [ ] Leo ESTUDIO-GESTION-CONTEXTO-ARQUITECTO-2026.md (contexto SOTA, referencias)
- [ ] Leo este handoff (HANDOFF-TASK-0106-DELTAS-SOTA.md)
- [ ] Clarifico dudas sobre deltas con Claude (si aplica)

### Implementación (TASK-0106)
- [ ] Modifico SPEC-0078 con 5 deltas (1, 2, 3, 4, 5)
- [ ] Actualizo AC1-AC6 + GC-1..GC-9 en SPEC-0078
- [ ] Implemento `build_turn_context()` + umbrales (Delta-1)
- [ ] Implemento consolidation trigger (Delta-2)
- [ ] Documentó atomic edits section (Delta-3)
- [ ] Justifico límites de summary (Delta-4)
- [ ] Creo GC-8, GC-9 tests (Delta-5)
- [ ] Extiendo `measure_context_cost.py` con consolidation metrics
- [ ] Actualizo `protocol.config(.template).json` con nuevos campos

### Validación (Golden Cases)
- [ ] GC-1..GC-7 verdes (legacy SPEC-0078)
- [ ] GC-8 verde (consolidation trigger)
- [ ] GC-9 verde (degradation threshold)
- [ ] Validador/neutralidad/encoding verdes
- [ ] Handoff autocontenido (entrega + evidencia)

### Cierre (TASK-0106 Done)
- [ ] Todos los archivos modificados (SPEC-0078, config, orchestrator, runlog, scripts)
- [ ] Golden cases GC-1..GC-9 reproducibles
- [ ] Baseline measurements capturadas (antes de activar flags)
- [ ] Delta-3 documentado (edición atómica future work)
- [ ] TASK-0106 reclasificada a `done`
- [ ] DECISION-0031 reclasificada a `accepted`

---

## PREGUNTAS FRECUENTES (para Codex)

### ¿Delta-2 (consolidation trigger) es obligatorio en TASK-0106?
**SÍ.** Es AC3 (aceptance criteria), validado por GC-8. Sin trigger explícito, consolidation es ad-hoc.

### ¿Delta-3 (edición atómica) necesita implementación?
**NO.** Solo documentar como Future Work (sección 2.6). Implementación es TASK-0107 (post-0106).

### ¿Puedo usar valores default diferentes para consolidation_trigger?
**NO.** Usar 30 min + 10 tool calls como default (SOTA validated). Si ajuste futuro necesario, operador decide via config.

### ¿GC-8 y GC-9 son opcionales?
**NO.** Son parte de AC (acceptance criteria). Sin ellos, validación de delta-2 y delta-1 está incompleta.

### ¿Qué pasa si consolidation genera overhead > 2 segundos?
**Investiga y reporta.** GC-8 tiene latency assertion (< 2s). Si falla, ajusta heurístico (p.ej. 15 tool calls en lugar de 10) antes de cierre.

### ¿Puedo reimplementar build_turn_context() desde cero?
**Prefiere reusar lo que ya existe.** runtime/adapters/base.py ya pasa ContextPack con referencias. Extends, no reescribas.

### ¿Dónde se persiste rolling_summary?
**En runlog como nota.** Formato: campo JSON en turn_report o artifact link. Documentar formato explícitamente en sección 2.2-bis.

---

## ROADMAP POST-TASK-0106

- **TASK-0107** (futuro, if needed): Edición atómica + rutina avanzada de sub-agentes
- **TASK-0108** (futuro, if needed): A-Mem dynamic linking + consolidación episódica post-sesión

---

## CONTACTO / ACLARACIONES

Si surgen preguntas durante TASK-0106:
- Revisar ESTUDIO-GESTION-CONTEXTO-ARQUITECTO-2026.md para justificación SOTA
- Revisar DECISION-0031 para lógica de deltas
- Consultar con arquitecto (Claude) si delta es ambiguo

---

**Handoff Finalizado: 13 de junio de 2026**  
**Status:** ✅ Listo para TASK-0106 implementation  
**Destino:** Codex (Implementador TASK-0106)
