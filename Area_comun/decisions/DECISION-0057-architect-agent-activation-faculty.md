---
decision_id: DECISION-0057
title: "Facultad del Arquitecto para activar y detener agentes (orquestacion con control de costo)"
status: accepted
date: 2026-06-22
deciders: [operador humano, Arquitecto]
supersedes: []
related: [DECISION-0018, DECISION-0020, DECISION-0047]
---

# DECISION-0057 - Facultad del Arquitecto para activar/detener agentes

## Contexto

Los agentes de implementacion y revision (Codex, Analista) corren como ejecutores/cron (procesos de runtime,
p.ej. `personal/<id>/*cron*.ps1`) que reclaman tareas, escriben el ledger gobernado y commitean/pushean de forma
autonoma. Hasta ahora la **activacion** de un agente fue prerrogativa exclusiva del operador humano (el Arquitecto
solo los mandaba a stand-down al cerrar un proceso). Eso deja al Arquitecto, que es el rol orquestador, sin poder
arrancar al agente que necesita para avanzar una tarea cuando su runtime esta caido (cron muerto / PID
NOT_RUNNING), y deja agentes encendidos consumiendo computo/costo cuando ya no hay trabajo para ellos.

## Decision

El rol **Arquitecto / orquestador** tiene la **facultad de activar (lanzar/relanzar el runtime) de los agentes
que necesite para cumplir una tarea, y el deber de detenerlos (stand-down de su runtime) cuando su trabajo
encolado esta hecho**, para control de costo. La activacion/desactivacion es **operacional** (gestion del proceso
de runtime), no concede ninguna autoridad nueva sobre el contenido del trabajo.

## Guardas (vinculantes)

1. **Alcance: solo el runtime.** El Arquitecto lanza/relanza y detiene UNICAMENTE el proceso de ejecutor/cron del
   agente. **Nunca** reconfigura su prompt, identidad, llaves, capacidades ni su entrada en el `agent_registry`
   (eso sigue siendo del operador y, donde aplique, un re-genesis-boundary gobernado).
2. **Disparo de activacion.** Solo activa cuando (a) hay una tarea/GO encolada para ese agente y (b) detecta su
   runtime inactivo (cron muerto / PID NOT_RUNNING).
3. **Marcador stale vs stand-down deliberado.** Solo relanza si la orden de parada es **stale** (marcador leftover
   de un proceso ya cerrado) y **no** corresponde a una instruccion vigente del operador de mantener ese agente
   detenido. Si el operador lo detuvo a proposito o lo fijo OFF, el Arquitecto **no** lo pisa.
4. **Desactivacion por costo.** Cuando un agente no tiene trabajo encolado ni en vuelo, el Arquitecto lo manda a
   stand-down (detiene su cron + higiene de mailbox), para no consumir.
5. **Instancia unica.** No arrancar runtimes/PIDs duplicados del mismo agente.
6. **Integridad de identidad.** Activar un agente nunca autoriza forjar su identidad: los commits del agente
   conservan su autoria (Co-Authored-By cuando el Arquitecto commitea trabajo de producto del agente). maker !=
   checker queda intacto (activar a Codex no habilita al Arquitecto a cerrar trabajo de implementer, ni viceversa).
7. **Activacion != autorizacion de riesgo.** Encender un agente NO concede ninguna capacidad viva/peligrosa: uso
   vivo de connectors/extractor, edicion del config bajo #4, pushes a remotos externos, re-genesis -- todo eso
   sigue exigiendo un GO aparte del operador. La facultad es solo de gestion de proceso.
8. **Auditabilidad.** Toda activacion/desactivacion se registra (FYI al operador + memoria del Arquitecto).
9. **Override humano.** El operador puede fijar cualquier agente ON/OFF y anular esta facultad en cualquier
   momento; su instruccion vigente manda (regla 3).

## Consecuencias

- El loop multi-agente (Codex implementa -> Arquitecto checker -> Analista pasada -> Arquitecto cierra) se vuelve
  autonomo: el Arquitecto puede revivir un ejecutor caido que bloquea una tarea encolada, y apagar a los agentes
  ociosos al terminar.
- Neutralidad de dominio intacta: esto es governanza de metodologia, generico, sin terminos de negocio.
- **Versionado por epoca (DECISION-0047):** capacidad documentada en CHANGELOG; el `protocol_version` del config
  vivo sigue **pinned 1.14.0** bajo #4 (sin re-genesis, sin tocar el config). Sin impacto en el core neutral.
- AGENTS.md s.3 (roles) se actualiza para reflejar la facultad.
