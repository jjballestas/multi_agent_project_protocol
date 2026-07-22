---
handoff_id: HANDOFF-TASK-0263-codex-to-arquitecto
task_id: TASK-0263
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-07-23
implementation_commit: f97e0e1
---

# TASK-0263 delivery

Implementation commit `f97e0e1` adds the C3-bis improvement-offer mechanism.

Design: `runtime/improvement_offers.py` consumes runtime JSON/JSONL and mailbox
`REPORTE` files through one evaluator. Root identity is NFKC + case-fold + trim +
whitespace-collapse, then exact equality. The governed durable registry is
`Area_comun/protocol/improvement_offer_registry.json`. Stable proposal ids derive
only from the normalized root key; evidence ids bind carrier, delivery, obstacle,
root, and resolution.

Anti-loop: accepted offers never recur. Rejected/parked offers recur only when the
evidence set changes AND the caller explicitly passes that proposal id through
`--new-evidence`. Unchanged open offers are suppressed.

No-auto-application: output is a drafted rule plus regression text and citations.
The module cannot edit skills/rules, create tasks/decisions, or submit ledger intents;
its declared application path is human acceptance -> DECISION -> governed task.

Evidence:

- `python examples/improvement_offer_cases/run_improvement_offer_cases.py` -> PASS,
  6 cases, including both carriers and all five acceptance cases.
- `python -m py_compile runtime/improvement_offers.py examples/improvement_offer_cases/run_improvement_offer_cases.py` -> PASS.
- `python scripts/validate_collaboration_state.py` -> exit 0.
- `python scripts/scan_encoding.py` -> exit 0.
- `python scripts/scan_domain_neutrality.py` -> exit 0.
- `git diff --check` -> exit 0.

Independent review requested from Analista. Codex has not reviewed or ratified this work.
