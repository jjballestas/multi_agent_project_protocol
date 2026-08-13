---
id: MSG-20260813-Codex-to-Arquitecto-HANDOFF-TASK-0364-R1
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0364
status: open
created: 2026-08-13T20:40:00Z
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0364 remediation delivered with a same-commit dirty-fail and clean-pass AC2 witness plus truthful Windows interpreter evidence.
requested_action: Route independent re-review of only AC2 and the corrected AC1/AC4 PowerShell evidence; prior passes for AC1 placement, AC3, AC5, AC6, and AC7 remain unchanged.
question: Does the independent checker accept the same-head dirty-fail and clean-pass pair as discriminating AC2 evidence?
context_refs:
  - Area_comun/tasks/TASK-0364-la-ci-canonica-pasa-a-runners-propios.md
  - .github/workflows/validate.yml
  - https://github.com/jjballestas/multi_agent_project_protocol/actions/runs/31740992623
---

# TASK-0364 remediation handoff

Implementation commits: `6397ab5a`, `f52eca43`, `17a04fb5`; evidence commit: `0f06c31c`.

## AC2 discrimination

Both arms use workflow commit `17a04fb507e53b08ce0ccadb3c4db5942f70b918` and run id
`31740992623`.

- Dirty arm: attempt 2, job `94584608517`. A user-global
  `core.hooksPath=/tmp/task0364-poisoned-hooks` survived checkout worktree cleaning and the job
  failed exactly at `Reject persistent Git metadata contamination`.
- Clean arm: attempt 3, job `94585084015`. After removing only the global override, the same job
  passed all 5/5 steps and logged `PERSISTENT_GIT_METADATA CLEAN hooksPath=unset`.

This contaminant is outside the checkout worktree, is invisible to `git status`, and survives
`git clean -ffdx` plus `git reset --hard HEAD`. The Linux runner global override was removed after
the dirty arm.

## AC1 and AC4 correction

The Windows job remains under pwsh 7 because the service policy rejects script files under Windows
PowerShell 5.1. Its placement reason is Windows path and process semantics in the mailbox retry
runner. The publication step now invokes `powershell.exe` explicitly, so Windows PowerShell 5.1 is
executed and its version is reported instead of printing the pwsh 7 version twice.

## Gates

- `validate_collaboration_state.py`: exit 0
- `scan_encoding.py`: exit 0
- `scan_domain_neutrality.py`: exit 0
- YAML structure check and `git diff --check`: exit 0

Codex is maker only. Independent checker review and architect ratification remain required.

-- Codex
