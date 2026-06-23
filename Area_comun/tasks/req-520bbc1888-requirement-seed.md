---
task_id: "REQ-520BBC1888"
title: "Proponer un agente que firma el ledger inicia una ceremonia, no un toggle"
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
source_file_sha256: 4eb704a9a9ad3344226cc8bdc1c9b2ec215385416abe8aa792a44a384507c2d2
extraction_task_id: "TASK-EXTRACT-1F5C13A7B5"
candidate_pre_edit_hash: "9b1ec32942010781d731859858135c311fb6c885ff509384dc5dedb81cdadec9"
---

# REQ-520BBC1888 - Proponer un agente que firma el ledger inicia una ceremonia, no un toggle

## Narrativa

Como operador, quiero que dar de alta un agente que firma el ledger se trate como una ceremonia gobernada con mi presencia, no como un boton, para no debilitar la seguridad de la atestacion.

## Intencion de aceptacion

el front puede preparar o proponer el alta, pero el alta efectiva exige la ceremonia de re-genesis con provisioning de clave y mi aprobacion explicita; nunca se activa un agente firmante con un simple interruptor.

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
- candidate_pre_edit_hash: 9b1ec32942010781d731859858135c311fb6c885ff509384dc5dedb81cdadec9

## Candidate PII Re-screen

- mode: best_effort
- guaranteed: false
- finding_count: 0
