---
task_id: "REQ-CD4CE3F1"
title: "UX: Agrupacion temporal y filtros en la bandeja Mailbox RF-2"
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

# REQ-CD4CE3F1 - UX: Agrupacion temporal y filtros en la bandeja Mailbox RF-2

## Narrativa

Como operador, quiero que la bandeja Mailbox agrupe los mensajes answered y archived por periodos de tiempo (hoy, esta semana, este mes, anteriores) y tenga un filtro por direccion de mensaje (Codex a Claude / Claude a Codex), para orientarme rapidamente en 120 mensajes sin tener que recorrer el scroll completo.

## Intencion de aceptacion

Los mensajes answered y archived se muestran agrupados bajo encabezados de fecha colapsables. El filtro por direccion muestra solo los mensajes de la direccion seleccionada. Cada grupo colapsado muestra el contador de mensajes que contiene. El grupo del periodo actual (hoy, esta semana) aparece expandido por defecto. Al seleccionar un filtro el agrupamiento temporal se mantiene sobre el subconjunto filtrado.

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
