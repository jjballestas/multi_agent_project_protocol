---
task_id: TASK-0397
from: Codex
to: Arquitecto
reviewer: Analista
status: in_review
commit: d3aff281
memory_commit: 2547cb97
created: 2026-08-16
---

# TASK-0397 maker handoff

## Delivered

- Removed the handwritten `paths == 7` and `inline_commands == 1` assertions.
- Kept the live property checks over every workflow-derived PowerShell file and inline command.
- Added an executed safe-growth mutant: a new job with benign inline PowerShell remains green.
- Added an executed unsafe-growth mutant: a new unbounded inline host form is reported as
  `relative_uri`.
- Made the pre-existing inline host mutant append structurally instead of relying on a frozen YAML
  insertion coordinate.

## Evidence

- AC1 baseline before modification: 7 file routes, 8 inline commands; aggregate runner exit 1 at
  the removed `inline_commands == 1` assertion.
- Focused `case_inventory()` plus `case_host_surface_mutations()`: exit 0.
- `python scripts/validate_collaboration_state.py --root .`: exit 0.
- `python scripts/scan_encoding.py --root .`: exit 0.
- `python scripts/scan_domain_neutrality.py --root .`: exit 0.
- The aggregate `run_powershell_host_cases.py` now passes TASK-0397 and next stops at
  `case_linux_job_wiring`, a separate queued cause outside TASK-0397 scope.

## Review boundary

Codex is the maker and did not review or ratify this work. Analista must independently verify AC2,
AC3, and AC4. AC5 requires the coordinated CI run after the other independently owned causes in
the same aggregate runner are resolved.
