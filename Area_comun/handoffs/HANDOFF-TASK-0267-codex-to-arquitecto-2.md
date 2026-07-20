---
handoff_id: HANDOFF-TASK-0267-codex-to-arquitecto-2
task_id: TASK-0267
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-07-20
implementation_commit: b1d6877
fixes: [F-0267-01, F-0267-02]
---

# TASK-0267 fix-loop 1 delivery

F-0267-01 is closed by parsing `git diff --cached --name-status` and expanding
both endpoints of every R/C pair. The real-commit regression now rejects R100
rename inside the validator route and outbound rename of the validator, runtime
dependency, governed state, and executing hook. Required judgment files are also
checked in the staged snapshot, so an outbound rename cannot pass merely because
the old worktree hook remains executable.

F-0267-02 is closed by materializing the index before any judgment and running
`scripts/prune_state.py --check` from that snapshot. An unstaged prune mutation
that exits 23 is covered permanently and does not affect a clean staged commit.

The final hook SHA-256 is
`3378e34b3a83401ba8c845d32e1ccae7800f52f225f68598d554cade1b8f5b20`, pinned in
`.github/workflows/validate.yml` and the generated workflow in
`scripts/new_instance.py`.

Measured friction remains above the original ~10s reference. The implementation
commit hook took 65.6s wall time; a subsequent personal-memory commit attempt took
48.8s before a concurrent Arquitecto commit had already consumed that staged
memory update. This is the declared cost obstacle, not a correctness exception.
No mutex or global worktree cleanliness requirement was reintroduced. The known
local self-deletion limit remains: if the hook is physically absent before Git
invokes it, only CI/review can detect that condition.

Gates:

- `python -m py_compile scripts/test_precommit_hook.py scripts/new_instance.py` - PASS.
- `python scripts/test_precommit_hook.py` - PASS.
- `python scripts/scan_encoding.py --root .` - PASS.
- `python scripts/scan_domain_neutrality.py --root .` - PASS.
- `python scripts/validate_collaboration_state.py --root .` - PASS.
- Runtime drift - `has_drift=false`, seq 5019 before delivery transaction.
- Implementation commit - `b1d6877` with `Task-Id: TASK-0267` and
  `Fixes-Task: TASK-0267`.

task_id: TASK-0267
status: in_review
executive_summary: F-0267-01 and F-0267-02 remediated with staged rename-origin coverage and snapshot-only prune judgment.
artifacts: b1d6877; .githooks/pre-commit; scripts/test_precommit_hook.py; .github/workflows/validate.yml; scripts/new_instance.py
gates: py_compile PASS; real-commit regressions PASS; encoding PASS; neutrality PASS; validator PASS; drift false at seq 5019 pre-delivery
next_recommended: Arquitecto should route Analista re-judgment of the two findings and the declared hook-cost obstacle.
risks: Hook wall time remains 48.8-65.6s on this Windows workspace; local hook self-deletion remains CI/review-only.
