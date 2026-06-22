---
task_id: "REQ-31100EAF"
title: "carga de requerimiento por archivo"
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

# REQ-31100EAF - carga de requerimiento por archivo

## Narrativa

Como operador requiero que se habilite poder cargar archivos para usarlos comorequerimientos, de modo que pueda adjuntar un archivo en el Intake y su contenidoalimente un requerimiento gobernado sin tener que transcribirlo a mano.

## Intencion de aceptacion

Aceptado cuando, desde el Intake de la consola, el operador puede adjuntar un archivoy su contenido queda relevado como requerimiento gobernado que aterriza en canonicocon id y seq reales (sin preview-as-green, mismo camino que el intake actual).Condiciones:(1) solo el execute gobernado escribe;(2) ingestion acotada: allowlist de tipo y limite de tamano, nombre de archivo saneado (sin path traversal), contenido nunca ejecutado;(3) PII structural guard y ASCII-only aplicados al texto extraido del archivo;(4) idempotente: re-subir el mismo archivo no duplica;(5) si abre una superficie de ingreso nueva, nace OFF/gateada y reversible por flag.Honestidad: exito solo con el requerimiento realmente escrito.

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
