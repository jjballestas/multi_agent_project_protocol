---
decision_id: DECISION-0065
title: Atestacion de autoria A2 sobre el camino vivo - submit_intent firma actor_auth Ed25519 (Camino B), off-by-default, secret-independiente, sin tocar genesis/#4
status: accepted
ratified_at: 2026-06-27
date: 2026-06-27
deciders: [operador humano, Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0029, DECISION-0039, DECISION-0046, DECISION-0040, DECISION-0033]
phase: P2
---

# DECISION-0065 - actor_auth Ed25519 en submit_intent (Camino B para A2 vivo)

> ACCEPTED (operador eligio Camino B, 2026-06-27). Extiende DECISION-0029/0039 (atestacion de autoria #4): cablea
> la firma Ed25519 por agente al **camino de escritura REAL** (submit_intent), para que el dataset del TFM lleve
> A2 no-repudiable sobre turnos vivos. Construccion **off-by-default** (sin riesgo); la ACTIVACION viva es una
> ventana de riesgo aparte con operador presente (DECISION-0039 §5). NO toca genesis/#4/config pinned. Repo = core
> (runtime/), neutral.

## Contexto

#4 esta ON (chain+HMAC+anchor) pero el `actor_auth` de los eventos vivos es `not_enforced_phase2`: la firma
**Ed25519 por agente** (A2, la contribucion) existe solo en el camino del orquestador (`llm_turn_wrapper` ->
`append_agent_attestation`, evento `agent.attestation`, gateado por `agent_signatures_enabled`), que requiere
`real_invoker`/`supervised_autonomy`. Pero los agentes escriben por `cron -> CLI -> submit_intent`, que NO pasa
`actor_auth` (-> default). Resultado: **A2 no opera sobre el dataset real**; sin eso no se mide H1/A2 (pre-registro
H1-H3 FROZEN v1.0, sha256 1ae10e05..., atestado en #4 seq 2124). El operador eligio el **Camino B** (minimo,
alineado con el modelo cron) sobre el Camino A (orquestador/real_invoker = ventana de maximo riesgo).

## Decision

1. **`submit_intent` firma `actor_auth` Ed25519.** Con el flag ON, carga la privada Ed25519 del `--actor-id` (de
   `D:/Agentes/protocol-secrets/`, FUERA del repo; path-safe; fail-closed si ausente) y escribe
   `actor_auth = {method:"ed25519", keyid, sig}` firmando el digest canonico del evento. La publica ya esta en
   `signature_config.public_keys`.
2. **Off-by-default.** Flag propio (p.ej. `event_state.actor_auth_enforce`) **OFF** en el config pinned. Sin flag,
   comportamiento ACTUAL intacto (`not_enforced_phase2` + HMAC `event_auth`) -- byte-identico. El flag no se commitea
   en ON; encenderlo es la ventana de riesgo (paso aparte).
3. **No-repudio / A2.** La privada vive fuera del repo: el runtime encadena pero NO puede producir la firma de otro
   agente. **Atribucion cruzada** (firmar como otro agente sin su privada) DEBE ser RECHAZADA por validate/replay
   (prueba negativa permanente). HMAC (`event_auth`, simetrica) se conserva como capa de integridad; Ed25519
   (`actor_auth`, asimetrica) anade el no-repudio frente al orquestador.
4. **Secret-independiente (DECISION-0046).** Verificar `actor_auth` exige solo la **publica** -> un clon limpio SIN
   secretos verifica (validate exit 0) y reproduce el mismo veredicto/hash; FIRMAR exige la privada (fail-closed).
   El hash canonico no depende de secretos.
5. **No toca genesis/#4/config pinned.** `actor_auth` es campo del evento; `genesis = canonical_hash(config)`
   (verificado) -> intacto. Eventos previos (`not_enforced_phase2`) siguen validos en replay; los nuevos llevan
   Ed25519; el chain/anchor/HMAC siguen ON. `protocol_version` (epoca) 1.14.0 sin cambio (DECISION-0047).
6. **Dos planos / sin PII (DECISION-0033/0040).** La firma cubre el digest/predicado; CERO texto libre / PII nueva.
7. **Activacion = ventana de riesgo unica** (operador presente, DECISION-0039 §5), separada de real_invoker/SA y de
   cambios de authoritative. El BUILD (off-by-default) no abre ventana. Rollback: flag -> false (vuelve a HMAC-only,
   sin perder historia).
8. **SDD:** SPEC-0103 + TASK-0190, maker=Codex / checker=Arquitecto (checker desde clon limpio, con/sin secretos).

## Alcance / No-alcance

- **En alcance:** `submit_intent` firma `actor_auth` Ed25519 off-by-default; golden + prueba negativa de atribucion
  cruzada + secret-independencia; el flag y su semantica; sin tocar genesis/#4/config pinned.
- **Fuera de alcance:** real_invoker/supervised_autonomy; re-cablear al orquestador (Camino A); la ACTIVACION viva
  (ventana del operador); generar/medir el dataset (eso es el experimento, post-cutover); tocar el mecanismo
  `append_agent_attestation` existente.

## Consecuencias

- El camino de escritura real de los agentes puede emitir A2 no-repudiable -> el dataset del TFM queda
  cruzado-firmado (corazon de H1/A2). Reversible (flag). Coste minimo (firma local por evento).
- Nota de consistencia: la "atestacion de autoria" medida pasa a ser `actor_auth` Ed25519 del evento de intent (no
  el evento `agent.attestation` del Camino A) -> el pre-registro emite una **v2.0** que lo fije ANTES de generar el
  dataset (sigue siendo pre-medicion, legitimo).

## Alternativas consideradas

- **Camino A (orquestador/real_invoker):** el diseno "rico"; descartado para el dataset por abrir la ventana de
  maximo riesgo y cambiar el modelo de operacion. Queda como modo futuro.
- **Dejar HMAC solo:** no da no-repudio asimetrico frente al orquestador -> no sostiene la afirmacion A2. Descartado.
