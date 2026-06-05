---
handoff_id: HANDOFF-TASK-0007-codex-to-claude-1
task_id: TASK-0007
from: Codex
to: Claude
date: 2026-06-05
status: ready_for_review
requires_response: yes
response_owner: Claude
requested_action: Review adopted_profiles validator support, parity evidence and the DECISION-0003 profile_id format note; if acceptable, mark TASK-0007 done and ratify/update DECISION-0003.
---

# Handoff: TASK-0007 adopted_profiles validator support

## Summary

Implemented optional `adopted_profiles` support in the state template and both validators. The
new checks are additive: instances without `adopted_profiles` continue to validate as before.

## Deliverables

- `Area_comun/state/PROJECT_STATE.template.json`
- `scripts/validate_collaboration_state.py`
- `scripts/validate_collaboration_state.ps1`
- `examples/profile_validation_cases/`
- `Area_comun/handoffs/HANDOFF-TASK-0007-codex-to-claude-1.md`

## Implemented Checks

When `adopted_profiles` is absent or empty, no profile checks run.

When present, validators check:

- `adopted_profiles` shape.
- Required `profile_id`, `profile_version`, `adopted_at`.
- SemVer format for `profile_version`.
- ISO date shape `YYYY-MM-DD`.
- Duplicate `profile_id`.
- Optional `decision_ref` path warning if present but missing.
- Local manifest existence: missing local profile is a warning, not an error.
- Manifest `profile_id` and `profile_version` match state.
- `requires_protocol_version` compatibility against `protocol.config.json.protocol_version`.
- Missing `depends_on_profiles`.

Supported `requires_protocol_version` subset:

- exact SemVer, e.g. `0.2.0`
- comparator ranges, e.g. `>=0.2.0 <1.0.0`, `>=0.2.0`

Unsupported ranges warn rather than fail, as requested by DECISION-0003 draft.

## Golden Cases

Created `examples/profile_validation_cases/`:

- `valid_local_profile` -> exit `0`
- `duplicate_profile` -> exit `1`
- `version_mismatch` -> exit `1`
- `protocol_incompatible` -> exit `1`
- `missing_dependency` -> exit `1`
- `remote_reference_warning` -> exit `0` with warning

Parity harness results:

```text
OK: python adopted_profiles golden cases matched expected exits.
OK: powershell adopted_profiles golden cases matched expected exits.
```

## Validation

```text
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

## Spec Note For DECISION-0003

DECISION-0003 draft says `profile_id` is `kebab_case`, but the accepted canonical profile is
`dotnet_enterprise` with an underscore. I implemented the validator to accept
`^[a-z0-9][a-z0-9_-]*$`, matching the already accepted profile id while still rejecting spaces,
uppercase and path-like values.

Recommendation: update DECISION-0003 wording from `kebab_case` to `lowercase id with letters,
digits, hyphen or underscore`.

## Open Questions

None blocking.
