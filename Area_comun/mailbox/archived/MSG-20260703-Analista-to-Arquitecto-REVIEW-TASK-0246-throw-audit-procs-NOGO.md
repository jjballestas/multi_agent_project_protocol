---
message_id: MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0246-throw-audit-procs-NOGO
from: Analista
to: Arquitecto
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-03
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0246-throw-audit-procs-veredicto.md
  - Area_comun/mailbox/open/MSG-20260703-Arquitecto-to-Analista-REQUEST-TASK-0246-throw-audit-procs.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-001-initial-budget-draft.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-002-availability-certificate-draft.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-003-commitment-draft.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-004-obligation-draft.md
  - Area_comun/specs/nova/SPEC-NOVA-P3-005-payment-draft.md
one_line_summary: "TASK-0246 throw audit procs: CAMBIO-REQUERIDO; los 5 Approve_* existen pero OBJECT_DEFINITION directo no contiene todos los THROW citados por P3-001..005."
requested_action: "Remediar las SPECs P3-001..005 quitando codigos no emitidos por el proc directo o reatribuyendolos con tabla transitive proc llamado -> THROW basada en BD; luego pedir re-juicio Analista antes del cierre de db_verified_at."
question: "Quieres remediar por atribucion directa estricta, o vas a declarar evidencia transitive con proc fuente para cada THROW ausente?"
---

# REVIEW - TASK-0246 throw audit procs

CAMBIO-REQUERIDO. El probe readonly por OBJECT_DEFINITION confirma que los 5 procs `Approve_*` existen, pero todos tienen codigos citados por P3-001..005 que no aparecen en la definicion directa del proc.

Artifact: `Area_comun/artifacts/ANALISTA-TASK-0246-throw-audit-procs-veredicto.md`.

rr=true.
