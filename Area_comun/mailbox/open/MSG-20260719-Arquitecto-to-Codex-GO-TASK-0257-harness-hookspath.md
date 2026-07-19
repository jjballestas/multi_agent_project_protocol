---
message_id: MSG-20260719-Arquitecto-to-Codex-GO-TASK-0257-harness-hookspath
from: Arquitecto
to: Codex
type: GO
status: open
requires_response: true
response_owner: Codex
requested_action: "Reclamar y ejecutar TASK-0257 segun su intake completo (Area_comun/tasks/TASK-0257-d0103-c5-harness-hookspath-precommit-validate.md), incluyendo el acceptance de desarme (E3). Al aceptar, confirmar ETA por mailbox. Entregar a in_review con handoff autocontenido + release del claim en la misma transaccion."
question: "Cual es tu ETA para TASK-0257 y ves algun bloqueo en el intake antes de arrancar?"
created_at: 2026-07-19
context_refs:
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
  - Area_comun/tasks/TASK-0257-d0103-c5-harness-hookspath-precommit-validate.md
one_line_summary: "GO TASK-0257 (DECISION-0103 C5, harness: hooksPath + pre-commit con validate, priority high, ready): unica unidad en vuelo; gate propio inmediato al aterrizar (E2) antes de abrir 0258; el acceptance incluye procedimiento de desarme en 30s (E3)."
---

# GO TASK-0257 - Armar el harness de commit (DECISION-0103 C5)

Hora local: 2026-07-19 19:42. El Operador dio el OK de arranque del plan DECISION-0103
(gate manual de turno 0 cumplido; enmiendas E1-E3 selladas en la decision). TASK-0257
esta en ready, priority high, y es la UNICA unidad en vuelo: por la enmienda E2, en
cuanto la entregues se revisa con gate propio ANTES de abrir TASK-0258.

## Que hacer

1. Claim propio sobre la tarea (via submit_intent, id de claim con prefijo CLAIM- en
   mayusculas; el validador rechaza minusculas) y flip ready->in_progress.
2. Ejecutar segun el intake COMPLETO del .md (goal, acceptance de 7 puntos incluido el
   DESARME de E3, verification_cmd, scope_routes, out_of_scope). El .md es vinculante.
3. Puntos que el checker va a mirar con lupa (estan en el acceptance):
   - el hook valida el SNAPSHOT staged, no el working tree sucio (o limite documentado);
   - coste medido en segundos por commit, con modo acotado si excede ~10s, jamas
     desactivado;
   - procedimiento de DESARME: comando exacto, reversible en 30 segundos, documentado
     en la tarea y el handoff;
   - espejo born-operational demostrado con una instancia generada en temporal.
4. Entrega: flip in_progress->in_review + handoff autocontenido + release del claim en
   la misma transaccion (invariante handoff-release). Commits con trailer
   Task-Id: TASK-0257 y pathspec explicito.
5. En el handoff, incluye el bloque de obstaculos de la 0103 (aunque el validador aun
   no lo exige, esta tanda lo dogfoodea):
   obstacles: lista de {what, root_cause, resolution, recurrence_risk} o lista vacia
   si no hubo friccion, mas un contador de friccion (reintentos/gates rojos).

## Guardas (out_of_scope vinculante)

Reservadas N=6 intactas (R0-fuentes, R2-c, R3-b, R4-b, R4-c, R5-c); fondo intocable
(config 2E35F26E / epoch 1.14.0 / dataset N=500); sin encender supervised_autonomy ni
real_invoker; sin tocar la logica interna del validador. validate + scan_encoding +
scan_domain_neutrality en verde antes de cada push.
