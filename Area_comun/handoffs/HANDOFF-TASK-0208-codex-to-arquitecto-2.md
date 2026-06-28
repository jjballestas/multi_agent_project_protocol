---
id: HANDOFF-TASK-0208-codex-to-arquitecto-2
task: TASK-0208
from: Codex
to: Arquitecto
date: 2026-06-28
status: in_review
product_repo: D:/Agentes/Zeus/Zeus-Aegis
product_commit: b47b707
---

# TASK-0208 review fix handoff

Producto: `D:/Agentes/Zeus/Zeus-Aegis@b47b707` (`test(f0): harden waiver guard transitively`).

## Cambios

- `src/server/governance-waiver.test.ts` ahora recorre el grafo de imports first-party desde los 13 entrypoints governance. Corta en imports bare externos y falla si cualquier modulo alcanzable resuelve a una superficie waiveada por import directo, alias `@/`, `src/`, dynamic import, `require`, barrel/re-export o transitive.
- El vector del Analista queda como regresion sintetica: `governance.tsx -> governance-waiver-transitive.ts -> ../lib/i18n` produce violacion.
- `docs/SEAMS.md` reclasifica superficies servidas como no certificadas por F0 y `fix-or-prune`, sin afirmar inocuidad de producto. `chat-message-list` queda como `served-product: 1 UI-behavior + 2 API/export-missing`.
- `scripts/zeus-aegis-f0-test.mjs` mantiene exactamente los mismos 11 excludes y actualiza los comentarios por superficie.

## Evidencia

- `node --check server-entry.js`: PASS.
- `node --check scripts/zeus-aegis-f0-test.mjs`: PASS.
- `corepack pnpm exec vitest run src/server/governance-waiver.test.ts --maxWorkers=1 --testTimeout=30000 --hookTimeout=30000`: PASS, 2 tests.
- Fail-closed real: se anadio temporalmente `src/routes/governance-waiver-transitive.ts` con `import '../lib/i18n'` y `src/routes/governance.tsx` importo ese modulo; el guard fallo con `src/routes/governance-waiver-transitive.ts reaches ../lib/i18n (src/lib/i18n)`. Se revirtio el probe y el guard volvio a PASS.
- `npm test`: primer intento fallo por `ERR_IPC_CHANNEL_CLOSED` de Vitest tras muchos tests; rerun inmediato PASS, 82 files / 548 tests.
- `corepack pnpm --dir vendor/hermes-2.3.0 governance:smoke`: PASS.
- `git diff --check`: PASS, solo warnings CRLF esperados.

## Protocolo

- `python scripts/scan_encoding.py --root .`: PASS.
- `python scripts/scan_domain_neutrality.py --root .`: PASS.
- `python scripts/validate_collaboration_state.py --root .`: PASS con warning preexistente de mailbox compacto TASK-0193.
- Drift #4: `has_drift=false`, `up_to_seq=2410` antes de la entrega.

Pendiente checker/adversarial: revisar `b47b707` y volver a pasar Analista sobre la refutacion sostenida.
