---
decision_id: DECISION-0039 (DRAFT - id final al promover)
title: Activacion gateada de la atestacion de autoria (#4) para instrumentar el modulo-app de Presupuesto - off->piloto->on + endurecimiento grado-tesis
status: draft (pendiente GO operador)
date: 2026-06-19
deciders: [operador humano (pendiente), Arquitecto]
supersedes: []
superseded_by: []
relates_to: [DECISION-0029, DECISION-0023, DECISION-0033, DECISION-0027, DECISION-0001, DECISION-0010]
phase: P2
---

# DECISION-0039 (DRAFT) - Activacion de la atestacion de autoria (#4)

> DRAFT del Arquitecto para revision (Analista + Codex en paralelo) y GO del operador. NO toca el
> ledger. Al recibir GO se promueve por `submit_intent` (intent `decision`) junto a SPEC-0081 y las
> tareas de activacion. SemVer: **MINOR** + CHANGELOG cuando se libere la activacion.

## Contexto

DECISION-0029 adopto la politica de "firmantes cruzados sin consenso" (atestacion de autoria con
adversario explicito) y dejo el mecanismo CONSTRUIDO off-by-default en tres piezas: prev_hash
encadenado (TASK-0101), firma por agente (TASK-0102), anclaje externo periodico (TASK-0103); TASK-0113
hizo segura la interaccion chain+auth. Hoy todo esta OFF en la instancia viva
(`chain_enabled`/`agent_signatures_enabled`/`anchor_enabled`/`event_auth.enabled` = false;
`signature_config.public_keys = {}`).

DECISION-0029 condiciono el ENCENDIDO a "SPEC cerrada + golden cases verdes + aprobacion explicita
posterior del operador". Esta decision es ese paso, motivado por una **necesidad real con fecha**
(regla 3.4): el modulo-aplicacion de Presupuesto se desarrollara bajo el protocolo e instrumentado
para la tesis; su dataset es la **coordinacion de agentes** (decisiones/handoffs/fallos/coste). El
**primer handoff real del modulo-app es T0 del dataset**, y debe quedar atestado en caliente.

**Restriccion de orden DURA (no negociable):** la cripto encadenada NO es retrofiteable. Si #4 se
enciende DESPUES del primer handoff, el historial previo no es atestable. Por eso #4 debe estar ON
antes del primer handoff real. Carril A va primero.

## Modelo de amenaza (clases de adversario - toda afirmacion de seguridad cita su clase)

Reusa DECISION-0029 sec. 3 y lo fija como contrato de la activacion:

- **A1 - Manipulacion post-hoc del log.** Alteracion puntual, borrado, insercion o reordenamiento de
  eventos ya escritos. Cubierto por prev_hash encadenado (TASK-0101).
- **A2 - Suplantacion de autoria entre agentes.** Un agente (o el runtime) atribuye a otro agente un
  turno/handoff que no produjo. Cubierto por firma por agente con llave privada FUERA del repo, que el
  runtime almacena y encadena pero NO puede producir (TASK-0102). La revision maker!=checker se
  registra como atestacion firmada del revisor.
- **A3-restringido - Reescritura por el runtime de historia ya anclada.** El escritor unico reescribe
  la cadena completa. Cubierto por anclaje externo periodico del digest de cabeza en un medio fuera de
  su control de escritura (TASK-0103). **Riesgo residual declarado:** omision de eventos AUN NO
  anclados (ventana entre ultimo evento y ancla). Mitigacion: ventanas de anclaje cortas + atestaciones
  huerfanas del revisor.
- **A4 - Operador humano malicioso.** FUERA DE ALCANCE. Tampoco se cubre: integridad bizantina,
  disponibilidad, prueba criptografica de identidad del MODELO. Sin clase asignada, no se afirma.

## Decision

1. **Autorizar la activacion gateada de #4** en la instancia viva, encendiendo las tres piezas
   (`chain_enabled`, `agent_signatures_enabled`, `anchor_enabled` y, como capa de compatibilidad,
   `event_auth.enabled`) bajo el plan off -> piloto -> on de la seccion siguiente. Vendor-neutral:
   firma Ed25519 local o keyless (patron DECISION-0023); anclaje configurable (remoto git
   independiente / transparency log / RFC 3161). Off-by-default se conserva en el template.

2. **Provisioning de identidad por agente.** Poblar `event_state.signature_config.public_keys` con la
   clave publica de cada agente del `agent_registry` (Arquitecto, Codex, y cualquier alta futura). Las
   **claves privadas viven FUERA del repo** (wrapper de cada agente), sin secretos en el repositorio
   (DECISION-0029 sec.5). Sin la llave publica registrada, la atestacion de ese agente no verifica.

3. **Criterio de instrumento sano (manipulation-check).** En runs legitimos, **>=99% de las
   atestaciones esperadas estan bien formadas y verificables** (definicion exacta y denominador en
   SPEC-0081). Por debajo de ese umbral el instrumento se declara roto y se vuelve a off (rollback). El
   instrumento debe ademas **detectar la mentira del adversario**: una atestacion forjada/alterada
   (A1/A2) DEBE ser rechazada por el validador (prueba negativa obligatoria en SPEC-0081).

4. **Dos planos / sin PII (DECISION-0033, reforzado por DECISION-0040/GATE-DATASET).** La atestacion
   firma el **hash** del artefacto (sujeto = `canonical_hash`); el predicado es agente / modelo-version
   / tarea / decision habilitante / `trust_boundary` de insumos. CERO texto libre, CERO PII de terceros
   en el event log. La firma no introduce datos nuevos de plano de payload.

5. **Una sola ventana de riesgo.** La activacion #4 es su propia ventana, con operador PRESENTE y
   rollback armado (los 4 flags a false). NO se combina con SA.4 (`real_invoker`/`supervised_autonomy`),
   ni con cambios de `authoritative`, ni con `subagents_enabled`, ni con Capa C (un multiplicador de
   riesgo por ventana).

6. **Regla de entrada SDD.** La activacion entra por SPEC-0081 (acceptance_criteria + test_plan +
   golden cases) + GO del operador antes de cada salto de fase del plan.

## Plan de activacion (off -> piloto -> on)

1. **OFF (hoy).** Mecanismo construido, flags false, `public_keys = {}`. Nada cambia.
2. **PROVISIONING.** Generar par de llaves por agente (privada fuera del repo); registrar publicas en
   `signature_config.public_keys`. Verificar: sin secretos en repo; cada agente firma con su llave.
3. **PILOTO (ventana supervisada).** Encender chain+firmas+anclaje en una ventana acotada con operador
   presente. Correr el manipulation-check sobre runs legitimos del propio protocolo (no del modulo-app
   todavia). Aceptacion: >=99% bien formadas + prueba negativa pasa + goldens verdes + drift 0.
   Rollback ensayado (4 flags a false restaura el estado dormido, byte-equivalente).
4. **ON.** Tras GO del operador sobre el resultado del piloto, dejar #4 ON en la instancia viva ANTES
   del primer handoff real del modulo-app. SemVer MINOR + CHANGELOG.

## Alcance / No-alcance

- **En alcance:** activar #4 en la instancia viva (no en el template); provisioning de llaves; el
  manipulation-check como instrumento; SemVer MINOR + CHANGELOG.
- **Fuera de alcance:** re-disenar el mecanismo (ya existe, DECISION-0029); encender SA.4 / Capa C /
  subagents; publicar/citar el dataset (eso es GATE-DATASET + GATE-INST + PRE-REG); tocar la DB de
  Budget o su migracion (corte limpio, DECISION-0001 + brief).

## Consecuencias

- El primer handoff del modulo-app queda atestado en caliente: el dataset de coordinacion nace con
  atestacion de autoria verificable (corazon del TFM, via G3.1 de DECISION-0029).
- El coste (tokens/latencia/bytes) entra en el presupuesto medible (#3 cost-attribution ya ON).
- Reversible: 4 flags a false dejan el mecanismo dormido sin perder historia.

## Alternativas consideradas

- **Encender sin piloto ni manipulation-check.** Descartada: sin medir "instrumento sano" no hay
  garantia de que las atestaciones del dataset sean validas; debilita la tesis.
- **Retrofitear atestacion al historial previo.** Imposible/deshonesto (la cadena no es retrofiteable);
  por eso el corte limpio empieza en el primer handoff del modulo-app.
- **Nueva decision de politica (duplicar DECISION-0029).** Descartada: la politica ya esta aceptada;
  esto es solo activacion + endurecimiento, referenciada a DECISION-0029.
