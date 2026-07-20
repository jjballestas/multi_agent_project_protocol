---
handoff_id: HANDOFF-TASK-0278-codex-to-arquitecto-1
task_id: TASK-0278
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-07-20
implementation_commit: ef0b645
---

# TASK-0278 delivery

## Result

The generic peer harness now classifies outcomes from the agent response stream only.
Invoker diagnostics, CLI epilogues, and echoed prompt text remain available in their log
but cannot affect consumption. Exact terminal `OUTCOME:` remains authoritative. Nonzero
exit remains transient, signed own evidence remains confirmed, and free text can request
a transient retry but can never produce definitive consumption.

Both live peer entrypoints already delegate to the generic harness, so the fix applies to
Codex and Analista without duplicated parser code. The generic harness remains the source
shipped by the born-operational export path.

## Field regression

The permanent retry suite contains reduced fixtures from the real 2026-07-20 Codex runs:

- done-flip 0272: response ended in `OUTCOME: transient`; diagnostic ended in `tokens used / 34.968`.
- TASK-0277: response ended in `OUTCOME: transient`; diagnostic ended in `tokens used / 42.041`.
- checker diagnostic epilogue and a conflicting diagnostic token cannot override response stdout.
- prompt and response lexical matches (`NO-GO`, `out_of_scope`, `fuera de alcance`) cannot create definitive.

## Evidence

- `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py`: PASS.
- `python scripts/test_anthropic_checker_harness.py`: PASS.
- `python scripts/test_exec_lease_harness.py`: PASS (9 cases).
- `python scripts/validate_collaboration_state.py --root .`: EXIT 0.
- `python scripts/scan_encoding.py --root .`: EXIT 0.
- `python scripts/scan_domain_neutrality.py --root .`: EXIT 0.
- Runtime drift: false at implementation time.

## Precondition repair

Before TASK-0278, the validator had exactly one error: the active orphan claim
`CLAIM-20260720-Codex-TASK-0272-done-response-memory` on done TASK-0272. Codex released it
through signed runtime event seq 5369. The validator then returned EXIT 0 before TASK-0278
was claimed or started.

## Review boundary

Codex is maker only. Arquitecto should route the committed implementation to Analista for
independent review. No protocol boundary or pinned configuration changed.
