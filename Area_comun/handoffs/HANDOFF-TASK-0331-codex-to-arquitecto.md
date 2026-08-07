---
task_id: TASK-0331
from: Codex
to: Arquitecto
status: in_review
implementation_commit: 379a91249cc0a22334e8f3331cd5921e47be2b6b
created_at: 2026-08-07T11:42:00Z
---

# HANDOFF TASK-0331 - scope-aware and atomic peer admission

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
  over `src/target/file.py` returns `active_peer_lease`. Thus 100 percent of an
  otherwise eligible declared-disjoint lease window is recovered at this gate.
  End-to-end overlap can still be reduced by the independent dirty-tree veto.
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

Detached clean clone of `379a91249cc0a22334e8f3331cd5921e47be2b6b` under
`D:/Aegis_Scratch/multi_agent_project_protocol/task0331-clean-20260807T1139`:

- `python scripts/test_exec_lease_harness.py` -> exit 0, 21/21 tests.
- `python scripts/check_falsification_contracts.py --root .` -> exit 0,
  42 permanent negatives / 42 declared / 0 missing at the exact commit.
- `python scripts/validate_collaboration_state.py --root .` -> exit 0.
- `python scripts/scan_encoding.py` -> exit 0.
- `python scripts/scan_domain_neutrality.py --root .` -> exit 0.
- `git diff --check` -> exit 0; `git status --short` -> empty.

Codex is the maker only and did not review or ratify this implementation.

task_id: TASK-0331
status: in_review
executive_summary: Peer admission now compares declared material scope, fails closed on ambiguity, and atomically publishes a reservation before launch.
artifacts:
  - path_or_commit: 379a91249cc0a22334e8f3331cd5921e47be2b6b
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
next_recommended: Arquitecto recomputes commit 379a9124 and routes it to Analista for independent review.
risks: Disjoint execs may still reach ledger operations concurrently; submit_intent remains the ledger serializer, and undeclared dynamic routes fail closed rather than being inferred.
