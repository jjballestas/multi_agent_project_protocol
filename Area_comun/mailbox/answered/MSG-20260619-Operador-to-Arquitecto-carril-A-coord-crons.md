---
message_id: MSG-20260619-Operador-to-Arquitecto-carril-A-coord-crons
type: INFO
task_id: COORD-20260619-CARRIL-A-REVERIFY
from: Operador
to: Arquitecto
status: answered
answered_by: MSG-20260619-Arquitecto-to-Operador-carril-A-promocion-done
requires_response: true
response_owner: Arquitecto
one_line_summary: Coordinacion de crons Carril A. NO detengas el cron de Codex mientras quede trabajo de implementacion (SPEC-0081 + A3). El GO de promocion sigue vivo en open/ esperando que promuevas.
requested_action: Promover los 4 drafts (GO ya dado); mantener a Codex ACTIVO mientras quede trabajo de Carril A; no detener su cron ni el tuyo hasta aviso explicito del operador/asistente.
question: Confirmas promocion hecha (ids/version/CHANGELOG/drift 0) y que dejas a Codex activo para la implementacion de SPEC-0081?
context_refs:
  - Area_comun/mailbox/open/MSG-20260619-Operador-to-Arquitecto-carril-A-GO-promocion.md
---

# Coordinacion de crons - Carril A

Arquitecto, dos cosas:

1. PROMOCION PENDIENTE. El GO de promocion (MSG ...GO-promocion en open/) sigue vivo y sin ejecutar:
   version aun 1.9.3, DECISION-0039/0040/0041 + SPEC-0081 no estan en el ledger. Promueve por
   submit_intent cuando puedas (SemVer MINOR + CHANGELOG, drift 0) y reporta ids finales/version.

2. CRONS - ORDEN DEL OPERADOR. Mientras quede trabajo de Carril A NO detengas a Codex:
   - Codex tiene trabajo PENDIENTE despues de la promocion: implementar SPEC-0081 (provisioning de
     event_auth.keys + public_keys por agente + anclaje remoto/proof; construir attestation_health_cases
     y los 6 goldens negativos de AC3; smoke de provisioning) y la prueba negativa de A3 (escritura al
     Core rechazada por el SO).
   - Por tanto: NO ordenes a Codex detener su cron, y NO detengas el tuyo, hasta que el operador/asistente
     te avise explicitamente que el trabajo de Carril A de Codex esta cerrado.
   - El asistente (coordinando en nombre del operador) te dara la senal de "Codex puede parar" cuando esa
     lista este verde, y la de "puedes detener tu cron" al cierre de la fase.

Analista queda en stand-down (no se necesita en esta fase de implementacion). Canal ASCII.
