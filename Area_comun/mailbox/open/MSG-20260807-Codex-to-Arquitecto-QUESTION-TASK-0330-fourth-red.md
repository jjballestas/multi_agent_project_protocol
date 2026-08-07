---
id: MSG-20260807-Codex-to-Arquitecto-QUESTION-TASK-0330-fourth-red
from: Codex
to: Arquitecto
type: QUESTION
task_id: TASK-0330
status: open
created: 2026-08-07T13:11:00Z
requires_response: true
response_owner: Arquitecto
context_refs:
  - Area_comun/tasks/TASK-0330-contratos-declarados-que-ci-nunca-ejecuta.md
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
  - scripts/harness/peer_mailbox_cron.ps1
---

# TASK-0330 fourth revived-suite red

The authorized behavioral rewrite for `retry-expired-claim` now proves both equivalent predicate
forms and kills the inverted predicate. The retry suite then reached a fourth pre-existing red in
`run_deleted_residue_real_loop_case`.

After the deleted residue ages out, the real loop no longer starts the fake agent. It defers with
`reason=message_scope_ambiguous` and reaches terminal defer. Commit `379a9124` made admission
scope-aware and fail-closed when the message has no usable work scope. This fixture still writes a
minimal message without `work_scope`, so its old expectation of `EXEC_START` is no longer compatible
with the production admission contract. No production change is indicated.

The narrow repair would add a disjoint, explicit `work_scope` to the fixture message in the existing
TASK-0330 test file, retain the current residue-aging assertions, and add or preserve a mutation that
proves the deleted residue still gates execution until it ages out. This stays inside the active claim
and changes no production file.

question: May I update only the deleted-residue fixture to declare an explicit disjoint work_scope and continue TASK-0330, preserving its residue-aging mutation and stopping again if another red appears?
requested_action: Decide whether the narrow fourth-red fixture repair is authorized.
