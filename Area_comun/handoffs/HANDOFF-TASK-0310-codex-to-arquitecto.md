---
task_id: TASK-0310
from: Codex
to: Arquitecto
status: in_review
product_repo: D:/Agentes/Zeus/Zeus-protocol
product_commit: 767f41f0074e4497cc9dfe7ca9dbcc63d68d1c40
created: 2026-08-02T12:52:10Z
---

# HANDOFF TASK-0310 - operator prompt console

## Delivered

- Product commit `767f41f` is pushed to `origin/main` in Zeus-protocol.
- The existing prompt console is now gated by `operatorPrompt.enabled: false` in
  `commit-push.config.json`, outside the pinned protocol config. The server endpoint is inert while off.
- An enabled execute additionally requires auto-commit-push readiness. The server remains the only builder:
  it accepts only Arquitecto, Codex, or Analista and only the bounded operator prompt shape.
- Canonical output uses REQUEST or QUESTION, `from: Operador`, `relayed_by: Arquitecto`,
  `endorsement: none`, `operator_directive: true`, ASCII output, structural PII redaction, and a complete
  response contract when requested.
- The UI runs dry_run preview before explicit browser confirmation, warns about public PII, and retains a
  read-only open/answered/archived thread filtered by agent.

## Permanent negative evidence

`TASK-0310 prompt endpoint rejects impersonation and previews only a server-built canonical message` rejects:

- client `from`, `actor`, or `relayed_by`;
- raw mailbox fields;
- a recipient outside Arquitecto/Codex/Analista;
- a foreign action kind;
- execute without confirmation (HTTP 409).

The same fixture asserts server-authored attribution, response fields, redaction, and canonical mailbox shape.
`TASK-0310 prompt endpoint is inert while the product flag is off` proves the default-disabled endpoint returns
HTTP 403.

## Verification

- Product `npm test`: exit 0; 140 total, 118 passed, 22 declared slow-tier skips, 0 failed.
- Product `npm run test:slow`: exit 0; 120 passed, 19 environment-guarded fixture skips, 0 failed.
- Clean clone at product commit `767f41f`: `npm test` exit 0 with the same 140/118/22/0 result.
- `node --check src/server.js` and `node --check public/app.js`: exit 0.
- Hub collaboration validator, encoding scan, domain-neutrality scan, and drift check: exit 0; drift false.
- `protocol.config.json`: byte-identical.
- Approved in-app browser inspection was attempted, but this execution had no browser backend. No visual verdict
  is claimed; contract and live endpoint fixtures cover the maker evidence.

## Independent review requested

Arquitecto should route Analista review of commit `767f41f`, focusing on the strict server-side builder,
anti-impersonation negatives, off-by-default behavior, honest auto-commit relay attribution, and UI
preview/confirm flow. Codex is maker only and did not review or ratify this work.
