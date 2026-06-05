---
handoff_id: HANDOFF-TASK-0002-codex-to-claude-1
task_id: TASK-0002
from: Codex
to: Claude
date: 2026-06-05
status: for_review
requires_response: no
---

# Handoff: TASK-0002 Python validator + CI

## 1. Minimal Context

TASK-0002 adds a cross-platform Python validator for this protocol repository and a GitHub
Actions workflow that runs it. The Python validator mirrors the existing PowerShell validator
while using only the Python standard library.

## 2. What Was Done

- Created `scripts/validate_collaboration_state.py`.
- Created `.github/workflows/validate.yml`.
- Validated both repository root and `examples/minimal_instance/`.
- Ran temporary negative checks for:
  - failed `state_invariants`;
  - task status mismatch between index and task markdown;
  - missing deliverable for a `done` task.

## 3. What Was Not Done

- Did not remove or deprecate the PowerShell validator.
- Did not add third-party dependencies.
- Did not change protocol semantics or domain boundaries.

## 4. How To Verify

```powershell
python scripts\validate_collaboration_state.py --root .
python scripts\validate_collaboration_state.py --root examples\minimal_instance
powershell -NoProfile -File scripts\validate_collaboration_state.ps1
powershell -NoProfile -File scripts\validate_collaboration_state.ps1 -Root examples\minimal_instance
```

Expected result for all four commands:

```text
OK: collaboration state is valid.
```

CI path:

- `.github/workflows/validate.yml`

## 5. Requested Action

Review for parity with the PowerShell validator and decide later whether both validators remain
supported or whether one becomes canonical.

## 6. Risks and Assumptions

- Assumption: keeping both validators is best for now because the Python version is new and the
  PowerShell version is already accepted.
- Risk: future logic drift between `.ps1` and `.py`; a future task can add shared fixtures or
  golden negative tests.

## 7. Open Questions / BLOCKED

None blocking. Open design question from the task remains: keep both validators or deprecate the
PowerShell version. Recommendation: keep both through v0.2.0, then reassess after CI history.

## 8. Pointers

- Task: `Area_comun/tasks/TASK-0002-codex-cross-platform-validator-ci.md`
- Python validator: `scripts/validate_collaboration_state.py`
- CI workflow: `.github/workflows/validate.yml`

