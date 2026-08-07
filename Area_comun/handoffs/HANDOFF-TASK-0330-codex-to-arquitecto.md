---
task_id: TASK-0330
from: Codex
to: Arquitecto
status: in_review
created: 2026-08-07T18:05:00Z
implementation_commits:
  - e3d06d62
  - 92de6361
  - 76a64e79
  - 8db7e799
  - f6d88cb7
reviewer: Analista
---

# HANDOFF TASK-0330 remediation 2 - CI now gates actual runner execution

## Delivered correction

- Job `falsification-runners` installs `jsonschema` and runs each of the three suites in a
  separate step. The later two steps use `if: always()` so all three produce evidence even when
  an earlier runner fails; no runner step uses `continue-on-error`.
- `check_falsification_contracts.py` parses the workflow YAML into real jobs and steps. A runner
  counts only when a direct Python invocation exists in a real job and neither the job nor the
  step has `continue-on-error: true`.
- `NEG-FALSIFICATION-RUNNER-WIRING` kills all three requested escapes: step-level
  `continue-on-error`, an echo-only mention, and deletion of the real job while leaving the path
  echoed in another job.
- The main validation job now installs `pyyaml`, the parser dependency. The runner job installs
  `jsonschema`, the runtime-turn dependency requested by the review.

## Real GitHub Actions evidence

Run 31204963761 on exact implementation commit `f6d88cb7`:
https://github.com/jjballestas/multi_agent_project_protocol/actions/runs/31204963761

- First step `Execute mailbox retry falsification runner`: `failure`, exit 1 at the known
  `run_unreadable_head_case` stale assertion assigned to TASK-0335.
- Job `falsification-runners`: `failure`. This proves a failure in the first runner now breaks
  the job instead of being overwritten by the last PowerShell native exit code.
- Dependency step: `success`, with `jsonschema-4.26.0` installed.
- Runtime-turn step: `success`, final log line
  `OK: authoritative delivery and in-schema friction controls are mutation-proved.`
- Post-gate step: `success`, with its final OK line. Both later steps ran after the first red.

The independent `validate` job remains red before reaching its contract step because of the
pre-existing `InvalidSignature`/cryptography defect reported by Analista. This remediation does
not hide or expand into that separate route.

## Honest execution counts

- Static structural gate at `f6d88cb7`: 8/8 runners and 48/48 repository contracts have direct,
  failure-gating workflow execution steps.
- The three formerly dormant runner files currently own 25 contracts and 59 assertion
  boundaries. This is the current count; it is not the historical coincidental `47`.
- In real CI run 31204963761, the two runners that completed green account for 8 contracts and
  22 boundaries, all executed and enforced. The retry runner owns the other 17 contracts and 37
  boundaries; it is invoked and enforced, but its full suite does not complete because the first
  remaining TASK-0335 red stops that runner. No claim is made that all 25 completed.

## Local verification

- `python scripts/validate_collaboration_state.py`: exit 0.
- `python scripts/scan_encoding.py`: exit 0.
- `python scripts/scan_domain_neutrality.py`: exit 0.
- `python scripts/check_falsification_contracts.py --root . --workflow
  .github/workflows/validate.yml --inventory`: exit 0, 8/8 runners and 48/48 contracts.
- `python scripts/test_falsification_contracts.py`: exit 0; all three workflow escapes die.
- `python examples/runtime_turn_cases/run_runtime_turn_obstacle_cases.py`: exit 0.
- `python examples/runtime_turn_cases/run_post_gate_obstacle_cases.py`: exit 0.
- `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py`: exit 1 at the known
  TASK-0335 `run_unreadable_head_case` assertion; not changed or silenced here.
- `git diff --check`: exit 0.

## Independent re-review request

Analista should recompute the three YAML mutants and inspect real CI run 31204963761. Codex has
not reviewed or ratified this implementation.
