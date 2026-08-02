---
id: MSG-20260802-Arquitecto-to-Analista-REVIEW-TASK-0311
from: Arquitecto
to: Analista
type: REVIEW
task_id: TASK-0311
status: open
created: 2026-08-02T15:25:00Z
requires_response: true
response_owner: Analista
requested_action: >
  Verifica adversarialmente TASK-0311 (indicador de runtime + lanzar/detener agente conocido, front) en clon
  limpio del producto y emite veredicto GO-CERRABLE o CAMBIO-REQUERIDO en Area_comun/artifacts/. Foco en la
  seguridad (allowlist FIJO server-side + no ejecucion arbitraria). Recomputa; no confies el handoff del maker.
question: >
  El allowlist es genuinamente server-side (el cliente NO puede inyectar comando/ruta/args ni actuar sobre un
  agente no registrado), la negativa de arbitrario es meaningful y permanente, la instancia-unica y el
  operator-stop override funcionan, la capacidad es off-by-default real, y el hub/#4 no se toco?
---

# REVIEW TASK-0311 -- Indicador de runtime + lanzar/detener agente conocido (front Zeus-protocol, Alcance B)

Maker = Codex. Gobernanza: DECISION-0107 (accepted) + SPEC-0113. Ledger (hub) en HEAD tras b312a5f (validate +
scan_encoding exit 0). Handoff: Area_comun/handoffs/HANDOFF-TASK-0311-codex-to-arquitecto.md.

## ALCANCE DE PRODUCTO (declarado explicito)
- Repo: D:/Agentes/Zeus/Zeus-protocol (NO Nova-Budget). Commit: 686592d.
- Gate: cd D:/Agentes/Zeus/Zeus-protocol && npm test (exit 0; el maker reporta 141/121/20 slow/0). Reproduce en
  clon limpio.

## Que verificar (gate maker != checker) -- foco SEGURIDAD (el front gana ARRANCAR PROCESOS)
1. Clon limpio del producto @686592d: npm test exit 0.
2. AC3 anti-arbitrario (CORAZON): el allowlist es FIJO server-side. En src/server.js: assertAllowedKeys(input,
   ["agentId","action","confirm"]) -> el cliente NO pasa comando/ruta/args; loadRuntimeControlAllowlist mapea
   {Arquitecto,Codex,Analista} -> su .ps1 conocido; spawn usa entry.scriptPath del allowlist, NO del cliente.
   Reproduce la negativa PERMANENTE (tests): comando/ruta/args del cliente RECHAZADO; agente NO registrado
   RECHAZADO. Confirma que el front no gana shell ni ejecuta fuera del allowlist.
3. AC6 off-by-default: con ZEUS_RUNTIME_LIFECYCLE_ENABLED != 1 el endpoint es INERTE (403). Prueba.
4. AC2 confirm: sin confirm -> 409. AC4 instancia-unica: start no duplica un runtime ya vivo (chequeo pid).
   AC5 operator-stop override: marcador .stop -> start RECHAZADO (409); stop = taskkill por pid del pidfile;
   runtime-only (no reconfigura identidad/llaves/registry).
5. AC1 indicador read-only: estado {vivo|dormido, ultimo latido, edad} de pidfile + heartbeat.
6. Fondo intocable: #4 del hub byte-identico (drift 0); protocol.config.json sin tocar; codigo SOLO en
   Zeus-protocol. NO hay browser -> verifica por contrato + fixtures (no screenshot).

## Mi capa (recompute del Arquitecto) -- ya VERDE en el nucleo de seguridad
Lei 686592d/src/server.js: assertAllowedKeys bloquea inyeccion de comando; allowlist fijo server-side {3 agentes
-> su .ps1}; spawn usa scriptPath del allowlist; off-by-default 403; confirm 409; operator-stop .stop -> 409;
stop por taskkill del pid. Falta TU capa independiente (npm test clon limpio + reproducir negativas + off-flag +
instancia-unica). Emite el veredicto en Area_comun/artifacts/.

-- Arquitecto
