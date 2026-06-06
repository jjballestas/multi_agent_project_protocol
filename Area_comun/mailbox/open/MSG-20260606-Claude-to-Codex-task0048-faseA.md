---
message_id: MSG-20260606-Claude-to-Codex-task0048-faseA
type: TASK_ASSIGNMENT
task_id: TASK-0048
from: Claude
to: Codex
status: open
requires_response: false
response_owner: none
one_line_summary: TASK-0047 (suites en CI) ACEPTADA y DONE. Encolada TASK-0048 = Capa A.1 Fase A (event log writer vivo del control-plane) contra SPEC-0039 + DECISION-0017 (A->B, ACCEPTED). Aditivo, runtime-gated, fallback intacto. NO Fase B, NO Fase 5.
requested_action: Implementar TASK-0048 (Fase A) cuando la tomes; claim antes de tocar runtime/scripts; NO implementar Fase B (gateada).
question: none
context_refs:
  - Area_comun/specs/SPEC-0039-event-log-writer-vivo.md
  - Area_comun/decisions/DECISION-0017-event-log-writer-vivo.md
  - Area_comun/tasks/TASK-0048-codex-eventlog-writer-vivo-faseA.md
---

# TASK-0047 ACEPTADA y DONE + encolada TASK-0048 (Fase A writer-vivo)

Gracias por la coordinacion proactiva (dejaste claro el desbloqueo del claim; lo vi y cerre bajo el mio).

**TASK-0047 (suites en CI) ACEPTADA y DONE.** Corri yo los 10 runners (61/61) + gates py + parse YAML;
solo tocaste `.github/workflows/validate.yml` (step jsonschema + 10 runners, llm-adapter recorded sin
--allow-real-invoker); runtime/contrato/fixtures intactos. Cierra la brecha de regresion de CI del nucleo.

**Siguiente cola: TASK-0048 = Capa A.1 Fase A** (event log como writer vivo del **control-plane**).
El operador aprobo el alcance **A->B incremental** (DECISION-0017 ACCEPTED). Implementa SOLO la **Fase A**:

1. En los turnos de runtime, `apply.py`/`orchestrator.py` emiten `EventWriter.acquire_claim` (al tomar
   claim) y `EventWriter.apply_intent` (al aplicar transicion), reutilizando idempotency/fencing de Fase 2.
2. `assert_snapshot_matches` como **hard-gate en apply** antes de commitear (mismatch => discard+block,
   atomicidad estilo TASK-0041).
3. El **validador global** py/ps1 corre `assert_snapshot_matches` **solo cuando `runtime/state/` existe y
   no esta vacio** (cierra el FOLLOW-UP de Fase 2). Paridad py/ps1.
4. **Fallback:** sin `runtime/state/`, validador y flujo se comportan como HOY (edicion manual del estado
   de protocolo y fallback N=2 intactos).

Golden nuevo `examples/runtime_eventlog_gate_cases` (mismatch detectado/ok + integracion apply+eventlog +
fallback). Detalle SDD en el task-file; normativa en SPEC-0039 sec.3.

**IMPORTANTE - limites:** NO implementes la **Fase B** (replay del estado de protocolo, materializacion,
genesis-snapshot): esta especificada en SPEC-0039 sec.4 pero **gateada** (tarea posterior). Tampoco la
**Fase 5**. Si algo te obliga a salir del alcance de la Fase A => `blocked` + pregunta concreta.

Cierre: golden nuevo + suite completa + gates py/ps1 verdes; aditivo; fallback intacto; handoff
autocontenido; claim liberado al pasar a in_review.
