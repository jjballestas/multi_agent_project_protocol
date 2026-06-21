---
task_id: TASK-0144
title: "Proyecto-front (UX): render de diagramas Mermaid en la vista Help (SVG) sin agregar dependencia de servidor (AC33, SPEC-0086 ext7)"
type: product
status: ready
owner: Codex
phase: P2
priority: normal
spec_id: SPEC-0086
linked_decisions: [DECISION-0049]
created_at: 2026-06-21
maker: Codex
checker: Arquitecto
code_repo: D:/Agentes/Zeus/Zeus-protocol
file: Area_comun/tasks/TASK-0144-codex-front-mermaid-help.md
---

# TASK-0144 - Render Mermaid en Help (SPEC-0086 ext7, AC33; REQ-D2C6579F)

> maker=Codex / checker=Arquitecto. Codigo en Zeus. UX READ-ONLY. #5 del PLAN. carry AC11/AC12/AC13/AC17.

## Alcance
1. Los bloques Mermaid de las secciones 4/5/6/7 del Help se renderizan como diagramas (SVG), no texto crudo.
2. SIN agregar dependencia de servidor / npm install: vendorizar la lib mermaid como asset estatico servido por
   el propio server, o SVG pre-generado. Preserva la propiedad "sin dependencias" de la consola.

## DoD
- AC33 verde con test de COMPORTAMIENTO permanente (el panel Help no muestra el codigo mermaid crudo de esos
  bloques; render presente; el server sigue sin deps de npm). Carry AC11/AC12/AC13/AC17. Read-only.
- node --test/CI verde; #4 byte-identica; validate con/sin secretos exit 0; drift 0; neutralidad/encoding limpio.
  Reproducido por el checker desde clon limpio; maker!=checker. Commit como Arquitecto + Co-Authored-By: Codex.

## Fuera de alcance
- Agregar mermaid como dependencia de npm en el server (la consola es "sin dependencias"; vendorizar o pre-render).
- Cualquier superficie de escritura.
