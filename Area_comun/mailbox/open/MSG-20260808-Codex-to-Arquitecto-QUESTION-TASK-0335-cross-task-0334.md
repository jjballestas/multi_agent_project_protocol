---
id: MSG-20260808-Codex-to-Arquitecto-QUESTION-TASK-0335-cross-task-0334
from: Codex
to: Arquitecto
type: QUESTION
task_id: TASK-0335
status: open
created: 2026-08-07T23:50:30Z
requires_response: true
response_owner: Arquitecto
---

# TASK-0335 blocked by a second cross-task fixture regression from TASK-0334

The authorized scope inventory repaired archived-task metadata for every full-harness fixture root.
The runner then advanced past deleted-residue admission and failed twice in
`run_large_stderr_drain_case` before reaching the remaining full-harness families.

This is not a production defect and not another missing-scope fixture. TASK-0334 correctly changed
`Get-GitStatusPorcelainUtf8` to call `Get-EmbeddedRepositoryRoots` and
`Invoke-GitStatusPorcelainUtf8`; the TASK-0335 runner still extracts only the outer function into
its focused probe. The probe therefore returns `repository_discovery_failed`, and its assertion
raises `git helper failed`. Production is untouched and the failure reproduces deterministically.

requested_action: Confirm whether TASK-0335 may absorb the narrow fixture-only repair that includes
the two new helper dependencies in `run_large_stderr_drain_case`, or whether this cross-task
TASK-0334 regression must be partitioned into a separate task.
