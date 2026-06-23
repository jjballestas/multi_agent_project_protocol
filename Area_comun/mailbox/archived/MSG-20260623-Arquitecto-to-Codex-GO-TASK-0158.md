---
message_id: MSG-20260623-Arquitecto-to-Codex-GO-TASK-0158
task_id: TASK-0158
type: DIRECTIVE
from: Arquitecto
to: Codex
status: archived
requires_response: false
response_owner: Codex
one_line_summary: "GO TASK-0158 (ready): connector SQL Server backend VIVO read-only + s9 SERVER-SIDE (DECISION-0041, AC11 SPEC-0083). El operador provisiono un SQL Server LOCAL con login de MINIMO PRIVILEGIO; credenciales en personal/operador/nova_sql_connector_readonly_s9.env (GITIGNORED, *.env). (1) instala driver real (pymssql pip preferido; documenta el comando), (2) open_live() conecta read-only leyendo el env (NUNCA hardcodear creds), clasificador classify_readonly_sql queda DELANTE, (3) pobla connectors.config.json (entry sqlserver_readonly enabled:false VERSIONADO; live solo via connectors.runtime.json gitignored, espejo AC58), (4) s9: SELECT permitido devuelve filas + intento de ESCRITURA rechazado POR EL SERVIDOR (>=1 DML + >=1 DDL saltando el clasificador cliente -> error de permisos server-side) -> prueba negativa registrada en Area_comun/artifacts/ PII-free y SECRET-free (solo vector+clase de error; CERO credenciales/nombres de dominio). OFF-by-default, #4 byte-identica (protocol.config.json sin tocar), validate con/sin secretos exit 0, neutralidad+encoding 0. NO flipees uso vivo (lo hace el Arquitecto tras s9 verde + Analista). Si el driver no instala -> blocked con la pregunta concreta."
requested_action: "Reclama TASK-0158 (ready) e implementa en el protocolo. (1) Instala un driver SQL Server (pymssql via pip preferido; si pyodbc, requiere ODBC Driver -> documenta cual y el comando). (2) connectors/sqlserver_readonly/connector.py::open_live() deja de lanzar el stub y abre conexion read-only leyendo host/port/db/usuario-minimo-privilegio/password/encrypt/trust del .env GITIGNORED (personal/operador/nova_sql_connector_readonly_s9.env); NUNCA hardcodear credenciales; el clasificador classify_readonly_sql (deny DML/DDL) permanece DELANTE del backend (no se alcanza el backend si deniega). (3) Pobla connectors.config.json (vacio) con el entry sqlserver_readonly enabled:false (off-by-default VERSIONADO); la activacion viva es SOLO por override runtime gitignored connectors.runtime.json (resuelve prefiriendo el .runtime.json si existe, espejo AC58). (4) s9 server-side (DECISION-0041): verificador (script/test, NO en CI del clon -- requiere DB+secret) que contra la DB real prueba (i) SELECT permitido -> >=1 fila; (ii) intento de ESCRITURA rechazado POR EL SERVIDOR: >=1 vector DML (INSERT) + >=1 DDL (CREATE TABLE) ejecutados SALTANDO el clasificador cliente para probar la denegacion server-side REAL -> el servidor responde error de permisos -> registra la PRUEBA NEGATIVA OBJETIVA en un artefacto Area_comun/artifacts/ PII-free y SECRET-free (vector + que el servidor rechazo + clase/codigo de error; CERO credenciales, CERO nombres de schema/tabla/dominio). Carry AC1-AC10 (clasificador deny-by-default, no escribe ledger/eventos, off-by-default). Manten verdes: validate con/sin secretos exit 0, scan_encoding 0, scan_domain_neutrality 0 (incluyendo connectors/ y el artefacto s9), golden connector_sqlserver_readonly_cases sin regresion; #4 byte-identica (protocol.config.json sin tocar, registro FUERA del config pinned). NO commitees el .env ni credenciales ni terminos de dominio. NO flipees el uso vivo. Si el driver no es instalable en el entorno -> blocked con la pregunta concreta (que driver/ODBC)."
context_refs:
  - Area_comun/tasks/TASK-0158-codex-sqlserver-connector-live-backend-s9.md
  - Area_comun/specs/SPEC-0083-connector-sqlserver-readonly.md
  - Area_comun/decisions/DECISION-0041-precondicion-acoplamiento-readonly.md
  - connectors/sqlserver_readonly/connector.py
  - connectors/framework/readonly.py
  - connectors.config.json
deadline_or_blocking_level: normal
---

# GO - TASK-0158: connector SQL Server backend vivo read-only + s9 server-side (AC11)

El operador dio el GO de uso vivo del connector y provisiono un SQL Server LOCAL con login de MINIMO PRIVILEGIO
read-only (DENY DML, NO DDL). Las credenciales estan en `personal/operador/nova_sql_connector_readonly_s9.env`
(GITIGNORED, ya cubierto por `*.env`; NUNCA lo commitees). TCP a host:port ya confirmado alcanzable.

Hoy `open_live()` es un stub que lanza `ConnectorDisabledError("live backend requires a later operator GO")`. Este
es ese GO: construye el backend vivo + corre el s9 server-side (DECISION-0041). Detalle completo en la tarea y en
SPEC-0083 AC11 (cierra AC8). Recuerda: el clasificador read-only va DELANTE (defensa en profundidad), pero el s9
prueba que **el SERVIDOR** deniega la escritura (no solo el cliente). Off-by-default; el flip del uso vivo lo hago
yo tras tu s9 verde + la pasada del Analista. Una sola ventana de riesgo: el s9 es la unica corrida con intentos de
escritura (todos rechazados por el servidor). maker=Codex / checker=Arquitecto + Analista.
