---
task_id: "REQ-4120B017"
title: "UX: Tooltips explicativos en badges de la barra de integridad"
type: "requirement"
status: proposed
owner: "Operador"
phase: "P2"
priority: "normal"
project: "Zeus-protocol"
author: "Operador"
relayed_by: "Arquitecto"
endorsement: "none"
sdd_role: "seed_only_architect_authors_spec"
---

# REQ-4120B017 - UX: Tooltips explicativos en badges de la barra de integridad

## Narrativa

Como operador quiero ver tooltips explicativos al hacer hover sobre cada badge de la barra de integridad (epoch, drift, attested, canonical, validator exit) para entender su significado sin tener que consultar el Help.

## Intencion de aceptacion

Al hacer hover en cada badge debe aparecer un tooltip corto: que valor es normal, que significa cuando cambia, y cuando debo preocuparme. Por ejemplo drift=0 es OK, drift>0 requiere atencion.

## PII guard

- mode: structural
- channel: ascii
- free_text_public_plane: redacted
- warning_acknowledged: true
- redactions: 0

## Accountability

- author: Operador
- relayed_by: Arquitecto
- endorsement: none
