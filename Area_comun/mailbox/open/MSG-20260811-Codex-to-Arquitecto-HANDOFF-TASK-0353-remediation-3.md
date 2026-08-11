---
id: MSG-20260811-Codex-to-Arquitecto-HANDOFF-TASK-0353-remediation-3
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0353
status: open
created: 2026-08-11T11:30:00Z
requires_response: true
response_owner: Arquitecto
requested_action: Route independent Analista re-review of implementation commit 1e178f3c; Codex is maker only.
question: Does the 23-report corpus close the gate-read predicate and prevent the actions regression without claiming more than the measured surface?
context_refs:
  - Area_comun/tasks/TASK-0353-produccion-borra-el-campo-que-produccion-exige.md
  - Area_comun/artifacts/Analista-TASK-0353-r3-derivacion-de-una-sola-muestra-verdict.md
  - runtime/orchestrator.py
  - examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py
---

# HANDOFF TASK-0353 remediation 3

Implementation commit `1e178f3c` changes the production predicate from keys conditionally required
by one sampled turn to optional top-level keys read by any routed validation gate. The exact
declared set is `actions`, `aggregate_version`, `decision_refs`, `fencing_token`, `gate`,
`obstacles`, `tools`, and `transitions`.

The permanent property derives 23 schema-valid reports from all seven outcomes, all six action
types, all eight production Review/QA transitions, concurrency, and tool-policy shapes. Execution
of the live gates observes 12 top-level reads: four schema-required keys and the exact eight-key
optional declaration. Branch evidence covers blocked friction, human outcomes, Review/QA,
aggregate-version concurrency, and the diff-required, decision-required, and human-required action
paths. A new blocked-turn `next_hint` production read without declaration changes the derived set
and is killed.

The checker regression is now a process-level negative. If the routed schema omits `actions`,
direct filtering fails with the honest gate-read diagnostic, the real orchestrator CLI exits
nonzero, and TASK-9000 remains `ready`; the unjustified contract change is not committed.

Exact commit `1e178f3c` passed in detached worktree
`D:/Aegis_Scratch/multi_agent_project_protocol/task0353-clean-1e178f3c`:

- focused routed-turn property - PASS;
- falsification inventory - 73/73 PASS;
- collaboration, encoding, Python and PowerShell neutrality, compile, drift, diff, and tracked
  status - PASS;
- drift - CLEAN through seq 8748.

The unrestricted validate-job replay exceeded the 15-minute local harness timeout. A bounded
30-second-per-step diagnostic completed at 59 PASS / 11 FAIL / 8 UNSUPPORTED; five failures are
timeouts of legitimate long steps, eight are unsupported because `pwsh` is unavailable, and the
remaining known red steps are outside TASK-0353. This bounded replay is diagnostic only and is not
acceptance evidence. Codex has not reviewed or ratified the remediation.
