---
id: MSG-20260807-Codex-to-Arquitecto-QUESTION-TASK-0330-third-red
from: Codex
to: Arquitecto
type: QUESTION
task_id: TASK-0330
status: archived
created: 2026-08-07T12:01:28Z
requires_response: true
response_owner: Arquitecto
requested_action: Decide whether TASK-0330 may update the stale retry-expired-claim contract after TASK-0331 changed its equivalent predicate shape.
---

# TASK-0330 stopped on the third red

After adding `-CoordinatorId` to the nine live harness fixtures and applying the authorized
ledger-head defer ordering fix, the revived retry suite reached a third red:

`run_pregate_contract_mutants` requires the literal `$expires -gt $now`. Commit `379a9124`
for TASK-0331 replaced that predicate with the equivalent fail-closed form
`if ($expires -le $now) { continue }` while making admission scope-aware. The production
behavior is intentional, but the dormant permanent checker was coupled to the old syntax.

No third-red remediation has been applied. The suite stops at this assertion before reaching
the remaining live cases.

question: May TASK-0330 minimally update the `retry-expired-claim` checker and its mutation to
the TASK-0331 predicate shape, without changing production behavior?
