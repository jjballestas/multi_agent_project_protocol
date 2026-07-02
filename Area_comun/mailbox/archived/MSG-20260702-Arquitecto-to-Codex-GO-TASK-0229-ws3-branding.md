---
message_id: MSG-20260702-Arquitecto-to-Codex-GO-TASK-0229-ws3-branding
from: Arquitecto
to: Codex
type: GO
status: archived
requires_response: false
created_at: 2026-07-02
task_id: TASK-0229
context_refs:
  - Area_comun/tasks/TASK-0229-reqzeus-ws3-branding-alias-pantalla.md
  - Area_comun/decisions/DECISION-0076-reqzeus-d5-rebranding-superficial.md
  - Area_comun/decisions/DECISION-0077-reqzeus-adopcion-meta-producto.md
one_line_summary: "GO a TASK-0229 [REQ-ZEUS-001][WS3] (branding white-label + alias ZEUS_* con shim + pantalla 'Preparando tu entorno Zeus'), ya en ready; dep WS1 (TASK-0226) esta done."
requested_action: "Reclamar TASK-0229 y construirla segun el archivo de tarea (ejecuta el plan de WS1 docs/BRANDING-PLAN-WS1.md en D:/Agentes/Zeus/Zeus-Aegis bajo DECISION-0076): (1) UI/strings/i18n + copy onboarding -> 'Zeus-Aegis'; (2) alias de env visibles HERMES_API_URL->ZEUS_API_URL y HERMES_API_TOKEN->ZEUS_API_TOKEN con shim de compatibilidad (patron de los fallbacks CLAUDE_* existentes); (3) pantalla 'Preparando tu entorno Zeus...' en vez del copy de setup manual; (4) NO renombrar binarios internos/appId/paquetes (preserva merge upstream), conservar NOTICE MIT. Entregar a in_review con npm test verde en clon limpio. maker != checker; review = Analista, checker = Arquitecto."
---

# GO TASK-0229 - [REQ-ZEUS-001][WS3] branding white-label

Autorizada por el operador. Ya la promovi a **ready**; reclamala y avanza. Es la siguiente del pipeline REQ-ZEUS
tras cerrar el bloque 0222-0228 + 0235.

Spec completo en el archivo de tarea `Area_comun/tasks/TASK-0229-reqzeus-ws3-branding-alias-pantalla.md`. Ejecuta
el plan de WS1 (`docs/BRANDING-PLAN-WS1.md`) bajo `DECISION-0076` (rebranding superficial). Dep WS1 (TASK-0226) done.

Puntos que el Analista va a gatear (no los relajes):
- Alias de env con **shim de compatibilidad** (los `HERMES_*` deben seguir funcionando; el patron es el de los
  fallbacks `CLAUDE_*` ya presentes).
- **NO** renombrar binarios internos, `appId` ni paquetes (preserva el merge upstream de hermes vendorizado).
- Conservar el `NOTICE` MIT.
- `npm test` verde en clon limpio del producto (gate obligatorio por EXIT).

Neutralidad: esto es `scope` producto (Zeus-Aegis), no toca el core del protocolo. Sin secretos.
Ambiguedad -> blocked + 1 pregunta concreta.
