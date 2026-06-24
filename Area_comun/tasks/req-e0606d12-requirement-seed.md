---
task_id: "REQ-E0606D12"
title: "RC-03 Intake: modal modo Manual con formulario para nuevo requisito"
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

# REQ-E0606D12 - RC-03 Intake: modal modo Manual con formulario para nuevo requisito

## Narrativa

Como operador quiero que el modal de nueva historia en modo Manual muestre barra de modo en una fila (radio+label Manual | radio+label Archivo), campos proyecto y titulo en grid 2 columnas, narrativa, intencion de aceptacion y [ADDR-REDACTED]; y que los requisitos creados por este flujo queden en estado Borrador; para tener un flujo de captura manual limpio y sin ambiguedad de estado inicial.

## Intencion de aceptacion

1. Barra de modo: etiqueta + radio+label Manual contiguos + divisor + radio+label Archivo contiguos, todo en una fila. 2. Proyecto y titulo en grid 2 columnas. 3. Narrativa y Intencion full-width. 4. [ADDR-REDACTED]. 5. Footer: meta firmante izquierda, Cancelar y Preview derecha. 6. Al ejecutar Submit el requisito queda en estado borrador. 7. El modo del header se preselecciona en el modal.

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
