---
task_id: "REQ-B6146E35"
title: "RC-04 Intake: modal revision prellenada para candidatas de archivo"
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

# REQ-B6146E35 - RC-04 Intake: modal revision prellenada para candidatas de archivo

## Narrativa

Como operador quiero que al pulsar Revisar sobre una candidata de la carpeta Pendientes el modal se abra con titulo Revisar requisito REQ-ID, modo bloqueado en Archivo, y todos los campos prellenados con los datos de la candidata; para verificar, editar y aprobar sin redigitar el contenido extraido por el Extractor.

## Intencion de aceptacion

1. Titulo del modal: Revisar requisito REQ-XXXXXXXX. 2. Radio Archivo bloqueado + chip [ADDR-REDACTED]. 3. [ADDR-REDACTED]. 4. Campos prellenados desde la candidata. 5. Tras Submit la tarjeta cambia estado a aprobado. Ref prototipo HTML seccion modal review.

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
