---
message_id: MSG-20260703-Operador-to-Arquitecto-ACTION-TASK-0230-ruta-real-handoff
from: Operador
to: Arquitecto
type: ACTION
status: open
requires_response: false
created_at: 2026-07-03
context_refs:
  - Area_comun/handoffs/HANDOFF-TASK-0230-codex-to-arquitecto-1.md
  - Area_comun/tasks/TASK-0230-reqzeus-ws2-bootstrapper.md
one_line_summary: "Ratifico la ruta de la instancia F2.1: D:/Agentes/Zeus/NOVA/nova-budget (anidada, se queda asi). El handoff de 0230 la lista como Zeus/nova-budget (stale) -> corregir a la ruta real antes/durante el review del Analista; NO reubicar."
requested_action: "[DIRECTIVA] (1) La instancia nova-budget se queda donde esta: D:/Agentes/Zeus/NOVA/nova-budget (anidada dentro de NOVA). El Operador RATIFICA la ruta -- NO reubicar, NO aplanar. (2) ANOMALIA (DECISION-0018): el HANDOFF-TASK-0230-codex-to-arquitecto-1.md lista los artefactos bajo D:/Agentes/Zeus/nova-budget (sin el segmento NOVA); la ruta REAL en disco es D:/Agentes/Zeus/NOVA/nova-budget/ (verificado: .agents/{Codex,Arquitecto,Analista}/config.json, .claude/settings.json, instance.profile.json presentes ahi; el path Zeus/nova-budget NO existe). El bootstrapper new-instance.mjs vive en D:/Agentes/Zeus/Zeus-protocol (commit e7c6da4). (3) Que Codex (owner del handoff) corrija los paths del handoff a la ruta real ANTES de que cierre el review; y que el gate del Analista valide la instancia contra D:/Agentes/Zeus/NOVA/nova-budget (no contra el path stale, que daria 'no existe'). [RECOMENDACION] Verificar tambien que instance.profile.json y los .agents/*/config.json referencien la ruta real, no la stale, para que el harness distribuido (F2.3/0232) apunte bien."
question: ""
---

# ACTION - Ruta real de la instancia F2.1 + handoff stale (TASK-0230)

El Operador ratifica: la instancia F2.1 se queda en **D:/Agentes/Zeus/NOVA/nova-budget**
(anidada). No reubicar, no aplanar.

Anomalia a corregir antes de aprobar 0230: el handoff de Codex lista la ruta como
`D:/Agentes/Zeus/nova-budget` (sin `NOVA`), pero esa carpeta NO existe; la instancia
real esta en `D:/Agentes/Zeus/NOVA/nova-budget/` (verificado en disco: `.agents/`
con los 3 config.json, `.claude/settings.json`, `instance.profile.json`). El
bootstrapper `new-instance.mjs` esta en `D:/Agentes/Zeus/Zeus-protocol` (e7c6da4).

Que Codex actualice los paths del handoff a la ruta real y que el Analista gatee
contra ella. Es un mismatch de texto/evidencia, no una reubicacion.

Firmado: Operador (John Ballestas), via asesor con autoridad delegada por escrito (2026-07-02).
