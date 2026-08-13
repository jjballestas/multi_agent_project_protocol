# HANDOFF TASK-0364

task_id: TASK-0364
maker: Codex
requested_status: in_review
implementation_commits: cefd5e02, f23ef6a7, 6b47e146, 6aee19ac

## Delivered behavior

The four canonical jobs now run on the provisioned owned runners. The Windows falsification job
uses `protocol-win`; the three Linux-dependent jobs use `protocol-linux`. Every job publishes its
interpreter versions, removes retained workspace residue before checkout, and leaves the retained
workspace clean even after a failed gate.

## Acceptance evidence

- AC1: placement follows the interpreter dependency, including Windows PowerShell 5.1 on
  `protocol-win` and pwsh 7 on Linux on `protocol-linux`.
- AC2: dirty run `31596823928` reports `DIRTY_REMEDIATED entries=3` for the seeded obsolete `.pyc`,
  residual artifact, and dirty tracked entry. Follow-up run `31597752400` reports the clean path.
- AC3: real run `31630955323` and clean replay at the exact same head
  `2eae1c393c9ca8f052469f248a981f6ac06d5374` have no opposite outcome among Actions-executed
  steps. Both pass steps 1-19, fail the Architect-owned pruning check, and pass the always-run actor
  auth and cleanup steps. Clean replay summary: 69 pass / 12 fail; later ordinary steps are skipped
  by Actions after the first failure and are not host divergences.
- AC4: observed Linux Python 3.14.7 and PowerShell 7.4.6; the Windows job publishes provisioned
  Python, pwsh, and Windows PowerShell 5.1.
- AC5: original step inventories remain 7/7, 80/80, 3/3, and 5/5, in order.
- AC6: reverting one job changes only its single `runs-on` declaration.
- AC7: run `31630955323`, the four named jobs, head
  `2eae1c393c9ca8f052469f248a981f6ac06d5374`; Actions timing returns `billable: {}`.

The workflow remains red only for existing product/protocol defects and due maintenance explicitly
outside this host-migration task. Codex did not review or ratify its own work.
