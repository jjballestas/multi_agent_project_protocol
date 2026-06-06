---
id: TASK-0048
owner: Codex
status: in_progress
type: implementation
priority: high
created_at: 2026-06-06
updated_at: 2026-06-06
depends_on: [TASK-0044, TASK-0046]
relates_to: [TASK-0047]
phase: P2
spec_id: Area_comun/specs/SPEC-0039-event-log-writer-vivo.md
linked_decisions: [DECISION-0017, DECISION-0015, DECISION-0009]
execution_pipeline: [en los turnos de runtime, apply.py/orchestrator.py invocan EventWriter.acquire_claim al tomar claim y EventWriter.apply_intent al aplicar transicion (reutilizando idempotency_key/fencing/aggregate de Fase 2); assert_snapshot_matches como hard-gate en apply ANTES de commitear (mismatch => discard+block, atomicidad estilo TASK-0041); scripts/validate_collaboration_state.py y .ps1 corren assert_snapshot_matches SOLO cuando runtime/state existe y no esta vacio; golden nuevo examples/runtime_eventlog_gate_cases]
acceptance_criteria: [en un turno de runtime, el control-plane del event log (claims/leases/fencing/idempotency) refleja lo que apply aplica (acquire_claim/apply_intent emitidos); assert_snapshot_matches es hard-gate en apply: snapshot incoherente => el turno NO commitea (discard+block, sin estado a medias); el validador global py/ps1 corre assert_snapshot_matches cuando runtime/state existe y no esta vacio, y es hard-fail si hay mismatch; FALLBACK: sin runtime/state (o vacio) el validador y el flujo actual se comportan EXACTAMENTE como hoy (edicion manual del estado de protocolo intacta, fallback N=2 byte-equivalente); NO se implementa Fase B (replay del estado de protocolo); sin red; neutralidad limpia; paridad py/ps1 del gate]
test_plan: [examples/runtime_eventlog_gate_cases nuevo: (1) snapshot coherente => apply commitea; (2) snapshot mismatch (up_to_seq o hash) => apply aborta con discard+block, sin commit; (3) integracion: un turno de runtime emite acquire_claim+apply_intent y el control-plane del log queda coherente con el snapshot; (4) fallback sin runtime/state => validador global verde como hoy; (5) determinismo (sin reloj/red, reutiliza negative replay de Fase 2). Correr ademas TODA la suite runtime (debe seguir verde) + validador/encoding/neutralidad py + paridad ps1 del gate]
closure_criteria: [apply/orchestrator emiten al EventWriter en turnos de runtime; assert_snapshot_matches hard-gate en apply + en validador global cuando runtime/state existe; fallback intacto sin runtime/state; golden runtime_eventlog_gate_cases verde + suite completa + gates py/ps1; aditivo, fallback N=2 sin regresion; neutralidad limpia; handoff autocontenido; claim liberado al pasar a in_review]
---

# TASK-0048 - Capa A.1 Fase A: event log como writer vivo del control-plane

> `implementation` -> SDD. Implementar contra **SPEC-0039** (seccion 3, Fase A) + **DECISION-0017**
> (alcance A->B incremental, ACCEPTED). Aditivo, runtime-gated, **fallback intacto**. NO implementar la
> Fase B (replay del estado de protocolo), que esta gateada.

## Contexto

El event log (Fase 2, TASK-0044) esta implementado pero es observacional: `apply.py` escribe el estado
directo y `assert_snapshot_matches` no esta cableado. Esta tarea hace que, EN LOS TURNOS DEL RUNTIME, el
control-plane del log refleje lo aplicado y que la consistencia del snapshot sea un hard-gate. Cierra el
FOLLOW-UP rastreado desde Fase 2 ("cablear assert_snapshot_matches al validador global cuando el event log
sea writer vivo"), para lo que el runtime efectivamente escribe.

## Alcance (Fase A, SPEC-0039 sec.3)

1. **Emision desde el runtime:** en `apply.py`/`orchestrator.py`, al ejecutar un turno de runtime, invocar
   `EventWriter.acquire_claim(...)` (al tomar claim) y `EventWriter.apply_intent(...)` (al aplicar la
   transicion), reutilizando idempotency_key por tupla + fencing por-aggregate de Fase 2.
2. **Gate en apply:** `assert_snapshot_matches(root)` ANTES de commitear el turno; si hay mismatch
   (up_to_seq o hash canonico), abortar con discard + block (atomicidad, estilo TASK-0041), sin dejar
   estado a medias.
3. **Gate global:** `scripts/validate_collaboration_state.py` y `.ps1` corren `assert_snapshot_matches`
   **solo cuando `runtime/state/` existe y no esta vacio**; mismatch => hard-fail. Paridad py/ps1.
4. **Fallback:** sin `runtime/state/` (o vacio) -> validador y flujo se comportan como hoy; edicion manual
   del estado de protocolo y fallback N=2 intactos.

## Restricciones

- **NO** implementar Fase B (replay del estado de protocolo, materializacion, genesis-snapshot): gateada.
- **Aditivo**: no romper la suite runtime existente ni el flujo de edicion manual actual del repo vivo.
- **Sin red**; sin secretos; **neutralidad de dominio** intacta.
- Paridad py/ps1 del gate global.
- Handoff autocontenido; claim liberado al pasar a `in_review`.

## Nota de proceso

Esta tarea es la implementacion de la **Fase A** del writer-vivo. La **Fase B** sera una tarea/SPEC
posterior, gateada por el operador, cuando el runtime sea el escritor habitual del estado de protocolo.
