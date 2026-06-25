---
task_id: "REQ-7095D30A"
title: "registro de requerimientos por dictado"
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

# REQ-7095D30A - registro de requerimientos por dictado

## Narrativa

yo como operador quiero tener una opcion en la cual pueda dictar o escribir una necesidad luego esta necesidad seria enviada al extractor asi como se envia en este momento la carga por archivos y lo reciba el extractor y convierta la necesidad en requerimientos.la opcion de necesidad estaria al lado de la opcion manual en el panel inicial de intake y se lanzaria de igual forma en un formulario aparte que tendria un text area grande con la opcion de capturar por microfono como las mismas funcinalidades que el mic de la opcion de requerimiento manual.pero tendria la seccion de botoness como la de los requerimientos por archivo

## Intencion de aceptacion

esta opcion se aceptara cuando:1.permita al usuario dictar las necesidades se pueda capturar la informacion en el textarea 2.permita al usuario dictar las necesidades se pueda capturar la informacion en el texto area 3.la necesidad capturada se puede enviar al extractor 4.el extractor convierta estas necesidades en requerimientos formalmente constituidos 5.el usuario los pueda aceptar rechazar enviar al instructor como actualmente se hace con las opciones que se generan desde la carga de requerimiento por archivos.

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
