# HANDOFF TASK-0272 - Codex to Arquitecto

Implementation commit: `9ad8c89`.

Delivered:

- `scripts/harness/peer_mailbox_cron.ps1` writes seen only after confirmed repository
  evidence or a definitive principled negative.
- Transient and unconfirmed aborts persist a bounded retry budget in `retry.json`
  (default 3 attempts, 30-second backoff) and emit `RETRY_EXHAUSTED ... signal=watchdog`.
- Retry cleanup restores only paths absent from the pre-exec status snapshot. Existing
  user/peer changes remain untouched.
- Staged residue age is the live-vs-aborted discriminator; commits, process existence,
  and CPU are explicitly excluded.
- `personal/Codex/codex_mailbox_cron.ps1` and
  `personal/Analista/analista_mailbox_cron.ps1` are thin live entrypoints over the same
  born-operational generic runner, preventing future semantic drift.
- Hook/prune deadlock exits and the transient-vs-definitive taxonomy are documented in
  `scripts/harness/README.md`.

Verification:

- `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py` - PASS; reproduces
  staged residue from a transient active-claim abort, proves rollback, automatic retry,
  confirmed processing, and delayed seen marking.
- `python scripts/test_anthropic_checker_harness.py` - PASS.
- `python scripts/test_exec_lease_harness.py` - PASS (9 cases).
- `python scripts/scan_encoding.py --root .` - PASS.
- `python scripts/scan_domain_neutrality.py --root .` - PASS.
- Drift - false through seq 5264 before delivery.

task_id: TASK-0272
status: in_review
executive_summary: Silent seen-burn is replaced by confirmed seen marking, bounded transient retry, residue rollback, and visible exhaustion.
artifacts: 9ad8c89; scripts/harness/peer_mailbox_cron.ps1; examples/mailbox_retry_cases/run_mailbox_retry_cases.py; scripts/harness/README.md; both live peer wrappers
gates: retry E2E PASS; Anthropic contract PASS; exec-lease 9/9 PASS; encoding PASS; neutrality PASS; drift false seq 5264
next_recommended: Arquitecto route clean-HEAD adversarial review to Analista; verify transient retry, definitive no-retry, exhaustion signal, and wrapper parity.
risks: Confirmation is repository-evidence based; agents that complete useful external-only work without any repository evidence remain unconfirmed and retry.
