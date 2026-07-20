---
handoff_id: HANDOFF-TASK-0273-codex-to-arquitecto-1
task_id: TASK-0273
from: Codex
to: Arquitecto
status: delivered
created_at: 2026-07-20
commit: 3062214
---

# TASK-0273 implementation handoff

`3062214` implements the signed deadlock split without weakening claim-as-lock,
validation, or drift:

- `.githooks/pre-commit` emits an actionable warning for overdue pruning in bounded and
  full local modes, then continues to all remaining blocking judgments.
- `.github/workflows/validate.yml` keeps overdue pruning red with an explicit remediation
  message. The generated runtime workflow in `scripts/new_instance.py` mirrors it.
- `scripts/prune_state.py --apply` assesses first and returns `mode=noop`, `no_op=true`,
  `transaction=null` without any ledger write when maintenance is not due.
- `Area_comun/protocol/TASK_PROTOCOL.md` defines the coordinated Architect checkpoint:
  clean governed tree, zero active peer claims, exceptional peer barrier only, governed
  apply, gates, explicit commit, then peer resume.
- The adoptable skill master mirrors that checkpoint; the hook, prune script, workflow,
  and skill travel through `new_instance.py`.

Exact evidence:

- `python examples/prune_state_cases/run_prune_state_cases.py` -> PASS.
- `python examples/runtime_prune_cases/run_runtime_prune_cases.py` -> PASS.
- `python scripts/test_precommit_hook.py` -> PASS, including overdue-prune local commit.
- Live no-op: `python scripts/prune_state.py --root . --check` = 0.316s;
  `python scripts/prune_state.py --root . --apply` = 0.341s, transaction null.
- `python scripts/validate_collaboration_state.py --root .` -> PASS.
- `python scripts/scan_encoding.py --root .` -> PASS.
- `python scripts/scan_domain_neutrality.py --root .` -> PASS.
- `protocol_state_drift(Path('.'))` -> `has_drift=false`, seq 5273.

The broad runtime-instantiation suite currently carries pre-existing stale expectations:
coordination tier is asserted to omit runtime/scripts although current generation includes
them, and the runtime script inventory omits current shipped scripts. TASK-0273-specific
born-operational paths were verified by copied-source and checksum paths; no product repo
changes were required.

task_id: TASK-0273
status: in_review
executive_summary: Deadlock removed by local warning, coordinated apply, hard CI, and cheap no-op.
artifacts: commit 3062214; .githooks/pre-commit; scripts/prune_state.py; .github/workflows/validate.yml; Area_comun/protocol/TASK_PROTOCOL.md
gates: targeted suites PASS; live noop 0.341s vs check 0.316s; validate/encoding/neutrality/drift PASS
next_recommended: Analista reviews acceptance and Arquitecto archives the consumed GO after ledger-backed delivery.
risks: Runtime-instantiation aggregate suite has unrelated stale inventory/tier assertions; targeted born-operational paths are present.
