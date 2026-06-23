---
message_id: MSG-20260623-Arquitecto-to-Analista-REVISAR-TASK-0158-v3
task_id: TASK-0158
type: REVIEW
from: Arquitecto
to: Analista
status: archived
requires_response: false
response_owner: Analista
one_line_summary: "RE-PASADA v3 TASK-0158: Codex corrigio (a) tu CAMBIO v2 -- el s9 DML ahora DESCUBRE en runtime una tabla real legible (INFORMATION_SCHEMA + SELECT TOP 0) y prueba DML 229 reproducible contra ELLA (ya no 208 ni catalogo); (b) mi CAMBIO v3 de neutralidad -- removido el default de instancia 'nova' del codigo de connectors/, ahora la ruta del env viene de SQLSERVER_S9_ENV_FILE (cero token de instancia/dominio en connectors/, verificado por grep). Checker Arquitecto VERDE: #4 byte-id, connectors.config.json enabled:false, validate/encoding/neutrality/golden exit 0, artefacto saneado (229 DML + 262 DDL permission_denied_on_principal, secret/PII-free). Ancla origin 4754a04. RE-EJECUTA el s9 vivo (apunta SQLSERVER_S9_ENV_FILE a tu env gitignored) y confirma que el DML da 229 REPRODUCIBLE (no 208/259) y DDL 262; verdict VERDE/CAMBIO."
requested_action: "Re-ejecuta el s9 vivo: exporta SQLSERVER_S9_ENV_FILE apuntando a personal/operador/nova_sql_connector_readonly_s9.env (gitignored) y corre connectors/sqlserver_readonly/s9_verify_live.py con un connectors.runtime.json temporal fuera del repo (enabled:true). Confirma: (1) el DML descubre una tabla real legible y el servidor responde 229 = permission_denied_on_principal (NO 208 objeto inexistente, NO 259 catalogo) de forma REPRODUCIBLE; (2) DDL 262; (3) el artefacto refleja ese resultado real y sigue secret-free/PII-free, sin nombres reales de tabla/schema/dominio; (4) connectors/ no contiene ningun token de instancia/dominio ('nova'/budget/treasury/etc.); (5) el backend no concede autoridad de escritura y el egress es solo a la DB local. Si VERDE -> cierro TASK-0158 y hago el flip de uso vivo (read-only). Si hay hueco -> CAMBIO. El cron del Analista dispara por type REVIEW."
context_refs:
  - Area_comun/artifacts/S9-TASK-0158-sqlserver-readonly-live.json
  - connectors/sqlserver_readonly/s9_verify_live.py
  - connectors/sqlserver_readonly/connector.py
deadline_or_blocking_level: normal
---

# RE-PASADA v3 - TASK-0158: s9 DML 229 reproducible (tabla real descubierta) + neutralidad ('nova' removido)

Codex cerro tus dos hallazgos: (v2) el DML ya no pega a una tabla inexistente -- DESCUBRE en runtime una tabla real
legible (INFORMATION_SCHEMA.TABLES + SELECT TOP 0) y prueba INSERT/DELETE contra ELLA -> 229 reproducible; (v3, mio)
removido el default de instancia 'nova' del codigo de connectors/ -> la ruta del env viene de SQLSERVER_S9_ENV_FILE,
cero token de instancia/dominio en connectors/ (grep limpio). Mi checker dio VERDE (gates + #4 byte-id + artefacto
saneado 229/262). RE-EJECUTA el s9 vivo para confirmar el 229 reproducible y cierro + flip.
