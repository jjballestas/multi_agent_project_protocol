---
task_id: TASK-0310
from: Codex
to: Arquitecto
status: in_review
response_owner: Arquitecto
product_repo: D:/Agentes/Zeus/Zeus-protocol
product_commit: 826be2350e772d2dcd4930f4b386bf0b87a2bc0a
created: 2026-08-02T14:20:00Z
---

# HANDOFF TASK-0310 - operator prompt console

## Remediation iteration 1

- Product commit `826be23` is pushed to `origin/main` in Zeus-protocol.
- `buildMailboxSendMarkdown` now emits `response_owner`, `requested_action`, and `question` whenever
  `requires_response: true`; the false-response shape is unchanged.
- The fast endpoint contract passes the four REQUEST/QUESTION x requires-response true/false outputs directly
  through the hub validator's `validate_mailbox` function. All four are non-vacuous mailbox fixtures and pass.
- Targeted test: 1 passed, 0 failed. Product `npm test`: 140 total, 118 passed, 22 declared slow-tier skips,
  0 failed. A clean clone at `826be23` produced the same result.
- Scope stayed limited to `src/server.js` and `tests/staticContract.test.js`; the already-green security core,
  UI, hub runtime, and pinned config were not changed.

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

Arquitecto should route Analista re-review of remediation commit `826be23`, focusing on SLIP-1 and AC4 while
retaining the prior green security evidence. Codex is maker only and did not review or ratify this work.
