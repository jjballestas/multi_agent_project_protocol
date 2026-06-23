---
message_id: MSG-20260623-Arquitecto-to-Codex-GO-TASK-0160
task_id: TASK-0160
type: DIRECTIVE
from: Arquitecto
to: Codex
status: answered
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0160 (ready): 2 fixes en Zeus-protocol. (AC64, BLOQUEANTE) la subida-para-EXTRAER NO debe exigir acceptanceIntent -- src/server.js sanitizeFileExtractionUpload (~864) llama validateHonestRequirementField('acceptanceIntent',...) y bloquea con 'acceptanceIntent is required'; quita esa exigencia (acceptanceIntent OPCIONAL al extraer, vacio permitido), pero MANTENLO REQUERIDO en sanitizeCandidate (~993, aprobacion de candidata); sigue exigiendo proyecto + ack PII para extraer (AC55: no se piden campos antes de la carga; vienen del archivo/modelo). (AC65) alinea/limpia la confirmacion de PII -- public/app.js ~1215 confirm-box: checkbox alineado al inicio, texto que envuelve limpio (CSS), y redaccion en lenguaje llano (simplifica 'escribe via runtime/submit_intent.py como relay acotado' -> 'esta accion se ejecuta de forma gobernada'), label asociado al input; el ack sigue OBLIGATORIO (AC43, solo cambia texto+alineacion). maker=Codex/checker=Arquitecto+Analista; #4 byte-id; carry AC16/17/43/51-63; NUNCA pilotar contra el log vivo (clon desechable)."
requested_action: "Reclama TASK-0160 (ready) e implementa en D:/Agentes/Zeus/Zeus-protocol. AC64: en src/server.js, QUITA de sanitizeFileExtractionUpload la llamada validateHonestRequirementField('acceptanceIntent', acceptanceIntent) (y cualquier exigencia de campos de requisito en la subida-para-extraer); acceptanceIntent queda OPCIONAL ahi (vacio permitido, se sigue saneando/redactando si viene); NO toques sanitizeCandidate, donde acceptanceIntent SIGUE requerido al aprobar una candidata. Manten requerido el proyecto y el ack de PII para extraer. Behavior-test: extraer con acceptanceIntent vacio -> 200 OK (no 400); aprobar candidata sin acceptanceIntent -> sigue 400. AC65: en public/app.js (~1215) alinea el confirm-box (checkbox alineado al inicio del texto, el texto envuelve limpio -- ajusta CSS en public/styles.css si hace falta) y reescribe la etiqueta a lenguaje llano: 'Confirmo que revise PII y que esta accion se ejecuta de forma gobernada.' (o equivalente claro, sin la jerga del path); asocia el label al input (anidado o htmlFor). El ack de PII sigue OBLIGATORIO -- solo cambian texto y alineacion, no la condicion. Manten verdes: node --test clon limpio, validate con/sin secretos exit 0, drift 0, neutralidad+encoding 0, #4 byte-identica (protocol.config.json sin tocar). REPRO: server vivo (runtime override + Ollama) + subir personal/operador/historias_panel_operar_agentes.md -> la extraccion YA no pide acceptanceIntent y salen tarjetas; el check de PII se ve alineado. NUNCA pilotar contra el canonico (clon desechable). Entrega in_review."
context_refs:
  - Area_comun/tasks/TASK-0160-codex-intake-extract-acceptanceintent-pii-label.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - D:/Agentes/Zeus/Zeus-protocol/src/server.js
  - D:/Agentes/Zeus/Zeus-protocol/public/app.js
  - D:/Agentes/Zeus/Zeus-protocol/public/styles.css
deadline_or_blocking_level: normal
---

# GO - TASK-0160: desbloquea extraccion (acceptanceIntent) + alinea confirmacion PII (AC64-AC65)

Dos fixes del feedback de uso. AC64 (BLOQUEANTE): la subida-para-extraer exige acceptanceIntent
(sanitizeFileExtractionUpload ~864) y bloquea con "acceptanceIntent is required" -- en modo archivo ese campo NO se
pide (AC55); quitalo de la extraccion (opcional/vacio) y MANTENLO requerido solo al APROBAR una candidata
(sanitizeCandidate ~993). Sigue exigiendo proyecto + ack PII para extraer. AC65: la confirmacion de PII (app.js
~1215) se ve mal -- alinea el checkbox+texto (CSS) y reescribe la etiqueta en lenguaje llano (sin la jerga
"runtime/submit_intent.py como relay acotado"); el ack sigue OBLIGATORIO, solo cambian texto y alineacion.

REPRO: subir historias_panel_operar_agentes.md -> ya no pide acceptanceIntent + salen tarjetas + check alineado.
maker=Codex / checker=Arquitecto + Analista. #4 byte-identica; clon desechable para el repro.
