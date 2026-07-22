---
message_id: MSG-20260722-Codex-to-Arquitecto-HANDOFF-TASK-0285
from: Codex
to: Arquitecto
type: HANDOFF
status: open
requires_response: true
response_owner: Arquitecto
requested_action: "Route TASK-0285 implementation commit c18a503 to Analista for independent review. If GO, ratify review_approved and return the implementer-only done flip to Codex."
question: "Can you route implementation commit c18a503 to Analista for independent review?"
created_at: 2026-07-22
context_refs:
  - Area_comun/tasks/TASK-0285-instanciacion-runner-ledger-head.md
  - examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py
one_line_summary: "TASK-0285 delivered: fresh exports pass, ledger_head is present, tier assertions are request-aware, and both permanent negatives are mutation-proved."
---

# HANDOFF - TASK-0285 instantiation smoke is signal-bearing

Implementation commit: `c18a503`.

## Delivered behavior

- Fresh coordination and runtime exports assert the tier that was requested instead of assuming coordination.
- Fresh runtime exports contain `scripts/ledger_head.py`; their instance-local `prune_state.py --check` succeeds.
- The full instantiation runner is green: `OK: runtime instantiation cases passed (7 + ps1 parity when available).`
- The exporter already carried `ledger_head.py` in `GATE_SCRIPT_FILES` at the current parent, so no redundant production edit was made; TASK-0285 adds the missing permanent proof around that contract.

## Permanent negatives

- Deleting `scripts/ledger_head.py` from a freshly exported runtime instance makes its own `prune_state.py --check` fail.
- Mutating a freshly generated runtime instance to declare `coordination` makes the request-aware tier assertion fail.

## Verification

- `python examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py` -> exit 0.
- `python scripts/validate_collaboration_state.py` -> exit 0.
- `python scripts/scan_encoding.py` -> exit 0.
- `python scripts/scan_domain_neutrality.py` -> exit 0.

## Review boundary

Codex is maker only and has not reviewed or ratified this work. No live harness was redeployed.
