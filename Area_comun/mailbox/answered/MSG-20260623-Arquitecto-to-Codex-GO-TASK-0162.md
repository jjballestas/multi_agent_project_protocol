---
message_id: MSG-20260623-Arquitecto-to-Codex-GO-TASK-0162
task_id: TASK-0162
type: DIRECTIVE
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0162 (ready): UX de tarjetas candidatas en Zeus-protocol (AC69-AC71). La extraccion YA genera tarjetas; arregla la UX de aprobar/usar/estado. (AC69) submitCandidateApproval (public/app.js ~1516) exige candidateDraft.piiReviewed; si falta escribe el error SOLO en #intake-preview (no visible) y vuelve -> 'Aprobar no hace nada'; muestra ese bloqueo VISIBLE en/junto a la tarjeta (rojo) para que el operador sepa que debe marcar 'PII revisada'. (AC70) selectCandidateDraft (~1501) llama applyIntakeInputMode('typed') pero NO sincroniza el radio intake-input-mode -> sincronizalo (radio en typed/manual consistente con la seccion), sin paso manual. (AC71) submitCandidateApproval NO refresca el panel tras aprobar -> la candidata sigue pending; el servidor debe marcar la candidata approved/discarded en el store NO-ledger (idempotente) y el front refresca -> la tarjeta refleja el nuevo estado o sale de pendientes. Carry AC16/17/43/51-68 (gate PII humano, candidatas no-ledger, no segundo escritor). maker=Codex/checker=Arquitecto+Analista; #4 byte-id; NUNCA pilotar contra el log vivo (clon desechable)."
requested_action: "Reclama TASK-0162 (ready) e implementa en D:/Agentes/Zeus/Zeus-protocol. AC69: cuando submitCandidateApproval bloquea por falta de 'PII revisada' (o validacion de la candidata), muestra el error VISIBLE en/junto a la tarjeta (estado rojo), no solo en #intake-preview; el operador debe ver por que no avanzo. Sigue gobernado (submit_intent + gate PII AC43). AC70: en selectCandidateDraft, ademas de applyIntakeInputMode('typed'), marca el radio/control de modo (intake-input-mode) en typed/manual de forma consistente con la seccion mostrada -> sin que el operador cambie el selector a mano. AC71: tras aprobar/descartar una candidata con exito, (a) el servidor marca su estado (approved/discarded) en el store NO-ledger de forma idempotente, y (b) el front refresca el panel (refreshController.refreshView intake) -> la tarjeta refleja el nuevo estado o sale del listado de pendientes; el requisito gobernado se sigue creando por submit_intent (no segundo escritor, AC17). Behavior-tests: (69) aprobar sin PII-revisada -> error visible en la tarjeta; con PII -> procede; (70) usar tarjeta -> radio de modo en typed + seccion typed consistente; (71) aprobar -> status approved y ya no pending; descartar -> discarded; panel refrescado. Manten verdes: node --test clon limpio (EXIT explicito), validate con/sin secretos exit 0, drift 0, neutralidad+encoding 0, #4 byte-id (protocol.config.json sin tocar). REPRO: server vivo+Ollama+subir un .md -> tarjetas; usar-tarjeta cambia a modo manual solo; aprobar sin PII -> error visible; con PII -> aprueba, la candidata cambia de estado y sale de pendientes. NUNCA pilotar contra el canonico (clon desechable). Entrega in_review."
context_refs:
  - Area_comun/tasks/TASK-0162-codex-candidate-cards-ux.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - D:/Agentes/Zeus/Zeus-protocol/public/app.js
  - D:/Agentes/Zeus/Zeus-protocol/src/server.js
deadline_or_blocking_level: normal
---

# GO - TASK-0162: UX de tarjetas candidatas (AC69-AC71)

La extraccion ya genera tarjetas; ahora la UX de aprobar/usar/estado. AC69: "Aprobar" parece no hacer nada porque
exige el check "PII revisada" y el error va a un preview JSON invisible -> muestralo VISIBLE en la tarjeta. AC70:
"Usar tarjeta" cambia la seccion pero no el radio de modo -> sincronizalo (modo manual solo). AC71: tras enviar, la
candidata sigue "pending" -> el servidor la marca approved/discarded (store no-ledger) y el front refresca.

Detalle en la tarea y SPEC-0086 AC69-AC71. maker=Codex / checker=Arquitecto + Analista. #4 byte-id; clon desechable.
