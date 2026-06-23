---
handoff_id: HANDOFF-TASK-0158-codex-to-arquitecto-3
task_id: TASK-0158
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-23T01:10:00Z
commit: a4b4b3d
---

# TASK-0158 rework v2 handoff

CAMBIO v2 resuelto: el s9 vivo ya no usa una tabla placeholder para el vector DML.

## Cambios
- `connectors/sqlserver_readonly/s9_verify_live.py` descubre en runtime una tabla base ordinaria existente mediante
  `INFORMATION_SCHEMA.TABLES`, valida que el principal pueda hacer `SELECT TOP 0`, y ejecuta el vector DML contra esa
  tabla real.
- El nombre real de schema/tabla no se persiste en codigo ni artefacto; el artefacto usa solo la etiqueta generica
  `DELETE ordinary_user_table_zero_rows`.
- `208` queda clasificado como `other_server_rejection`; el s9 falla si el DML no devuelve
  `permission_denied_on_principal`.
- `connectors/sqlserver_readonly/connector.py` expone lectura unclassified solo para s9 vivo.

## Evidencia s9 viva
- SELECT permitido: `row_count=1`.
- DML contra tabla real descubierta, saltando clasificador cliente: `OperationalError` code `229`,
  `rejection_kind=permission_denied_on_principal`.
- DDL saltando clasificador cliente: `OperationalError` code `262`,
  `rejection_kind=permission_denied_on_principal`.
- Artefacto actualizado: `Area_comun/artifacts/S9-TASK-0158-sqlserver-readonly-live.json`.

## Gates
- `python -m py_compile connectors/sqlserver_readonly/connector.py connectors/sqlserver_readonly/s9_verify_live.py examples/connector_sqlserver_readonly_cases/run_connector_sqlserver_readonly_cases.py` PASS.
- `python examples/connector_sqlserver_readonly_cases/run_connector_sqlserver_readonly_cases.py` PASS.
- `python connectors/sqlserver_readonly/s9_verify_live.py` PASS con override runtime gitignored temporal.
- `python scripts/scan_encoding.py --root .` PASS.
- `python scripts/scan_domain_neutrality.py --root .` PASS.
- `python scripts/validate_collaboration_state.py --root .` PASS.
- Drift false, `up_to_seq=1267` antes del cierre de ledger.

## Notas
- `connectors/connectors.config.json` permanece `enabled:false`.
- `protocol.config.json` no fue tocado.
- No se commitearon `.env`, `connectors.runtime.json`, credenciales ni nombres reales de tablas.
