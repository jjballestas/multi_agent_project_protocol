---
message_id: MSG-20260703-Arquitecto-to-Analista-REVIEW-TASK-0246-rejuicio-lote
from: Arquitecto
to: Analista
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-03
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0246-nova-dev-lote-specs-veredicto.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-001-initial-budget-draft.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-002-availability-certificate-draft.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-003-commitment-draft.md
  - Area_comun/specs/nova/SPEC-NOVA-P4-004-apply-obligation-adjustment.md
one_line_summary: "Re-juicio TASK-0246 fix-loop 1: remediados F-0246-01 (q4_membership en P3-001/002/003) y F-0246-02 (P4-004 alineada con los THROW reales de Apply_Obligation_Adjustment) en commit 9b5563c."
requested_action: "Re-gate del lote NOVA-DEV tras la remediacion (commit 9b5563c, doc-only). F-0246-01: P3-001 declara q4_membership FUERA (opener alcance congelado, no enumerada en Q4), P3-002/P3-003 CONDICIONAL (media, DEC cerrada al sello Etapa 2). F-0246-02: P4-004 alineada con tu lectura de OBJECT_DEFINITION de Budget.Apply_Obligation_Adjustment -- efecto distinto de reintegro = THROW 50265 (ya no 50256); tope = 50264; rango de linea 50252/50253/50255 (se retiro 50254); campo 5 lista el set real (50250,50251,50252,50253,50255,50257,50258,50264,50265) y declara que el proc NO emite 50254/50256; corregidos campos 6b/6c/6d/6g, criterios 2-5, seccion 8 y tabla de riesgos. CONFIRMACION del residual que senalaste: los procs Get_*_List de P2-004 (Get_Availability_Certificate_List/Get_Commitment_List/Get_Obligation_List/Get_Payment_List) son BRECHA INTENCIONAL a CREAR por esa SPEC (BR-C3, sobre vistas de saldo existentes), NO cita de objeto existente -- asi que su ausencia en BD no es bloqueo. Verifica gates del hub verdes y re-verificacion readonly. Emite GO/NO-GO."
question: "GO o NO-GO sobre el lote NOVA-DEV re-gateado (fix-loop 1) de TASK-0246?"
---

# REVIEW - Re-juicio lote NOVA-DEV (TASK-0246, fix-loop 1)

Veredicto anterior CAMBIO-REQUERIDO con 2 bloqueantes, ambos remediados en commit 9b5563c (doc-only):

- **F-0246-01 (q4_membership):** agregado al preambulo de las 3 SPECs que lo omitian. P3-001 = FUERA
  (opener de la familia, alcance congelado, no enumerada en el pool Q4). P3-002 y P3-003 = CONDICIONAL
  (criticidad media; entran al pool Q4 si su DEC esta cerrada al sello de Etapa 2). Consistente con el
  estudio y con el campo ya presente en P3-004/P3-005/P4-004.

- **F-0246-02 (THROW de Apply_Obligation_Adjustment):** P4-004 ahora cita la definicion REAL que
  verificaste readonly: efecto distinto de reintegro (effect_code != counter_credit) = **50265** (antes
  50256, erroneo); tope obligacion-pagado = **50264**; rango de linea 50252/50253/50255 (retirado 50254).
  El campo 5 declara el set real completo y que el proc NO emite 50254/50256 (leccion F-NOVA-01: citar la
  definicion del proc, no la familia generica de PRES-03). Corregidos restricciones 6b/6c/6d/6g,
  criterios de aceptacion 2-5, seccion 8 (integracion) y la tabla de riesgos.

Residual confirmado: los Get_*_List de P2-004 son objetos a CREAR (BR-C3), no citas de existencia -> no
bloqueante, como anticipaste.

Fix-loop 1 de 2. Si aun ves un bloqueante real, remedio la iteracion 2 antes de escalar al Operador. rr=true.
