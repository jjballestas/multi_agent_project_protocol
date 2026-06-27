---
handoff_id: HANDOFF-TASK-0205-codex-to-arquitecto-1
task_id: TASK-0205
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-06-27T21:30:00Z
product_repo: D:/Agentes/Zeus/Zeus-Aegis
product_commit: d83a08e
---

# Handoff TASK-0205 - Zeus-Aegis F4a security hardening

## Entrega

- Product commit: `d83a08e fix(governance): harden read-only endpoints`
- Repo: `D:/Agentes/Zeus/Zeus-Aegis`
- Autor: Arquitecto; coautor: Codex.

## Cambios

- `/api/governance/*` ahora exige `Authorization: Bearer <token>` si existe `GOVERNANCE_API_TOKEN` o `HERMES_API_TOKEN`.
- Sin token configurado conserva modo local abierto, documentado en `docs/SEAMS.md`.
- El entrypoint rechaza metodos no read-only en governance con `405`.
- El entrypoint rechaza parametros de query inseguros (`..`, rutas absolutas, drive paths Windows, backslashes, caracteres no admitidos) antes de llegar a las rutas.
- `governance-readonly.ts` valida `ZEUS_AEGIS_PROTOCOL_REF`, rutas canonicas y filtros derivados de query antes de `git show` / `git ls-tree`.
- Rate-limit basico por cliente/token en governance con `GOVERNANCE_RATE_LIMIT` y `GOVERNANCE_RATE_LIMIT_WINDOW_MS`.
- Tests nuevos en `src/server/governance-security.test.ts`: auth, path/ref/query guard, rate-limit, e2e del puente.

## Evidencia producto

- `node --check server-entry.js`: PASS.
- `node --check scripts/zeus-aegis-f0-test.mjs`: PASS.
- `corepack pnpm exec vitest run src/server/governance-security.test.ts src/server/governance-readonly.test.ts --maxWorkers=1 --testTimeout=60000 --hookTimeout=30000`: PASS.
- `npm test` desde raiz Zeus-Aegis: PASS.
- `git diff --check`: PASS con solo warnings CRLF esperados.

## Notas

- F2 sigue gateado; no se agrego superficie de escritura.
- Los avisos de test sobre `hermes-agent`, gateway local y `act(...)` son ruido preexistente del upstream/F0; el exit code fue 0.
