---
task_id: "REQ-E782911A"
title: "Compositor de mensajes del Operador a agentes desde el Mailbox del front RF-2"
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

# REQ-E782911A - Compositor de mensajes del Operador a agentes desde el Mailbox del front RF-2

## Narrativa

Como operador, quiero poder escribir y enviar un mensaje directamente a un agente especifico (Arquitecto, Codex, Analista) desde el front sin salir de la consola, para darles contexto, corregir una direccion de trabajo o responder a una situacion en curso sin tener que editar archivos del mailbox a mano ni usar la terminal.

## Intencion de aceptacion

El Mailbox muestra un boton Nuevo mensaje o compositor inline que permite seleccionar el agente destinatario (Arquitecto, Codex, Analista), escribir el cuerpo del mensaje en texto libre, opcionalmente asociar el mensaje a una tarea existente (taskId), y elegir el tipo de mensaje (DIRECTIVE, GO, ACK u OPERATOR_NOTE). El envio se ejecuta como una accion gobernada via submit_intent con un nuevo intent kind mailbox_send (o el equivalente canonico que defina el Arquitecto), firmado por Operador como from y el agente elegido como to. El mensaje queda registrado en el ledger atestado como cualquier otro evento. El compositor no permite editar mensajes ya enviados ni suplantar el from de otro agente. El campo de texto tiene al menos 6 rows visibles. El envio fallido muestra el error real sin limpiar el borrador.

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
