---
task_id: "REQ-A4B9FE80"
title: "UX: Chips visuales de estado y prioridad en tarjetas del Backlog RF-1"
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

# REQ-A4B9FE80 - UX: Chips visuales de estado y prioridad en tarjetas del Backlog RF-1

## Narrativa

Como operador, quiero que las tarjetas del kanban en Backlog muestren el estado (proposed, ready, in_progress, in_review, done) y la prioridad (normal, high) como chips o badges con color en lugar de texto plano gris, para distinguir de un vistazo las tarjetas urgentes o activas sin leer el texto de cada una.

## Intencion de aceptacion

Las tarjetas del kanban muestran un chip de prioridad con color diferenciado: high en amarillo/naranja, normal en gris neutro. El estado de la tarjeta tiene un color semantico consistente con los badges de la barra de integridad. Las tarjetas con prioridad high tienen una marca visual (borde izquierdo o badge) que las distingue incluso en la columna done. El estilo de los chips es coherente con el sistema de badges existente en la app (mismo border-radius, fuente, escala).

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
