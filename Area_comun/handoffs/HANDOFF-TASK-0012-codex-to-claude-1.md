---
handoff_id: HANDOFF-TASK-0012-codex-to-claude-1
task_id: TASK-0012
spec_id: Area_comun/specs/SPEC-0012-example-minimal-sdd.md
from: Codex
to: Claude
date: 2026-06-05
status: for_review
requires_response: yes
response_owner: Claude
requested_action: Review TASK-0012 against SPEC-0012; if acceptable, mark TASK-0012 done.
acceptance_criteria_verified: yes
tests_run:
  - python validator on examples/minimal_sdd_instance
  - powershell validator on examples/minimal_sdd_instance
  - neutrality scan over examples/minimal_sdd_instance
spec_deviations:
  - none
decisions_referenced:
  - DECISION-0004
  - DECISION-0002
---

# Handoff: TASK-0012 Minimal SDD Instance

## 1. Minimal Context
`TASK-0012` creates a neutral example instance with SDD enabled.

## 2. What Was Done
- Created `examples/minimal_sdd_instance/` from the minimal instance.
- Enabled `sdd.enabled:true` in its `protocol.config.json`.
- Added `Area_comun/specs/SPEC-0002-sdd-example.md`.
- Added `TASK-0002` as an `implementation` task with the six SDD fields.
- Added a matching handoff inside the example.

## 3. What Was Not Done
No profiles, stack-specific content or domain policy were added.

## 4. Acceptance Criteria Verified
| Criterion | Evidence | Status |
|-----------|----------|--------|
| Example validates with SDD enabled. | Python and PowerShell validators return OK. | met |
| Contains at least one spec. | `Area_comun/specs/SPEC-0002-sdd-example.md`. | met |
| Contains at least one conforming implementable task. | `TASK-0002` declares all six SDD fields. | met |
| Neutral of domain. | Neutrality scan returned no matches. | met |

## 5. Tests Run
```text
python scripts\validate_collaboration_state.py --root examples\minimal_sdd_instance
OK: collaboration state is valid.

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root examples\minimal_sdd_instance
OK: collaboration state is valid.

rg -n "(trading|\.NET|dotnet|SQL Server|Azure DevOps|Docker|Dev Container|Desarrollo_DotNet)" examples\minimal_sdd_instance
Result: no matches.
```

## 6. Spec Deviations
None.

## 7. Requested Action
Review against `SPEC-0012-example-minimal-sdd.md`; if acceptable, mark `TASK-0012` done.

## 8. Risks and Assumptions
The example intentionally keeps the original `TASK-0001` from `minimal_instance` as pre-SDD history
and adds `TASK-0002` as the SDD demonstration.

## 9. Open Questions / BLOCKED
None.

## 10. Pointers
- `examples/minimal_sdd_instance/`
- `Area_comun/specs/SPEC-0012-example-minimal-sdd.md`
- `Area_comun/artifacts/DISENO-SDD.md`
