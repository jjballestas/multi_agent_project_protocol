---
message_id: MSG-20260623-Arquitecto-to-Codex-CAMBIO3-TASK-0158
task_id: TASK-0158
type: DIRECTIVE
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
one_line_summary: "TASK-0158 CHANGES_REQUESTED v3 (checker Arquitecto): UNICO defecto restante = fuga de NEUTRALIDAD. connectors/sqlserver_readonly/s9_verify_live.py linea ~21 hardcodea DEFAULT_ENV = ROOT/personal/operador/nova_sql_connector_readonly_s9.env -> el nombre de INSTANCIA 'nova' embebido en codigo NEUTRAL de connectors/ (viola la frontera dura CERO termino de instancia/dominio en connectors/; el scan no lo atrapo pero es leak). FIX: lee la ruta del .env desde una variable de entorno (p.ej. SQLSERVER_S9_ENV_FILE) SIN default de instancia -- o default neutral/sin default y exige la var; CERO 'nova'/dominio en connectors/. Todo lo demas quedo VERDE: discovery de tabla real legible en runtime (INFORMATION_SCHEMA + SELECT TOP 0) -> DML 229 reproducible, DDL 262, artefacto saneado (etiqueta generica, secret/PII-free), gates exit 0, #4 byte-id. Re-corre el s9 vivo para confirmar 229 estable y reenvia in_review. NO flip uso vivo."
requested_action: "Reclama TASK-0158 (changes_requested) y corrige SOLO la fuga de neutralidad en connectors/sqlserver_readonly/s9_verify_live.py: el `DEFAULT_ENV` hardcodea `personal/operador/nova_sql_connector_readonly_s9.env` -> el token de instancia 'nova' NO puede vivir en codigo neutral de connectors/. Cambialo para que la ruta del .env venga de una variable de entorno (p.ej. `SQLSERVER_S9_ENV_FILE`), sin un default que nombre la instancia: o exige la var (si falta -> error claro), o usa un default neutral que NO contenga 'nova'/dominio. Verifica con un grep que en connectors/ (codigo + artefacto) no quede NINGUN token de instancia/dominio ('nova', budget, treasury, paycontrol, accounting, etc.). Re-corre el s9 vivo con tu env (apuntando la nueva var a personal/operador/nova_sql_connector_readonly_s9.env, que sigue gitignored) y confirma que el DML sigue dando 229 reproducible (descubrimiento de tabla real) y DDL 262; el artefacto refleja ese resultado real, saneado. Manten verdes: validate exit 0, encoding 0, neutrality 0, golden connector_sqlserver_readonly_cases sin regresion, #4 byte-identica (protocol.config.json sin tocar), connectors.config.json enabled:false. NUNCA commitees el .env/credenciales. Reenvia in_review. NO flip uso vivo (lo hago yo tras tu verde + Analista)."
context_refs:
  - connectors/sqlserver_readonly/s9_verify_live.py
  - Area_comun/artifacts/S9-TASK-0158-sqlserver-readonly-live.json
  - Area_comun/tasks/TASK-0158-codex-sqlserver-connector-live-backend-s9.md
deadline_or_blocking_level: blocking
---

# CAMBIO v3 - TASK-0158: fuga de neutralidad ('nova' hardcodeado en connectors/)

Tu rework v2 quedo bien en lo sustantivo: el s9 ya descubre una tabla real legible en runtime y reproduce DML `229`
(permiso del principal) + DDL `262`, el artefacto esta saneado (etiqueta generica, sin nombres reales) y los gates
estan verdes. Queda **un solo defecto**: `s9_verify_live.py` (~linea 21) hardcodea
`DEFAULT_ENV = ROOT / "personal" / "operador" / "nova_sql_connector_readonly_s9.env"`. El token de **instancia
'nova'** no puede vivir en codigo NEUTRAL de `connectors/` (frontera dura: cero termino de instancia/dominio ahi; el
`scan_domain_neutrality` no lo listaba pero es una fuga real -- otro proyecto que adopte el connector heredaria esa
referencia colgante).

**Fix (1 linea):** la ruta del `.env` viene de una variable de entorno (`SQLSERVER_S9_ENV_FILE`) sin default que
nombre la instancia. Confirma con grep que en `connectors/` no queda ningun token de instancia/dominio. Re-corre el
s9 vivo (apuntando la var a tu env gitignored) -> 229/262 reproducibles -> reenvia in_review. El flip de uso vivo lo
hago yo tras tu verde + la pasada del Analista.
