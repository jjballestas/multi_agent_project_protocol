---
decision_id: DECISION-0108
title: Supervisor front-server de runtimes de agentes (Alcance C / P3 de TASK-0178) -- event-driven (wake-on-event), sandbox, off-by-default
status: proposed
date: 2026-08-02
deciders: [operador humano, Arquitecto]
amends: [DECISION-0057, DECISION-0107]
relates_to: [DECISION-0107, DECISION-0057, DECISION-0051, DECISION-0106, DECISION-0050, REQ-ZEUS-001]
phase: P2
---

# DECISION-0108 - Supervisor front-server de runtimes (Alcance C / P3 de TASK-0178)

> PROPUESTA. Autorizada por la META del operador (2026-08-02: completar Alcance C + P4). Gate de superficie de
> runtime (CLAUDE.md regla 2 / AGENTS.md s4). Codigo SOLO en Zeus-protocol; core neutral. NO toca config pinned
> (#4 1.14.0), INTENT_TYPES, genesis/keys ni agent_registry.

## Contexto
TASK-0178 Alcance C. DECISION-0107 dio el lanzar/detener ON-DEMAND (one-shot por boton). C automatiza eso: el
front-server (unico proceso always-on mientras el operador trabaja) actua de SUPERVISOR de los runtimes de los
agentes conocidos -> el sistema "trabaja solo con el front abierto", sin depender de una sesion VS Code/terminal.
Es la pieza de mayor implicacion (un servidor que gestiona el ciclo de vida de procesos de IA), por eso el
control de COSTO y el sandbox son el corazon de esta decision.

## Decision
1. **Supervisor event-driven (NO clock-polling):** el front-server mantiene "uno-y-solo-uno" runtime por agente
   segun la DEMANDA, disparado por EVENTOS, no por reloj: (a) cuando un agente REGISTRADO tiene trabajo encolado
   (nuevo MSG *-to-<agente> en mailbox/open, o tarea ready/GO para el) y su runtime esta caido -> lo LANZA
   (mecanismo 0107); (b) cuando un agente lleva un umbral OCIOSO (sin trabajo encolado ni en vuelo) -> lo DETIENE.
   Es la automatizacion de DECISION-0057 (revive con trabajo, apaga ocioso), movida al front-server.
2. **Control de COSTO (guarda central):** PROHIBIDO el polling ocioso caro. El supervisor DUERME agresivamente y
   despierta por EVENTO (cambio en mailbox/estado, p.ej. watch de archivos), no por un reloj que quema tokens. Un
   agente vivo corre su heartbeat normal SOLO mientras tiene trabajo; sin trabajo, se apaga. Sin este modelo, C no
   se activa (el default es OFF y la activacion exige el flag + el guard de costo declarado).
3. **Sandbox DURO (hereda 0107):** solo runtimes de agentes REGISTRADOS via el allowlist FIJO server-side; sin
   shell; sin comandos arbitrarios. Uno-y-solo-uno por agente (nunca duplica). Runtime-only (nunca reconfigura
   identidad/llaves/registry). Activacion != autorizacion de riesgo.
4. **Override del operador (soberano):** el operador puede FIJAR un agente ON (siempre vivo) u OFF (nunca
   levantado por el supervisor), y PARAR el supervisor entero. El supervisor honra esos marcadores; no pisa un OFF
   deliberado. Un STOP explicito del operador siempre gana.
5. **Off-by-default, FUERA del config pinned, reversible:** nace deshabilitado; su flag + parametros (umbral
   ocioso, fuentes de evento) viven en un registro FUERA de protocol.config.json. #4 byte-identico; sin re-genesis.
6. **Observabilidad:** el supervisor expone su estado (que agentes gestiona, ultimo evento, decisiones de
   lanzar/apagar) en el panel para que el operador vea que hace y por que.

## Boundaries que esta DECISION NO mueve
- NO alta de agentes ni enlace a LLM (P4). NO nuevo INTENT_TYPES/firmante. NO toca agent_registry/config/#4/genesis.
- NO concede shell ni ejecucion arbitraria (allowlist fijo, hereda 0107). El agente supervisado sigue SUS reglas
  de protocolo (SDD/gates); supervisarlo no hace bypass.

## Descartes
- Supervisor por clock-polling (mantener todos vivos sondeando por reloj): NO -- quema tokens sin ser mas capaz
  (leccion viva: rondas de "heartbeat sin novedad"). El modelo es wake-on-event.
- Auto-restart infinito sin freno: NO -- respeta el override del operador + un tope de reintentos con backoff.

## Implementacion
Via SDD: SPEC-0114 (autora el Arquitecto) + tarea (maker Codex, checker Analista+Arquitecto), off-by-default,
codigo solo en Zeus-protocol. Verificacion: supervisor event-driven (prueba: lanza ante evento de trabajo
encolado, apaga tras umbral ocioso; NO hay bucle de clock-polling), sandbox/allowlist (negativa de arbitrario),
uno-y-solo-uno, honra ON/OFF del operador + stop, off-by-default inerte, #4 byte-identico (drift 0), core neutral,
npm test producto exit 0.
