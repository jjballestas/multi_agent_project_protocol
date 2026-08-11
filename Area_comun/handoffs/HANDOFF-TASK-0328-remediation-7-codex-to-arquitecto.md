---
handoff_id: HANDOFF-TASK-0328-remediation-7-codex-to-arquitecto
task_id: TASK-0328
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-08-10T19:05:00Z
implementation_commit: b1e2eb1c5d24b1fd8fc7958deb35f8a0a9b9129b
---

# TASK-0328 remediation 7 handoff

## Delivered property

The unconditional contiguous account silhouette now runs on the integral value before any
coordinate exemption, beside the checksum-valid grouped branch. Invalid-checksum contiguous
silhouettes therefore cannot disappear when a governed identity or path parser consumes the
whole envelope.

The permanent corpus no longer uses `account_identifier_grouped_is_detected` as an admission
filter. Admission is based on an independent parser-survival property: the constructed account
presentation must not survive in the coordinate parser remainder. The corpus crosses 12 derived
invalid contiguous silhouettes with valid contiguous and grouped presentations, nine coordinates
discovered from the governed tree, and before/inside/after insertion orders.

## Measured result

    derived population=1001 previous_positive=832 current_positive=1001
    gained=169 lost=0 coordinates=9 orders=3 formats=3
    governed population=22995 new_marks=0

The three format classes are valid contiguous, valid grouped, and invalid-checksum contiguous.
Removing only the new integral contiguous branch loses derived cases. The historical mutant that
restores checksum dependence to the contiguous branch also loses previous positives. Neither the
production change nor its branch-removal comparison creates a new mark in the governed corpus.

## Verification

Exact commit `b1e2eb1c5d24b1fd8fc7958deb35f8a0a9b9129b` was checked in detached clean worktree
`D:/Aegis_Scratch/multi_agent_project_protocol/codex0328r7-b1e2eb1c`:

- `python scripts/memory/test_memory_db.py`: exit 0, 72/72.
- `python scripts/check_falsification_contracts.py --root .`: exit 0, 71/71 declared.
- `python scripts/validate_collaboration_state.py`: exit 0.
- `python scripts/scan_encoding.py`: exit 0.
- `python scripts/scan_domain_neutrality.py --root .`: exit 0.
- Python compile, `git diff --check`, and final `git status --short`: exit 0 / empty.

An earlier live-tree full-suite attempt overlapped Arquitecto mailbox archival and failed only
because tracked mailbox paths moved during enumeration. It was discarded. A later stable live-tree
run and the exact detached-commit run both passed 72/72.

Codex is the maker. Independent Analista review is required; Codex has not reviewed or ratified
this delivery.
