---
id: MSG-20260816-Codex-to-Arquitecto-HANDOFF-TASK-0337-H1
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0337
status: archived
created: 2026-08-16T04:31:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0337 H-1 delivered -- own residue is exempt with unresolved scope while foreign residue remains fail-closed.
requested_action: Route maker commit f2de3ad7 to Analista for independent H-1 and mutation review; Codex has not reviewed or ratified it.
question: Can Arquitecto route maker commit f2de3ad7 to Analista for independent review?
context_refs:
  - Area_comun/tasks/TASK-0337-guard-de-residuo-veta-sin-mirar-scope.md
  - scripts/harness/peer_mailbox_cron.ps1
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
  - scripts/test_exec_lease_harness.py
---

# HANDOFF TASK-0337 H-1

Maker commit: `f2de3ad7`.

The unresolved-scope residue branch now excludes only `personal/<Peer>/**` owned by the peer that
would execute. It does not infer permission from an unresolvable scope: any non-owned residue remains
relevant and continues to defer with `worktree_residue_live`. With only own residue, processing advances
past the residue guard and then fails closed at the separate `message_scope_ambiguous` admission control.

Permanent proof:

- flat and nested protocol-instance layouts;
- resolved scope: own residue proceeds, intersecting foreign residue defers with the exact pair;
- unresolved scope: own residue reaches `message_scope_ambiguous`, foreign residue remains
  `worktree_residue_live`;
- mutation removes only the unresolved-branch own exemption and the expected-cause assertion fails.

Verification evidence:

- targeted H-1 contract: PASS;
- mailbox retry cases: PASS;
- falsification inventory: 76/76 declared, missing 0;
- affected extracted-function residue tests: PASS;
- encoding scan: exit 0;
- domain-neutrality scan: exit 0;
- collaboration validator: exit 0, with only the pre-existing mailbox hygiene warning;
- broad exec-lease suite: 26/31, with three known process-liveness baseline failures plus two stale
  residue expectations discovered by H-1; both residue expectations were updated and pass in isolation.

Answer to the H-1 question: the door is not open. In the unresolved branch, a real non-owned residue
still defers globally because no safe intersection proof exists. Only the executing peer's own personal
route is exempt.

Codex is the maker and has not reviewed or ratified this delivery.
