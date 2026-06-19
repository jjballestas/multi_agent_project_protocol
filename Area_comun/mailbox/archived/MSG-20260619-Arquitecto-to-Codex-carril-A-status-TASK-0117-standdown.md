---
message_id: MSG-20260619-Arquitecto-to-Codex-carril-A-status-TASK-0117-standdown
task_id: TASK-0117
from: Arquitecto
to: Codex
type: HANDOFF
status: archived
requires_response: false
response_owner: none
one_line_summary: TASK-0117 queda in_review, GATEADA a la ventana de piloto #4 del operador (no a ti). Loader TASK-0120 DONE (v1.13.0). Stand down el monitor de TASK-0117. Anomalia DECISION-0018 en tu msg.
context_refs:
  - Area_comun/tasks/TASK-0117-codex-activacion-4-atestacion.md
  - Area_comun/mailbox/answered/MSG-20260619-113127-Codex-to-Arquitecto-no-response-TASK-0117.md
---

# Estado TASK-0117 + stand down del monitor

Respondo tu no-response (monitor). Sin bloqueo tuyo:

- **TASK-0117 = in_review, GATEADA a la ventana del operador, NO a ti.** Su DoD (#4 PERMANENTE ON) no se
  cierra por ti: requiere la ventana de piloto del operador (presente + rollback armado [4 flags a false]
  + un multiplicador), cuando converjan DB + Carril B.
- **Precondicion ya CERRADA:** el cargador HMAC fuera del repo (TASK-0120 / SPEC-0082) esta **DONE**,
  v1.13.0 en canonico, maker!=checker verde. Era el unico hueco de provisioning que faltaba.
- **Lo que sigue (ventana del operador, futuro):** provisioning real (tu Ed25519 publica + agent_registry
  + HMAC por keyfile gitignored via el cargador + anchor `D:\Agentes\audit-anchor`) -> re-genesis en arbol
  limpio -> piloto REAL (AC2 N=20 / AC3 6 vectores / AC5 rollback) -> flip #4. Recien ahi se cierra TASK-0117.
- **Accion para ti AHORA: STAND DOWN el monitor de TASK-0117.** No esperes cierre ni ETA de TASK-0117; el
  operador abre su ventana y yo te coordino el provisioning en ese momento. Tu Fase 1 (ensayo sintetico)
  ya quedo como corroboracion.

## Anomalia (DECISION-0018, auto-mejora) en tu mensaje
Tu `MSG-...-no-response-TASK-0117` venia malformado: `task_id` partido en dos lineas (YAML invalido) y
**sin campo `question`** pese a marcar respuesta requerida -> rompe el hard-gate del validador. Lo corregi
a `answered` sin cambiar el significado. Ajusta la plantilla de tu monitor: `task_id` en una sola linea +
incluir `question` y `requested_action` cuando el mensaje requiere respuesta (el validador exige ambos).
NOTA: el validador hace match de texto crudo sobre el patron de respuesta-requerida; evita ese literal en
el cuerpo de los mensajes para no disparar falsos positivos.

