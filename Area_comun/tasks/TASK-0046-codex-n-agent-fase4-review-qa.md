---
id: TASK-0046
owner: Codex
status: done
type: implementation
priority: high
created_at: 2026-06-06
updated_at: 2026-06-06
depends_on: [TASK-0045]
relates_to: [TASK-0044]
phase: P2
spec_id: Area_comun/specs/SPEC-0038-n-agent-registry.md
linked_decisions: [DECISION-0015, DECISION-0001]
execution_pipeline: [formalizar maquina de estados Review/QA en runtime (turn_schema/turn_validate/apply + router) con transiciones reject_review->changes_requested, fail_qa->qa_failed, pass_qa->done (qa!=autor), assign_fix->claimed con attempt++; counters review_attempts/qa_attempts por tarea; defect_log asociado a attempt_id con checks fallidos; failure_signature canonica = check_id + clase de error normalizada + artefacto/ruta afectada; corte de bucles: mismo check 2x consecutivas con misma firma => bloquear reasignacion automatica => architect_review; qa_attempts > max_qa_cycles (config) => escalado a architect; golden examples/runtime_review_qa_cases nuevo]
acceptance_criteria: [QA fail produce evento qa.failed con checks fallidos + crea defect_log asociado al attempt_id + mueve a qa_failed + incrementa qa_attempts (D-9); pass_qa nunca lo ejecuta el autor (qa != autor, I2); reject_review mueve a changes_requested con defect log y reviewer != autor (I1); SEGUNDO fallo del mismo check con la MISMA failure_signature (A8: diferencias superficiales de log NO saltan el corte) dispara architect_review y bloquea reasignacion automatica; qa_attempts > max_qa_cycles => escalado a architect (no a humano salvo requires_human_decision); NO se alcanza done sin evidencia (artefacto/test segun tipo); routing de fix reasigna preferentemente al autor original si sigue habilitado+capacidad, si no a otro implementador elegible; aditivo/config-gated; fallback N=2 byte-equivalente (golden actuales intactos); sin red]
test_plan: [examples/runtime_review_qa_cases nuevo: (1) fail_qa => qa_failed + defect_log + qa_attempts++; (2) segundo fallo misma firma => architect_review (corte de bucle); (3) fallo con firma distinta NO dispara el corte; (4) diferencias superficiales de log NO cambian la firma (no saltan el corte); (5) qa_attempts > max_qa_cycles => escalate architect; (6) pass_qa por autor => rechazado (I2); reject_review por autor => rechazado (I1); (7) intento de done sin evidencia => rechazado; toda la suite runtime + validador/encoding/neutralidad py+ps1 verdes; fallback N=2 sin regresion]
closure_criteria: [maquina de estados Review/QA con defect logs + failure_signature canonica + corte de bucles + escalado architect/max_qa_cycles; done exige evidencia; golden nuevos verdes + suite completa + gates py/ps1; fallback N=2 sin regresion; neutralidad limpia; handoff autocontenido; claim liberado al pasar a in_review]
---

# TASK-0046 - N-agente Fase 4: maquina de estados Review/QA + defect logs + corte de bucles

Estado operativo: DONE. ACEPTADA por Claude con ratificacion adversarial (2026-06-06): suite 61/61
(review_qa 9/9) + gates py verdes; A8 (firma canonica neutraliza logs superficiales), corte de bucles
con guarda bidireccional (no evadible), I1/I2 reviewer/qa != autor, defect/evidencia obligatorios y
fallback N=2 verificados. FOLLOW-UP no-bloqueante (Fase 5 hardening): autor-de-record desde el estado,
no del payload, para la guarda I1/I2. Ver `Area_comun/handoffs/HANDOFF-TASK-0046-codex-to-claude-1.md`.

> `implementation` -> SDD. Implementar contra **SPEC-0038 (congelada)** Fase 4 (sec.13, linea "Fase 4 -
> Maquina de estados Review/QA") + regla **3.3 (fallo de QA, D-9)** + addenda **A8 (firma de fallo canonica)**
> y **A9 (sin escalado oculto / exclusion multi-capacidad)**. Aditivo, config-gated, **fallback N=2 intacto**.

## Contexto

Las Fases 1-3 ya entregaron: registry de capacidades + validacion semantica (TASK-0043), event log
append-only + idempotencia/fencing + negative replay (TASK-0044), y router weighted-least-loaded
determinista con exclusion de autor + fairness gate (TASK-0045). La Fase 4 cierra el lazo de calidad:
formaliza los estados de Review/QA, registra defectos y **corta bucles** de re-trabajo improductivo.

## Alcance (Fase 4, SPEC-0038 sec.13 + 3.2/3.3)

Tabla de transiciones objetivo (SPEC-0038 sec.3.2):

| Desde | Evento | Hacia | Guarda | Evidencia |
|---|---|---|---|---|
| `in_review` | `reject_review` | `changes_requested` | reviewer != autor (I1) | defect_log |
| `in_review` | `approve_review` | `review_approved`/`qa_pending` | reviewer != autor | nota de review |
| `qa_pending` | `pass_qa` | `done` | qa != autor (I2) | evidencia QA completa |
| `qa_pending` | `fail_qa` | `qa_failed` | qa != autor | defect_log + checks fallidos |
| `qa_failed` | `assign_fix` | `claimed` | orchestrator | defect_log + attempt++ |

### Regla de fallo de QA (D-9, SPEC-0038 sec.3.3)
Al fallar QA: (1) emitir `qa.failed` con checks fallidos; (2) crear `defect_log` asociado al `attempt_id`;
(3) mover a `qa_failed`; (4) reasignar preferentemente al autor original si sigue habilitado y con
capacidad; (5) si no, a otro implementador elegible (via router Fase 3); (6) `qa_attempts++`;
(7) si `qa_attempts > max_qa_cycles` => escalar al `architect` para rediseno; (8) escalar al humano solo
si el arquitecto marca `requires_human_decision`.

### Corte de bucles (A8 + sec.3.3)
`failure_signature` canonica = `check_id` + **clase de error normalizada** + **artefacto/ruta afectada**.
Diferencias superficiales de log (timestamps, ids efimeros, rutas absolutas) **NO** cambian la firma y
**NO** saltan el corte. Si el mismo check falla **2 veces consecutivas con la misma firma**, bloquear la
reasignacion automatica y enviar a `architect_review`.

## Entregables
- `runtime/` (turn_schema.json, turn_validate.py, apply.py, router.py segun haga falta): estados/counters/
  defect_log/failure_signature/corte de bucles, todo **aditivo** y **config-gated** (max_qa_cycles en config).
- `examples/runtime_review_qa_cases/` (nuevo harness golden, py).
- `Area_comun/handoffs/HANDOFF-TASK-0046-codex-to-claude-1.md` (autocontenido).

## Restricciones
- **Neutralidad de dominio innegociable** en nucleo y `*.template.*`.
- **Aditivo**: fallback N=2 byte-equivalente; golden actuales intactos; no editar fixtures legacy.
- **Sin red**; sin secretos.
- Cambios de contrato (schema/transiciones publicas) ya estan **cubiertos por DECISION-0015 + SPEC-0038
  congelada**; si surge algo fuera de la spec congelada => `blocked` + pregunta concreta (no improvisar
  contrato).
- Handoff autocontenido; claim liberado al pasar a `in_review`.
