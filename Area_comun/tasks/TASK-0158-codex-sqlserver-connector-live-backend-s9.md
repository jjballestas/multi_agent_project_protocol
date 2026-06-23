---
task_id: TASK-0158
title: "Connector SQL Server read-only: backend VIVO (driver real, env gitignored) + verificacion s9 SERVER-SIDE (SELECT ok + escritura rechazada por el servidor, prueba negativa registrada) -- cumple AC8/AC11 SPEC-0083, DECISION-0041; off-by-default"
type: connector
status: ready
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0083
linked_decisions: [DECISION-0041, DECISION-0044]
created_at: 2026-06-23
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/multi_agent_project_protocol
file: Area_comun/tasks/TASK-0158-codex-sqlserver-connector-live-backend-s9.md
---

# TASK-0158 - Connector SQL Server: backend vivo read-only + s9 server-side (AC11)

> GO del operador (uso vivo del connector, DECISION-0041). El operador provisiono un SQL Server LOCAL con login de
> MINIMO PRIVILEGIO read-only. Credenciales en `personal/operador/nova_sql_connector_readonly_s9.env` (GITIGNORED,
> ya cubierto por `*.env`). maker=Codex / checker=Arquitecto + PASADA DEL ANALISTA (PII/secret/egress). NO commitees
> credenciales ni terminos de dominio. NO flipees el uso vivo (el flip del runtime lo hace el Arquitecto tras s9 verde + Analista).

## Insumo (env gitignored, NO commitear)
- `SQLSERVER_HOST` (localhost), `SQLSERVER_PORT` (1433), `SQLSERVER_DATABASE`, `SQLSERVER_USER` (minimo privilegio),
  `SQLSERVER_PASSWORD`, `SQLSERVER_ENCRYPT`, `SQLSERVER_TRUST_SERVER_CERTIFICATE`, `SQLSERVER_READONLY=true`.
- TCP a host:port ya confirmado alcanzable. Profile del login: `...DENY_DML_NO_DDL_GRANTS` (el SERVIDOR deniega escritura).

## Alcance (AC11, cierra AC8)
1. **Driver real:** instala un driver de SQL Server (preferencia `pymssql` por pip; si usas `pyodbc` requiere ODBC
   Driver instalado -- documenta cual). Deja constancia del comando de instalacion.
2. **Backend vivo:** `connectors/sqlserver_readonly/connector.py::open_live()` deja de lanzar el stub y abre conexion
   read-only leyendo los parametros del `.env` gitignored (NUNCA hardcodear credenciales). El clasificador
   `classify_readonly_sql` (deny DML/DDL) permanece DELANTE del backend (defensa en profundidad; el backend NO se
   alcanza si el clasificador deniega). Conexion con `ApplicationIntent=ReadOnly`/read-only segun el driver.
3. **Registro:** pobla `connectors.config.json` (esta vacio) con el entry `sqlserver_readonly` (`enabled:false`
   VERSIONADO = off-by-default); el uso vivo se activa SOLO por override runtime gitignored `connectors.runtime.json`
   (espejo del patron AC58: la resolucion prefiere el `.runtime.json` si existe).
4. **s9 server-side (DECISION-0041):** un verificador (script/test, NO en el CI del clon -- requiere DB+secret) que
   contra la DB real prueba: (i) un `SELECT` permitido devuelve >=1 fila; (ii) un intento de ESCRITURA lo rechaza EL
   SERVIDOR -- >=1 vector DML (p.ej. `INSERT`) + >=1 DDL (p.ej. `CREATE TABLE`) ejecutados SALTANDO el clasificador
   cliente (para probar la denegacion server-side real, no la del cliente) -> el servidor responde error de permisos.
   Registra la **prueba negativa objetiva** en un artefacto `Area_comun/artifacts/` PII-free y secret-free (sin
   credenciales, sin nombres de schema/tabla/dominio; solo: vector, que el servidor rechazo, codigo/clase de error).

## DoD
- AC11 verde: SELECT vivo ok + rechazo SERVER-SIDE de DML y DDL registrado (prueba negativa). Carry AC1-AC10
  (clasificador deny-by-default, no escribe ledger/eventos AC4/AC7, off-by-default AC5, neutralidad AC9).
- OFF-by-default: `connectors.config.json` versionado `enabled:false`; sin `connectors.runtime.json` -> fail-closed
  (sin conexion). #4 byte-identica (`protocol.config.json` sin tocar; el registro vive FUERA del config pinned).
- `validate_collaboration_state.py` exit 0 con y SIN secretos; `scan_encoding.py` 0; `scan_domain_neutrality.py` 0
  incluyendo `connectors/` y el artefacto s9 (CERO termino de dominio en lo commiteado). El golden de fixtures
  `connector_sqlserver_readonly_cases` sigue verde (sin regresion); el s9 vivo es SMOKE documentado, NO en CI del clon.
- Reproducido por el checker (Arquitecto) + PASADA DEL ANALISTA antes de cerrar. NO flip de uso vivo (lo hace el Arquitecto).

## Notas
- NUNCA commitear el `.env`, credenciales, ni nombres de dominio (budget/treasury/etc.); esos viven solo en el env
  gitignored y en el SERVIDOR. El artefacto s9 se sanea (vectores + clase de error, nada mas).
- Si el driver/instalacion no es factible en el entorno, deja `blocked` con la pregunta concreta (que driver/ODBC).
- Una sola ventana de riesgo: el s9 es la unica corrida que intenta escrituras (todas rechazadas por el servidor).
