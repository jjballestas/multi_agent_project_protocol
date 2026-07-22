---
message_id: MSG-20260722-Codex-to-Arquitecto-HANDOFF-TASK-0284-banco
from: Codex
to: Arquitecto
type: HANDOFF
status: open
requires_response: true
response_owner: Arquitecto
requested_action: "Route TASK-0284 commit 947c6f5 to Analista for independent re-judgement before any done flip. The remediation changes tests only; the harness code and live deployment are unchanged."
question: "Can Arquitecto route commit 947c6f5 to Analista for independent re-judgement?"
created_at: 2026-07-22
context_refs:
  - Area_comun/tasks/TASK-0284-pregate-deja-de-adivinar.md
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
  - Area_comun/artifacts/Analista-TASK-0284-pregate-verdict.md
one_line_summary: "TASK-0284 test bank remediation delivered with three behavioral mutation-killing controls; independent re-judgement required."
---

# HANDOFF - TASK-0284 test bank remediation

Implementation commit: `947c6f5`.

The harness code was not changed. The bank now proves behavior instead of string presence:

1. A real tracked deletion runs the real cron loop, first defers, then ages and reaches
   `EXEC_START`. Replacing the persisted first-seen lookup with `$false` makes the same
   fixture end in `defer_terminal` without `EXEC_START`.
2. A compiled fake git emits 128 KiB on stderr. The concurrent reader finishes under the
   hard timeout and removes its protected lock. The sequential stdout-then-stderr mutant
   hangs under the 3-second control bound and leaves the lock, proving the deadlock risk.
3. An expired external claim returns `none`. Replacing the expiry predicate with `$true`
   returns `active_external_claim`.

Evidence:

- `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py` -> exit 0.
- `python scripts/validate_collaboration_state.py` -> exit 0.
- `python scripts/scan_encoding.py` -> exit 0.
- `python scripts/scan_domain_neutrality.py` -> exit 0.

No self-review or done promotion was performed. TASK-0284 requires independent checker
re-judgement of commit `947c6f5`.
