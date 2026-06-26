---
skill_id: migration-verification
title: Migration verification
profile: financiero_presupuesto
version: 0.1.0
neutral_core: false
---

# Procedure

Use this checklist to verify a migration or bulk transformation:

1. Capture pre-checks before writing: source counts, target counts, null/duplicate checks, referential checks, and
   any invariants that must survive the move.
2. Define idempotency expectations. A repeated run must either perform no additional mutation or fail with a clear
   already-applied signal.
3. Run the smallest representative dry path first when the tooling supports it, then record the exact command or
   script version used for the real run.
4. Compare post-checks to the pre-checks. Reconcile count changes, rejected rows, defaulted values, and transformed
   fields with explicit reasons.
5. Verify downstream readability through the normal application or reporting path, not only through direct storage
   inspection.
6. Keep rollback practical. Record the restore point, reverse command, or compensating migration, and state when
   rollback is no longer safe.
7. Handoff with evidence: pre/post numbers, reconciliation notes, idempotency result, and any residual follow-up.
