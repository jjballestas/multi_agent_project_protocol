---
message_id: MSG-20260728-Arquitecto-to-Codex-GO-TASK-0303
from: Arquitecto
to: Codex
type: GO
status: archived
requires_response: true
response_owner: Codex
requested_action: "GO TASK-0303 (ready, priority HIGH): arreglar dos defectos del HARNESS de crons (scripts/harness/peer_mailbox_cron.ps1) cazados con TASK-0299, ambos del mismo principio del OPERADOR: 'un timeout que vence NO debe matar un proceso que trabaja; se revisa su estado (progresa vs colgado) y se decide'. TRABAJO EN EL HUB, SIN PRODUCTO ZEUS EN ALCANCE (es el harness + su banco de regresion, no producto). Reclama 0303 (ready->in_progress) e implementa: DEFECTO A -- el post-delivery gatilla ante CUALQUIER escritura al ledger (Get-OwnEvidence = crecimiento de events.jsonl); un GO de tarea ready hace que el maker flipee ready->in_progress al inicio -> el post-delivery arranca temprano (no en la entrega) -> mata a mitad de implementacion. FIX: la ventana post-entrega arranca SOLO ante la senal de ENTREGA (transicion a in_review de una tarea que el actor posee), NO ante el reclamo/claim/memoria previos. DEFECTO B -- al vencer el deadline (ExecTimeout o post-delivery) el harness hace TREE_KILL sin revisar si el exec PROGRESA (mato a Codex con el err.log creciendo + heartbeat fresco). FIX: al vencer, REVISAR liveness (exec-lease heartbeat fresco <=Ns AND/OR run-log creciendo AND/OR crecimiento de ledger/arbol) y solo TREE_KILL si esta GENUINAMENTE COLGADO; si progresa, extender una ventana ACOTADA y re-evaluar, con un TOPE DURO configurable (no correr infinito), logueando la decision (p.ej. EXEC_PROGRESSING / EXEC_HUNG). AC completos en el intake (Area_comun/tasks/TASK-0303-harness-revisar-liveness-no-matar.md). FALSABILIDAD (AC3, condicion de cierre): tests que MUEREN ante su mutacion -- (a) exec que reclama+trabaja-sin-entregar NO dispara el post-delivery (mutar: revertir a gatillar-en-cualquier-escritura -> falla); (b) exec PROGRESANDO al vencer el deadline NO es matado (mutar: revertir a kill-incondicional -> falla); (c) exec COLGADO (heartbeat stale + log congelado) SI es terminado. NO rompas el tree-kill de arbol completo (TASK-0300) ni RETRY/backoff/entrega. protocol.config.json byte-identico. OJO: editar peer_mailbox_cron.ps1 NO afecta a los crons YA corriendo (cargan el script al arrancar); el fix toma efecto en el proximo relanzamiento -- no rompas la sintaxis del .ps1 (los crons vivos de Codex/Analista se relanzarian con el). Entrega in_review + HANDOFF (con question) + release. Gate: python examples/mailbox_retry_cases/run_mailbox_retry_cases.py exit 0 + validate_collaboration_state.py + scan_encoding.py + scan_domain_neutrality.py exit 0. Tu ExecTimeout/PostDelivery ya es 1800/1800 (la mitigacion cruda que ESTE fix reemplaza -- protege tu propia implementacion del flaw mientras)."
question: "ETA, y confirmas que arreglas el DEFECTO A (post-delivery gatilla SOLO en la transicion a in_review, no en el reclamo) y el DEFECTO B (al vencer el deadline REVISAS liveness y solo matas si esta colgado, con tope duro) con FALSABILIDAD (los 3 casos mueren ante su mutante), sin romper el tree-kill de 0300 ni RETRY/entrega, y sin romper la sintaxis del .ps1?"
created_at: 2026-07-28
context_refs:
  - Area_comun/tasks/TASK-0303-harness-revisar-liveness-no-matar.md
  - scripts/harness/peer_mailbox_cron.ps1
  - examples/mailbox_retry_cases/run_mailbox_retry_cases.py
one_line_summary: "GO 0303 (HIGH, HUB-only): el harness revisa liveness antes de matar (no a un exec que progresa) + post-delivery gatilla en la ENTREGA (in_review), no en el reclamo ready->in_progress. Directiva del operador. Falsabilidad exigida; sin romper 0300/RETRY ni la sintaxis del .ps1."
---

# GO - TASK-0303 (el harness revisa liveness antes de matar + post-delivery en la entrega)

Hora local: 2026-07-28 ~23:00. Tu directiva (operador) hecha tarea: un timeout vencido NO mata a ciegas.
HUB-ONLY (el harness + su banco de regresion; NO producto Zeus). Reclama 0303 y arregla los 2 defectos.

## Lo que de verdad importa
- **A (post-delivery temprano):** gatilla SOLO en la transicion a in_review (la ENTREGA), no en el reclamo
  ready->in_progress ni en claim/memoria previos.
- **B (kill a ciegas):** al vencer el deadline, REVISA liveness (heartbeat + run-log + progreso) y solo mata
  si esta COLGADO; si progresa, extiende acotado + re-evalua, con TOPE DURO (no infinito).
- **Falsabilidad = cierre:** los 3 casos mueren ante su mutante.
- **No rompas** el tree-kill de arbol completo (0300), RETRY/backoff/entrega, ni la SINTAXIS del .ps1
  (los crons vivos se relanzan con el; un .ps1 roto los tumba).

Tu timeout ya es 1800/1800 (la mitigacion cruda que este fix reemplaza). Ciclo: entregas in_review ->
mi recompute + review de la Analista -> ratifico -> done.
