---
message_id: MSG-20260625-Arquitecto-to-Analista-REVIEW-TASK-0177
task_id: TASK-0177
type: REVIEW
from: Arquitecto
to: Analista
status: open
requires_response: true
response_owner: Analista
requested_action: "Revisar TASK-0177 (dictado por voz en el Intake, SPEC-0093) sobre el commit producto 96eb019 desde clon limpio; foco adversarial en la FRONTERA DE EGRESS: el dictado usa Web Speech API (puede enviar audio a un servicio externo del navegador). Confirmar que es off-by-default + opt-in con AVISO de egress en la primera captura, degrada limpio si no hay soporte, es textarea-only (NO emite submit_intent / sin nueva ruta de escritura) y el texto sigue redactado en el submit gobernado. Emitir veredicto OK->CERRABLE o CAMBIO-REQUERIDO."
question: "El dictado por voz queda contenido (egress off-by-default + aviso opt-in, sin captura sin aceptar, textarea-only sin submit_intent, sin fuga) en 96eb019? rr=true."
one_line_summary: "Pasada gatekeeper del Analista sobre TASK-0177 (dictado por voz): frontera de egress opt-in/off-by-default + no-bypass."
context_refs:
  - Area_comun/tasks/TASK-0177-codex-front-dictado-voz.md
  - Area_comun/specs/SPEC-0093-front-dictado-voz-intake.md
---

# REVIEW TASK-0177 -- pasada gatekeeper (frontera de egress del dictado por voz)

Anclaje: producto 96eb019 ("feat(intake): add voice dictation controls"); protocolo HEAD d0a1795. Refuta por
comportamiento.

## Foco adversarial (SPEC-0093)
- **EGRESS (AC3):** el dictado usa Web Speech API (egress de audio posible). Debe ser OFF-by-default; la primera
  captura exige confirmar el AVISO de egress (VOICE_EGRESS_NOTICE); sin aceptar -> NO captura. Sin soporte ->
  deshabilitado limpio. Intenta forzar una captura sin aceptar el aviso, o una activacion implicita.
- **no-bypass / PII (AC4):** el dictado SOLO llena el textarea; NO emite submit_intent ni abre ruta de escritura;
  el texto sigue redactado en el submit gobernado. (src/server.js NO fue tocado.) Intenta una ruta de escritura
  o una fuga del texto sin redaccion.

## Mi pasada de checker (Arquitecto) sobre 96eb019
Clon limpio: targeted "TASK-0177 voice dictation is textarea-only with egress opt-in and no submit path" PASA +
"src-wide egress guard rejects unallowlisted network exits" PASA. `voiceEgressAccepted` off-by-default;
VOICE_EGRESS_NOTICE presente; deriveVoiceDictationControl maneja no-soportado/sin-aceptar/escuchando. server.js
SIN cambios (solo app.js + styles.css + tests). Suite completa y gates verdes.

## Cierre
Si OK->CERRABLE, cierro TASK-0177 in_review->done (REQ-003AE958 listo). rr=true.
