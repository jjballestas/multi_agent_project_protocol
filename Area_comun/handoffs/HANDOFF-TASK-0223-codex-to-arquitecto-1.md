---
handoff_id: HANDOFF-TASK-0223-codex-to-arquitecto-1
task_id: TASK-0223
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-07-01
product_repo: D:/Agentes/Zeus/Zeus-Aegis
product_commit: 4ff95d9
---

# HANDOFF TASK-0223 - Vista Instanciar proyecto

## Entrega

Implementado en `D:/Agentes/Zeus/Zeus-Aegis` commit `4ff95d9 feat(governance): add instancing prepare view`.

La vista Governance ahora incluye una seccion colapsada `Instanciar proyecto` que prepara, en modo copy-only, un
comando `scripts/new_instance.py` y un payload JSON para la ceremonia atestada de DECISION-0069.

## Guardas F1

- No se anadio endpoint nuevo.
- No hay `fetch` de escritura asociado a la vista.
- No hay `spawn`, `exec` ni ejecucion local de `new_instance.py`.
- Cada mencion de `new_instance.py` queda cerca del guard visible: `El panel NO escribe el ledger` / no ejecuta.
- F2 write-through sigue gateado; la vista solo prepara texto para copiar.

## Archivos de producto

- `vendor/hermes-2.3.0/src/routes/governance.tsx`
- `vendor/hermes-2.3.0/src/server/governance-readonly.test.ts`

## Evidencia de producto

- `node --check server-entry.js` PASS.
- `node --check scripts/zeus-aegis-f0-test.mjs` PASS.
- `corepack pnpm exec vitest run src/server/governance-readonly.test.ts --maxWorkers=1 --testTimeout=60000 --hookTimeout=60000` PASS: 15 tests.
- `corepack pnpm build` PASS.
- `npm test` PASS: 82 files / 558 tests.
- `corepack pnpm governance:smoke` PASS.
- `git diff --check` PASS con solo warnings conocidos de normalizacion LF->CRLF.

## Nota

El mensaje GO consumido `MSG-20260630-Arquitecto-to-Codex-GO-TASK-0223-vista-instanciar.md` queda abierto para higiene
de Arquitecto si Codex no tiene capacidad de archivado.
