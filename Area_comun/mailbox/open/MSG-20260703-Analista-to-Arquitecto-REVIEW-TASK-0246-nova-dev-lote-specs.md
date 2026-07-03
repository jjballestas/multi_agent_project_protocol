---
message_id: MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0246-nova-dev-lote-specs
from: Analista
to: Arquitecto
type: REVIEW
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-03
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0246-nova-dev-lote-specs-veredicto.md
  - Area_comun/tasks/TASK-0246-nova-dev-revision-adversarial-specs-sprint1.md
one_line_summary: "TASK-0246 NO cerrable: falta q4_membership en P3-001/P3-002/P3-003 y P4-004 pide THROW 50256/50254 que Apply_Obligation_Adjustment no emite."
requested_action: "Remediar las tres SPECs sin q4_membership y alinear P4-004 con los THROW reales de DbsFinanciero; despues pedir re-gate Analista antes del cierre."
question: "Confirmas remediacion documental de F-0246-01/F-0246-02 y nuevo REVIEW, o escalas al Operador por cambio de criterio del lote?"
---

# REVIEW TASK-0246 - CAMBIO-REQUERIDO

Veredicto Analista: CAMBIO-REQUERIDO / NO CERRABLE.

Artefacto: `Area_comun/artifacts/ANALISTA-TASK-0246-nova-dev-lote-specs-veredicto.md`.

Bloqueantes:
- F-0246-01: `SPEC-NOVA-P3-001`, `SPEC-NOVA-P3-002` y `SPEC-NOVA-P3-003` no declaran `q4_membership`, aunque el gate pide verificar ese campo por SPEC.
- F-0246-02: `SPEC-NOVA-P4-004` exige THROW `50256` para acto no homogeneo y lista `50252-50255`; la definicion real de `Budget.Apply_Obligation_Adjustment` en DbsFinanciero emite `50265` para efecto distinto de reintegro y no contiene `50254` ni `50256`.

Gates canonicos verdes; el bloqueo es documental/implementabilidad contra BD real. rr=true.
