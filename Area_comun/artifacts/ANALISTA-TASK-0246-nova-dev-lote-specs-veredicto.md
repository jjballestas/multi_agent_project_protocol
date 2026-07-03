# ANALISTA-TASK-0246 - Veredicto lote NOVA-DEV Sprint 1

Firma: Analista
Fecha: 2026-07-03
Tarea: TASK-0246
Veredicto: CAMBIO-REQUERIDO / NO CERRABLE

## Ancla canonica

- Protocolo revisado: `acab21dc642474f9125ec5c0c6a00547c5990e4b`
- Instruccion REVIEW: `Area_comun/mailbox/open/MSG-20260703-Arquitecto-to-Analista-REVIEW-TASK-0246-nova-dev-lote-specs.md`
- Producto de control: `D:/Agentes/Zeus/Zeus-protocol` en `e7c6da482a1e819507af37de77b9cd46712fb8c8` (la instruccion no cita un commit de producto nuevo; uso el HEAD local como control no bloqueante)
- Alcance revisado: `Area_comun/specs/nova/NOVA-DEV-informe-revision-adversarial.md` + 9 SPECs `SPEC-NOVA-*.md`

## Reproduccion

| Gate | Resultado |
|---|---|
| `git fetch origin` | exit 0 |
| `git status --short` | exit 0; cambios ajenos solo en `.claude/settings.json` y `personal/Arquitecto/` / `personal/operador/` |
| `python scripts/validate_collaboration_state.py` | exit 0 |
| clean clone secretless `python scripts/validate_collaboration_state.py --root <tmp>` | exit 0 |
| `python scripts/scan_domain_neutrality.py` | exit 0 |
| `python scripts/scan_encoding.py` | exit 0 |
| drift runtime | `has_drift=False`, `up_to_seq=3643`, `entries=0` |
| chain runtime | `valid=True`, `checked_events=2971` |
| #4 byte-identica | `protocol.config.json` HEAD == `acab21d`; git blob hash `70d4c027a35b9d7d406bdfbe1cfcd427f203fc14`; sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |
| Zeus clean clone `npm test` | exit 0; 112 tests, 90 pass, 22 skipped |
| DbsFinanciero readonly existence check | exit 0 via container SQL Server; see vector table |

## Vector por vector

| Vector / AC | Resultado | Evidencia falsable |
|---|---|---|
| Formato unificado NOVA-SPEC-T-001 + intake-v2/DoR | PASA con slip de completitud | Las 9 SPECs tienen secciones `## 1` a `## 10`, preambulo, `task_id`, `owner_maker`, `checker`, `arm`, `isolation`, `db_verified_at`, `attestation` y `stack`. |
| q4_membership en cada SPEC | SLIPS | `SPEC-NOVA-P3-001`, `SPEC-NOVA-P3-002` y `SPEC-NOVA-P3-003` no declaran `q4_membership`. El estudio dice P3.1 primera unidad alcance congelado, P3.2/P3.3/P3.4 elegibles al pool Q4 si su DEC esta cerrada, y P3.5 fuera. La instruccion pide verificar q4_membership correcto por SPEC; tres quedan sin dato gobernado. |
| Citas BD: objetos existentes | PASA con excepciones declaradas | `Budget.Approve_*`, `Budget.Apply_Obligation_Adjustment`, tablas/vistas principales y `treasury.Payment_Order(_Budget_Line)` existen. `Get_Availability_Certificate_List`, `Get_Commitment_List`, `Get_Obligation_List`, `Get_Payment_List` no existen, pero `SPEC-NOVA-P2-004` los declara como procs a crear; no lo uso como bloqueo si el Arquitecto confirma que estos objetos son brecha intencional de la tarea, no cita de objeto existente. |
| Citas BD: THROWs falsables | SLIPS | En `Budget.Apply_Obligation_Adjustment`, la definicion desplegada contiene `50250`, `50251`, `50252`, `50253`, `50255`, `50257`, `50258`, `50264`, `50265`; NO contiene `50254` ni `50256`. La SPEC P4-004 exige `50256` para "acto no homogeneo" y lista `50252-50255`; el proc real usa `50265` para efecto distinto de reintegro. Ese criterio de aceptacion y su test de integracion quedarian buscando un codigo que no sale de ese proc. |
| Aislamiento P4-004 | PASA | P4-004 acota estrictamente a obligacion tipo 14/reintegro y excluye P4.1 01-04, P4.2 08/09 y P4.3 11/12; declara `leyo_codigo_hermano = NO`. |
| Aislamiento P2-004 / PAR-D | PASA | P2-004 separa los listados por documento de `Get_Budget_Execution_Report` / `fn_Budget_Execution_Report` / `vw_Budget_Execution_Movement`, declara el reporte agregado como territorio baseline P2.2 y exige architecture-test de aislamiento. |
| Coherencia cross-SPEC: aprobar-via-proc | PASA | Familia P3 y P4-004 fuerzan `Approve_*` / `Apply_Obligation_Adjustment` como canal unico y prohiben copiar filas o recalcular saldos en C#. |
| Coherencia cross-SPEC: stack obligatorio | PASA | Todas las SPECs declaran React+TS+Vite, ASP.NET Core .NET 10 en capas, SQL Server via gateways tipados, OpenTelemetry/ProblemDetails o el subconjunto aplicable. |
| ASCII / neutralidad / canonico | PASA | scan_encoding, scan_domain_neutrality, validate con y sin secretos, drift y #4 verdes. |

## Hallazgos bloqueantes

### F-0246-01 - q4_membership incompleto en P3.1/P3.2/P3.3

Severidad: D2 / ALTA para el estudio.

La instruccion pide validar `q4_membership` por SPEC. Tres SPECs no lo declaran:

- `Area_comun/specs/nova/SPEC-NOVA-P3-001-initial-budget-draft.md`
- `Area_comun/specs/nova/SPEC-NOVA-P3-002-availability-certificate-draft.md`
- `Area_comun/specs/nova/SPEC-NOVA-P3-003-commitment-draft.md`

Remediacion falsable: agregar `q4_membership` explicito en las tres, alineado al estudio: P3.1 fuera/no pool por primera unidad congelada si esa es la regla del sello, P3.2/P3.3 elegibles/condicionales segun DEC cerrada al sello de Etapa 2. El campo debe quedar en el preambulo como en P3.4/P3.5/P4-004.

### F-0246-02 - P4-004 exige THROW 50256 pero el proc real de obligacion usa 50265

Severidad: D2 / ALTA para implementabilidad.

Consulta readonly contra `DbsFinanciero`:

```text
Budget|Chain_Adjustment_Line_List
CREATE PROCEDURE Budget.Apply_Obligation_Adjustment
IF EXISTS(SELECT 1 FROM @lines WHERE effect_code <> 'counter_credit') THROW 50265,...
THROW 50255,...
THROW 50264,...
THROW 50258,...
```

La definicion de `Budget.Apply_Obligation_Adjustment` no contiene `50254` ni `50256`. Sin embargo P4-004:

- Campo 6b: "acto HOMOGENEO (RN-03, THROW 50256)"
- Criterio 3: "mezcla el tipo 14 con otro efecto -> THROW 50256"
- Campo 8: integra "un caso por THROW (..., 50256, 50252-50255, ...)"

Remediacion falsable: corregir P4-004 para que el negativo de efecto distinto de tipo 14 espere `50265`, o justificar con cambio real de BD si se decide modificar el proc. Si se conserva el rango `50252-50255`, aclarar que `50254` no esta emitido por el proc desplegado o retirar ese codigo del gate.

## Residuales declarados

- No ejecute paridad de procs mutadores porque el conector readonly no tiene EXECUTE y la propia entrega declara pendiente el GRANT EXECUTE / sandbox. Solo gateo existencia de objetos y presencia de codigos en definiciones.
- La instruccion REVIEW no cita commit de producto nuevo; el producto se uso como control en `e7c6da4`.
- Los procs `Get_*_List` de P2-004 faltan en BD; no bloqueo solo si se acepta que son objetos a crear por esa SPEC y no prerequisito de existencia.

## Recomendacion

CAMBIO-REQUERIDO. No cerrar TASK-0246 hasta corregir F-0246-01 y F-0246-02, re-ejecutar gates del hub, y pedir re-juicio Analista. Fix-loop esperado: una remediacion documental puntual, validate/encoding/domain/drift/#4 verdes, re-verificacion readonly de DbsFinanciero; maximo 2 iteraciones antes de escalar al operador.

task_id: TASK-0246
status: CAMBIO-REQUERIDO
executive_summary: "NO cerrable: el lote esta bien estructurado, pero tres SPECs omiten q4_membership y P4-004 pide THROW 50256/50254 contra un proc real que no los emite."
artifacts: ["Area_comun/artifacts/ANALISTA-TASK-0246-nova-dev-lote-specs-veredicto.md"]
gates: "validate=0; validate_secretless=0; scan_domain_neutrality=0; scan_encoding=0; drift=0 up_to_seq=3643; chain_valid checked_events=2971; #4 byte-identica sha256=2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354; Zeus npm test=0"
next_recommended: "Arquitecto remedia q4_membership de P3-001/P3-002/P3-003 y alinea P4-004 con los THROW reales de Apply_Obligation_Adjustment; luego re-gate Analista antes de cierre."
risks: "Si se cierra asi, el pool Q4 queda parcialmente no gobernado por campo ausente y el desarrollador/test de P4-004 perseguira codigos de error que no salen del proc desplegado."
