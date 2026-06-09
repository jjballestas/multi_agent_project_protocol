---
id: TASK-0087
owner: Claude
status: done
type: analysis
priority: normal
created_at: 2026-06-08
updated_at: 2026-06-08
depends_on: [TASK-0086]
relates_to: [TASK-0085, SPEC-0067]
phase: P2
spec_id: none
linked_decisions: [DECISION-0022]
objective: Decidir el rol definitivo del flag event_state.authoritative - (A) cablear teeth propias (defense-in-depth: que authoritative agregue enforcement adicional mas alla de enforce, p.ej. prohibir invariantes/escrituras que enforce no cubre, o un check de autoridad de escritor) vs (B) documentar oficialmente que ENFORCE es el mecanismo de escritor-unico y authoritative es solo el marcador declarativo del modo (DECISION-0022). Resolver con una DECISION.
expected_output: una DECISION (nueva o addendum a DECISION-0022) que fije la postura A o B; si A, un SPEC/TASK de implementacion de las teeth con su golden; si B, actualizar AGENTS.md/TASK_PROTOCOL/N_AGENT_RUNTIME para documentar enforce como el mecanismo y authoritative como marcador (evitando el false-secure ya mitigado por el guard de TASK-0086). En ambos casos, neutral y sin tocar defaults del template salvo decision.
question_to_resolve: Authoritative debe tener enforcement propio (defense-in-depth) o se documenta enforce como el unico mecanismo y authoritative como marcador? Lo decide el operador + arquitecto.
closure_criterion: DECISION registrada con la postura (A teeth / B documentar) + artefacto consecuente (SPEC/TASK de teeth, o docs actualizadas); coherencia con el guard de TASK-0086; neutral. BLOQUEANTE PARA ADOPCION (una instancia que adopte runtime-authoritative debe saber que garantiza authoritative), NO bloqueante para SA.4.
sdd_required: false
---

# TASK-0087 - Authoritative: teeth propias (defense-in-depth) vs documentar enforce como el mecanismo

> PROPOSED (registrada por Claude 2026-06-08 como follow-up del flip authoritative). **BLOQUEANTE PARA
> ADOPCION**, NO para SA.4. No arrancar hasta que el arquitecto/operador fijen la direccion (A o B).

## Contexto

Al flipear `authoritative=true` se verifico que el flag **no tiene callers de comportamiento**: la garantia
escritor-unico (JSON==log, edicion manual hard-failea) la provee **`enforce`** (gate B.3). `authoritative` es
hoy un **marcador declarativo** del modo runtime-authoritative (DECISION-0022). TASK-0086 ya mata el
false-secure (rechaza authoritative-sin-enforce). Falta decidir el rol DEFINITIVO de authoritative.

## Opciones

- **(A) Teeth propias / defense-in-depth:** cablear enforcement adicional que SOLO authoritative active (algo
  que enforce no cubra hoy): p.ej. un check de autoridad de escritor mas estricto, prohibir ciertas rutas de
  escritura directa adicionales, o invariantes extra. Pro: el flag "significa algo" por si mismo. Con: complejidad;
  hay que justificar QUE agrega sobre enforce sin redundar.
- **(B) Documentar enforce como el mecanismo:** declarar oficialmente que ENFORCE es el escritor-unico y
  authoritative es el marcador del modo; actualizar AGENTS.md/TASK_PROTOCOL/N_AGENT_RUNTIME. Pro: simple, honesto,
  refleja el codigo. Con: el flag es "solo" un marcador (mitigado: el guard impide false-secure).

## Por que bloquea ADOPCION (no SA.4)

Una instancia externa que adopte runtime-authoritative necesita saber **que garantiza** `authoritative` para no
confiar de mas. SA.4 (autonomia con invoker real) NO depende de esto: corre bajo el mismo enforce + sobre de
DECISION-0024; el rol de authoritative no cambia las paradas duras de SA.4.

## Cierre

DECISION con postura A o B + artefacto consecuente. Coherente con TASK-0086. Neutral.
