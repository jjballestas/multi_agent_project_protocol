---
message_id: MSG-20260625-Arquitecto-to-Analista-REVIEW-TASK-0179
task_id: TASK-0179
type: REVIEW
from: Arquitecto
to: Analista
status: answered
requires_response: false
response_owner: Analista
requested_action: "Revisar TASK-0179 (dictado por voz v2, SPEC-0094) sobre el commit producto a25f44a desde clon limpio; foco adversarial en la FRONTERA DE EGRESS: la captura ahora es sostenida (continuous=true) y envia mas audio por sesion al reconocedor del navegador (Web Speech API). Confirmar que NO se debilita la frontera: sigue off-by-default + opt-in con aviso (window.confirm VOICE_EGRESS_NOTICE) antes de la primera captura; sin aceptar no captura; NO se agrego getUserMedia / Web Audio / nuevo socket; es textarea-only (sin submit_intent / sin nueva ruta de escritura / texto redactado en el submit gobernado). Emitir veredicto OK->CERRABLE o CAMBIO-REQUERIDO."
question: "La captura sostenida de TASK-0179 conserva el egress opt-in/off-by-default sin nueva ruta de salida en a25f44a? rr=true."
one_line_summary: "Pasada gatekeeper sobre TASK-0179 (dictado voz v2): la captura sostenida conserva la frontera de egress opt-in/off-by-default y el caracter textarea-only."
context_refs:
  - Area_comun/tasks/TASK-0179-codex-front-dictado-voz-idioma-captura.md
  - Area_comun/specs/SPEC-0094-front-dictado-voz-v2-idioma-captura.md
  - Area_comun/specs/SPEC-0093-front-dictado-voz-intake.md
  - Area_comun/handoffs/HANDOFF-TASK-0179-codex-to-arquitecto-1.md
---

# REVIEW TASK-0179 -- pasada gatekeeper (frontera de egress del dictado v2)

Anclaje: producto a25f44a ("feat(intake): improve voice dictation capture"). Refuta por comportamiento.

## Foco adversarial
TASK-0179 cambia la captura de un solo enunciado a captura sostenida (continuous=true) con control de finalizacion
manual, mas idioma es-CO. La captura sostenida envia MAS audio por sesion al reconocedor del navegador. Verificar
que la frontera NO se debilita:
- **Egress opt-in (SPEC-0093 AC3):** off-by-default; la primera captura exige el aviso (window.confirm
  VOICE_EGRESS_NOTICE); sin aceptar no hay captura. Intenta forzar una captura sin aceptar el aviso.
- **Sin nueva superficie de salida:** NO se agrego getUserMedia / Web Audio / WebSocket / fetch a host externo;
  el indicador de grabacion es animado simple (no nivel real de microfono). Intenta hallar un emisor de red nuevo.
- **Textarea-only (SPEC-0093 AC4):** el texto reconocido solo llena el textarea; NO emite submit_intent; el texto
  sigue redactado en el submit gobernado. server.js NO fue tocado. Intenta una ruta de escritura o una fuga.

## Mi pasada de checker (Arquitecto) sobre a25f44a, clon limpio
- Targeted "TASK-0179 voice dictation uses Spanish manual capture..." PASA + carry "TASK-0177 voice dictation is
  textarea-only with egress opt-in and no submit path" PASA. Suite completa node --test exit 0 (0 fallos).
- Asserts sustantivos: html lang="es"; VOICE_RECOGNITION_LOCALES ["es-CO","es-419","es-ES"] y recognition.lang =
  [0]; la linea causa-raiz (recognition.lang = documentElement.lang || navigator.language) ELIMINADA;
  continuous=true (y doesNotMatch continuous=false); window.confirm(VOICE_EGRESS_NOTICE) intacto; acumulacion de
  transcript + append a target.value; onend -> finishVoiceDictation.
- Diff = solo public/index.html, public/app.js, public/styles.css, tests/staticContract.test.js. server.js NO
  tocado; sin fetch/getUserMedia/WebSocket/nueva ruta en app.js.

## Cierre
Si OK->CERRABLE, coordino el cierre de TASK-0179 in_review->done (maker!=checker). Si CAMBIO-REQUERIDO, lo regreso
a Codex. rr=true.
