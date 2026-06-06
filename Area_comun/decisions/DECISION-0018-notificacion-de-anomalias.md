---
decision_id: DECISION-0018
title: Regla de notificacion de anomalias entre agentes (avisar por mailbox, no silenciar ni corregir rutas ajenas)
status: accepted
date: 2026-06-06
ratified_at: 2026-06-06
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0007, DECISION-0011, DECISION-0013, DECISION-0015, DECISION-0001]
phase: P2
---

# DECISION-0018 - Notificacion de anomalias entre agentes

> Estado: ACCEPTED (2026-06-06, pedida y aprobada por el operador). Regla de proceso del protocolo de
> colaboracion, aditiva. SemVer MINOR (DECISION-0001). Neutral de dominio.

## Contexto

Durante la consolidacion del nucleo N-agente (TASK-0051, Capa A.3) Codex dejo un handoff-release
INCOMPLETO: escribio el handoff y el mensaje in-review declarando "claim liberado", pero el estado quedo
inconsistente (claim `active`, status `in_progress`). Claude, que detecto la anomalia durante el monitoreo,
solo la reporto al operador humano y a su memoria; no se la notifico directamente a Codex por el canal. El
operador tuvo que avisar a Codex manualmente. Esto evidencia una brecha: el protocolo no exigia que el
agente que detecta una anomalia de otro se la comunique por el canal compartido.

## Decision

Se incorpora al protocolo de colaboracion la **regla de notificacion de anomalias**:

1. Todo agente que detecte una anomalia o inconsistencia en el trabajo de otro participante o en el estado
   compartido (p.ej. handoff-release incompleto, status que contradice claims/mailbox, claim vencido o
   huerfano, artefacto faltante o que no coincide) **debe notificarla al responsable via `mailbox/open/`**
   con un mensaje concreto y accionable, y dejar constancia.
2. **No** debe corregir silenciosamente rutas cubiertas por el claim activo de otro, **ni** dejar la
   anomalia sin senalar. Si el arreglo requiere esas rutas, pregunta al owner (o al humano) y espera.
3. La notificacion al humano no sustituye la notificacion al agente responsable: el canal entre agentes
   (mailbox) es el medio primario; el humano puede intervenir, pero la regla aplica agente-a-agente.

Aclaracion complementaria (no normativa nueva, refuerzo): un handoff-release es atomico en intencion -- el
mensaje que declara `in_review`/`done` y la transicion de estado (liberar claim + flip de status) deben
quedar juntos; si un turno termina con el mensaje escrito pero el estado sin transicionar, es una anomalia
a notificar y completar, no una entrega valida.

## Aplicacion

- `AGENTS.md` sec.7 (Collaboration Protocol) y `AGENTS.template.md` sec.7: nuevo bullet de notificacion de
  anomalias.
- `Area_comun/protocol/TASK_PROTOCOL.md`: subseccion "Anomaly notification" + nota de atomicidad del
  handoff-release en "Handoff-release and liveness".

## Versionado y neutralidad (DECISION-0001)

Aditiva (nueva regla de proceso; no rompe comportamiento ni contrato de datos). **MINOR.** Neutral de
dominio: es coordinacion de proceso, sin terminos de negocio.

## Consecuencias

- Las anomalias dejan de depender de que el humano sea el intermediario; el agente que las ve las comunica
  al responsable por el canal, acelerando la correccion y dejando traza auditable.
- Complementa DECISION-0013 (liveness/visibilidad) y la disciplina de claims (DECISION-0007/0011): ver una
  anomalia bajo claim ajeno => avisar, no tocar.
- Un futuro endurecimiento podria validar/alertar anomalias automaticamente (validador), fuera de alcance
  aqui.
