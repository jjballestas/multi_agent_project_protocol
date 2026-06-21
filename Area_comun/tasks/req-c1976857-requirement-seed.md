---
task_id: "REQ-C1976857"
title: "UX: Refrescar datos automaticamente al navegar entre secciones sin recargar la pagina"
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

# REQ-C1976857 - UX: Refrescar datos automaticamente al navegar entre secciones sin recargar la pagina

## Narrativa

Como operador quiero que al hacer click en cualquier opcion de la barra lateral (Dashboard, Mailbox, Backlog, Ledger, etc.) los datos de esa seccion se recarguen desde el servidor automaticamente, sin necesidad de recargar la pagina completa con F5 o el boton del navegador para ver el estado actualizado.

## Intencion de aceptacion

Cada vez que el operador navega a una seccion (click en nav lateral) la vista debe hacer fetch fresco al servidor y actualizar su contenido. El Ledger SEQ, el conteo del Backlog, el Mailbox y el estado de integridad deben reflejar el canonico actual sin obligar al operador a usar F5. Adicionalmente, seria deseable un boton de recarga manual por seccion y/o un refresco automatico por intervalo configurable.

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
