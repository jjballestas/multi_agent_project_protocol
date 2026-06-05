---
handoff_id: HANDOFF-TASK-0010-codex-to-claude-1
task_id: TASK-0010
spec_id: Area_comun/specs/SPEC-0010-specs-folder.md
from: Codex
to: Claude
date: 2026-06-05
status: for_review
requires_response: yes
response_owner: Claude
requested_action: Review TASK-0010 against SPEC-0010; if acceptable, mark TASK-0010 done.
acceptance_criteria_verified: yes
tests_run:
  - rg neutrality scan over protocol/report/spec templates
  - powershell validator on root, minimal_instance, dotnet_enterprise_instance
  - python validator on root, minimal_instance, dotnet_enterprise_instance
spec_deviations:
  - Added REQUIREMENTS_TEMPLATE.md and ACCEPTANCE_CRITERIA_TEMPLATE.md as requested by the human owner; this is additive to SPEC-0010's four-template minimum.
decisions_referenced:
  - DECISION-0004
  - DECISION-0002
---

# Handoff: TASK-0010 Reusable SDD Spec Templates

## 1. Minimal Context
`TASK-0010` creates reusable, domain-neutral templates under `Area_comun/specs/`.

## 2. What Was Done
Created:

- `Area_comun/specs/SPEC_TEMPLATE.md`
- `Area_comun/specs/PROJECT_BRIEF_TEMPLATE.md`
- `Area_comun/specs/REQUIREMENTS_TEMPLATE.md`
- `Area_comun/specs/ACCEPTANCE_CRITERIA_TEMPLATE.md`
- `Area_comun/specs/TEST_PLAN_TEMPLATE.md`
- `Area_comun/specs/TRACEABILITY_MATRIX_TEMPLATE.md`

## 3. What Was Not Done
Concrete rollout specs `SPEC-0009..SPEC-0013` were not modified.

## 4. Acceptance Criteria Verified
| Criterion | Evidence | Status |
|-----------|----------|--------|
| Templates exist and are domain-neutral. | Six templates created; neutrality scan returned no matches. | met |
| `SPEC_TEMPLATE.md` covers the six SDD fields. | Includes `execution_pipeline`, `acceptance_criteria`, `linked_decisions`, `test_plan`, `closure_criteria` and frontmatter `spec_id`. | met |
| Templates are coherent with `TASK_TEMPLATE.md`. | Both use the same SDD field names and task/spec references. | met |

## 5. Tests Run
```text
rg -n --glob '*TEMPLATE*.md "(trading|\.NET|dotnet|SQL Server|Azure DevOps|Docker|Dev Container|Desarrollo_DotNet)" Area_comun\protocol Area_comun\reports Area_comun\specs
Result: no matches.

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .
OK: collaboration state is valid.

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root examples\minimal_instance
OK: collaboration state is valid.

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root examples\dotnet_enterprise_instance
OK: collaboration state is valid.

python scripts\validate_collaboration_state.py --root .
OK: collaboration state is valid.

python scripts\validate_collaboration_state.py --root examples\minimal_instance
OK: collaboration state is valid.

python scripts\validate_collaboration_state.py --root examples\dotnet_enterprise_instance
OK: collaboration state is valid.
```

## 6. Spec Deviations
The human request explicitly listed `REQUIREMENTS_TEMPLATE.md` and
`ACCEPTANCE_CRITERIA_TEMPLATE.md`. I included them as additive templates beyond the four listed in
`SPEC-0010`; the original four were also created.

## 7. Requested Action
Review against `SPEC-0010-specs-folder.md`; if acceptable, mark `TASK-0010` done.

## 8. Risks and Assumptions
The two additional templates are additive and neutral. They do not change validator behavior.

## 9. Open Questions / BLOCKED
None.

## 10. Pointers
- `Area_comun/specs/SPEC-0010-specs-folder.md`
- `Area_comun/artifacts/DISENO-SDD.md`
- `Area_comun/decisions/DECISION-0004-sdd-pipeline-y-cierre.md`
