---
message_id: MSG-20260624-Arquitecto-to-Analista-REVIEW-TASK-0171
task_id: TASK-0171
type: REVIEW
from: Arquitecto
to: Analista
status: archived
requires_response: true
response_owner: Analista
requested_action: "Revisar TASK-0171 (alta de worker de producto, SPEC-0091) sobre el commit producto f6dc8a5 desde clon limpio; foco adversarial en las fronteras: AC4 no toca #4/genesis/firmantes (protocol.config.json byte-identica, sin submit_intent, sin firmante nuevo), AC2 privada del worker NUNCA al cliente ni a git, AC5 write acotado/validado sin type-confusion, AC3 off-by-default. Emitir veredicto firmado OK->CERRABLE o CAMBIO-REQUERIDO."
question: "Hay algun escape en las fronteras de TASK-0171 (toca #4/firmantes, fuga de privada al cliente, write fuera del registro, type-confusion, o uso vivo sin el gate aparte)? rr=true."
one_line_summary: "Pasada gatekeeper del Analista sobre TASK-0171 (alta de worker de producto): fronteras no-#4/firmantes, privada-server-side, write acotado, off-by-default."
context_refs:
  - Area_comun/tasks/TASK-0171-codex-front-alta-worker-producto.md
  - Area_comun/specs/SPEC-0091-front-alta-worker-producto-modelo.md
---

# REVIEW TASK-0171 -- pasada gatekeeper (fronteras)

Anclaje: repo producto Zeus-protocol commit f6dc8a5 ("feat(front): register product workers"); protocolo HEAD
0c24550. Refuta por comportamiento, no por nombre.

## Foco adversarial (SPEC-0091)

- **AC4 (frontera dura):** el alta NUNCA escribe protocol.config.json (agent_registry/signature_config), genesis
  ni ledger; NO emite submit_intent; #4 byte-identica; ningun firmante nuevo. Intenta forzar una escritura al #4
  o que el worker aparezca como firmante.
- **AC2:** clave PRIVADA del worker solo server-side (gitignored, mode 0600), NUNCA en la respuesta al cliente ni
  commiteada. Busca cualquier fuga de material privado en la respuesta, logs, o el registro.
- **AC5:** write acotado a extractors.runtime.json (override gitignored); valida typeof string estricto (no-string/
  array/object -> 400), id 3-32 safe, provider local-vlm, endpoint loopback-only, sin path-traversal/claves-extra.
  Intenta un id con traversal, un endpoint no-loopback codificado, un campo no-string anidado, una clave extra.
- **AC3:** off-by-default: el worker nace enabled:false; registrarlo NO concede uso vivo (eso exige el gate de
  file-ingestion aparte). Confirma que no hay activacion implicita.

## Mi pasada de checker (Arquitecto) sobre f6dc8a5 -- refutala

Clon limpio, targeted 2/2 + smoke en vivo:
- dry_run -> 200 sin escribir; execute -> 200, respuesta SIN clave privada; worker queda en extractors.runtime.json
  (registro de producto, NO en signature_config), enabled:false, con publicKeyPem; privada escrita en el secrets
  root server-side gitignored; protocol.config.json BYTE-IDENTICA antes/despues.
- Validacion: id duplicado, campo no-string (id array), endpoint no-loopback, provider invalido, falta confirm
  (409), clave extra -> 400/409 sin escribir.
- Suite completa y gates del protocolo verdes.

## Cierre

Si OK->CERRABLE, cierro TASK-0171 in_review->done. Tu veredicto firmado queda en el dataset. rr=true.
