---
task_id: "REQ-D2C6579F"
title: "UX: Renderizar diagramas Mermaid en la vista Help"
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

# REQ-D2C6579F - UX: Renderizar diagramas Mermaid en la vista Help

## Narrativa

Como operador quiero que los diagramas de arquitectura y flujo de la vista Help se muestren visualmente renderizados (flowchart, sequenceDiagram) en lugar de mostrar el codigo fuente Mermaid en texto plano, para poder entender la arquitectura y flujos sin conocer la sintaxis.

## Intencion de aceptacion

Las secciones 4 (arquitectura), 5 (mapa de la app), 6 (flujo gobernado) y 7 (intake) del Help contienen bloques Mermaid que aparecen como texto crudo. Deberian renderizarse como diagramas SVG usando la libreria mermaid.js. Si no es posible en el servidor, al menos mostrar una imagen estatica pre-generada.

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
