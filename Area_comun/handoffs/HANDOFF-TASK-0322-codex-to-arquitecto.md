---
task_id: TASK-0322
from: Codex
to: Arquitecto
status: in_review
implementation_commit: dd3692f93d8c0d599a4d6001dc96841dd349f621
created_at: 2026-08-07T05:39:00Z
---

# HANDOFF TASK-0322 - bounded timestamp components

## Result

Commit `0eb060ee868bd10072ed5dd7061cae2f9d153ee3` narrows `DATE_RE` so
month is 01-12, day is 01-31, hour is 00-23, minute and second are 00-59,
and UTC offsets are 00:00-14:00. Both colon and compact time forms remain
supported, including 1-6 fractional digits on the colon form.

Commit `dd3692f93d8c0d599a4d6001dc96841dd349f621` adds the permanent
`NEG-MEMORY-DATE-RANGE-VALIDATION` source mutant. It restores the former broad
grammar and proves that all 14 declared out-of-range vectors become accepted.

This remediation changes declarations only. Production and test code remain untouched.

## Carrier family and metric qualification

The residual is a family, not one sampled string: 2 of the 33 language forms are
phone-candidate carriers. They are the colon-time forms with a 5- or 6-digit
fraction and a negative numeric offset. Colons break digit runs and `+` is outside
the phone heuristic character class, so only `SS.fffff[f]-HH` can accumulate the
required 9 consecutive digits. The deterministic sample that survived was
`9592-12-22T10:41:54.27956-07:53`.

The published 2.9 percent and 0.05 percent figures are relative only to the AC1
deterministic sampler. They are not language densities. Exact-language analysis by
the independent checker measured carrier density at 49.50 percent before and 49.44
percent after. The material change is absolute size: the accepted language shrinks
about 3,695 times and its carrier subset about 3,699 times, or 3.6 orders of magnitude.

The carrier family also becomes less controllable. Its leading pair is `SS`, now
bounded to 00-59, and its trailing pair is offset `HH`, now bounded to 00-14. In
the 5-digit-fraction subfamily, a Spanish mobile number beginning with 6 or 7 no
longer fits because the 9-digit run forces its first digit into `SS`. In the
6-digit-fraction subfamily, the run has 10 digits and a mobile number can still
fit shifted by one position.

## Acceptance evidence

- AC1: deterministic seed `20260805` generates 200,000 strings accepted by the
  old grammar. The phone-candidate carrier count is 5,789, or 2.9 percent within
  this sampler, not the density of the old language.
- AC2: boundary tests accept months 01/12, days 01/31, hours 00/23, minute and
  second 00/59, offsets through `+14:00` and `-14:00`, and reject every adjacent
  out-of-range component. Calendar validity beyond component ranges is intentionally
  unchanged: for example `2026-02-31` remains in grammar.
- AC3: the exact-commit clean clone indexed 4,254 real artifacts and 540 events.
  It produced zero warnings for `created_at`, `updated_at`, or `closed_at`.
- AC4: all 11 suffix vectors remain rejected. The existing
  `NEG-MEMORY-DATE-EXEMPTION-PHONE-ONLY` contract still proves that DATE_RE only
  exempts the phone heuristic and cannot bypass later configured PII checks.
- AC5: after range narrowing, 2,006 generated strings remain in the accepted
  sampler population and exactly 1 is a phone-candidate carrier: 0.05 percent
  within that sampler. The language-level result is the approximately 3.7e3-fold
  absolute reduction and the 2-of-33 residual family declared above.
- AC6: every gate below passed by exit code in a detached clean clone of the exact
  implementation head.

## Exact-commit gates

Detached clone of `dd3692f93d8c0d599a4d6001dc96841dd349f621` under the designated
`D:/Aegis_Scratch/multi_agent_project_protocol/` root:

- `python scripts/memory/test_memory_db.py` -> exit 0, 62/62 tests.
- `python scripts/memory/build_memory_db.py --root .` -> exit 0, 4,254 artifacts,
  540 events, 15 tables, foreign keys enabled.
- memory drift `--fast` and `--full` -> exit 0; full round trip and bidirectional
  comparison pass.
- falsification inventory -> exit 0, 34 permanent negatives / 34 declared / 0 missing.
- collaboration, encoding, domain-neutrality, and diff gates -> exit 0.
- final `git status --short` -> empty.

## Independent-review focus

1. Remove the bounded grammar through the declared mutant and confirm all 14 invalid
   component vectors become accepted.
2. Recompute the seeded population and confirm 5,789/200,000 before and 1/2,006 after,
   treating both ratios only as sampler-relative measurements.
3. Confirm the corpus build adds no date-key warnings and the 11 suffix vectors remain
   rejected.
4. Confirm the date exemption remains inside the phone heuristic only.
5. Confirm the residual family is exactly the two colon-time forms with 5- or
   6-digit fractions and negative numeric offsets.

Codex is the maker only and did not review or ratify this work.
