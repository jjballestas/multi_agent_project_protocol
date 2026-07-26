---
handoff_id: HANDOFF-TASK-0296-codex-to-arquitecto-remediation-1
task_id: TASK-0296
from: Codex
to: Arquitecto
status: ready
created_at: 2026-07-26
implementation_commit: 31680dd14b322a99a707c6322919cc0f7c30f535
---

# TASK-0296 remediation iteration 1

Commit `31680dd` fixes B1 without changing the previously verified detector hardening or the
pinned config. The scheduled-task installer now trims terminal path separators, applies Windows
argv escaping for embedded quotes and terminal backslashes, and prints the exact composed argument
line under `-WhatIf` and `-Verbose`. The monitor accepts scanner arguments both with and without the
optional `--` separator.

The Windows-guarded fixture invokes the real installer with terminal separators, reads its preview,
parses the argument line through `CommandLineToArgvW`, and asserts exact argv equality including
`--known-repo`, `--max-depth`, and `--allow-home`. It also proves separator-free monitor forwarding.

Verification exited 0:

- `python examples/scratch_discipline_cases/run_scratch_discipline_cases.py --scratch-root D:/Aegis_Scratch/multi_agent_project_protocol/task0296-remediation`
- `python scripts/scan_domain_neutrality.py`
- `python scripts/scan_encoding.py`
- `python scripts/validate_collaboration_state.py`
- trailing-separator reproduction: identical finding set with and without a terminal backslash
- `git diff --check`

Independent recomputation and Analista re-review are required. Codex did not review or ratify this work.
