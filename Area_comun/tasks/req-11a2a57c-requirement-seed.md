---
task_id: "REQ-11A2A57C"
title: "Routing por hash URL en la navegacion lateral del front RF-1..RF-14"
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

# REQ-11A2A57C - Routing por hash URL en la navegacion lateral del front RF-1..RF-14

## Narrativa

Como operador, quiero que la URL del navegador refleje la seccion activa con un hash (ejemplo: #mailbox, #backlog, #intake) cuando navego por la barra lateral, para poder marcar como favorito una vista especifica, compartir un enlace directo a una seccion y usar el boton Atras del navegador para volver a la vista anterior sin perder el contexto.

## Intencion de aceptacion

Al hacer click en cualquier item de la sidebar la URL cambia a /#<vista> sin recargar la pagina. Al cargar la app con una URL que incluye hash valido (ej: /#mailbox), la vista correspondiente se activa directamente. El boton Atras del navegador navega a la vista anterior correctamente. Si el hash no corresponde a ninguna vista conocida la app carga la vista por defecto (dashboard) sin error. La barra lateral resalta el item activo segun el hash actual.

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
