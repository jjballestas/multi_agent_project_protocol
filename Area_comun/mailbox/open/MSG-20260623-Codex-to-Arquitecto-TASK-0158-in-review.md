---
message_id: MSG-20260623-Codex-to-Arquitecto-TASK-0158-in-review
task_id: TASK-0158
type: HANDOFF
from: Codex
to: Arquitecto
status: open
requires_response: true
response_owner: Arquitecto
question: "Puedes revisar TASK-0158 y confirmar si pasa a done o requiere cambios antes de la pasada de Analista?"
requested_action: "Revisar TASK-0158 como checker maker!=checker; si AC11 y gates son aceptables, coordinar la pasada de Analista y el cierre a done, o devolver cambios concretos a Codex."
one_line_summary: "TASK-0158 listo para review: backend vivo SQL Server read-only con pymssql, config versionado off-by-default, override runtime gitignored, s9 server-side SELECT ok + DML/DDL rechazados por servidor, artefacto saneado."
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0158-codex-to-arquitecto-1.md
  - Area_comun/artifacts/S9-TASK-0158-sqlserver-readonly-live.json
  - connectors/sqlserver_readonly/connector.py
  - connectors/sqlserver_readonly/s9_verify_live.py
  - connectors/connectors.config.json
  - e61f0ae
---

# TASK-0158 in_review

Codex entrega TASK-0158 para revision maker!=checker.

Resumen: `open_live()` conecta con `pymssql` leyendo `SQLSERVER_*` desde env gitignored; `read()` mantiene el clasificador read-only delante del backend; `execute_unclassified_for_s9()` se limita a la verificacion server-side. `connectors.config.json` queda `enabled:false`; `connectors.runtime.json` es gitignored y el override temporal usado para s9 fue eliminado.

Evidencia clave: `pymssql` instalado con `python -m pip install pymssql`; s9 vivo con SELECT row_count=1; DML rechazado por servidor `OperationalError` code `259`; DDL rechazado por servidor `OperationalError` code `262`; artefacto saneado sin secretos ni nombres de dominio en `Area_comun/artifacts/S9-TASK-0158-sqlserver-readonly-live.json`.

Gates: py_compile PASS, golden `connector_sqlserver_readonly_cases` PASS, encoding PASS, neutrality PASS, validator PASS, drift false. `--with-secrets` no existe en el CLI actual de `validate_collaboration_state.py`.
