---
task_id: "REQ-885632826E"
title: "Boton \"Enviar al Arquitecto\" en el Intake"
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
candidate_pre_edit_hash: "8c33afe77dc3b6f43089e5b6656e2ad409b170d7edb39222feec36e3b78166a2"
---

# REQ-885632826E - Boton "Enviar al Arquitecto" en el Intake

## Narrativa

Como operador, cuando monto un requisito en el Intake, quiero un boton que lo registre y ademas avise o despierte al Arquitecto, para que lo tome enseguida sin que yo tenga que hacer push manual ni esperar el sondeo.

## Intencion de aceptacion

al presionar, el requisito se registra por submit_intent y llega al canonico, y el Arquitecto recibe la notificacion por el mailbox y se activa si estaba dormido; el front indica que el requisito fue tomado.

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
- candidate_pre_edit_hash: 8c33afe77dc3b6f43089e5b6656e2ad409b170d7edb39222feec36e3b78166a2

## Candidate PII Re-screen

- mode: best_effort
- guaranteed: false
- finding_count: 1
