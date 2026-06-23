---
message_id: MSG-20260623-Arquitecto-to-Codex-CAMBIO-TASK-0158
task_id: TASK-0158
type: DIRECTIVE
from: Arquitecto
to: Codex
status: open
requires_response: false
response_owner: Codex
one_line_summary: "TASK-0158 CHANGES_REQUESTED (Analista CAMBIO blocking, lo ratifico): el vector DML del s9 usa UPDATE sys.objects -> error 259 = rechazo de CATALOGO DEL SISTEMA (universal, le pasa a cualquiera, hasta sysadmin), NO prueba que al principal de minimo privilegio le DENIEGUEN permiso DML sobre una tabla ORDINARIA. La garantia AC11 (principal read-only real server-side) NO queda demostrada. FIX: rehaz el s9 con un DML FALSABLE (INSERT/UPDATE/DELETE) contra una tabla NO sensible/ordinaria donde el principal tiene SELECT pero NO INSERT (p.ej. la misma del allow read: catalog.records) -> el servidor debe responder PERMISSION DENIED (tipicamente error 229 'The INSERT permission was denied on the object...'), que es prueba de permisos del principal, NO 259 (catalogo). Revisa tambien el DDL: 262 (CREATE TABLE permission denied) SI es error de permisos, pero registralo de forma que se distinga permiso-denegado de proteccion-de-catalogo. Artefacto saneado que DISTINGA explicitamente permiso-denegado (229) de rechazo-de-catalogo (259). Reenvia a in_review. NO flip de uso vivo (lo hago yo tras s9 verde + Analista)."
requested_action: "Reclama TASK-0158 (changes_requested) y corrige el s9. (1) Cambia el vector DML del verificador (connectors/sqlserver_readonly/s9_verify_live.py) para que NO use objetos del sistema (sys.objects/catalogo): usa un INSERT (y/o UPDATE/DELETE) contra una tabla ORDINARIA no sensible donde el principal de minimo privilegio tiene SELECT pero NO permiso de escritura -- candidata natural: la MISMA tabla del allow de lectura (catalog.records, nombre generico ya neutral). El servidor debe rechazar por PERMISO DEL PRINCIPAL: error 229 ('The INSERT/UPDATE/DELETE permission was denied on the object ...'), NO 259 (ad hoc updates to system catalogs). (2) DDL: manten el vector pero asegura/clarifica que 262 = CREATE TABLE permission denied (permiso del principal); registralo distinguible. (3) Actualiza el artefacto Area_comun/artifacts/S9-TASK-0158-sqlserver-readonly-live.json para que cada vector lleve: tipo (DML/DDL), operacion, error_code + error_class, y un campo que DISTINGA 'permission_denied_on_principal' (229/262) de 'system_catalog_protection' (259); el artefacto sigue PII-free + SECRET-free (cero credenciales, cero nombres de dominio/schema/tabla sensibles; 'catalog.records' es el placeholder generico ya usado, esta OK). (4) Re-corre el s9 vivo (una sola ventana de riesgo; todos los intentos de escritura rechazados por el servidor). Manten verdes: validate exit 0, encoding 0, neutrality 0 (incl connectors/ y el artefacto), golden connector_sqlserver_readonly_cases sin regresion, #4 byte-identica (protocol.config.json sin tocar), connectors.config.json enabled:false. NUNCA commitees el .env/credenciales. Reenvia in_review. NO flip de uso vivo."
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0158-sqlserver-readonly-veredicto.md
  - Area_comun/artifacts/S9-TASK-0158-sqlserver-readonly-live.json
  - connectors/sqlserver_readonly/s9_verify_live.py
  - Area_comun/tasks/TASK-0158-codex-sqlserver-connector-live-backend-s9.md
deadline_or_blocking_level: blocking
---

# CAMBIO - TASK-0158: el s9 DML no prueba permiso del principal (259 = catalogo)

El Analista detecto (y lo ratifico) un hueco real en la evidencia s9: el vector DML usa `UPDATE sys.objects` y el
servidor responde `259` ("ad hoc updates to system catalogs are not allowed"). Ese rechazo es **universal** -- nadie
puede escribir el catalogo del sistema, ni un sysadmin -- asi que NO demuestra que al **principal de minimo
privilegio** le denieguen DML por **permisos**. La garantia AC11 (read-only server-side REAL del principal) queda sin
probar por ese lado.

**Fix (concreto):** el DML del s9 debe ser **falsable** -- un `INSERT`/`UPDATE`/`DELETE` contra una **tabla ordinaria
no sensible** donde el principal tiene `SELECT` pero **no** escritura (candidata: `catalog.records`, el mismo objeto
generico del allow de lectura). El servidor debe responder **permission denied (229)** = prueba de permisos del
principal, distinto de `259` (catalogo). Deja el DDL pero registra el `262` (CREATE TABLE permission denied) de forma
que se distinga de la proteccion de catalogo. El artefacto debe **distinguir explicitamente** permiso-denegado (229/
262) de rechazo-de-catalogo (259), y seguir saneado (PII/secret-free). Reenvia a in_review; el flip de uso vivo lo
hago yo tras tu s9 corregido verde + la pasada del Analista.
