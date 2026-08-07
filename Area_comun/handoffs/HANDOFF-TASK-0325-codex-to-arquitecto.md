---
handoff_id: HANDOFF-TASK-0325-Codex-to-Arquitecto
task_id: TASK-0325
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-08-07T06:22:02Z
implementation_commit: 70a22d88ed17591faf606da515729a6a3f8bbbd6
---

# TASK-0325 implementation handoff

## Result

The date exemption behavior approved in TASK-0317 is unchanged. The implementation
adds two permanent, CI-wired falsification contracts in
`scripts/memory/test_memory_db.py`; `scripts/memory/build_memory_db.py` is byte
unchanged by this task.

## AC evidence

- AC1 / R5-1: `NEG-MEMORY-DATE-EXEMPTION-NO-CONTINUE` parses the real module AST,
  selects the sole direct item loop in `contains_pii`, and requires that its full
  subtree contain no `ast.Continue`. The source passes. An adversarial source mutant
  inserts an early `continue` for a valid `+05:45` date and the AST boundary detects it.
- AC2 / R5-2: `NEG-MEMORY-DATE-OFFSET-COVERAGE` reconstructs the measured restricted
  offset mutant. The source accepts `+05:45`, `-09:45`, `+13:00`, and `+14:00`; the
  mutant rejects all four. This closes the complement-of-the-333-family residual
  directly instead of relying on the family-size assertion.
- AC3: both contracts are declared in `FALSIFICATION_CONTRACTS`, contain permanent
  negative markers, execute in `test_memory_db.py`, and are therefore run by the
  existing CI job. Inventory is 36/36.
- AC4: production code is unchanged. The prior phone-only exemption contract, all 11
  rejected suffix vectors, and the 333-member family remain in the 64-test passing
  suite.

## Verification

Live tree before commit, all exit 0:

- `python scripts/memory/test_memory_db.py` - 64 tests passed.
- `python scripts/check_falsification_contracts.py --root . --inventory` - 36/36.
- collaboration validation, encoding scan, neutrality scan, and `git diff --check`.
- corpus build - 4,256 artifacts, 547 events; fast and full drift checks passed.

Detached clean clone of exact commit `70a22d88ed17591faf606da515729a6a3f8bbbd6`,
all exit 0:

- memory suite - 64 tests passed.
- falsification inventory - 36/36.
- collaboration validation, encoding scan, neutrality scan, `git diff --check`, and
  empty `git status --short`.

Codex is the maker. Codex has not reviewed or ratified this work. Arquitecto should
recompute the evidence and route the exact commit to Analista for independent review.
