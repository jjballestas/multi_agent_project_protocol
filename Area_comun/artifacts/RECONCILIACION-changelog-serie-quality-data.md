# Reconciliacion changelog Nova-Budget <-> serie formal quality-data del hub

> ACTION del Operador 2026-07-06 (reconciliar-changelog-quality-series). Objetivo: que TODO
> defecto baseline sea hallazgo atestado en el hub, no solo nota de changelog del producto.
> Fix-forward, sin reabrir unidades medidas. Mapeo generado con subagente adversarial +
> claim de tenant-isolation VERIFICADO por el Arquitecto en codigo real (2026-07-06 ~17:15
> local). Insumo de la reconciliacion 26-29-jul.

## 0. ALERTA: dos numeraciones en circulacion (fijar antes del 26-29 o hay doble conteo)

La serie FORMAL del hub (#1-#13, asignada en los MSG del Operador/Arquitecto 2026-07-05/06) y
la numeracion de la TABLA del changelog del producto NO comparten indices. El caso critico:
- changelog "punto 8 / hallazgo de seguridad auth" == hub **#5** (auth, dueno Analista).
- hub **#8** == esquema de persistencia (deuda docs), NO seguridad.
=> "#5/#8 de seguridad" citado en `SPEC-NOVA-P4-006` (lineas 52, 154) mezcla un alias del
changelog con la serie del hub. **NO existen dos hallazgos de auth; es UNO con dos alias.**
La serie CANONICA es la del HUB. La tabla de abajo usa la numeracion del changelog en la
columna 1 SOLO para trazar el origen; la columna "hub" es la autoridad.

## 1. Tabla de correspondencia (15 puntos del changelog)

| # changelog | Punto | Hub | Estado |
|---|---|---|---|
| 1 | Transiciones BudgetDocumentState + quien ejecuta | #7 | owned, horneado SPEC-P4-006:52-64 |
| 2 | Esquema de persistencia (tablas/PK/FK) | #8 | deuda docs ("BD manda") |
| 3 | Verticales placeholders Budget/* | #9 | roadmap + guard Q4 |
| 4 | Salto RN-07/08/09 en Map | #4 | deuda registrada |
| 5 | Nomenclatura ReadOnlySql | #1 | RESUELTO commit 75913aa |
| 6 | Carpeta huerfana ExecutionReports | #2 | higiene |
| 7 | Carpetas vacias src/NOVA/* | #3 | higiene |
| 8a | API sin autenticacion (10 endpoints) | **#5** | ATESTADO (ANALISTA-HALLAZGO-AUTH-DD01) |
| 8b | Aislamiento de tenant sin filtro | **#14 (NUEVO)** | registrado aqui, veredicto Analista pendiente |
| 9 | README desactualizado | #6 | deuda |
| 10 | Titulo cruzado THROW 50212 | #10 | ruteado, veredicto pendiente |
| 11 | Brecha RN-A06 en mapeo | **#15 (NUEVO)** | registrado aqui (baja) |
| 12 | Vertical Apply_Commitment_Adjustment | #9 + SPEC-P4-003 | roadmap gobernado |
| 13 | Annul_Commitment roadmap + omision guard frontend | #9/SPEC-P4-006 + #13 | ruteado |
| 14 | Sin test HTTP annul-preview/annul | #12 | ruteado, fix-forward 6j |
| 15 | Nombres de columna inciertos + default 'A' | #11 | ruteado, fix-forward 6i |

Honestidad Q2: de la serie, solo **#5** tiene artefacto de veredicto ATESTADO. #10-#13
ruteados (2 ACTIONs vivas, response_owner Analista) sin artefacto aun. #1-#9 viven en MSG de
triage, no en artefactos de veredicto. #14/#15 registrados hoy (este artefacto).

## 2. Hallazgos NUEVOS registrados (fix-forward, NO reabren baseline)

### #14 - Aislamiento de tenant en lecturas de gateway (SEGURIDAD, ALTA)
VERIFICADO por el Arquitecto en codigo real: `SqlAvailabilityAdjustmentGateway.
GetBalancesAsync` (`src/NOVA.Infrastructure/Budget/AvailabilityAdjustments/...:94-98`) hace
`SELECT ... FROM vw_Commitment_Availability_Validation WHERE availability_certificate_line_id
IN (...)` -- sin `tenant_id` ni `fiscal_year_id`. Setea `sp_set_session_context('tenant_id')`
antes (`:90`), PERO la vista de referencia NO expone `tenant_id` ni consume SESSION_CONTEXT y
NO hay RLS en el arbol de migracion (grep SECURITY POLICY = 0). => saldos enumerables
cross-tenant por line_id, agravado por #5 (cero auth). Alcance MAYOR que el changelog: tambien
`SqlAvailabilityCertificateAnnulmentGateway` (`:137-142`, `:157-163`) lee sin filtro tenant.
Contraste (no es exageracion general): `SqlBudgetParametersGateway`, `SqlAppropriation
ModificationGateway`, `SqlBudgetExecutionReportGateway` SI filtran tenant -- el defecto es
especifico de las lecturas de saldo de los 2 gateways nuevos (P4.2/PAR-2). Caveat: la BD
desplegada podria diferir de las fuentes Ingenas (RLS anadida por el DBA), no verificable
desde los repos; ningun artefacto del hub sugiere que exista.
- Disposicion: **quality-data Q2 del baseline, NO reabre la unidad medida** (igual que #5/#8).
- Fix-forward HORNEADO: `SPEC-NOVA-P4-006` restriccion **6l** + criterio **13** (harness con
  caso negativo cross-tenant). Replica anotada a SPEC-NOVA-P4-003/P4-004 (misma vista).
- Nota para el DBA: como la vista no expone tenant_id, el fix exige cambiar la vista/camino de
  lectura o cablear RLS -- no es solo un WHERE. Entra en el encargo DBA de Contabilidad/Sprint 1.

### #15 - Brecha RN-A06 en el mapeo de disponibilidad (BAJA, documental)
Solo en el changelog; mismo patron que #4. Mecanismo de fix ya existe (SPEC-P4-006 s.5,
re-verificacion F-NOVA-01 de codigos contra OBJECT_DEFINITION). Criterio a hornear: "mapa RN
contiguo o hueco justificado por evidencia DBA". Baja prioridad, no seguridad.

## 3. Proximo numero libre de la serie: #16 (tras registrar #14 y #15)

## 4. Recomendacion de proceso
Fijar la TABLA DE ALIAS (seccion 0/1) como parte del material de reconciliacion 26-29-jul para
evitar doble contabilidad en Q2; corregir la cita "#5/#8 de seguridad" de SPEC-P4-006 a
"#5 (auth) + #14 (tenant)" en la proxima edicion gobernada de esa SPEC.
