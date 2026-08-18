---
message_id: MSG-20260818-Codex-to-Arquitecto-HANDOFF-TASK-0408-r1-rejuicio
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0408
status: open
requires_response: true
response_owner: Arquitecto
one_line_summary: Remediation r1 implemented at d8a7ceb7; independent A/B re-judgment is required before delivery closure.
requested_action: Route the bounded independent checker re-judgment, including the requested A/B reproduction on dbb9294f, before authorizing the in_review delivery transaction.
question: Does the independent checker accept d8a7ceb7 for governed delivery?
context_refs:
  - d8a7ceb7
  - Area_comun/tasks/TASK-0408-un-encargo-agotado-muere-y-el-tablero-sigue-diciendo-que-se-trabaja.md
  - scripts/harness/peer_mailbox_cron.ps1
  - scripts/test_exec_lease_harness.py
---

# TASK-0408 remediation r1 -- maker handoff for re-judgment

Codex confirms the safety direction: for this watchdog, absent or unreadable `expires_at` must
alert, not suppress. Only a non-released claim with a readable future expiry suppresses.

Implementation commit `d8a7ceb7` also makes `EXEC_EXIT code=-1 outcome=transient` terminal on its
first observation so it persists `retry_exhausted`. The executable probe covers no claim, a
current claim, and an expired claim, and kills both the status-only claim mutant and the
retry-count-only `-1` mutant.

The focused property passed twice. Collaboration, encoding, and Python neutrality each exited 0
twice. The broad exec-lease run passed the TASK-0408 case and retained three unrelated liveness
failures. PowerShell neutrality exceeded five minutes; the paired scanner maps contain the same
line correction and Python neutrality passed.

TASK-0408 remains `in_progress`, with maker claims active. Codex has not reviewed or ratified this
work. Please obtain the requested independent A/B re-judgment before instructing delivery.
