---
task_id: TASK-0267
from: Codex
to: Arquitecto
status: in_review
implementation_commit: b583090
memory_commit: ca9587a
hook_sha256: 6871e582122702cd8d31ff4c2ad6f8af21db87948482810d961942560055304e
friction_count: 2
---

# TASK-0267 handoff

Hook v2 materializes the complete Git index with `git checkout-index` into an
always-cleaned temporary directory and runs the collaboration validator from
that snapshot. Unstaged and untracked peer work no longer participates in the
verdict. The permanent harness now uses real `git commit` calls and covers
staged-invalid rejection, unstaged validator isolation, unstaged governed peer
work, R100 judgment-code rename, and cleanup after rejection.

The born-operational runtime export copies hook v2. Hub and generated CI verify
that `.githooks/pre-commit` exists and matches SHA-256
`6871e582122702cd8d31ff4c2ad6f8af21db87948482810d961942560055304e`.

Structural limit: deleting the hook itself locally cannot be detected by code
inside that hook. Only CI existence/hash verification and diff review cover it.

## Measurements

- Hook cold: 53.251s.
- Hook hot: 51.487s.
- Direct validator in the live worktree: 15.044s.
- Validator in a materialized temporary snapshot: approximately 52s.
- Index materialization itself was sub-second; validation in the temporary tree
  dominates. This exceeds the approximately 10s reference and is a review risk.
  No validator internals were changed because the intake declares that out of
  scope; no weaker cleanliness fallback was substituted.

## Obstacles

- what: runtime instantiation aggregate reported failures in the coordination
  and runtime-tier cases.
  root_cause: both assertions concern the current generated layout (`runtime/`
  unexpectedly present for coordination, and the exact gate-script set), not
  hook-v2 bytes or the pinned workflow assertion.
  resolution: ran a focused runtime export proof that generated hook v2, matched
  its SHA-256, included the CI existence/hash step, and contained index checkout.
  recurrence_risk: medium; the pre-existing aggregate expectations need their
  own owner/scope reconciliation.
- what: hook execution exceeded the reference budget.
  root_cause: full validation from the temporary snapshot takes about 52s versus
  15s in the live worktree; materialization is not the dominant cost.
  resolution: retained correctness and reported exact cold/hot figures rather
  than weakening the validator outside scope.
  recurrence_risk: high; reviewer must accept the exception or open a bounded
  validator-performance unit.

task_id: TASK-0267
status: in_review
executive_summary: Hook v2 judges the complete staged index without a global worktree-cleanliness mutex; real-commit negatives, export mirror, and pinned CI hash are implemented.
artifacts: b583090; ca9587a; .githooks/pre-commit; scripts/test_precommit_hook.py; scripts/new_instance.py; .github/workflows/validate.yml
gates: precommit regression PASS; focused runtime export PASS; validator PASS; encoding PASS; neutrality PASS; drift false; runtime instantiation aggregate FAIL 2 pre-existing layout assertions; cold/hot 53.251s/51.487s over reference
next_recommended: Analista reviews correctness and Arquitecto decides whether the measured cost exception is acceptable or needs a separate validator-performance unit.
risks: High recurrence risk from 51-53s hook latency; local deletion of the hook remains structurally detectable only in CI/review.
