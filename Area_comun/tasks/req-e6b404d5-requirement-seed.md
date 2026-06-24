---
task_id: "REQ-E6B404D5"
title: "RC-05 Intake: modal por archivo solo uploader sin lista de candidatas"
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

# REQ-E6B404D5 - RC-05 Intake: modal por archivo solo uploader sin lista de candidatas

## Narrativa

Como operador quiero que el modal en modo Archivo muestre unicamente la zona de drop del archivo, los estados procesando/ok/error y el boton Aceptar tras exito; sin mostrar formulario manual ni lista de candidatas; para tener un flujo de ingesta por archivo limpio y sin duplicacion de informacion.

## Intencion de aceptacion

1. Solo zona de drop con formatos aceptados. 2. Estado procesando amarillo. 3. Estado OK verde con nombre y cantidad de candidatas. 4. Error rojo con descripcion del error. 5. Boton Aceptar solo en estado OK. 6. Al Aceptar el modal cierra y las candidatas aparecen en carpeta Pendientes. Ref prototipo HTML seccion modal archivo.

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
