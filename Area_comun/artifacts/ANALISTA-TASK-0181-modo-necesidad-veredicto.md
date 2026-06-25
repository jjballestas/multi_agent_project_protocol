# ANALISTA TASK-0181 - veredicto modo necesidad

Firma: Analista
Fecha: 2026-06-25

## Veredicto

CAMBIO-REQUERIDO.

No recomiendo cierre. El gate obligatorio de producto en clon limpio no pasa: `npm test` sobre el commit producto canonico `2d7e80535f52f6e71dd1bf9b0a6425d1d7325195` termino con exit 1, 86/91 tests pass y 5 fallos. Ademas, en prueba propia del builder del modo necesidad, PII cruda del textarea queda dentro del body enviado a `/api/protocol/actions/submit` como `file.text`; si el AC exige que el submit gobernado ya viaje redactado, ese vector slips antes de cualquier redaccion posterior del servidor.

Ancla canonica usada:
- Producto: `2d7e80535f52f6e71dd1bf9b0a6425d1d7325195` (`feat(intake): add need extraction mode`).
- Protocolo/instruccion REVIEW: `5f9354619e0b1e604eb12331daf8f5c8da08b388`.
- Repositorio producto revisado en clon limpio: `C:\Users\johnb\AppData\Local\Temp\zeus-protocol-0181-analista-575a9991ad9e4f45b9753c9388f4af85`.

## Reproduccion

| Prueba | Resultado |
|---|---|
| `git clone D:/Agentes/Zeus/Zeus-protocol <tmp>; git checkout 2d7e805; npm test` | exit 1. 91 tests, 86 pass, 5 fail. |
| Fallos del full `npm test` | `intake endpoint rejects impersonation...` killed by SIGTERM during `python scripts/validate_collaboration_state.py --root .`; `file ingestion...` 502 != 200; `local-vlm extractor reports...` 502 != 200; `candidate review stays outside...` 502 != 200; `auto commit push lands...` 502 != 200. |
| `npm test -- --test-name-pattern "TASK-0181|file intake|TASK-0179|TASK-0177"` | exit 0, 8/8 pass. |
| `npm test -- --test-name-pattern "candidate review stays outside"` | exit 1; validator child killed by SIGTERM inside test. |
| Payload propio `buildFileRequirementPayload({name:"necesidad.txt", text:<PII>}, ...)` | exit 0; el JSON resultante conserva `persona@example.com`, `+57 300 123 4567`, `Calle 10 No 20-30` y `123456789` en `file.text` y en el body completo. |
| Payload propio `buildCandidateApprovalPayload(... piiReviewed:false/true)` | exit 0; `piiReviewed:false` queda false y `piiReviewed:true` queda true en el payload. |
| Control propio `deriveVoiceDictationControl` | exit 0; sin soporte queda disabled; con soporte y sin opt-in expone aviso `VOICE_EGRESS_NOTICE`; con opt-in ya no marca egress requerido. |
| Diff producto `HEAD^..HEAD` | Solo `public/app.js`, `public/styles.css`, `tests/staticContract.test.js`. |

## Tabla adversarial

| Vector / AC | Estado | Evidencia falsable |
|---|---|---|
| Gate full de producto en clon limpio | CAMBIO-REQUERIDO | `npm test` exit 1 en clon limpio del commit canonico. La instruccion gatea por exit code, no por targeted tests. |
| PII del texto libre del textarea | SLIPS | `buildFileRequirementPayload` con texto `persona@example.com telefono +57 300 123 4567 direccion Calle 10 No 20-30 cedula 123456789` conserva esos literales en `file.text` del body enviado a `/api/protocol/actions/submit`. La redaccion de `acceptanceIntent` si ocurre, pero no la fuente `necesidad.txt`. |
| Gate PII humano AC43 | PASA parcial | Builder conserva `piiReviewed` como booleano estricto; el codigo de `submitCandidateApproval` bloquea localmente si falta. No doy cierre porque el test full que cubre candidate review falla en clon limpio. |
| Egress de voz opt-in/off-by-default | PASA | `deriveVoiceDictationControl` y el codigo de `toggleVoiceDictation` mantienen aviso `VOICE_EGRESS_NOTICE`, `window.confirm(...)` antes de construir `SpeechRecognition`, y sin aceptar retorna sin captura. |
| No-egress de modelo en modo necesidad | PASA estatico | La funcion `submitNeedExtraction` solo hace fetch a `/api/protocol/actions/submit` y `/api/protocol/intake-extractions/run` con consent `DETERMINISTIC_FILE_CONSUMER`; no contiene `localVlm`, `http.request`, `net.connect` ni fetch a modelo. |
| Store fuera del dataset / drift 0 | PASA protocolo, no cerrable por producto | Drift vivo del protocolo `has_drift=false`, `up_to_seq=1979`. El store de candidatas sigue fuera de ledger por inspeccion de rutas, pero el full test de producto que ejerce flujo de candidatas no pasa. |
| OFF-by-default | PASA | Selector `value="need"` y boton `data-need-extract` quedan disabled cuando `fileIngestion.enabled` no es true. |

## Gates de protocolo

| Gate | Resultado |
|---|---|
| `python scripts/validate_collaboration_state.py` en vivo | exit 0. |
| `python scripts/validate_collaboration_state.py` sin secretos en clon `5f93546` | exit 0. |
| Drift vivo | exit 0; `has_drift=false`, `up_to_seq=1979`. |
| `python scripts/scan_domain_neutrality.py` | exit 0. |
| `python scripts/scan_encoding.py` | exit 0. |
| `protocol.config.json` #4 byte-identica | sha256 vivo y clon `5f93546`: `2e35f26e06de4d0a7e5278babb2107a9bbe6441c78b99a1886a613070b1eb354`. |

## Residuales

- El fallo del full `npm test` puede ser flake/timeout de harness, pero la instruccion exige gatear por EXIT. Con exit 1 no es cerrable.
- La PII cruda en `file.text` puede estar pensada como raw upload fuera del dataset en el flujo de archivos; aun asi, para este AC la superficie es texto libre y la instruccion pide refutar que el submit gobernado vaya screened/redactado. Mi payload demuestra que el body front->server no va redactado en la fuente.

## Recomendacion

CAMBIO-REQUERIDO: devolver a Codex. Minimo: full `npm test` verde en clon limpio o hardening del harness que elimine los 502/SIGTERM; y aclarar/corregir la frontera de PII del modo necesidad para que el texto libre no viaje crudo en el submit gobernado si esa es la garantia buscada por SPEC-0095.
