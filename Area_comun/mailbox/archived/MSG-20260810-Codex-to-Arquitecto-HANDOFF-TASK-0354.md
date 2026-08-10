---
id: MSG-20260810-Codex-to-Arquitecto-HANDOFF-TASK-0354
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0354
status: archived
created: 2026-08-10T03:30:00Z
requires_response: true
response_owner: Arquitecto
requested_action: Route implementation commit a583e189 to an independent checker; retain AC1 as pending behavioral evidence until Actions billing is available.
question: Does the independent checker confirm the runner-by-runner placement and the declared cancellation residual?
context_refs:
  - Area_comun/tasks/TASK-0354-concurrencia-y-colocacion-de-jobs-en-el-workflow.md
  - .github/workflows/validate.yml
---

# HANDOFF TASK-0354 -- workflow concurrency and host-derived runner placement

Implementation commit: `a583e189`.

## Delivered behavior

- Workflow concurrency key: `validate-${{ github.workflow }}-${{ github.ref }}`.
- `cancel-in-progress: true` cancels an older run of the same workflow and ref when a newer run starts.
- `run_mailbox_retry_cases.py` stays in `falsification-runners` on `windows-latest` because it
  directly invokes `powershell.exe` and exercises the Windows PowerShell 5.1 cron path.
- `run_runtime_turn_obstacle_cases.py` moves to `falsification-runners-python` on `ubuntu-latest`;
  its external process dependency is Git.
- `run_post_gate_obstacle_cases.py` moves to `falsification-runners-python` on `ubuntu-latest`;
  it is Python-only.

## Coverage and falsification evidence

- Workflow-derived Python example command sets before and after are equal: 62 runners in each,
  with no added or removed command.
- Derived placement assertion passes for all three runners: mailbox retry -> Windows; runtime turn
  and post-gate -> Ubuntu.
- The mailbox retry source still invokes `powershell.exe` directly and contains no `shutil.which`
  or `FileNotFoundError` availability bypass.
- All three runners pass locally:
  - `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py`
  - `python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py`
  - `python examples/runtime_turn_cases/run_post_gate_obstacle_cases.py`
- Full workflow replay balance is unchanged after the implementation commit: before 60 PASS / 9
  FAIL / 8 UNSUPPORTED; after 60 PASS / 9 FAIL / 8 UNSUPPORTED. Residual failed steps are 34, 36,
  39, 40, 43, 50, 53, 58, and 59. Unsupported PowerShell steps are 6, 7, 12, 19, 20, 21, 73,
  and 77.
- Collaboration validation, encoding scan, neutrality scan, YAML parse, and diff checks exit 0.

## Explicit residual and tradeoff

AC1 is not yet accredited. The YAML change is present, but behavioral proof requires two rapid
pushes and the first Actions run observed in `cancelled` state. Actions billing remains outside
this task and unavailable by operator instruction, so that proof must be collected after billing
is restored.

Cancellation means intermediate commits in a burst are not each validated. This instance gates
the HEAD tree, so that is accepted; the cost is reduced granularity when bisecting a future
regression.

Codex is the maker and has not reviewed or ratified this implementation.
