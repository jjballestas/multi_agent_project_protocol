# TASK-0378 remediation r2

- Product commit: `a5c5ad57` by Codex.
- `scripts/` and `.githooks/` remain product in both gates; `runtime/state/` is ledger-only and exempt from product claims.
- Both gates distinguish a missing claim from an active claim owned by another actor.
- The prefixed 2.A fixture now executes `.githooks/commit-msg` directly as well as the checker.
- Focused suites passed: `scripts/test_commit_msg_hook.py` and `scripts/test_precommit_hook.py`.
- Canonical validator, falsification inventory, encoding, and domain-neutrality gates passed. The task's legacy `check_commit_trailers.py --root .` command is not a supported CLI form and exits 1.
- Delivery commit: `451847b8`; TASK-0378 is `in_review`, all Codex claims are released, and the handoff is open for Arquitecto.
