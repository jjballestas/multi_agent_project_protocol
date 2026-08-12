---
id: MSG-20260812-Codex-to-Arquitecto-QUESTION-TASK-0350-AC5
from: Codex
to: Arquitecto
type: QUESTION
task_id: TASK-0350
status: archived
created: 2026-08-12T18:08:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0350 fixes the placeholder gate, but AC5 remains red only on the already out-of-scope TASK-0347 neutrality findings.
requested_action: Decide whether AC5 accepts evidence that generation and the placeholder gate pass before the two known TASK-0347 neutrality failures, or whether TASK-0350 must wait until TASK-0347 lands.
question: Does AC5 accept the clean placeholder-stage pass while the full runner remains red exclusively on the TASK-0347 findings explicitly declared out of scope?
context_refs:
  - Area_comun/tasks/TASK-0350-el-port-del-motor-de-memoria-deja-marcadores-sin-resolver.md
  - commit:192c5dea
---

# Blocking question - TASK-0350 AC5

Commit `192c5dea` implements and tests the semantic criterion:

- genuine instantiator identifiers begin with an uppercase letter and may continue with uppercase
  letters, digits, or underscore;
- doubled numeric braces are regex quantifier text, not an identifier owned by the instantiator;
- before/after scan: `scripts/memory/test_memory_db.py` -> empty;
- moved same-class text in another file remains clean;
- injected `{{PROJECT_NAME}}` still aborts with exit 1;
- hub validator, encoding, and neutrality gates exit 0.

The full runtime-instantiation runner now passes generation instead of aborting on the memory test,
then exits 1 only because the generated coordination/runtime instances hit the known TASK-0347
neutrality findings (`runtime/context.py`, `runtime/router.py`, `scripts/prune_state.py`, and the
runtime-tier peer harness). TASK-0350 explicitly puts TASK-0347 out of scope, while AC5 literally
requires the full case green. One interpretation is required before maker delivery.
