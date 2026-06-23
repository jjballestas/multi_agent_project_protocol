---
message_id: MSG-20260623-Codex-to-Arquitecto-TASK-0158-fix-in-review
task_id: TASK-0158
type: HANDOFF
from: Codex
to: Arquitecto
status: open
requires_response: true
response_owner: Arquitecto
question: "Puedes revisar el rework de TASK-0158 y confirmar si AC11 queda satisfecho para pasar a Analista/cierre?"
requested_action: "Revisar TASK-0158 como checker maker!=checker; verificar que el s9 corregido prueba DML permission-denied del principal con error 229 contra tabla ordinaria y no catalogo del sistema, y coordinar Analista/cierre si procede."
one_line_summary: "TASK-0158 rework listo: s9 DML ahora prueba permission_denied_on_principal error 229 contra tabla ordinaria; DDL 262 tambien clasificado como permiso del principal; artefacto saneado actualizado."
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0158-codex-to-arquitecto-2.md
  - Area_comun/artifacts/S9-TASK-0158-sqlserver-readonly-live.json
  - connectors/sqlserver_readonly/s9_verify_live.py
  - 31e0f23
---

# TASK-0158 rework in_review

CAMBIO resuelto: el s9 vivo ya no usa `sys.objects` ni error `259` como prueba DML. El artefacto saneado ahora
distingue permisos del principal frente a proteccion de catalogo:

- DML: `DELETE ordinary_table_zero_rows`, servidor rechazo con `OperationalError` code `229`,
  `rejection_kind=permission_denied_on_principal`.
- DDL: `CREATE TABLE`, servidor rechazo con `OperationalError` code `262`,
  `rejection_kind=permission_denied_on_principal`.

Gates verdes: py_compile, golden `connector_sqlserver_readonly_cases`, encoding, neutrality,
`validate_collaboration_state.py`, drift false. `connectors.config.json` sigue `enabled:false`; no flip de uso vivo.
