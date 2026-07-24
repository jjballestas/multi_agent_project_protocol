---
handoff_id: HANDOFF-TASK-0293-Codex-to-Arquitecto
task_id: TASK-0293
from: Codex
to: Arquitecto
reviewer: Analista
status: ready_for_review
created_at: 2026-07-24
implementation_commit: 130f63c
delivery_commit: pending
---

# HANDOFF TASK-0293 - Roster policy residual polish

## Delivered

- `AGENTS.template.md` now governs every agent participant in the roster, without
  narrowing scope to code execution or altering human-owner authority.
- The signer/worker tier exception is conditional on a registry defining those tiers.
- Rule 3 explains that a checker unable to refute the maker makes the gate a rubber stamp.
- `examples/generated_minimal_instance/AGENTS.md` contains the same policy and all three rules.
- Runtime, validators, configuration, live instances, and the meaning of the three rules
  were not changed.

## Temporary tier evidence

Evidence root:
`C:/Users/johnb/AppData/Local/Temp/task0293-tier-evidence`

| Tier | Policy | Rules | Scope | Conditional registry | Rationale | agent_registry |
|---|---:|---:|---:|---:|---:|---:|
| coordination | 1 | 3 | 1 | 1 | 1 | 0 |
| runtime | 1 | 3 | 1 | 1 | 1 | 0 |
| attested | 1 | 3 | 1 | 1 | 1 | 1 |

The generated coordination/runtime configs contain no `agent_registry`, while their
generated policy wording remains valid because the tier exception is conditional.

## Verification

- `python scripts/validate_collaboration_state.py` -> 0
- `python scripts/scan_domain_neutrality.py` -> 0
- `python scripts/scan_encoding.py` -> 0
- `python runtime/protocol_replay.py --check-drift` -> 0
- `python scripts/test_attested_instancing.py` -> 0
- `python examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py` -> 0
- generated sample `Roster policy` count -> 1
- temporary generation for coordination/runtime/attested with five policy assertions -> 0

## Review boundary

Analista should independently verify the four requested text residuals and that the
three DECISION-0099 rules retain their normative meaning. Codex has not reviewed or
ratified its own work.
