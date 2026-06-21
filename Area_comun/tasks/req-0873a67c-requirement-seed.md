---
task_id: "REQ-0873A67C"
title: "UX: Boton Nueva historia/requisito no resetea el formulario del Intake"
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

# REQ-0873A67C - UX: Boton Nueva historia/requisito no resetea el formulario del Intake

## Narrativa

Como operador quiero que al hacer click en el boton Nueva historia/requisito el formulario del Intake se limpie completamente (todos los campos vacios, checkbox desmarcado, wizard en paso 1) para poder iniciar un nuevo requisito desde cero sin datos del draft anterior.

## Intencion de aceptacion

Al pulsar el boton: titulo vacio, narrativa vacia, intencion de aceptacion vacia, proyecto destino en valor por defecto, checkbox PII desmarcado, wizard en paso 1, sin resultados de preview ni submit anteriores visibles.

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
