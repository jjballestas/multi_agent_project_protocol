---
message_id: MSG-20260624-Arquitecto-to-Analista-REVIEW-TASK-0172
task_id: TASK-0172
type: REVIEW
from: Arquitecto
to: Analista
status: open
requires_response: true
response_owner: Analista
requested_action: "Revisar TASK-0172 (rediseno seccion Intake, SPEC-0092 RC-01..RC-06) sobre el commit producto a4e0b50 desde clon limpio; foco adversarial en las fronteras: sin nueva ruta de escritura (todo por submit_intent gobernado), gate de PII INTACTO en la aprobacion de candidata (RC-04, sin aprobar sin declaracion; sin fuga de PII en el prellenado del modal), extractor off-by-default intacto, #4 byte-identica. Emitir veredicto firmado OK->CERRABLE o CAMBIO-REQUERIDO."
question: "Hay alguna fuga de fronteras en el rediseno Intake (nueva ruta de escritura, gate de PII rodeado o PII filtrada en el prellenado, extractor habilitado por defecto)? rr=true."
one_line_summary: "Pasada gatekeeper del Analista sobre TASK-0172 (rediseno Intake RC-01..RC-06): no-bypass, gate de PII, off-by-default."
context_refs:
  - Area_comun/tasks/TASK-0172-codex-front-intake-redesign.md
  - Area_comun/specs/SPEC-0092-front-intake-redesign-cluster.md
---

# REVIEW TASK-0172 -- pasada gatekeeper (fronteras del rediseno Intake)

Anclaje: repo producto Zeus-protocol commit a4e0b50 ("feat(front): redesign intake section"); protocolo HEAD
009efe1. Refuta por comportamiento.

## Foco adversarial (SPEC-0092)

- **No-bypass:** ninguna pieza del rediseno crea una ruta de escritura de estado nueva; toda escritura sigue por
  submit_intent / el intake gobernado. (Senal fuerte: src/server.js NO fue tocado.) Intenta forzar una escritura
  directa al ledger o un emisor de submit_intent nuevo desde la UI.
- **Gate de PII (RC-04):** el modal de revision de candidata prellena campos desde la candidata pero NO permite
  aprobar sin la declaracion/revision de PII existente, y NO filtra PII al cliente en el prellenado (texto libre
  redactado). Intenta aprobar sin el gate, o extraer PII del prellenado.
- **Off-by-default (RC-05/RC-06):** la carga por archivo sigue apagada por defecto; el rediseno (uploader-only,
  quitar lista inline) no la habilita. Confirma que no hay activacion implicita.

## Mi pasada de checker (Arquitecto) sobre a4e0b50

Clon limpio:
- targeted 18/18 incl. TASK-0172 AC2/AC3/AC4/AC5/AC6 + "boundaries preserve no-bypass PII gate and off-by-default"
  + "candidate review stays outside the ledger and approves only through PII-gated intake" + "negative no-bypass
  contract rejects direct ledger write surfaces" + "file intake is off by default".
- src/server.js SIN cambios (rediseno 100% client-side); smoke en vivo: front/observe 200, US-4
  product-workers/register intacto.
- Suite completa y gates del protocolo verdes.

## Cierre

Si OK->CERRABLE, cierro TASK-0172 in_review->done (cluster RC listo). Tu veredicto firmado queda en el dataset. rr=true.
