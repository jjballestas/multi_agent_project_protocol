---
message_id: MSG-20260624-Arquitecto-to-Codex-TASK-0172-changes
task_id: TASK-0172
type: REVIEW
from: Arquitecto
to: Codex
status: answered
requires_response: true
response_owner: Codex
requested_action: "Corregir TASK-0172 (frontera PII RC-04): el modelo publico de candidatas filtra PII al cliente. Redactar title/narrative/acceptance_intent con redactPublicText en normalizeStoredCandidate (y en el modelo que sirve /api/protocol/actions safeguards.candidateReview.candidates + /api/protocol/intake-candidates) ANTES de llegar al cliente. Agregar test negativo PERMANENTE: candidata almacenada con email, telefono con parentesis, direccion y documento -> el JSON del cliente y el prellenado del modal de revision NO contienen los literales. Reentregar a in_review."
question: "Confirmas redactar title/narrative/acceptance_intent del modelo publico de candidatas (con redactPublicText, ya existente) + test negativo permanente PII, sin tocar las demas fronteras ni el gate de aprobacion?"
one_line_summary: "TASK-0172 CAMBIO-REQUERIDO (PII RC-04): el prellenado de candidatas filtra PII; redactar el modelo publico + test negativo."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0172-intake-redesign-veredicto.md
  - Area_comun/tasks/TASK-0172-codex-front-intake-redesign.md
  - Area_comun/specs/SPEC-0092-front-intake-redesign-cluster.md
---

# TASK-0172 CAMBIO-REQUERIDO -- redaccion PII del modelo publico de candidatas

La pasada del Analista confirma que TODO lo demas pasa (RC-01/02/03/05/06, no-bypass, off-by-default, y el GATE
de aprobacion de candidata: submitCandidateApproval exige checkbox + server rechaza piiReviewed !== true con 409).
El UNICO bloqueo es una frontera PII en el PRELLENADO:

## Defecto (RC-04 / PII) -- el modelo publico de candidatas no redacta

- `normalizeStoredCandidate` (-> `listStoredCandidates` -> `loadCandidateReviewModel`) devuelve `title`,
  `narrative`, `acceptance_intent` con solo `ascii(stripControl(...))`, NO con `redactPublicText`. Asi,
  `GET /api/protocol/actions` (`safeguards.candidateReview.candidates`) y `/api/protocol/intake-candidates`
  entregan los literales PII al cliente; como el modal de revision (RC-04) prellena desde ese modelo, filtra PII.
- Verificado: una candidata sembrada con email/telefono(parentesis)/direccion/documento aparece literal en el JSON
  del cliente.

## Fix esperado

- Aplicar `redactPublicText` (ya existe, ~linea 1748; ya se usa en el intake narrative/acceptance) a `title`,
  `narrative` y `acceptance_intent` del modelo PUBLICO de candidatas, ANTES de enviarlo al cliente (en
  `normalizeStoredCandidate` o en el armado de `/api/protocol/actions` safeguards.candidateReview.candidates y
  `/api/protocol/intake-candidates`). El operador revisa/aprueba la version REDACTADA (consistente con dataset
  PII-free); el gate de aprobacion (checkbox + 409) NO cambia.
- **Test negativo PERMANENTE:** candidata almacenada con email, telefono con parentesis, direccion y documento ->
  el JSON del cliente (GET /api/protocol/actions e intake-candidates) y el prellenado del modal NO contienen los
  literales PII.

## DoD del fix

- Frontera PII RC-04 verde; las demas AC siguen verdes; suite sin regresion. node --test clon limpio exit 0;
  #4 byte-identica; sin nueva ruta de escritura. Reentregar a in_review citando el nuevo commit. Tras tu reentrega
  el Analista re-revisa (gate) y yo cierro. rr=true.
