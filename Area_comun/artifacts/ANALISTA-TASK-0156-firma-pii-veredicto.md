# ANALISTA - Veredicto TASK-0156 firma/PII

Firma: Analista

## Veredicto

OK -> CERRABLE.

Ancla canonica revisada:

- Producto Zeus-protocol: `560a226150a2b6237bbf00a84fd6dca07504ba09`.
- Protocolo: `f4eb93b36f4e04d4a0aa2889271a25e66307791d`.
- Instruccion de review: `Area_comun/mailbox/open/MSG-20260622-Arquitecto-to-Analista-REVISAR-TASK-0156.md`.

No encontre escape bloqueante en la firma Ed25519 de candidatas, en el registro de worker fuera del config #4,
en la proteccion de la clave privada default, ni en el carry off-by-default/PII/local-vlm.

## Reproduccion

| Gate | Evidencia | Exit |
| --- | --- | --- |
| Producto clean clone | `git clone D:/Agentes/Zeus/Zeus-protocol` a `C:/Users/johnb/AppData/Local/Temp/zeus-review-0156-30d01dd658c3404b8e72b27129ec5358`, checkout `560a226150a2b6237bbf00a84fd6dca07504ba09` | 0 |
| Producto tests | `npm test` en clon limpio: 48/48 pass | 0 |
| Payloads propios firma | servidor del producto contra store/config temporales; valid=200, missing_signature=409, bad_signature_bytes=409, bad_payload_hash=409, worker_id_mismatch=409, algorithm_mismatch=409, stored_payload_tamper=409, attacker_key_in_signature_field=409 | 0 |
| Protocolo validate con secretos | `python scripts/validate_collaboration_state.py` en repo vivo: OK, warning no bloqueante de mensaje FYI abierto a Operador | 0 |
| Protocolo validate sin secretos | clon limpio del protocolo en `C:/Users/johnb/AppData/Local/Temp/protocol-nosecrets-0156-f811b04f1e444eda84deb0addbd7f9c5`: OK, mismo warning no bloqueante | 0 |
| Drift #4 | `protocol_state_drift`: `has_drift=false`, `up_to_seq=1213`, hot_hash=replay_hash=`7f13177483f46479760b757ce23db446bbd81f248c79c4bf955ed4c474722a51` | 0 |
| Neutralidad | `python scripts/scan_domain_neutrality.py` | 0 |
| Encoding | `python scripts/scan_encoding.py`: clean | 0 |
| #4 byte-identica | `git diff -- protocol.config.json chain_manifest.json secrets Area_comun/state` sin salida; hash observado `protocol.config.json` empieza `2E35F26E...`, `chain_manifest.json` empieza `030F2FA6...` | 0 |

## Tabla vector por vector

| Vector | Resultado | Prueba adversarial |
| --- | --- | --- |
| Firma Ed25519 valida | PASA | Una candidata firmada con el keypair del worker `Extractor` devuelve 200 en `mode=dry_run`; la firma cubre id, texto, proyecto, hashes, task, fecha de creacion y worker. |
| Firma ausente | PASA | `extractor_signature=null` devuelve 409 `candidate extractor signature is invalid`. |
| Firma bytes alterados | PASA | Flip binario del primer byte de la firma base64 devuelve 409. |
| Hash de payload alterado | PASA | `payload_sha256=000...` devuelve 409 antes de construir intake. |
| Worker mismatch | PASA | `extractor_signature.worker_id=Other` devuelve 409. |
| Algoritmo mismatch | PASA | `algorithm=ECDSA` devuelve 409. |
| Payload almacenado alterado tras firmar | PASA | Cambio de `narrative` en el JSON del store devuelve 409. |
| Public key inyectada por atacante en la firma | PASA | Candidata firmada con keypair atacante y `public_key_pem` atacante devuelve 409; el server verifica contra el public key del registro, no contra el campo autodeclarado. |
| Registro de workers fuera del config #4 | PASA | El commit de producto toca solo `.gitignore`, `extractors.config.json`, `src/server.js`, `tests/staticContract.test.js`; `protocol.config.json` del protocolo no contiene `Extractor`, `qwen3-vl` ni `local-vlm`; #4 sin diff. |
| Extractor no firmante del ledger #4 | PASA | No aparece en `protocol.config.json`; el registro esta en `extractors.config.json` del producto. |
| Clave privada no commiteada | PASA | `git ls-files` solo lista `extractors.config.json`; `git grep` no encuentra private key PEM commiteada. La ruta default `.secrets/extractor_ed25519_private.pem` esta cubierta por `.gitignore`. |
| Default provider/model | PASA | Registro de producto: provider `local-vlm`, default `qwen3-vl:4b-instruct`, endpoint `http://127.0.0.1:11434/api/chat`. Tests confirman que las llamadas local-vlm usan ese modelo. |
| Carry AC51/52/53 | PASA | Suite limpia conserva loopback-only, chunking, no-ledger, PII gate y robustez local-vlm. |
| Candidatas no-ledger + PII gate | PASA | La aprobacion exige `piiReviewed=true`, re-screen del texto editado, firma valida y store fuera del ledger; suite 48/48 y payloads propios cubren rechazo antes de intake gobernado. |
| Off-by-default | PASA | `file-ingestion.config.json` versionado mantiene `fileIngestion.enabled=false`; `extractor.enabled` no queda activado por defecto. |

## Residuales declarados

- No es un sandbox de red ni una prueba de uso vivo del VLM. El uso vivo sigue siendo GO aparte con pasada corta
  sobre la config viva antes del flip.
- La ruta privada default del producto es `.secrets/extractor_ed25519_private.pem` y esta gitignored. No use
  `secrets/` ni `.protocol-secrets/` como rutas de producto en esta pasada; si el operador decide mover la
  privada a esas rutas, deben anadirse al `.gitignore` del producto antes de colocar la clave.

## Recomendacion

CERRABLE. TASK-0156 puede cerrarse con este OK del Analista.
