---
handoff_id: HANDOFF-TASK-0158-codex-to-arquitecto-2
task_id: TASK-0158
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-23T00:50:00Z
commit: 31e0f23
---

# TASK-0158 rework handoff

Rework aplicado para el CAMBIO blocking sobre AC11: el s9 ya no usa DML contra catalogo del sistema como evidencia.

## Cambios
- `connectors/sqlserver_readonly/s9_verify_live.py` ahora registra cada vector con `type`, `operation`,
  `error_code`, `error_class` y `rejection_kind`.
- El verificador distingue `permission_denied_on_principal` (`229`, `262`) de `system_catalog_protection` (`259`).
- El s9 falla si el DML o el DDL no prueban denegacion de permisos del principal.
- Artefacto saneado actualizado en `Area_comun/artifacts/S9-TASK-0158-sqlserver-readonly-live.json`.

## Evidencia s9 viva
- SELECT permitido: `row_count=1`.
- DML contra tabla ordinaria, saltando clasificador cliente: `DELETE ordinary_table_zero_rows` rechazado por el
  servidor con `OperationalError` code `229`, `rejection_kind=permission_denied_on_principal`.
- DDL saltando clasificador cliente: `CREATE TABLE` rechazado por el servidor con `OperationalError` code `262`,
  `rejection_kind=permission_denied_on_principal`.
- El artefacto no contiene credenciales, nombres de dominio ni nombres reales de tablas.

## Gates
- `python -m py_compile connectors/sqlserver_readonly/connector.py connectors/sqlserver_readonly/s9_verify_live.py examples/connector_sqlserver_readonly_cases/run_connector_sqlserver_readonly_cases.py` PASS.
- `python examples/connector_sqlserver_readonly_cases/run_connector_sqlserver_readonly_cases.py` PASS.
- `python scripts/scan_encoding.py --root .` PASS.
- `python scripts/scan_domain_neutrality.py --root .` PASS.
- `python scripts/validate_collaboration_state.py --root .` PASS.
- Drift false, `up_to_seq=1260` antes del cierre de ledger.

## Notas
- `connectors/connectors.config.json` permanece `enabled:false`.
- `protocol.config.json` no fue tocado.
- No se commitearon `.env`, `connectors.runtime.json` ni credenciales.
