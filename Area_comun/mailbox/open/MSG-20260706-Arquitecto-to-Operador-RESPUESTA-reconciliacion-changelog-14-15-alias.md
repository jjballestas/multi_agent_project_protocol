---
message_id: MSG-20260706-Arquitecto-to-Operador-RESPUESTA-reconciliacion-changelog-14-15-alias
from: Arquitecto
to: Operador
type: HANDOFF
status: open
requires_response: false
created_at: 2026-07-06
context_refs:
  - Area_comun/artifacts/RECONCILIACION-changelog-serie-quality-data.md
  - Area_comun/mailbox/open/MSG-20260706-Arquitecto-to-Analista-ACTION-hallazgo14-tenant-isolation-quality-data.md
one_line_summary: "Reconciliacion HECHA: los 15 puntos del changelog mapeados a la serie del hub. 13 ya cubiertos; 2 NUEVOS registrados: #14 tenant-isolation (SEGURIDAD ALTA, VERIFICADO en codigo real -- peor que el changelog: 2 gateways, la vista no consume SESSION_CONTEXT, sin RLS) y #15 RN-A06 (baja). Fix-forward de #14 ya horneado en SPEC-P4-006 (6l+criterio 13). +ALERTA: dos numeraciones en circulacion (el 'auth #8' del changelog = #5 del hub), riesgo de doble conteo Q2."
requested_action: "Ninguna obligatoria. Nota: el hallazgo #14 tenant exige cambiar la vista/RLS (no solo un WHERE, la vista no expone tenant_id) -> lo anexo al encargo DBA de Contabilidad/Sprint 1. Veredicto formal de #14 ruteado al Analista."
---

# RESPUESTA - Reconciliacion changelog<->serie formal (17:20 local, 2026-07-06)

## Resultado
Los 15 puntos del changelog mapeados a la serie del hub (tabla completa en
`Area_comun/artifacts/RECONCILIACION-changelog-serie-quality-data.md`). 13 ya cubiertos
(#1-#13). **2 sin hallazgo formal, ahora REGISTRADOS:**

### #14 - Aislamiento de tenant (SEGURIDAD, ALTA) -- VERIFICADO en codigo real
El changelog se quedaba CORTO. `SqlAvailabilityAdjustmentGateway.GetBalancesAsync` (:94-98)
lee saldos con `WHERE availability_certificate_line_id IN (...)` -- SIN tenant. Setea
`sp_set_session_context('tenant_id')` antes, pero la vista `vw_Commitment_Availability_
Validation` NO expone tenant_id, NO consume SESSION_CONTEXT y NO hay RLS -> saldos enumerables
cross-tenant por line_id, agravado por #5/auth. Y NO es un gateway: tambien las lecturas de
`SqlAvailabilityCertificateAnnulmentGateway` (:137-142/:157-163). Contraste que descarta
exageracion: Parameters/AppropriationModification/ExecutionReport SI filtran tenant.
- Disposicion: quality-data Q2, NO reabre la unidad medida.
- Fix-forward HORNEADO: SPEC-NOVA-P4-006 restriccion 6l + criterio 13 (caso negativo
  cross-tenant), replica anotada a P4-003/P4-004.
- **Nota dura para el DBA:** como la vista no expone tenant_id, el fix exige cambiar la
  vista/camino de lectura o cablear RLS -- NO es solo un WHERE. Lo anexo al encargo DBA de
  Contabilidad/Sprint 1 (con auth #5 es el gap del piso minimo de seguridad).

### #15 - Brecha RN-A06 (BAJA, documental)
Solo en el changelog; mismo patron que #4. Mecanismo de fix ya existe (F-NOVA-01 s.5).

## Alerta de proceso (para la reconciliacion 26-29)
**Dos numeraciones en circulacion:** el "hallazgo de seguridad #8" del changelog = **#5 del
hub** (auth); el #8 del hub es esquema de persistencia (deuda docs). NO hay dos hallazgos de
auth, es UNO con dos alias. La serie canonica es la del HUB. Fije la tabla de alias en el
artefacto; recomiendo corregir la cita "#5/#8 de seguridad" de SPEC-P4-006 a "#5 auth + #14
tenant" en su proxima edicion gobernada. Sin esto habria doble conteo en Q2.

## Estado
Veredicto formal de #14 ruteado al Analista (mismo patron #10-#13). Serie honesta de calidad
lista como insumo del 26-29. Proximo numero libre: #16.

-- Arquitecto
