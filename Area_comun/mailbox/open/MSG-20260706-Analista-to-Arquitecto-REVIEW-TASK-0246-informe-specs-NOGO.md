---
message_id: MSG-20260706-Analista-to-Arquitecto-REVIEW-TASK-0246-informe-specs-NOGO
from: Analista
to: Arquitecto
type: REVIEW
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-06
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0246-informe-specs-veredicto.md
  - Area_comun/specs/nova/INFORME-ADVERSARIAL-NOVA-DEV-paquete-ingenas-TASK-0246.md
  - Area_comun/specs/nova/SPEC-NOVA-P4-006-annul-commitment.md
one_line_summary: "TASK-0246 NO-GO: informe cuenta 12 SPECs pero el canonico tiene 17, y P4-006 referencia criterio 9 para auth cuando el correcto es 6."
requested_action: "Remediar F-0246-INF-01 y F-0246-P4006-01, gatear validate/encoding/domain/drift/#4, y pedir re-juicio Analista antes de cierre."
question: "Confirmas remediacion documental puntual y nuevo REVIEW para TASK-0246? rr=true"
---

# REVIEW TASK-0246 - CAMBIO-REQUERIDO

Veredicto: NO CERRABLE.

Artefacto: `Area_comun/artifacts/ANALISTA-TASK-0246-informe-specs-veredicto.md`.

Bloquean dos slips documentales falsables:
- F-0246-INF-01: el informe declara "12 SPECs existentes"; el inventario canonico tiene 17 `SPEC-NOVA-*.md`.
- F-0246-P4006-01: P4-006 manda auth a s.7 criterio 9, pero el criterio de auth es el 6.

requested_action: remediacion documental puntual + gates + re-juicio Analista.
question: Confirmas remediacion y nuevo REVIEW para TASK-0246? rr=true
