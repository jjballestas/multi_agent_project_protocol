---
task_id: "REQ-B97838C6"
title: "UX: Backlog Kanban - colapsar columnas vacias y mostrar contenido de done"
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

# REQ-B97838C6 - UX: Backlog Kanban - colapsar columnas vacias y mostrar contenido de done

## Narrativa

Como operador quiero que el kanban del Backlog colapse o minimice las columnas que tienen 0 tareas (ready, in_progress, in_review) para reducir el ruido visual, y que la columna done muestre su contenido (actualmente done=40 pero no lista las tareas).

## Intencion de aceptacion

Las columnas con count=0 deberian mostrarse en modo compacto (solo cabecera, sin espacio vacio). La columna done deberia mostrar las tareas completadas o al menos un resumen paginado. El ancho del kanban deberia adaptarse al contenido real.

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
