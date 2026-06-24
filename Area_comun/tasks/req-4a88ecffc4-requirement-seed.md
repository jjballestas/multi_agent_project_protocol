---
task_id: "REQ-4A88ECFFC4"
title: "Registrar un worker de producto y enlazarlo a un modelo"
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
source_file_sha256: 4eb704a9a9ad3344226cc8bdc1c9b2ec215385416abe8aa792a44a384507c2d2
extraction_task_id: "TASK-EXTRACT-1F5C13A7B5"
candidate_pre_edit_hash: "76bac2c7c56a8eca5e98df5a6bee090de60d927efa8040ec7462c862d8510969"
---

# REQ-4A88ECFFC4 - Registrar un worker de producto y enlazarlo a un modelo

## Narrativa

Como operador, quiero dar de alta desde el front un worker de producto (del tipo Extractor) y enlazarlo a un modelo de lenguaje (endpoint y nombre del modelo local), para sumar capacidades sin tocar el nucleo ni la firma del ledger.

## Intencion de aceptacion

el worker se registra fuera del config atestado (en un registro de workers de producto), con su propia clave, apagado por defecto; el alta no cambia el genesis ni el registro de agentes firmantes; el uso vivo del worker exige un permiso aparte.

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

## Procedencia

- source_file_sha256: 4eb704a9a9ad3344226cc8bdc1c9b2ec215385416abe8aa792a44a384507c2d2
- extraction_task_id: TASK-EXTRACT-1F5C13A7B5
- candidate_pre_edit_hash: 76bac2c7c56a8eca5e98df5a6bee090de60d927efa8040ec7462c862d8510969

## Candidate PII Re-screen

- mode: best_effort
- guaranteed: false
- finding_count: 0
