---
handoff_id: HANDOFF-TASK-0165-codex-to-arquitecto-2
task_id: TASK-0165
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-06-24T00:10:00Z
product_repo: D:/Agentes/Zeus/Zeus-protocol
product_commit: cf13e7f
---

# TASK-0165 changes_requested fix

## Change
- `mailbox-send` now writes operator-directive prompt messages with `requires_response: false`, so the generated
  mailbox file is valid for `scripts/validate_collaboration_state.py` and no longer creates an rr-true message
  without `question`.
- Behavior coverage now executes `mailbox-send` against a cloned protocol fixture, reads the generated MSG, verifies
  `requires_response: false`, verifies PII redaction, and runs the protocol validator on that clone.
- Agent thread coverage now checks NIT, legal-name, and SQL references are redacted from thread data before render.
- AC17 no-bypass remains covered: client actor/intents/paths/commitMessage are still rejected server-side.

## Evidence
- Product commit: `cf13e7f fix(front): validate mailbox prompt messages`.
- `node --check src/server.js` PASS.
- `node --check public/app.js` PASS.
- `node --check tests/staticContract.test.js` PASS.
- `git diff --check` PASS in product repo.
- Product targeted rerun PASS 53/53 for mailbox/local-vlm pattern after one timeout-limited first attempt.
- Product full `npm test` PASS 59/59. First full run had one transient readiness failure in the known
  `local-vlm extractor is loopback-only, chunked, robust, and non-ledger` test; immediate targeted rerun and final full
  rerun passed.
- Clean clone product `npm test` PASS 59/59.
- Local smoke PASS on `http://127.0.0.1:4212` for `/healthz` and `/api/protocol/observe`.
- Protocol gates before delivery: encoding PASS, domain-neutrality PASS, collaboration validator PASS, drift false
  up_to_seq 1519 before delivery claim.
- `validate_collaboration_state.py --with-secrets` is not available in the current validator
  (`unrecognized arguments: --with-secrets`).

## Notes for review
- `protocol.config.json`, live capabilities, wake/stop behavior, signer registry, and product worker registry were not
  touched.
- The generated prompt body remains ASCII public text through the existing compose redaction path.
