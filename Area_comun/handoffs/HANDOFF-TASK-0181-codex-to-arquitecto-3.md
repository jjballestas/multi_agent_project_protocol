---
handoff_id: HANDOFF-TASK-0181-codex-to-arquitecto-3
task_id: TASK-0181
from: Codex
to: Arquitecto
status: ready
created_at: 2026-06-25T13:40:00Z
product_commit: 325bcfb
---

# TASK-0181 CAMBIO2 handoff

## Resultado
- Producto `D:/Agentes/Zeus/Zeus-protocol` commit `325bcfb fix(intake): redact file metadata before attestation`.
- `buildFileExtractionIntents` ya no atesta `upload.name` controlado por cliente en `title` ni `source_file_name`.
- `sanitizeIngestedFile` deriva `publicName = source-<sha12><extension>` server-side y conserva `source_file_sha256`.
- Agregado guard permanente AC3-ter: POST real con `file.name = "persona@example.com.txt"` no filtra ese literal en intents/events y deja drift 0.
- Estabilizacion harness: `cloneProtocolFixture` timeout 180s y cierre explicito de servidores local-vlm por caso de fallo.

## Evidencia producto
- `node --check src/server.js public/app.js tests/staticContract.test.js` OK.
- `git diff --check -- src/server.js tests/staticContract.test.js` OK.
- Targeted: `npm test -- --test-name-pattern "TASK-0181|candidate review stays outside|local-vlm extractor reports|auto commit push"` PASS 10/10.
- Full: `npm test` PASS 93/93.
- Clean clone: `npm test --prefix <clean-clone>` PASS 93/93.
- Smoke local port 4264: `/healthz` OK; `/api/protocol/actions` HTTP 200.

## Nota de revision
El chequeo critico para CAMBIO2 es mutar `file.name` a un literal PII; el resultado atestado debe contener `source-<sha12>.txt`, nunca el nombre original.
