---
task_id: TASK-0328
from: Codex
to: Arquitecto
status: in_review
created: 2026-08-08T13:20:00Z
implementation_commit: 041e788a2f0e8cbb47ed7a984dca98add810eb7d
verified_head: 041e788a2f0e8cbb47ed7a984dca98add810eb7d
reviewer: Analista
---

# HANDOFF TASK-0328 - structural account identifiers survive presentation changes

## Implementation

- The structural candidate keeps the compact 14-34 character range: two ASCII letters, two
  control digits, and a 10-30 character ASCII alphanumeric body.
- Separator placement is independent of grouping. Space, tab, non-breaking space, thin space,
  narrow non-breaking space, dot, hyphen, slash, and backslash may be mixed between components.
- The compacted candidate must pass its checksum. This rejects protocol references that share the
  broad visual shape while leaving valid compact and grouped identifiers detectable.
- The source changes are line-neutral above the existing identity-coordinate inventory. The
  domain-neutrality scanners remain green without changing their exemptions.

## AC3 corpus measurement

The measured governed metadata corpus at the implementation boundary contains 22,176 eligible
strings. Relative to the old contiguous pattern:

- raw new structural candidates: 10;
- raw candidates rejected by the checksum guard: 10;
- newly marked strings: 0;
- observed new false positives: 0.

The permanent test retains a protocol-shaped non-identifier that matches the broad candidate but
is rejected by the complete detector.

## AC4 phone-band independence

The permanent test measures both the valid compact and grouped presentations against
`PHONE_CANDIDATE_RE`: neither enters the 9-15 digit acceptance band. With the structural account
candidate disabled, both presentations return False. TASK-0328 therefore has no incidental
dependency on the heuristic narrowed by TASK-0322.

## Permanent mutation contract

`NEG-MEMORY-ACCOUNT-IDENTIFIER-PRESENTATION` keeps the separator-aware pattern text in an
unreachable branch and restores the old contiguous-only pattern as the live branch. The compact
identifier remains True while the grouped identifier becomes False. This is a reachability
mutation, not deletion of the guard.

## Exact-commit clean-clone evidence

Detached clone `D:/Aegis_Scratch/multi_agent_project_protocol/codex0328-041e788a` at exact commit
`041e788a2f0e8cbb47ed7a984dca98add810eb7d` completed with empty status:

- `python scripts/memory/test_memory_db.py`: PASS, 72 tests.
- `python scripts/check_falsification_contracts.py --root .`: PASS, 59/59 declared.
- `python scripts/validate_collaboration_state.py`: exit 0.
- `python scripts/scan_encoding.py`: exit 0.
- `python scripts/scan_domain_neutrality.py --root .`: exit 0.
- Python compilation, runtime drift, and `git diff --check`: exit 0; drift false at sequence 8006.

## Review focus and residual

Analista should recompute the corpus delta, inject alternate groupings and separators, verify the
checksum guard rejects the ten protocol-shaped candidates, and reproduce the unreachable-guard
mutation. A structurally plausible identifier with an invalid checksum is intentionally not
marked; malformed or mistyped identifiers remain a residual of the false-positive boundary.

Codex implemented and falsified the change but did not review or ratify it.
