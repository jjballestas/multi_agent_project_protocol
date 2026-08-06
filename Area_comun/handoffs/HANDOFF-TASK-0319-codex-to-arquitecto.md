---
handoff_id: HANDOFF-TASK-0319-CODEX-TO-ARQUITECTO
task_id: TASK-0319
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-08-06T14:18:00Z
implementation_commit: a7c6e96317a07b2e6316d96e28b2b70741763c51
---

# HANDOFF TASK-0319 - stable-cause wall-clock pre-exec defer budget

## Result

Commit `a7c6e96317a07b2e6316d96e28b2b70741763c51` removes pre-exec defers from
`MaxTransientRetries`. Actual transient exec failures still consume `attempts` and retain the
existing count budget. A pre-exec veto instead records `defer_reason` and `defer_started_at`, resets
when the cause changes or one observation reaches the executable path, and becomes terminal only
when the same cause survives `PreExecDeferTimeoutSeconds`.

The default is 7,200 seconds: twice the existing 3,600-second exec deadline and safely above the
observed 30-60 minute peer turns. A genuinely stuck unchanged cause still reaches
`defer_terminal`. The dirty-tree veto, active external claim veto, active peer lease veto, and
single-exec lock remain intact.

`worktree_residue_live` now records `paths_json` with at most 10 causal paths. An active live lease
records `peer=<owner>`. Another peer's `personal/<id>/` tree is removed from residue computation,
while the invoking peer's own personal tree remains visible.

## AC evidence

- AC1: the permanent negative seeds the historical mixed sequence at `defers=2` under
  `active_peer_lease`, changes the cause to `worktree_residue_live`, and applies the old shared-count
  mutant. The mutant reaches its third defer and becomes terminal; the fixed implementation resets
  to defer 1 and stays eligible. The fixture runs under the designated scratch root on Windows.
- AC2: the same behavioral probe preserves `attempts=2` across pre-exec defers and clear/reset;
  `MaxTransientRetries` is absent from the fixed pre-exec terminal predicate.
- AC3/AC4: a cause change resets defer count and clock; a clear observation resets defer state; the
  same cause seeded beyond a 300-second test budget reaches `defer_terminal`.
- AC5: the residue probe retains only 10 own causal paths, and the live-lease probe emits
  `peer=Analista`.
- AC6: foreign `personal/Analista/**` residue is ignored, while `personal/Codex/**` residue remains
  live and diagnostic.
- AC7: the behavioral probe confirms `active_external_claim`; source contract tests retain the live
  lease veto, lock, PID guard, and process-tree termination.
- AC8: `new_instance.copy_peer_harness` exports a byte-identical generic runner. CI now runs the
  13-case harness suite, and `NEG-HARNESS-PREEXEC-DEFER-STARVATION` is declared in the 29/29
  falsification inventory.

Codex is the maker only and did not review or ratify this work.

task_id: TASK-0319
status: in_review
executive_summary: Commit a7c6e96 replaces the shared three-poll pre-exec budget with a resettable stable-cause wall-clock budget while preserving bounded terminal handling and every single-writer veto. The permanent mutant reproduces the old mixed-cause starvation and is killed by the fixed behavior.
artifacts:
  - path_or_commit: a7c6e96317a07b2e6316d96e28b2b70741763c51
  - path_or_commit: scripts/harness/peer_mailbox_cron.ps1
  - path_or_commit: scripts/harness/README.md
  - path_or_commit: scripts/test_exec_lease_harness.py
  - path_or_commit: .github/workflows/validate.yml
gates:
  - command: python scripts/test_exec_lease_harness.py
    result: PASS (13 cases, including old-counter mutant, stable timeout, reset, diagnostics, veto, and export)
  - command: python scripts/check_falsification_contracts.py --root . --inventory
    result: PASS (29 permanent negatives, 29 declared, 0 missing)
  - command: python scripts/scan_encoding.py --root .
    result: PASS
  - command: python scripts/scan_domain_neutrality.py --root .
    result: PASS
  - command: python scripts/validate_collaboration_state.py --root .
    result: PASS (two unrelated existing compact-mailbox context_refs warnings)
  - command: git diff --check
    result: PASS
  - command: python examples/mailbox_retry_cases/run_mailbox_retry_cases.py
    result: FAIL (pre-existing fixture omits mandatory CoordinatorId and exits before exercising TASK-0319)
next_recommended: Arquitecto recomputes commit a7c6e96 and routes TASK-0319 to Analista for independent review; separately repair the stale mailbox-retry fixture invocation before treating that optional suite as evidence.
risks: The legacy mailbox-retry runner is independently red because its real-loop fixture omits the already-mandatory CoordinatorId; its older count-based defer expectations also require a separately scoped alignment with this approved contract.
