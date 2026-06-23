---
task_id: "REQ-A54DAD73"
title: "Accion gobernada mailbox_send: compositor de mensajes Operador a agentes desde Operate/Mailbox"
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

# REQ-A54DAD73 - Accion gobernada mailbox_send: compositor de mensajes Operador a agentes desde Operate/Mailbox

## Narrativa

Como operador, quiero poder escribir y enviar mensajes a agentes (Arquitecto, Codex) directamente desde el front sin usar la terminal ni editar archivos a mano, ya que el canal Operador como from ya existe en el protocolo (19 mensajes previos con tipos INFO, CHANGES, DECISION, REVIEW) pero hoy no hay ninguna accion gobernada ni UI para emitirlos desde la consola.

## Intencion de aceptacion

Se agrega un nuevo intent kind mailbox_send al runtime/submit_intent con campos: from fijo Operador, to seleccionable entre agentes registrados, type seleccionable entre los tipos validos del Operador (INFO CHANGES DECISION REVIEW), taskId opcional, y body en texto libre ASCII. En el front aparece una nueva accion gobernada en Operate (o un boton Nuevo mensaje en la cabecera del Mailbox) que prepara y ejecuta este intent con el flujo dry_run -> confirmar -> enviado-atestado [DOC-REDACTED] al de Intake. El mensaje resultante queda en el mailbox open del destinatario como cualquier otro mensaje del protocolo. No se puede falsificar el from ni usar tipos de mensaje exclusivos de agentes. El envio fallido muestra el error sin limpiar el borrador.

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
