---
task_id: TASK-0309
file: Area_comun/tasks/TASK-0309-mermaid-text-contrast-front.md
title: "Front Zeus-protocol: contraste de texto legible en diagramas manual-mermaid de la seccion Ayuda (SPEC-0111 / REQ-040EC397)"
status: ready
type: product
owner: Codex
reviewer: Analista
priority: normal
project: Zeus-protocol
spec_id: SPEC-0111
relates_to:
  - REQ-040EC397
  - SPEC-0111
created_at: 2026-08-02
intake:
  type: fix
  goal: >
    Corregir el contraste ilegible del texto en los diagramas manual-mermaid de la seccion Ayuda del panel
    Zeus-protocol (bloques Arquitectura, Mapa de la aplicacion, Flujo de accion gobernada). El texto de los nodos
    se renderiza negro (fill SVG por defecto) sobre fondo oscuro (--surface-2) porque no hay regla de fill de
    texto; debe tomar un color claro del design system legible (var(--text) #e6edf3), sin alterar cajas, bordes,
    aristas, flechas ni lifelines. Implementar en el repo de producto D:\Agentes\Zeus\Zeus-protocol.
  acceptance:
    - "AC1 (legibilidad): el texto de los nodos (<text> dentro de .manual-mermaid-svg) se renderiza con color claro del design system (var(--text) #e6edf3 o token equivalente), NO negro; las cajas de los 3 diagramas de Ayuda quedan legibles."
    - "AC2 (contraste): ratio de contraste del texto sobre --surface-2 (#1c2330) >= WCAG AA (>=4.5:1); declarar par color/fondo y ratio en el handoff."
    - "AC3 (sin regresion): cajas (fill --surface-2, stroke #2e4a7a), aristas/lifelines (stroke --accent), flechas (fill --accent) y bordes sin cambio de estilo; el cambio se limita al fill del texto; sin tocar otros paneles."
    - "AC4 (contrato estatico): tests/staticContract.test.js extendido para ASERTAR la regla de fill de texto legible del SVG manual-mermaid (p.ej. .manual-mermaid-svg text con fill var(--text)); FALLA sin el fix, PASA con el."
    - "AC5 (gates producto): npm test del repo Zeus-protocol exit 0 en clon limpio; sin nuevos warnings."
  verification_cmd:
    - "cd D:/Agentes/Zeus/Zeus-protocol && npm test"
  scope_routes:
    - public/styles.css
    - tests/staticContract.test.js
  out_of_scope: >
    Cambiar layout/estructura/contenido de los diagramas o del manual; color de cajas/aristas/flechas; otros
    paneles o estilos; cualquier archivo del hub (protocolo). Solo el fill del texto del SVG manual-mermaid.
  risk: low
  estimate: S
notes: >
  Operacionaliza REQ-040EC397 (autor Operador; sdd_role seed_only_architect_authors_spec -> spec redactado por el
  Arquitecto: SPEC-0111). Repo de producto Zeus-protocol; gobernanza en el hub. El color concreto del seed quedo
  redactado por el PII guard -> el spec elige var(--text) (#e6edf3), coherente con el design system. Gate del
  Analista: verificar el RENDER (imagen de los 3 diagramas + contraste), no solo el string (leccion checker
  verify-rendered-not-just-text).
---

# TASK-0309 - Contraste de texto en diagramas manual-mermaid (front Zeus-protocol)

## Contexto
REQ-040EC397 del operador. En public/styles.css, .manual-mermaid-node pinta la caja con fill: var(--surface-2)
(oscuro) pero no hay regla de fill para los <text> -> negro por defecto -> ilegible. Ver SPEC-0111 para el
diagnostico completo y el fix (una regla CSS: .manual-mermaid-svg text { fill: var(--text); }).

## Entregable
- public/styles.css: regla de fill de texto legible del SVG manual-mermaid.
- tests/staticContract.test.js: asercion AC4.
- Handoff con par color/fondo + ratio de contraste + screenshot de los 3 diagramas.
