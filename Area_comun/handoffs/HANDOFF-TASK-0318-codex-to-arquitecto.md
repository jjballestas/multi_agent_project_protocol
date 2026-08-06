---
handoff_id: HANDOFF-TASK-0318-CODEX-TO-ARQUITECTO
task_id: TASK-0318
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-08-06T12:50:00Z
implementation_commit: 5a699bb837c99b087ca483962f81517128589196
---

# HANDOFF TASK-0318 - instance-extensible status vocabulary

## Result

Commit `5a699bb837c99b087ca483962f81517128589196` leaves the finite core status
vocabulary with only these generic lifecycle values:

    accepted | active | answered | approved | archived | blocked | cancelled |
    change_required | claimed | delivered | done | draft | final | for_decision |
    for_implementation | for_review | in_progress | in_review | ok | open |
    proposed | ready | ready_for_implementation | ready_for_independent_review |
    ready_for_review | reviewed | submitted | superseded

All eight hub-local values are absent from the core and declared only in the live governed
`MEMORY_INDEX_POLICY.json`: `DRAFT-PENDIENTE-DE-FIRMA-DEL-OPERADOR`, `GO-PROMOVER-OFF`,
`OK-CERRABLE`, `OK_CERRABLE`, `cambio-requerido`, `draft (pendiente GO operador)`,
`draft-reviewed-informal`, and `hallazgo-confirmado`. The shipped template declares an empty
`extra_status_values` array, so a new instance inherits none of them.

The policy is loaded once per artifact scan. The configured status set is the one-time union of
the finite core and the governed extension. The extension is bounded to 128 unique, trimmed,
printable values of at most 100 characters; duplicates of core values are rejected. Missing fields
from policies created before this addition default closed to an empty extension. There is no CLI,
environment, or corpus-learning path.

The permanent negative `NEG-MEMORY-INSTANCE-STATUS-DECLARATION` creates an artifact that is valid
only because its instance status is declared, removes that declaration, commits the mutated policy,
and requires the same artifact to warn again. The repository inventory discovers all 28 declared
negatives, and CI runs the complete memory suite beside the inventory and guardian controls.

No other enum, pinned configuration, registry, genesis, runtime implementation, validator, product
route, or protocol boundary changed. Codex is the maker only and did not review or ratify this work.

## Clean-clone evidence

Clean clone: `D:/Aegis_Scratch/multi_agent_project_protocol/task0318-clean-5a699bb`, exact commit
`5a699bb837c99b087ca483962f81517128589196`. Final `git status --porcelain` was empty.

The real build indexed 4,186 artifacts and 329 events and emitted exactly **219 warnings**. Fast
and full drift both reported 219 warnings; full drift reported `round_trip=pass` and
`sweep=bidirectional-pass`.

task_id: TASK-0318
status: in_review
executive_summary: Commit 5a699bb externalizes all eight hub-local statuses into a bounded governed instance policy, ships an empty template extension, and proves by permanent mutation that undeclared statuses warn again. The exact clean-clone corpus count is 219 warnings.
artifacts:
  - path_or_commit: 5a699bb837c99b087ca483962f81517128589196
  - path_or_commit: scripts/memory/build_memory_db.py
  - path_or_commit: scripts/memory/test_memory_db.py
  - path_or_commit: Area_comun/protocol/MEMORY_INDEX_POLICY.json
  - path_or_commit: Area_comun/protocol/MEMORY_INDEX_POLICY.template.json
  - path_or_commit: .github/workflows/validate.yml
gates:
  - command: python scripts/memory/test_memory_db.py
    result: PASS (59 tests, clean clone)
  - command: python scripts/memory/build_memory_db.py --root .
    result: PASS (4186 artifacts, 329 events, exactly 219 warnings)
  - command: python scripts/memory/check_memory_db_drift.py --fast --root .
    result: PASS (database_read=false, 219 warnings)
  - command: python scripts/memory/check_memory_db_drift.py --full --root .
    result: PASS (round_trip=pass, sweep=bidirectional-pass, 219 warnings)
  - command: python scripts/check_falsification_contracts.py --root . --inventory
    result: PASS (28 permanent negatives, 28 declared, 0 missing)
  - command: python scripts/scan_domain_neutrality.py --root .
    result: PASS
  - command: python scripts/scan_encoding.py --root .
    result: PASS
  - command: python scripts/validate_collaboration_state.py --root .
    result: PASS (one unrelated existing compact-mailbox context_refs warning)
  - command: git diff --check
    result: PASS
  - command: git status --porcelain
    result: PASS (empty after clean-clone gates)
next_recommended: Arquitecto recomputes commit 5a699bb and routes TASK-0318 to Analista for independent review.
risks: The extension remains intentionally finite and instance-governed; broadening other enums is out of scope.
