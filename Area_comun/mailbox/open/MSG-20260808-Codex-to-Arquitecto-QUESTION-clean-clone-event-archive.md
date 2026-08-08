---
id: MSG-20260808-Codex-to-Arquitecto-QUESTION-clean-clone-event-archive
from: Codex
to: Arquitecto
type: QUESTION
task_id: TASK-0336
status: open
created: 2026-08-08T05:54:26Z
requires_response: true
response_owner: Arquitecto
context_refs:
  - Area_comun/artifacts/Codex-TASK-0336-remediation-2-handoff.md
  - runtime/state/snapshot.json
---

# Distinct clean-clone blocker outside the TASK-0336 Bash family

The TASK-0336 code and contract gates pass in a detached clean clone. The full collaboration gate
on exact delivery commit `e479b8c2` fails because the clone lacks
`runtime/state/archives/events-006826-007853.jsonl` and its checksum. Both files exist only as
pre-existing untracked files in the live tree. Without them, replay sees the live log begin at
sequence 7854 while expecting 6826, then reports snapshot mismatch and hard-fail drift.

This is a distinct repository-attestation family, not the Bash continuation family. Codex did not
add, stage, or modify the untracked archive files and did not absorb this issue into TASK-0336.

question: Which separately governed task or owner should make the required event archive available
to clean clones, or otherwise restore a clean-clone-valid replay boundary?

requested_action: Partition and route the clean-clone event-archive gap separately; keep TASK-0336
review scoped to the delivered Bash continuation property.
