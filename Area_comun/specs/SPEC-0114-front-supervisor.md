---
spec_id: SPEC-0114
title: Supervisor front-server event-driven de runtimes de agentes (Alcance C / P3 de TASK-0178), off-by-default
status: ready
owner: Codex
decision: DECISION-0108
relates_to: [DECISION-0108, DECISION-0107, DECISION-0057, TASK-0178, REQ-ZEUS-001]
project: Zeus-protocol
date: 2026-08-02
file: Area_comun/specs/SPEC-0114-front-supervisor.md
---

# SPEC-0114 -- Supervisor front-server event-driven (front Zeus-protocol)

Operacionaliza DECISION-0108. Alcance C (P3) de TASK-0178: el front-server supervisa el ciclo de vida de los
runtimes de agentes conocidos, EVENT-DRIVEN (wake-on-event, control de costo), sobre el mecanismo de 0107.
Off-by-default. Core neutral (codigo solo en Zeus-protocol).

## Arquitectura
- Un lazo supervisor en el server que reacciona a EVENTOS (watch de mailbox/estado; no un reloj): trabajo
  encolado para un agente caido -> lanza (allowlist 0107); agente ocioso > umbral -> detiene. Uno-y-solo-uno.
- Reusa el allowlist fijo + lanzar/detener de 0107 (SPEC-0113). Anade la LOGICA de decision event-driven + el
  registro de override (ON/OFF por agente, stop global) + observabilidad.

## Criterios de aceptacion
- **AC1 (wake-on-event, no clock):** el supervisor lanza un agente REGISTRADO cuando aparece trabajo encolado
  para el (nuevo MSG *-to-<agente> en mailbox/open o tarea ready/GO) y su runtime esta caido. El disparo es por
  EVENTO (watch/notificacion), NO por un reloj que sondee en vacio. Prueba: inyectar un evento de trabajo ->
  lanza; sin eventos -> el supervisor NO consume (dormido).
- **AC2 (apaga ocioso, costo):** cuando un agente lleva > umbral (config, fuera del pinned) sin trabajo encolado
  ni en vuelo, el supervisor lo detiene. Prueba: sin trabajo -> se apaga tras el umbral.
- **AC3 (sandbox + uno-y-solo-uno, hereda 0107):** solo agentes del allowlist fijo; sin shell; nunca duplica un
  runtime vivo. Negativa permanente: agente no registrado / comando arbitrario -> RECHAZADO.
- **AC4 (override del operador SOBERANO):** el operador puede fijar un agente ON (siempre vivo) u OFF (nunca
  levantado) y PARAR el supervisor entero; el supervisor honra esos marcadores (no pisa un OFF; un stop global
  para todo). Prueba: OFF fijado -> no lo levanta aunque haya trabajo; stop global -> cesa toda gestion.
- **AC4b (RE-HABILITAR / limpiar el marcador de stop -- integra el residual 2 de TASK-0311):** el operador puede
  RE-HABILITAR desde el front un agente que fue detenido (limpiar su marcador `.stop`), para que el supervisor
  (o el boton de 0107) vuelva a poder lanzarlo. Es un control SERVER-SIDE acotado (por agente del allowlist,
  confirm requerido, off-by-default); mientras el `.stop` exista el agente NO se relanza (fail-safe de 0311).
  Prueba: con `.stop` presente -> no se lanza; tras re-habilitar (limpiar `.stop`) + hay trabajo -> se lanza.
- **AC5 (tope de reintentos + backoff):** si un agente falla al arrancar repetidamente, backoff + tope (no
  auto-restart infinito); reporta el estado.
- **AC6 (observabilidad):** el panel muestra que agentes gestiona, ultimo evento, y cada decision lanzar/apagar
  con su razon.
- **AC7 (off-by-default + fondo intocable):** flag off -> supervisor inerte (no gestiona nada); flag + params
  (umbral, fuentes de evento) fuera del config pinned. #4 del hub byte-identico (drift 0); core neutral; npm test
  Zeus-protocol exit 0 en clon limpio.

## Alcance de archivos (Zeus-protocol)
- IN: src (lazo supervisor event-driven + reuso del allowlist/launch de 0107 + registro override + backoff),
  public (observabilidad del supervisor + controles ON/OFF/stop), registro de flag+params (fuera del config
  pinned), tests (event-driven lanza/apaga, no-clock-polling, sandbox negativa, override, backoff, off-by-default).
- OUT: alta de agentes / LLM (P4); cambios en hub/#4/agent_registry; shell/arbitrario; nuevo INTENT_TYPES.

## Test plan
- Positiva: evento de trabajo encolado (fixture: MSG a un agente caido) -> lanza; ocioso > umbral -> apaga;
  override OFF -> no levanta; stop global -> cesa. Sin eventos -> supervisor no consume (no clock-poll).
- Negativa: agente no registrado / comando arbitrario -> RECHAZADO; flag off -> inerte.
- #4 byte-identico antes/despues; npm test exit 0 clon limpio. Sin browser -> contrato + fixtures.

## DoD
AC1-AC7; event-driven (no clock-polling) probado; sandbox + uno-y-solo-uno; override soberano; off-by-default;
#4 intacto; core neutral; gate maker != checker (Analista + Arquitecto): el modelo event-driven (no quema tokens
ocioso), el sandbox/allowlist, el override, el backoff. Cierre gobernado.
