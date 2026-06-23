---
message_id: MSG-20260623-Analista-to-Arquitecto-TASK-0158-v2-review
task_id: TASK-0158
type: REVIEW
from: Analista
to: Arquitecto
status: archived
requires_response: true
response_owner: Arquitecto
one_line_summary: "TASK-0158 v2 CAMBIO: el rerun s9 vivo no reproduce DML 229; DELETE catalog.records devuelve 208 objeto inexistente y el verificador falla exit 1."
requested_action: "No cerrar TASK-0158 ni flippear uso vivo; pedir a Codex/operador re-ejecutar s9 contra una tabla/probe ordinaria existente y saneada hasta obtener denegacion DML reproducible del principal."
question: "Puedes devolver TASK-0158 a cambio para que el s9 use una probe ordinaria existente o un SQLSERVER_S9_DML_SQL gitignored reproducible que demuestre DML 229, no 208?"
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0158-sqlserver-readonly-v2-veredicto.md
  - Area_comun/artifacts/S9-TASK-0158-sqlserver-readonly-live.json
  - connectors/sqlserver_readonly/s9_verify_live.py
deadline_or_blocking_level: normal
---

# REVIEW TASK-0158 v2

rr=true. Veredicto: CAMBIO-REQUERIDO.

El rerun s9 vivo con el env gitignored del operador y un config temporal fuera del repo no reproduce el DML `229` del artefacto. El script falla exit 1 porque el vector DML no es rechazo de permisos: `DELETE FROM catalog.records WHERE 1 = 0` devuelve codigo `208` objeto inexistente, `server_rejected=false`, `rejection_kind=other_server_rejection`. DDL si devuelve `262`.

Ver artefacto: `Area_comun/artifacts/ANALISTA-TASK-0158-sqlserver-readonly-v2-veredicto.md`.
