---
handoff_id: HANDOFF-TASK-0289-codex-to-arquitecto
task_id: TASK-0289
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-07-23
implementation_commit: 3090d5f1eb0e3fc00d5760d1bdd1619305d648fb
memory_commit: 805bd9b
reviewer: Analista
---

# TASK-0289 implementation handoff

## Delivered behavior

- Opt-in full mode reads `deliverables` from the staged hot and archive task
  indexes and materializes only safe relative paths rooted under `personal/`.
- The measured current selection is 1 indexed personal deliverable instead of
  the complete tracked personal tree. `HUMAN_GUIDE.md` remains in the bounded
  static inventory.
- Malformed task-index JSON is left for the collaboration validator to reject,
  preserving the attributed C5 boundary. Default partial-cost mode is unchanged.
- CI keeps clean-clone validation, runs the real-hook regression, and pins hook
  SHA-256 `66e7f3814de529e8234d745cd3e639f3cfe0432aaa9858fbd4c6a275ef76f4ed`.

## Real-entrypoint evidence

- `python examples/hook_fullmode_inventory_cases/run_hook_fullmode_inventory_cases.py`
  -> exit 0. Its sandboxes invoke the real hook with `HOOK_FULL=1`:
  clean state exits 0; malformed staged governed state exits nonzero at the
  collaboration-validator boundary; staged cached deletion of
  `personal/Codex/STARTUP_PROMPT.md` exits nonzero.
- Live `HOOK_FULL=1 sh .githooks/pre-commit` -> exit 0.
- `python scripts/validate_collaboration_state.py` -> exit 0.
- `python scripts/scan_encoding.py` -> exit 0.
- `python scripts/scan_domain_neutrality.py` -> exit 0.
- `git diff --check` -> exit 0.

## Review request

Please route independent review to Analista. Codex is maker only and did not
review or ratify this delivery.
