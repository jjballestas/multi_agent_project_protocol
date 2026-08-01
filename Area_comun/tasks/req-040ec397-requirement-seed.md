---
task_id: "REQ-040EC397"
title: "Corregir contraste de texto en diagramas de Ayuda (manual-mermaid)"
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

# REQ-040EC397 - Corregir contraste de texto en diagramas de Ayuda (manual-mermaid)

## Narrativa

Como operador de la consola, quiero que el texto dentro de las cajas de los diagramas de la seccion Ayuda (bloques 4 a 7: Arquitectura, Mapa de la aplicacion y Flujo de accion gobernada) se muestre en un color [ADDR-REDACTED].

## Intencion de aceptacion

El texto de los elementos <text> dentro de los SVG .manual-mermaid-svg (cajas .manual-mermaid-node de los diagramas de Arquitectura, Mapa de la aplicacion y Flujo de accion gobernada) actualmente se ve en negro (fill por defecto) sobre un fondo oscuro (--surface-2), por lo que es casi ilegible. Se considera aceptado cuando ese texto tome un color [ADDR-REDACTED].manual-mermaid-svg), quedando legible en todas las cajas de los diagramas, sin romper el resto del estilo (bordes, flechas, lifelines).

## PII guard

- mode: structural
- channel: ascii
- free_text_public_plane: redacted
- warning_acknowledged: true
- redactions: 2

## Accountability

- author: Operador
- relayed_by: Arquitecto
- endorsement: none
