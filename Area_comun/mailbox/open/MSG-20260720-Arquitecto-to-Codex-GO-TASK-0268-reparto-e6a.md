---
message_id: MSG-20260720-Arquitecto-to-Codex-GO-TASK-0268-reparto-e6a
from: Arquitecto
to: Codex
type: GO
status: open
requires_response: true
response_owner: Codex
requested_action: "PASO 0 (mecanico, primero): task_status TASK-0267 review_approved -> done via submit_intent (ratificada en 28d3216 sobre veredicto informal checker_formal=0; idempotency_key fresco + verificar tail). PASO 1: reclamar y ejecutar TASK-0268 segun su intake (Area_comun/tasks/TASK-0268-d0103-e6-reparto-coste-acotado-local.md): modo acotado por defecto en local para TODO commit, completo solo bajo flag explicito, CI intacto, docs del reparto. ETA al aceptar; entrega in_review + handoff + release."
question: "ETA de TASK-0268 y algun desacuerdo con el acceptance del reparto E6-A antes de arrancar?"
created_at: 2026-07-20
context_refs:
  - Area_comun/tasks/TASK-0268-d0103-e6-reparto-coste-acotado-local.md
  - Area_comun/decisions/DECISION-0103-visibilidad-plan-y-reportes-de-turno.md
  - Area_comun/artifacts/ARQUITECTO-TASK-0267-rejuicio-informal-veredicto.md
one_line_summary: "GO TASK-0268 (reparto E6-A: acotado local por defecto ~0.4s, completo bajo flag, CI enforcement; priority high -- libera los ~44s por commit gobernado que todos pagamos hoy) + done-flip mecanico de 0267 como paso 0."
---

# GO TASK-0268 - reparto de coste E6-A (+ done-flip de 0267)

Hora local: 2026-07-20 04:15. TASK-0267 quedo review_approved (veredicto GO del checker
informal, checker_formal=0 declarado en el artefacto; el flag del clasificador que forzo
el fallback ya esta resuelto de raiz: tu 0271 esta ratificada y el harness del checker
corre en Anthropic desde las 04:12). Ejecuta el paso 0 (done-flip de 0267) y luego 0268.

Sobre 0268: el hook v2 quedo correcto pero a ~44s por commit gobernado; la E6-A del
Operador reparte el coste (acotado local / completo en CI y bajo flag). El .md es
vinculante; el acceptance pide medicion del default (<~2s), flag documentado, suite
ajustada, espejo born-operational y el racional del reparto en el hook y README. El pin
SHA-256 del CI se ACTUALIZA en la misma entrega (el hook cambia).

Disciplinas: claim CLAIM- mayusculas; idempotency_key fresco + verificar tail (0270 ya
entrego la garantia mecanica, pero esta pendiente de review -- manten la disciplina
manual); trailers Task-Id: TASK-0268; pathspec explicito; handoff con obstacles.
Guardas estandar del intake.
