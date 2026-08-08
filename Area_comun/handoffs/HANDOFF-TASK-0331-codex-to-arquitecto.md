---
task_id: TASK-0331
from: Codex
to: Arquitecto
status: in_review
implementation_commit: a29e2ceae185b2370b31590cd5a2040113c0a224
created_at: 2026-08-08T14:35:00Z
---

# HANDOFF TASK-0331 - scope-aware and atomic peer admission

## Remediation iteration 5

Implementation commit: `a29e2ceae185b2370b31590cd5a2040113c0a224`.

- `lease_process_state_probe` now executes the real `Get-LeaseProcessState` through all three
  checker gaps: forced `Get-Process` failure, forced `StartTime` failure, and a live PID whose
  declared start time differs by seven seconds. Healthy results are respectively `unknown`,
  `unknown`, and `dead`.
- The permanent negative applies M1, M2, and M3 while preserving the old `return "unknown"`
  literals as unreachable code. M1 and M2 produce `dead` on their forced-error branch; M3 produces
  `live` for the reused-PID case. The old three-literal count is gone, and all three mutant
  behaviors are asserted.
- The TASK-0284 pre-gate contract discovers the exec-lock evidence writer from its effect
  (`$LockPath`, `$MessageName`, and `process_start_time_utc`) and resolves its invocation from
  `Invoke-PeerForMessage`. It requires that call after `Get-StagedResidueState`; the new mutant
  moves the intact call above the probe and dies. Helper identity is not part of the property.
- Once that contract stopped aborting early, the complete retry runner reached an existing
  Windows PowerShell failure: `File.Replace($temporaryPath, $Path, $null)` rejects the null backup
  when replacing an existing lock. `Write-AtomicUtf8NoBom` now supplies a unique sibling backup
  and cleans backup plus temporary paths in `finally`. The same complete runner now passes.
- The task verification declaration now includes the complete retry runner and both missing
  neutrality readers requested by Arquitecto.

Exact implementation commit `a29e2ceae185b2370b31590cd5a2040113c0a224` passed in detached clean
clone `D:/Aegis_Scratch/multi_agent_project_protocol/codex0331r5-a29e2cea-20260808T1426` with
empty status:

- `python scripts/test_exec_lease_harness.py` -> exit 0, 28/28 tests;
- `python scripts/check_falsification_contracts.py --root .` -> exit 0, 59/59, missing 0;
- `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py` -> exit 0;
- `python scripts/validate_collaboration_state.py --root .` -> exit 0;
- `python scripts/scan_domain_neutrality.py --root .` -> exit 0;
- `python scripts/test_scan_domain_neutrality.py` -> exit 0, 5/5 tests;
- `powershell scripts/scan_domain_neutrality.ps1 -Root .` -> exit 0;
- `python scripts/scan_encoding.py --root .`, Python compile, runtime drift, and
  `git diff --check` -> exit 0; runtime drift false at sequence 8033.

Re-judgement against the checker findings: B1 is closed by branch behavior and deaths for M1/M2/M3;
B2 is closed by effect-resolved order plus a moved-call mutant; B3 is closed by the widened task
gate. The production overwrite repair is exercised by the runner that B2 restored. Codex is the
maker only and did not review or ratify this remediation.

## Remediation iteration 3

Implementation commit: `4c4e26655df215e88d1befd4a3e325e452466849`.

- Running-lease publication and every heartbeat now write a complete sibling temporary file and
  replace the prior JSON. A reader sees the old or new complete document rather than the 0-byte
  `WriteAllText` window measured by the checker.
- Startup retries an unreadable lease three times. After that it removes artifacts only when a
  parseable lease or lock identity proves its process is dead. A live identity preserves both
  files with `SELF_HEAL_UNREADABLE_LEASE liveness=live action=preserve`; missing identity also
  preserves them with `liveness=unknown`. Proven-dead evidence removes them with the distinct
  `SELF_HEAL_ORPHAN_LEASE liveness=dead action=remove` event.
- The lock carries PID plus process-start identity: the supervisor while the reservation is being
  published and the child after launch. The existing-cron guard now runs before self-heal, so a
  redundant live supervisor cannot mutate the active instance's artifacts.
- `NEG-HARNESS-LIVE-UNREADABLE-LEASE-PRESERVED` starts real child processes and verifies that
  truncated, empty, and missing-reservation-deadline live leases are never removed. Its deadline
  selector mutant preserves safety but emits the live-unreadable event for the valid reserved
  control, making the regression observable and the gate red.
- `NEG-HARNESS-RESERVED-LEASE-SELF-HEAL` still proves three-restart convergence for the four orphan
  states, now with explicit dead-process evidence for unreadable artifacts. A mutant that discards
  that evidence leaves the truncated and empty cases present through all three restarts.

New boundary: an unreadable lease without parseable process identity is not declared orphaned. It
is preserved with `liveness=unknown` and requires operator intervention. This is deliberate
fail-closed behavior: unreadability alone cannot authorize deletion of a potentially live exec.

Exact implementation commit `4c4e26655df215e88d1befd4a3e325e452466849` passed in detached
clean clone `D:/Aegis_Scratch/multi_agent_project_protocol/task0331-r3-4c4e2665-codex`:

- exec-lease harness: 27/27 tests, exit 0;
- falsification inventory: 55 declared / 55 permanent / 0 missing, exit 0;
- falsification guardian, collaboration validator, encoding scan, neutrality scan, and diff check:
  exit 0;
- final clean-clone status: empty.

## Remediation iteration 2

Commit `9def32142513ebe81d1a7f81684838dc4456ac5a` closes G1-G4 from the independent
remediation-1 verdict:

- `Clear-StaleCronLockIfSafe` no longer requires a lock before inspecting an own lease. It parses
  a deadline only when `Test-LeaseProcessMatches` proves a live owner; unreadable leases converge
  through the same stale cleanup path.
- Exec publication creates the lock before the exclusive reservation lease. Normal cleanup and
  self-heal remove the lease before the lock, eliminating the reachable own-lease-without-lock
  window introduced by exclusive creation.
- `NEG-HARNESS-RESERVED-LEASE-SELF-HEAL` now executes three recovery rounds over all four required
  states: reserved without lock, truncated with lock, empty with lock, and reserved without
  `reservation_deadline`. Shipped code removes both artifacts in round 1 and stays clean in rounds
  2 and 3; the old lock-required/deadline-first/fail-only mutant leaves every lease present in all
  three rounds.
- The archive-resolution statement is corrected below with the checker's measured population. No
  claim is made that archive membership alone makes a message resolvable.

## Remediation iteration 1

Commit `4e536ffcd3c6a3527d49c7475a43195fc957ab91` preserves the original scope-aware
and atomic admission core and closes checker findings F1-F4:

- Startup self-heal reads `reservation_deadline` for `state=reserved`, so a hard death
  between reservation and process launch no longer leaves an own lease that survives every
  restart. The permanent negative restores the wrong running-deadline read and proves that both
  lock and lease then survive with `SELF_HEAL_FAIL`.
- Task work resolution searches the hot and archived task indexes as one fail-closed population.
  A permanent hot-only mutant cannot resolve the archived fixture. A task present zero or multiple
  times, an unreadable index, a missing task file, or missing `scope_routes` remains ambiguous.
- Routes containing `*`, `?`, `[` or `]` are ambiguous and veto. The glob-guard mutant makes both
  `*` and `src/**` pass as disjoint literals and is killed.
- The dirty-tree permanent negative now executes `Invoke-PeerForMessage`: live residue reaches
  `worktree_residue_live` with zero admission calls. A dead-wiring mutant leaves the guard text in
  source but reaches admission and is killed.

Message-loss boundary: `message_scope_ambiguous` remains a stable terminal defer cause. A message
without a valid task id, without a unique row across hot plus archive, without its task file, or
without resolvable `scope_routes` reaches `defer_terminal` and is not executed until manual rearm.
The archive lookup resolves only archived tasks whose contracts declare `scope_routes`: the
checker measured 228 of 1,033 archived-task messages recovered, while 272 of 365 archived task
contracts lacked `scope_routes`. A message whose hot or archived task lacks that declaration
remains terminally deferred until manual rearm.

Measured overlap boundary: the checker measured 255.2 minutes (4 h 15 min), 60 percent of 422.2
deferred minutes, as the ceiling attacked by TASK-0331. Actual recovered overlap is only the
declared-disjoint subset. The shared working tree and `.git/index` remain undeclared dynamic
resources; the dirty-tree check is a pre-admission sample, not a lifetime lock. Concurrent ledger
writes remain serialized by the real `submit_intent` file lock in this authoritative instance.

## Result

Commit `379a91249cc0a22334e8f3331cd5921e47be2b6b` replaces both unconditional
peer vetoes with fail-closed material-route comparison and replaces the launch
check-then-act race with one atomic check-and-reserve critical section.

- Claim and lease routes normalize separators, remove claim fragments, compare
  exact or ancestor/descendant paths, and ignore only runtime-authoritative ledger
  containers. Treating the common ledger containers as material overlap would
  serialize every task; `submit_intent` remains their single-writer mechanism.
- A message derives its work from the canonical task `scope_routes` plus its task
  file. A live external claim or lease blocks only on an intersection with that
  work. A missing task, missing declared scope, unreadable JSON, missing/empty
  claim scope, non-array claim scope, or ambiguous lease still blocks.
- Every running lease now publishes `task_id`, normalized `work_scope`, and state.
  Before process launch, the peer acquires a shared `FileMode.CreateNew` admission
  file with `DeleteOnClose`, rechecks all claims and leases inside that critical
  section, and atomically creates its per-peer reservation lease before releasing
  admission. A second overlapping peer therefore sees either admission busy or the
  first reservation; it cannot pass the same empty snapshot.
- The dirty-tree check still runs before admission. No-claim and disjoint-scope
  results are not permission to bypass that separate fail-closed veto.

## Acceptance and falsification evidence

- AC1/AC2/AC5: the old unconditional claim behavior is the over-veto mutant. It
  returns `active_external_claim` for `src/other/file.py`; shipped code returns
  `none`. The opposite mutant lets `src/target/file.py` pass; shipped code blocks.
- AC2b: an alive peer lease over `src/other/file.py` returns `none`; the same lease
  over `src/target/file.py` returns `active_peer_lease`. The measured 255.2-minute
  figure is a ceiling; only its declared-disjoint subset is recoverable, and the
  independent dirty-tree veto can reduce end-to-end overlap further.
- AC3: missing, empty, and non-array claim scope all return
  `active_external_claim`; invalid claim JSON returns `claims_unreadable`.
  An unresolvable live lease returns `active_peer_lease`.
- AC4: `NEG-HARNESS-DIRTY-VETO-PRECEDES-SCOPE-ADMISSION` kills a mutant that
  disables the live-residue guard and verifies that the guard precedes admission.
- AC4b: two real PowerShell processes are released by the same gate against one
  overlapping task. Shipped shared admission admits exactly 1 and leaves 1 lease.
  A peer-specific-lock mutant admits 2 and leaves 2 leases. This test passed in
  three consecutive full harness runs before delivery.
- AC5: the four new permanent negatives are inventoried and already CI-wired
  through the existing exec-lease harness and falsification steps.

## AC4c - exact guarantee boundary

The change guarantees atomic serialization of the peer launch decision and
reservation publication. Two simultaneous peers cannot both decide from the same
pre-reservation snapshot. Overlapping declared material scopes cannot run together;
disjoint declared material scopes may run together after serialized admission.

It does not globally serialize the complete exec lifetime, does not prevent two
disjoint peers from reaching ledger operations concurrently, and does not infer
undeclared dynamic routes. Runtime-authoritative `submit_intent` remains responsible
for atomic ledger writes. Ambiguous or absent declarations fail closed, and the
dirty-tree veto remains independent and stricter.

## Exact-commit gates

Detached clean clone of `4c4e26655df215e88d1befd4a3e325e452466849` under
`D:/Aegis_Scratch/multi_agent_project_protocol/task0331-r3-4c4e2665-codex`:

- `python scripts/test_exec_lease_harness.py` -> exit 0, 27/27 tests.
- `python scripts/check_falsification_contracts.py --root .` -> exit 0,
  55 permanent negatives / 55 declared / 0 missing at the exact commit.
- `python scripts/test_falsification_contracts.py` -> exit 0.
- `python scripts/validate_collaboration_state.py --root .` -> exit 0.
- `python scripts/scan_encoding.py` -> exit 0.
- `python scripts/scan_domain_neutrality.py --root .` -> exit 0.
- `git diff --check` -> exit 0; `git status --short` -> empty.

Codex is the maker only and did not review or ratify this implementation.

task_id: TASK-0331
status: in_review
executive_summary: Remediation 5 replaces the verdict count with real branch behavior, binds pre-gate order to the resolved lock-write effect, and restores the complete retry runner. The checker M1/M2/M3 and moved-write mutant now die.
artifacts:
  - path_or_commit: a29e2ceae185b2370b31590cd5a2040113c0a224
  - path_or_commit: Area_comun/handoffs/HANDOFF-TASK-0331-codex-to-arquitecto.md
gates:
  - command: python scripts/test_exec_lease_harness.py
    result: PASS
  - command: python scripts/check_falsification_contracts.py --root .
    result: PASS
  - command: python examples/mailbox_retry_cases/run_mailbox_retry_cases.py
    result: PASS
  - command: python scripts/validate_collaboration_state.py --root .
    result: PASS
  - command: python scripts/scan_domain_neutrality.py --root .
    result: PASS
  - command: python scripts/test_scan_domain_neutrality.py
    result: PASS
  - command: powershell scripts/scan_domain_neutrality.ps1 -Root .
    result: PASS
  - command: python scripts/scan_encoding.py --root .
    result: PASS
next_recommended: Arquitecto routes commit a29e2cea to Analista for independent remediation-5 review before any closure.
risks: The 24 declared table cells still contain 18 distinct fixtures by deliberate observational convergence; unreadable owner evidence remains fail-closed and may require operator recovery.
