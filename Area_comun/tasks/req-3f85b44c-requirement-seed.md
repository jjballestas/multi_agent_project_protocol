---
task_id: "REQ-3F85B44C"
title: "RC-02 Intake: dashboard de carpetas en pantalla principal"
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

# REQ-3F85B44C - RC-02 Intake: dashboard de carpetas en pantalla principal

## Narrativa

Como operador quiero que la pantalla principal de la seccion Intake muestre un dashboard de carpetas (Pendientes aprobacion, Borrador, En Preview, Aprobados) con contadores, y debajo la lista de requisitos de la carpeta activa; eliminando la tarjeta actual de borrador/Mis-requisitos; para tener visibilidad inmediata del estado de mis requisitos sin navegar a otras pantallas.

## Intencion de aceptacion

1. Se muestran exactamente 4 carpetas en grid horizontal: Pendientes aprobacion (badge rojo con conteo), Borrador (badge azul), En Preview (badge amarillo), Aprobados (badge verde). 2. Cada carpeta tiene icono + nombre + descripcion breve + badge de conteo. 3. Por defecto se selecciona Pendientes aprobacion al cargar la vista. 4. Al hacer [ADDR-REDACTED]. 5. Cada tarjeta de requisito muestra: icono de estado, titulo, id+fecha+proyecto+origen, badge de estado y boton Revisar/Submit (solo para Pendientes) o accion correspondiente. 6. Se elimina la tarjeta borrador/Mis-requisitos actual. Referencia visual: prototipo HTML adjunto seccion folders-grid y req-list.

## PII guard

- mode: structural
- channel: ascii
- free_text_public_plane: redacted
- warning_acknowledged: true
- redactions: 1

## Accountability

- author: Operador
- relayed_by: Arquitecto
- endorsement: none
