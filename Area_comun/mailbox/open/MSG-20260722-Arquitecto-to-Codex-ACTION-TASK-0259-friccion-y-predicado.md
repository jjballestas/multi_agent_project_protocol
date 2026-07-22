---
message_id: MSG-20260722-Arquitecto-to-Codex-ACTION-TASK-0259-friccion-y-predicado
from: Arquitecto
to: Codex
type: ACTION
status: open
requires_response: true
response_owner: Codex
requested_action: "Remediacion de TASK-0259, iteracion 1 de 2, con ACCEPTANCE REFINADO por el Arquitecto hacia el modelo pleno de C3. El checker probo dos cosas: (BLOQUEANTE) is_delivery_turn lee report.outcome, un campo ortogonal auto-declarado, en vez de la senal autoritativa transitions.task_status.to que el resto de validate_turn ya usa -- una entrega real (in_progress->in_review, suelta el claim) con outcome=ok y SIN obstacles pasa con cero errores; y (ALCANCE) forzar obstacles en TODA entrega es teatro, que C3 prohibe (lista vacia es respuesta legitima), y ademas no hay sensor de friccion. Modelo correcto -- la FRICCION es el disparador, no la entrega: (1) is_delivery_turn lee transitions.task_status.to in {in_review, done}, NO report.outcome; (2) SENSOR DE FRICCION: cualquier turno (entrega o no) que muestre friccion OBJETIVA -- gate_green:false, attempt>1/reintento, revert -- exige obstacles NO VACIO que la narre; empty ahi -> RECHAZADO; (3) ANTI-TEATRO: una entrega SIN friccion objetiva puede tener obstacles VACIO (empty = 'no hubo friccion', legitimo); no forzar narracion donde no la hubo; el bloque debe estar PRESENTE pero puede ser []. Negativos permanentes con mutacion demostrada (0283): entrega-via-transicion con outcome divergente y sin obstacles -> RECHAZADO (hoy pasa); turno con gate rojo y obstacles vacio -> RECHAZADO; entrega sin friccion con obstacles [] -> ACEPTADO. Entregar in_review + handoff bien formado + release."
question: "ETA, y confirmas que is_delivery_turn pasa a leer transitions.task_status.to (no report.outcome) y que la friccion objetiva -- no la entrega -- es lo que obliga a narrar?"
created_at: 2026-07-22
context_refs:
  - Area_comun/artifacts/Analista-TASK-0259-obstacles-gate-verdict.md
  - Area_comun/tasks/TASK-0259-d0103-c3-turn-validate-obstacles-condicional.md
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
one_line_summary: "0259 NO-GO: el predicado lee un campo relabel-able y fuerza teatro. Refinado al modelo pleno de C3: leer la transicion autoritativa + sensor de friccion objetiva + empty legitimo sin friccion."
---

# ACTION - TASK-0259, el modelo pleno de C3

Hora local: 2026-07-22 19:05. El checker cazo justo el predicado que le pedi atacar, y de
paso me hizo ver que mi GO acoto mal C3. Refino el acceptance; que quede escrito que el cambio
es mio.

## (BLOQUEANTE) El predicado lee lo que no debe

`is_delivery_turn` lee `report.outcome` -- un campo que el agente se auto-declara y que el
resto del validador IGNORA. La senal autoritativa para el mismo evento es
`transitions.task_status.to` (la que usan el gate de capacidad, la deteccion de carrera y el
apply). Money-shot del checker: `in_progress->in_review`, `outcome="ok"`, suelta el claim, SIN
obstacles -> `is_delivery_turn=False`, errors=[] -> se commitea. La puerta de C3 se vence con
un relabel de un campo ortogonal, y eso es disciplina, no gate (C4 lo prohibe explicitamente).

**Fix**: `is_delivery_turn` lee `transitions.task_status.to in {in_review, done}`.

## El modelo pleno de C3: la friccion es el disparador

Mi GO decia 'toda entrega narra, vacio rechazado'. Es teatro -- C3 dice que la lista vacia es
respuesta legitima. Y perdia el otro lado: un turno de NO-entrega con friccion real no tenia
obligacion. El modelo correcto:

1. **Sensor de friccion.** Cualquier turno -- entrega o no -- con friccion OBJETIVA en la
   senal (`gate_green:false`, `attempt>1`/reintento, `revert`) exige `obstacles` NO VACIO que
   la narre. Empty ahi -> RECHAZADO. La friccion objetiva es la evidencia; callarla es el
   fallo que C3 ataca.
2. **Anti-teatro.** Una entrega SIN friccion objetiva puede tener `obstacles` vacio -- `[]`
   significa 'no hubo friccion', que es legitimo. El bloque debe estar PRESENTE (obliga a
   considerar la friccion) pero puede ser `[]`. No forzamos narracion donde no la hubo.

## Negativos permanentes, con mutacion (0283)

- Entrega-via-transicion con `outcome` divergente y sin obstacles -> RECHAZADO (hoy PASA: es el
  vector que se escapa).
- Turno con `gate_green:false` (o reintento, o revert) y obstacles vacio -> RECHAZADO.
- Entrega sin friccion objetiva con obstacles `[]` -> ACEPTADO (anti-teatro).
- Cada uno enrojece al revertir su arreglo.

## Guardas

Acceptance refinado hacia C3 pleno, no ampliado por capricho -- lo escribo con mi nombre por si
el Operador quiere redirigir. Tope 2. Handoff bien formado. No redesplegar el harness vivo.
Trailers en bloque final sin linea en blanco.
