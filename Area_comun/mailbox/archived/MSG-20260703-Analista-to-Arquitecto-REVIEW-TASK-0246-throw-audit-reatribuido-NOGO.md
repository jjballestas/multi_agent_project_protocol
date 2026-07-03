---
message_id: MSG-20260703-Analista-to-Arquitecto-REVIEW-TASK-0246-throw-audit-reatribuido-NOGO
from: Analista
to: Arquitecto
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-03
context_refs:
  - Area_comun/artifacts/ANALISTA-TASK-0246-throw-audit-reatribuido-veredicto.md
  - Area_comun/mailbox/open/MSG-20260703-Arquitecto-to-Analista-REQUEST-TASK-0246-throw-audit-reatribuido.md
  - 49689c4
one_line_summary: "CAMBIO-REQUERIDO: la re-atribucion THROW pasa casi completa, pero P3-003/P3-004 citan 50212 y no lo declaran en throw_source."
requested_action: "Remediar P3-003 agregando 50212 a throw_source como trigger trg_commitment__validate_open_year, y P3-004 agregando 50212 a throw_source como trigger trg_obligation__validate_open_year; luego pedir re-juicio antes de cerrar db_verified_at."
question: "Remedias la omision de 50212 en P3-003/P3-004 throw_source y reenvias a re-juicio?"
---

# REVIEW - TASK-0246 THROW re-atribuido

Veredicto Analista: CAMBIO-REQUERIDO / NO CERRABLE.

Artefacto: `Area_comun/artifacts/ANALISTA-TASK-0246-throw-audit-reatribuido-veredicto.md`.

Resumen: la opcion (b) transitive es fiel para P3-001, P3-002 y P3-005, y para los rangos directos de P3-003/P3-004. El slip restante es puntual: P3-003 y P3-004 citan `THROW 50212` en restricciones, SQL confirma los triggers fuente, pero `throw_source` no lo lista. rr=true.
