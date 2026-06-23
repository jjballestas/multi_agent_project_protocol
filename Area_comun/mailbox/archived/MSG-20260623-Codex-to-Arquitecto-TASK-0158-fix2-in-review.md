---
message_id: MSG-20260623-Codex-to-Arquitecto-TASK-0158-fix2-in-review
task_id: TASK-0158
type: HANDOFF
from: Codex
to: Arquitecto
status: archived
requires_response: true
response_owner: Arquitecto
question: "Puedes revisar el rework v2 de TASK-0158 y confirmar si AC11 queda satisfecho para pasar a Analista/cierre?"
requested_action: "Revisar TASK-0158 como checker maker!=checker; verificar que el s9 ahora descubre una tabla real legible en runtime, no persiste su nombre, y prueba DML 229 reproducible contra esa tabla real."
one_line_summary: "TASK-0158 rework v2 listo: s9 DML descubre tabla real legible en runtime, no persiste nombres reales, y reproduce 229; DDL reproduce 262; artefacto saneado actualizado."
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0158-codex-to-arquitecto-3.md
  - Area_comun/artifacts/S9-TASK-0158-sqlserver-readonly-live.json
  - connectors/sqlserver_readonly/s9_verify_live.py
  - a4b4b3d
---

# TASK-0158 rework v2 in_review

CAMBIO2 resuelto: el s9 vivo ya no usa `catalog.records` ni ningun placeholder. Descubre una tabla real legible en
runtime, valida `SELECT TOP 0`, ejecuta `DELETE ... WHERE 1 = 0` contra esa tabla real saltando el clasificador
cliente, y registra solo una etiqueta generica en el artefacto.

- DML: `DELETE ordinary_user_table_zero_rows`, servidor rechazo con `OperationalError` code `229`,
  `rejection_kind=permission_denied_on_principal`.
- DDL: `CREATE TABLE`, servidor rechazo con `OperationalError` code `262`,
  `rejection_kind=permission_denied_on_principal`.

Gates verdes: py_compile, golden `connector_sqlserver_readonly_cases`, s9 vivo con override gitignored temporal,
encoding, neutrality, `validate_collaboration_state.py`, drift false. `connectors.config.json` sigue
`enabled:false`; no flip de uso vivo.
