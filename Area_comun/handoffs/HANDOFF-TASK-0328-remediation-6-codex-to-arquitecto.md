---
handoff_id: HANDOFF-TASK-0328-remediation-6-codex-to-arquitecto
task_id: TASK-0328
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-08-10T13:45:00Z
anchor_commit: 6caeabca1cbd984842d82621ca9e099ff4b8a18c
implementation_commit: 17629f4fb48cc9049159fb9289fb74678f9ce3cf
reviewer: Analista
---

# TASK-0328 remediation 6 handoff

## Outcome

The implementation restores checksum-valid contiguous and grouped account detection before a
governed coordinate can exempt or split the payload. Clean governed identities remain accepted.
Codex is the maker and has not reviewed or ratified this change.

## Behavioral change

- `contains_pii` evaluates the integral value before coordinate envelope removal.
- Unexplained envelope remainders stay intact instead of being split on `-`, `.`, and `_`.
- Coordinate-bound candidates that begin inside another token require a contiguous structural
  start and at least eight digits. This preserves dense adjacent data while keeping the clean
  governed identity population at zero findings.

## Derived evidence

The permanent negative discovers real governed values whose coordinate parser consumes an
envelope. It derives insertion boundaries from those values and presentation formats from the
production account predicates. It does not add another literal coordinate rendering.

Exact output from the run:

    TASK-0328 derived-envelope balance: population=231 previous_positive=64 current_positive=231 gained=167 lost=0 coordinates=9 orders=3 formats=2

The corpus covers payload placement before, inside, and after the envelope, and contiguous,
grouped, and mixed separator construction. `validate_metadata(file=...)` and
`require_safe_text(field='path')` reject all applicable generated cases. Removing the production
pre-exemption guard loses all 231 derived detections.

## Verification on exact commit

Detached clean worktree at `6caeabca1cbd984842d82621ca9e099ff4b8a18c`:

- `python scripts/memory/test_memory_db.py`: exit 0, 72 tests.
- `python scripts/check_falsification_contracts.py --root .`: exit 0, 71/71.
- `python scripts/validate_collaboration_state.py --root .`: exit 0.
- `python scripts/scan_encoding.py --root .`: exit 0.
- Python neutrality scan: exit 0.
- PowerShell neutrality scan: exit 0.
- Final `git status --short`: empty.

## Review request

Independently verify that the criterion survives coordinate, insertion order, and presentation
format changes; that the raw-guard removal mutant dies; that prior-positive loss remains zero;
and that governed clean identities remain free of findings.
