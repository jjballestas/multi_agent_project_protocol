# Veredicto Analista - TASK-0246 informe + SPEC P4-006

Firma: Analista.

## Veredicto

CAMBIO-REQUERIDO / NO CERRABLE.

Ancla canonica revisada: protocolo `af18d5be3224212dbee7235bfc0dbeaa8d7d3a62` (`coord(TASK-0255/0246): fix-forward hallazgos #11-13 + REVIEW TASK-0246`). Producto Nova-Budget: N/A por instruccion canonica; el REVIEW declara alcance 100% documental del hub y no cita commit de producto. Ejecutar un HEAD arbitrario de producto no seria una prueba canonica.

## Reproduccion

| Gate / prueba | Resultado |
|---|---|
| `git fetch origin` + `git status --short` | HEAD `af18d5b` == `origin/main`; arbol vivo con cambios ajenos no stageados fuera de este veredicto |
| `python scripts/validate_collaboration_state.py` vivo | EXIT 0 |
| Lectura `Area_comun/state/*.json` con `utf-8-sig` | OK |
| Clean clone hub checkout `af18d5b`: `python scripts/validate_collaboration_state.py` | EXIT 0 |
| Clean clone hub checkout `af18d5b`: `python scripts/scan_encoding.py` | EXIT 0 |
| Clean clone hub checkout `af18d5b`: `python scripts/scan_domain_neutrality.py` | EXIT 0 |
| Drift clean clone | `has_drift=false`, `up_to_seq=4256` |
| Chain clean clone | valid, `checked_events=3584`, head `533217125279f093f1cb92dc1e75519ffc64d3135e1cfda1637367a8f158b556` |
| #4 byte-identica | `protocol.config.json` sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Vectores

| Vector / AC | Veredicto | Evidencia falsable |
|---|---|---|
| Alcance docs-only / sin producto | PASA | REVIEW canonico declara `SIN PRODUCTO EN ALCANCE`; no hay commit de Nova-Budget citado. |
| Inventario de SPECs del hub | SLIPS | `Area_comun/specs/nova/` contiene 17 `SPEC-NOVA-*.md`: F3.3, P2-001..004, P3-001..005, P4-001..006, P6-003. El informe dice "12 SPECs existentes" aunque su propia enumeracion suma 17. |
| Mapeo RES-000..012 -> SPEC | PASA con correccion de conteo pendiente | La familia cubierta coincide con los archivos existentes: RES-001 P2-002; RES-002 P2-001/P3-001; RES-003 P4-001; RES-004 P3-002/P4-002/P4-005; RES-005 P3-003/P4-003/P4-006; RES-006 P3-004/P4-004; RES-007 P3-005; transversales P6-003/F3.3. |
| Gaps fuera de alcance | PASA | No hay SPEC dedicada para anulacion de obligacion, ajuste/anulacion de pago, cascada pago-radicacion-obligacion, cierre de vigencia, PAC, libros oficiales ni reportes regulatorios. El sello Ingenas declara PAR-2 = `Annul_Availability_Certificate` vs `Annul_Commitment` y pool Q4 separado; estos gaps no entran en pares ya sorteados. |
| P4-006 formato NOVA-SPEC-T-001 + DoR | PASA | En `SPEC-NOVA-P4-006-annul-commitment.md` existen `spec_id`, checker Analista formal, arm PAR-2 gobernado, `q4_membership`, isolation critica, measurement, F-NOVA-01, guard de procedencia y stack obligatorio. |
| Fix-forward #11/#12/#13 | PASA | Canonico `af18d5b` contiene restricciones 6i/6j/6k y criterios 10/11/12: lectura exacta de result-set, tests HTTP de integracion y lista de aislamiento con `Annul_Commitment`. |
| Referencias internas de P4-006 | SLIPS | El preambulo de autorizacion dice "ver s.6 restriccion (h) y s.7 criterio 9", pero el criterio de autorizacion es el 6; el criterio 9 es guard de procedencia SQL real. |

## Hallazgos bloqueantes

- F-0246-INF-01 (WARNING-real, D3/S5): `Area_comun/specs/nova/INFORME-ADVERSARIAL-NOVA-DEV-paquete-ingenas-TASK-0246.md` declara "12 SPECs existentes" aunque el inventario canonico tiene 17. Repro: `Get-ChildItem Area_comun/specs/nova/SPEC-NOVA-*.md` cuenta 17 y la propia lista P2-001..004 + P3-001..005 + P4-001..006 + P6-003 + F3.3 suma 17.
- F-0246-P4006-01 (WARNING-real, D3/S5): `Area_comun/specs/nova/SPEC-NOVA-P4-006-annul-commitment.md` referencia el criterio 9 para autorizacion real; el criterio correcto es el 6. Repro: buscar "criterio 9" en el preambulo y comparar con s.7.

## Residuales

- Producto Nova-Budget no ejecutado: fuera de alcance canonico y sin commit de producto citado.
- No hice verificacion SQL directa; el REVIEW pedido es documental. Las afirmaciones de DBA/sello quedan como entradas documentales a re-verificar por F-NOVA-01 al implementar.

## Fix-loop esperado

Remediacion documental puntual en maximo 2 iteraciones antes de escalar al operador:

1. Corregir el conteo del informe a 17 SPECs o reescribir la frase sin numero si se pretendia otra taxonomia.
2. Corregir la referencia de P4-006 de `criterio 9` a `criterio 6` para autorizacion real.
3. Re-gatear `validate_collaboration_state.py`, `scan_encoding.py`, `scan_domain_neutrality.py`, drift 0 y #4 byte-identica; pedir re-juicio Analista antes de cierre.

---
task_id: TASK-0246
status: CAMBIO-REQUERIDO
executive_summary: No cerrable por dos slips documentales falsables: inventario de SPECs declarado como 12 cuando el canonico tiene 17, y referencia interna de P4-006 a criterio 9 para autorizacion cuando el criterio correcto es 6.
artifacts: Area_comun/artifacts/ANALISTA-TASK-0246-informe-specs-veredicto.md
gates: validate vivo EXIT 0; clean clone hub validate EXIT 0; scan_encoding EXIT 0; scan_domain_neutrality EXIT 0; drift has_drift=false up_to_seq=4256; chain valid checked_events=3584; protocol.config sha256 2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354.
next_recommended: Remediacion documental puntual y re-juicio Analista; no cerrar TASK-0246 todavia.
risks: Producto fuera de alcance por instruccion canonica; SQL no re-verificado en esta pasada documental.
