# ANALISTA-TASK-0177-dictado-voz-veredicto

Firma: Analista
Fecha: 2026-06-25

## Veredicto

OK->CERRABLE para TASK-0177.

Ancla canonica revisada:
- Producto Zeus-protocol: `96eb019c5697512282afe6155979d2678cca7157`.
- Protocolo citado por la instruccion REVIEW: `d0a1795af5099525048c666df9053623810367aa`.
- Instruccion REVIEW materializada en protocolo: `e7ca646a04dfb521c6f795592aee528ff3384f68`.

No encontre escape bloqueante en la frontera de egress del dictado: la captura queda off-by-default, el primer uso requiere aviso/confirmacion, el control sin soporte queda deshabilitado, el dictado solo muta el textarea y el submit gobernado sigue redaccion PII.

## Reproduccion

| Gate | Resultado |
| --- | --- |
| Clon limpio producto `D:/Agentes/Zeus/Zeus-protocol`, checkout `96eb019c5697512282afe6155979d2678cca7157` | exit 0 |
| Producto `npm test` en clon limpio | exit 0, 88/88 |
| Payload propio de comportamiento sobre `deriveVoiceDictationControl` + `toggleVoiceDictation` extraido de `public/app.js` | exit 0 |
| Payload propio de no-write-surface sobre funciones de voz + diff `96eb019^..96eb019` | exit 0 |
| Protocolo vivo con secretos `python scripts/validate_collaboration_state.py` | exit 0 |
| Protocolo vivo `python scripts/scan_domain_neutrality.py` | exit 0 |
| Protocolo vivo `python scripts/scan_encoding.py` | exit 0 |
| Protocolo vivo drift | `has_drift=false`, `up_to_seq=1919` |
| Protocolo sin secretos en clon limpio checkout `d0a1795` `validate_collaboration_state.py --root` | exit 0 |
| Protocolo sin secretos `scan_domain_neutrality.py --root` | exit 0 |
| Protocolo sin secretos `scan_encoding.py --root` | exit 0 |
| Protocolo sin secretos drift | `has_drift=false`, `up_to_seq=1908` |
| #4 `protocol.config.json` | byte-identica, sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Vectores adversariales

| Vector / AC | Resultado | Evidencia falsable |
| --- | --- | --- |
| AC3 off-by-default: primera captura sin aceptar aviso | PASA | `window.confirm` devuelve `false`: `confirmCalls=1`, `starts=0`, textarea sin cambios. |
| AC3 aviso de egress antes de capturar | PASA | `VOICE_EGRESS_NOTICE` contiene aviso de audio a servicio externo; con confirmacion `true`, la captura arranca una sola vez. |
| AC3 sin soporte | PASA | `deriveVoiceDictationControl({supported:false})` devuelve `enabled=false`; un boton ya deshabilitado no llama confirm ni `start`. |
| AC2 texto reconocido al campo correcto | PASA | `onresult` con email/telefono/direccion/documento concatena transcript al textarea y dispara evento `input` con `bubbles=true`. |
| AC2 segundo toque detiene | PASA | Segundo click sobre el mismo target llama `stop`; no crea segunda captura. |
| AC4 textarea-only / no submit path | PASA | Las funciones de voz extraidas no contienen `fetch(`, `actions/submit`, `submit_intent`, `writeFile`, `appendFile` ni `createWriteStream`. |
| AC4 sin nueva ruta server-side | PASA | Diff del commit producto toca solo `public/app.js`, `public/styles.css`, `tests/staticContract.test.js`; `src/server.js` no fue tocado. |
| AC4 texto dictado sigue redaccion PII | PASA | `buildRequirementIntakePayload` sobre texto dictado con `persona@example.com`, telefono, direccion y cedula no serializa literales y conserva tokens `EMAIL/PHONE/ADDR/ID-REDACTED`. |
| Familia de egress server-side existente | PASA | Test `src-wide egress guard rejects unallowlisted network exits with positive control` pasa dentro del `npm test` full. |

## Residuales

- No bloqueante: `deriveVoiceDictationControl({supported:false})` conserva `egressRequired=true` aunque `enabled=false`. No abre captura ni escritura; solo es semantica interna del modelo del boton.
- No bloqueante: si el navegador pierde `SpeechRecognition` entre render y click, `toggleVoiceDictation` evalua el aviso antes de deshabilitar. En el flujo normal sin soporte, el boton se renderiza deshabilitado y no captura.
- No bloqueante: Web Speech API puede enviar audio a proveedor del navegador tras opt-in; esto es la frontera honesta de SPEC-0093, no cero-egress local.

## Recomendacion

OK->CERRABLE.
