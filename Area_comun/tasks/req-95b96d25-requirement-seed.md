---
task_id: "REQ-95B96D25"
title: "Boton \"Enviar al Arquitecto\" en el Intake"
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

# REQ-95B96D25 - Boton "Enviar al Arquitecto" en el Intake

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
