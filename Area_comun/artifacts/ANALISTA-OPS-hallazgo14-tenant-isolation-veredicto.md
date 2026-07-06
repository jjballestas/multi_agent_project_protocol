# Veredicto Analista - Hallazgo #14 tenant isolation

Firma: Analista
Fecha: 2026-07-06
Ancla protocolo: `aa38f18ff01fdd678350d59d2a3dc7bf729096ee`
Ancla producto revisada: `edbc037be8ce8297fbf308f611eef8c84aeccbf0`
Instruccion: `Area_comun/mailbox/open/MSG-20260706-Arquitecto-to-Analista-ACTION-hallazgo14-tenant-isolation-quality-data.md`

## Veredicto

CONFIRMADO. El hallazgo #14 es real: las lecturas de saldo/preview revisadas establecen `SESSION_CONTEXT('tenant_id')`, pero las queries que devuelven datos no filtran por `tenant_id` y no hay evidencia versionada de RLS o de una vista que consuma `SESSION_CONTEXT('tenant_id')`. El fix-forward de `SPEC-NOVA-P4-006` en restriccion 6l y criterio 13 cubre el defecto correcto.

Recomendacion de cierre: OK->CERRABLE para registrar el hallazgo #14 como quality-data Q2 del baseline, sin reabrir la unidad medida. Residual declarado: el gate `npm test` en raiz del producto sale `-4058` porque el repo no tiene `package.json` raiz; la instruccion canonica del MSG declara `SIN PRODUCTO EN ALCANCE`, por lo que lo trato como residual de gate transversal, no como refutacion del hallazgo.

## Reproduccion

| Comando | Resultado |
|---|---:|
| `git fetch origin` en protocolo | 0 |
| `python scripts/validate_collaboration_state.py` en protocolo vivo | 0 |
| `git clone D:/Agentes/Zeus/NOVA/Nova-Budget <tmp>` | 0 |
| `git -C <tmp> checkout edbc037be8ce8297fbf308f611eef8c84aeccbf0` | 0 |
| `npm test --prefix <tmp>` | -4058 |
| `dotnet test <tmp>/NOVA.sln --no-restore` | 0 |
| Probe propio de commandText de gateways | 0 |
| `python scripts/validate_collaboration_state.py` vivo | 0 |
| `python scripts/validate_collaboration_state.py` en clon limpio sin `secrets/` | 0 |
| `python scripts/scan_domain_neutrality.py` | 0 |
| `python scripts/scan_encoding.py` | 0 |
| Drift runtime | 0 drift, `up_to_seq=4351` |
| `protocol.config.json` byte-identico contra HEAD | 0, sha256 `2E35F26E06DE4D0A7E5278BABB2107A9BBE6441C78B99A1886A613070B1EB354` |

## Vector por vector

| Vector / AC a refutar | Evidencia independiente | Resultado |
|---|---|---|
| `SqlAvailabilityAdjustmentGateway.GetBalancesAsync` filtra tenant | En `src/NOVA.Infrastructure/Budget/AvailabilityAdjustments/SqlAvailabilityAdjustmentGateway.cs`, el commandText selecciona de `AvailabilityAdjustmentService.BalanceViewName` y filtra solo `availability_certificate_line_id IN (...)`. El parametro `tenantId` solo alimenta `sp_set_session_context`. | SLIPS confirmado |
| La familia de lecturas de anulacion filtra tenant | En `SqlAvailabilityCertificateAnnulmentGateway.cs`, `ReadCurrentAvailabilityAsync` filtra por `fiscal_year_id` y `availability_certificate_id`; `ReadActiveReservationCountAsync` filtra por `fiscal_year_id`, `availability_certificate_id` y `current_committed_amount > 0`. Ninguna query agrega `tenant_id`. | SLIPS confirmado |
| La vista/RLS compensa la ausencia de WHERE tenant | Busqueda versionada no encontro `CREATE/ALTER SECURITY POLICY` ni definicion versionada de `vw_Commitment_Availability_Validation` con `SESSION_CONTEXT('tenant_id')`; el unico hit de `SESSION_CONTEXT` fuera de codigo/test es documentacion del harness. | SLIPS confirmado |
| Contraste: no es un defecto global de todos los gateways | `SqlAppropriationModificationGateway` filtra `WHERE tenant_id = @tenant_id`; `SqlBudgetParametersGateway` filtra tenant en sus queries; `SqlBudgetExecutionReportGateway` pasa `@tenant_id` al proc. | PASA, defecto acotado |
| Fix-forward en SPEC-P4-006 cubre toda la familia | Restriccion 6l exige filtro tenant explicito o vista/RLS verificada por `OBJECT_DEFINITION` + `SECURITY POLICY`; criterio 13 exige negativo cross-tenant y falla si solo se setea session context. | PASA |

## Residuales

- No verifique la BD desplegada: no habia credenciales ni alcance DBA en la instruccion; si el DBA agrego RLS fuera del repo, no queda atestado aqui.
- `npm test` raiz no es reproducible en este repo de producto porque no existe `package.json` raiz. El control no cambia el veredicto tecnico sobre las queries C#/SQL revisadas.
- La remediacion debe decidir con DBA si expone `tenant_id` en la vista, cambia el camino de lectura o cablea RLS.

## Envelope

task_id: OPS-HALLAZGO-14
status: CONFIRMADO-CERRABLE
executive_summary: Hallazgo #14 confirmado; las lecturas de saldo/preview setean session context pero no filtran tenant y no hay RLS/vista versionada que lo compense.
artifacts: Area_comun/artifacts/ANALISTA-OPS-hallazgo14-tenant-isolation-veredicto.md
gates: validate vivo 0; validate sin secretos 0; domain 0; encoding 0; drift 0 up_to_seq=4351; protocol.config byte-identico; producto dotnet 0; producto npm raiz -4058 residual por ausencia de package.json.
next_recommended: Registrar #14 como quality-data Q2 fix-forward ya horneado en SPEC-P4-006 6l/criterio 13; no reabrir baseline medido.
risks: BD desplegada podria tener RLS no versionada; root npm test no aplica hasta que exista package.json raiz o gate canonico acotado.
