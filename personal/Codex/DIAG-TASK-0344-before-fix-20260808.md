# TASK-0344 pre-fix diagnosis

Recorded before changing either `scripts/prune_state.py` or the mailbox-status runner.

Measured result:

- `MSG-001-old.md`: `requires_response: false`, `status: answered`; therefore
  `requires_unresolved_response()` is false and the message would enter `eligible` if pruning ran.
- `MSG-002-new.md`: identical fields and branch result; it also would enter `eligible`.
- `assess()` returns `due=False`, with no reasons and 36 estimated cold-start tokens.
- Consequently `apply_prune()` returns `mode=noop`, archives zero messages, and never calls
  `prune_mailbox()`.

Conclusion: production is correct and the fixture is stale. The failure is unrelated to the
unresolved-response branch proposed in the task hypothesis. TASK-0273, commit `3062214d`, changed
`apply_prune()` so that a non-due maintenance assessment is an intentional no-op. The mailbox
fixture predates that change and retained thresholds of 99 percent with empty task and claim
ledgers, so it no longer reaches the behavior it claims to test. The correct repair is to make the
fixture explicitly due while preserving its two resolved FYI messages and `mailbox_keep_recent: 1`;
`scripts/prune_state.py` must not change.
