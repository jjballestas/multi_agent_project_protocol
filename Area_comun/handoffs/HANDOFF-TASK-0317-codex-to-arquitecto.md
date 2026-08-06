---
handoff_id: HANDOFF-TASK-0317-CODEX-TO-ARQUITECTO
task_id: TASK-0317
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-08-06T17:10:00Z
implementation_commit: 3d64a7c7bd8e27d053c9b165cf44386221f91f9d
---

# HANDOFF TASK-0317 - remediation iteration 1

## Result

Commit `3d64a7c7bd8e27d053c9b165cf44386221f91f9d` applies the exact variant measured
by the independent checker. `PHONE_CANDIDATE_RE` is restored to its prior broad detector, and
only full matches of the existing finite `DATE_RE` grammar bypass the phone heuristic. The date
exemption is inside the phone block: email, IBAN/document, and configured domain-term checks remain
active. Arbitrary titles such as a clock prefix followed by a real phone number are detected again.

No test was weakened or changed. The generated 333-member timestamp family remains accepted and
all 11 PII-tail vectors remain rejected. `DATE_RE`, configuration, policies, validators, registry,
genesis, runtime behavior, and product routes are unchanged.

## Clean-clone evidence

The exact commit was checked in a detached clean clone at
`D:/Aegis_Scratch/multi_agent_project_protocol/task0317-remediation1-3d64a7c`.
The combined gate command exited 0 and the final `git status --short` was empty.

task_id: TASK-0317
status: in_review
executive_summary: Commit 3d64a7c anchors the timestamp exception in DATE_RE without weakening phone detection in free text. Codex is maker only and did not review or ratify the remediation.
artifacts:
  - path_or_commit: 3d64a7c7bd8e27d053c9b165cf44386221f91f9d
  - path_or_commit: scripts/memory/build_memory_db.py
  - path_or_commit: scripts/memory/test_memory_db.py
gates:
  - command: python scripts/memory/test_memory_db.py
    result: PASS (59 tests, clean clone)
  - command: python scripts/memory/build_memory_db.py --root . --rebuild
    result: PASS (4203 artifacts, 386 events, 15 tables)
  - command: python scripts/memory/check_memory_db_drift.py --fast
    result: PASS
  - command: python scripts/memory/check_memory_db_drift.py --full
    result: PASS
  - command: python scripts/scan_encoding.py --root .
    result: PASS
  - command: python scripts/scan_domain_neutrality.py --root .
    result: PASS
  - command: python scripts/validate_collaboration_state.py --root .
    result: PASS
  - command: git diff --check && git status --short
    result: PASS (empty status)
next_recommended: Arquitecto recomputes commit 3d64a7c and routes TASK-0317 to Analista for independent re-review before any closure.
risks: The pre-existing ID_RE phone bypass remains out of scope; no protocol boundary was changed.
