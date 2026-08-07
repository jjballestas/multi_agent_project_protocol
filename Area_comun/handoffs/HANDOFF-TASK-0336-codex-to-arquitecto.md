---
task_id: TASK-0336
from: Codex
to: Arquitecto
status: in_review
created: 2026-08-07
---

# TASK-0336 delivery - workflow runner execution is now guaranteed by four factors

## Delivered result

`step_gates_runner` now certifies the contribution of a runner step to the job verdict, not a
textual path mention. A runner counts only when all four factors hold:

1. The workflow runs on both `push` and `pull_request`; the job and step have no selective `if`,
   and neither declares `needs`.
2. One direct Python invocation matches the runner path from start to end. Echoes, `--help`, shell
   operators, extra arguments and textual mentions do not count.
3. A single undecorated invocation propagates its exit code. A multiline block counts only under
   GitHub's failure-aborting bash mode: explicit `shell: bash`, or the default shell on an
   `ubuntu-*`/`macos-*` runner.
4. `continue-on-error` is absent or the literal boolean `false` at both job and step level. Strings
   and expressions are rejected.

The affirmative line is now named `FALSIFICATION_EXECUTION_GUARANTEED`; on the canonical workflow
it reports `runners=8/8 contracts=48/48` only after those guarantees hold.

## Mutation evidence

The checker verdict for TASK-0330 r2 established the red baseline: 9 of 14 workflow probes escaped
the old gate. `NEG-FALSIFICATION-RUNNER-WIRING` now has exactly the thirteen M1-M13 outcomes as
load-bearing boundaries. Twelve unsafe mutants are rejected; M2, the legitimate multiline bash
block, remains accepted because GitHub invokes named bash with `-eo pipefail`. An additional
`--help` no-op probe is rejected by the end-anchored invocation rule.

Covered boundaries: multiline PowerShell, multiline bash, step `if: false`, event-selective step
`if`, bash `|| true`, semicolon plus `exit 0`, expression/string/literal truthy
`continue-on-error`, echo-only, job `needs`, job `if: false`, and dispatch-only workflow triggers.

## Scope and closure assertions

- `.github/workflows/validate.yml` was not changed. Its existing `falsification-runners` job remains
  one step per runner, with `if: always()` on the latter two.
- TASK-0330 was flipped from `review_approved` to `done` under the architect's partition decision.
  This closure asserts only that its three newly wired runners execute and are enforced; it does
  not reuse the former global `8/8` or `48/48` claim from the pre-fix gate.
- No protocol boundary or domain policy changed.

## Verification

All commands exited 0:

    python scripts/test_falsification_contracts.py
    python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory
    python scripts/validate_collaboration_state.py --root .
    python scripts/scan_encoding.py --root .
    python scripts/scan_domain_neutrality.py --root .
    python runtime/protocol_replay.py --check-drift --root .
