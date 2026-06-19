---
id: TASK-0124
title: Proyecto-front MVP etapa 1 - andamiaje (Zeus-protocol web + CI verde + lectura read-only del canonico) (DECISION-0049 / SPEC-0086)
type: product
status: ready
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0086
linked_decisions: [DECISION-0049, DECISION-0029, DECISION-0048, DECISION-0047]
created_at: 2026-06-19
---

# TASK-0124 - Proyecto-front MVP etapa 1 (andamiaje)

## Objective

T0 del proyecto-front (DECISION-0049). Etapa 1 (andamiaje) del MVP single-operator en el repo producto
`D:\Agentes\Zeus\Zeus-protocol` (ya git-init): stack web + pipeline CI verde (via connector CI del floor) +
**lectura read-only del estado/ledger del CANONICO** del protocolo (objetos git/origin, NO el working tree)
+ esqueleto de navegacion/base de componentes (segun diseno UI cuando aterrice). maker=Codex, checker=
Arquitecto. Ver SPEC-0086 (AC1-AC10) + requirements/pipeline en D:\Agentes\Zeus\design.

## Prerequisito (CI antes del codigo que compila/testea)

El connector **CI** del floor (DECISION-0048, deny-by-default, fixtures) es PREREQUISITO de esta etapa (CI
verde). El Arquitecto autora su SPEC como la siguiente pieza del floor; impleméntalo ANTES del codigo del
front que compila/testea. Git connector ya esta (TASK-0123).

## Alcance (SPEC-0086 etapa 1)

- Codigo SOLO en `Zeus-protocol` (producto, repo separado; acoplamiento unidireccional; NO tocar el core
  neutral). Gobernanza (esta task, handoffs) en el protocolo (atestada #4 = dataset).
- Lectura del protocolo por **patron read-only sobre el canonico**; NINGUNA escritura directa al estado/
  ledger (eso es etapa 3, y SIEMPRE via submit_intent; sin bypass de gates/#4/drift).
- CI verde como gate (RNF-8); neutralidad (RNF-6); PII-free (RNF-5); canal ASCII (RNF-11).

## DoD

SPEC-0086 AC aplicables a etapa 1 (AC1 read-only canonico, AC5 integridad de fuente, AC6 neutralidad/
acoplamiento, AC7 CI verde, AC10 gates del protocolo); maker=Codex/checker=Arquitecto; sin tocar #4/config
pinned; gobernanza en Area_comun valida (validate exit 0 con y SIN secretos, drift 0). Reporta a in_review
con claim file-scoped + submit_intent.

## Verification

- CI del producto verde (via connector CI); el front lee el canonico read-only (sin escrituras directas).
- `validate_collaboration_state.py --root .` (con y sin secretos) + scan_encoding + scan_domain_neutrality
  del protocolo exit 0; drift 0.
