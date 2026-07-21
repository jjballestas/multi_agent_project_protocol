---
handoff_id: HANDOFF-TASK-0281-iter3-codex-to-arquitecto
task_id: TASK-0281
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-07-21
implementation_commit: 8c70dbb
iteration: 3
---

# TASK-0281 iteration 3 handoff

## Result

The generic born-operational runner now reads `git status --porcelain=v1 -z`
through a child process whose stdout decoder is strict UTF-8, independent of the
console encoding. The same decoder serves the pre-exec residue gate and the
worktree disk proof.

If git reports a path that cannot be resolved, the residue gate returns `live`.
That ambiguity therefore defers execution and can no longer become
`staged_residue_aborted` or permit agent startup.

The live Codex and Analista harnesses were not redeployed.

## Permanent control and falsification

`examples/mailbox_retry_cases/run_mailbox_retry_cases.py` writes the extracted
probe outside the sandbox, so the probe cannot create its own fresh residue. It
then proves the real non-ASCII target returns `live`, mutates the decoder to
cp850 and confirms the unresolved-path fail-safe still returns `live`, and
combines that mutation with the former unsafe unresolved-path behavior. The
repaired control kills the combined mutant because it returns `aborted`.

## Verification by exit code

- `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py` -> 0
- `python scripts/validate_collaboration_state.py` -> 0
- `python scripts/scan_encoding.py` -> 0
- `python scripts/scan_domain_neutrality.py` -> 0

Codex is maker only and did not review or ratify this delivery. Route commit
`8c70dbb` to Analista for independent iteration-3 judgement.
