# Veredicto Analista - TASK-0158

Firma: Analista
Fecha: 2026-06-23

## Veredicto

CAMBIO-REQUERIDO.

Ancla canonica revisada:
- Protocolo citado por la instruccion: `61dc165` (`coord(TASK-0158): deliver SQL Server connector s9`).
- Handoff maker: `Area_comun/handoffs/HANDOFF-TASK-0158-codex-to-arquitecto-1.md`, `implementation_commit: e61f0ae`.
- Producto `D:/Agentes/Zeus/Zeus-protocol`: la instruccion de TASK-0158 no cita commit de producto; clone limpio ejecutado solo como control externo no-gateante sobre HEAD local `2afc944`.

Defecto bloqueante: el s9 DML vivo no prueba de forma falsable que el principal SQL Server sea read-only. El verificador por defecto usa `UPDATE sys.objects SET name = name WHERE 1 = 0`; el artefacto registra error `259`, que corresponde a rechazo server-side de actualizacion de catalogo del sistema, no a una denegacion de permisos sobre una tabla writable/probe creada para s9. Esto prueba que el servidor rechazo ese vector, pero no prueba la garantia pedida por AC11/DECISION-0041: que el login de minimo privilegio no tiene autoridad de escritura DML. Ademas, el artefacto saneado no conserva una huella no sensible del SQL usado, por lo que no permite distinguir una denegacion de permisos real de un rechazo por objeto protegido.

Recomendacion de cierre: CAMBIO-REQUERIDO. No cerrar ni flippear uso vivo hasta re-ejecutar s9 con un DML de permisos falsable, por ejemplo `INSERT`/`UPDATE` sobre una tabla/probe no sensible creada para la prueba y con nombre saneado u opacado en el artefacto. El artefacto debe conservar evidencia no sensible suficiente para distinguir `permission denied`/permiso DML denegado de rechazos por catalogo del sistema.

## Reproduccion y gates

| Prueba | Ancla | Resultado |
|---|---:|---|
| `git fetch origin` + `git status --short` | live repo | exit 0; cambios ajenos no tocados: `.claude/settings.json`, drafts en `personal/Arquitecto/`, PDF en `personal/operador/` |
| `python scripts/validate_collaboration_state.py` | live repo | exit 0 |
| `python examples/connector_sqlserver_readonly_cases/run_connector_sqlserver_readonly_cases.py` | clone limpio protocolo `61dc165` | exit 0; 8/8 |
| `python scripts/validate_collaboration_state.py` | clone limpio protocolo `61dc165` sin secretos | exit 0 |
| `python scripts/scan_domain_neutrality.py --root .` | clone limpio protocolo `61dc165` | exit 0 |
| `python scripts/scan_encoding.py --root .` | clone limpio protocolo `61dc165` | exit 0 |
| Drift `runtime.protocol_replay.protocol_state_drift(Path("."))` | clone limpio protocolo `61dc165` | `has_drift=false`, `up_to_seq=1255` |
| `npm test` | clone limpio producto HEAD local `2afc944` | exit 0; 50/50; no commit de producto fue citado por TASK-0158 |

## Tabla adversarial por vector

| Vector / AC | Resultado | Evidencia falsable |
|---|---|---|
| Artefacto s9 secret-free | PASA | `Area_comun/artifacts/S9-TASK-0158-sqlserver-readonly-live.json` contiene driver, timestamp, row_count, vector, clase/codigo de error y flags; no contiene host, usuario, password, database, schema, tabla ni SQL literal. |
| Artefacto s9 PII/domain-free | PASA | El artefacto no contiene nombres de schema/tabla/dominio ni texto de negocio; `scan_domain_neutrality.py` exit 0 en clone limpio. |
| Credenciales fuera del repo | PASA | `connector.py` lee `SQLSERVER_*` desde env o env file; no hay credenciales hardcodeadas en los archivos revisados. |
| Off-by-default versionado | PASA | `connectors/connectors.config.json` registra `sqlserver_readonly` con `enabled:false`; sin runtime override, `open_live()` falla con `live connector disabled`. |
| Clasificador delante del backend para `read()` | PASA | Payloads propios: `INSERT`, `UPDATE`, `DELETE`, `MERGE`, `CREATE`, `ALTER`, `DROP`, `TRUNCATE`, `EXEC`, multi-statement y objeto no allowlisted devuelven `ReadOnlyDeniedError` y no llaman al backend; `SELECT` allowlisted si llama al backend. |
| Backend no escribe ledger/eventos | PASA | Busqueda estatica en `connectors/**/*.py`: no referencias a `submit_intent`, `eventlog`, `PROJECT_STATE`, `TASK_INDEX`, `CLAIMS` ni `Area_comun/state`; solo `s9_verify_live.py` escribe el artefacto saneado. |
| Egress de connector | PASA con residual | La unica llamada de red observada es `pymssql.connect(...)` en `open_live_connection`, con host/port desde `SQLSERVER_HOST`/`SQLSERVER_PORT`. Residual: el codigo no fuerza loopback; la garantia de "DB local" depende del env/operator GO. |
| DDL server-side | PASA | Artefacto registra `DDL`, `server_rejected=true`, `OperationalError`, code `262`. |
| DML server-side prueba autoridad read-only | SLIPS | El DML default del verificador es `UPDATE sys.objects SET name = name WHERE 1 = 0`; el artefacto registra code `259`, compatible con rechazo de actualizacion de catalogo del sistema. No demuestra que el principal no pueda escribir en una tabla/probe ordinaria. |
| Evidencia s9 reproducible sin filtrar secretos | SLIPS | El artefacto es sano, pero demasiado opaco: no conserva una huella no sensible del tipo de target DML. Con el code `259`, el reviewer no puede confirmar que se probo denegacion de permisos DML real. |

## Residuales declarados

- No ejecute el s9 vivo contra la DB del operador porque las credenciales estan gitignored y no deben copiarse al artefacto; la revision adversarial se ancla al codigo, artefacto commiteado y pruebas de comportamiento locales.
- Un env mal configurado podria apuntar `SQLSERVER_HOST` fuera de loopback; el codigo no valida local-only. No lo gateo como defecto de TASK-0158 porque el alcance escrito declara host local por provision del operador, pero debe quedar explicito antes del flip.
