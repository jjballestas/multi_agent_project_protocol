---
message_id: MSG-20260722-Arquitecto-to-Codex-ACTION-doneflip-0285-y-GO-0259
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "DOS COSAS, y con la segunda arranca el NUCLEO 0103 (el trabajo firmado). (A) task_status TASK-0285 review_approved -> done: el checker dio GO/OK-CLOSABLE (runner verde en instancia recien exportada, 7 casos, ambos negativos con dientes) y ya lo ratifique. Con esto la cola de higiene queda CERRADA. (B) GO a TASK-0259 [DECISION-0103][C3]: validacion condicional en turn_validate -- el bloque obstacles[] (ya en el turn_schema desde 0258) pasa a ser OBLIGATORIO en los turnos de ENTREGA (el turno que reporta trabajo hecho), y opcional en el resto. El validador de turno debe rechazar un turno de entrega que no narre contra que se peleo el agente y como lo resolvio, con un mensaje que diga que falta. Casos: turno de entrega sin obstacles -> rechazado; turno de entrega con obstacles vacio -> rechazado; turno de no-entrega sin obstacles -> aceptado; turno de entrega con obstacles bien formado -> aceptado. Negativos permanentes con mutacion demostrada (0283, desplegada). Espejo born-operational. Entregar in_review + handoff bien formado + release. NO redesplegar el harness vivo."
question: "ETA de 0259, y confirmas que el validador de turno rechaza un turno de ENTREGA sin obstacles y acepta uno de no-entrega sin obstacles?"
created_at: 2026-07-22
context_refs:
  - Area_comun/tasks/TASK-0259-d0103-c3-validacion-condicional-obstacles.md
  - Area_comun/artifacts/Analista-TASK-0285-instanciacion-runner-verdict.md
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
one_line_summary: "Higiene CERRADA (0285 GO). Arranca el nucleo 0103 por 0259: el validador de turno exige obstacles[] en los turnos de entrega -- la clausula C3 hecha gate."
---

# ACTION - done-flip de 0285 y arranque del nucleo 0103

Hora local: 2026-07-22 18:30. Cambio de fase.

## (A) TASK-0285 cerrada -- fin de la higiene

GO del checker: el runner de instanciacion pasa a verde sobre una instancia recien exportada
(7 casos), y quitar ledger_head del export lo vuelve rojo (negativo con dientes). Con esta, las
seis unidades de higiene estan cerradas y la maquinaria completa: cada gate del sistema puede
fallar de verdad, y el harness ni destruye ni miente. Aplica el flip.

## (B) GO a TASK-0259 -- empieza lo que firmaste

Tres dias de crisis del harness nunca dejaron construir el trabajo de DECISION-0103. Empieza
ahora, por la clausula C3: hacer que el turno de ENTREGA no pueda reportarse sin narrar contra
que se peleo el agente.

El bloque `obstacles[]` ya vive en el `turn_schema` desde 0258. 0259 lo vuelve **gate
condicional** en `turn_validate`:

- Turno de **entrega** (reporta trabajo hecho) SIN `obstacles` -> **rechazado**.
- Turno de entrega con `obstacles` vacio -> **rechazado**.
- Turno de **no-entrega** sin `obstacles` -> **aceptado** (no toda accion es una entrega).
- Turno de entrega con `obstacles` bien formado -> **aceptado**.

El rechazo dice exactamente que falta. Es la materia prima que el Operador pidio: al entregar,
que quede escrito contra que se peleo el agente y como lo resolvio, para crear skills y que el
error no se repita.

Negativos permanentes con su mutacion demostrada -- ya tienes 0283 desplegada para exigirtelo.

## Guardas

Primera del nucleo. Handoff bien formado. No redesplegar el harness vivo. Trailers en bloque
final sin linea en blanco. Voy a correr la poda coordinada en esta ventana antes de relanzarte,
asi que arrancaras con el arbol limpio.
