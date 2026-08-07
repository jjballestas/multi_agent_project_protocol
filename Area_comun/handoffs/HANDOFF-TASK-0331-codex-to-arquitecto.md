---
task_id: TASK-0331
from: Codex
to: Arquitecto
status: in_review
implementation_commit: 4e536ffcd3c6a3527d49c7475a43195fc957ab91
created_at: 2026-08-07T22:52:00Z
---

# HANDOFF TASK-0331 - scope-aware and atomic peer admission

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
This remediation removes archived tasks from that class; it does not claim every message is
resolvable.

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

Detached clean clone of `4e536ffcd3c6a3527d49c7475a43195fc957ab91` under
`D:/Aegis_Scratch/multi_agent_project_protocol/r331-4e536ffc`:

- `python scripts/test_exec_lease_harness.py` -> exit 0, 25/25 tests.
- `python scripts/check_falsification_contracts.py --root .` -> exit 0,
  52 permanent negatives / 52 declared / 0 missing at the exact commit.
- `python scripts/test_falsification_contracts.py` -> exit 0.
- `python scripts/validate_collaboration_state.py --root .` -> exit 0.
- `python scripts/scan_encoding.py` -> exit 0.
- `python scripts/scan_domain_neutrality.py --root .` -> exit 0.
- `git diff --check` -> exit 0; `git status --short` -> empty.

Codex is the maker only and did not review or ratify this implementation.

task_id: TASK-0331
status: in_review
executive_summary: Peer admission now compares declared material scope, fails closed on ambiguity, and atomically publishes a reservation before launch.
artifacts:
  - path_or_commit: 4e536ffcd3c6a3527d49c7475a43195fc957ab91
  - path_or_commit: Area_comun/handoffs/HANDOFF-TASK-0331-codex-to-arquitecto.md
gates:
  - command: python scripts/test_exec_lease_harness.py
    result: PASS
  - command: python scripts/check_falsification_contracts.py --root .
    result: PASS
  - command: python scripts/validate_collaboration_state.py --root .
    result: PASS
  - command: python scripts/scan_encoding.py
    result: PASS
  - command: python scripts/scan_domain_neutrality.py --root .
    result: PASS
  - command: git diff --check
    result: PASS
next_recommended: Arquitecto routes commit 4e536ffc to Analista for independent remediation review.
risks: Structurally unresolvable messages terminate deferred until manual rearm; disjoint execs share the Git working tree and may reach ledger operations concurrently, while submit_intent remains the ledger serializer.
