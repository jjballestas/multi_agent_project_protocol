---
message_id: MSG-20260623-Arquitecto-to-Codex-GO-TASK-0163
task_id: TASK-0163
type: DIRECTIVE
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0163 (ready): cuando una escritura gobernada del front choca con un claim activo (contencion del ledger), el operador NO debe ver el comando submit_intent crudo ni el traceback. (AC72) src/server.js (runSubmitIntent/runFileExtractionAgent) detecta el error de contencion del submit_intent ('claim acquire overlaps active claim' u otro) y responde un error LIMPIO y TIPADO (p.ej. 409 code 'ledger-busy'/'retry-later') SIN exponer el argv/comando ni el stacktrace; ningun otro error tecnico debe filtrar el argv crudo al cliente. public/app.js mapea ese error tipado a un mensaje AMABLE visible 'Canal ocupado, intente mas tarde' (rojo/aviso, idealmente con reintento), en aprobar-candidata + requirement-intake + kickoff. maker=Codex/checker=Arquitecto+Analista; #4 byte-id; NUNCA pilotar contra el log vivo (clon desechable). NO cambia la semantica de gobierno (la escritura sigue serializada por DECISION-0020); solo el MENSAJE. El fix de RAIZ (claim de grano fino) es pieza/decision SEPARADA, no aqui."
requested_action: "Reclama TASK-0163 (ready) e implementa en D:/Agentes/Zeus/Zeus-protocol. SERVER: en runSubmitIntent (y donde se ejecute submit_intent), captura el error del CLI y DETECTA el caso de contencion ('claim acquire overlaps active claim', u otros de contencion del ledger) -> responde un error LIMPIO y tipado (p.ej. status 409, body { error: 'ledger-busy', retryable: true } o equivalente) SIN incluir el comando/argv ni el traceback; para otros errores tecnicos, tampoco devuelvas el argv crudo al cliente (loguea server-side si hace falta, pero el body al cliente va saneado). FRONT: en public/app.js (submitCandidateApproval, submitFileExtraction/requirement-intake, kickoff) mapea ese error tipado de contencion a un mensaje amable VISIBLE 'Canal ocupado, intente mas tarde' (estado rojo/aviso), idealmente con un boton/opcion de reintentar; no muestres el error tecnico crudo. Behavior-tests: respuesta de submit_intent con claim-overlap -> el server responde error tipado de contencion (body SIN comando/traceback) y el front muestra el mensaje amable; otros errores no filtran el argv. Manten verdes: node --test clon limpio (EXIT explicito), validate con/sin secretos exit 0, drift 0, neutralidad+encoding 0, #4 byte-id (protocol.config.json sin tocar). REPRO: aprobar/escribir mientras hay un claim activo de otro escritor -> el front dice 'Canal ocupado, intente mas tarde', no el comando crudo. NUNCA pilotar contra el canonico (clon desechable). Entrega in_review."
context_refs:
  - Area_comun/tasks/TASK-0163-codex-ledger-busy-friendly-message.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - D:/Agentes/Zeus/Zeus-protocol/src/server.js
  - D:/Agentes/Zeus/Zeus-protocol/public/app.js
deadline_or_blocking_level: normal
---

# GO - TASK-0163: canal ocupado -> mensaje amable (AC72)

Cuando una escritura del front choca con un claim activo, el operador vio el comando submit_intent + traceback
crudo. Eso no debe verse. Server: detecta la contencion ('claim acquire overlaps active claim') -> error tipado
409 ledger-busy SIN argv/traceback. Front: 'Canal ocupado, intente mas tarde' (rojo, con reintento) en
aprobar-candidata/requirement-intake/kickoff. Solo el mensaje; la serializacion (DECISION-0020) no cambia.
maker=Codex / checker=Arquitecto + Analista. #4 byte-id; clon desechable.
