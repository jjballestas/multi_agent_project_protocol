---
task_id: TASK-0334
from: Codex
to: Arquitecto
status: in_review
implementation_commit: 6c0a645b6fd2beba0bdd57e0af20f55c5605d85f
remediation_iteration: 1
created_at: 2026-08-08T00:43:30Z
---

# HANDOFF TASK-0334 remediation 1 - consumer-specific ignore boundary

## Result

Commit `6c0a645b` separates the two safety directions without weakening embedded-repository
detection. The destructive Python claim-veto reader still discovers physical embedded Git
repositories at arbitrary depth and composes their dirty paths relative to the hub. The PowerShell
status reader now makes that expansion explicit with `-IncludeEmbeddedRepositories`; its two
blocking/comparison consumers, `Get-StagedResidueState` and `Get-WorktreeDiskProof`, use the parent
repository view by default and therefore preserve the parent's `.gitignore` policy.

The criterion is consumer-specific: over-detection is safe for the claim veto because it prevents a
termination, but it is unsafe for residue and disk-proof readers because it can defer an exec or
create a rollback-drift comparison from content that the parent deliberately excludes.

## Permanent mutation contract

`NEG-HARNESS-PARENT-IGNORE-BOUNDARY` creates a real parent repository that ignores
`.protocol-tmp/`, a real embedded repository below `.protocol-tmp/zc`, an uncommitted `note.md`, and
an active file-scoped claim on that path.

- Parent status is empty while expanded status reports `.protocol-tmp/zc/note.md`.
- `dirty_claimed_route` remains true, so the destructive sweep is vetoed.
- Healthy residue is `none` and the disk proof excludes the ignored path.
- A mutant that feeds expanded status into both blocking readers makes residue `live` and includes
  the ignored path in the disk proof.

The 26-test exec-lease harness passes. The falsification inventory reports 53/53 permanent
contracts across 8/8 CI-wired runners; the new contract owns seven load-bearing boundaries.

## Measured live PowerShell cost

Measured once on the live hub after the remediation, with seven repository roots:

- physical discovery walk: 0.7046 seconds;
- expanded composite status: 1.3220 seconds, 2,758 records;
- parent-view `Get-WorktreeDiskProof`: 1.0298 seconds, 159,719-byte payload.

The expanded walk/status cost is paid only by callers that explicitly request embedded repository
coverage. Each rollback verification still computes the parent-view disk proof twice. These are
wall-clock observations of the live dirty hub, not performance guarantees.

## Declared limits

- R1: a live file ignored by the embedded repository's own `.gitignore` remains invisible to Git
  status and can escape the claim veto. This task does not close that pre-existing family.
- R2: a partial or empty `.git` marker can resolve status against the parent and produce prefixed
  phantom routes. Its direction remains fail-safe for termination but may over-detect.
- Physical discovery remains depth-unbounded and does not follow symlink/reparse targets.

## Exact-commit verification

Detached clean clone of exact commit `6c0a645b6fd2beba0bdd57e0af20f55c5605d85f` under the designated
scratch root:

- `python scripts/test_exec_lease_harness.py` -> exit 0, 26/26.
- `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml`
  -> exit 0, 53/53 contracts and 8/8 runners.
- `python scripts/validate_collaboration_state.py --root .` -> exit 0.
- `python scripts/scan_encoding.py --root .` -> exit 0.
- `python scripts/scan_domain_neutrality.py --root .` -> exit 0.
- Runtime drift -> false at sequence 7778.
- `git diff --check` -> exit 0; clone status empty.

## Independent review focus

1. Recompute the ignored-parent fixture and verify the claim veto remains true.
2. Verify residue remains `none` and disk proof excludes the ignored embedded path.
3. Apply the blocking-reader expansion mutant and verify both consequences return.
4. Re-measure the PowerShell walk, expanded status, and parent-view disk proof.
5. Reassess R1/R2 and the existing fail-closed discovery behavior.

Codex is maker only and did not review or ratify this remediation.
