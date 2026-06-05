---
handoff_id: HANDOFF-TASK-0011-codex-to-claude-1
task_id: TASK-0011
spec_id: Area_comun/specs/SPEC-0011-validator-sdd.md
from: Codex
to: Claude
date: 2026-06-05
status: for_review
requires_response: yes
response_owner: Claude
requested_action: Review TASK-0011 against SPEC-0011; if acceptable, mark TASK-0011 done.
acceptance_criteria_verified: yes
tests_run:
  - examples/sdd_validation_cases/run_sdd_cases.ps1
  - python validator on root, minimal_instance, generated_minimal_instance, dotnet_enterprise_instance
  - powershell validator on root, minimal_instance, generated_minimal_instance, dotnet_enterprise_instance
  - domain-neutrality scan over protocol/report/spec templates
spec_deviations:
  - none
decisions_referenced:
  - DECISION-0004
  - DECISION-0001
  - DECISION-0003
---

# Handoff: TASK-0011 SDD Validator Mode

## 1. Minimal Context
`TASK-0011` adds config-gated SDD validation to both collaboration state validators. The feature is
off by default and is governed by `Area_comun/specs/SPEC-0011-validator-sdd.md`.

## 2. What Was Done
- Added `sdd` defaults to `protocol.config.template.json` with `enabled:false`.
- Added SDD parsing and validation to `scripts/validate_collaboration_state.py`.
- Mirrored the SDD behavior in `scripts/validate_collaboration_state.ps1`.
- Created `examples/sdd_validation_cases/` with positive, negative, pre-SDD exemption and
  lightweight-warning cases.
- Added a fixture harness that compares Python and PowerShell exit codes and normalized output.
- Completed TASK-0011 frontmatter with the six SDD fields.

## 3. What Was Not Done
No live instance was switched to `sdd.enabled:true`. No retroactive migration of historical tasks was
performed.

## 4. Acceptance Criteria Verified
| Criterion | Evidence | Status |
|-----------|----------|--------|
| SDD disabled preserves existing behavior. | Root and existing examples validate green without `sdd.enabled`. | met |
| Enabled SDD errors on missing full fields. | `missing_required_fields` covers each of the six full SDD fields. | met |
| Enabled SDD errors on unresolved `spec_id`. | `missing_required_fields` includes `TASK-BAD-SPEC`. | met |
| Pre-SDD tasks are exempt. | `presdd_exempt` exits 0. | met |
| Lightweight tasks warn without failing. | `lightweight_warnings` exits 0 with matching warnings. | met |
| Python and PowerShell parity. | `run_sdd_cases.ps1` compares exit codes and normalized output. | met |

## 5. Tests Run
```text
powershell -NoProfile -ExecutionPolicy Bypass -File examples\sdd_validation_cases\run_sdd_cases.ps1
OK valid_enforced
OK missing_required_fields
OK presdd_exempt
OK lightweight_warnings
OK: SDD validation cases passed.

python scripts\validate_collaboration_state.py --root .
OK: collaboration state is valid.

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root .
OK: collaboration state is valid.

python scripts\validate_collaboration_state.py --root examples\minimal_instance
python scripts\validate_collaboration_state.py --root examples\generated_minimal_instance
python scripts\validate_collaboration_state.py --root examples\dotnet_enterprise_instance
All returned: OK: collaboration state is valid.

powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root examples\minimal_instance
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root examples\generated_minimal_instance
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\validate_collaboration_state.ps1 -Root examples\dotnet_enterprise_instance
All returned: OK: collaboration state is valid.

python -m py_compile scripts\validate_collaboration_state.py
Result: OK.

rg -n --glob '*TEMPLATE*.md "(trading|\.NET|dotnet|SQL Server|Azure DevOps|Docker|Dev Container|Desarrollo_DotNet)" Area_comun\protocol Area_comun\reports Area_comun\specs
Result: no matches.
```

## 6. Spec Deviations
None.

## 7. Requested Action
Review against `SPEC-0011-validator-sdd.md`; if acceptable, mark `TASK-0011` done.

## 8. Risks and Assumptions
The frontmatter parser intentionally supports the repo's current lightweight subset: scalar fields,
one-line arrays and Markdown sections. It does not introduce a YAML dependency.

## 9. Open Questions / BLOCKED
None.

## 10. Pointers
- `scripts/validate_collaboration_state.py`
- `scripts/validate_collaboration_state.ps1`
- `protocol.config.template.json`
- `examples/sdd_validation_cases/`
- `Area_comun/specs/SPEC-0011-validator-sdd.md`
- `Area_comun/artifacts/DISENO-SDD.md`
