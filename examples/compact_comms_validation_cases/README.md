# Compact communication validation cases

Golden cases for DECISION-0005 soft checks.

| Case | Expected exit | Purpose |
|------|---------------|---------|
| `valid_compact` | 0 | Compact open message with response request, `requested_action`, `question` and `context_refs`. |
| `missing_question` | 1 | Compact open message with `requires_response:true` but no `question`. |
| `legacy_exempt` | 0 | Legacy open message with `requested_action` but no compact fields. |
| `missing_context_refs_warning` | 0 | Compact message references existing work without `context_refs`, producing a warning. |

Run:

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File examples\compact_comms_validation_cases\run_compact_comms_cases.ps1
```
