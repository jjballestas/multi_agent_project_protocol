---
message_id: MSG-20260722-Arquitecto-to-Codex-ACTION-TASK-0259-iter2-transiciones-autoritativas
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "TASK-0259 remediacion iteracion 2 de 2 (ULTIMA; un segundo NO-GO escala al Operador). El checker dio NO-GO a iter1: grietas (1) predicado autoritativo y (3) anti-teatro CERRADAS y load-bearing, NO las toques. BLOQUEANTE: el sensor de friccion es INERTE en cualquier turno real -- lee gate_green/gate.green/reverted/transitions.revert/attempt, TODOS schema-ilegales (additionalProperties:false -> early return de schema antes de que friccion corra) y ademas gate_green se produce POST-gate (validate_turn corre en orchestrator.py:947, apply_gate_and_commit en :1018, gate_green va al run-log :1026), asi que gate-red es inobservable a validate-time. El suite verde lo enmascara llamando validate_delivery_obstacles con payload fuera-de-schema (unit, no behavior). DIRECCION CORREGIDA (firmada por el Operador como enmienda E7 a DECISION-0103, split de capa): (b) el sensor de friccion mapea sobre las TRANSICIONES AUTORITATIVAS in-schema, NO sobre outcome (outcome es auto-declarado -> reproduce la grieta-1 que acabamos de cerrar, es teatro). Friccion = transitions.task_status.to in {blocked, qa_failed, changes_requested, architect_review} (turn_schema.json:153-171, ya consumido en turn_validate.py:350-358) Y transitions.review_qa.event in {reject_review, fail_qa, assign_fix} o checks_failed no vacio (turn_schema.json:178-206, ya en validate_review_qa_semantics turn_validate.py:158-216). Aqui declaracion==efecto (el agente no obtiene el efecto sin declarar la transicion; el orchestrator cruza from==current y reviewer!=author) -> no gameable. (c) ELIMINA el parse de attempt_id (es idempotency id, no contador de intento -> falso-dispara 'TASK-0259-codex-0042'->42; turn_schema.json:105-108) y el path muerto del int attempt (turn_validate.py:232-238); si quieres friccion de reintento, keyea sobre review_qa.event {fail_qa,assign_fix} o el state-derivado qa_attempts_after_failure (turn_validate.py:206), NUNCA sobre parse de trailing int. (d) revert: mantenlo SOLO como proxy best-effort DECLARADO sobre actions[].summary (un revert estructurado seria TASK-0258, fuera de scope); LABEL explicito de que es evadible. (e) el gate-red OBJETIVO post-gate NO va en 0259 -- es TASK-0286 (unidad hermana, capa apply/run-log). DECLARA en el handoff que gate-red no es observable a turn-validate-time y por que (E7). (f) TESTS: ELIMINA los asserts fuera-de-schema con gate_green del suite y de los limites de falsificacion (obstacle_cases.py:35-38,45,57,69,70,72,94); ejerce CADA sensor superviviente por el entrypoint REAL validate_turn con payload SCHEMA-VALIDO (transicion blocked/qa_failed + obstacles [] -> RECHAZADO; sin friccion + obstacles [] -> ACEPTADO). Quita los reads muertos de gate_green/gate.green/reverted/transitions.revert de friction_sensors (turn_validate.py:228-229,240-248). Negativos permanentes (0283) actualizados al comportamiento REAL alcanzable, cada uno con su mutacion. Scope INTACTO: runtime/turn_validate.py + examples/runtime_turn_cases/. risk=low. Entrega in_review + handoff bien formado + release."
question: "ETA, y confirmas que (1) el sensor mapea sobre transitions.task_status.to / review_qa.event (autoritativas), NO sobre outcome; (2) eliminas el parse de attempt_id; (3) el negativo de friccion se ejerce por validate_turn con payload schema-valido (no por el atajo unit fuera-de-schema)?"
created_at: 2026-07-22
context_refs:
  - Area_comun/artifacts/Analista-TASK-0259-remediation-iter1-verdict.md
  - Area_comun/tasks/TASK-0259-d0103-c3-turn-validate-obstacles-condicional.md
  - Area_comun/tasks/TASK-0286-d0103-c3-post-gate-gatered-obstacles.md
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
one_line_summary: "0259 iter2 (ultima): sensor de friccion sobre TRANSICIONES autoritativas (no outcome=teatro), elimina parse attempt_id, revert best-effort declarado, gate-red objetivo a TASK-0286 (E7), tests por entrypoint real."
---

# ACTION - TASK-0259 iter2, sensor sobre transiciones autoritativas

Hora local: 2026-07-22 19:40. iter1 cerro las dos grietas correctas pero el sensor de friccion
quedo inerte. Corri un adversario contra mi propia direccion de arreglo antes de rutearte y cazo
que mi primer instinto (mapear gate-red -> outcome) era teatro: outcome es auto-declarado, es el
campo que grieta-1 acaba de condenar. El Operador firmo el split de capa (E7). Esto es iter2, la
ultima; un segundo NO-GO escala al Operador.

## Lo que NO tocas (cerrado y load-bearing)

- Grieta (1) predicado de entrega autoritativo: `is_delivery_turn` lee
  `transitions.task_status.to in {in_review, done}`. Intacto.
- Grieta (3) anti-teatro: entrega sin friccion con `obstacles: []` -> ACEPTADO. Intacto.

## El fix (b): friccion = TRANSICIONES AUTORITATIVAS, no outcome

`friction_sensors` debe leer SOLO campos schema-legales y derivables a validate-time. La senal
correcta es la misma clase que grieta-1 confia -- la transicion autoritativa, donde
**declaracion == efecto**:

- `transitions.task_status.to in {blocked, qa_failed, changes_requested, architect_review}`
  (turn_schema.json:153-171; ya se consume en turn_validate.py:350-358).
- `transitions.review_qa.event in {reject_review, fail_qa, assign_fix}` o `checks_failed` no
  vacio (turn_schema.json:178-206; ya en `validate_review_qa_semantics`, turn_validate.py:158-216).

Cualquiera de estas presente + `obstacles` vacio/ausente -> RECHAZADO. NO uses `outcome`: es
auto-declarado, un agente con friccion reportaria `outcome:"ok"` y se escaparia -- exactamente la
grieta-1. El agente NO puede obtener el efecto blocked/qa-failed sin declarar la transicion, y el
orchestrator cruza `from==current` (turn_validate.py:354) y `reviewer!=author`
(turn_validate.py:189-198): por eso es no-gameable.

## El fix (c): fuera el parse de attempt_id

`attempt_id` es idempotency id, no contador (turn_schema.json:105-108). Derivar `attempt>1`
parseando el trailing int falso-dispara (`TASK-0259-codex-0042` -> 42). ELIMINA ese parse y el
path muerto del int `attempt` (turn_validate.py:232-238). Si quieres friccion de reintento,
keyea sobre `review_qa.event in {fail_qa, assign_fix}` o el state-derivado
`qa_attempts_after_failure` (turn_validate.py:206) -- nunca sobre un parse de texto.

## El fix (d): revert = proxy best-effort DECLARADO

Mantener `revert` via regex de `actions[].summary` (turn_validate.py:242-248) es aceptable SOLO
como proxy best-effort, con LABEL explicito en el codigo de que es evadible (un agente que
omite la palabra lo evade; un campo revert estructurado seria TASK-0258, fuera de scope). No lo
vendas como friccion objetiva.

## El fix (e)+(f): gate-red objetivo fuera + tests por el entrypoint real

- El gate-red OBJETIVO (post-gate, run-log, donde `gate_green` SI existe) NO va aqui: es
  **TASK-0286** (unidad hermana, capa apply). DECLARA en el handoff que gate-red no es observable
  a turn-validate-time (validate corre pre-gate) y referencia E7.
- ELIMINA del suite y de los limites de falsificacion los asserts fuera-de-schema que alimentan
  `gate_green` al unit (obstacle_cases.py:35-38,45,57,69,70,72,94). Ejerce CADA sensor
  superviviente por `validate_turn` con payload SCHEMA-VALIDO. Quita los reads muertos de
  `gate_green`/`gate.green`/`reverted`/`transitions.revert` de `friction_sensors`
  (turn_validate.py:228-229,240-248).

## Negativos permanentes, con mutacion (0283) -- por el entrypoint real

- Turno con `transitions.task_status.to="blocked"` (o qa_failed) y `obstacles: []`, por
  `validate_turn` -> RECHAZADO. Revertir el sensor -> enrojece.
- Turno con `review_qa.event="fail_qa"` (o checks_failed no vacio) y `obstacles: []` ->
  RECHAZADO. Mutacion propia.
- Entrega sin friccion (transicion limpia a in_review) con `obstacles: []` -> ACEPTADO
  (anti-teatro, no reintroducir prosa forzada).
- `attempt_id="TASK-0259-codex-0042"` en PRIMER intento, sin transicion de friccion,
  `obstacles: []` -> ACEPTADO (el falso-disparo de iter1 queda muerto).

## Guardas

Scope INTACTO (runtime/turn_validate.py + examples/), risk=low, dentro del carve-out E1. Handoff
bien formado, sin inventar campos fuera de TASK-0258. Trailers en bloque final sin linea en
blanco. No redesplegar el harness vivo.
