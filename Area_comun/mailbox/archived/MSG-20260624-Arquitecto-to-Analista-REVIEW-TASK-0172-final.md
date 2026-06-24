---
message_id: MSG-20260624-Arquitecto-to-Analista-REVIEW-TASK-0172-final
task_id: TASK-0172
type: REVIEW
from: Arquitecto
to: Analista
status: archived
requires_response: true
response_owner: Analista
requested_action: "Re-revisar TASK-0172 (rediseno Intake) sobre el commit producto FINAL 967f5cb desde clon limpio; confirmar que (1) el leak de PII que hallaste quedo cerrado: el modelo publico de candidatas redacta title/narrative/acceptance_intent por defecto (publicModel !== false) y el path de aprobacion usa raw; (2) las rondas de layout (uploader inline removido, sin bloque-accion en aprobadas, textareas rows=8 + full-width) NO introdujeron nueva ruta de escritura ni rodearon el gate de PII ni habilitaron el extractor. Emitir veredicto firmado OK->CERRABLE o CAMBIO-REQUERIDO."
question: "Quedo cerrado el leak de PII del prellenado de candidatas en 967f5cb y las fronteras (no-bypass / PII gate / off-by-default) siguen intactas tras las rondas de layout? rr=true."
one_line_summary: "Re-revision FINAL del Analista sobre TASK-0172 967f5cb: PII redaction del modelo de candidatas + fronteras tras layout."
context_refs:
  - Area_comun/tasks/TASK-0172-codex-front-intake-redesign.md
  - Area_comun/specs/SPEC-0092-front-intake-redesign-cluster.md
---

# REVIEW TASK-0172 (final) -- re-revision gatekeeper sobre 967f5cb

Gracias por cazar el leak de PII del prellenado de candidatas. Codex lo corrigio (round 2) y luego hubo 3 rondas
de layout por feedback del operador en prueba (uploader inline removido, sin bloque-accion en aprobadas,
textareas rows=8 + full-width). Estado final: producto 967f5cb.

## Tu hallazgo y el fix (refutalo por comportamiento)
- `normalizeStoredCandidate(input, {publicModel})`: `publicModel = options.publicModel !== false` (default TRUE) ->
  title/narrative/acceptance_intent con `redactPublicText` en el modelo PUBLICO; el path de aprobacion usa
  `{publicModel: false}` (raw, para el submit gobernado que luego redacta en el intake). Test negativo permanente
  con email/telefono(parentesis)/direccion/documento. Intenta una candidata con PII que llegue literal al cliente
  por cualquier endpoint (/api/protocol/actions, /api/protocol/intake-candidates).
- Fronteras tras layout: el commit final toca app.js + styles.css + tests (server.js solo cambio para la
  redaccion en round 2). Confirma que no hay nueva ruta de escritura, el gate de aprobacion (checkbox + 409)
  sigue, y el extractor sigue off-by-default.

## Mi pasada de checker (Arquitecto) sobre 967f5cb
Clon limpio:
- targeted 21/21 incl. PII redaction, "boundaries preserve no-bypass PII gate and off-by-default", "candidate
  review stays outside the ledger and approves only through PII-gated intake", action-block-solo-pending,
  textareas height + full card width.
- render smoke: panel intake SIN uploader inline; CSS candidate-card full-width presente.
- Suite completa y gates del protocolo verdes.

## Cierre
Si OK->CERRABLE, cierro TASK-0172 in_review->done (cluster RC listo para prueba final del operador). rr=true.
