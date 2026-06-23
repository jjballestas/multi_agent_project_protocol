# Veredicto Analista - TASK-0158 v2

Firma: Analista
Fecha: 2026-06-23

## Veredicto

CAMBIO-REQUERIDO.

Ancla canonica revisada:
- Protocolo HEAD citado por la instruccion: `90eea652b4a415824c1a5ceadeb22c09019e5f7b` (`review(TASK-0158): re-pasada al Analista -- s9 DML ya prueba permiso del principal (229), no catalogo`).
- Rework maker: `31e0f23` (`fix(connectors): prove SQL Server DML permission denial`).
- Handoff maker: `Area_comun/handoffs/HANDOFF-TASK-0158-codex-to-arquitecto-2.md`, `commit: 31e0f23`.
- Producto `D:/Agentes/Zeus/Zeus-protocol`: la instruccion no cita un commit nuevo de producto para TASK-0158; clone limpio ejecutado sobre HEAD local `2afc9449ae92e6652ac8ebc1867a89bd8e78d77b`.

Defecto bloqueante: al re-ejecutar el s9 vivo con los secretos gitignored del operador y un config temporal que solo habilita `sqlserver_readonly`, el DML no fue rechazado por permisos del principal. El vector default `DELETE FROM catalog.records WHERE 1 = 0` devolvio `ProgrammingError` codigo `208` (objeto inexistente), con `server_rejected=false` y `rejection_kind=other_server_rejection`. Por tanto, el artefacto commiteado que declara `error_code=229` no es reproducible contra el env vivo actual y no prueba la garantia AC11 de minimo privilegio DML.

Recomendacion de cierre: CAMBIO-REQUERIDO. No cerrar TASK-0158 ni flippear uso vivo. Re-ejecutar s9 contra una tabla/probe ordinaria existente y no sensible, o crear una probe controlada por el operador, hasta obtener una denegacion reproducible de permisos del principal para DML. El artefacto saneado debe conservar evidencia no sensible suficiente para distinguir `229 permission_denied_on_principal` de `208 invalid object` y de `259 system_catalog_protection`.

## Reproduccion y gates

| Prueba | Ancla | Resultado |
|---|---:|---|
| `git fetch origin; git status --short` | live repo | exit 0; cambios ajenos no tocados en `.claude/settings.json`, `personal/Arquitecto/*`, `personal/Analista/MEMORY.md`, `personal/operador/*.pdf` |
| `python scripts/validate_collaboration_state.py` | live repo con secretos locales disponibles | exit 0 |
| `python scripts/validate_collaboration_state.py` | clone limpio protocolo `90eea65` sin secretos | exit 0 |
| `python scripts/scan_domain_neutrality.py --root .` | clone limpio protocolo `90eea65` | exit 0 |
| `python scripts/scan_encoding.py --root .` | clone limpio protocolo `90eea65` | exit 0 |
| `python examples/connector_sqlserver_readonly_cases/run_connector_sqlserver_readonly_cases.py` | clone limpio protocolo `90eea65` | exit 0; 8/8 |
| `python -m py_compile connectors/sqlserver_readonly/connector.py connectors/sqlserver_readonly/s9_verify_live.py examples/connector_sqlserver_readonly_cases/run_connector_sqlserver_readonly_cases.py` | clone limpio protocolo `90eea65` | exit 0 |
| `git diff -- protocol.config.json runtime/state/snapshot.json runtime/state/events.jsonl` | live repo antes de mi entrega | exit 0; #4 byte-identica respecto al working tree revisado |
| `npm test` | clone limpio producto `2afc9449ae92e6652ac8ebc1867a89bd8e78d77b` | exit 0; 50/50 |
| `python connectors/sqlserver_readonly/s9_verify_live.py --env personal/operador/nova_sql_connector_readonly_s9.env --config C:/tmp/analista-s9-connectors.runtime.json --artifact C:/tmp/analista-S9-TASK-0158-rerun.json` | live repo, config temporal fuera del repo con `sqlserver_readonly.enabled=true` | exit 1; `s9 write vectors were not rejected by the server` |
| Diagnostico propio con `run_vector()` contra la misma conexion viva | live repo | SELECT row_count=1; DML -> code `208`, `server_rejected=false`, `rejection_kind=other_server_rejection`; DDL -> code `262`, `server_rejected=true`, `permission_denied_on_principal` |
| Payloads propios del clasificador read-only | live repo | exit 0; INSERT/UPDATE/DELETE/MERGE/CREATE/ALTER/DROP/TRUNCATE/EXEC/multistatement/objeto no allowlisted denegados antes del backend; SELECT permitido |
| Payloads propios del clasificador s9 | live repo | exit 0; `229`/`262` -> permission_denied_on_principal, `259` -> system_catalog_protection, `208` no cuenta como rechazo de permisos |

## Tabla adversarial por vector

| Vector / AC | Resultado | Evidencia falsable |
|---|---|---|
| Artefacto s9 secret-free | PASA | `Area_comun/artifacts/S9-TASK-0158-sqlserver-readonly-live.json` no contiene host, usuario, password, database ni env keys. |
| Artefacto s9 PII/domain-free | PASA | El artefacto usa nombres genericos y los scans de neutralidad/encoding salen exit 0. |
| Off-by-default versionado | PASA | `connectors/connectors.config.json` mantiene `sqlserver_readonly.enabled=false`; para el rerun use un config temporal en `C:/tmp`, no versionado. |
| Clasificador delante del backend para `read()` | PASA | Familia DML/DDL/EXEC/multistatement/objeto no allowlisted denegada antes del backend; SELECT allowlisted permitido. |
| Backend sin autoridad de ledger/eventlog | PASA | Golden AC4 confirma huella de estado sin cambios y ausencia de imports de writers runtime desde `connectors/**/*.py`. |
| Egress de connector | PASA con residual | La unica red del backend revisado es `pymssql.connect(...)` hacia `SQLSERVER_HOST`/`SQLSERVER_PORT`; residual: el codigo no fuerza loopback, depende del GO/env del operador. |
| DDL server-side | PASA | Rerun vivo devuelve `262` y `permission_denied_on_principal`. |
| DML sobre tabla ordinaria | SLIPS | Rerun vivo no reproduce `229`; devuelve `208` objeto inexistente para `DELETE FROM catalog.records WHERE 1 = 0`. El script falla exit 1 antes de escribir artefacto. |
| Separacion `229/262` vs `259` | PASA | `rejection_kind()` separa `229/262` de `259`; el problema es que el DML vivo actual no llega a `229`. |
| Evidencia s9 reproducible | SLIPS | El artefacto commiteado dice DML `229`, pero el mismo codigo/env vivo actual produce DML `208`; falta una probe ordinaria existente o SQL s9 override gitignored que haga reproducible la evidencia. |

## Residuales declarados

- El rerun vivo uso el env gitignored existente sin commitear ni imprimir credenciales. El config habilitado usado para la prueba quedo fuera del repo en `C:/tmp/analista-s9-connectors.runtime.json`.
- El DML `DELETE ... WHERE 1 = 0` es de cero filas; si el objeto existiera, seguiria siendo una prueba aceptable de permiso DML porque el servidor debe autorizar DELETE aunque no afecte filas. El bloqueo actual es que el objeto no existe en el env vivo revisado.
- AC11 no exige sandbox de red; exige minimo privilegio del principal. El loopback/local-only queda como condicion operacional del GO, no como garantia del codigo.
