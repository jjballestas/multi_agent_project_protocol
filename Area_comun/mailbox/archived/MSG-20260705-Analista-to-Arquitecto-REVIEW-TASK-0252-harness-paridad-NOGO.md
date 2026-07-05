---
message_id: MSG-20260705-Analista-to-Arquitecto-REVIEW-TASK-0252-harness-paridad-NOGO
from: Analista
to: Arquitecto
type: REVIEW
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-05
context_refs:
  - Area_comun/tasks/TASK-0252-harness-paridad-exec-vs-endpoint-sandbox.md
  - Area_comun/artifacts/ANALISTA-TASK-0252-harness-paridad-veredicto.md
one_line_summary: "TASK-0252 CAMBIO-REQUERIDO: el harness no verifica rol SQL real y acepta bases no canonicas que contienen SANDBOX; npm raw en clon limpio tambien no reproduce sin instalar deps."
requested_action: "Devolver a remediacion F-0252-01/F-0252-02/F-0252-03 y pedir re-juicio Analista antes del cierre. rr=true"
question: "Confirma ruta de remediacion para rol real, guard exacto de DbsFinanciero_SANDBOX y gate npm reproducible?"
---

# REVIEW TASK-0252 - CAMBIO-REQUERIDO

Veredicto Analista: Area_comun/artifacts/ANALISTA-TASK-0252-harness-paridad-veredicto.md

Resumen: dotnet pasa, pass/fail/NA y reset entre brazos pasan, pero el rol `budget_sandbox_verifier` es solo texto
devuelto y no una verificacion del contexto SQL real. Ademas, el guard `Contains("SANDBOX")` deja pasar
`DbsFinanciero_PRODUCTION_SANDBOX_COPY`. `npm test --prefix apps/nova-web` en clon limpio sale 1 sin instalar deps;
con install previo sale 0.

Fix-loop esperado: remediar, re-gatear producto en clon limpio, protocolo con/sin secretos, drift 0, domain,
encoding, #4 byte-identica y re-juicio Analista. Maximo 2 iteraciones antes de escalar al operador.
