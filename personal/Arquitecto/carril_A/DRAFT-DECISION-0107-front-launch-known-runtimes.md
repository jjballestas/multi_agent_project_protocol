---
decision_id: DECISION-0107
title: El front puede lanzar/detener runtimes de agentes CONOCIDOS por accion del operador (indicador + boton de empuje/despertar) -- extiende DECISION-0057, sandbox server-side, off-by-default
status: proposed
date: 2026-08-02
deciders: [operador humano, Arquitecto]
amends: [DECISION-0057]
relates_to: [DECISION-0057, DECISION-0051, DECISION-0052, DECISION-0106, DECISION-0050, REQ-ZEUS-001]
phase: P2
---

# DECISION-0107 - El front lanza/detiene runtimes de agentes CONOCIDOS (Alcance B / P2 de TASK-0178)

> PROPUESTA para ratificacion del operador. Gate de superficie de escritura/runtime (CLAUDE.md regla 2 /
> AGENTS.md s4). Codigo SOLO en Zeus-protocol (producto); core neutral. NO toca el config pinned (#4 epoca
> 1.14.0), ni INTENT_TYPES, ni genesis/keys, ni el agent_registry.

## Contexto
TASK-0178 Alcance B. Hoy DECISION-0057 faculta al ARQUITECTO a lanzar/detener runtimes de agentes conocidos
(runtime-only). El operador necesita ver el estado vivo/dormido de los agentes y empujar/despertar uno desde el
front sin abrir una terminal. El "enviar prompt" ya lo cubre DECISION-0106; lo NUEVO aqui es (a) un INDICADOR de
estado (lectura) y (b) LANZAR/DETENER el runtime de un agente conocido por accion del operador via el front.

## Decision
1. **Extiende DECISION-0057 al operador-via-front:** el front puede LANZAR (arrancar/relanzar) y DETENER el
   runtime de un agente REGISTRADO por accion EXPLICITA del operador. Es la misma facultad runtime-only de 0057,
   ahora accionable por el operador desde la UI (ademas del Arquitecto).
2. **Sandbox DURO (server-side, hereda 0051/0052):** un handler SERVER-SIDE con un ALLOWLIST FIJO
   {agente_registrado -> comando de arranque/paro CONOCIDO (su .ps1/cron)}. El cliente SOLO elige QUE agente
   registrado lanzar/detener (de la lista); NUNCA envia un comando, ruta, ni argumentos. El front NO gana una
   shell ni ejecuta comandos arbitrarios. Cualquier otra forma -> RECHAZADA (prueba negativa PERMANENTE).
3. **Indicador (LECTURA):** el front LEE el estado del runtime de cada agente (pid vivo/muerto, ultimo latido,
   edad) de las senales existentes (pidfile/heartbeat del cron); read-only, sin nueva superficie de escritura.
4. **Guardas de 0057 (vinculantes, heredadas):** (a) runtime-only -- NUNCA reconfigura prompt/identidad/llaves/
   capacidades/agent_registry; (b) INSTANCIA UNICA -- no arranca un runtime duplicado si ya hay uno vivo (evita
   la cascada de crons duplicados); (c) ACTIVACION != AUTORIZACION DE RIESGO -- encender un agente no concede
   ninguna capacidad viva/peligrosa; (d) HONRA EL STOP DEL OPERADOR -- no relanza un agente que el operador fijo
   OFF/detuvo a proposito (marcador vigente, no stale); (e) integridad de identidad -- el agente lanzado firma su
   propio trabajo; maker != checker intacto.
5. **Confirmacion + off-by-default (hereda 0051/0106):** lanzar/detener exige confirmacion explicita del operador
   (sin confirm -> no actua). La capacidad nace DESHABILITADA; su flag vive FUERA del config pinned (patron
   0054/0106). Reversible por flag.
6. **On-demand, NO supervisor:** esto es lanzar/detener PUNTUAL por accion del operador (one-shot), NO el
   supervisor always-on que MANTIENE vivos los crons (eso es Alcance C / P3, decision futura). Sin bucle de
   auto-reinicio ni polling ocioso adicional: el agente lanzado corre su heartbeat normal (mismo costo que hoy al
   lanzarlo a mano). El operador conserva el override.

## Boundaries que esta DECISION NO mueve
- NO el supervisor front-server always-on (Alcance C / P3): sin mantener-vivo ni auto-restart.
- NO alta de agentes ni enlace a LLM (Alcance D / P4 / roster RF-9).
- NO nuevo INTENT_TYPES; NO nuevo firmante; NO toca agent_registry/config/#4/genesis (byte-identico).
- NO concede al front una shell ni ejecucion de comandos arbitrarios (allowlist fijo server-side).
- El agente lanzado sigue SUS reglas de protocolo (SDD, gates); lanzarlo no hace bypass de nada.

## Descartes
- Cliente envia el comando/ruta a ejecutar: NO -- reabre superficie de ejecucion arbitraria (impersonacion/RCE).
- Mantener agentes vivos en bucle desde el front: NO en esta decision -- es el supervisor (C), con su modelo de
  costo (wake-on-event) y gobernanza propios, a decidir aparte.

## Implementacion
Via SDD: SPEC-0113 (autora el Arquitecto) + tarea(s) (maker Codex, checker Analista+Arquitecto), off-by-default,
codigo solo en Zeus-protocol. Verificacion: handler server-side con allowlist fijo (prueba negativa de
comando-arbitrario/agente-no-registrado RECHAZADO), indicador read-only, instancia-unica (no duplica cron vivo),
confirm obligatorio, honra stop del operador, off-by-default inerte, #4 byte-identico (drift 0), core neutral,
npm test producto exit 0.
