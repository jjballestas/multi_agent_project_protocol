# TASK-0328 remediation 3 - maker handoff

Author: Codex
Implementation commit: `9639535f`
Status requested: `in_review`
Reviewer requested: Analista

## Delivered property

Grouped candidates accept a checksum-valid prefix only when the cut reaches an admitted
separator or the real end. The next source character is preserved when the structural match
stops at its 34-character ceiling, so a longer continuation cannot masquerade as a terminated
identifier.

The unconditional contiguous branch remains monotonic for complete 14-34 character values. It
now measures the maximal surrounding alphanumeric run and rejects a silhouette inside a longer
run. Protocol identity tokens and governed paths are excluded only from account-identifier and
phone heuristics; email, declared domain terms, and the finite shape validators still apply.
Complete hexadecimal git object ids of 40 or 64 characters are recognized by property in the
`git_ref` ingestion path and no longer throw through an incidental PII heuristic.

## Bidirectional governed-corpus measurement

The production selector `iter_source_paths` and every `ALLOWLIST_KEYS` coordinate yielded 22,576
metadata strings on the delivery tree. Against the real pre-TASK-0328 engine at `f732292a`:

- New marks: 0.
- Lost marks: 0.
- Previous-engine marks: 0.
- Repaired-engine marks: 0.
- Governed `message_id`/`spec_id`/`task_id` values: 4,385; marked: 0.

The powered coverage population remains non-vacuous: 5,400 previous positives, 8,660 repaired
positives, 3,260 gains, and 0 losses.

## Permanent negative

`NEG-MEMORY-ACCOUNT-IDENTIFIER-PRESENTATION` now declares 13 behavioral boundaries. It retains
the single-cut, first-start-only, and checksum-contiguous production mutants. It also derives the
governed metadata corpus and real object ids from `git rev-list --all`:

- removing the prefix terminator creates new governed-corpus marks;
- every governed message/spec/task identity remains unmarked in production;
- the bounded contiguous branch rejects silhouettes inside real 40-character object ids;
- re-enabling the PII gate for complete object ids produces hard `git_ref` rejects.

## Verification

Live tree and detached clean clone
`D:/Aegis_Scratch/multi_agent_project_protocol/codex0328r3-9639535f-20260809` at exact commit
`9639535f` both exited 0 for:

- `python scripts/memory/test_memory_db.py` - 72/72 tests;
- `python scripts/check_falsification_contracts.py --root .` - 69/69 contracts;
- `python scripts/validate_collaboration_state.py --root .`;
- `python scripts/scan_encoding.py --root .`;
- Python and PowerShell neutrality scans and six parity tests;
- runtime drift, Python compile, and `git diff --check`.

The detached clone status was empty.

## Independent review focus

Reproduce the 22,576-string bidirectional measurement against `f732292a`, delete the terminator
guard and confirm new governed marks, derive every protocol identity rather than sampling one,
and test actual 40/64-character object ids through the `git_ref` decision. Confirm that the
previous 10,800-case coverage population still reports 5,400 / 8,660 / 3,260 / 0.

Codex is the maker only and did not review or ratify this remediation.
