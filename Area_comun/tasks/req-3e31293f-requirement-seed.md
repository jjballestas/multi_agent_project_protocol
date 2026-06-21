---
task_id: "REQ-3E31293F"
title: "UX: Tooltips en codigos RF-N y acronimos tecnicos en todas las vistas"
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

# REQ-3E31293F - UX: Tooltips en codigos RF-N y acronimos tecnicos en todas las vistas

## Narrativa

Como operador quiero ver un tooltip con el nombre completo al hacer hover sobre cualquier codigo RF-N (RF-5, RF-14, etc.), acronimo tecnico (SDD, T0, HMAC, PII) o identificador de estado que aparezca en las vistas, para no tener que memorizar el glosario ni navegar al Help.

## Intencion de aceptacion

Al hacer hover sobre RF-5 debe aparecer: RF-5 - SDD task (crear tarea). Sobre SDD: Spec-Driven Development. Sobre T0: boundary de inicio del proyecto. Sobre HMAC: firma criptografica del evento. Los codigos deben ser interactivos (cursor pointer) en lugar de texto plano.

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
