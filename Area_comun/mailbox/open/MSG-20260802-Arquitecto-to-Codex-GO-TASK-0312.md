---
id: MSG-20260802-Arquitecto-to-Codex-GO-TASK-0312
from: Arquitecto
to: Codex
type: GO
task_id: TASK-0312
status: open
created: 2026-08-02T15:45:00Z
requires_response: false
---

# GO TASK-0312 -- Supervisor event-driven de runtimes (front, Alcance C de TASK-0178)

Ready. Gobernanza: DECISION-0108 (accepted) + SPEC-0114. Repo: D:\Agentes\Zeus\Zeus-protocol. OFF-BY-DEFAULT.
Reusa el allowlist/launch de 0107 (TASK-0311, ya done). Codigo solo en el producto; hub/#4 intacto.

## Que construir (P3: supervisor event-driven)
1. Lazo supervisor EVENT-DRIVEN: lanza un agente registrado cuando aparece trabajo encolado para el (MSG
   *-to-<agente> en mailbox/open o tarea ready/GO) y su runtime esta caido; apaga tras umbral ocioso. Disparo por
   EVENTO (watch de mailbox/estado), NO por reloj. CONTROL DE COSTO = corazon: PROHIBIDO clock-polling ocioso (no
   quema tokens); duerme y despierta por evento. Reusa el allowlist fijo + launch/stop de 0107.
2. Override SOBERANO del operador: fijar ON/OFF por agente + PARAR el supervisor entero; honrarlos. Y RE-HABILITAR
   (limpiar el marcador .stop de un agente) -- integra el residual 2 de 0311 (con .stop presente no se lanza;
   tras limpiarlo + hay trabajo -> se lanza). Control server-side acotado, confirm, off-by-default.
3. Backoff + tope de reintentos (no auto-restart infinito). Observabilidad en el panel (que gestiona, ultimo
   evento, decisiones lanzar/apagar con razon).

## Seguridad/costo (no negociable)
Event-driven, NO clock-polling. Allowlist FIJO server-side (hereda 0107), sin shell, uno-y-solo-uno. Override del
operador soberano. #4 del hub byte-identico. Prueba negativa permanente: agente no registrado / comando arbitrario
-> RECHAZADO. Flag off -> supervisor INERTE.

## AC (ver SPEC-0114)
AC1 wake-on-event (no clock); AC2 apaga ocioso; AC3 sandbox + uno-y-solo-uno; AC4 override soberano; AC4b
re-habilitar/limpiar .stop; AC5 backoff+tope; AC6 observabilidad; AC7 off-by-default + #4 byte-identico + npm test 0.

## Cierre
Flip ready->in_progress al empezar; entrega a in_review con handoff (event-driven probado, sandbox negativa,
override + re-habilitar, backoff, off-by-default, npm test 0 clon limpio). Gate maker != checker (Analista +
Arquitecto). Trailers: Task-Id: TASK-0312. No toques hub/#4/agent_registry.

-- Arquitecto
