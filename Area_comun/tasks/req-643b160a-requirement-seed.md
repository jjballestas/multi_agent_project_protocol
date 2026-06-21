---
task_id: REQ-643B160A
type: requirement
status: proposed
owner: Operador
phase: P2
priority: high
project: Zeus-protocol
author: Operador
relayed_by: Arquitecto
endorsement: none
sdd_role: seed_only_architect_authors_spec
file: Area_comun/tasks/req-643b160a-requirement-seed.md
---

# REQ-643B160A - Bug: el Intake crea un requerimiento fantasma desde texto de ejemplo/placeholder

## Narrativa

Como operador no quiero que el Intake persista textos de ejemplo/placeholder como requerimientos reales.
Aparecio REQ-984A85C6 "Conciliar saldos por cuenta al cierre mensual" con narrativa e intencion de aceptacion
vacias, que yo no escribi: un mensaje generico de ejemplo que no deberia convertirse en requerimiento (ya
cancelado por prune).

## Intencion de aceptacion

El Intake nunca debe crear un requerimiento a partir de texto placeholder/ejemplo. Un EXECUTE solo procede con
narrativa e intencion de aceptacion reales y no vacias (validacion que rechaza campos vacios o iguales al
placeholder, sin preview-as-green). Ademas el proyecto destino debe elegirse explicitamente y no defaultear a
Zeus-protocol.

## Accountability

- author: Operador
- relayed_by: Arquitecto
- endorsement: none
