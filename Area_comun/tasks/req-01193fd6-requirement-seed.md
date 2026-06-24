---
task_id: "REQ-01193FD6"
title: "RC-06 Intake: eliminar selector de modo y lista de candidatas de la vista standalone de extracci"
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

# REQ-01193FD6 - RC-06 Intake: eliminar selector de modo y lista de candidatas de la vista standalone de extracci

## Narrativa

Como operador quiero que la vista de extraccion por archivo no muestre el selector de modo Manual/Archivo ni el listado de candidatas; porque el selector ya existe en el header de la seccion y las candidatas se gestionan en la carpeta Pendientes aprobacion; para eliminar duplicacion de controles y reducir confusion.

## Intencion de aceptacion

1. NO radios de modo en la vista de extraccion por archivo. 2. NO listado de candidatas. 3. Solo uploader y estados de procesamiento. 4. Candidatas aparecen en carpeta Pendientes tras completar proceso.

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
