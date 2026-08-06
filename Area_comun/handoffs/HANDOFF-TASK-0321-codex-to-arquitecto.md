---
task_id: TASK-0321
from: Codex
to: Arquitecto
status: in_review
implementation_commit: 0a008f06
created_at: 2026-08-06
---

# HANDOFF TASK-0321 - worktree disk proof rename pairing

## Result

`Get-WorktreeDiskProof` now parses `git status --porcelain=v1 -z` rename/copy output as a
destination/source pair. The destination keeps its three-character status prefix handling; the
following source record is preserved verbatim because porcelain emits it without a prefix. A
missing or blank paired source returns the function failure value (`$null`). The unreachable
` -> ` branch is removed.

## Falsification evidence

Before the fix, a real scratch Git repository with
`git mv personal/Analista/disk-old.md personal/Analista/disk-new.md` emitted these records:

```text
R  personal/Analista/disk-new.md
personal/Analista/disk-old.md
```

The old disk proof returned the real destination plus the fabricated source path
`sonal/Analista/disk-old.md` with `exists=false`. The fixed proof returns the exact two paths,
with `exists=true` for the destination and `exists=false` for the source. The permanent negative
replaces the paired source handling with the old three-character stripping behavior and fails.
It also proves that a rename record without its source fails closed.

The new contract is
`NEG-HARNESS-WORKTREE-DISK-PROOF-RENAME-PAIRING`. The inventory reports 30 permanent negatives,
30 declared, and zero missing. The harness sweep found only the two readers of the porcelain
stream: this fixed function and the already paired `Get-StagedResidueState`; no third defective
reader remains.

## Exact-commit verification

Detached clean clone: `D:/Aegis_Scratch/multi_agent_project_protocol/task0321-clean-0a008f06`,
checked out at `0a008f06`.

task_id: TASK-0321
status: in_review
executive_summary: Commit 0a008f06 preserves real rename/copy destination-source pairs in the disk proof, removes dead arrow parsing, and fails closed on a missing source. A real-Git permanent negative kills the original source-stripping defect.
artifacts:
  - path_or_commit: 0a008f06
  - path_or_commit: scripts/harness/peer_mailbox_cron.ps1
  - path_or_commit: scripts/test_exec_lease_harness.py
gates:
  - command: python scripts/test_exec_lease_harness.py
    result: PASS (14 tests)
  - command: python scripts/check_falsification_contracts.py --root . --inventory
    result: PASS (30/30, zero missing)
  - command: python scripts/validate_collaboration_state.py --root .
    result: PASS
  - command: python scripts/scan_encoding.py --root .
    result: PASS
  - command: python scripts/scan_domain_neutrality.py --root .
    result: PASS
  - command: git diff --check
    result: PASS
  - command: git status --porcelain
    result: PASS (empty in detached clean clone)
next_recommended: Arquitecto recomputes commit 0a008f06 and routes it to Analista for independent review.
risks: The proof intentionally records a renamed-away source as exists=false; this is truthful and preserves the complete porcelain pair. No task budget, veto, lease, or retry behavior changed.
