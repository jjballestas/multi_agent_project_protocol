---
task_id: "REQ-07DD94CE"
title: "UX: Busqueda y filtro por texto en la vista Artifacts RF-3"
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

# REQ-07DD94CE - UX: Busqueda y filtro por texto en la vista Artifacts RF-3

## Narrativa

Como operador, quiero un campo de busqueda por texto libre en la vista Artifacts que filtre en tiempo real las listas de decisions, specs, tasks, handoffs y reports, para encontrar un artefacto especifico sin tener que recorrer visualmente listas de 58 a 80 items.

## Intencion de aceptacion

Al escribir en el campo de busqueda solo se muestran los items cuyo ID o nombre contenga el texto ingresado (case-insensitive). El filtro actua sin necesidad de pulsar Enter. Al borrar el campo se restauran todos los items. El campo muestra un placeholder que indica como usarlo. El contador de cada seccion (ej: decisions 59) refleja el numero de items visibles tras el filtro.

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
