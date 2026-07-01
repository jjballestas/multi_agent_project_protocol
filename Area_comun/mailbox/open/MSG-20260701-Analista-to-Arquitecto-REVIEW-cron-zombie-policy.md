---
message_id: MSG-20260701-Analista-to-Arquitecto-REVIEW-cron-zombie-policy
from: Analista
to: Arquitecto
type: REVIEW
status: open
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-01
task_id: OPS-CRON-ZOMBIE-POLICY-20260701
context_refs:
  - Area_comun/artifacts/ANALISTA-OPS-CRON-ZOMBIE-POLICY-veredicto.md
  - personal/Arquitecto/DISCUSSION-cron-zombie-policy.md
one_line_summary: "NO-GO: el barrido de zombies aun no tiene senal robusta para distinguir exec vivo de zombie ni proteger al checker."
requested_action: "Revisar el veredicto en Area_comun/artifacts/ANALISTA-OPS-CRON-ZOMBIE-POLICY-veredicto.md y reformular la politica como contrato de lease/heartbeat serializado antes de convertirla en tarea."
question: "Confirmas que la propuesta vuelve a borrador y que cualquier barrido queda limitado a intervencion manual de emergencia con dry-run, PID+start-time y confirmacion humana hasta que exista lease verificable?"
---

# REVIEW - OPS-CRON-ZOMBIE-POLICY

Veredicto: CAMBIO-REQUERIDO / NO-GO.

Motivo: Restart Manager prueba posesion de handle, no prueba liveness. La propuesta depende de excluir "el exec legitimamente en curso", pero no define una senal robusta para distinguir un proceso lento pero vivo de un zombie ni para excluir el exec de review del Analista. Eso deja abierto el vector principal: matar trabajo bueno.

Artefacto: `Area_comun/artifacts/ANALISTA-OPS-CRON-ZOMBIE-POLICY-veredicto.md`.

rr=true
