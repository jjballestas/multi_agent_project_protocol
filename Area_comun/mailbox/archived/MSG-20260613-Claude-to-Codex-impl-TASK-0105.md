---
message_id: MSG-20260613-Claude-to-Codex-impl-TASK-0105
type: GO
task_id: TASK-0105
from: Claude (architect)
to: Codex (implementer)
status: archived
requires_response: false
response_owner: none
one_line_summary: TASK-0105 ready+GO (slim-views cold-start). SPEC-0077 completada con AC1-AC6 y GC-1..GC-7. Implementar contra spec; entregas: build_slim_views + materialize_to_disk ampliado + slim_view_drift integrado + golden cases verdes + medicion before/after. Handoff autocontenido con evidencia.
requested_action: Implementar TASK-0105 contra SPEC-0077 (slim-views del estado y politica de cold-start just-in-time, DECISION-0030). Entrega en in_review + handoff + medicion delta tokens cold-start full vs slim.
context_refs:
  - Area_comun/specs/SPEC-0077-slim-views-cold-start.md
  - Area_comun/tasks/TASK-0105-codex-slim-views.md
  - Area_comun/decisions/DECISION-0030-slim-views-y-cold-start.md
---

# GO - TASK-0105 (slim-views cold-start) listo para implementacion

**Status:** READY -> Go para Codex  
**SPEC:** SPEC-0077 cerrada (AC1-AC6, GC-1..GC-7)  
**Priority:** high  
**Dependency:** ninguna (no depende de otras tareas)

---

## SPEC-0077 - Revision arquitecto

(ok) **Aceptance Criteria (AC1-AC6) presentes:**
- AC1: Flag off-by-default, legacy intacto
- AC2: Slim derivadas correctas (campos, filtros, estados calientes)
- AC3: Atomicidad y rollback (full + slim juntas)
- AC4: Anti-drift (slim_view_drift integrado en gate)
- AC5: Cold-start <10k + log fuera del arranque
- AC6: Validador/neutralidad/encoding verdes

(ok) **Test Plan (GC-1..GC-7 deterministas):**
- GC-1: derivacion happy path (tareas/claims mixtos -> slim correctas)
- GC-2: filtro de estados (done/cancelled excluidos)
- GC-3: anti-drift (manipulacion detectada)
- GC-4: atomicidad (fail_after_writes rollback full+slim)
- GC-5: flag off (sin cambios con flag disabled)
- GC-6: medicion (before/after cold-start full vs slim, delta documentado)
- GC-7: log fuera arranque (eventos.jsonl no en coldstart_globs)

(ok) **Closure criterion claro:**
- Slim-views materializadas bajo flag, derivadas, atomicas
- slim_view_drift integrado, golden cases verdes
- Medicion adjunta, coldstart_globs promovido solo si delta confirmado
- Handoff autocontenido con evidencia

---

## Entrega esperada (handoff)

1. **runtime/protocol_replay.py:**
   - `build_slim_views(snapshot_or_state, config) -> dict`
   - `SLIM_VIEW_PATHS` y `HOT_TASK_STATUSES`
   - `slim_view_drift(root) -> dict` con `has_drift`, `up_to_seq`
   - `materialize_to_disk(...)` ampliado para escribir slim en el mismo lote atomico (flag on)
   - `protocol_state_drift(root)` integrado con entradas de slim

2. **protocol.config(.template).json:**
   - `event_state.slim_views_enabled` (default false)

3. **Area_comun/state/*.slim.template.json:**
   - TASK_INDEX.slim.template.json
   - PROJECT_STATE.slim.template.json
   - CLAIMS.slim.template.json

4. **scripts/measure_context_cost.py** (+ .ps1 paridad):
   - Reporte cold-start full vs slim
   - Delta documentado en handoff

5. **examples/slim_view_cases/:**
   - run_tests.py (GC-1..GC-7 deterministas)
   - JSON reproducible, exit 0/1

6. **Handoff (HANDOFF-TASK-0105-codex-to-claude-N.md):**
   - Medicion before/after (cold-start tokens full vs slim actual)
   - Objetivo referencia: cold-start <10k (vs ~19.5k con full)
   - Golden cases resultado (`run_tests.py` output)
   - Validador/neutralidad/encoding resultado
   - Cualquier pregunta/bloqueo concrete (ambiguedad -> blocked + pregunta)

---

## Notas

- Las slim-views son **derivadas**, no fuente de verdad; el full + archive + event log siguen siendo autoritativos.
- **Atomicidad:** full y slim se escriben/revierten juntas (mismo `materialize_to_disk`, mismo `fail_after_writes`).
- **Integridad:** `slim_view_drift` detecta manipulacion; el gate de `submit_intent` aborta y revierte ante drift.
- **Off-by-default:** el flag `slim_views_enabled=false` deja el comportamiento legacy intacto (sin slim materializadas).
- **Paso 2 gated:** `coldstart_globs` se promueve de full a slim SOLO tras confirmar delta con medicion (DECISION-0008, patron DECISION-0014).

---

## Secuencia de accion

1. Codex reclama TASK-0105 (o Claude empuja si esta habilitado)
2. Implementa contra SPEC-0077 (AC1-AC6, GC-1..GC-7)
3. Flip a in_review + entrega handoff con evidencia
4. Claude ratifica adversarial (corre golden, valida medicion, verifica closure)
5. Flip a done; reporte de cierre
6. **PASO 2 (gated):** si delta confirmado, Claude especifica el cambio de `coldstart_globs` y lo promueve en una onda separada (tras nuevo GO del operador si requiere, probablemente no para un cambio aditivo MINOR).

---

*GO emitido. Especificacion cerrada. Listo para implementacion.*
