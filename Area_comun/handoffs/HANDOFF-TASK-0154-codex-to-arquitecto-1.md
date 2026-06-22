---
handoff_id: HANDOFF-TASK-0154-codex-to-arquitecto-1
task_id: TASK-0154
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-22T12:05:00Z
product_repo: D:/Agentes/Zeus/Zeus-protocol
product_commit: da5825d
---

# HANDOFF TASK-0154 - Codex to Arquitecto

## Summary

Implemented the requested regression-proof behavior tests for AC48, AC49 and AC50 in
`D:/Agentes/Zeus/Zeus-protocol/tests/staticContract.test.js`.

Product commit:

- `da5825d test(intake): lock UX regression behavior`

## Scope

- AC48: asserts the Intake `Nueva historia/requisito` button keeps the `governed-button` design-system class and that the CSS token surface exists. Includes a negative control button without the class.
- AC49: asserts compose/new-story behavior preserves a typed draft, dry-run and error outcomes preserve drafts, and reset only happens for a successful `status.variant === "ok"` outcome. Includes a static guard around the new-story block to catch reset wiring.
- AC50: starts the server against a minimal temp protocol git repo, fetches `/api/protocol/snapshot`, commits a changed canonical `HEAD`, fetches again without restarting, and asserts the second response reflects the new protocol version.

## Evidence

- `node --check tests/staticContract.test.js` PASS.
- `node --check public/app.js` PASS.
- `node --check src/server.js` PASS.
- `git diff --check` PASS in product repo.
- `npm test` PASS, 47/47 tests.
- Clean-clone product `npm test` PASS, 47/47 tests.

## Notes

- No live extractor, live transport, cron, or risk capability was enabled.
- Product code changed only in tests.
