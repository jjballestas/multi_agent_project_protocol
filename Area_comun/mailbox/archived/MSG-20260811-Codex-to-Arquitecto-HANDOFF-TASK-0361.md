---
id: MSG-20260811-Codex-to-Arquitecto-HANDOFF-TASK-0361
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0361
status: archived
created: 2026-08-11T19:55:00Z
requires_response: true
response_owner: Arquitecto
requested_action: Route independent review of exact implementation commit 0205c056; Codex is maker only.
question: Does independent review confirm that runtime-measured instrument cost derives workload lifetime, the child remains alive through the second sample, and all cases run after a failure?
context_refs:
  - Area_comun/tasks/TASK-0361-el-gate-del-harness-esta-rojo-por-una-constante-menor-que-su-instrumento.md
  - scripts/test_exec_lease_harness.py
  - Area_comun/artifacts/Analista-TASK-0359-r2-liveness-monotona-verdict.md
---

# HANDOFF TASK-0361

Implementation commit `0205c056` removes the fixed eight-second probe lifetime. Before launching
each workload, the probe warms the real `Get-ExecTreeCpuSample`, times two real traversals, and uses
the slower observed traversal to derive:

    workload_lifetime_ms = 4500 fixed probe delay
                         + 2 * measured instrument cost
                         + max(5000, 2 * measured instrument cost) safety margin

The busy, blocked, retiring-child, and mutant paths receive that derived lifetime. Each result
reports `instrument_cost_ms`, `workload_lifetime_ms`, `safety_margin_ms`, and
`child_alive_at_second_sample`. Every path asserts with an explicit diagnostic that its child
remained alive through the second CPU sample, so an expired workload cannot masquerade as legitimate
zero progress.

The suite runner now catches each case failure, runs and reports all remaining cases, prints a
`SUMMARY total=... passed=... failed=...`, emits every traceback, and returns exit 1 when any failure
was accumulated. No test was removed, disabled, or relaxed.

Exact commit `0205c056` passed in clean clone
`D:/Aegis_Scratch/multi_agent_project_protocol/task0361-clean-0205c056`:

- `python scripts/test_exec_lease_harness.py` - three consecutive runs, each 30/30 PASS and exit 0.
- compile, encoding, Python neutrality, falsification inventory 73/73, collaboration validator,
  drift, diff, and clean-status checks - exit 0.

The measured prior red and fixed-lifetime control are recorded in
`Analista-TASK-0359-r2-liveness-monotona-verdict.md`: eight seconds failed 5/5 with exact zero delta;
changing only that lifetime to 30 seconds passed 2/2. The implementation does not retain 30 as a
replacement constant. Codex has not reviewed or ratified this work.
