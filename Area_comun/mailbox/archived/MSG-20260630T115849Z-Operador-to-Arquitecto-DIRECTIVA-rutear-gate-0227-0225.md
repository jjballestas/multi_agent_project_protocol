---
message_id: MSG-20260630T115849Z-Operador-to-Arquitecto-DIRECTIVA-rutear-gate-0227-0225
task_id: OPS-ROUTE-GATE-20260630
type: DIRECTIVE
from: Operador
to: Arquitecto
status: archived
requires_response: true
response_owner: Arquitecto
operator_directive: true
created_at: 2026-06-30T11:58:49Z
context_refs:
  - Area_comun/mailbox/open/MSG-20260630-Codex-to-Arquitecto-TASK-0227-in-review.md
  - Area_comun/mailbox/open/MSG-20260630-Codex-to-Arquitecto-TASK-0225-remediation-2-in-review.md
question: "Ruteadas TASK-0227 y TASK-0225 (remediacion-2) al gate adversarial del Analista? Confirmar con los REVIEW emitidos."
requested_action: "Rutear al gate adversarial del Analista las dos entregas in_review: TASK-0227 (boundary F1, entrega 9e0206e) y TASK-0225 (remediacion-2, entrega 8385868). Emitir un REVIEW Arquitecto->Analista por cada una (type REVIEW, response_owner Analista, requested_action no vacio, ASCII). El Analista reproduce desde clon limpio de HEAD y emite veredicto GO/NO-GO con artefacto en Area_comun/artifacts; cerrar via submit_intent segun resultado. maker(Codex) != checker(Analista)."
one_line_summary: "Operador ordena rutear TASK-0227 (boundary F1) y TASK-0225 (remediacion-2) al gate adversarial del Analista."
---

Directiva del Operador al Arquitecto.

CONTEXTO
- Ambas estan in_review y entregadas por Codex (maker):
  - TASK-0227 boundary F1 -> entrega 9e0206e (MSG Codex-to-Arquitecto-TASK-0227-in-review).
  - TASK-0225 cron, remediacion-2 -> entrega 8385868 "repair ws snapshot classifier"
    (MSG Codex-to-Arquitecto-TASK-0225-remediation-2-in-review). Cierra el NO-GO previo del Analista
    (Get-WsSnapshot filtraba por project).

ORDEN
1) Emitir REVIEW Arquitecto->Analista por cada tarea (type REVIEW; el cron del Analista NO acepta "GO"):
   - response_owner: Analista; requested_action concreto; ASCII puro; gatear el propio mensaje
     (validate_collaboration_state.py exit 0 + scan_encoding.py exit 0) antes de soltarlo.
   - Pista de redaccion: no combinar un verbo de corte con nombres de cron/monitor o de los peers en una
     misma linea (footgun de auto-corte del cron del Analista).
2) El Analista reproduce desde clon limpio de HEAD, conteos/gates verdes por exit-code, emite veredicto
   GO/NO-GO con artefacto en Area_comun/artifacts.
3) Cierre via submit_intent segun el veredicto (in_review -> review_approved o changes_requested),
   liberando el claim correspondiente. maker(Codex) != checker(Analista).
4) Commitea el saneamiento ANTES de pedir el review (HEAD verde en clon limpio).

Reportar con los dos REVIEW emitidos + ETA del gate.
