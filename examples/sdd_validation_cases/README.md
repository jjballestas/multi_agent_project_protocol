# SDD validation cases

Golden cases for `validate_collaboration_state.py` and `validate_collaboration_state.ps1`.

| Case | Expected exit | Purpose |
|------|---------------|---------|
| `valid_enforced` | 0 | SDD enabled, implementable task complete, `spec_id` resolves. |
| `missing_required_fields` | 1 | One task missing each full SDD field, plus one task with unresolved `spec_id`. |
| `presdd_exempt` | 0 | Pre-SDD task is exempt with SDD enabled. |
| `lightweight_warnings` | 0 | Lightweight task missing minimum fields emits warnings, not errors. |

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File examples\sdd_validation_cases\run_sdd_cases.ps1
```
