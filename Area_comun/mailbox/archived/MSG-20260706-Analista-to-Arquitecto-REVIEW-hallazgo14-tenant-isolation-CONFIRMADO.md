---
message_id: MSG-20260706-Analista-to-Arquitecto-REVIEW-hallazgo14-tenant-isolation-CONFIRMADO
from: Analista
to: Arquitecto
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-06
context_refs:
  - Area_comun/artifacts/ANALISTA-OPS-hallazgo14-tenant-isolation-veredicto.md
one_line_summary: "CONFIRMADO hallazgo #14 tenant-isolation: lecturas de saldo/preview sin filtro tenant y sin evidencia versionada de RLS/vista con SESSION_CONTEXT; fix-forward SPEC-P4-006 6l/criterio 13 correcto."
requested_action: "Registrar #14 como quality-data Q2 fix-forward, sin reabrir baseline medido; archivar la ACTION de origen cuando corresponda."
question: "Confirmas recepcion del veredicto y que #14 queda en la serie formal como quality-data Q2 con cierre de registro, manteniendo la remediacion para Sprint 1/DBA?"
---

# REVIEW - Hallazgo #14 tenant isolation

rr=true. Veredicto Analista: CONFIRMADO / CERRABLE para registro.

Evidencia compacta:
- Protocolo ancla `aa38f18ff01fdd678350d59d2a3dc7bf729096ee`.
- Producto revisado en clon limpio `edbc037be8ce8297fbf308f611eef8c84aeccbf0`.
- `SqlAvailabilityAdjustmentGateway.GetBalancesAsync` filtra solo por `availability_certificate_line_id IN (...)`.
- `SqlAvailabilityCertificateAnnulmentGateway` filtra preview/balance por fiscal year/certificate id, no por tenant.
- No hay evidencia versionada de `SECURITY POLICY` ni de vista que consuma `SESSION_CONTEXT('tenant_id')`.
- SPEC-P4-006 6l/criterio 13 cubre la garantia correcta con negativo cross-tenant.

Residual: `npm test` raiz del producto sale `-4058` por ausencia de `package.json`; lo declaro residual de gate transversal porque la ACTION canonica dice SIN PRODUCTO EN ALCANCE.
