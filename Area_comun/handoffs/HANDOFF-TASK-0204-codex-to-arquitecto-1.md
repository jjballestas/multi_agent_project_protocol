---
handoff_id: HANDOFF-TASK-0204-codex-to-arquitecto-1
task_id: TASK-0204
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-06-27T23:10:00Z
product_repo: D:/Agentes/Zeus/Zeus-Aegis
product_commit: 8c29b58
---

# HANDOFF TASK-0204 - Zeus-Aegis F3 read-only

## Entrega

- Producto: `D:/Agentes/Zeus/Zeus-Aegis`.
- Commit: `8c29b58 feat(governance): add f3 read-only dashboard`.
- Autor: Arquitecto. Co-authored-by: Codex.

## Cambios

- Endpoint read-only `/api/governance/projects`: deriva proyectos desde `TASK_INDEX.json`, devuelve entidades `id/kind/label` sin rutas de disco crudas.
- Endpoint read-only `/api/governance/metrics`: deriva conteos desde estado/ledger canonico: tareas por estado, metodos de firma de evento/actor, firmantes, drift, validator y salud no-verde si validator/drift no estan verdes.
- UI `/governance`: selector multi-proyecto que filtra Backlog/Artifacts y dashboard de metricas read-only.
- Denylist F1 queda intacta y extendida con los endpoints nuevos; no se agregan rutas de escritura ni superficie `submit_intent`.

## Evidencia

- `node --check vendor/hermes-2.3.0/server-entry.js`: PASS.
- `node --check vendor/hermes-2.3.0/scripts/zeus-aegis-f0-test.mjs`: PASS.
- `corepack pnpm --dir vendor/hermes-2.3.0 exec vitest run src/server/governance-readonly.test.ts --maxWorkers=1 --testTimeout=30000 --hookTimeout=30000`: PASS, 9/9.
- `corepack pnpm --dir vendor/hermes-2.3.0 build`: PASS.
- `npm test`: PASS, 80 files / 542 tests.
- Smoke local `PORT=4312 HOST=127.0.0.1 node server-entry.js`: HTTP 200 para `/api/governance/projects`, `/api/governance/metrics?project=zeus-aegis` y `/governance`.
- `git diff --check`: PASS con solo warnings de normalizacion CRLF.

## Caveats

- El build conserva warnings preexistentes de chunk size, sourcemap del plugin `client-process-env`, dynamic imports mixtos y entorno Hermes gateway/token ausente en tests; no bloquean F0.
