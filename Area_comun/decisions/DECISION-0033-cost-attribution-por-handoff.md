---
decision_id: DECISION-0033
title: Cost-attribution por handoff/decision/agente (instrumentacion de medicion de dos planos)
status: accepted
date: 2026-06-14
ratified_at: 2026-06-14
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0009, DECISION-0022, DECISION-0024, DECISION-0028, DECISION-0030]
phase: P2
---

# DECISION-0033 - Cost-attribution por handoff/decision/agente

> Estado: ACCEPTED (2026-06-14). Cambio ADITIVO, off-by-default. Instrumentacion de medicion que
> debe quedar VIVA antes del piloto del loop (para capturar en caliente, no retrofitar).

## Contexto

Hoy la medicion de coste de tokens es agregada o por tope global (`runtime/budget.py`: `soft/hard
cost_tokens`, `max_cost_tokens`) y agregaciones post-hoc por tarea/corrida (`runtime/metrics.py`:
`cost_per_task`). Falta GRANULARIDAD por evento: no se puede imputar cuanto costo un handoff
concreto, una decision concreta o el trabajo de un agente concreto. Esa granularidad es el insumo
para gobernar el coste cuando el loop dirija turnos (DECISION-0009/0024); si no esta VIVA antes del
piloto, no captura en caliente y habria que retrofitarla (estimacion, no medicion).

## Decision

Se anade una **instrumentacion de imputacion de coste por evento** con tres dimensiones -- **handoff,
decision y agente** -- construida sobre el event log (`runtime/eventlog.py`), leida por `metrics.py`
y con el constructor del registro en `budget.py`. Es **aditiva** y **off-by-default**.

**Esquema de DOS PLANOS (innegociable):**
- **Plano de protocolo:** un evento `cost.attributed` (estructurado, SIN texto libre) con la metrica:
  `dimension`, `subject_hash`, `subject_seq`, `actor`, `cost_tokens`, los tags `cost_unit`/`cost_schema`
  e identificadores estructurados (`task_id`/`decision_id`). Vive en el event log.
- **Plano de carga util:** el contenido real del handoff/decision (prosa, deliverable) **NO** se copia
  al plano de protocolo; se referencia **solo por hash** (`subject_hash = canonical_hash(subject_canonico)`).
  No filtra texto libre al plano de protocolo.

**Esquema fijado ANTES de la primera emision en caliente (endurecimiento analista pasada-3, el log es
inmutable):**
- **Subject canonico por dimension.** El `subject` se construye de UN identificador tipado:
  `handoff -> {handoff_id}`, `decision -> {decision_id}`, `agent -> {agent_id}`; sin prosa ni campos
  variables. Dos emisiones logicamente iguales producen el MISMO `subject_hash` (apareamiento estable
  para H2; `idempotency_key` estable).
- **`cost_tokens` = total del PRODUCTOR** (input contexto + output generacion) gastado por `actor` al
  producir `subject`. Tags `cost_unit` (`tokens_total` por defecto) + `cost_schema` (`"1"`) en cada
  emision; si la convencion cambia, se bumpea `cost_schema`. El summarizer rechaza filas sin ambos tags.
- **`subject_hash` es SEUDONIMO, no anonimo.** Bajo RGPD (Considerando 26) / Ley 1581, un hash de
  contenido con el plano de carga util **retenido** es dato **seudonimizado y re-identificable**, no
  anonimo. El plano de protocolo es *regulado-pero-minimizado*: NO es "publicable" sin romper el enlace
  (no retener `subject`, o salar por-publicacion y descartar la sal) o acotar explicitamente.
  GATE-DATASET trata el corpus como seudonimizado, carga util retirada. `actor` se restringe por
  esquema a un vocabulario controlado de ids de agente **no-humano**; si alguna vez fuera un id humano
  (usuario/correo) seria dato personal directo, por eso se acota.

**No-mutador del estado.** El evento `cost.attributed` se emite con `applied:false`: es una anotacion
(como `agent.attestation`/`chain.anchor`). El replay de estado de protocolo lo **omite**
(`protocol_replay.replay_protocol_state` salta `applied:false`), de modo que **no produce drift** y no
toca `Area_comun/state/*.json`. No pasa por `submit_intent` (no es una transicion de estado): se anade
via `EventWriter.append_cost_attribution`, gateado por el flag, igual que las demas anotaciones.

**Flag.** `metrics.cost_attribution_enabled` en `protocol.config.json` (ausente => `false`). Con el
flag en `false`, `append_cost_attribution` no escribe nada: el event log queda **byte-equivalente**.
La emision es **explicita** (la llama el orquestador/wrapper al cierre de turno con la cifra de coste),
**no** automatica dentro de `submit_intent`: las transiciones normales quedan byte-identicas con el
flag on u off.

**Activacion en la instancia viva.** El TEMPLATE (`protocol.config.template.json`) se publica con el
flag en `false` (off-by-default, neutral). La instancia viva de este repo lo activa (`true`) para
capturar en caliente antes del piloto del loop -- mismo patron dogfooding que `compaction_enabled`
(DECISION-0030). No es un multiplicador de riesgo de los gateados (chain/firmas/anclaje/subagents/
SA.4/team_bridge): es una anotacion `applied:false`, sin mutacion de estado ni autonomia.

## Alcance / No-alcance

- **En alcance:** evento `cost.attributed`, constructor del registro, lectura/resumen
  (`by_handoff`/`by_decision`/`by_agent`), flag, golden determinista, activacion en la instancia viva.
- **Fuera de alcance:** export W3C PROV (PROV-AGENT, otra tarea), firma por agente (otra tarea),
  activacion del loop/SA.4. No se tocan `enforce`/`authoritative` ni `subagents_enabled`.

## Versionado y neutralidad (DECISION-0001)

Aditiva, off-by-default, sin remover ni cambiar comportamiento existente. **MINOR** (v1.6.0). Neutral
de dominio (imputacion generica de tokens; sin terminos de negocio); sin secretos. No afecta el
escritor unico (DECISION-0022): el estado de protocolo se sigue mutando solo por `submit_intent`; la
anotacion `cost.attributed` no muta estado.

## Consecuencias

- Antes del piloto del loop, cada handoff/decision/agente puede imputarse en caliente (leido del event
  log), no estimado a posteriori. Insumo directo para los topes de coste del loop (DECISION-0009/0024).
- El plano de protocolo nunca contiene el contenido del handoff/decision: solo su hash (seudonimo). No
  expone texto libre, pero NO es publicable como "anonimo": el enlace a la carga util retenida lo hace
  re-identificable (ver GATE-DATASET arriba).
- Maker != checker intacto: esto es instrumentacion de medicion, no una relajacion de autorizacion.
