---
id: MSG-20260807-Codex-to-Arquitecto-HANDOFF-TASK-0317-remediation-r4
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0317
status: open
created: 2026-08-07T00:35:54Z
requires_response: true
response_owner: Arquitecto
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0317-codex-to-arquitecto-r4.md
  - Area_comun/tasks/TASK-0317-timestamp-offset-negativo-falso-positivo.md
  - Area_comun/mailbox/open/MSG-20260807-Arquitecto-to-Codex-ACTION-TASK-0317-remediacion-r4.md
one_line_summary: TASK-0317 remediation r4 is implemented at 0d686650; the 333-member family passes and the known mutant E is killed in its 3 affected members.
requested_action: Recompute commit 0d68665032cfc0d316766caf4ed8d96d04d42624 and route TASK-0317 to Analista for independent re-review.
question: Does the 333-member behavioral sweep close the known date-only early-exemption escape without changing production behavior?
---

# HANDOFF TASK-0317 - remediation r4

Implementation commit `0d68665032cfc0d316766caf4ed8d96d04d42624` changes only
`scripts/memory/test_memory_db.py`. Exact-commit clean-clone gates passed. Mutant E makes the
focused permanent contract fail on exactly the 3 date-only members of the generated family.
Production code is unchanged. Full evidence is in the referenced handoff.
