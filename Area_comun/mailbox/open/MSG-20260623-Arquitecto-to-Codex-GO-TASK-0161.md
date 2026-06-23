---
message_id: MSG-20260623-Arquitecto-to-Codex-GO-TASK-0161
task_id: TASK-0161
type: DIRECTIVE
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0161 (ready): 3 fixes del flujo carga-por-archivo en re-prueba (Zeus-protocol). (AC66 BLOQUEANTE) re-subir el MISMO archivo da 409 'auto commit push has no staged submit_intent output changes' porque submit_intent es idempotente (TASK-EXTRACT ya existe) -> commitAndPushSubmitIntentOutputs (src/server.js ~1964: git add + git diff --cached --quiet -> si limpio throw 409) debe tratar diff-limpio como NO-OP EXITOSO que devuelve el taskId existente para que el front PROCEDA a /intake-extractions/run (re-extrae). (AC67) el catch generico reason:'extractor failed' (~1615) traga la causa; callLocalVlm (~1681) usa AbortController -> al exceder timeoutMs el fetch lanza AbortError -> se ve como 'extractor failed'. Distingue: timeout (con ms), HTTP !ok, JSON no parseable, firma. (AC68) el modelo local es lento (carga frio ~10s+gen ~10s); sanitizeLocalVlmConfig (~1150) recorta timeoutMs a min(30000): PRECARGA el modelo (keep_alive en la peticion local-vlm y/o warm-up best-effort al boot) + sube/quita el tope del clamp (permitir minutos). maker=Codex/checker=Arquitecto+Analista; #4 byte-id; off-by-default+loopback intactos; carry AC16/17/43/51-65; NUNCA pilotar contra el log vivo (clon desechable)."
requested_action: "Reclama TASK-0161 (ready) e implementa en D:/Agentes/Zeus/Zeus-protocol. AC66: en commitAndPushSubmitIntentOutputs (src/server.js ~1964), cuando `git diff --cached --quiet` indica diff LIMPIO (sin cambios staged, re-submit idempotente), NO lances 409: tratalo como NO-OP EXITOSO y devuelve un resultado que conserve el taskId de la TASK-EXTRACT existente, de modo que submitFileExtraction (public/app.js) obtenga el taskId y PROCEDA a /intake-extractions/run. Cuida que NO sea bypass (el output gobernado ya existe en el canonico; no creas segundo escritor; carry AC17). AC67: deja de colapsar toda excepcion en reason:'extractor failed' (~1615); mapea la causa -> en callLocalVlm distingue AbortError (timeout: incluye los ms del timeoutMs en el reason), respuesta HTTP !ok (error de endpoint), JSON no parseable (parseo), error de firma/clave; el estado fallido y el mensaje rojo del front muestran esa causa especifica. AC68: (a) precarga del modelo -> agrega keep_alive (p.ej. '30m') al body de la peticion en callLocalVlm y/o un warm-up best-effort al arrancar el server (sin bloquear el boot si Ollama no esta, solo log); (b) timeout generoso -> en sanitizeLocalVlmConfig sube o quita el tope Math.min(30000,...) para local-vlm (permitir varios minutos), configurable; opcional timeout por-segmento. Manten off-by-default + loopback estricto (AC52). Behavior-tests: (66) re-submit mismo archivo -> sin 409, taskId devuelto, extraccion procede (git mockeado diff limpio->no-op); (67) abort->reason timeout con ms, HTTP !ok->reason endpoint, basura->reason parseo; (68) config timeout>30s respetado (clamp no recorta), peticion incluye keep_alive. Manten verdes: node --test clon limpio (captura EXIT explicito), validate con/sin secretos exit 0, drift 0, neutralidad+encoding 0, #4 byte-id (protocol.config.json sin tocar). REPRO: server vivo (runtime override+Ollama) + subir personal/operador/historias_panel_operar_agentes.md -> extrae+tarjetas; re-subir el mismo -> sin 409 y re-extrae; si excede timeout el error dice 'timeout'. NUNCA pilotar contra el canonico (clon desechable). Entrega in_review."
context_refs:
  - Area_comun/tasks/TASK-0161-codex-intake-resubmit-extractor-robust.md
  - Area_comun/specs/SPEC-0086-proyecto-front-mvp-single-operator.md
  - D:/Agentes/Zeus/Zeus-protocol/src/server.js
  - D:/Agentes/Zeus/Zeus-protocol/public/app.js
deadline_or_blocking_level: normal
---

# GO - TASK-0161: re-submit idempotente + extractor robusto (AC66-AC68)

Tres fixes del flujo en re-prueba. AC66 (BLOQUEANTE): re-subir el mismo archivo -> submit_intent idempotente -> nada
staged -> commitAndPushSubmitIntentOutputs (~1964) lanza 409 y bloquea; debe ser NO-OP exitoso que devuelve el
taskId existente para que el front re-extraiga. AC67: "extractor failed" generico (~1615) traga la causa real (el
AbortError del timeout en callLocalVlm se ve igual que todo); distingue timeout/HTTP/parseo. AC68: el modelo local
es lento (~21s frio); precarga (keep_alive + warm-up al boot) + timeout generoso (sube/quita el clamp de 30s).

Detalle en la tarea y SPEC-0086 AC66-AC68. REPRO: subir el .md -> tarjetas; re-subir -> sin 409 y re-extrae.
maker=Codex / checker=Arquitecto + Analista. #4 byte-identica; off-by-default; clon desechable para el repro.
