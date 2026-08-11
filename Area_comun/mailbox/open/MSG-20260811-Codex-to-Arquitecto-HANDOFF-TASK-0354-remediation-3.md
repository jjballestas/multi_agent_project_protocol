---
id: MSG-20260811-Codex-to-Arquitecto-HANDOFF-TASK-0354-remediation-3
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0354
status: open
created: 2026-08-11T12:25:00Z
requires_response: true
response_owner: Arquitecto
requested_action: Route independent Analista re-review of implementation commit 736b03f2; Codex is maker only.
question: Does G1 now discover direct and module Python invocations at any line position and fail on a runner-count decrease?
context_refs:
  - Area_comun/tasks/TASK-0354-concurrencia-y-colocacion-de-jobs-en-el-workflow.md
  - Area_comun/artifacts/Analista-TASK-0354-r2-gate-dependencias-verdict.md
  - .github/workflows/validate.yml
---

# HANDOFF TASK-0354 remediation 3

Implementation commit `736b03f2` closes the operator-authorized G1 scope. The dependency gate now
tokenizes every line of each workflow `run` block, recognizes Python at any token position, accepts
direct `.py` entry points and `python -m` module entry points, and resolves both forms to the runner
file before checking imports.

The informational counter is now an invariant: the workflow declares 73 expected runner
invocations and fails when discovery differs. A runner-removal mutant produced expected 73 versus
discovered 72 and EXIT=1.

The two checker escapes were executed against the gate extracted from the workflow:

- `cd . && python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py` with `pyyaml`
  removed: dependency diagnostic for `yaml`, EXIT=1;
- `python -m examples.runtime_turn_cases.run_runtime_turn_obstacle_cases` with `pyyaml` removed:
  the same dependency diagnostic, EXIT=1.

The intact gate passed with `runners=73`. The falsification inventory passed 73/73. Exact commit
`736b03f2` passed in a detached clean Aegis worktree with empty tracked status: collaboration,
encoding, Python neutrality, Windows PowerShell neutrality, drift, diff, and the focused dependency
gate all exited 0.

The unrestricted 78-step `validate` replay completed at 60 PASS, 10 FAIL, and 8 UNSUPPORTED. The
changed dependency gate passed at step 3 and `prune_state.py` passed at step 18. The red steps are
runtime/materialization/harness suites outside the two touched files; the unsupported steps require
`pwsh`, which is unavailable on this host. This replay is residual diagnostic evidence, not a green
acceptance claim.

G2 is explicitly declared out of scope in the task artifact. The covered surface ends at the
discovered runner file; transitive local imports and child processes require another mechanism and
task. Codex has not reviewed or ratified this remediation.
