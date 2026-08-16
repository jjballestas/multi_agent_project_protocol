# TASK-0378 remediation 3 memory

- Implementation commit: `07642021` (`fix(TASK-0378): fail closed without commit actor`).
- `commit_actor()` now returns `None` when no Git work tree or configured actor is available.
- Claim enforcement treats that value as `unavailable` and fails closed because ownership cannot be verified.
- `scripts/test_commit_msg_hook.py` copies the gate into a non-repository temporary directory and verifies the declared sentinel and fail-closed state; removing the protection makes the case raise/fail.
- The full-mode inventory fixture now provides an explicit product claim for its synthetic `protocol.config.json` mutation.
- Verified green: commit-msg regression suite, encoding scan, domain-neutrality scan, and collaboration-state validator.
- The full-mode inventory runner did not complete inside a 10-minute local timeout; the original no-repository traceback is removed, but the whole runner still requires independent/CI confirmation.
- TASK-0378 remains `in_progress` until the delivery transaction moves it to `in_review` and releases all Codex claims.
- Delivery commit: `49298356`; TASK-0378 is now `in_review`, all remediation claims are released, and the self-contained handoff is open for Arquitecto.
