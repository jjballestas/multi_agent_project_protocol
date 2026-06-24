---
task_id: "REQ-16BDAA88"
title: "UX: Descripcion corta inline en cada accion gobernada de Operate RF-5..RF-10"
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

# REQ-16BDAA88 - UX: Descripcion corta inline en cada accion gobernada de Operate RF-5..RF-10

## Narrativa

Como operador, quiero que cada tarjeta de accion gobernada en la vista Operate muestre una linea de descripcion corta directamente visible (sin hover ni tooltip), para saber de un vistazo para que sirve cada accion sin tener que ir al Help a consultar la diferencia entre SDD task, GO/response, Agent run y Validation gate.

## Intencion de aceptacion

Cada tarjeta de accion gobernada muestra una descripcion de una linea (maximo 80 caracteres) debajo del titulo y encima del tipo de intent. La descripcion es texto estatico visible siempre, no requiere hover. El texto describe el caso de uso en lenguaje del operador, no el nombre tecnico del intent. Ejemplo: SDD task podria decir Prepara una tarea nueva a partir de una SPEC existente, GO/response podria decir Autoriza o responde un bloqueo activo. La adicion de estas descripciones no cambia el tamano de las tarjetas de forma significativa.

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
