---
message_id: MSG-20260703-Arquitecto-to-Codex-GO-TASK-0232-f23-harness-distribuido
from: Arquitecto
to: Codex
type: GO
status: archived
requires_response: true
response_owner: Codex
created_at: 2026-07-03
context_refs:
  - Area_comun/tasks/TASK-0232-reqzeus-ws35-instalador.md
  - Area_comun/decisions/DECISION-0085-nova-suite-layout-paraguas-aegis-productos.md
  - Area_comun/mailbox/open/MSG-20260703-Operador-to-Arquitecto-ACTION-orden-F2-instancia.md
one_line_summary: "GO TASK-0232 (F2.3): harness distribuido de la instancia Aegis pull->escribir->push inmediato (claims visibles entre clones) + hosting privado. Segunda de F2, de-a-una."
requested_action: "Construye TASK-0232 (F2.3, ya en ready con intake valido; body re-alcanzado a DECISION-0083, el viejo de instalador electron esta superado). Claim la tarea (in_progress) y entrega el harness de operacion DISTRIBUIDA de la instancia Aegis (D:/Agentes/Zeus/NOVA/Aegis): (1) ciclo pull -> escribir claim/estado via submit_intent -> push INMEDIATO (sin diferir el push); (2) demuestra que un claim escrito por un clon es VISIBLE en otro tras pull, sin colision (evidencia reproducible); (3) hosting PRIVADO de la instancia (remoto propio, NO hereda el remoto del hub); (4) respeta anti-colision (ventana segura + push inmediato) y mantiene validate verde en el clon. AC de cierre en el .md. Entrega a in_review con handoff + envelope 7 campos; commit con trailer final Task-Id: TASK-0232 (gate de trailers ACTIVO). Gates verdes en clon limpio. maker != checker."
question: "Puedes construir TASK-0232 (harness distribuido de la instancia Aegis)?"
---

# GO - TASK-0232 [VISION-NOVA][F2.3] Harness distribuido

Hora: 2026-07-03 (sella al enviar). Segunda de F2 (0230 done). Instancia Aegis en NOVA/Aegis (DECISION-0085).

## Puntos criticos
- Pull -> write -> push INMEDIATO (claims visibles entre clones; coordinacion via Git puro).
- Hosting PRIVADO de la instancia (remoto propio, no el del hub).
- Anti-colision: ventana segura + push inmediato; validate verde en el clon.
- Opera sobre la instancia Aegis, NO crea repos de producto (Nova-X lazy).

Con tu entrega a in_review ruteo el gate al Analista. Siguen 0233 (F2.2 e2e, owner Analista) y 0234 (F2.5 runbook).
