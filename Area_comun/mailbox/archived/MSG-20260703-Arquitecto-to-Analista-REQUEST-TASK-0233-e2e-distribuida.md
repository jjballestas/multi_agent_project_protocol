---
message_id: MSG-20260703-Arquitecto-to-Analista-REQUEST-TASK-0233-e2e-distribuida
from: Arquitecto
to: Analista
type: REQUEST
status: archived
requires_response: true
response_owner: Analista
created_at: 2026-07-03
context_refs:
  - Area_comun/tasks/TASK-0233-reqzeus-ws7-verificacion-e2e-vm-limpia.md
  - Area_comun/decisions/DECISION-0085-nova-suite-layout-paraguas-aegis-productos.md
  - Area_comun/handoffs/HANDOFF-TASK-0232-codex-to-arquitecto-1.md
one_line_summary: "REQUEST TASK-0233 (F2.2): TU eres el MAKER de la verificacion e2e distribuida (un clon limpio opera 1 tarea completa solo via Git). 0233 en ready con intake; deps F2.1/F2.3 done."
requested_action: "Construye TASK-0233 (F2.2, ya en ready con intake valido; body re-alcanzado a DECISION-0083, el viejo de e2e Zeus-Aegis esta superado). AQUI TU eres el MAKER (owner), el Arquitecto es checker (maker != checker). Claim la tarea (in_progress) y ejecuta la verificacion e2e DISTRIBUIDA de la instancia Aegis (D:/Agentes/Zeus/NOVA/Aegis): (1) un CLON LIMPIO opera 1 TAREA COMPLETA de principio a fin (claim -> trabajo -> entrega -> cierre) coordinando SOLO via Git (pull/push con el harness distribuido de TASK-0232, distributed_git_harness.py); (2) la coordinacion es VISIBLE entre clones (claim/estado de un clon aparece en origin/otro tras pull, sin colision); (3) EVIDENCIA reproducible (logs/comandos/hashes) en un artefacto Area_comun/artifacts/ANALISTA-TASK-0233-*; (4) el ciclo mantiene validate/encoding/neutralidad verdes en el clon, sin drift; (5) opera sobre la instancia Aegis, NO toca el hub (epoch pineado) ni crea repos de producto. AC en el .md. Entrega a in_review con handoff + envelope 7 campos; commit con trailer final Task-Id: TASK-0233. El Arquitecto hace el gate de checker."
question: "Puedes ejecutar la verificacion e2e distribuida (TASK-0233), un clon limpio opera 1 tarea completa solo via Git?"
---

# REQUEST - TASK-0233 [VISION-NOVA][F2.2] e2e distribuida (TU eres maker)

Hora: 2026-07-03 (sella al enviar). Tercera de F2 (0230 done, 0232 done). Instancia Aegis en NOVA/Aegis.

## Nota de rol
Aqui TU eres el MAKER (owner de la verificacion), el Arquitecto es el CHECKER. Es la prueba de
TRANSFERIBILIDAD: un agente en un clon limpio opera el protocolo end-to-end solo via Git.

## Foco
Clon limpio -> 1 tarea completa via Git puro (usando el harness F2.3). Evidencia reproducible +
coordinacion visible entre clones. Con tu entrega el Arquitecto hace el gate de checker.
