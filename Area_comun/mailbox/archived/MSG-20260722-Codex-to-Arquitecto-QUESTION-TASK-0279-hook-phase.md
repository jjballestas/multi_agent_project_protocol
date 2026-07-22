---
message_id: MSG-20260722-Codex-to-Arquitecto-QUESTION-TASK-0279-hook-phase
from: Codex
to: Arquitecto
type: QUESTION
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "Resolve the hook-phase contradiction for TASK-0279: Git pre-commit receives no message-file argument and runs before the proposed commit message is finalized; authorize .githooks/commit-msg as the aborting trailer gate, while keeping .githooks/pre-commit for staged-snapshot checks."
question: "Do you authorize implementing the reliable abort in .githooks/commit-msg instead of reading stale COMMIT_EDITMSG from .githooks/pre-commit?"
created_at: 2026-07-22
context_refs:
  - Area_comun/tasks/TASK-0279-trailers-gate-precommit-aborta.md
  - .githooks/pre-commit
one_line_summary: "TASK-0279 is blocked on a Git lifecycle contradiction: pre-commit cannot reliably validate the pending commit message; commit-msg can abort with the finalized message."
---

# QUESTION - TASK-0279 reliable hook phase

Evidence from a real commit fixture: during `pre-commit`, `.git/COMMIT_EDITMSG` still contained
the previous commit message, so a valid pending `Task-Id: TASK-0278` commit was rejected as missing
its trailer. Git gives the finalized message path to `commit-msg`, whose non-zero exit aborts the
commit before creation and preserves the requested correction point.

One decision is required: authorize `.githooks/commit-msg` as the aborting trailer gate. The existing
`.githooks/pre-commit` remains the staged-snapshot gate, and born-operational export installs both.
