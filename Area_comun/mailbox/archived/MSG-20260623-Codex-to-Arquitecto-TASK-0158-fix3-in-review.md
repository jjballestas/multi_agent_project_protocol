---
message_id: MSG-20260623-Codex-to-Arquitecto-TASK-0158-fix3-in-review
task_id: TASK-0158
type: HANDOFF
from: Codex
to: Arquitecto
status: archived
requires_response: false
response_owner: Arquitecto
one_line_summary: "TASK-0158 CAMBIO v3 delivered: s9 verifier env path is no longer instance-hardcoded; live s9 reconfirmed 229/262; task returned to in_review."
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0158-codex-to-arquitecto-4.md
  - connectors/sqlserver_readonly/s9_verify_live.py
  - Area_comun/artifacts/S9-TASK-0158-sqlserver-readonly-live.json
---

# TASK-0158 CAMBIO v3 in_review

Codex removed the instance-specific default env path from `connectors/sqlserver_readonly/s9_verify_live.py`.
The verifier now requires `--env` or `SQLSERVER_S9_ENV_FILE`, with no neutral-code default containing an instance
token.

Evidence is in `Area_comun/handoffs/HANDOFF-TASK-0158-codex-to-arquitecto-4.md`.
