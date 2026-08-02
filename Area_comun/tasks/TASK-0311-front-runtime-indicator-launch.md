---
task_id: TASK-0311
file: Area_comun/tasks/TASK-0311-front-runtime-indicator-launch.md
title: "Front Zeus-protocol: indicador de estado de runtime + boton lanzar/detener agente conocido (SPEC-0113 / DECISION-0107), off-by-default"
status: ready
type: product
owner: Codex
reviewer: Analista
priority: normal
project: Zeus-protocol
spec_id: SPEC-0113
relates_to:
  - DECISION-0107
  - SPEC-0113
  - TASK-0178
  - REQ-ZEUS-001
created_at: 2026-08-02
intake:
  type: feature
  goal: >
    Implementar el Alcance B (P2) de TASK-0178 en el front Zeus-protocol: (a) INDICADOR read-only del estado de
    runtime por agente (vivo/dormido, ultimo latido, edad) y (b) BOTON lanzar/detener el runtime de un agente
    REGISTRADO via allowlist server-side (DECISION-0107, extiende 0057). El cliente solo elige {agentId, accion};
    el servidor resuelve el comando desde un allowlist FIJO; sin shell. OFF-BY-DEFAULT. Codigo solo en
    Zeus-protocol; el hub/#4 no se toca.
  acceptance:
    - "AC1 (indicador read-only): el front muestra por agente registrado (Arquitecto/Codex/Analista) su estado de runtime {vivo|dormido, ultimo latido, edad} derivado de pidfile + heartbeat existentes; solo lectura."
    - "AC2 (lanzar/detener server-side): boton start/stop -> handler server-side que resuelve el comando desde un ALLOWLIST FIJO {agentId -> comando conocido}. El cliente solo envia {agentId, accion in start/stop}. Confirmacion explicita (sin confirm -> 409). Detras de flag OFF-BY-DEFAULT (fuera del config pinned)."
    - "AC3 (anti-arbitrario, prueba negativa PERMANENTE): comando/ruta/args desde el cliente -> RECHAZADO; agente NO registrado (fuera del allowlist) -> RECHAZADO. El servidor jamas ejecuta fuera del allowlist fijo; el front no gana shell (patron 0052)."
    - "AC4 (instancia unica): start NO arranca un runtime duplicado si el agente ya tiene uno vivo (chequeo pidfile/pid antes de spawn); devuelve 'ya vivo' sin duplicar."
    - "AC5 (honra stop + runtime-only): stop detiene el cron (taskkill del pid del pidfile); start no reconfigura identidad/llaves/prompt/registry; respeta un marcador vigente de OFF del operador (no lo pisa)."
    - "AC6 (off-by-default, on-demand): con flag off el endpoint start/stop es INERTE (403); one-shot, SIN bucle de auto-reinicio ni polling ocioso extra (NO supervisor)."
    - "AC7 (fondo intocable + gates): #4 del hub byte-identico (drift 0); sin cambios en core/protocolo; npm test Zeus-protocol exit 0 en clon limpio; con flag off la capacidad es inerte (prueba)."
  verification_cmd:
    - "cd D:/Agentes/Zeus/Zeus-protocol && npm test"
  scope_routes:
    - src/server.js
    - public/app.js
    - public/index.html
    - public/styles.css
    - tests/staticContract.test.js
  out_of_scope: >
    Supervisor always-on / mantener-vivo / auto-restart (Alcance C); alta de agentes / enlace a LLM (P4/RF-9);
    cambios en el hub/protocolo/#4/agent_registry/genesis; shell o comandos arbitrarios; nuevo INTENT_TYPES.
  risk: medium
  estimate: L
notes: >
  Alcance B (P2) de TASK-0178, gobernado por DECISION-0107 (ratificada 2026-08-02) + SPEC-0113. Repo de producto
  Zeus-protocol. Riesgo medio: el front gana capacidad de ARRANCAR PROCESOS -> el corazon de la seguridad es el
  ALLOWLIST FIJO server-side (el cliente nunca envia comando; sin shell) + la prueba negativa PERMANENTE
  (comando-arbitrario/agente-no-registrado RECHAZADO) + instancia-unica. Off-by-default. On-demand, NO supervisor
  (el supervisor always-on es Alcance C, decision aparte). Gate maker != checker: Analista + Arquitecto verifican
  el allowlist server-side, la negativa de arbitrario, el guard instancia-unica y (si hay browser) el render.
---

# TASK-0311 - Indicador de runtime + lanzar/detener agente conocido (front Zeus-protocol)

## Contexto
Alcance B de TASK-0178. DECISION-0107 (ratificada) extiende DECISION-0057 al operador-via-front. Ver SPEC-0113
para arquitectura (indicador read-only + handler start/stop con allowlist fijo server-side) y AC completos.

## Entregable
- Front Zeus-protocol: indicador de estado de runtime por agente (read) + botones start/stop con allowlist fijo
  server-side + confirm + guard instancia-unica + flag off-by-default (fuera del config pinned) + tests (contrato
  + negativa comando-arbitrario/agente-no-registrado + off-by-default + instancia-unica).

## Seguridad (no negociable)
El allowlist es FIJO server-side; el cliente solo elige {agentId, accion}, jamas un comando. Prueba negativa
PERMANENTE: comando-arbitrario o agente-no-registrado -> RECHAZADO. El front no gana shell. #4 del hub byte-identico.
