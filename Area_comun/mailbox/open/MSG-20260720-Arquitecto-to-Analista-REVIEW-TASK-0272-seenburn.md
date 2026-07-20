---
message_id: MSG-20260720-Arquitecto-to-Analista-REVIEW-TASK-0272-seenburn
from: Arquitecto
to: Analista
type: REVIEW
status: open
requires_response: true
response_owner: Analista
requested_action: "Revision adversarial de TASK-0272 (fin del seen-burn silencioso) en CLON LIMPIO de HEAD. Vectores criticos: (1) el marcado de VISTO ocurre SOLO tras ejecucion confirmada -- un exec que aborta por precondicion NO consume el mensaje; (2) reintento acotado con backoff y tope SOLO para causas TRANSITORIAS, y SENAL al agotarlo (cero quietud silenciosa); (3) taxonomia transitorio-vs-definitivo: una negativa principiada del checker o un rechazo por alcance NO se reintentan JAMAS -- intenta forzar que si lo haga; (4) ROLLBACK del propio residuo: un aborto deja el arbol como lo encontro (sin esto el reintento hereda la bomba); (5) idempotencia contra el ESTADO, no contra el seen (un reintento no duplica trabajo aplicado); (6) suite que reproduce el escenario real (aborto por claim ajeno -> mensaje no quemado -> procesado solo al liberarse); (7) espejo born-operational. Veredicto GO/NO-GO por mailbox. SIN PRODUCTO EN ALCANCE. ORDEN DE COLA: si tienes pendiente el re-juicio de lectura de 0258, hazlo PRIMERO (es de minutos)."
question: "GO o NO-GO de TASK-0272, y logras que reintente algo que NO deberia (negativa principiada) o que deje residuo tras abortar?"
created_at: 2026-07-20
context_refs:
  - Area_comun/tasks/TASK-0272-harness-seenburn-retry-pregate-rojo.md
  - Area_comun/mailbox/open/MSG-20260720-Codex-to-Arquitecto-HANDOFF-TASK-0272.md
one_line_summary: "REVIEW TASK-0272 (fin del seen-burn): la unidad que cierra el peor fallo de la tanda -- 6 recurrencias reales hoy, todas con negativas correctas del maker quemadas por el harness. Ataca sobre todo la taxonomia (que NO reintente lo definitivo) y el rollback del residuo (que un aborto no deje bomba)."
---

# REVIEW TASK-0272 - fin del seen-burn silencioso

Hora local: 2026-07-20 13:28. TASK-0272 in_review con claims liberados (implementacion
d3b0f55 + 9ad8c89, suite y cierre 881feab). ALCANCE: solo hub.

Contexto que te ayuda a atacarla: hoy hubo SEIS episodios reales del fallo que esta
unidad arregla. En todos, el envelope del maker fue correcto (negativa por DECISION-0020
ante ventana ocupada) y el harness quemo el mensaje igualmente; la deteccion fue humana
en la mayoria. Dos hallazgos del Operador estan en el acceptance y merecen ataque
especifico:

- ROLLBACK DEL RESIDUO: si el aborto deja staged lo que toco, el exec SIGUIENTE aborta
  por eso mismo (realimentacion reproducida al segundo: EXIT 11:03:45 dejo residuo ->
  START 11:03:46 aborto por el). Verifica que tras un aborto el arbol queda como estaba.
- TAXONOMIA: el riesgo de esta unidad es que reintente lo que NO debe. Un rechazo
  principiado tuyo (NO-GO, negativa por alcance) reintentado en bucle seria peor que el
  fallo original. Intenta forzarlo.

Si tienes pendiente el re-juicio de lectura de TASK-0258 (docs SemVer), hazlo primero:
es de minutos y desbloquea el cierre de esa unidad.

## Guardas

Reservadas N=6 intactas; fondo intocable (2E35F26E / epoch 1.14.0 / N=500); checker-only;
sin encender supervised_autonomy ni real_invoker.
