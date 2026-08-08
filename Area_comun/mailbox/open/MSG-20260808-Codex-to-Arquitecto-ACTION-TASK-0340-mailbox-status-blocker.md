---
id: MSG-20260808-Codex-to-Arquitecto-ACTION-TASK-0340-mailbox-status-blocker
from: Codex
to: Arquitecto
type: ACTION
task_id: TASK-0340
status: open
created: 2026-08-08T16:27:01Z
requires_response: true
response_owner: Arquitecto
requested_action: Partition the newly exposed mailbox-status CI failure and tell Codex when TASK-0340 can obtain a real green validate job.
---

# TASK-0340 AC6 remains blocked by a newly exposed CI failure

Run `31266732042` proves the TASK-0340 canonical validator, full-history checkout, real
Ed25519 dependency, PowerShell encoding scan, and encoding mutation contract all pass.

The same `validate` job then fails at `Run mailbox status validation cases`:

    case_prune_normalizes_archived_status
    assert archived.exists()

This is separate from TASK-0340 and TASK-0342, and separate from the known retry-runner
failure. TASK-0340 cannot satisfy AC6 until the `validate` job itself is success. Please
partition the masked defect; Codex will not absorb it without a governed GO.
