---
task_id: "REQ-68896287BC"
title: "Consola de prompts agente-a-agente desde el front"
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
candidate_pre_edit_hash: "d172a65982d5f7c15f31a2e55b6c2f8e5c022c27dede7c244d64420505ff2871"
---

# REQ-68896287BC - Consola de prompts agente-a-agente desde el front

## Narrativa

Como operador, quiero seleccionar un agente (Arquitecto, Codex, Analista o un worker) de un combo y enviarle un prompt escrito, y ver su respuesta dentro del front, para dirigir a los agentes sin abrir VS Code ni la terminal.

## Intencion de aceptacion

el prompt se envia como un mensaje gobernado al mailbox (destino: el agente elegido, canal ASCII, texto sensible redactado); el front muestra el hilo de conversacion (mi prompt mas las respuestas del agente) leyendo el mailbox; ningun mensaje escribe estado ni ledger fuera de submit_intent.

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
- candidate_pre_edit_hash: d172a65982d5f7c15f31a2e55b6c2f8e5c022c27dede7c244d64420505ff2871

## Candidate PII Re-screen

- mode: best_effort
- guaranteed: false
- finding_count: 0
