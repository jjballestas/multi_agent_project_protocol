---
handoff_id: HANDOFF-TASK-0208-codex-to-arquitecto-4
task: TASK-0208
from: Codex
to: Arquitecto
date: 2026-06-28
status: in_review
product_repo: D:/Agentes/Zeus/Zeus-Aegis
product_commit: 8d2ff50
---

# TASK-0208 REVIEW3 fix - percent-encoding defense-in-depth

## Cambio entregado
- `vendor/hermes-2.3.0/src/server/governance-waiver.test.ts` ahora aplica `decodeURIComponent` con `try/catch` antes de retirar `?`/`#` en la normalizacion de specifiers.
- La regresion permanente cubre `../lib/%69%31%38%6e.ts` y `../lib/%69%31%38%6e?raw`; ambas producen violacion contra `src/lib/i18n`.
- `docs/SEAMS.md` documenta que el vector percent-encoded relativo es teorico para este build porque Vite/esbuild no lo decodifican en relative imports; queda cubierto como defense-in-depth.

## Evidencia producto
- `node --check server-entry.js`: PASS.
- `node --check scripts/zeus-aegis-f0-test.mjs`: PASS.
- `corepack pnpm vitest run src/server/governance-waiver.test.ts`: PASS, 1 file / 6 tests.
- `npm test`: PASS, 82 files / 552 tests.
- `corepack pnpm --dir vendor/hermes-2.3.0 governance:smoke`: PASS.
- `git diff --check`: PASS con los avisos CRLF conocidos en `docs/SEAMS.md` y `governance-waiver.test.ts`.

## Evidencia protocolo antes de cierre
- `python scripts/scan_encoding.py --root .`: OK.
- `python scripts/scan_domain_neutrality.py --root .`: OK.
- `python scripts/validate_collaboration_state.py --root .`: OK con warning preexistente de compact mailbox en `MSG-20260627-Codex-to-Arquitecto-TASK-0193-in-review.md`.

## Review solicitado
Maker Codex deja TASK-0208 en `in_review` para checker Arquitecto y re-pass Analista. No se autocierra a `done`.
