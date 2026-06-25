# ANALISTA TASK-0179 voice egress verdict

Firma: Analista

## Veredicto

OK -> CERRABLE.

Ancla canonica: protocolo `c4dd79b` (`coord(TASK-0179): deliver voice dictation v2`) y producto Zeus-protocol `a25f44a` (`feat(intake): improve voice dictation capture`). Instruccion procesada: `Area_comun/mailbox/open/MSG-20260625-Arquitecto-to-Analista-REVIEW-TASK-0179.md`.

La captura sostenida (`continuous=true`) conserva la frontera: off-by-default, opt-in con aviso antes de la primera captura, sin captura cuando el aviso se rechaza, sin `getUserMedia`, Web Audio, WebSocket ni emisor de red nuevo en el diff de voz, y el texto reconocido queda en textarea hasta el submit gobernado existente con redaccion.

## Reproduccion

| Gate | Resultado |
| --- | --- |
| Producto clean clone `git checkout a25f44a && npm test` | exit 0, 89/89 |
| Producto `node --check public/app.js src/server.js tests/staticContract.test.js` | exit 0 |
| Payloads propios sobre guard de voz extraido | exit 0 |
| Protocolo vivo `python scripts/validate_collaboration_state.py` | exit 0 |
| Protocolo secretless clean clone en `c4dd79b`, `python scripts/validate_collaboration_state.py` | exit 0 |
| Drift runtime `protocol_state_drift(Path("."))` | exit 0, `has_drift=false`, `up_to_seq=1956` |
| `python scripts/scan_domain_neutrality.py` | exit 0 |
| `python scripts/scan_encoding.py` | exit 0 |
| #4 `protocol.config.json` | byte-identica contra `c4dd79b`, sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Vectores adversariales

| Vector / AC | Veredicto | Evidencia falsable |
| --- | --- | --- |
| AC3 egress off-by-default | PASA | Payload propio con `window.confirm` falso no construye `SpeechRecognition`, no llama `start`, no altera textarea y no dispara `fetch`. |
| AC3 opt-in antes de capturar | PASA | Con `window.confirm` verdadero se crea una sola instancia, `start()` ocurre despues de aceptar y el boton queda en estado grabando. |
| AC1 idioma | PASA | La instancia propia queda con `recognition.lang == "es-CO"` aunque el documento simulado declare `lang="en"`; `VOICE_RECOGNITION_LOCALES == ["es-CO","es-419","es-ES"]`. |
| AC3 captura sostenida/manual | PASA | La instancia propia queda `continuous=true`, `interimResults=false`; segundo click llama `stop()` y `onend` finaliza. |
| AC4 post-stop a textarea | PASA | Dos eventos `onresult` acumulados se insertan una sola vez al detener: `prev primer texto segundo texto tercero`; se emite evento `input`. |
| Sin nueva superficie de salida | PASA | Diff del commit toca solo `public/index.html`, `public/app.js`, `public/styles.css`, `tests/staticContract.test.js`; `src/server.js` no cambia. Busqueda en diff de voz no agrega `fetch`, `getUserMedia`, `AudioContext`, `WebSocket`, `EventSource`, `sendBeacon` ni `XMLHttpRequest`. |
| Textarea-only / no submit path nuevo | PASA | El flujo de voz probado no invoca `fetch`; las rutas `actions/submit` existentes siguen fuera del path de voz y no hubo cambio de servidor. |
| Redaccion en submit gobernado | PASA | Payload dictado con email, telefono, direccion y documento no conserva literales crudos en `buildRequirementIntakePayload`; aparecen tokens de redaccion estructural. |
| Unsupported browser | PASA | El render deriva control deshabilitado cuando no hay constructor de SpeechRecognition. |

## Residuales

- La captura sostenida envia mas audio al reconocedor del navegador por sesion que TASK-0177; esto esta declarado y queda cubierto por el mismo aviso opt-in. No es regresion mientras el operador acepte la frontera antes de capturar.
- Si el soporte desaparece entre render y click, el codigo pide confirmacion antes de detectar ausencia de constructor y deshabilitar. No inicia captura ni escribe estado; no lo bloqueo porque no abre egress ni ruta de escritura.

## Recomendacion

OK -> CERRABLE. Arquitecto puede cerrar TASK-0179 si sus propios gates siguen verdes.
