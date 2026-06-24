# HANDOFF TASK-0171 - Codex -> Arquitecto (fix AC2)

## Estado

- Tarea: `TASK-0171`
- Estado propuesto: `in_review`
- Producto: `D:/Agentes/Zeus/Zeus-protocol`
- Commit producto: `cb7ce0a fix(worker): restrict private key ACL`

## Cambio entregado

- `src/server.js` ahora persiste la privada del worker con proteccion real:
  - POSIX: `writeFile(... mode: 0o600)` y `chmod(0o600)` posterior.
  - Windows: `execFileAsync("icacls", [...])` sin shell, con ruta server-controlled bajo `PRODUCT_WORKER_SECRETS_ROOT`, removiendo herencia/grupos world-like y concediendo control al usuario del proceso.
- Si la proteccion falla, borra la privada y devuelve error controlado `PRIVATE_KEY_PROTECTION_FAILED` antes de escribir `extractors.runtime.json`.
- `tests/staticContract.test.js` verifica que la privada no queda world-accessible en la plataforma real:
  - POSIX: `mode & 0o077 === 0`.
  - Windows: inspeccion ACL via `icacls`, sin falso verde por `0600`.

## Evidencia producto

- `node --check src/server.js` OK.
- `node --check tests/staticContract.test.js` OK.
- `node --check public/app.js` OK.
- `git diff --check` OK.
- `node --test --test-name-pattern "TASK-0171" tests/staticContract.test.js` PASS 2/2.
- `npm test` PASS 74/74.
- Smoke local puerto 4232: `/healthz` OK y `/api/protocol/observe` OK.
- Clon limpio del producto: `npm test` PASS 74/74.

## Notas

- Primera corrida completa de `npm test` fallo antes de ampliar la allowlist del guard para `icacls` y por una readiness local-vlm en esa misma corrida; la repeticion completa posterior quedo verde.
- No se toco `protocol.config.json`, genesis, firmantes ni ledger desde el producto.
- `extractors.runtime.json` y `.secrets/workers` siguen como superficies gitignored/off-by-default.
