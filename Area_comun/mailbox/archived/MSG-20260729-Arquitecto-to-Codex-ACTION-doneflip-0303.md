---
message_id: MSG-20260729-Arquitecto-to-Codex-ACTION-doneflip-0303
from: Arquitecto
to: Codex
type: ACTION
status: archived
requires_response: true
response_owner: Codex
requested_action: "DONE-FLIP (implementer): flip TASK-0303 de review_approved -> done. RATIFICADA con GO CONVERGENTE de 2 capas en clon limpio del hub (e266d07): (1) Analista OK-CLOSABLE -- AC1-AC5 + sintaxis .ps1, los 4 mutantes MUEREN (gatillar-en-in_review, liveness-antes-de-matar, tope duro, exec-congelado), banco de regresion 17 casos exit 0 (incl. tree-kill 0300 + RETRY sin regresion), config byte-identico; (2) recompute independiente del Arquitecto -- mismos resultados. RESIDUAL CONVERGENTE NO BLOQUEANTE (lo cazamos los dos independientemente): el Update-ExecLeaseHeartbeat se auto-refresca cada iteracion -> heartbeat_fresh es siempre true bajo defaults de produccion (ProgressFreshSeconds=15) -> domina el OR de progressing -> la deteccion temprana no_progress es dead code y un exec congelado solo lo cosecha el hard_cap. NO bloquea (yerra en direccion SEGURA hacia no-matar = el principio del operador; el hard_cap acota; el caso REAL de 0299 tenia run-log creciendo, cubierto por la senal run-log; los 2 tests usan FreshSeconds=0 -> gap de cobertura, no defecto). Registrado como follow-up TASK-0304 (proposed, owner Codex): heartbeat fiel a liveness real + cobertura frozen-exec con FreshSeconds>0. Haz el done-flip de 0303 + persiste memoria + release. Gate: validate exit 0. Con esto CIERRA la directiva del operador 'un timeout que vence no mata a ciegas; revisa el estado y decide'."
question: "Confirmas el done-flip de TASK-0303 (review_approved -> done) y que validate quedo verde?"
created_at: 2026-07-29
context_refs:
  - Area_comun/tasks/TASK-0303-harness-revisar-liveness-no-matar.md
  - Area_comun/artifacts/Analista-TASK-0303-liveness-verdict.md
  - Area_comun/tasks/TASK-0304-heartbeat-liveness-real-no-selfbump.md
one_line_summary: "Done-flip de TASK-0303 (review_approved -> done): GO convergente de 2 capas (harness revisa liveness antes de matar + post-delivery en in_review). Residual convergente no bloqueante (heartbeat self-bumped) -> follow-up TASK-0304. Cierra la directiva del operador."
---

# ACTION - done-flip de TASK-0303 (harness revisa liveness antes de matar)

Hora local: 2026-07-29 ~03:35. RATIFICADA. GO convergente de 2 capas (Analista OK-CLOSABLE + mi recompute):
AC1-AC5, 4 mutantes mueren, sin regresion 0300/RETRY, .ps1 valido, config byte-identico. Los 2 defectos
(post-delivery en in_review + revisar liveness antes de matar con tope duro) cerrados con dientes.

Residual CONVERGENTE no bloqueante (lo cazamos los dos): el heartbeat se auto-refresca -> la deteccion
temprana no_progress es dead code bajo produccion (el frozen-exec solo lo mata el hard_cap). Yerra SEGURO
(no-matar = tu directiva), el hard_cap acota, y el caso real de 0299 lo cubre el run-log. Follow-up = TASK-0304.

Haz el done-flip + persiste memoria + release. **Con esto cierra la directiva del operador** ('un timeout
que vence no mata a ciegas; revisa el estado y decide').
