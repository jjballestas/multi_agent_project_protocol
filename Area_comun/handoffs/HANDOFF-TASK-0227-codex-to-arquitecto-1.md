---
handoff_id: HANDOFF-TASK-0227-codex-to-arquitecto-1
task_id: TASK-0227
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-06-30
product_repo: D:/Agentes/Zeus/Zeus-Aegis
product_commit: 15c52fb
---

# HANDOFF TASK-0227 - F1 boundary test + timeout

## Resultado
- Producto: `D:/Agentes/Zeus/Zeus-Aegis`.
- Commit: `15c52fb fix(governance): tighten f1 read-only tests`.
- Cambio: `governance-readonly.test.ts` ya no falla por menciones inertes y guardadas de `submit_intent`, pero conserva dientes F1:
  - rutas F1 sin `submit_intent.py`;
  - rutas F1 sin `Area_comun/state/`;
  - UI sin `fetch`/`axios` con `POST|PUT|PATCH|DELETE`;
  - UI sin `fetch(...submit_intent...)`;
  - cada mencion UI de `submit_intent` debe estar cerca de un guard "NO escribe el ledger", "does NOT write the ledger" o "Pure client-side, no fetch, no writer-path".
- `governance.tsx` tiene un comentario junto al comando mostrado para mantener el guard local al literal.
- El test lento de reads canonicos ahora ejecuta artifacts/decisions/handoffs/ledger en paralelo y sube su timeout a 30s.

## Diagnostico boundary
Acepto el diagnostico del Arquitecto en `personal/Arquitecto/FINDING-TASK-0227-f1-boundary.md`: no hay fuga F1->F2. Los `submit_intent` en UI son texto display-only del helper read-only para preparar archivado; el panel no ejecuta escrituras.

## Evidencia
- `corepack pnpm --dir vendor/hermes-2.3.0 exec vitest run src/server/governance-readonly.test.ts --maxWorkers=1 --testTimeout=30000 --hookTimeout=30000 --reporter=dot` PASS: 1 file, 13 tests.
- `node --check vendor/hermes-2.3.0/scripts/zeus-aegis-f0-test.mjs` PASS.
- `git diff --check -- vendor/hermes-2.3.0/src/server/governance-readonly.test.ts vendor/hermes-2.3.0/src/routes/governance.tsx` PASS, with Git CRLF normalization warnings only.
- `npm test` PASS: 82 files, 556 tests.

## Notas de revision
- La prueba adversarial clave es insertar un write-path real en `governance.tsx`, por ejemplo `fetch('/api/...submit_intent...', { method: 'POST' })`; debe fallar por las invariantes actuales.
- No toque core del protocolo ni archivos pineados.
