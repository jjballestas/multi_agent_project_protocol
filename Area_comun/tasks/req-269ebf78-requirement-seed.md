---
task_id: "REQ-269EBF78"
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
---

# REQ-269EBF78 - Consola de prompts agente-a-agente desde el front

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
