---
task_id: TASK-0312
file: Area_comun/tasks/TASK-0312-front-supervisor.md
title: "Front Zeus-protocol: supervisor event-driven de runtimes de agentes + re-habilitar/limpiar .stop (SPEC-0114 / DECISION-0108), off-by-default"
status: ready
type: product
owner: Codex
reviewer: Analista
priority: normal
project: Zeus-protocol
spec_id: SPEC-0114
relates_to:
  - DECISION-0108
  - SPEC-0114
  - DECISION-0107
  - TASK-0178
  - TASK-0311
  - REQ-ZEUS-001
created_at: 2026-08-02
intake:
  type: feature
  goal: >
    Implementar el Alcance C (P3) de TASK-0178 en el front Zeus-protocol: un SUPERVISOR event-driven que
    mantiene uno-y-solo-uno runtime por agente segun la DEMANDA (lanza ante trabajo encolado para un agente
    caido, apaga tras umbral ocioso), sobre el allowlist/launch de 0107. Control de COSTO: wake-on-event (NO
    clock-polling ocioso). Override soberano del operador (ON/OFF/stop global) + RE-HABILITAR (limpiar .stop,
    integra el residual 2 de 0311). Off-by-default. Codigo solo en Zeus-protocol; hub/#4 no se toca.
  acceptance:
    - "AC1 (wake-on-event, NO clock): lanza un agente registrado cuando aparece trabajo encolado para el (MSG *-to-<agente> en mailbox/open o tarea ready/GO) y su runtime esta caido; disparo por EVENTO (watch), NO por reloj que sondee en vacio. Prueba: evento -> lanza; sin eventos -> supervisor no consume (dormido)."
    - "AC2 (apaga ocioso, costo): agente > umbral (config fuera del pinned) sin trabajo encolado ni en vuelo -> lo detiene. Prueba: sin trabajo -> se apaga tras el umbral."
    - "AC3 (sandbox + uno-y-solo-uno, hereda 0107): solo agentes del allowlist fijo server-side; sin shell; nunca duplica un runtime vivo. Negativa permanente: agente no registrado / comando arbitrario -> RECHAZADO."
    - "AC4 (override SOBERANO): el operador puede fijar ON (siempre vivo) / OFF (nunca levantado) por agente y PARAR el supervisor entero; se honran (no pisa OFF; stop global cesa todo)."
    - "AC4b (re-habilitar / limpiar .stop, residual 2 de 0311): control server-side acotado para limpiar el marcador .stop de un agente (confirm, off-by-default) -> el supervisor/boton puede relanzarlo. Con .stop presente NO se lanza (fail-safe); tras limpiar + hay trabajo -> se lanza."
    - "AC5 (backoff + tope): fallo repetido al arrancar -> backoff + tope (no auto-restart infinito); reporta estado."
    - "AC6 (observabilidad): el panel muestra que agentes gestiona, ultimo evento y cada decision lanzar/apagar con su razon."
    - "AC7 (off-by-default + fondo intocable): flag off -> supervisor inerte (no gestiona); flag + params (umbral, fuentes de evento) fuera del config pinned. #4 del hub byte-identico (drift 0); core neutral; npm test Zeus-protocol exit 0 en clon limpio."
  verification_cmd:
    - "cd D:/Agentes/Zeus/Zeus-protocol && npm test"
  scope_routes:
    - src/server.js
    - public/app.js
    - public/index.html
    - public/styles.css
    - tests/staticContract.test.js
  out_of_scope: >
    Alta de agentes / enlace a LLM (P4/RF-9); cambios en el hub/protocolo/#4/agent_registry/genesis; shell o
    comandos arbitrarios; nuevo INTENT_TYPES; clock-polling ocioso (prohibido por costo).
  risk: medium
  estimate: L
notes: >
  Alcance C (P3) de TASK-0178, gobernado por DECISION-0108 (accepted via meta del operador) + SPEC-0114. Repo de
  producto Zeus-protocol. Automatiza DECISION-0057 (revive con trabajo, apaga ocioso) en el front-server, EVENT-
  DRIVEN (el control de costo es el corazon: NO clock-polling). Reusa el allowlist/launch de 0107 (TASK-0311).
  Integra el residual 2 de 0311 (limpiar .stop). Off-by-default. Gate maker != checker: Analista + Arquitecto
  verifican el modelo event-driven (no quema tokens ocioso), el sandbox/allowlist, el override soberano + re-habilitar,
  el backoff. Sin browser -> por contrato + fixtures.
---

# TASK-0312 - Supervisor event-driven de runtimes (front Zeus-protocol)

## Contexto
Alcance C de TASK-0178. DECISION-0108 (accepted) automatiza el ciclo de vida de runtimes en el front-server,
event-driven (wake-on-event, control de costo). Ver SPEC-0114 para arquitectura y AC completos. Integra el
residual 2 de TASK-0311 (re-habilitar / limpiar .stop).

## Entregable
- Front Zeus-protocol: lazo supervisor event-driven (lanza/apaga por demanda) sobre el allowlist de 0107 +
  override soberano (ON/OFF/stop/re-habilitar) + backoff + observabilidad + flag off-by-default (fuera del config
  pinned) + tests (event-driven lanza/apaga, no-clock-polling, sandbox negativa, override, re-habilitar, backoff,
  off-by-default).

## Seguridad/costo (no negociable)
Event-driven (NO clock-polling ocioso: no quema tokens). Allowlist fijo server-side (hereda 0107); sin shell.
Override del operador soberano. #4 del hub byte-identico.
