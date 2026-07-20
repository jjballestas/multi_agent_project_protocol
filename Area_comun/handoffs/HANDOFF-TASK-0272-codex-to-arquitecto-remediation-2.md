# HANDOFF TASK-0272 - remediation iteration 2

TASK-0273 was first moved from `review_approved` to `done` through the authoritative
runtime and committed as `455313d`.

TASK-0272 remediation is implemented in `02cee08`:

- `Get-OwnEvidence` no longer reads git authors. It accepts only an event newer than the
  pre-exec ledger sequence, with exact `actor == PeerId` and a non-empty ed25519
  `actor_auth`. If no own signed event exists in the window, evidence does not confirm.
- Only the last non-empty transcript line may carry the exact `OUTCOME:` token.
- Both binary diff snapshots must succeed before the agent starts.
- Rollback rechecks HEAD immediately before and after `reset --hard`; movement or reset
  failure defers restoration.
- The permanent E2E uses a uniform git author, proves that a concurrent commit without a
  signed own event remains unconfirmed, then proves confirmation through a signed own
  ledger event.

The requested exclusions remain untouched: untracked quarantine is TASK-0275 and the
real drift CLI gate is TASK-0274.

Gates, all exit 0:

- `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py`
- `python scripts/test_anthropic_checker_harness.py`
- `python scripts/test_exec_lease_harness.py`
- `python scripts/validate_collaboration_state.py --root .`
- `python scripts/scan_encoding.py --root .`
- `python scripts/scan_domain_neutrality.py --root .`
- `protocol_state_drift(Path('.'))`: `has_drift=false`, `up_to_seq=5331` before delivery.
- `protocol.config.json` SHA256: `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354`.

task_id: TASK-0272
status: in_review
executive_summary: Iteration 2 removes uniform-author false confirmation by using signed ledger-window evidence, terminal-only OUTCOME tokens, snapshot fail-closed behavior, and rollback HEAD rechecks. TASK-0273 is done.
artifacts: commit 02cee08; commit 455313d; scripts/harness/peer_mailbox_cron.ps1; examples/mailbox_retry_cases/run_mailbox_retry_cases.py; scripts/harness/README.md
gates: retry E2E PASS; Anthropic harness PASS; exec-lease suite PASS; validate PASS; encoding PASS; neutrality PASS; drift false at seq 5331; config SHA256 2E35F26E...354
next_recommended: Arquitecto should route independent iteration-2 re-judgment to Analista, including uniform-author negative, terminal-token attacks, and snapshot/rollback fault paths.
risks: This is iteration 2 of 2. A new checker failure must be escalated to the operator. TASK-0274 and TASK-0275 remain separate ready work.
