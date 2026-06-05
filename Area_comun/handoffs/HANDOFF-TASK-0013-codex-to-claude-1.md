---
handoff_id: HANDOFF-TASK-0013-codex-to-claude-1
task_id: TASK-0013
spec_id: Area_comun/specs/SPEC-0013-doc-sdd-onboarding.md
from: Codex
to: Claude
date: 2026-06-05
status: for_review
requires_response: yes
response_owner: Claude
requested_action: Review TASK-0013 against SPEC-0013; if acceptable, mark TASK-0013 done.
acceptance_criteria_verified: yes
tests_run:
  - python validator on root and examples
  - powershell validator on root and examples
  - neutrality scan over README_INSTANCIACION.md
spec_deviations:
  - none
decisions_referenced:
  - DECISION-0004
  - DECISION-0001
---

# Handoff: TASK-0013 SDD Onboarding Documentation

## 1. Minimal Context
`TASK-0013` documents how a new instance starts in SDD mode.

## 2. What Was Done
- Added an SDD onboarding section to `README_INSTANCIACION.md`.
- Documented the config block, spec creation, six implementable-task fields and validation commands.
- Linked the flow to `examples/minimal_sdd_instance/`.

## 3. What Was Not Done
No release/version publication was performed.

## 4. Acceptance Criteria Verified
| Criterion | Evidence | Status |
|-----------|----------|--------|
| Documentation explains SDD activation. | New section shows the `sdd` config block. | met |
| Documentation explains task fields. | New section lists the six full SDD fields and four lightweight fields. | met |
| Documentation points to templates and example. | References `SPEC_TEMPLATE.md` and `examples/minimal_sdd_instance/`. | met |
| Validator remains green. | Root and examples validate with both validators. | met |

## 5. Tests Run
```text
python scripts\validate_collaboration_state.py --root .
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .
Result: OK.

python scripts\validate_collaboration_state.py --root examples\minimal_sdd_instance
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root examples\minimal_sdd_instance
Result: OK.

rg -n "(trading|\.NET|dotnet|SQL Server|Azure DevOps|Docker|Dev Container|Desarrollo_DotNet)" README_INSTANCIACION.md
Result: no matches.
```

## 6. Spec Deviations
None.

## 7. Requested Action
Review against `SPEC-0013-doc-sdd-onboarding.md`; if acceptable, mark `TASK-0013` done.

## 8. Risks and Assumptions
The documentation keeps SDD optional and config-gated, matching DECISION-0004.

## 9. Open Questions / BLOCKED
None.

## 10. Pointers
- `README_INSTANCIACION.md`
- `examples/minimal_sdd_instance/`
- `Area_comun/specs/SPEC-0013-doc-sdd-onboarding.md`
