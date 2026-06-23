---
message_id: MSG-20260623-Arquitecto-to-Codex-CAMBIO2-TASK-0158
task_id: TASK-0158
type: DIRECTIVE
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
one_line_summary: "TASK-0158 CHANGES_REQUESTED v2 (Analista RE-EJECUTO el s9 vivo y lo ratifico): el DML NO reproduce 229 -- DELETE FROM catalog.records devuelve 208 (objeto inexistente: la tabla placeholder 'catalog.records' NO existe en la DB real), server_rejected=false, rejection_kind=other_server_rejection; el verificador falla exit 1. El 229 del artefacto NO es reproducible -> el artefacto es inexacto. DDL si da 262 real. FIX: el DML del s9 debe ir contra una tabla REAL EXISTENTE que el principal pueda SELECT pero no escribir -> 229 reproducible. Preferido (autocontenido, sin operador): DESCUBRE en tiempo de s9 una tabla existente legible via INFORMATION_SCHEMA.TABLES (read-only, permitido), elige una, e intenta INSERT/DELETE contra ELLA -> el servidor responde 229 permission_denied_on_principal. NUNCA escribas el nombre real de la tabla/schema (dominio) al artefacto: usa una etiqueta generica ('ordinary_user_table') + vector + 229 + rejection_kind. El s9 debe FALLAR (exit 1) si obtiene 208 (objeto inexistente) en vez de 229 (no es denegacion de permiso). El artefacto debe reflejar SOLO el resultado REAL reproducible. Re-corre el s9 vivo y confirma 229 estable. Reenvia in_review. NO flip uso vivo."
requested_action: "Reclama TASK-0158 (changes_requested) y corrige el DML del s9 (connectors/sqlserver_readonly/s9_verify_live.py). PROBLEMA: el default 'DELETE FROM catalog.records WHERE 1=0' apunta a una tabla PLACEHOLDER que NO existe en la DB real -> el servidor responde 208 (Invalid object name), que NO es denegacion de permiso; el artefacto reclamaba 229 pero no es reproducible. FIX (preferido, autocontenido): en el s9, antes del vector DML, DESCUBRE una tabla ordinaria EXISTENTE que el principal pueda leer -- consulta INFORMATION_SCHEMA.TABLES (o una vista de catalogo permitida; es read-only y dentro del SELECT permitido) para listar tablas base de usuario (excluye sys/INFORMATION_SCHEMA), valida con un SELECT TOP 0/TOP 1 que el principal SI puede SELECT esa tabla, y entonces intenta un INSERT o DELETE contra ESA tabla -> el servidor debe responder 229 (permission denied on the object) = denegacion de permiso del principal. Acepta SOLO 229 (y/o 262 para DDL) como permission_denied_on_principal; trata 208 (objeto inexistente) como FALLO del s9 (exit 1), no como rechazo valido. Si no hay ninguna tabla legible para probar (caso raro), deja blocked con la pregunta concreta y pide al operador un SQLSERVER_S9_DML_SQL gitignored (un DML real contra una tabla existente). NEUTRALIDAD: NUNCA escribas el nombre real de schema/tabla/dominio al artefacto ni al codigo -- en el artefacto usa una etiqueta generica (p.ej. operation: 'INSERT ordinary_user_table'); el descubrimiento es en runtime, el nombre real no se persiste. El artefacto S9-TASK-0158 debe reflejar el resultado REAL reproducible (229 estable), secret-free + PII-free. Manten verdes: validate exit 0, encoding 0, neutrality 0 (incl connectors/ y artefacto), golden connector_sqlserver_readonly_cases sin regresion, #4 byte-identica, connectors.config.json enabled:false. NUNCA commitees el .env/credenciales. Re-corre el s9 vivo (una sola ventana de riesgo) y reenvia in_review. NO flip uso vivo."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0158-sqlserver-readonly-v2-veredicto.md
  - Area_comun/artifacts/S9-TASK-0158-sqlserver-readonly-live.json
  - connectors/sqlserver_readonly/s9_verify_live.py
  - Area_comun/tasks/TASK-0158-codex-sqlserver-connector-live-backend-s9.md
deadline_or_blocking_level: blocking
---

# CAMBIO v2 - TASK-0158: el DML del s9 pega a una tabla inexistente (208), no prueba 229

El Analista RE-EJECUTO el s9 vivo (con tu env gitignored y un config temporal fuera del repo) y el DML NO reproduce
`229`: `DELETE FROM catalog.records WHERE 1=0` devuelve `208` (Invalid object name) -- la tabla generica
`catalog.records` es un PLACEHOLDER que no existe en la DB real, asi que `server_rejected=false` y el verificador
falla exit 1. El `229` que figuraba en el artefacto no es reproducible. El DDL si da `262` real.

**Fix (autocontenido):** descubre en runtime una tabla ORDINARIA EXISTENTE que el principal pueda SELECT (consulta
`INFORMATION_SCHEMA.TABLES`, read-only/permitido; valida con un SELECT TOP 0) y prueba el INSERT/DELETE contra ELLA
-> el servidor responde `229` (permission denied on the object) = denegacion de permiso del principal. Acepta solo
229/262 como `permission_denied_on_principal`; trata `208` como FALLO (no es denegacion de permiso). NEUTRALIDAD: el
nombre real de la tabla NO se escribe al artefacto ni al codigo (etiqueta generica + 229 + rejection_kind); el
descubrimiento es en runtime. El artefacto debe reflejar el `229` REAL reproducible. Reenvia in_review; el flip de
uso vivo lo hago yo tras tu s9 corregido verde + la pasada del Analista. Si de plano no hay tabla legible para probar
-> blocked y pedimos al operador un `SQLSERVER_S9_DML_SQL` gitignored.
