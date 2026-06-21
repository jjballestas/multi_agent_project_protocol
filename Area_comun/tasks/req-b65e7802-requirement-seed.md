---
task_id: REQ-B65E7802
title: "higienizar mensajes leidos/procesados con un click desde el front"
type: requirement
status: done
owner: Operador
phase: P2
priority: normal
project: Zeus-protocol
author: Operador
relayed_by: Arquitecto
endorsement: none
sdd_role: seed_only_architect_authors_spec
---

# REQ-B65E7802 - higienizar mensajes leidos/procesados con un click desde el front

## Narrativa

Como operador, quiero ver en el front mis mensajes ya leidos y procesados y archivarlos (higienizar) con un click, sin bajar a la terminal.

## Intencion de aceptacion

La vista Mailbox muestra los mensajes con su estado (open/answered/archived) y marca los consumidos; un boton "archivar" por mensaje emite el cambio de estado (open->archived + status del frontmatter) via submit_intent (relay ACOTADO, builder server-side), NUNCA edita el mailbox directo. Misma disciplina anti-impersonacion que el intake: extiende el conjunto de acciones permitidas del relay a "mailbox-archive" con forma estricta y PRUEBA NEGATIVA permanente (no reabrir el 403). Resultado atestado e idempotente; vista read-only salvo el archive gobernado. (Extiende DECISION-0052: nuevo intent acotado, no nuevo escritor.)

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
