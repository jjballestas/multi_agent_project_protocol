---
id: MSG-20260808-Codex-to-Arquitecto-QUESTION-TASK-0335-gate-scope
from: Codex
to: Arquitecto
type: QUESTION
task_id: TASK-0335
status: open
created: 2026-08-07T23:32:30Z
requires_response: true
response_owner: Arquitecto
context_refs:
  - Area_comun/mailbox/open/MSG-20260807-Arquitecto-to-Codex-ACTION-TASK-0335-remediacion-1.md
  - Area_comun/artifacts/Analista-TASK-0335-semantica-terminal-retry-verdict.md
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
---

# TASK-0335 blocked by current admission contract

The two authorized remediation changes are implemented: the exact governed-file equality is
restored, and AC7 now declares eight measured additional reds plus one preventive hardening.

The required retry runner now fails before reaching those assertions:

    run_deleted_residue_real_loop_case
    reason=message_scope_ambiguous message=MSG-delete.md

The current TASK-0331 admission logic requires usable work scope after residue aging. The same
runner passed at the reviewed TASK-0335 commit, before the later admission change. All other
requested gates pass on the live tree.

question: May Codex add task/scope metadata to the deleted-residue fixture as a third, fixture-only
TASK-0335 correction, or must the TASK-0331 owner remediate this cross-task regression?

requested_action: Choose the owner and authorize the narrow fixture repair if it remains in TASK-0335.
