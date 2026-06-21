---
task_id: "REQ-28118FC3"
title: "UX: Jerarquia tipografica en vistas Mailbox y Backlog"
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

# REQ-28118FC3 - UX: Jerarquia tipografica en vistas Mailbox y Backlog

## Narrativa

Como operador quiero que la jerarquia visual en Mailbox y Backlog priorice el asunto/titulo sobre el identificador tecnico (MSG-..., REQ-...) para procesar la informacion mas rapido. Actualmente el ID tecnico tiene el mismo peso visual que el cuerpo del mensaje.

## Intencion de aceptacion

En tarjetas del Mailbox: el asunto del mensaje debe ser prominente (mayor tamano o peso), el identificador MSG-... debe aparecer en texto secundario (mas pequeno, menor contraste). En tarjetas del Backlog: el titulo de la tarea es lo primero, el REQ-ID en formato secundario debajo.

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
