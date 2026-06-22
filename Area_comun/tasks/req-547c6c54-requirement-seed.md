---
task_id: "REQ-547C6C54"
title: "UX: Indicador de ultima actualizacion y estado de refresco de datos"
type: "requirement"
status: done
owner: "Operador"
phase: "P2"
priority: "normal"
project: "Zeus-protocol"
author: "Operador"
relayed_by: "Arquitecto"
endorsement: "none"
sdd_role: "seed_only_architect_authors_spec"
---

# REQ-547C6C54 - UX: Indicador de ultima actualizacion y estado de refresco de datos

## Narrativa

Como operador quiero ver una indicacion de cuando se actualizaron por ultima vez los datos que estoy viendo (Ledger seq, estado del backlog, mailbox) para saber si lo que veo es fresco o puede estar desactualizado sin tener que interpretar manualmente los badges de integridad.

## Intencion de aceptacion

La barra de integridad o el pie de cada seccion debe mostrar hace cuanto se refresco el dato (ej: 'actualizado hace 30s'). Durante una carga activa debe mostrarse un spinner o indicador de progreso sutil. Si los datos son stale (mas de N segundos sin actualizar) el indicador debe cambiar de estado visualmente.

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
