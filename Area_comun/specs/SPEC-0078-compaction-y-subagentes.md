---
spec_id: SPEC-0078
title: "Compaction / tool-result clearing y sub-agentes en el turno del runtime (DECISION-0030 piezas 4-5)"
status: accepted
date_created: 2026-06-13
date_updated: 2026-06-13
authored_by: Claude (architect)
task_id: TASK-0106
related_decisions: [DECISION-0031, DECISION-0030, DECISION-0009, DECISION-0024, DECISION-0022, DECISION-0017, DECISION-0008]
---

# SPEC-0078 - Compaction / tool-result clearing y sub-agentes

> **Deltas SOTA integrados (DECISION-0031, revision adversarial TASK-0109).** Esta version incorpora los
> 5 deltas corregidos tras la revision de 3 voces (operador/analista/codex). Cambios clave: el umbral de
> degradacion (DELTA-1) se mide como `assembled_context_tokens` en `build_turn_context`, NO como KV-cache;
> el trigger (DELTA-2) es determinista con cadencia provisional y `overhead <5%` como GATE MEDIDO; la
> edicion atomica (DELTA-3) queda FUERA de 0106 (Future Work TASK-0107, solo via `submit_intent`); los
> limites de summary (DELTA-4) se deciden por medicion propia, no por cita. **GATE DE MEDICION BLOQUEANTE:
> ningun umbral/cadencia de DELTA-1/2/4 se congela en AC/golden sin correr `measure_context_cost` baseline
> antes (DECISION-0008).** Trazabilidad de fuentes en la seccion 11.

**Resumen ejecutivo:** Formalizar la politica de ensamblado del contexto por turno del runtime para que
(a) nunca incluya estado full ni event log crudo, (b) descarte resultados crudos de lecturas/tools de
turnos previos conservando solo su resumen destilado (compaction / tool-result clearing), y (c) habilite
un primitivo de **delegacion a sub-agente** con `ContextPack` limpio que devuelve solo un resumen acotado
(1-2k tokens). Todo aditivo y off-by-default (`runtime.context_policy.*`), medible con
`measure_context_cost`, y como evolucion del loop M1/M2 (DECISION-0009/0024). Construye sobre SPEC-0077
(slim-views).

---

## 1. Contexto y justificacion

Ver DECISION-0030 (piezas 4 y 5). El runtime ya ejecuta turnos **single-shot** (`runtime/llm_turn_wrapper.py`
invoca `claude -p` / `codex exec` no interactivo y normaliza una `turn_report`), y el `ContextPack`
(`runtime/adapters/base.py`) ya pasa **referencias** (`spec_paths`, `decision_ids`, `replay_report_path`),
no volcados de estado. Lo que falta es una **politica explicita** que:

- garantice que el contexto del turno se arma desde slim-views (SPEC-0077) + referencias, nunca desde los
  archivos full ni `runtime/state/events.jsonl`;
- al encadenar turnos de una misma tarea, aporte solo el **resumen destilado** de turnos previos
  (`turn_report.summary` + `changed_paths`), descartando stdout/lecturas/tool-output crudos;
- permita **aislar** trabajo profundo en un sub-agente con ventana limpia que devuelve un resumen acotado.

Sin esto, a medida que una tarea acumula turnos, el contexto reincorpora salida cruda y vuelve a crecer
(context rot), anulando la ganancia de las slim-views.

---

## 2. Diseno tecnico

### 2.1 Politica de ensamblado del turno (compaction)

Definir un ensamblador de contexto determinista (en `runtime/orchestrator.py`, helper nuevo
`build_turn_context(...)`), cuya entrada al adaptador sea exactamente:

1. Cold-start slim (SPEC-0077): `*.slim.json` + `AGENTS.md` + `README` + `TASK_PROTOCOL.md`.
2. `ContextPack` de la unidad/tarea: `spec_paths`, `decision_ids`, `task` (campos minimos), `turn_index`.
3. **Resumenes destilados** de los ultimos `recent_turn_summaries` turnos de la MISMA tarea (de `runlog`),
   no su salida cruda.

Prohibido en el contexto del turno: archivos full (`PROTOCOL_STATE_PATHS`), `events.jsonl`, stdout crudo
de tools/lecturas de turnos previos, y handoffs completos viejos (se referencian, se leen on-demand).

Flag: `runtime.context_policy.compaction_enabled` (default false). Con flag off, el comportamiento actual
queda intacto.

### 2.1-bis Umbral de degradacion (DELTA-1, reformulado)

**Procedencia corregida (DECISION-0031):** este umbral NO deriva de compactacion de KV-cache
(arXiv:2602.16284 es atencion en espacio latente del backend, que el runtime CLI no controla). El runtime
solo arma contexto plano para stdin del CLI; el punto de control real esta ANTES de la llamada.

- **Mecanismo:** `build_turn_context(...)` instrumenta `assembled_context_tokens` (tokens del contexto
  ensamblado del turno, via `measure_context_cost`/proxy). Si supera un umbral configurable, emite
  `compaction_warning: true` en la `turn_report` y aplica fallback (rolling summary del 2.2).
- **Valores por medicion, no por cita (GATE BLOQUEANTE, DECISION-0008):** los cortes concretos del umbral
  se derivan de un baseline propio (`measure_context_cost --baseline`) corrido ANTES de congelarlos. No se
  graban numeros heredados de papers (p.ej. ">100k", "F1 <5%").
- **Config:** `context_policy.assembled_context_warn_tokens` (default `null` = sin umbral hasta medir).

### 2.2 Tool-result clearing (retencion rodante)

- Cada `turn_report` ya contiene `summary` y `changed_paths` (ver `REQUIRED_REPORT_KEYS` en
  `llm_turn_wrapper.py`). Esos son la **unidad de compaction**: lo que se reinyecta de un turno previo.
- Retencion: mantener verbatim los ultimos `recent_turn_summaries` (config) resumenes; los mas viejos se
  colapsan en un **rolling summary** persistido como nota (`Area_comun/artifacts/NOTES-<task>.md` o campo
  en `runlog`), reinyectable como una sola entrada.
- El stdout/tool-output crudo nunca se reinyecta: queda en el `runlog`/evidencia, recuperable on-demand,
  no en el contexto del siguiente turno (analogo a tool-result clearing del Developer Platform).

### 2.2-bis Trigger de consolidacion (DELTA-2, reformulado)

**Procedencia corregida (DECISION-0031):** la cadencia NO proviene de Focus (arXiv:2601.07190 es un
mecanismo agente-autonomo; no especifica "cada 10-15 tool calls" ni el 22.7% se deriva de esa cadencia).
El trigger es **determinista del runtime** (correcto para single-writer), definido por nosotros.

- **Disparo:** la consolidacion (colapso a rolling summary del 2.2) se dispara por el primero de: N
  tool-results, T minutos, o tokens acumulados desde la ultima consolidacion. Encaja en
  `orchestrator`/`runlog`.
- **Cadencia provisional/tuneable:** `consolidation_tool_call_count` (p.ej. `10`) es **valor inicial
  provisional**, NO baseline SOTA; se ajusta tras medicion.
- **`overhead <5%` = GATE MEDIDO, no supuesto:** el overhead (tiempo de construccion + consolidacion frente
  al wall-time del turno, y delta de tokens enviados) se MIDE contra el baseline propio. El objetivo `<5%`
  es un gate verificado, no una suposicion.
- **Consolidacion barata y FUERA del hot path (refinamiento de la voz Codex):** la consolidacion NO debe
  invocar un LLM en caliente dentro del turno; si lo hiciera, el coste puede superar el margen del 5%.
  Preferir colapso estructural barato (truncado/seleccion de `summary`+`changed_paths`); cualquier resumen
  por LLM va fuera del hot path.
- **Config:** `consolidation_trigger` (`min(time, volume, tokens)`), `consolidation_interval_minutes`,
  `consolidation_tool_call_count`, `consolidation_overhead_budget_pct` (default `5`).

### 2.3 Resumen destilado al cierre de tarea (note-taking)

- En la transicion de una tarea a `done`, el runtime exige/produce un **resumen destilado acotado**
  (<= `task_close_summary_max_tokens`, p.ej. 1-2k) persistido en `handoffs/` o `reports/`. Converge con la
  regla 7 de CLAUDE.md (reporte humano de cierre) y con el note-taking de DECISION-0030.
- Ese resumen es lo unico que turnos/tareas posteriores reinyectan sobre la tarea cerrada.

### 2.4 Primitivo de delegacion a sub-agente

- Anadir al orquestador una operacion `delegate_subagent(subtask, context_pack)` que ejecuta un turno con
  un `ContextPack` **limpio** (solo la subtarea + referencias), aislado del contexto del lead.
- El sub-agente devuelve una `turn_report` cuyo `summary` esta **acotado** (`subagent_summary_max_tokens`,
  ~1-2k); el lead reincorpora solo ese summary + `changed_paths`, nunca el contexto interno del sub-agente.
- Limites por presupuesto reutilizando `runtime/budget.py` (`Budget.max_cost_tokens` / `soft`/`hard`).
- Encaje con autonomia supervisada (DECISION-0024): la delegacion respeta `caps` (`max_turns`,
  `human_checkpoint_every_k`, `wall_clock_ms`). Off-by-default; activacion opt-in como el patron M2.

### 2.5 Config (nuevo bloque, off-by-default)

```json
"runtime": {
  "context_policy": {
    "compaction_enabled": false,
    "recent_turn_summaries": 3,
    "task_close_summary_max_tokens": 2000,
    "subagents_enabled": false,
    "subagent_summary_max_tokens": 2000,
    "assembled_context_warn_tokens": null,
    "consolidation_trigger": "min(time, volume, tokens)",
    "consolidation_interval_minutes": 30,
    "consolidation_tool_call_count": 10,
    "consolidation_overhead_budget_pct": 5
  }
}
```
Se publica tambien en `protocol.config.template.json`. Neutral de dominio.

**DELTA-4 (limites de summary, reformulado, DECISION-0031):** `task_close_summary_max_tokens` y
`subagent_summary_max_tokens` se mantienen en `2000` como valor **provisional conservador**, NO se bajan a
1200 por cita (arXiv:2604.01707 es no-verificable; el rango 450-1200 es guia, no ley). El valor definitivo
se **decide por medicion propia** del tamano real de resumenes (`measure_context_cost`) y se **justifica
aqui** antes del cierre de TASK-0106. 2000 conservador es defendible si la medicion no muestra ganancia
clara al reducir.

### 2.6 Edicion atomica de memoria de protocolo (DELTA-3, Future Work, TASK-0107)

**FUERA del alcance de TASK-0106.** Patron confirmado (arXiv:2603.18718 MemMA: ops ADD/UPDATE/DELETE; se
adopta el patron, NO la coordinacion multi-agente de 4 roles del paper). Cuando la delegacion a
sub-agentes lo requiera, el runtime podra soportar operaciones estructuradas sobre el estado de protocolo:

```text
protocol_state_edit(operation: ADD|UPDATE|DELETE, entity_type: claim|task|decision, entity_id, changes)
```

**Regla innegociable (operador, DECISION-0031):** si algun dia entra, **EXCLUSIVAMENTE via
`submit_intent`** (transaccion con rollback/idempotencia/drift-gate; respeta DECISION-0022). NUNCA edicion
directa de `CLAIMS/TASK_INDEX/PROJECT_STATE` — editar estado fuera del flujo es justo lo que causo el drift
que el arquitecto reparo con re-genesis. Habilitacion: `subagents_enabled=false` + GO explicito.
Implementacion = **TASK-0107** (post-0106).

---

## 3. Out of scope

- Slim-views y politica de `coldstart_globs`: cubiertas por SPEC-0077.
- Rotacion/segmentado de `events.jsonl`: item separado.
- Cambios al modelo single-writer / al replay del estado (sin cambios de semantica de estado).
- Eleccion de proveedor LLM: el wrapper sigue vendor-neutral (DECISION-0021).

---

## 4. execution_pipeline

1. Anadir bloque `runtime.context_policy` (off-by-default) a `protocol.config(.template).json`.
2. Implementar `build_turn_context(...)` en `orchestrator.py` (ensamblado slim + referencias + resumenes).
3. Implementar retencion rodante de resumenes + rolling summary en `runlog`.
4. Exigir/producir resumen destilado al cierre de tarea (gate en la transicion a `done`).
5. Implementar `delegate_subagent(...)` con `ContextPack` limpio + acotado por `budget.py` + caps de
   DECISION-0024.
6. Extender `measure_context_cost` para reportar tokens de contexto por turno (con/sin compaction).
7. Golden cases (seccion 6).

---

## 5. acceptance_criteria

**AC1 - Off-by-default, legacy intacto:**
- [ ] `runtime.context_policy.compaction_enabled` y `subagents_enabled` existen, default false.
- [ ] Con flags off, el ensamblado del turno y la orquestacion no cambian.

**AC2 - Ensamblado sin estado full ni log:**
- [ ] Con `compaction_enabled`, `build_turn_context` no incluye `PROTOCOL_STATE_PATHS` full ni
      `events.jsonl`; usa slim-views (SPEC-0077) + referencias.
- [ ] Aserto verificable sobre el contexto ensamblado (lista de fuentes).

**AC3 - Tool-result clearing:**
- [ ] Turnos previos aportan solo `summary` + `changed_paths`; stdout/tool-output crudo no se reinyecta.
- [ ] Mas alla de `recent_turn_summaries`, los resumenes viejos se colapsan en un rolling summary.

**AC4 - Resumen de cierre acotado:**
- [ ] Al pasar una tarea a `done`, existe un resumen destilado <= `task_close_summary_max_tokens`
      persistido en `handoffs/` o `reports/`.

**AC5 - Sub-agente aislado y acotado:**
- [ ] `delegate_subagent` ejecuta con `ContextPack` limpio; el lead solo recibe el `summary`
      (<= `subagent_summary_max_tokens`) + `changed_paths`.
- [ ] Respeta `budget.py` y los `caps` de DECISION-0024.

**AC6 - Medicion, validador, neutralidad:**
- [ ] `measure_context_cost` reporta tokens de contexto por turno con/sin compaction (delta documentado).
- [ ] Validador/neutralidad/encoding verdes; sin secretos.

**AC7 - Umbral de degradacion medido (DELTA-1):**
- [ ] `build_turn_context` instrumenta `assembled_context_tokens`; si supera
      `assembled_context_warn_tokens`, emite `compaction_warning: true` + fallback a rolling summary.
- [ ] El umbral proviene de `measure_context_cost` baseline propio (no de cita); con el config en `null`,
      no hay umbral hasta medir. GC-9 verifica con un umbral fijado en el caso, no heredado de un paper.

**AC8 - Trigger de consolidacion determinista (DELTA-2):**
- [ ] La consolidacion se dispara por `min(N tool-results, T min, tokens)`; `consolidation_tool_call_count`
      es cadencia inicial **provisional** ajustable tras medicion.
- [ ] Overhead de consolidacion medido contra baseline; objetivo `<5%` como **gate** (no supuesto). La
      consolidacion no invoca un LLM en el hot path del turno (colapso estructural barato).

---

## 6. test_plan y golden cases

Directorio: `examples/context_policy_cases/` (deterministas, sin red, timestamps fijos).

- **GC-1 (ensamblado compacto):** dado un estado + 5 turnos previos, `build_turn_context` produce un
  contexto que (a) no contiene rutas full ni `events.jsonl`, (b) incluye solo los ultimos
  `recent_turn_summaries` resumenes. Asercion sobre la lista de fuentes.
- **GC-2 (tool-result clearing):** turno previo con stdout crudo grande -> el contexto del siguiente turno
  solo trae su `summary`+`changed_paths`; el crudo sigue en runlog/evidencia.
- **GC-3 (rolling summary):** con > `recent_turn_summaries` turnos, los viejos se colapsan en una sola
  entrada de rolling summary.
- **GC-4 (cierre de tarea):** transicion a `done` sin resumen destilado -> gate falla; con resumen
  <= limite -> pasa.
- **GC-5 (sub-agente acotado):** `delegate_subagent` con summary que excede el limite -> truncado/rechazado
  segun politica; el contexto interno del sub-agente no aparece en el contexto del lead.
- **GC-6 (flags off):** con `compaction_enabled=false` y `subagents_enabled=false`, comportamiento legacy
  identico (sin cambios de contexto ni de orquestacion).
- **GC-7 (medicion):** `measure_context_cost` reporta delta de tokens por turno con/sin compaction (> 0).
- **GC-8 (trigger de consolidacion, DELTA-2):** dado un turno que ejecuta > `consolidation_tool_call_count`
  tool-results, la consolidacion dispara: los resumenes previos al rolling summary salen del contexto del
  siguiente turno; el `runlog` conserva referencia recuperable; el drift-checker pasa. **Asertos
  ESTRUCTURALES** (presencia/ausencia de fuentes, referencia en runlog), NO sobre F1 ni cifras de papers.
- **GC-9 (umbral de degradacion, DELTA-1):** con `assembled_context_warn_tokens` fijado **en el caso** (no
  heredado) y `assembled_context_tokens > umbral`, se emite `compaction_warning: true` + fallback; el
  siguiente turno usa el resumen almacenado y no recompacta. Aserto sobre el flag y la lista de fuentes,
  con el umbral **del caso/medicion**, no de cita.

> **Gate de medicion (DELTA-1/2/4):** los valores de umbral/cadencia usados en AC7/AC8/GC-8/GC-9 y en la
> decision de DELTA-4 provienen del baseline `measure_context_cost` corrido ANTES del freeze; los golden
> cases fijan el umbral localmente y aseveran comportamiento, nunca numeros atribuidos a SOTA.

Ejecucion: `python examples/context_policy_cases/run_tests.py [--golden-case GC-1|...]`, exit 0/1, reporte
JSON reproducible.

---

## 7. closure_criteria

- Politica de ensamblado, tool-result clearing, resumen de cierre y delegacion a sub-agente implementados
  off-by-default; GC-1..GC-7 verdes.
- Medicion del contexto por turno con/sin compaction adjunta.
- Validador/neutralidad/encoding verdes; handoff autocontenido.
- TASK-0106 cierra en `done`.

## 8. Risks

- **Sobre-compactacion:** perder contexto sutil necesario despues (DECISION-0030/Anthropic). Mitigacion:
  empezar maximizando recall (`recent_turn_summaries` generoso) y ajustar con medicion; el crudo queda
  recuperable on-demand.
- **Aislamiento de sub-agente mal calibrado:** el lead pierde senal util. Mitigacion: el summary debe
  cubrir decisiones/cambios; medir tasa de re-consulta.
- **Interaccion con autonomia supervisada (DECISION-0024):** la delegacion debe respetar caps y
  checkpoints humanos; no habilitar `subagents_enabled` sin GO del operador.

## 9. linked_decisions

- `DECISION-0030`: piezas 4 (compaction/tool-result clearing) y 5 (sub-agentes).
- `DECISION-0009`: loop de orquestacion del runtime (M1/M2) donde encaja el ensamblado y la delegacion.
- `DECISION-0024`: autonomia supervisada; los sub-agentes respetan sus caps/checkpoints.
- `DECISION-0017` / `DECISION-0022`: event log y escritor unico (la salida cruda queda en evidencia, no en
  contexto).

## 10. Traceability

| Requirement | Task | Test | Closure criterion |
|-------------|------|------|-------------------|
| Ensamblado sin full ni log | TASK-0106 | GC-1 | AC2 |
| Tool-result clearing + rolling summary | TASK-0106 | GC-2, GC-3 | AC3 |
| Resumen de cierre acotado | TASK-0106 | GC-4 | AC4 |
| Sub-agente aislado y acotado | TASK-0106 | GC-5 | AC5 |
| Off-by-default legacy | TASK-0106 | GC-6 | AC1 |
| Medicion por turno | TASK-0106 | GC-7 | AC6 |
| Umbral de degradacion medido (DELTA-1) | TASK-0106 | GC-9 | AC7 |
| Trigger de consolidacion determinista (DELTA-2) | TASK-0106 | GC-8 | AC8 |
| Edicion atomica (DELTA-3) | TASK-0107 (futuro) | — | s.2.6 (fuera de 0106) |

---

## 11. Trazabilidad de fuentes SOTA (revision adversarial TASK-0109 / DECISION-0031)

Reclasificacion de los votos del ESTUDIO tras verificacion de la voz analista. **Ningun numero no
verificado entra a AC/golden; los umbrales salen de `measure_context_cost` (DECISION-0008).**

| arXiv | Pieza | Estado |
|-------|-------|--------|
| 2603.18718 (MemMA) | edicion atomica (patron) | Verified 3-0 (patron; descartar coord. 4-agentes) -> DELTA-3 |
| 2502.12110 (A-Mem) | dynamic linking / consolidacion post-sesion | Verified 3-0 (patron; offline, fuera del hot path) |
| 2603.09619 (taxonomia memoria) | Working/Episodic/Semantic/Procedural | Verified 3-0 (fundacional conceptual) |
| 2602.16284 (Attention Matching) | umbrales ">100k", "F1 <5%" | **Cifra NO atribuible** (KV-cache; no aplica a CLI) -> DELTA-1 reformulado |
| 2601.07190 (Focus) | "cada 10 tool calls", 22.7% | **Cifra NO atribuible** (autonomo; heuristica no es del paper) -> DELTA-2 reformulado |
| 2604.01707 (Memory in LLM Era) | "sub-450 tokens" | No-verificable (guia, no ley) -> DELTA-4 por medicion |
| 2603.10062 (Multi-Agent Memory) | "mayoria usa hybrid" | No-verificable (claim generico) |
| 2606.00610 (MemGraphRAG) | "8x-49x", ontologia 3-capas | No-verificable / vago (asume graph DB) -> RECHAZADO |

**Rechazos explicitos (neutralidad + single-writer):** Neo4j/Memgraph/graph-DB como prescripcion;
LlamaIndex PropertyGraphIndex; servicio de memoria persistente externo (Mem0/Letta) en el core; "agente de
fondo" de consolidacion vago (sustituido por trigger determinista medido).
