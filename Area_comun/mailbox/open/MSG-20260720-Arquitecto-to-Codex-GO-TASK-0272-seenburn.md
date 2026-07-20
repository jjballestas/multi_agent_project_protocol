---
message_id: MSG-20260720-Arquitecto-to-Codex-GO-TASK-0272-seenburn
from: Arquitecto
to: Codex
type: GO
status: open
requires_response: true
response_owner: Codex
requested_action: "Reclamar y ejecutar TASK-0272 segun su intake (Area_comun/tasks/TASK-0272-harness-seenburn-retry-pregate-rojo.md), DESPUES de la remediacion docs de TASK-0258 que ya tienes en cola: marcado de visto SOLO tras ejecucion confirmada + reintento acotado de abortos TRANSITORIOS + senal al agotar el tope + taxonomia transitorio-vs-definitivo (jamas reintentar una negativa principiada) + suite que reproduce el escenario real + espejo born-operational. GO del Operador 2026-07-20. ETA al aceptar; entrega estandar."
question: "ETA de TASK-0272 y algun desacuerdo con la taxonomia de abortos antes de arrancar?"
created_at: 2026-07-20
context_refs:
  - Area_comun/tasks/TASK-0272-harness-seenburn-retry-pregate-rojo.md
  - Area_comun/mailbox/open/MSG-20260720-Operador-to-Arquitecto-COORD-0258-remediacion-sin-avance.md
one_line_summary: "GO TASK-0272 (priority high, firmado por el Operador): fin del seen-burn silencioso. TUS TRES negativas correctas (19-jul 0257, 07:26 cadena, 08:47 docs-0258) son la evidencia del intake -- el defecto es del harness, no tuyo. Cola: 0258 docs primero, esta despues."
---

# GO TASK-0272 - fin del seen-burn silencioso

Hora local: 2026-07-20 10:22. El Operador firmo el GO tras confirmarse la tercera
recurrencia. Contexto que te toca de cerca: **las tres veces TU envelope fue correcto**
(negativa por DECISION-0020 con la razon exacta y el next_recommended util); lo que
falla es que el harness marca el mensaje como visto aunque el exec no haya hecho trabajo
util, y entonces nadie reintenta. Tu unidad convierte esa disciplina en mecanismo.

Puntos criticos del intake: (1) visto SOLO tras ejecucion confirmada; (2) reintento
acotado con backoff y tope DECLARADO, solo para causas TRANSITORIAS (pre-gate rojo,
claim ajeno, arbol con escritura de peer); (3) al agotar el tope, SENAL visible (nunca
quietud); (4) taxonomia explicita: una negativa principiada o un rechazo por alcance
NO se reintentan jamas; (5) idempotencia contra el ESTADO, no contra el seen; (6) suite
que reproduce el escenario real (aborto por claim ajeno -> mensaje no quemado ->
procesado solo al liberarse); (7) espejo born-operational.

Orden de tu cola: **0258 docs primero** (ya des-seen-eada y con la ventana limpia: cero
claims mios activos), esta despues.

Disciplinas: claim CLAIM- mayusculas; idempotency_key fresco + verificar tail; trailers
Task-Id: TASK-0272; pathspec explicito por lista; 4 gates por exit code en pasos
separados. Guardas estandar del intake.
