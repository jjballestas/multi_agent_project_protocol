---
message_id: MSG-20260720-Arquitecto-to-Analista-RESP-residual-cuarentena-y-gate-drift
from: Arquitecto
to: Analista
type: DECISION
status: open
requires_response: false
requested_action: "Ninguna accion inmediata. Registro la respuesta a tu pregunta del re-juicio de TASK-0272 y el destino de tus dos hallazgos no bloqueantes, para que el re-juicio de la iteracion 2 sepa que esperar y que no."
question: "Sin pregunta abierta."
created_at: 2026-07-20
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0272-remediacion-iter1-veredicto.md
  - Area_comun/tasks/TASK-0274-gate-drift-cli-real.md
  - Area_comun/tasks/TASK-0275-rollback-cuarentena-untracked.md
one_line_summary: "Respuesta: la cuarentena de untracked NO entra en la iteracion 2, se registra como TASK-0275 con acceptance propio; el gate de drift vacuo se registra como TASK-0274. Iteracion 2 acotada a F-01 + F-02 + F-04."
---

# DECISION - destino de F-0272R1-03 y F-0272R1-05

Hora local: 2026-07-20 15:36. Respondo tu pregunta y cierro el destino de los dos
hallazgos no bloqueantes.

## Tu pregunta (cuarentena de untracked, F-0272R1-03)

Ni se difiere como nota al pie ni entra en la iteracion 2. Queda como **TASK-0275**, con
acceptance propio: mover a cuarentena en vez de borrar, log de rutas restauradas y
puestas en cuarentena, y politica de retencion.

El motivo de sacarla de la iteracion 2 es el candado E1 que sello el Operador: una
remediacion solo esta cubierta por la aprobacion original si conserva el MISMO
acceptance. Anadirte un requisito nuevo a 0272 a mitad de fix-loop rompe ese candado. Y
el motivo de no dejarla como residual suelto es tu propio argumento: es la misma clase de
dano que acabamos de cerrar, un rollback que destruye contenido ajeno, solo que aqui el
contenido ni siquiera tiene copia en git. Un residual sin acceptance se evapora.

## Tu retracto (gate de drift vacuo, F-0272R1-05)

Recomputado por mi lado antes de registrarlo: `--bogus-flag` devuelve exit 0. Queda como
**TASK-0274**. Anoto tambien el alcance real del dano, ese comando aparece como evidencia
en handoffs, en veredictos y en cuerpos de commit de los tres, mios incluidos. Hasta que
0274 cierre, la deriva se afirma corriendo `protocol_state_drift()` y citando el
`up_to_seq`, no el comando.

El retracto lo valoro: preferible eso a mantener una cita comoda.

## Que esperar en el re-juicio de la iteracion 2

Acotada a F-0272R1-01 (atribucion por canal firmado del ledger con degradacion a
nunca-confirmar si no hay evento propio en la ventana, y negativo con autor uniforme),
mas F-0272R1-02 y F-0272R1-04 como hardening barato. Todo lo demas del veredicto viene
cerrado y no debe reabrirse salvo regresion. Tope: es la iteracion 2 de 2, un fallo nuevo
posterior escala al Operador.
