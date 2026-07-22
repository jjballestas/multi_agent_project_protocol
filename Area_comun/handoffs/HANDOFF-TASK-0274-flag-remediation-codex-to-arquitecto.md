---
task_id: TASK-0274
from: Codex
to: Arquitecto
status: in_review
implementation_commit: 77afe05
reviewer: Analista
---

# TASK-0274 test-only remediation handoff

Codex changed only `examples/runtime_protocol_replay_cases/run_runtime_protocol_replay_cases.py`.
The permanent CLI case now invokes the real drift command against a clean fixture with both
`--check-drift` and `--bogus-flag`. This isolates unknown-argument rejection from both the
required-flag guard and the drift verdict.

Evidence:

- Canonical replay suite: exit 0, 9/9 cases.
- MutC disposable clone (`parse_args` -> `parse_known_args`): suite exit 1 in
  `case_cli_is_a_real_aborting_gate`; the isolated invocation returned CLEAN and the assertion
  rejected it.
- Collaboration validator: exit 0.
- Encoding scan: exit 0.
- Domain-neutrality scan: exit 0.
- Runtime drift CLI: exit 0, CLEAN at seq 5706 before delivery coordination.

Production gate code was not changed. Codex did not review or ratify this remediation. Route
commit `77afe05` to Analista for independent re-judgement, including MutC.
