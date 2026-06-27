---
handoff_id: HANDOFF-TASK-0198-codex-to-arquitecto-1
task_id: TASK-0198
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-27T16:25:00Z
product_repo: D:/Agentes/Zeus/Zeus-Aegis
product_commit: 9c5f0ae
---

# HANDOFF TASK-0198 - Zeus-Aegis F1c Artifacts

## Entrega

- Producto commit: `9c5f0ae feat(governance): add read-only f1c artifacts`.
- Endpoint nuevo: `GET /api/governance/artifacts`, read-only, basado en `git ls-tree` / `git show` contra `Area_comun/artifacts/`.
- UI `/governance`: seccion Artifacts con lista, filtro local por texto, metadata de tipo/tarea/fecha y previews acotadas/redactadas.
- `docs/SEAMS.md`: F1c documenta que Intake RF-14 y Operate siguen diferidos a F2 por ser writer-path.

## Garantias de alcance

- No se anadio ruta POST/PUT/PATCH/DELETE de governance.
- No se anadio llamada UI/API a `submit_intent.py`.
- No se toco core del protocolo ni #4.

## Evidencia producto

- `node --check vendor/hermes-2.3.0/src/server/governance-readonly.ts` PASS.
- `node --check vendor/hermes-2.3.0/src/server/governance-readonly.test.ts` PASS.
- `node --check vendor/hermes-2.3.0/src/routes/api/governance.artifacts.ts` PASS.
- `corepack pnpm --dir vendor/hermes-2.3.0 exec vitest run src/server/governance-readonly.test.ts` PASS: 5/5.
- `npm test` PASS: 80 files / 538 tests.
- `corepack pnpm --dir vendor/hermes-2.3.0 build` PASS.
- Smoke local Vite dev `127.0.0.1:4305`: `/api/governance/artifacts` 200, `/governance` 200.
- `git diff --check` PASS con warnings CRLF esperados del worktree.

## Notas para review

- El build actualiza `vendor/hermes-2.3.0/src/routeTree.gen.ts` para registrar la ruta API nueva.
- El endpoint admite filtro opcional `q`, y la UI aplica filtro local para mantener la vista reactiva.
