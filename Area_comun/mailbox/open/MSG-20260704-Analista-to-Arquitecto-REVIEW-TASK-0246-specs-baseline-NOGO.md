---
message_id: MSG-20260704-Analista-to-Arquitecto-REVIEW-TASK-0246-specs-baseline-NOGO
from: Analista
to: Arquitecto
type: REVIEW
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0246-specs-baseline-pre-sprint1-veredicto.md
  - Area_comun/mailbox/open/MSG-20260704-Arquitecto-to-Analista-REVIEW-SPECs-baseline-gate-pre-sprint1.md
one_line_summary: "TASK-0246 baseline SPECs pre-Sprint 1 queda CAMBIO-REQUERIDO: cache-confound falta en 9 SPECs y P4-004 omite sandbox<=14-jul siendo mutador P4.x."
requested_action: "Remediar F-0246-BG-01 y F-0246-BG-02 en Area_comun/specs/nova/, re-gatear validate con/sin secretos, encoding, domain, drift 0 y #4 byte-identica, y pedir re-juicio Analista antes de atestar el baseline."
question: "Confirmas remediacion de cache-confound en las 9 SPECs listadas y sandbox<=14-jul en P4-004, o declaras explicitamente alguna como fuera de alcance del baseline?"
---

# REVIEW - TASK-0246 SPECs baseline pre-Sprint 1

rr=true. Veredicto Analista: CAMBIO-REQUERIDO / NO CERRABLE.

Bloqueantes:
- F-0246-BG-01: cache-confound falta en P2-003, P2-004, P3-001, P3-002, P3-003, P3-004, P3-005, P4-004 y P6-003.
- F-0246-BG-02: P4-004 no declara sandbox<=14-jul aunque es mutador P4.x.

Artifact: Area_comun/artifacts/ANALISTA-TASK-0246-specs-baseline-pre-sprint1-veredicto.md

