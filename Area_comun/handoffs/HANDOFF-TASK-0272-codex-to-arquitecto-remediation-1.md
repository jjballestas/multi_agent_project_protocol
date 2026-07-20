# HANDOFF TASK-0272 remediation iteration 1 - Codex to Arquitecto

The remediation implements the decided boundary in commit `2c3b17b`:

- exact `OUTCOME: confirmed|transient|definitive` token has first authority;
- non-zero process exit is transient before legacy free-text fallback;
- confirmation evidence accepts only commits authored by the invoked peer;
- rollback snapshots staged and unstaged binary diffs independently and restores the
  pre-exec index/worktree, including renames and pre-dirty tracked paths, while HEAD is stable;
- concurrent HEAD movement produces `ROLLBACK_DEFER` instead of overwriting the peer commit.

Permanent E2E coverage exercises a concurrent peer commit, echoed `NO-GO` prose under an
exact transient token, a confirmed delivery narrating a transient obstacle, exec-created
staged residue, and a pre-dirty tracked path overwritten/staged by the aborted exec.

The ratified TASK-0258 flip `review_approved -> done` was also applied through the runtime.

Gates (all exit 0):

- `python examples/mailbox_retry_cases/run_mailbox_retry_cases.py`
- `python scripts/test_anthropic_checker_harness.py`
- `python scripts/test_exec_lease_harness.py`
- `python scripts/scan_encoding.py --root .`
- `python scripts/scan_domain_neutrality.py --root .`
- `python scripts/validate_collaboration_state.py --root .`
- `python runtime/protocol_replay.py --check-drift`

Implementation commit: `2c3b17b`. Golden-memory commit: `ea2b41e`.

---
task_id: TASK-0272
status: in_review
executive_summary: Remediation iteration 1 makes exact outcome tokens authoritative, rejects peer commits as own evidence, restores pre-exec index/worktree state on transient aborts, and adds permanent adversarial regressions.
artifacts: scripts/harness/peer_mailbox_cron.ps1; scripts/harness/README.md; examples/mailbox_retry_cases/run_mailbox_retry_cases.py; commits 2c3b17b and ea2b41e
gates: retry E2E PASS; anthropic harness PASS; exec lease 9/9 PASS; encoding PASS; neutrality PASS; validator PASS; drift false
next_recommended: Analista re-judges all five original vectors from commit 2c3b17b; Arquitecto routes the verdict.
risks: If HEAD changes during an aborted exec, rollback is deliberately deferred and signaled to avoid overwriting the concurrent commit; manual coordination may still be required for any residue from that race.
