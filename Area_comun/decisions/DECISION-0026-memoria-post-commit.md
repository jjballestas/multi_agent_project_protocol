---
decision_id: DECISION-0026
title: Regla de oro de memoria post-commit para todos los agentes
status: accepted
date: 2026-06-08
ratified_at: 2026-06-08
deciders: [operador humano]
supersedes: []
superseded_by: []
relates_to: [DECISION-0016, DECISION-0020, DECISION-0022]
phase: P2
---

# DECISION-0026 - Regla de oro de memoria post-commit

## Contexto

El protocolo depende de arranques frios confiables: cada agente debe poder reconstruir el estado real del
proyecto leyendo `AGENTS.md`, el estado compartido y su memoria privada. Cuando hay commits frecuentes, la
memoria privada queda obsoleta si no se actualiza junto con el cambio que acaba de entrar en git.

El operador humano establecio la regla el 2026-06-08:

```text
regla de oro para todos los agentes despues de cada commit deben actualizar su memoria
```

## Decision

Tras cada commit, todo agente debe actualizar su propia memoria persistente en `personal/<id>/` o su runbook
personal equivalente. La actualizacion debe capturar el contexto relevante del commit: que cambio, por que
importa, estado esperado despues del commit, mensajes/claims/tareas relevantes y cualquier restriccion nueva.

Un commit no se considera completamente cerrado para el agente hasta que su memoria queda actualizada.

## Alcance

- Aplica a todos los agentes registrados y al operador cuando actue como participante con area personal.
- No reemplaza los handoffs, mailbox, task files ni el ledger compartido; los complementa para mejorar el
  arranque frio y reducir perdida de contexto.
- No autoriza ediciones manuales de `Area_comun/state/*.json`. Con `event_state.enforce=true`, las transiciones
  de ledger siguen pasando por `submit_intent`.

## Consecuencias operativas

- Despues de un commit propio: actualizar memoria antes de empezar trabajo nuevo.
- Despues de observar un commit de otro participante que cambia el contexto esperado: actualizar memoria antes
  de actuar sobre ese nuevo estado.
- Si la memoria no puede actualizarse, dejar una nota explicita de bloqueo o avisar por mailbox si afecta a otro
  participante.
