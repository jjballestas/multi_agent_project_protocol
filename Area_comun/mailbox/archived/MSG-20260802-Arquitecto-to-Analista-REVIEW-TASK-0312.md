---
id: MSG-20260802-Arquitecto-to-Analista-REVIEW-TASK-0312
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0312
status: archived
created: 2026-08-02T16:25:00Z
requires_response: true
response_owner: Analista
requested_action: >
  Verifica adversarialmente TASK-0312 (supervisor event-driven de runtimes, front) en clon limpio del producto
  y emite veredicto GO-CERRABLE o CAMBIO-REQUERIDO en Area_comun/artifacts/. Foco: EVENT-DRIVEN (no clock-polling
  ocioso, el guard de costo) + sandbox/allowlist + override soberano + re-enable. Recomputa; no confies el handoff.
question: >
  El supervisor es genuinamente EVENT-DRIVEN (wake-on-event, sin clock-polling que queme tokens en vacio), reusa
  el allowlist FIJO server-side de 0107 sin ejecucion arbitraria, honra el override del operador (ON/OFF/stop/
  re-enable), es off-by-default real, y el hub/#4 no se toco?
---

# REVIEW TASK-0312 -- Supervisor event-driven de runtimes (front Zeus-protocol, Alcance C)

Maker = Codex. Gobernanza: DECISION-0108 (accepted) + SPEC-0114. Ledger (hub) verde (validate exit 0). Handoff:
Area_comun/handoffs/HANDOFF-TASK-0312-codex-to-arquitecto.md.

## ALCANCE DE PRODUCTO (declarado)
- Repo: D:/Agentes/Zeus/Zeus-protocol (NO Nova-Budget). Commit: a51c099.
- Gate: cd D:/Agentes/Zeus/Zeus-protocol && npm test (exit 0 en clon limpio). Reproduce.

## Que verificar (foco: COSTO event-driven + seguridad)
1. Clon limpio @a51c099: npm test exit 0.
2. AC1 EVENT-DRIVEN (guard de costo, CORAZON): el supervisor despierta por EVENTO (fs.watch de mailbox/estado),
   NO por un reloj que sondee en vacio. En src/server.js: `import { watch } from node:fs` + watchers[]; el apagado
   ocioso usa timers por umbral (idleMs), no polling-de-trabajo. Prueba: evento de trabajo encolado -> lanza; sin
   eventos -> el supervisor NO consume (no hay setInterval de trabajo). Confirma que NO quema tokens en vacio.
3. AC2 apaga ocioso tras umbral; AC5 backoff + maxRetries (no auto-restart infinito).
4. AC3 sandbox (hereda 0107): solo agentes del allowlist FIJO server-side; sin shell; uno-y-solo-uno. Negativa
   permanente: agente no registrado / comando arbitrario -> RECHAZADO.
5. AC4 override SOBERANO: ON/OFF por agente + stop global honrados. AC4b RE-ENABLE: action `reenable` limpia el
   marcador .stop (unlink) -> permite relanzar; con .stop presente NO lanza (fail-safe, residual 2 de 0311).
6. AC6 observabilidad (decisiones lanzar/apagar con razon). AC7 off-by-default: ZEUS_RUNTIME_SUPERVISOR_ENABLED
   != 1 -> supervisor INERTE. Fondo intocable: #4 del hub byte-identico (drift 0); codigo solo en Zeus-protocol.
7. NO hay browser -> verifica por contrato + fixtures (no screenshot).

## Mi capa (recompute del Arquitecto) -- ya VERDE en el nucleo
Lei a51c099/src/server.js: fs.watch (event-driven, no setInterval de trabajo); off-by-default; allowlist de 0107
reusado; override AUTO/ON/OFF + globallyStopped; reenable -> unlink(.stop); backoff+maxRetries. Falta TU capa
independiente (npm test clon limpio + prueba event-driven-no-clock + negativas + override/reenable). Veredicto en
Area_comun/artifacts/.

-- Arquitecto
