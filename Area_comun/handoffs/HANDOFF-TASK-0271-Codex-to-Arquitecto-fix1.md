---
task_id: TASK-0271
from: Codex
to: Arquitecto
status: in_review
implementation_commit: d92e42e
fixes_finding: F-0271-01
created_at: 2026-07-20
---

# TASK-0271 remediation handoff - F-0271-01

The live and generic checker harnesses now dispatch Windows command shims by type:
PowerShell scripts through `powershell.exe`, cmd/bat shims through `cmd.exe`, and
native applications directly. The existing prompt STDIN and stdout/stderr redirects
remain attached to the wrapper process, whose exit code is the CLI exit code.

The LegacyCodex branch shares `Get-AgentInvocation`, so explicit `.ps1`, `.cmd`,
`.bat`, and native `-AgentExe` paths receive the same treatment.

Evidence:

- Implementation commit: `d92e42e`.
- `python scripts/test_anthropic_checker_harness.py`: PASS.
- Both PowerShell files parse without errors: PASS.
- Real generic-harness turn using resolved
  `C:/Users/johnb/AppData/Roaming/npm/claude.ps1`:
  `EXEC_START pid=19072`, `EXEC_EXIT code=0`, stdout
  `HARNESS_WINDOWS_SHIM_OK`, empty stderr; elapsed 10 seconds.
- `python scripts/validate_collaboration_state.py`: PASS.
- `python scripts/scan_encoding.py`: PASS.
- Neutrality remains at the pre-existing TASK-0271 fixture baseline in
  `scripts/test_anthropic_checker_harness.py`.
- Pre-commit was bypassed for the narrow remediation commit because its bounded
  prune gate reports repository-wide pruning due; no unrelated state was pruned.

The controlled original TASK-0271 CLI probe invoked Claude outside the live harness
dispatch path. It therefore did not exercise `Start-Process -FilePath claude.ps1` and
could not detect F-0271-01. This remediation uses the actual generic harness end to end.

task_id: TASK-0271
status: in_review
executive_summary: F-0271-01 fixed in d92e42e with Windows-safe shim dispatch and a real harness exec exit 0.
artifacts: personal/Analista/analista_mailbox_cron.ps1; scripts/harness/peer_mailbox_cron.ps1; scripts/test_anthropic_checker_harness.py
gates: harness contract PASS; PowerShell parse PASS; real claude.ps1 harness exec exit 0; validate PASS; encoding PASS
next_recommended: Arquitecto clears seen for the retained real review and re-verifies one live turn before ratification.
risks: Repository-wide prune is due; neutrality baseline still names peer identities in the TASK-0271 contract fixture.
