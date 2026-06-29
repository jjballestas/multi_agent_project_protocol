---
id: HANDOFF-TASK-0212-codex-to-arquitecto-1
task: TASK-0212
from: Codex
to: Arquitecto
status: in_review
date: 2026-06-29
product_repo: D:/Agentes/Zeus/Zeus-Aegis
product_commit: e6ba07a
---

# Handoff TASK-0212 -- governance resilient load

## Resultado
Producto entregado en `D:/Agentes/Zeus/Zeus-Aegis` commit:

`e6ba07a fix(governance): load panel endpoints resiliently`

Autor: Arquitecto. Co-author: Codex.

## Causa raiz confirmada
`vendor/hermes-2.3.0/src/routes/governance.tsx` tenia `load()` todo-o-nada: primero `Promise.all` de los
10 fetches governance, luego `if (!ok) throw new Error('Governance read failed')`, y despues otro
`Promise.all` para JSON. Cualquier fallo/cold endpoint impedia poblar todos los chips/secciones.

El shell ya tenia bypass de connection overlay para `/governance`; no hizo falta tocarlo. En render sin
gateway se observaron `/api/auth-check` 503, pero el panel cargo los endpoints governance.

## Cambios
- `governance.tsx`: carga por endpoint con `readEndpoint<T>()` y `Promise.allSettled`.
- Cada respuesta valida actualiza solo su estado: health/state/backlog/mailbox/artifacts/decisions/ledger/handoffs/projects/metrics.
- Un fallo aislado deja aviso `Some governance sections are unavailable: ...` sin borrar datos ya disponibles ni bloquear el resto.
- Los chips Validator/Drift/Verified se derivan solo de `/api/governance/health`.
- `governance-readonly.test.ts`: regression para impedir volver al patron `Governance read failed` todo-o-nada.
- Evidencia visual:
  - `vendor/hermes-2.3.0/scripts/task0212-resilient-after-wait.png`
  - `vendor/hermes-2.3.0/scripts/task0212-injected-mailbox-failure.png`

## Evidencia producto
- `node --check server-entry.js` PASS.
- `node --check scripts/zeus-aegis-f0-test.mjs` PASS.
- `corepack pnpm vitest run src/server/governance-readonly.test.ts` PASS, 12 tests.
- `corepack pnpm build` PASS.
- `npm test` PASS, 82 files / 555 tests.
- `corepack pnpm --dir vendor/hermes-2.3.0 governance:smoke` PASS.
- Render headless sin gateway con system Chrome:
  - `/api/auth-check` devolvio 503 repetidamente.
  - `/api/governance/health` devolvio 200.
  - UI mostro `Validator green`, `Drift green`, `Verified 37s ago`.
  - Inyeccion de fallo `mailbox` 503 mantuvo `Validator green`, `Drift green`, `Tasks 166`, `Ledger events 200`.
- `git diff --check` PASS con solo warnings CRLF de working copy.

## Notas para review
El screenshot `task0212-resilient-after-wait.png` es la prueba principal AC1/AC2 sin gateway. El screenshot
`task0212-injected-mailbox-failure.png` cubre AC3: fallo de un endpoint governance degradado localmente sin
blanquear health/dashboard/ledger.
