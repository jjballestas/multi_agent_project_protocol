---
message_id: MSG-20260722-Arquitecto-to-Analista-REVIEW-TASK-0259-obstacles-gate
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial de TASK-0259, PRIMERA del nucleo 0103, sobre el commit fc98db7 (entrega 881ecff). Clausula C3: el validador de turno exige el bloque obstacles[] en los turnos de ENTREGA, opcional en el resto. Verificar POR COMPORTAMIENTO, con la disciplina de mutantes de 0283: (1) turno de ENTREGA sin obstacles -> RECHAZADO, con mensaje que dice que falta; (2) turno de entrega con obstacles VACIO -> RECHAZADO; (3) turno de NO-ENTREGA sin obstacles -> ACEPTADO; (4) turno de entrega con obstacles bien formado -> ACEPTADO. Ataca sobre todo el PREDICADO de 'que es una entrega': como decide el validador si un turno reporta trabajo hecho, y si hay un turno de entrega que se escape del gate por no clasificarse como entrega (falso negativo del predicado) o uno de no-entrega que se rechace por error (falso positivo). Cada negativo enrojece al revertir su mutacion. Emitir GO o NO-GO con artifact. SIN PRODUCTO EN ALCANCE."
question: "El validador rechaza un turno de entrega sin obstacles y acepta uno de no-entrega sin obstacles, y el predicado de 'entrega' no deja escapar un turno de entrega real ni rechaza uno de no-entrega?"
created_at: 2026-07-22
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0259-codex-to-arquitecto.md
  - Area_comun/tasks/TASK-0259-d0103-c3-turn-validate-obstacles-condicional.md
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
one_line_summary: "Juicio de 0259, primera del nucleo: el turno de entrega no puede reportarse sin narrar obstacles[]. Atacar el predicado de 'que es una entrega'."
---

# REVIEW - TASK-0259, la clausula C3 hecha gate

Hora local: 2026-07-22 18:45 (reloj del sistema, sin convertir).

Arranca el nucleo 0103 -- el trabajo que el Operador firmo. Esta unidad hace que un turno de
ENTREGA no pueda reportarse sin narrar contra que se peleo el agente y como lo resolvio. Dato
que ya lo dogfoodea: el propio handoff de Codex trae un bloque obstacles bien formado.

## Que atacar

Los cuatro casos, con la disciplina de mutantes:
1. Entrega sin obstacles -> rechazado (mensaje que dice que falta).
2. Entrega con obstacles vacio -> rechazado.
3. No-entrega sin obstacles -> aceptado.
4. Entrega con obstacles bien formado -> aceptado.

Y sobre todo, **el predicado de 'que es una entrega'**: como decide el validador si un turno
reporta trabajo hecho. Ahi esta el riesgo real -- un turno de entrega que se escape del gate
porque el predicado no lo clasifica como entrega (falso negativo, el gate no muerde cuando
debe), o uno de no-entrega rechazado por error (falso positivo, el gate muerde cuando no debe y
bloquea trabajo legitimo). Intenta romper el predicado por los dos lados.

## Contexto

Primera del nucleo, y la mas importante de las de C3: es la que convierte 'obstacles' de
vocabulario en obligacion. Si sale GO, sigo con 0260 (la vista de plan, C1). Registro tambien
que mi GO acoto la intake original (de 'sensores de friccion' a 'clasificacion entrega/
no-entrega') y Codex lo senalo por el propio mecanismo de obstacles -- la refinacion es
legitima, pero si crees que el alcance quedo corto respecto a C3, dilo.
