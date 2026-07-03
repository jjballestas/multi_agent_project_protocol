# ANALISTA-TASK-0246 - THROW audit procs P3-001..005

Firma: Analista
Fecha: 2026-07-03
Tarea: TASK-0246
Veredicto: CAMBIO-REQUERIDO / NO CERRABLE para el gancho `db_verified_at` de F-NOVA-01

## Ancla canonica

- Protocolo HEAD / instruccion REQUEST: `5fdfb39edc2c292fb818e2bd4bfa1f567129525b`
- Instruccion: `Area_comun/mailbox/open/MSG-20260703-Arquitecto-to-Analista-REQUEST-TASK-0246-throw-audit-procs.md`
- Producto de control: `D:/Agentes/Zeus/Zeus-protocol` en `e7c6da482a1e819507af37de77b9cd46712fb8c8` (la instruccion es doc-only y no cita producto nuevo)
- BD auditada: conexion readonly via `personal/operador/nova_sql_connector_readonly_s9.env`; evidencia reportada solo como codigos THROW saneados, sin secretos ni definiciones completas.

## Reproduccion

| Gate | Resultado |
|---|---|
| `git fetch origin` | exit 0 |
| `git status --short` | exit 0; cambios ajenos preexistentes en `.claude/settings.json`, `personal/Analista/MEMORY.md`, `personal/Arquitecto/` y `personal/operador/`; no se tocaron para el juicio |
| `python scripts/validate_collaboration_state.py` | exit 0; warning no bloqueante sobre MSG informativo archivable |
| clean clone secretless `python scripts/validate_collaboration_state.py` | exit 0 en `5fdfb39edc2c292fb818e2bd4bfa1f567129525b` |
| `python scripts/scan_domain_neutrality.py` | exit 0 |
| `python scripts/scan_encoding.py` | exit 0 |
| drift runtime | `has_drift=False`, `up_to_seq=3643`, `entries=[]` |
| chain runtime | `valid=True`, `checked_events=2971`, head `631af8d8e7a091589f27480e3415d6489e8e0c960cd4093ec054891649261d91` |
| #4 byte-identica | `protocol.config.json` sin cambios; git blob `81cf406eb6e200deea001d3b48d5cf12f33d3f10`; sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |
| Zeus clean clone `npm test` | exit 0; 112 tests, 90 pass, 22 skipped, commit `e7c6da482a1e819507af37de77b9cd46712fb8c8` |
| SQL readonly `OBJECT_DEFINITION` probe | query exit 0; comparison exit 1 porque los cinco procs existen pero faltan codigos citados por las SPECs |

## Vector por vector

| Vector / AC | Resultado | Evidencia falsable |
|---|---|---|
| P3-001 `Budget.Approve_Initial_Budget_Draft` cita `50270-50278` | PASA | `OBJECT_DEFINITION` contiene `50270,50271,50272,50273,50274,50275,50276,50277,50278`. |
| P3-001 cita doc soporte y triggers de linea `50054`, `50057-50062` | SLIPS | El proc directo no contiene `50054,50057,50058,50059,50060,50061,50062`. |
| P3-002 `Budget.Approve_Availability_Certificate_Draft` cita `50145-50150` | PASA | `OBJECT_DEFINITION` contiene `50145,50146,50147,50148,50149,50150`. |
| P3-002 cita `50210/50211/50212`, `50220-50223`, `50066-50068`, `50076` | SLIPS | El proc directo no contiene `50066,50067,50068,50076,50210,50211,50212,50220,50221,50222,50223`. |
| P3-003 `Budget.Approve_Commitment_Draft` cita `50109-50115` | PASA | `OBJECT_DEFINITION` contiene `50109,50110,50111,50112,50113,50114,50115`. |
| P3-003 cita `50091-50094`, `50210/50211` | SLIPS | El proc directo no contiene `50091,50092,50093,50094,50210,50211`. |
| P3-004 `Budget.Approve_Obligation_Draft` cita `50128-50134` | PASA | `OBJECT_DEFINITION` contiene `50128,50129,50130,50131,50132,50133,50134`. |
| P3-004 cita `50116-50121`, `50210/50211` | SLIPS | El proc directo no contiene `50116,50117,50118,50119,50120,50121,50210,50211`. |
| P3-005 `Budget.Approve_Payment_Draft` cita `50180-50190`, `54257` | SLIPS | El proc directo contiene solo `50180,50181,50182,50183,50184,50185,50186,50187`; no contiene `50188,50189,50190,54257`. |

## Hallazgos

- CRITICAL / D2-S2: F-NOVA-01 no puede marcar `db_verified_at` como cerrado si la evidencia prometida es `OBJECT_DEFINITION` del proc de aprobacion directo. Los cinco procs existen, pero todos tienen codigos citados que el proc desplegado no contiene.
- WARNING-real / D2-S3: Puede existir una explicacion transitive por procs llamados, pero esa no es la evidencia pedida ni queda expresada en las SPECs. Si se acepta semantica transitive, cada SPEC debe decirlo y listar el proc fuente del THROW, no atribuirlo al `Approve_*` directo.

## Recomendacion

CAMBIO-REQUERIDO. No revierte por si mismo el OK previo de F-0246-01/F-0246-02, pero el cierre del gancho `db_verified_at` de F-NOVA-01 no es cerrable con la evidencia actual.

Fix-loop esperado: Codex/Arquitecto debe remediar las SPECs P3-001..005 eliminando o reatribuyendo los codigos ausentes, o aportar una tabla transitive falsable `Approve_* -> proc llamado -> THROW` basada en BD. Gates afectados: validate con y sin secretos, encoding, neutrality, drift 0, #4 byte-identica y re-juicio Analista por OBJECT_DEFINITION. Maximo 2 iteraciones antes de escalar al operador.

## Residuales declarados

- No ejecute procs mutadores; la verificacion fue readonly por `OBJECT_DEFINITION`, como pidio la instruccion.
- No publique definiciones SQL completas ni datos de conexion; solo codigos THROW y nombres de procs ya citados por la instruccion.
- La instruccion no cita commit nuevo de producto; use `e7c6da482a1e819507af37de77b9cd46712fb8c8` como control de `npm test`, no como ancla de aceptacion documental.

task_id: TASK-0246
status: CAMBIO-REQUERIDO
executive_summary: "No cerrable para db_verified_at: los 5 procs Approve_* existen, pero OBJECT_DEFINITION directo no contiene todos los THROW que P3-001..005 citan."
artifacts: ["Area_comun/artifacts/ANALISTA-TASK-0246-throw-audit-procs-veredicto.md"]
gates: "validate=0; validate_secretless=0; scan_domain_neutrality=0; scan_encoding=0; drift=0 up_to_seq=3643; chain_valid checked_events=2971; #4 byte-identica sha256=2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354; Zeus npm test=0; SQL readonly query=0 comparison=1"
next_recommended: "Remediar P3-001..005: quitar codigos no emitidos por el proc directo o documentar la cadena transitive proc llamado -> THROW con evidencia BD; luego re-juicio Analista antes de cierre."
risks: "Si se marca db_verified_at sin corregir atribucion directa vs transitive, se repite la clase de error de P4-004: SPEC afirma codigos que la evidencia OBJECT_DEFINITION directa no sostiene."
