---
decision_id: DECISION-0028
title: enforce es el mecanismo de escritor-unico; authoritative es el marcador del modo (postura B, aclaracion de DECISION-0022)
status: accepted
date: 2026-06-10
ratified_at: 2026-06-10
deciders: [operador humano, Claude (architect)]
supersedes: []
superseded_by: []
relates_to: [DECISION-0022, DECISION-0026, TASK-0086, TASK-0087]
phase: P2
---

# DECISION-0028 - enforce = mecanismo de escritor-unico; authoritative = marcador del modo (postura B)

> ACEPTADA por el operador + arquitecto (2026-06-10). Resuelve TASK-0087 (ultimo bloqueante de ADOPCION,
> no de SA.4). Aclaracion/enmienda DOCUMENTAL de DECISION-0022. Aditiva, neutral de dominio, SIN cambiar
> defaults del template (sigue off-by-default). No es un flip de runtime ni un multiplicador.
> enforce/authoritative intactos; SA.4 y Capa C OFF.

## Contexto

DECISION-0022 introdujo el modo runtime-authoritative con cuatro flags
(`event_state.enabled/materialize/enforce/authoritative`). Al cablearlo en vivo quedo una pregunta
abierta (TASK-0087): bajo `authoritative=true`, conviene (A) cablear "teeth" propias de comportamiento
para `authoritative` (defense-in-depth), o (B) documentar que `enforce` es el mecanismo de escritor-unico
y `authoritative` un marcador declarativo del modo. La nota de v1.1.0 lo registro como bloqueante de
adopcion.

## Decision: POSTURA B

1. **`enforce` ES el mecanismo de escritor-unico.** Su hard-gate B.3 rechaza como drift cualquier edicion
   manual de `Area_comun/state/*.json`: la garantia "solo el runtime escribe el ledger" la provee
   `enforce`, no `authoritative`.
2. **`authoritative` es el MARCADOR declarativo** del modo runtime-authoritative (DECISION-0022). Formaliza
   que la instancia opera en ese modo, pero **no tiene callers de comportamiento propios**: no existe hoy
   un camino de codigo que cambie su decision en funcion de `authoritative` por separado de `enforce`.
3. **NO se cablean teeth propias para `authoritative`.** No hay hoy un invariante que `enforce` no cubra y
   que justifique la complejidad adicional. Anadir teeth duplicaria la garantia sin ganar seguridad.
4. **El false-secure ya esta muerto.** El guard de TASK-0086 (`authoritative => enforce => materialize =>
   enabled`, tier runtime) en el validador + `submit_intent` + `apply` RECHAZA `authoritative` sin
   `enforce`. Por tanto no es posible un estado "authoritative-sin-enforce" que aparente seguridad sin
   tenerla.

## Consecuencias

- Documental: los docs del protocolo (AGENTS.md seccion 7, Area_comun/protocol/TASK_PROTOCOL.md,
  Area_comun/protocol/N_AGENT_RUNTIME.md) y, donde describe el modo, AGENTS.template.md, usan el lenguaje
  "enforce = mecanismo, authoritative = marcador".
- CHANGELOG v1.1.0: la nota de "Open follow-up (blocking for adoption)" pasa a "resolved - posture B".
- Cierra TASK-0087 y, con ello, el ultimo bloqueante de ADOPCION.
- Reversibilidad/rollback del modo: sin cambios (apagar `enforce` y `authoritative` devuelve a edicion
  manual; la garantia se apaga con `enforce`).

## No-alcance

- NO cambia el comportamiento del runtime ni los defaults del template (off-by-default intactos).
- NO toca SA.4 ni Capa C (ambos OFF).
- Si en el futuro aparece un invariante que `enforce` no cubra y sea especifico de `authoritative`, se
  reabre con una DECISION nueva (esta no lo prohibe; solo constata que hoy no existe).
