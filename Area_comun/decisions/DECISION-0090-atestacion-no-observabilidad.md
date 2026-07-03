---
decision_id: DECISION-0090
title: "Posicionamiento (linea roja): la propuesta de Aegis es ATESTACION criptografica del ciclo multi-agente, NO observabilidad/telemetria; la distincion se mantiene explicita en todo material publicable"
status: accepted
date: 2026-07-04
deciders: [operador humano, Arquitecto]
supersedes: []
supersedes_partial: []
superseded_by: []
relates_to: [DECISION-0089, DECISION-0087, DECISION-0088, DECISION-0022, DECISION-0050, GOAL-VISION-NOVA-001]
phase: P2
scope: positioning
carril: B
approval_ref: "Aprobada por el Operador (John Ballestas) 2026-07-04 (aprobacion interactiva 'aprobadas' de los drafts 0089/0090). Origen: R-EXT-07 de F1.6. Posicionamiento del material publicable, NO cambio de doctrina interna (el core ya HACE atestacion)."
---

# DECISION-0090 - Linea roja: atestacion != observabilidad

> Carril B (posicionamiento del spec/preprint/material comercial). NO cambia la doctrina interna: el core
> ya HACE atestacion; esta DECISION fija como se DICE hacia afuera para no diluir la propuesta.

## Contexto

R-EXT-07 (F1.6) barrio el mercado: hay mucho producto de OBSERVABILIDAD/eval de agentes (Braintrust,
LangSmith, Arize, Patronus: traces y scores, logging convencional) y de gateways MCP/politicas (MintMCP,
Lasso, Arthur, Credo). NINGUNO ofrece atestacion criptografica del ciclo MULTI-AGENTE. Ese espacio es
whitespace. El riesgo de posicionamiento es que el mercado nos lea como "otra herramienta de
observabilidad", diluyendo exactamente el diferenciador.

## Decision

1. **Linea roja de posicionamiento:** la evidencia de Aegis es ATESTADA y ENCADENADA -- firmada,
   content-addressed, verificable por un TERCERO en clon limpio sin confiar en el emisor (cadena #4;
   R-EXT-04). NO es telemetria, NO son traces, NO son scores de un juez. "Atestacion criptografica del
   ciclo multi-agente" es la categoria; "observabilidad" NO lo es.

2. **Distincion explicita en TODO material publicable.** Spec de referencia, preprint, README, material
   comercial: cada uno declara la distincion atestacion-vs-telemetria y por que traces/scores no son
   atestacion (no verificables por terceros, no encadenados, no firmados, editables sin deteccion).

3. **Criterio operativo de la distincion (para no quedarse en eslogan):** un artefacto es ATESTADO si y
   solo si (a) esta firmado por una sesion/actor identificado, (b) esta encadenado (content-addressed,
   append-only, tamper-evident: cadena #4), y (c) un externo lo verifica en clon limpio en pocos comandos
   (R-EXT-04). Si falla cualquiera de las tres, es telemetria/logging, no atestacion. Este criterio se cita
   en el material como la prueba de la linea roja.

4. **Mapping, no dilucion.** Se PUEDE hablar el idioma de observabilidad para interoperar (p.ej. exportar
   trazas OTel de producto, per SPEC-NOVA-P6-003), pero SIEMPRE marcando que la traza OTel es telemetria de
   PRODUCTO y NO la evidencia atestada del ciclo. Las dos capas se nombran distinto y no se confunden.

## Alcance y limites

- Es posicionamiento del material EXTERNO; no altera el core ni ninguna capability. El core ya cumple los
  tres criterios del punto 3.
- Interactua con DECISION-0089 (que se publica) y con R-EXT-01 (mapping Plan/Generation/Approval de Hinds)
  y R-EXT-06 (mapping SOC2/ISO): el mapping a estandares externos NO diluye la linea roja, la vocaliza en su
  idioma.
- **Seguimiento (GAP-5 del ensayo del sello, RUNBOOK-ENSAYO-atestacion-sello-etapa1.md):** el hub no tiene
  un intent de atestacion de PRIMERA CLASE (`attest {artifact, sha256}`); hoy se usa el vehiculo `decision`.
  Si se formaliza "atestacion" como categoria, conviene un primitivo explicito. Candidato de diseno de Carril
  B; NO bloquea esta DECISION.

## Consecuencias

- (+) La propuesta no se diluye a "otra observabilidad"; el whitespace queda defendido.
- (+) Criterio falsable (punto 3) que un tercero puede aplicar para distinguirnos de los competidores.
- (-) Exige disciplina de mensaje: cada material debe repetir la distincion (costo de redaccion, no de
  producto).
