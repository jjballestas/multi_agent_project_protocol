---
handoff_id: HANDOFF-TASK-0164-codex-to-arquitecto-1
task_id: TASK-0164
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-23T21:55:00Z
---

# HANDOFF TASK-0164 - Codex to Arquitecto

## Summary

Implemented DECISION-0059 fine-grained claim rows and physical event-log serialization.

Protocol commits:
- `c4dd413 feat(runtime): serialize ledger writes and row-scope claims`
- `693ec1a chore(runtime): ignore ledger lock file`

Product commit:
- `4faacd1 fix(intake): row-scope front claims`

## Changes

- `runtime/submit_intent.py`
  - Adds `Area_comun/state/CLAIMS.json` to row-scoped ledger paths.
  - Changes claim intent authority from whole-file `CLAIMS.json` to `CLAIMS.json#<claim-id>`.
  - Wraps `submit_intent` and transactional `submit_intents` in a cross-process ledger file lock before idempotency lookup, validation, append, materialization, snapshot write, and drift check.
  - Re-reads state/head inside the lock by constructing the writer and validating after lock acquisition.
- `runtime/eventlog.py`
  - Adds `runtime/state/.ledger.lock` file lock using `msvcrt` on Windows and `fcntl` elsewhere.
- Validators
  - Python and PowerShell validators now understand `CLAIMS.json#CLAIM-*` selectors and still treat bare `CLAIMS.json` as whole-file compatibility scope.
- Goldens
  - Row-scoped claim cases now cover distinct claim rows, same claim row conflict, and bare-vs-row compatibility conflict.
  - Transaction cases now include claim-row behavior and a deterministic two-process concurrent submit test with chain validation and drift 0.
- Front
  - `src/server.js` emits `Area_comun/state/CLAIMS.json#<claim-id>` for front-generated claims and does not list runtime materialization paths in claim scopes.
  - Test fixture overlays/commits protocol runtime overlays so product clean-clone write tests validate with the current runtime implementation.
- `.gitignore`
  - Ignores `runtime/state/.ledger.lock`.

## Evidence

- Protocol:
  - `python -m py_compile runtime/eventlog.py runtime/submit_intent.py scripts/validate_collaboration_state.py examples/intent_tx_cases/run_intent_tx_cases.py examples/row_scoped_claim_cases/run_row_scoped_claim_cases.py` PASS.
  - `python examples/row_scoped_claim_cases/run_row_scoped_claim_cases.py` PASS, 8 cases with PowerShell parity.
  - `python examples/intent_tx_cases/run_intent_tx_cases.py` PASS, 8 cases.
  - `python scripts/scan_encoding.py --root .` PASS.
  - `python scripts/scan_domain_neutrality.py --root .` PASS.
  - `python scripts/validate_collaboration_state.py --root .` PASS.
  - Drift before delivery artifacts: `has_drift=false`, `up_to_seq=1425`.
- Product:
  - `node --check src/server.js; node --check tests/staticContract.test.js` PASS.
  - `npm test` PASS, 57/57.
  - Targeted rerun for `submit_intent contention|intake endpoint rejects` PASS.
  - Targeted rerun for `auto commit push lands only exact` PASS.

## Notes for Review

- `protocol.config.json`, genesis, registry, and keys were not touched.
- The physical lock file is intentionally untracked and ignored.
- I did not enable or change capabilities.
- The initial full `npm test` after the first protocol commit failed because the product fixture overlaid `submit_intent.py` without `eventlog.py`; this was fixed by overlaying and committing the matching runtime files in the fixture. The final full run passed.
