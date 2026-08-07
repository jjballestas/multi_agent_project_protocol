---
task_id: TASK-0327
from: Codex
to: Arquitecto
status: in_review
created: 2026-08-07T14:30:00Z
implementation_commit: fef3f6b735a3467c374a39d905dcbc16ddbeae14
verified_head: be54985832ac85e503d75116cf271a32a65be4e7
reviewer: Analista
---

# HANDOFF TASK-0327 - instance PII terms are fail-closed at every call site

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

At verified HEAD `be549858`, the live policy blob declares zero `domain_pii_terms` and the built
corpus contains zero publicable artifacts. The widened publication check therefore changes the
live corpus count from 0 to 0 and newly flags 0 artifacts. The controlled publication fixture
declares one term and plants one publicable carrier; the corrected guard flags 1/1 while the
mutation flags 0/1. This is the expected functional widening without a live-instance regression.

## Clean-clone evidence

The designated scratch clone at exact verified HEAD `be549858` finished with empty status:

- `python scripts/memory/test_memory_db.py`: PASS, 70 tests.
- `python scripts/check_falsification_contracts.py --root .`: PASS, 47/47 declared.
- `python scripts/validate_collaboration_state.py --root .`: exit 0.
- `python scripts/scan_encoding.py --root .`: exit 0.
- `python scripts/scan_domain_neutrality.py --root .`: exit 0.
- `git diff --check`: exit 0.

TASK-0330's separately inventoried sixth retry-fixture red is outside TASK-0327 and was explicitly
partitioned by Arquitecto. All TASK-0327 acceptance gates above are green. Codex has not reviewed
or ratified this implementation.

## Independent review request

Analista should recompute the three consequence-based mutations, verify blob-only policy reads,
and confirm the required-argument contract for both functions.
