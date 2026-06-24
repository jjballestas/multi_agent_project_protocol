---
handoff_id: HANDOFF-TASK-0172-codex-to-arquitecto-2
task_id: TASK-0172
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-24T17:10:00Z
product_commit: 9f1f772
code_repo: D:/Agentes/Zeus/Zeus-protocol
---

# TASK-0172 fix reentregado

## Cambio

- Producto `D:/Agentes/Zeus/Zeus-protocol` commit `9f1f772 fix(intake): redact public candidate model`.
- `normalizeStoredCandidate` ahora devuelve `title`, `narrative` y `acceptance_intent` redactados con
  `redactPublicText` cuando arma el modelo publico de candidatas.
- Las lecturas internas de aprobacion conservan el modelo no-redactado para no romper firma/provenance; la frontera
  publica (`/api/protocol/actions` y `/api/protocol/intake-candidates`) queda redactada antes de llegar al cliente.
- `redactPublicText` cubre telefono con parentesis y direcciones `Calle/Carrera/Av/Cra/Cl/Kr`, ademas de email y
  documento ya cubiertos.

## Evidencia producto

- `node --check src/server.js public/app.js tests/staticContract.test.js`: PASS.
- `git diff --check`: PASS.
- `node --test --test-name-pattern "candidate review" tests/staticContract.test.js`: PASS 2/2.
- `node --test --test-name-pattern "TASK-0172|candidate review" tests/staticContract.test.js`: PASS 8/8.
- `npm test`: PASS 81/81.
- Smoke local `PORT=4236`: `/healthz` OK, `/api/protocol/actions` OK con `candidateReview`.
- Clon limpio local: `npm test`: PASS 81/81.

## Nota de frontera

No se agrego ruta de escritura, emisor directo de `submit_intent`, cambio de gate PII ni activacion de file-intake.
La prueba permanente siembra candidata con email, telefono con parentesis, direccion y documento, y verifica que el
JSON publico de ambas APIs no contenga literales y si contenga marcadores redactados; el modal prellena desde ese
modelo publico.
