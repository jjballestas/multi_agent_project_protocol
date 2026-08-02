---
spec_id: SPEC-0113
title: Front Zeus-protocol: indicador de estado de runtime + boton lanzar/detener agente conocido (Alcance B / P2 de TASK-0178), off-by-default
status: ready
owner: Codex
decision: DECISION-0107
relates_to: [DECISION-0107, DECISION-0057, DECISION-0051, DECISION-0052, DECISION-0106, TASK-0178, REQ-ZEUS-001]
project: Zeus-protocol
date: 2026-08-02
file: Area_comun/specs/SPEC-0113-front-runtime-indicator-launch.md
---

# SPEC-0113 -- Indicador de runtime + lanzar/detener agente conocido (front Zeus-protocol)

Operacionaliza DECISION-0107 (ratificada 2026-08-02). Alcance B (P2) de TASK-0178: el operador ve el estado
vivo/dormido de cada agente y puede empujar/despertar (lanzar) o detener su runtime desde el front, sin terminal.
Repo de producto: `D:\Agentes\Zeus\Zeus-protocol`. Gobernanza en el hub. **Off-by-default.** Core neutral.

## Alcance (P2)
DOS piezas: (a) INDICADOR (lectura) del estado de runtime por agente; (b) LANZAR/DETENER (escritura de runtime)
el runtime de un agente REGISTRADO via allowlist server-side. El "enviar prompt" ya es SPEC-0112/DECISION-0106.
NO incluye supervisor always-on (Alcance C), ni alta de agentes (P4).

## Arquitectura (hereda DECISION-0057/0051/0052)
- **Indicador read-only:** el server LEE senales existentes del runtime de cada agente registrado (pidfile del
  cron + heartbeat/ultimo latido del log) y expone estado {vivo|dormido, ultimo_latido, edad}. Sin escritura.
- **Lanzar/detener con sandbox DURO:** un handler SERVER-SIDE con ALLOWLIST FIJO en el servidor
  {agente_registrado -> comando de arranque conocido (su .ps1) / comando de paro (taskkill del pid del pidfile)}.
  El cliente SOLO envia {agentId (de la lista), accion in {start,stop}}. NUNCA comando/ruta/args. El front NO gana
  shell.

## Criterios de aceptacion
- **AC1 (indicador, read-only):** el front muestra por cada agente registrado (Arquitecto/Codex/Analista) su
  estado de runtime: vivo|dormido, ultimo latido, edad. Derivado de pidfile + heartbeat existentes; solo lectura;
  coherente con el resto del panel (frescura/stale).
- **AC2 (lanzar/detener server-side):** boton start/stop por agente -> handler server-side que resuelve el comando
  desde un ALLOWLIST FIJO {agentId -> comando conocido}. El cliente solo envia {agentId, accion}. Confirmacion
  explicita (confirm:*; sin confirm -> 409, prueba negativa). Detras de un flag OFF-BY-DEFAULT (registro FUERA del
  config pinned).
- **AC3 (anti-arbitrario, prueba negativa PERMANENTE):** cualquier intento de (a) enviar un comando/ruta/args
  desde el cliente, o (b) actuar sobre un agente NO registrado (fuera del allowlist) -> RECHAZADO. El servidor
  jamas ejecuta algo fuera del allowlist fijo (patron 0052). El front no gana shell.
- **AC4 (instancia unica):** start NO arranca un runtime duplicado si el agente ya tiene uno vivo (chequeo de
  pidfile/pid vivo antes de spawn); devuelve estado 'ya vivo' sin duplicar.
- **AC5 (honra stop del operador + runtime-only):** stop detiene el cron del agente (taskkill del pid del
  pidfile). start no reconfigura identidad/llaves/prompt/registry (runtime-only). No relanza si hay un marcador
  vigente de OFF del operador (respeta el override).
- **AC6 (off-by-default, on-demand):** con el flag off, el endpoint de start/stop es INERTE (403); el indicador
  puede seguir en read-only o tambien gatearse (declararlo). Es on-demand (one-shot), SIN bucle de auto-reinicio
  ni polling ocioso extra (NO supervisor).
- **AC7 (fondo intocable + gates):** #4 del hub byte-identico (drift 0); sin cambios en core/protocolo (codigo
  solo en Zeus-protocol); npm test Zeus-protocol exit 0 en clon limpio; con flag off la capacidad es inerte (prueba).

## Alcance de archivos (Zeus-protocol)
- IN: src/server.js (lector de estado read-only + handler start/stop con allowlist fijo + guard instancia-unica),
  public (indicador UI + botones start/stop + confirm), registro del flag off-by-default (fuera del config pinned),
  tests (contrato + prueba negativa comando-arbitrario/agente-no-registrado + off-by-default + instancia-unica).
- OUT: supervisor always-on / mantener-vivo / auto-restart (Alcance C); alta de agentes / LLM (P4); cambios en el
  hub/protocolo/#4/agent_registry; shell o comandos arbitrarios; nuevo INTENT_TYPES.

## Test plan
- Negativa AC3: comando/ruta desde cliente -> RECHAZADO; agente no registrado -> RECHAZADO. AC2: sin confirm ->
  409. AC4: start con pid vivo -> no duplica. AC6: flag off -> 403 inerte.
- Positiva (fixtures, sin spawn real de IA donde sea posible; o spawn de un stub inocuo): start/stop resuelven el
  comando del allowlist; indicador lee estado de un pidfile/heartbeat fixture. #4 byte-identico antes/despues.
  npm test exit 0 en clon limpio. Sin browser -> render por contrato + fixtures.

## DoD
Cumple AC1-AC7; off-by-default; anti-arbitrario probado (negativa permanente); instancia-unica; honra stop del
operador; #4 intacto; core neutral; gate maker != checker (Analista + Arquitecto): verificar el allowlist fijo
server-side, la negativa de comando-arbitrario, el guard instancia-unica, y (si hay browser) el render; sin
browser, por contrato + fixtures. Cierre gobernado.
