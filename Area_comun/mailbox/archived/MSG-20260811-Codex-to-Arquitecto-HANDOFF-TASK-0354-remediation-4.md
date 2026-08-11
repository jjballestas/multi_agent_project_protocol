---
id: MSG-20260811-Codex-to-Arquitecto-HANDOFF-TASK-0354-remediation-4
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0354
status: archived
created: 2026-08-11T15:03:43Z
requires_response: true
response_owner: Arquitecto
requested_action: Route exact implementation 90fa8ffa to Analista for independent TASK-0354 remediation-4 re-review.
question: Does independent review approve the changed membership criterion and Windows host parsing?
context_refs:
  - .github/workflows/validate.yml
  - Area_comun/tasks/TASK-0354-concurrencia-y-colocacion-de-jobs-en-el-workflow.md
  - Area_comun/artifacts/Analista-TASK-0354-r4-formas-invocacion-verdict.md
---

# TASK-0354 remediation 4 maker handoff

Implementation commit: `90fa8ffa`.

The membership criterion is now independent of invocation-form recognition. For each workflow
`run` block, the gate derives every repository `.py` path named in the raw command, normalizes path
separators, and requires the discovered runner set for that same block to contain the derived set.
An omission is fail-closed and reports the concrete missing path. The literal
`expected_runner_invocations = 73` is gone.

Tokenization is host-aware: jobs whose `runs-on` contains `windows` use non-POSIX shlex semantics,
so an unquoted backslash remains a Windows path separator. Other jobs retain POSIX parsing. This
closes the category error without adding the reported invocation forms to the production recognizer.

Measured evidence:

- Intact gate: EXIT=0, `invocations=73 referenced=72`.
- Fourteen previously silent additions: 14/14 EXIT=1, each naming
  `examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py` as the missing runner.
- Four Windows backslash additions under the Windows job: 4/4 EXIT=1 through the dependency check,
  proving host-aware discovery retained the runner path.
- Exact commit `90fa8ffa` in a detached clean worktree: dependency gate, collaboration, encoding,
  Python neutrality, PowerShell neutrality, drift through seq 8790, and falsification inventory
  73/73 all EXIT=0; tracked status was empty.

Answer to the Arquitecto question: YES. The discovered set is asserted against the condition-derived
set, and a failure names the missing route. G2 remains explicitly outside this remediation, unchanged.

Codex is maker only. No self-review, ratification, or closure was performed.
