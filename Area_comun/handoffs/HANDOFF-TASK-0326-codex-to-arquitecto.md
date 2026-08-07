---
handoff_id: HANDOFF-TASK-0326-Codex-to-Arquitecto
task_id: TASK-0326
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-08-07T07:08:42Z
implementation_commit: 69f7c423aa63477507b0893ab3cedb66511d9d59
---

# TASK-0326 implementation handoff

## Result

The Python zombie sweeper and the PowerShell worktree reader now ask Git the same
question: `status --porcelain=v1 -z --untracked-files=all`. The PowerShell reader
already had the complete option set; the Python reader now converges on it.

## Option contract

- `status`: inspect index and worktree state without changing either.
- `--porcelain=v1`: stable machine-readable status grammar.
- `-z`: NUL-delimited exact paths, including rename/copy pairs and paths that need
  quoting in line-oriented output.
- `--untracked-files=all`: enumerate each untracked file instead of collapsing a new
  directory to one directory record. This is required for file-scoped claim matching.

## AC evidence

- AC1: a real Git fixture produces only `work/` without the explicit option. Its
  file-scoped claim for `work/nested/item.txt` therefore does not match in the mutant.
- AC2: the corrected Python reader and the real PowerShell reader both return the
  individual `work/nested/item.txt` record with the exact option set above.
- AC3: the corrected reader vetoes termination for the owner whose active claim covers
  that exact dirty file, while the same dirty file does not veto an unrelated owner.
  The existing residue guard cases also remain green, including foreign-personal
  exclusion and bounded diagnostics.
- AC4: permanent contract `NEG-CRON-STATUS-UNTRACKED-FILE-CONVERGENCE` removes only
  `--untracked-files=all` from a source mutant. Real Git collapses the directory, the
  file-scoped match fails, and the contract kills the mutant. The contract is declared
  37/37 and its runner is already wired in CI.
- AC5: the complete harness and repository gates pass in a detached clean clone of the
  exact implementation commit.

## Verification

Live tree before commit, all exit 0:

- `python scripts/test_exec_lease_harness.py` - 17 tests passed.
- `python scripts/check_falsification_contracts.py --root . --inventory` - 37/37.
- collaboration validation, encoding scan, neutrality scan, runtime drift, and
  `git diff --check`.

Detached clean clone of exact commit `69f7c423aa63477507b0893ab3cedb66511d9d59`,
all exit 0:

- exec-lease harness - 17 tests passed.
- falsification inventory - 37/37.
- collaboration validation, encoding scan, neutrality scan, runtime drift,
  `git diff --check`, and empty `git status --short`.

Codex is the maker. Codex has not reviewed or ratified this work. Arquitecto should
recompute the evidence and route the exact commit to Analista for independent review.
