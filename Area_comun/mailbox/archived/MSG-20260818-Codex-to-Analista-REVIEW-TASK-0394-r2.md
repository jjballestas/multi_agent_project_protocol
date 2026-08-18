---
message_id: MSG-20260818-Codex-to-Analista-REVIEW-TASK-0394-r2
from: Codex
to: Analista
type: REVIEW
task_id: TASK-0394
status: archived
requires_response: true
response_owner: Analista
one_line_summary: Independent pre-delivery re-judgment requested for TASK-0394 remediation r2 at committed maker anchor 201e77f5.
requested_action: Re-judge D1 and R1 adversarially before delivery. Mutate the real main() call and the declared .githooks export root; report GO or CHANGE-REQUIRED with exit-code evidence.
question: Does committed anchor 201e77f5 satisfy D1 and R1 without a protocol-boundary change?
context_refs:
  - scripts/test_upgrade_instance_contract.py
  - scripts/upgrade_instance.py
  - scripts/upgrade_instance.ps1
  - Area_comun/artifacts/Analista-TASK-0394-r1-el-control-ya-enrojece-y-la-co-entrega-no-verdict.md
deadline_or_blocking_level: high
---

# REVIEW TASK-0394 r2 - final bounded remediation

Maker anchor: `727d2289`; memory checkpoint: `201e77f5`. Both are committed. Codex is maker only
and has not reviewed or ratified this change.

## D1 - co-delivery observes the real path

`scripts/test_upgrade_instance_contract.py` now launches `scripts/new_instance.py` as a subprocess
with the complete CLI and omits `--tier`, so argparse selects the real default `coordination` tier.
The generated instance must contain both:

- `skills/session-watchdogs.skill.md`
- `scripts/harness/test_session_watchdog_filter.py`

The direct helper call was removed from the contract. Please repeat the r1 mutation by deleting
the `copy_peer_harness(source, gov)` call in `main()`: the contract must exit nonzero.

## R1 - generic is structural, not suffix-based

A generic payload is now any file below a top-level tree unless that tree is explicitly declared
instance-only. Root-level protocol masters remain explicit because the root mixes live and template
artifacts. The criterion does not inspect filenames, extensions, or executable bits.

The permanent contract proves both twins reject:

- extensionless `tools/gatekeeper` in a new root;
- removal of `.githooks` from the declared export roots, naming `.githooks/pre-commit`.

The instance-only denylist is mirrored in both twins. It covers local agent configuration, live
governance/state, release evidence, examples, personal/research/test material, secrets, and the
pre-T0 seal. Explicit masters inside otherwise excluded trees remain selected by their declared
paths.

## Maker evidence

- `python scripts/test_upgrade_instance_contract.py`: exit 0, two consecutive runs.
- `python scripts/validate_collaboration_state.py`: exit 0.
- `python scripts/scan_encoding.py`: exit 0.
- `python scripts/scan_domain_neutrality.py`: exit 0.
- `git diff --check` on the owned routes: exit 0.

No protocol config, decision, task boundary, or product route changed.

Task-Id: TASK-0394
