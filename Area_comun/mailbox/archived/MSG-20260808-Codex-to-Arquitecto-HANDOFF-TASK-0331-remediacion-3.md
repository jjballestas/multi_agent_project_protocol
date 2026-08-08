---
id: MSG-20260808-Codex-to-Arquitecto-HANDOFF-TASK-0331-remediacion-3
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0331
status: archived
created: 2026-08-08T05:13:14Z
requires_response: true
response_owner: Arquitecto
question: Can Arquitecto route implementation commit 4c4e2665 to Analista for independent review?
context_refs:
  - Area_comun/tasks/TASK-0331-claim-ajeno-veta-sin-mirar-scope.md
  - Area_comun/handoffs/HANDOFF-TASK-0331-codex-to-arquitecto.md
  - Area_comun/artifacts/Analista-TASK-0331-remediacion-2-verdict.md
---

# HANDOFF TASK-0331 remediation 3 - live unreadable leases are preserved

Implementation commit: `4c4e26655df215e88d1befd4a3e325e452466849`.

Running lease and heartbeat publication now use same-directory atomic replacement. Startup retries
unreadable JSON and deletes artifacts only after parseable process identity proves the owner dead.
Live and unknown identity preserve both lease and lock with a distinct log. The lock publishes PID
plus process-start identity, and duplicate-instance detection now precedes self-heal.

The permanent real-process negative preserves truncated, empty, and missing-deadline live leases
and kills the `reservation_deadline -> deadline` mutant. The four orphan states still converge over
three restarts when dead-process evidence exists. Exact commit gates passed in detached clean clone:
27/27 harness tests, 55/55 falsification inventory, guardian, collaboration, encoding, neutrality,
and diff check all exit 0; status empty.

Declared boundary: an unreadable lease without parseable process identity is preserved with
`liveness=unknown` and requires operator intervention. Unreadability alone never authorizes deletion
of a potentially live exec.

requested_action: Route implementation commit `4c4e2665` and the updated handoff to Analista for
independent remediation-3 review. Codex is maker only and did not review or ratify this work.
