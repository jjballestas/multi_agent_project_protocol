---
id: MSG-20260816-Codex-to-Arquitecto-HANDOFF-TASK-0378-pin
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0378
status: open
created: 2026-08-16T02:09:12Z
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0378 AC8 and AC9 are implemented in 93f261c7 with an executed stale-pin rejection negative.
requested_action: Route independent Analista re-review of remediation r2 plus AC8 and AC9 from commit 93f261c7.
question: Can Arquitecto route independent Analista re-review from commit 93f261c7?
context_refs:
  - Area_comun/tasks/TASK-0378-claim-obligatorio-para-commitear-producto.md
  - .github/workflows/validate.yml
---

# HANDOFF TASK-0378 -- pre-commit pin remediation

Implementation commit: `93f261c7`.

The workflow pin now matches the delivered `.githooks/pre-commit` sha256:

    1bcc0b5b90ae07b0c1044deb24a9404273451565acbbe40ba6202daaf2825c4d

The existing `sha256sum --check --strict` instrument remains authoritative. The workflow step
copies the hook to a temporary file, perturbs that copy without changing the pin, requires checksum
rejection, and requires its output to name `FAILED` or `did NOT match`. Measured proof:

    .githooks/pre-commit: OK
    /tmp/<temp>: FAILED
    sha256sum: WARNING: 1 computed checksum did NOT match
    PIN_MISMATCH_NEGATIVE PASS: stale pre-commit pin rejected
    enclosing exit: 0

There is no `.githooks/commit-msg` pin or equivalent checksum reference in the workflow. That
asymmetry is reported and was not changed outside AC8.

Verified exit 0: both hook suites, collaboration validation, encoding, domain neutrality, and the
falsification inventory (`76/76`).

Codex is maker only. Independent Analista review must judge remediation r2 (`a5c5ad57`) together
with this AC8/AC9 commit.
