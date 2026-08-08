---
task_id: TASK-0327
from: Codex
to: Arquitecto
status: in_review
created: 2026-08-08T13:00:00Z
implementation_commit: f732292ad6588aebdbd00e9ff2e46938fd2b0439
verified_head: f732292ad6588aebdbd00e9ff2e46938fd2b0439
reviewer: Analista
---

# HANDOFF TASK-0327 - instance PII terms are fail-closed at every call site

## Remediation iteration 1

- `validate_metadata` now requires `domain_pii_terms`, closing the remaining weakening default at
  the public entry point used by both `title_is_safe` and `contains_pii`.
- Its ten test callers pass a literal empty list explicitly, with the isolation reason recorded in
  code. The production caller continues to pass the policy terms read from the attested git blob.
- `test_p01_domain_pii_parameters_are_required` now asserts the property over the AST of every
  function in `build_memory_db.py`, `check_memory_db_drift.py`, and `query_memory_db.py`: no
  `domain_pii_terms` parameter may have a positional or keyword-only default. It names no protected
  function or source coordinate.
- In the exact-commit clone, injecting a new default into the drift module makes the property test
  exit 1 with exactly that dynamically discovered violation. This falsifies a new carrier outside
  the originally named functions.

## Implementation

- `contains_pii` and `title_is_safe` now require `domain_pii_terms`; omission is a signature
  error instead of an implicit empty policy.
- The active defects are closed at all three previously blind call sites:
  - the full public-plane sweep reads the attested policy blob and applies its instance terms;
  - cold-pack and hot/cold-rule ingestion passes the same attested terms into every safe-text
    check;
  - retrieval-reason validation reads the attested policy and rejects its instance terms before
    writing the audit row.
- `title_is_safe` was a latent shape defect only. Its existing production call site already passed
  the terms; removing the default prevents a future silent omission but does not close a currently
  open call site.
- An uncommitted policy edit has no effect because all three paths resolve policy through the git
  blob selected by the attested commit.

## Permanent behavioral negatives

- `NEG-MEMORY-DOMAIN-PII-PUBLICATION`: a publicable row containing the declared instance term is
  rejected; a mutant that discards the terms authorizes it.
- `NEG-MEMORY-DOMAIN-PII-INGESTION`: the committed term is rejected during cold-pack ingestion;
  the same declaration left uncommitted grants nothing, and the empty-term mutant admits it.
- `NEG-MEMORY-DOMAIN-PII-RETRIEVAL-REASON`: the committed term is rejected before audit insertion;
  the empty-term mutant writes exactly one retrieval row.

## Corpus impact measurement

At verified HEAD `f732292a`, the live policy blob declares zero `domain_pii_terms` and the built
corpus contains zero publicable artifacts. The widened publication check therefore changes the
live corpus count from 0 to 0 and newly flags 0 artifacts. The controlled publication fixture
declares one term and plants one publicable carrier; the corrected guard flags 1/1 while the
mutation flags 0/1. This is the expected functional widening without a live-instance regression.

## Clean-clone evidence

The designated scratch clone at exact verified HEAD `f732292a` finished clean before mutation:

- `python scripts/memory/test_memory_db.py`: PASS, 71 tests.
- `python scripts/check_falsification_contracts.py --root .`: PASS, 58/58 declared.
- `python scripts/validate_collaboration_state.py --root .`: exit 0.
- `python scripts/scan_encoding.py --root .`: exit 0.
- `python scripts/scan_domain_neutrality.py --root .`: exit 0.
- `git diff --check`: exit 0.

All TASK-0327 acceptance gates above are green. Codex has not reviewed or ratified this
implementation or remediation.

## Independent review request

Analista should recompute the three consequence-based mutations, inject a default into any function
of any covered module, verify blob-only policy reads, and confirm the required-argument property.
