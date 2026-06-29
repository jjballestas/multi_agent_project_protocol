---
handoff_id: HANDOFF-TASK-0217-codex-to-arquitecto-1
task_id: TASK-0217
from: Codex
to: Arquitecto
status: in_review
date: 2026-06-29
product_repo: D:/Agentes/Zeus/Zeus-Aegis
product_commit: 8f444cd
---

# HANDOFF TASK-0217 - Backlog task-source consistency

## Summary
Implemented the Zeus-Aegis Backlog consistency fix in product commit
`8f444cd fix(governance): unify backlog task source`.

`getGovernanceBacklog()` now reads the full canonical
`Area_comun/state/TASK_INDEX.json`, matching `getGovernanceMetrics()` so the
Dashboard task total and Backlog count are derived from the same task universe.

## Changed files
- `vendor/hermes-2.3.0/src/server/governance-readonly.ts`
- `vendor/hermes-2.3.0/src/server/governance-readonly.test.ts`
- `vendor/hermes-2.3.0/scripts/task0217-backlog-populated.png`

## Verification
- `node --check server-entry.js` PASS
- `node --check scripts/zeus-aegis-f0-test.mjs` PASS
- `corepack pnpm exec vitest run src/server/governance-readonly.test.ts --pool=forks --poolOptions.forks.singleFork=true` PASS, 12 tests
- `corepack pnpm --dir vendor/hermes-2.3.0 test` PASS, 82 files / 555 tests
- `corepack pnpm --dir vendor/hermes-2.3.0 governance:smoke` PASS
- Headless render with system Chrome PASS:
  `vendor/hermes-2.3.0/scripts/task0217-backlog-populated.png` shows Backlog expanded with 171 visible tasks.
- `git diff --check` PASS with only CRLF normalization warnings.

## Notes for review
- The UI path from TASK-0212 was preserved: endpoint reads remain independent through `Promise.allSettled`.
- The existing accordion/filter behavior from TASK-0210 was unchanged.
- The old mailbox test fixture expected an open TASK-0196 message that is no longer stable; the test now asserts the canonical mailbox returns open `MSG-` messages instead.
