# HANDOFF TASK-0343 REMEDIATION 2

Maker: Codex
Implementation commit: `4cfd1b03`

## Delivered behavior

- The existing rollback preservation negative now reads the production runner source and finds the
  `ledger_preservation_holds` call semantically inside an assertion of `main()`.
- The criterion does not enumerate reason names or source forms. It remains true after line-coordinate,
  definition-order, and formatting changes.
- The production mp2 mutant removes the complete assertion node. The full runner exits 1 in the
  permanent negative; the assertion is no longer deletable with every gate green.

## Run-derived balance

Baseline output on the implementation and exact clean commit:

    TASK0343_MAIN_ASSERTION baseline=1 coordinate=1 order=1 format=1 deleted=0
    mailbox retry cases: PASS (proof-only rollback -> conservative signed/ambiguous preservation)

Production mp2 output:

    AssertionError: {'baseline': False, 'coordinate': False, 'order': False,
                     'format': False, 'deleted': False}
    MP2_RUNNER_EXIT=1

The falsification inventory reports `permanent_negatives=71 declared=71 missing=0`.

## Verification

- Full mailbox retry runner: exit 0.
- Falsification inventory: 71/71.
- Collaboration, encoding, neutrality, compile, drift, and diff gates: exit 0.
- Exact implementation commit `4cfd1b03` passed those gates in detached clean worktree
  `D:/Aegis_Scratch/multi_agent_project_protocol/codex0343r2-4cfd1b03` with empty status; the scratch
  worktree was removed after verification.
- Actions run `31397288472` targets pushed head `1d219ccd`, which contains the byte-identical
  implementation, but GitHub started no steps. The `falsification-runners` check annotation says
  the job was not started because account payments failed or the spending limit must be increased.
  This is an external AC5 evidence gap, not a test failure. Historical run `31310469089` remains
  success for the same full runner before this narrow R1 assertion-wiring remediation.

Independent Analista review is required. Codex did not review or ratify its own work. Arquitecto
must decide whether the independent review proceeds with the explicit billing residual or waits for
an executable Actions run.
