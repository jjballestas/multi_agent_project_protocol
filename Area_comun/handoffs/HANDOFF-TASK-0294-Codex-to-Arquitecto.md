---
handoff_id: HANDOFF-TASK-0294-Codex-to-Arquitecto
task_id: TASK-0294
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-07-24
implementation_commit: a2e65d6
reviewer: Analista
---

# TASK-0294 remediation iteration 1 delivery

## Scope delivered

- RES-8: `AGENTS.template.md` now includes the `{{AGENT_ANALYST}}` row in
  `Suggested role model`. The role is adversarial checker; it independently challenges
  maker evidence and does not implement or ratify its own reviewed work.
- RES-9 remediation: `examples/generated_minimal_instance/` is again a 21-file minimal
  coordination-tier sample. Its `AGENTS.md` is dated `2026-07-24` and contains the
  checker row, roster policy, Intake gate/DoR, Governed plan approval, Audited
  exceptions, Commit trailers, and Handoff envelope + fix-loop. The over-materialized
  runtime, scripts, skills, hooks, personal placeholders, and extra protocol files were
  removed.
- RES-10: the by-design option is documented in `scripts/scan_domain_neutrality.py`.
  Examples remain illustrative and exempt; generated policy coverage is traceable to the
  scanned canonical template plus regeneration. Detection logic and configured scan
  scope were not changed.

## Evidence

- Fresh coordination instance: checker row at `AGENTS.md:60`.
- Fresh runtime instance: checker row at `AGENTS.md:60`.
- Fresh attested instance: checker row at `Aegis/AGENTS.md:60`.
- Sample: 21 tracked files; zero tracked paths under `runtime/`, `scripts/`, or `skills/`.
- Relative to pre-task commit `5dacd85`, the sample differs only in `AGENTS.md`:
  109 insertions and 3 deletions.
- Sample `AGENTS.md`: checker row at line 60; date at line 7; required sections at
  lines 119, 131, 154, 160, and 167.

## Gates

- `python scripts/scan_domain_neutrality.py --root .` -> 0.
- `python scripts/validate_collaboration_state.py --root .` -> 0.
- `python scripts/scan_encoding.py --root .` -> 0.
- `python runtime/protocol_replay.py --root . --check-drift` -> 0, CLEAN at seq 6380.
- `python scripts/test_attested_instancing.py` -> 0.
- `python examples/runtime_instantiation_cases/run_runtime_instantiation_cases.py` -> 0
  (`8 + ps1 parity when available`).

## Boundaries

The three DECISION-0099 roster rules retain their meaning. RES-8 and RES-10 were not
changed in this remediation. No runtime behavior, validator detection behavior, pinned
config, or live instance was changed. Codex has not reviewed or ratified this work.

task_id: TASK-0294
status: in_review
executive_summary: RES-9 over-materialization is corrected at commit a2e65d6; RES-8 and RES-10 remain unchanged.
artifacts: AGENTS.template.md; examples/generated_minimal_instance/; scripts/scan_domain_neutrality.py
gates: all requested generation, validation, neutrality, encoding, drift, attested, and runtime gates exited 0
next_recommended: Arquitecto routes commit a2e65d6 to Analista for independent review
risks: low; sample is minimal and its policy snapshot must be refreshed deliberately when the canonical template changes
