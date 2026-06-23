---
handoff_id: HANDOFF-TASK-0158-codex-to-arquitecto-4
task_id: TASK-0158
from: Codex
to: Arquitecto
status: in_review
created_at: 2026-06-23T01:12:00Z
---

# TASK-0158 - CAMBIO v3 delivered

## Change
- Removed the instance-specific default env path from `connectors/sqlserver_readonly/s9_verify_live.py`.
- The live s9 verifier now reads the env file from `--env` or `SQLSERVER_S9_ENV_FILE`.
- Missing env path fails closed with a clear error.

## Evidence
- `Get-ChildItem -Recurse -File connectors | Select-String -Pattern 'nova|budget|treasury|paycontrol|accounting'`: no matches.
- `python -m py_compile connectors\sqlserver_readonly\connector.py connectors\sqlserver_readonly\s9_verify_live.py examples\connector_sqlserver_readonly_cases\run_connector_sqlserver_readonly_cases.py`: PASS.
- `python examples\connector_sqlserver_readonly_cases\run_connector_sqlserver_readonly_cases.py`: PASS.
- Live s9 with `SQLSERVER_S9_ENV_FILE` pointing to the gitignored operator env: PASS.
  - SELECT row_count=1.
  - DML `DELETE ordinary_user_table_zero_rows`: error 229, `permission_denied_on_principal`.
  - DDL `CREATE TABLE`: error 262, `permission_denied_on_principal`.
- `python scripts\scan_encoding.py --root .`: PASS.
- `python scripts\scan_domain_neutrality.py --root .`: PASS.
- `python scripts\validate_collaboration_state.py --root .`: PASS.
- Drift: `has_drift=false`, `up_to_seq=1274` before delivery close.

## Notes
- `connectors/connectors.config.json` remains `enabled:false`.
- `protocol.config.json` was not touched.
- No `.env`, credential, schema name or table name was committed.
- No live-use flip was made.
