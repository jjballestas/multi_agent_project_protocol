# TASK-0328 remediation 2 - maker handoff

Author: Codex
Implementation commit: `f5581ca7`
Status requested: `in_review`
Reviewer requested: Analista

## Delivered property

The account-identifier PII guard is now monotonic over the old contiguous silhouette:
checksum validation can broaden detection to separated presentations, but cannot remove a
contiguous detection. The contiguous silhouette is therefore marked even with an invalid
checksum, which preserves fail-closed treatment of mistyped, truncated, or partly masked PII.

Separated presentations are context invariant over the admitted structure. The engine enumerates
every position satisfying the structural start and evaluates every admissible prefix from each
position. A greedy match opened by prose on the left no longer hides a later identifier, and prose
on the right no longer invalidates an otherwise valid prefix.

## Powered bidirectional measurement

The deterministic population contains 10,800 strings: 300 valid-checksum identifiers and 300
invalid-checksum silhouettes, each in compact and grouped form, crossed with nine contexts. Six
contexts are generated from the pattern's own `[A-Z]{2}[sep]*\d{2}` start condition.

- Previous-engine positives: 5,400.
- Repaired-engine positives: 8,660.
- Gained: 3,260.
- Lost: 0.

The loss result is not vacuous. The denominator contains 5,400 previous positives. Removing the
unconditional contiguous branch loses 2,140 of those positives in the same population.

## Permanent negative

`NEG-MEMORY-ACCOUNT-IDENTIFIER-PRESENTATION` kills three independent source mutants:

1. Single candidate cut: grouped detection changes under right-side prose.
2. First structural start only: grouped detection changes when the identifier moves after a
   competing left-side start.
3. Checksum-gated contiguous silhouette: prior-engine positives are lost.

The source behavior passes every tested left/right placement for both compact and grouped forms.

## AC4 correction and declared tradeoff

The earlier claim that neither form entered the phone heuristic was false as a general statement.
In the ten-country sample, GB33, NL91, BE68, and NO93 are inside the 9-15 digit band in both forms:
4/10. Structural coverage is evaluated independently and does not rely on this incidental path.

Prefix validation remains deliberately fail-closed. The checker measured false-positive rates of
1.050 percent for an isolated compact form, 3.140 percent for an isolated grouped form, and 4.990
percent for a grouped form in prose. The checker also measured +3.9 percent on the governed corpus
and 14.3 ms for its worst 20 kB load; no performance change was requested in this iteration.

## Verification

Live tree and detached clean clone of exact implementation commit `f5581ca7` both exited 0 for:

- `python scripts/memory/test_memory_db.py` - 72/72 tests;
- `python scripts/check_falsification_contracts.py --root .` - 68/68 contracts;
- `python scripts/validate_collaboration_state.py --root .`;
- `python scripts/scan_encoding.py --root .`;
- Python and PowerShell domain-neutrality scans plus six parity tests;
- Python compile and `git diff --check`.

The detached clone status was empty.

## Independent review focus

Recompute the powered population and all three mutants. Test left and right contamination with
both separated and adjacent prose. Confirm that an invalid-checksum contiguous silhouette remains
marked, that grouped invalid silhouettes still require checksum, and that the 4/10 phone-band
statement reproduces.

Codex is the maker only and did not review or ratify this remediation.
