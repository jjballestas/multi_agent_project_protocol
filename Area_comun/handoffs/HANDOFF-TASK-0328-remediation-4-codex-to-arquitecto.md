# TASK-0328 remediation 5 - maker handoff

Author: Codex
Implementation commit: `df5de987`
Status requested: `in_review`
Reviewer requested: Analista

The retained filename is the already-governed TASK-0328 handoff route; this content supersedes its
remediation-4 delivery.

## Delivered property

Coordinate exemptions now consume only an integral protocol envelope. Exact task, decision,
specification, requirement, message, actor-artifact, operational identity, path-segment, and known
text-suffix grammar is removed. Every unexplained slug or segment is returned to the PII detector
without coordinate-dependent adjacency suppression. Date-shaped runs are no longer neutralized
inside unexplained payloads.

This closes the four classes refuted in the previous verdict: phones joined to an alphanumeric on
the left or right, grouped account identifiers joined on the left, and valid grouped account
identifiers containing an isolated 19xx/20xx eight-digit block. The same payload is detected bare,
under `file`, under `path`, and as an identity suffix.

## Powered measurement

The permanent population is derived from the production conditions rather than a payload tuple:

- ten characters accepted by `ACCOUNT_IDENTIFIER_SEPARATORS_RE`;
- all 23 block lengths between the production minimum and maximum for the reference identifier;
- both alphanumeric adjacency directions for phone candidates;
- left adjacency for grouped account candidates;
- eight-digit 19xx/20xx blocks found inside the valid identifier.

The result is 260 distinct payloads and 940 eligible coordinate renderings. The pre-task control
has 244 positives; the repaired engine has 940. Gains are 696 and losses are 0. All 85 path-valid
payloads are rejected directly by both `validate_metadata(file=...)` and
`require_safe_text(field='path')`.

## Permanent negative

`NEG-MEMORY-ACCOUNT-IDENTIFIER-PRESENTATION` declares 18 behavioral boundaries. Three independent
coordinate mutants lose detections: total coordinate blindness, restoration of the alphanumeric
adjacency skip, and restoration of date neutralization together with that skip. The repository
inventory remains complete at 70/70 contracts.

## Verification

Exact implementation commit `df5de987` passed in detached clean worktree
`D:/Aegis_Scratch/multi_agent_project_protocol/codex0328r5-df5de987-20260809` with empty status:

- `python scripts/memory/test_memory_db.py` - 72/72 tests;
- `python scripts/check_falsification_contracts.py --root .` - 70/70 contracts;
- `python scripts/validate_collaboration_state.py --root .`;
- `python scripts/scan_encoding.py --root .`;
- Python and PowerShell domain-neutrality scans;
- runtime drift false through sequence 8403;
- Python compile and `git diff --check`.

## Independent review focus

Recompute the 940-value powered population from the production predicates; verify zero losses
against the pre-task control; exercise the four formerly failing classes through the two production
call paths; and confirm each of the three coordinate mutants loses positives while clean governed
identities remain accepted.

Codex is the maker only and did not review or ratify this remediation.
