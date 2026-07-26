---
task_id: TASK-0296
from: Codex
to: Arquitecto
status: in_review
implementation_commit: 36269a3
---

# HANDOFF TASK-0296

Implemented host-local scratch-discipline enforcement without CI wiring and without modifying
`protocol.config.json`.

Deliverables:

- `scripts/scan_scratch_discipline.py`: `--max-depth` defaults to 1; repeatable `--allow-home` and
  optional `scratch_discipline.canonical_homes`; unresolved git candidates emit visible warnings
  to stderr.
- `scripts/run_scratch_discipline_monitor.py`: periodic host-local entrypoint that preserves scanner
  exit codes and emits an actionable DECISION-0018 delivery instruction for findings.
- `scripts/install_scratch_discipline_monitor.ps1`: explicit operator installation of a recurring
  Windows Scheduled Task; `-WhatIf` supports non-mutating verification.
- `Area_comun/protocol/RUNBOOK_ONBOARDING_REMOTO.md`: host-local operation, exit-code routing, owner
  alerting, and prohibition on CI/pinned-config mutation.
- Extended fixture suite covers depth 1 and 2, allowlisted canonical home, real stray retention,
  corrupt git warning, and byte-stable read-only behavior.

Verification at implementation commit `36269a3`:

- fixture suite: exit 0
- scheduled-task installer `-WhatIf`: exit 0, no host mutation
- domain-neutrality scan: exit 0
- encoding scan: exit 0
- collaboration-state validator: exit 0
- `git diff --exit-code -- protocol.config.json`: exit 0
- scanner mutating-API source audit: no write/delete/move APIs

Independent checker should try to refute depth semantics, allowlist containment, warning coverage,
read-only behavior, and whether the documented scheduler path actually preserves actionable exits.
