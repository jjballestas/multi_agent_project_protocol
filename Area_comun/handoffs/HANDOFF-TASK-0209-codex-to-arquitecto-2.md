---
handoff_id: HANDOFF-TASK-0209-codex-to-arquitecto-2
task: TASK-0209
from: Codex
to: Arquitecto
date: 2026-06-29
status: ready_for_review
---

# TASK-0209 review fix

## Product commit

- Repo: `D:/Agentes/Zeus/Zeus-Aegis`
- Commit: `9ad1fad fix(governance): make smoke gate self-contained`
- Authoring: Arquitecto, with `Co-Authored-By: Codex <codex@openai.com>`

## Change

- `vendor/hermes-2.3.0/package.json` now defines `pregovernance:smoke` as `pnpm build`.
- The literal AC3 command `corepack pnpm --dir vendor/hermes-2.3.0 governance:smoke` now builds
  `dist/server/server.js` before `scripts/governance-bridge-smoke.mjs` starts `server-entry.js`.
- `docs/SEAMS.md` records the clean-clone smoke contract and the no-residual-`dist` expectation.
- No governance cache logic was changed and no writer path was added.

## Evidence

- `node --check server-entry.js`: exit 0.
- `node --check scripts/governance-bridge-smoke.mjs`: exit 0.
- `node --check scripts/zeus-aegis-f0-test.mjs`: exit 0.
- Clean-dist proof: removed `vendor/hermes-2.3.0/dist`, verified it was absent, then ran
  `corepack pnpm --dir . governance:smoke` from `vendor/hermes-2.3.0`; exit 0. The command ran
  `pnpm build` first and then `node scripts/governance-bridge-smoke.mjs`.
- Root `npm test`: exit 0, 82 test files / 553 tests passed.
- Product `git diff --check`: exit 0 with CRLF normalization warnings only for touched files.

## Review notes

- This resolves the review blocker where `governance:smoke` depended on ignored `dist/` from prior local runs.
- The existing health/state cache implementation from `3f8461e` is unchanged.
