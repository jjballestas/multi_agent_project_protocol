# ANALISTA-TASK-0246 - THROW audit re-atribuido P3-001..005

Firma: Analista
Fecha: 2026-07-03
Tarea: TASK-0246
Veredicto: CAMBIO-REQUERIDO / NO CERRABLE para `db_verified_at` hasta corregir una omision de fuente

## Ancla canonica

- Protocolo HEAD / instruccion REQUEST: `2a0e89f` (`mailbox(REQUEST): Arquitecto -> Analista re-audit THROW re-atribuido opcion b (49689c4)`)
- Remediacion revisada: `49689c4` (`docs(TASK-0246): re-atribuye THROW por fuente en P3-001..005`)
- Instruccion: `Area_comun/mailbox/open/MSG-20260703-Arquitecto-to-Analista-REQUEST-TASK-0246-throw-audit-reatribuido.md`
- Producto de control: `D:/Agentes/Zeus/Zeus-protocol` en `e7c6da482a1e819507af37de77b9cd46712fb8c8` (la instruccion es doc-only y no cita producto nuevo)
- BD auditada: conexion readonly via `personal/operador/nova_sql_connector_readonly_s9.env`; evidencia reportada solo como codigos THROW y objetos, sin secretos ni definiciones completas.

## Reproduccion

| Gate | Resultado |
|---|---|
| `git fetch origin` | exit 0 |
| `git status --short` | exit 0; cambios ajenos preexistentes en `.claude/settings.json`, `personal/Analista/MEMORY.md`, `personal/Arquitecto/` y `personal/operador/`; no se tocaron para el juicio |
| `python scripts/validate_collaboration_state.py` | exit 0; warning no bloqueante sobre MSG informativo archivable |
| clean clone secretless `python scripts/validate_collaboration_state.py --root <tmp>` | exit 0 en `2a0e89f` |
| `python scripts/scan_domain_neutrality.py` | exit 0 |
| `python scripts/scan_encoding.py` | exit 0 |
| drift runtime | `has_drift=False`, `up_to_seq=3643`, `entries=[]` |
| chain runtime | `valid=True`, `checked_events=2971`, head `631af8d8e7a091589f27480e3415d6489e8e0c960cd4093ec054891649261d91` |
| #4 byte-identica | `protocol.config.json` blob `81cf406eb6e200deea001d3b48d5cf12f33d3f10` en `49689c4`, `HEAD` y tag `v1.18.0`; sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |
| Zeus clean clone `npm test` | exit 0; 112 tests, 90 pass, 22 skipped, commit `e7c6da482a1e819507af37de77b9cd46712fb8c8` |
| SQL readonly `OBJECT_DEFINITION` mapping | exit 0; todos los codigos auditados existen en proc directo, trigger o `Allocate_Document_Number` segun tabla abajo |

## Vector por vector

| Vector / AC | Resultado | Evidencia falsable |
|---|---|---|
| P3-001 proc directo vs trigger/check | PASA | `Approve_Initial_Budget_Draft` contiene `50270-50278`; `50054` esta en `trg_initial_budget__support_document_type_catalog`; `50057/50058` en `trg_initial_budget_line__validate_account`; `50059-50062` en `trg_initial_budget_draft_line__validate_account`. |
| P3-002 proc directo, numeracion y triggers | PASA | `Approve_Availability_Certificate_Draft` contiene `50145-50150`; `Allocate_Document_Number` contiene `50220-50223`; triggers contienen `50210/50211/50212`, `50066-50068` y `50076`. |
| P3-003 proc directo, numeracion y triggers declarados | SLIPS | `Approve_Commitment_Draft` contiene `50109-50115`; `Allocate_Document_Number` contiene `50220-50223`; triggers contienen `50091-50094` y `50210/50211`. Pero la SPEC tambien cita `THROW 50212` en la restriccion 6e y `throw_source` no lo lista ni lo atribuye. SQL confirma `50212` en `trg_commitment__validate_open_year`. |
| P3-004 proc directo, numeracion y triggers declarados | SLIPS | `Approve_Obligation_Draft` contiene `50128-50134`; `Allocate_Document_Number` contiene `50220-50223`; triggers contienen `50116-50121` y `50210/50211`. Pero la SPEC tambien cita `THROW 50212` en la restriccion 6f y `throw_source` no lo lista ni lo atribuye. SQL confirma `50212` en `trg_obligation__validate_open_year`. |
| P3-005 proc directo vs triggers | PASA | `Approve_Payment_Draft` contiene solo `50180-50187`; la SPEC ya corrigio PROC-DIRECTO a `50180-50187`; `50188/50189` estan en `trg_payment_draft__validate`; `50190` en `trg_payment_draft_line__same_obligation`; `54257` en `treasury.trg_Payment_Order_Budget_Line_Validate`. |

## Hallazgos

- WARNING-real / D2-S3: la re-atribucion opcion (b) cierra la clase original para casi todos los codigos, pero P3-003 y P3-004 siguen citando `50212` como THROW alcanzable de vigencia abierta sin incluirlo en `throw_source`. No es un codigo inventado: existe en la BD, pero la tabla de fuente queda incompleta.
- Residual no bloqueante: no ejecute procs mutadores; la verificacion fue readonly por `OBJECT_DEFINITION`, como pidio la instruccion.

## Recomendacion

CAMBIO-REQUERIDO. Remediacion minima: en `SPEC-NOVA-P3-003` agregar `50212` a `throw_source` como trigger `trg_commitment__validate_open_year`, y en `SPEC-NOVA-P3-004` agregar `50212` como trigger `trg_obligation__validate_open_year`; luego re-gatear validate con y sin secretos, encoding, neutrality, drift 0, #4 byte-identica y re-juicio Analista antes del cierre. Maximo 2 iteraciones antes de escalar al operador.

task_id: TASK-0246
status: change_required
executive_summary: "La re-atribucion transitive es mayormente fiel, pero db_verified_at no queda cerrable porque P3-003 y P3-004 aun citan THROW 50212 sin declararlo en throw_source."
artifacts:
  - Area_comun/artifacts/ANALISTA-TASK-0246-throw-audit-reatribuido-veredicto.md
gates:
  - command: git fetch origin
    result: PASS
  - command: python scripts/validate_collaboration_state.py
    result: PASS
  - command: clean clone secretless python scripts/validate_collaboration_state.py --root <tmp>
    result: PASS
  - command: python scripts/scan_domain_neutrality.py
    result: PASS
  - command: python scripts/scan_encoding.py
    result: PASS
  - command: runtime drift and chain probe
    result: PASS
  - command: protocol.config.json byte identity check against 49689c4, HEAD and v1.18.0
    result: PASS
  - command: Zeus clean clone npm test at e7c6da482a1e819507af37de77b9cd46712fb8c8
    result: PASS
  - command: SQL readonly OBJECT_DEFINITION mapping for P3-001..005 THROW families
    result: PASS
next_recommended: "Arquitecto remedia P3-003/P3-004 throw_source for 50212 and requests one re-juicio before closure."
risks: "If db_verified_at closes with 50212 omitted from throw_source, the SPEC still mixes cited THROWs and source evidence incompletely."
