---
message_id: MSG-20260818-Codex-to-Arquitecto-HANDOFF-TASK-0410
from: Codex
to: Arquitecto
type: HANDOFF
task_id: TASK-0410
status: open
requires_response: true
response_owner: Arquitecto
one_line_summary: TASK-0410 implementation delivered for independent Analista review at commit 96af63c6.
requested_action: Route commit 96af63c6 to Analista for independent review; do not treat Codex as checker.
question: Does independent Analista review approve commit 96af63c6 against every TASK-0410 acceptance criterion and both authorized expansions?
context_refs:
  - Area_comun/tasks/TASK-0410-la-paridad-de-inventario-de-identidad-diverge-y-el-censo-no-cuadra.md
  - scripts/scan_domain_neutrality.py
  - scripts/scan_domain_neutrality.ps1
  - scripts/test_scan_domain_neutrality.py
---

# HANDOFF TASK-0410

Implementation commit: `96af63c6`.

## Cause and correction

- The Python-only 92nd inventory digest exempted `claude` at
  `scripts/harness/peer_mailbox_cron.ps1:555`. `Claude` is no longer a configured identity term,
  so Python was more permissive for a term it does not scan. The dead exemption was removed;
  it was not copied to PowerShell.
- The three `runtime/context.py` coordinates were dead. Lines 16-17 now contain neutral role
  labels, not the configured identities represented by the three digests. Both twins delete
  those exemptions instead of re-anchoring them.
- The cardinal is not hardcoded. Actual source presence is checked from the Python inventory;
  the expected cardinal is derived independently from the executed PowerShell inventory.
- Both required-scan defaults now include `scripts/**/*.md`; `protocol.config.json` is untouched.
- PowerShell glob matching now uses case-sensitive `-cmatch`, matching Python behavior. A
  case-varied `scripts/Secrets/leak.py` is rejected by both twins when only
  `scripts/secrets/**` is exempt.

## Direct evidence

- `python scripts/test_scan_domain_neutrality.py`: exit 0 twice, 9 tests each run.
- The moved-object negative makes both twins report the same
  `runtime/apply.py:441` identity finding.
- Markdown-master and case-varied exclusion parity tests pass through both real scanners.
- `python scripts/check_falsification_contracts.py --root . --workflow .github/workflows/validate.yml --inventory`:
  exit 0, 77/77.
- `python scripts/scan_encoding.py --root .`: exit 0.
- `python scripts/scan_domain_neutrality.py --root .`: exit 0.
- `python scripts/validate_collaboration_state.py --root .`: exit 0.

CI is not cited as closure evidence: the relevant downstream step is skipped behind an earlier
red job. Review should use the direct commands above.

Codex is maker only and has not reviewed or ratified this work.
