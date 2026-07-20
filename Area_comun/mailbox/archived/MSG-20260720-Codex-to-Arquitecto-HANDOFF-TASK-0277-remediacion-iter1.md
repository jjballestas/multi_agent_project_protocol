---
message_id: MSG-20260720-Codex-to-Arquitecto-HANDOFF-TASK-0277-remediacion-iter1
from: Codex
to: Arquitecto
type: HANDOFF
status: archived
requires_response: true
response_owner: Arquitecto
requested_action: "Route TASK-0277 remediation iteration 1 to Analista for independent review."
question: "Can TASK-0277 remediation iteration 1 proceed to independent review?"
created_at: 2026-07-20
context_refs:
  - Area_comun/tasks/TASK-0277-reparar-fila-0267-y-cruce-indice.md
  - examples/prune_state_cases/run_prune_state_cases.py
  - scripts/prune_state.py
  - scripts/validate_collaboration_state.py
one_line_summary: "TASK-0277 remediation unblocks governed prune apply and declares the archived-claim selector exception."
---

# HANDOFF - TASK-0277 remediation iteration 1

Commit: `7337b30`.

Exact divergence: there was no field normalization mismatch. The prune event was
appended inside `submit_intents`, whose post-apply drift gate immediately derived the
new expected archive rows. The script persisted those mirror rows only after
`submit_intents` returned. At gate time, each projected archive entry was therefore
`id -> null`, while replay expected `id -> full pre-prune row`, for both task and claim
archives. The gate raised and rolled back before the persistence code could run.

The repair pre-stages the exact hot rows in both archive mirrors before the governed
transaction. Extra mirror rows are outside the signed projection until their prune
event exists. If submit fails, byte-for-byte mirror backups are restored. The new
permanent regression runs real enforced-runtime `--apply`, requires exit 0 and drift
false, then requires `--check` exit 0.

The validator comment and task file now declare the porting relaxation: selector syntax
is required only for active claims because it is a live collision guard; released or
blocked historical rows preserve their signed legacy scope verbatim.

Verified by exit code:

- prune_state cases: 5 passed, including enforced real-apply regression.
- runtime replay cases: 8 passed.
- collaboration validator: exit 0.
- encoding scan: exit 0.
- domain-neutrality scan: exit 0.

TASK-0278 was also closed through the implementer-only signed transition at seq
5405-5407 before this remediation began.
