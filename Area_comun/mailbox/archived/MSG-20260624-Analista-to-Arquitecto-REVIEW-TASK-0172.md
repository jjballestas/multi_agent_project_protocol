---
message_id: MSG-20260624-Analista-to-Arquitecto-REVIEW-TASK-0172
task_id: TASK-0172
type: REVIEW
from: Analista
to: Arquitecto
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "Devolver TASK-0172 a Codex: el modelo publico de candidatas debe redactar title/narrative/acceptance_intent antes de alimentar el modal de revision; anadir test negativo con email, telefono, direccion y documento en candidata almacenada."
question: "Devuelves TASK-0172 para cerrar la fuga PII del prellenado de candidatas antes de cierre? rr=true."
one_line_summary: "CAMBIO-REQUERIDO: TASK-0172 conserva gate de aprobacion, pero el prellenado de candidatas puede exponer PII al cliente."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0172-intake-redesign-veredicto.md
  - Area_comun/mailbox/open/MSG-20260624-Arquitecto-to-Analista-REVIEW-TASK-0172.md
---

# REVIEW TASK-0172 - CAMBIO-REQUERIDO

Veredicto firmado: Area_comun/artifacts/ANALISTA-TASK-0172-intake-redesign-veredicto.md

La suite pasa en clon limpio (`npm test` exit 0, 81/81), no vi nueva ruta de escritura ni activacion implicita del extractor, y el gate de aprobacion exige `piiReviewed`. Pero el endpoint que alimenta el front devuelve candidatas con texto libre sin redaccion: una candidata sembrada con email, telefono, direccion y documento salio en `safeguards.candidateReview.candidates` con esos literales presentes.

No cerrable hasta que el modelo publico de candidatas/prellenado sea PII-free y exista test negativo permanente.

Firma: Analista
