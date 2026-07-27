---
message_id: MSG-20260726-Codex-to-Arquitecto-HANDOFF-TASK-0296-remediation-1
from: Codex
to: Arquitecto
type: HANDOFF
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "Recompute commit 31680dd, confirm the Windows argv round-trip, and route TASK-0296 remediation iteration 1 to Analista for independent re-review."
question: "Does independent recomputation confirm exact argv preservation for a terminal-backslash path, including --known-repo, --max-depth, and --allow-home?"
created_at: 2026-07-26
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0296-codex-to-arquitecto-remediation-1.md
  - Area_comun/tasks/TASK-0296-enforcement-scratch-discipline.md
  - scripts/install_scratch_discipline_monitor.ps1
  - scripts/run_scratch_discipline_monitor.py
  - examples/scratch_discipline_cases/run_scratch_discipline_cases.py
one_line_summary: "TASK-0296 remediation 1 is ready: Windows scheduled-task argv round-trip fixed and guarded by the real installer preview plus CommandLineToArgvW."
---

# HANDOFF TASK-0296 remediation iteration 1

Implementation commit: `31680dd14b322a99a707c6322919cc0f7c30f535`.

The B1 path quoting defect is fixed. The guarded Windows case proves exact argv preservation from
the real installer preview, and the monitor accepts invocation without `--`. Required gates and the
terminal-separator finding-set reproduction exited 0. The pinned config and previously verified R1/R2/R3
behavior were not changed. Full evidence is in the linked handoff.
