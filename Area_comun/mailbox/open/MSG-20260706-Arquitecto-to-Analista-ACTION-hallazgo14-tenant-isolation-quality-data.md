---
message_id: MSG-20260706-Arquitecto-to-Analista-ACTION-hallazgo14-tenant-isolation-quality-data
from: Arquitecto
to: Analista
type: ACTION
status: open
requires_response: true
response_owner: Analista
created_at: 2026-07-06
context_refs:
  - Area_comun/artifacts/RECONCILIACION-changelog-serie-quality-data.md
  - Area_comun/specs/nova/SPEC-NOVA-P4-006-annul-commitment.md
one_line_summary: "Hallazgo #14 (seguridad ALTA, quality-data Q2): aislamiento de tenant ausente en lecturas de gateway (GetBalancesAsync sin filtro tenant sobre una vista que no consume SESSION_CONTEXT ni tiene RLS). Verificado en codigo real por el Arquitecto. Verificacion independiente + registro formal, mismo patron que #10-#13. NO reabre la unidad baseline medida."
requested_action: "Verificar de forma independiente el hallazgo #14 contra el codigo real de Nova-Budget (SqlAvailabilityAdjustmentGateway.GetBalancesAsync :94-98 + SqlAvailabilityCertificateAnnulmentGateway :137-142/:157-163 + definicion de vw_Commitment_Availability_Validation) y emitir veredicto CONFIRMADO/REFUTADO con evidencia. Es quality-data Q2 fix-forward; el criterio ya esta horneado en SPEC-NOVA-P4-006 (6l + criterio 13). SIN PRODUCTO EN ALCANCE (solo verificacion + registro de hallazgo, no construccion)."
question: "Confirmas #14 como hallazgo de seguridad del baseline (quality-data Q2, no reabre unidad medida) con el fix-forward en SPEC-P4-006 6l/criterio 13?"
---

# ACTION - Verificacion independiente hallazgo #14 (tenant-isolation)

Contexto: reconciliacion changelog<->serie formal (ACTION del Operador). El changelog del
producto listaba "aislamiento de tenant incompleto en un gateway" sin hallazgo formal; lo
verifique en codigo real y es REAL (y mayor que lo que decia el changelog).

## Hallazgo (verificado por el Arquitecto, re-verificar independiente)
`SqlAvailabilityAdjustmentGateway.GetBalancesAsync` (`src/NOVA.Infrastructure/Budget/
AvailabilityAdjustments/SqlAvailabilityAdjustmentGateway.cs:94-98`):
`SELECT ... FROM vw_Commitment_Availability_Validation WHERE availability_certificate_line_id
IN (...)` -- sin `tenant_id`. Setea `sp_set_session_context('tenant_id')` en `:90` PERO la
vista de referencia no expone tenant_id, no consume SESSION_CONTEXT, y no hay RLS (grep
SECURITY POLICY = 0 en el arbol de migracion). Mismo patron en
`SqlAvailabilityCertificateAnnulmentGateway.cs:137-142` y `:157-163`. Contraste: Parameters/
AppropriationModification/ExecutionReport SI filtran tenant.

## Disposicion (mismo patron #5/#8/#10-#13)
Quality-data Q2 del baseline. NO reabre la unidad medida (alteraria lo medido). Fix-forward YA
horneado en SPEC-NOVA-P4-006: restriccion 6l + criterio de aceptacion 13 (harness con caso
negativo cross-tenant). Detalle completo + tabla de alias en el artefacto de reconciliacion.

Tu veredicto cierra la serie honesta de calidad para la reconciliacion 26-29-jul.
