---
decision_id: DECISION-0062
title: Consola del Arquitecto - puente interactivo PERSISTENTE Operador<->Arquitecto (canal vivo, gobernado no-bypass, runtime-only, off-by-default)
status: accepted
ratified_at: 2026-06-26
date: 2026-06-26
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0057, DECISION-0050, DECISION-0040, DECISION-0022, DECISION-0038, DECISION-0051]
phase: P2
---

# DECISION-0062 - Consola del Arquitecto (puente interactivo persistente)

> ACCEPTED (operador ratifico 2026-06-26). El operador eligio el enfoque "puente interactivo persistente"
> (avance de TASK-0178). Gobernanza/SPEC en el protocolo (dataset); codigo en Zeus-protocol (producto),
> unidireccional (DECISION-0050). NO toca #4 (registro de activacion fuera del config pinned). Implementacion =
> SPEC-0098 + tareas por pieza (maker=Codex / checker=Arquitecto).

## Contexto

Hoy al Arquitecto lo dirige el operador desde VS Code; Codex/Analista por cron. El operador quiere **reemplazar
VS Code por el front** para coordinar al Arquitecto: una **consola conversacional VIVA** donde escribe, el
runtime del Arquitecto se **activa**, y ve en **streaming** lo que el Arquitecto hace/reporta. Es DISTINTO del
mailbox (async gobernado) y de la consola de prompts Q2 (operador->agente via `mailbox_send`). Enfoque elegido =
**puente interactivo PERSISTENTE** (wrapper de larga vida, como los crons pero interactivo + streaming; el
Arquitecto queda "caliente"). Es la palanca "front como supervisor siempre-activo".

## Decision

1. **Puente de runtime interactivo y persistente del Arquitecto.** Un wrapper gobernado de larga vida lanza y
   mantiene una sesion VIVA del runtime del Arquitecto, recibe los mensajes del operador desde el front y
   **transmite (streaming)** el trabajo/reporte del Arquitecto a la UI. Expuesto como **consola del Arquitecto**
   en el front (Operador<->Arquitecto en vivo).

2. **NO-BYPASS (invariante dura).** El canal es **control + observabilidad**, NUNCA una ruta directa de escritura
   al ledger/event-log. **Toda** mutacion de estado que produzca el Arquitecto sigue por `submit_intent`
   (DECISION-0022): el #4 permanece como escritor unico. La consola no puede aplicar transiciones por fuera de
   `submit_intent` ni editar `Area_comun/state/*` a mano.

3. **Runtime-only (espejo DECISION-0057).** El puente solo **lanza/relanza/detiene** el runtime del Arquitecto;
   **nunca** reconfigura identidad/llaves/registro de agentes, ni concede capacidades que el Arquitecto no tenga.
   Honra un **stop explicito** del operador. (No es alta/baja de agente: eso sigue siendo re-genesis-boundary.)

4. **Sesion unica viva (anti-colision).** El puente garantiza **exactamente una** sesion viva del Arquitecto; no
   dos en paralelo (regla "no correr dos sesiones de Arquitecto"). Si ya hay una, el operador la reusa o la
   detiene; el puente serializa.

5. **Auditoria + guarda PII (DECISION-0040).** La conversacion Operador<->Arquitecto es **auditable** en un store
   controlado, PERO el transcript NO contamina el dataset atestado: texto libre/PII de terceros **NUNCA** al
   event-log #4; redaccion best-effort en lo que se persista. La consola es narracion de coordinacion, no
   evidencia atestada (DECISION-0038: el deliverable atestado sigue siendo el handoff/intent, no el chat).

6. **Off-by-default, operador presente, gateada.** Es una superficie poderosa (un proceso que dirige al
   Arquitecto). Nace **APAGADA**; se activa por configuracion de runtime **FUERA del config pinned** (un registro
   tipo `*.runtime.json` gitignored, nunca commiteando el flag), con el operador presente. Sin activacion, no hay
   puente.

7. **Repos (DECISION-0050).** Gobernanza/DECISION/SPEC en el protocolo (dataset atestado). El **codigo** (UI de la
   consola en el front + proceso-puente) en **Zeus-protocol** (producto), acoplamiento unidireccional; el core
   neutral intacto.

8. **SDD por pieza, maker!=checker.** Tras ratificar: SPEC propia + tareas, de a una:
   (i) **proceso-puente** gobernado (lanzar/streamear/detener la sesion viva del Arquitecto, no-bypass, sesion
   unica, stop honrado); (ii) **consola en el front** (UI conversacional + transporte de streaming, read-only
   sobre el trabajo, entrada que va al puente); (iii) **auditoria** (store controlado + guarda PII). maker=Codex /
   checker=Arquitecto. Cada pieza off-by-default, gates verdes clon limpio.

## Alcance

- **En alcance:** la consola VIVA del Arquitecto, single-operator (un operador, un Arquitecto).
- **Fuera de alcance:** consolas vivas para Codex/Analista u otros (futuro); la **fabrica multi-agente NOVA**
  (~11 roles, producto municipal/financiero -- futuro, su propia gobernanza); multi-tenant (RNF-7); alta/baja de
  agente (re-genesis-boundary, RF-9, su propio flujo).

## Consecuencias

- El operador coordina al Arquitecto desde el front en vivo, sin VS Code, manteniendo #4 como escritor unico y la
  neutralidad del core.
- Coste/riesgo: un proceso persistente que dirige al Arquitecto = superficie nueva potente -> por eso no-bypass +
  runtime-only + sesion unica + off-by-default + operador presente + auditoria. Mas infra (proceso de larga vida +
  streaming) que el spawn-por-mensaje.

## Alternativas consideradas (descartadas por el operador)

- **Spawn por mensaje + streaming:** cada mensaje dispara una corrida del Arquitecto y termina (reusa el patron
  cron). Mas simple e incremental; el operador prefirio el puente persistente (experiencia VS-Code-like).
- **Observabilidad primero:** solo streaming read-only del trabajo, entrada por el mailbox existente. Menor paso;
  no cumple "hablar en vivo".
