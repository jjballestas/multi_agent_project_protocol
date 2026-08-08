# HANDOFF TASK-0328 remediation 1

- Maker: Codex
- Implementation commit: `41a38082`
- Memory commit: `44f578c9`
- Requested checker: Analista
- Status requested: `in_review`

## Delivered behavior

The separator-aware account-identifier candidate is still broad, but detection
now validates bounded prefixes. A prefix is accepted only when its compact length
is 14-34, its checksum is valid, and its end is followed by an allowed separator
or the real end of the source string. The source character after a regex match is
also checked, so the 34-character ceiling cannot hide an unseparated continuation.

The original regression is closed:

    contains_pii("account: ES9121000418450200051332 from holder", []) -> True

The permanent mutant restores whole-match checksum validation. Isolated compact
and grouped forms remain true, while the embedded compact form becomes false.

## Bidirectional measurement

- Same governed HEAD metadata corpus: 22,342 eligible strings, old and new engines
  evaluated on the identical values; gained 0, lost 0.
- Permanent six-value boundary corpus: gained 2, lost 1.
- The sole loss is `ES9121000418450200051332A`: the former shape-only engine marked
  it, but its checksum is invalid. This rejection is deliberate and asserted.
- No valid positive detected by the former engine is lost in the boundary corpus.

## Verification

Exact commit `41a38082` was checked in detached clean clone
`D:/Aegis_Scratch/multi_agent_project_protocol/codex0328r1-41a38082`:

- `python scripts/memory/test_memory_db.py`: 72/72 passed.
- `python scripts/check_falsification_contracts.py --root .`: 67/67 declared.
- collaboration validator: exit 0.
- encoding scan: exit 0.
- domain-neutrality scan: exit 0.
- `git diff --check`: exit 0.
- clean-clone status before and after gates: empty.

Codex is the maker only. Independent review and ratification remain required.
