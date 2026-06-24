---
task_id: "REQ-FA303A81"
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

# REQ-FA303A81 - RC-03 Intake: modal modo Manual con formulario para nuevo requisito

## Narrativa

Como operador quiero que el modal de nueva historia/requisito en modo Manual muestre: barra de modo en una fila (radio+label Manual | radio+label Archivo), proyecto+titulo en grid 2 columnas, narrativa, intencion de aceptacion y [ADDR-REDACTED]; y que los requisitos creados por este flujo queden en estado Borrador (no Pendiente aprobacion); para tener un flujo de captura manual limpio y sin ambiguedad de estado inicial.

## Intencion de aceptacion

1. La barra de modo ocupa una fila: etiqueta Modo de captura, luego radio+label Manual contiguos, divisor vertical, radio+label Archivo contiguos. 2. Proyecto y titulo en grid 2 columnas. 3. Narrativa full-width. 4. Intencion de aceptacion full-width. 5. [ADDR-REDACTED]. 6. Footer: meta firmante a la izquierda, Cancelar y Preview a la derecha. 7. Al completar el wizard y ejecutar Submit, el requisito se crea en estado borrador. 8. El modo seleccionado en el header se refleja en el modal al abrirse. Referencia visual: prototipo HTML adjunto seccion modal form-manual.

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
