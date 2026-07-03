---
message_id: MSG-20260704-Operador-to-Arquitecto-REQUEST-asiento-coordinacion-build-nova
from: Operador
to: Arquitecto
type: REQUEST
status: archived
requires_response: true
response_owner: Arquitecto
created_at: 2026-07-04
context_refs:
  - Area_comun/decisions/DECISION-0050-repos-arquitectura-acoplamiento.md (governance en el hub)
  - Area_comun/decisions/DECISION-0085-nova-suite-layout-paraguas-aegis-productos.md (NOVA/Aegis instancia + Nova-X productos)
  - Area_comun/specs/nova/ (SPECs viven hoy en el HUB)
one_line_summary: "Clarificacion de arquitectura para el workflow del Operador: el CODIGO va en NOVA/Nova-Budget (settled) y el ESTUDIO se queda en el HUB (settled); pero para la COORDINACION del build de Nova (claims/tasks/mailbox/GOs de GOAL-P1 + SPECs Sprint 1), cual es el asiento de gobernanza del Operador -- el HUB o la instancia distribuida NOVA/Aegis (F2)?"
requested_action: "[REQUEST] Clarificacion de arquitectura (tu dominio, DECISION-0050/0085), para fijar el workflow de VS Code del Operador. SETTLED (no es la pregunta): (1) el CODIGO de producto va en NOVA/Nova-Budget (repo propio, LAZY) -> el Operador abre ese repo para escribir/revisar codigo; (2) el ESTUDIO (sello, medicion, corpus TFM-medicion, ledger #4) se queda en el HUB. LA PREGUNTA FINA: para la COORDINACION del BUILD de Nova (los claims / tasks / mailbox / GOs del trabajo de PRODUCTO: GOAL-P1 y luego las SPECs del Sprint 1), cual es el ASIENTO de gobernanza del Operador -- (a) el HUB multi_agent_project_protocol (donde HOY viven Area_comun/specs/nova/ + el sello + el ledger #4 atestado), o (b) la instancia distribuida NOVA/Aegis que construiste en F2 (governance/coordinacion/atestacion propia del equipo Nova via Git)? Definir esto fija en que carpeta de GOBERNANZA se sienta el Operador para coordinar el build (aparte de Nova-Budget para el codigo; sin multi-root, per DECISION-0050). Si la respuesta es (b) NOVA/Aegis: aclara como se relaciona con el HUB (donde el estudio se queda) -- si la coordinacion del build MIGRA a Aegis, se mantiene DUAL (estudio en hub / build en Aegis), y como cruzan la atestacion. Responde con la regla clara + cualquier ajuste/nota a DECISION-0050/0085 si hace falta. NO urge para GOAL-P1 inmediato (hoy se coordina desde el hub, que funciona), pero conviene fijarlo antes de que escale a varios modulos."
question: "Para coordinar el BUILD de producto de Nova (GOAL-P1 + SPECs Sprint 1), el asiento de gobernanza del Operador es el HUB o la instancia NOVA/Aegis? Si es Aegis, como se relaciona con el estudio que se queda en el hub?"
---

# REQUEST - Asiento de coordinacion del build de Nova (hub vs instancia Aegis)

El Operador esta fijando su workflow de VS Code. Settled: codigo en NOVA/Nova-Budget; estudio (sello/
medicion/#4) en el HUB. Pregunta fina para ti (DECISION-0050/0085):

**Para coordinar el BUILD de producto de Nova (claims/tasks/mailbox/GOs de GOAL-P1 + SPECs Sprint 1),
el asiento de gobernanza del Operador es el HUB o la instancia distribuida NOVA/Aegis (F2)?**

- Si HUB: se mantiene todo donde esta hoy (SPECs en Area_comun/specs/nova/, coordinacion en el mailbox del hub).
- Si NOVA/Aegis: aclara como se relaciona con el HUB (el estudio se queda en el hub), si la coordinacion
  del build migra a Aegis o queda dual, y como cruza la atestacion.

No urge para GOAL-P1 (hoy se coordina desde el hub, funciona); conviene fijarlo antes de escalar a varios
modulos. Responde con la regla + ajuste a 0050/0085 si aplica.
