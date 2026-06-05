---
handoff_id: HANDOFF-TASK-0009-codex-to-claude-1
task_id: TASK-0009
spec_id: Area_comun/specs/SPEC-0009-sdd-templates.md
from: Codex
to: Claude
date: 2026-06-05
status: for_review
requires_response: yes
response_owner: Claude
requested_action: Review TASK-0009 against SPEC-0009; if acceptable, mark TASK-0009 done.
acceptance_criteria_verified: yes
tests_run:
  - rg neutrality scan over protocol/report/spec templates
  - powershell validator on root, minimal_instance, dotnet_enterprise_instance
  - python validator on root, minimal_instance, dotnet_enterprise_instance
spec_deviations:
  - none
decisions_referenced:
  - DECISION-0004
  - DECISION-0002
  - DECISION-0001
---

# Handoff: TASK-0009 SDD Protocol Templates

## 1. Minimal Context
`TASK-0009` updates the core protocol templates to express SDD fields, clarity-before-execution
rules, acceptance criteria verification and test-plan evidence.

## 2. What Was Done
- Updated `Area_comun/protocol/TASK_PROTOCOL.md` with the SDD gate, task types, clarity before
  execution, claim eligibility and review against spec/criteria.
- Updated `Area_comun/protocol/TASK_TEMPLATE.md` with `type`, full SDD fields and lightweight SDD
  fields.
- Updated `Area_comun/protocol/HANDOFF_TEMPLATE.md` with `spec_id`,
  `acceptance_criteria_verified`, `tests_run`, `spec_deviations`, `decisions_referenced`, criteria
  evidence and tests sections.
- Updated `Area_comun/reports/HUMAN_REPORT_TEMPLATE.md` with SDD report summary fields.

## 3. What Was Not Done
No validator SDD enforcement was implemented; that is `TASK-0011`.

## 4. Acceptance Criteria Verified
| Criterion | Evidence | Status |
|-----------|----------|--------|
| The 4 templates include DISENO-SDD section 2 elements and stay domain-neutral. | Files listed above plus neutrality scan. | met |
| `TASK_TEMPLATE.md` distinguishes fields by `type`. | Full SDD and lightweight SDD sections added. | met |
| Existing instances/examples are not broken. | Python and PowerShell validators green. | met |

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
None.

## 7. Requested Action
Review against `SPEC-0009-sdd-templates.md`; if acceptable, mark `TASK-0009` done.

## 8. Risks and Assumptions
`TASK_TEMPLATE.md` now includes both full and lightweight SDD field examples. The future validator
will define how strictly these are parsed.

## 9. Open Questions / BLOCKED
None.

## 10. Pointers
- `Area_comun/specs/SPEC-0009-sdd-templates.md`
- `Area_comun/artifacts/DISENO-SDD.md`
- `Area_comun/decisions/DECISION-0004-sdd-pipeline-y-cierre.md`
