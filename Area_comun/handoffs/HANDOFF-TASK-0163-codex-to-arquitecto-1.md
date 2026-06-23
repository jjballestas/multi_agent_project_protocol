# HANDOFF TASK-0163 - Codex to Arquitecto

## Estado

- Tarea: TASK-0163
- Estado propuesto: in_review
- Producto: D:/Agentes/Zeus/Zeus-protocol
- Commit producto: d1de0c1 fix(intake): sanitize ledger busy errors
- Maker: Codex
- Checker: Arquitecto + Analista

## Cambios

- `src/server.js` ahora captura fallos del CLI `submit_intent` y convierte contencion de ledger/claim en respuesta tipada y saneada:
  `{ error: "ledger-busy", code: "ledger-busy", retryable: true }` con HTTP 409.
- `src/server.js` no expone argv, `--intents-json`, comando ni traceback en el cuerpo de errores de `submit_intent`; otros fallos CLI salen como `submit_intent failed`.
- `public/app.js` mapea `ledger-busy` a `Canal ocupado, intente mas tarde` para:
  requirement-intake, escritura previa de file extraction, y aprobacion de candidata.
- `tests/staticContract.test.js` agrega AC72: helper front friendly-error y repro de contencion en clon desechable con claim activo.

## Evidencia

- `node --check src/server.js` PASS.
- `node --check public/app.js` PASS.
- `node --check tests/staticContract.test.js` PASS.
- `git diff --check` PASS en producto.
- `npm test` PASS 57/57 en producto.
- Smoke local `PORT=4201 node src/server.js`: `/healthz` + `/api/protocol/observe` OK.
- Clean-clone Zeus `npm test` PASS 57/57.
- Protocolo antes de delivery: encoding OK, neutrality OK, `validate_collaboration_state.py` OK, drift false up_to_seq 1382.

## Notas

- Hubo un primer smoke fallido por no inyectar `PORT` al proceso; rerun con `PORT=4201` paso.
- Hubo una primera corrida clean-clone con flake de readiness en `local-vlm extractor is loopback-only, chunked, robust, and non-ledger`; rerun clean-clone completo paso 57/57.
- No se cambio la semantica de serializacion del ledger ni el grano de claims.
- `protocol.config.json` no fue tocado.
