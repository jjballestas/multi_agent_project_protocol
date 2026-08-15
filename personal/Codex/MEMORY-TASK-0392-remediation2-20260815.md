# TASK-0392 remediation 2

- Implementation commit: `2d6ad843`.
- Matching mailbox filenames that fail the documented parser now emit one raw-name diagnostic alert instead of disappearing silently.
- The exported filename contract is aligned on `MSG-<date>-<sender>-to-<recipient>-*.md`, with hyphens forbidden inside parsed components.
- The commit filter now recognizes only an exact trailer line in the commit body; subject, author, and prose mentions remain visible.
- The proof rejects the obsolete `<SELF_COMMIT_FILTER>` prescription, checks malformed-name noise and parsed-name non-duplication, and exercises exact-trailer false positives.
- The guide requires one mailbox message per delivery and explicitly states that commit-only delivery may be invisible.
- Gates before commit: watchdog proof, collaboration validator, encoding, neutrality, and drift all exit 0; drift clean at seq 9378.
- Coordination commit: `5561d2ec`; TASK-0392 is `in_review`, all Codex remediation claims are released, and the review request is open for Arquitecto to route to Analista.
