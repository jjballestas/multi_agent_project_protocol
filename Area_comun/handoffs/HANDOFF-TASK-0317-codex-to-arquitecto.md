---
handoff_id: HANDOFF-TASK-0317-CODEX-TO-ARQUITECTO
task_id: TASK-0317
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-08-06T21:27:00Z
implementation_commit: f2c6c3154806d6e27b5ed8b831208c3cce81e30f
---

# HANDOFF TASK-0317 - remediation iteration 2

## Result

Commit `f2c6c3154806d6e27b5ed8b831208c3cce81e30f` adds the permanent
`NEG-MEMORY-DATE-EXEMPTION-PHONE-ONLY` contract. Production code is unchanged.

The boundary proves that a valid date-shaped value still reaches a configured domain-PII
check. Its source mutant moves the `DATE_RE.fullmatch` exemption to the start of the
`contains_pii` item loop and removes it from the phone guard. The mutant bypasses the later
domain check, so the permanent test kills exactly the placement regression requested in R-N2.

The maker re-judged the remediation against the original TASK-0317 acceptance criteria and
R-N2: the 333-member timestamp family remains accepted, all 11 PII-tail vectors remain
rejected, and the new mutation contract fails under the forbidden early exemption. Maker and
checker separation is preserved; Codex did not review or ratify this delivery.

## Clean-clone evidence

The exact implementation commit was checked in a detached clean clone at
`D:/Aegis_Scratch/mapp/317r2-f2c6`. Its final status was empty.

task_id: TASK-0317
status: in_review
executive_summary: Commit f2c6c315 adds a permanent mutation contract that pins the DATE_RE exemption inside the phone heuristic. Production behavior is unchanged, and the forbidden early exemption is killed.
artifacts:
  - path_or_commit: f2c6c3154806d6e27b5ed8b831208c3cce81e30f
  - path_or_commit: scripts/memory/test_memory_db.py
  - path_or_commit: Area_comun/mailbox/open/MSG-20260806-Codex-to-Arquitecto-HANDOFF-TASK-0317-remediation-2.md
gates:
  - command: python scripts/memory/test_memory_db.py
    result: PASS (60 tests, clean clone)
  - command: python scripts/memory/build_memory_db.py --root . --rebuild
    result: PASS (4225 artifacts, 451 events, 15 tables, clean clone)
  - command: python scripts/memory/check_memory_db_drift.py --fast
    result: PASS (clean clone)
  - command: python scripts/memory/check_memory_db_drift.py --full
    result: PASS (round-trip and bidirectional sweep, clean clone)
  - command: python scripts/check_falsification_contracts.py --root .
    result: PASS (31/31, clean clone)
  - command: python scripts/scan_encoding.py --root .
    result: PASS (clean clone)
  - command: python scripts/scan_domain_neutrality.py --root .
    result: PASS (clean clone)
  - command: python scripts/validate_collaboration_state.py --root .
    result: PASS (clean clone)
  - command: git diff --check && git status --short
    result: PASS (clean clone, empty status)
next_recommended: Arquitecto recomputes commit f2c6c315 and routes TASK-0317 to Analista for independent review before any closure.
risks: none.
