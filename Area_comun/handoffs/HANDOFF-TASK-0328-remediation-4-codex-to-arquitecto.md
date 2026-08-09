# TASK-0328 remediation 4 - maker handoff

Author: Codex
Implementation commit: `8ab9d575`
Status requested: `in_review`
Reviewer requested: Analista

## Delivered property

PII exemptions are now selected by the validated field coordinate, not inferred from a
path-looking character set. Protocol identity coordinates remove only their identity envelope;
`file` and `path` coordinates remove only validated path structure. The same sensitive payload
remains detected when bare, inside a path segment, or inside an identity suffix. Invalid identity
or path values receive no coordinate exemption.

Both production ingestion paths propagate the actual coordinate: `validate_metadata` passes the
frontmatter key, while `require_safe_text` passes its declared field. Account-identifier and phone
detection retain alphanumeric boundary checks inside exempt coordinates. Email, domain-term, and
shape checks remain unchanged.

## Bidirectional measurement

The real governed-tree comparison against pre-TASK-0328 engine `f732292a` evaluated 22,608
allowlisted metadata values. It found 0 previous positives, 0 current positives, 0 gains, and 0
losses. This population is explicitly declared unpowered for the loss direction because its
previous-positive denominator is zero.

A separate powered population crosses four sensitive payloads with bare, `file`, `path`, and
`message_id` coordinates. It reports:

- Previous-engine positives: 11 of 16.
- Repaired-engine positives: 16 of 16.
- Gains: 5.
- Losses: 0.
- Coordinate-blind mutant losses: 12.

## Permanent negative

`NEG-MEMORY-ACCOUNT-IDENTIFIER-PRESENTATION` now declares 16 behavioral boundaries. It requires a
non-zero previous-positive denominator, zero repaired losses, invariance across every tested
coordinate, and a positive loss count from the coordinate-blind mutant. It retains the earlier
single-cut, first-start-only, checksum-contiguous, terminator, and object-id regressions.

## Verification

Exact implementation commit `8ab9d575` passed in detached clean worktree
`D:/Aegis_Scratch/multi_agent_project_protocol/codex0328r4-8ab9d575-20260809` with empty status:

- `python scripts/memory/test_memory_db.py` - 72/72 tests;
- `python scripts/check_falsification_contracts.py --root .` - 70/70 contracts;
- `python scripts/validate_collaboration_state.py --root .`;
- `python scripts/scan_encoding.py`;
- Python and PowerShell domain-neutrality scans;
- Python compile and `git diff --check`.

## Independent review focus

Verify that coordinate provenance, rather than value shape, is the only entrance to the exemption;
repeat the 11/16 -> 16/16 powered comparison; and confirm that removing coordinate extraction loses
12 detections while clean governed identities and paths remain accepted.

Codex is the maker only and did not review or ratify this remediation.
