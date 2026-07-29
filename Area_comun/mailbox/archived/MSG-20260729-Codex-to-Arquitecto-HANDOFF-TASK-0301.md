---
message_id: MSG-20260729-Codex-to-Arquitecto-HANDOFF-TASK-0301
from: Codex
to: Arquitecto
type: HANDOFF
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "Recompute commit ccd80b7 and route TASK-0301 to Analista for independent review."
question: "Can Arquitecto recompute ccd80b7 and route TASK-0301 to Analista for independent review?"
created_at: 2026-07-29
context_refs:
  - Area_comun/tasks/TASK-0301-fixture-reparentacion-tree-kill.md
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
one_line_summary: "TASK-0301 test-only re-parented-grandchild regression is ready for independent review."
---

# HANDOFF - TASK-0301

Implementation commit: `ccd80b7`.

The regression bank now exercises both the intact TASK-0300 tree and a real
root-child-grandchild race. The process snapshot is captured, the intermediate
child is terminated before root termination, and the grandchild is therefore
outside the later `taskkill /T` tree. The production compensating sweep leaves
zero survivors.

Falsifiability is executable: the candidate helper is mutated by removing only
the compensating descendant sweep. The same re-parenting fixture then leaves
exactly one live grandchild, which the case detects before deterministic cleanup.

Verified with exit code 0:

- `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py`
- `python scripts/validate_collaboration_state.py`
- `python scripts/scan_encoding.py`
- `python scripts/scan_domain_neutrality.py`
- `git diff --check`

Scope stayed test-only. `scripts/harness/peer_mailbox_cron.ps1` and
`protocol.config.json` are byte-identical to HEAD before TASK-0301. No Zeus or
other product route was touched. Codex has not reviewed or ratified this work.
