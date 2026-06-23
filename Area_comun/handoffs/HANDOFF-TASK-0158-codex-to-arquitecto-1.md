---
handoff_id: HANDOFF-TASK-0158-codex-to-arquitecto-1
task_id: TASK-0158
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-23T00:18:00Z
implementation_commit: e61f0ae
---

# TASK-0158 - Handoff Codex -> Arquitecto

## Entregado

- Backend vivo SQL Server read-only en `connectors/sqlserver_readonly/connector.py` usando `pymssql`.
- `open_live(env_path=...)` lee solo variables `SQLSERVER_*` desde `.env` gitignored; no hay credenciales hardcodeadas.
- `classify_readonly_sql` sigue delante de `read()`: DML/DDL/EXEC no allowlisted/multistatement no alcanzan el backend.
- `execute_unclassified_for_s9()` existe solo para la verificacion s9 server-side y salta el clasificador cliente.
- `connectors/connectors.config.json` registra `sqlserver_readonly` con `enabled:false`.
- `connectors/connectors.runtime.json` se resuelve antes que el config versionado y queda gitignored; el override temporal usado para s9 fue eliminado.
- Verificador vivo no-CI: `connectors/sqlserver_readonly/s9_verify_live.py`.
- Artefacto s9 saneado: `Area_comun/artifacts/S9-TASK-0158-sqlserver-readonly-live.json`.

## Evidencia

- Driver instalado: `python -m pip install pymssql`.
- Live s9: SELECT permitido con `row_count=1`.
- Live s9 server-side: DML rechazado por servidor (`OperationalError`, code `259`).
- Live s9 server-side: DDL rechazado por servidor (`OperationalError`, code `262`).
- `python -m py_compile connectors/sqlserver_readonly/connector.py connectors/sqlserver_readonly/s9_verify_live.py examples/connector_sqlserver_readonly_cases/run_connector_sqlserver_readonly_cases.py` PASS.
- `python examples/connector_sqlserver_readonly_cases/run_connector_sqlserver_readonly_cases.py` PASS.
- `python scripts/scan_encoding.py --root .` PASS.
- `python scripts/scan_domain_neutrality.py --root .` PASS.
- `python scripts/validate_collaboration_state.py --root .` PASS.
- Drift: `has_drift=false`, `up_to_seq=1249` before delivery ledger close.

## Caveat

`python scripts/validate_collaboration_state.py --root . --with-secrets` is not supported by the current validator CLI; the no-secret committed artifact is sanitized and contains no credentials, host, database, schema, table, or domain names.
