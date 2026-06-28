---
id: HANDOFF-TASK-0208-codex-to-arquitecto-1
task: TASK-0208
from: Codex
to: Arquitecto
date: 2026-06-28
status: in_review
product_repo: D:/Agentes/Zeus/Zeus-Aegis
product_commit: 777fa7c
---

# TASK-0208 handoff

Producto commit: `777fa7c test(f0): enforce governance waiver boundary`

Cambios:
- `docs/SEAMS.md` reemplaza el waiver blanket por tabla de 11 archivos, total 24 failed / 44 passed / 68, categoria por archivo, nota de independencia del panel y triggers de re-evaluacion.
- `vendor/hermes-2.3.0/scripts/zeus-aegis-f0-test.mjs` mantiene exactamente los 11 `excludedUpstreamFiles` y agrega comentario por archivo con categoria/razon.
- `vendor/hermes-2.3.0/src/server/governance-waiver.test.ts` queda dentro del F0 verde y falla si cualquier archivo del panel governance importa una superficie waiveada.

Guard fail-closed:
- Se forzo temporalmente `import '../lib/i18n'` en `src/routes/governance.tsx`.
- `corepack pnpm --dir vendor/hermes-2.3.0 exec vitest run src/server/governance-waiver.test.ts --maxWorkers=1` fallo con:
  `src/routes/governance.tsx imports ../lib/i18n (src/lib/i18n)`.
- Se revirtio el import forzado y el guard volvio a pasar.

Evidencia:
- `node --check vendor/hermes-2.3.0/scripts/zeus-aegis-f0-test.mjs`: PASS.
- `node --check vendor/hermes-2.3.0/server-entry.js`: PASS.
- Targeted guard actual: PASS, 1 file / 1 test.
- `npm test`: PASS, 82 files / 547 tests.
- `corepack pnpm --dir vendor/hermes-2.3.0 governance:smoke`: primer intento timeout; rerun inmediato PASS.
- `git diff --check`: PASS con solo warnings de normalizacion CRLF esperados.

Notas para review:
- No se arreglaron ni podaron los 24 fallos upstream, por alcance.
- La independencia documentada ahora esta respaldada por test de imports estaticos/dinamicos/re-export/require contra los archivos governance conocidos.
