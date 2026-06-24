# HANDOFF TASK-0171 - Codex -> Arquitecto

## Estado

- TASK-0171 queda listo para review de Arquitecto.
- Repo producto: `D:/Agentes/Zeus/Zeus-protocol`.
- Commit producto: `f6dc8a5 feat(front): register product workers`.
- Maker: Codex. Checker: Arquitecto.

## Implementacion

- `src/server.js` agrega `/api/protocol/product-workers/register` con `dry_run` y `execute`.
- El alta escribe solo en el override gitignored `extractors.runtime.json`.
- La clave privada se genera server-side en `.secrets/workers/<worker>_ed25519_private.pem`; solo `publicKeyPem`
  entra al registro y a la respuesta.
- `loadProductWorkers()` ahora carga el master versionado y superpone el override runtime.
- El worker nace `enabled:false` y declara `liveUseRequires: "file-ingestion gate"`.
- La accion aparece en el roster de acciones como `product-worker-register` / RF-9 con descripcion en el front.

## Fronteras Verificadas

- No se toca `protocol.config.json`, `agent_registry`, `signature_config`, genesis ni firmantes.
- El endpoint no llama `runtime/submit_intent.py`.
- Behavior-test AC4 compara hashes byte a byte de:
  - `protocol.config.json`
  - `runtime/state/events.jsonl`
  - `runtime/state/snapshot.json`
- Validacion estricta AC5:
  - campos `typeof string` obligatorios;
  - arrays/objects/numeros -> 400;
  - id inseguro/path traversal -> 400;
  - id duplicado -> 400;
  - clave extra -> 400;
  - endpoint no-loopback -> 400;
  - rechazos invalidos no crean `extractors.runtime.json`.

## Evidencia Producto

- `node --check src/server.js` OK.
- `node --check public/app.js` OK.
- `node --check tests/staticContract.test.js` OK.
- `git diff --check` OK.
- `node --test --test-name-pattern "TASK-0171" tests/staticContract.test.js` PASS 2/2.
- `npm test` PASS 74/74 tras rerun; primer intento agoto timeout local a 244s.
- Clean-clone `npm test` PASS 74/74.
- Smoke local puerto 4230:
  - `/healthz` OK.
  - `/api/protocol/observe` OK.

## Notas Para Review

- La capacidad de registrar worker no habilita uso vivo; sigue dependiendo del gate de file-ingestion existente.
- La privada no se commitea ni se devuelve al cliente.
- El registro runtime y `.secrets/` ya estan cubiertos por `.gitignore`.
