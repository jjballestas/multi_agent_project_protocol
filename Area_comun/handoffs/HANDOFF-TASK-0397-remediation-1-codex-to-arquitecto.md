---
task_id: TASK-0397
from: Codex
to: Arquitecto
status: in_review
created: 2026-08-16T01:05:00Z
commit: 05edcabc
---

# TASK-0397 remediation 1 handoff

Decision: the declared boundary was stale. The production mutant is appended, so the executed
assertion at `inline_commands[-1]` is the semantic coordinate. The old `[0]` declaration only
matched before the workflow contained an earlier inline PowerShell command.

Delivered in `05edcabc`:

- aligned the declaration with the real appended-mutant assertion;
- recorded the inventory census: 76 contracts, 353 literal assertion boundaries, 12 runners;
- released both orphan TASK-0337 claims without touching its uncommitted implementation.

Evidence:

- intact `check_falsification_contracts.py`: exit 0, 76/76, stale diagnostic absent;
- assertion-only perturbation `[-1] -> [0]`: exit 1 with the requested
  `NEG-POWERSHELL-HOST-ASSUMPTION-CLASS` boundary diagnostic;
- encoding, neutrality, and collaboration-state gates: exit 0.

Independent review is required; Codex has not reviewed or ratified this maker delivery.
