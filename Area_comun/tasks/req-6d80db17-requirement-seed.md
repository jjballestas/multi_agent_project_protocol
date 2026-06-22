---
task_id: "REQ-6D80DB17"
title: "UX: El sitio no refleja cambios nuevos del protocolo sin reiniciar el servidor"
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

# REQ-6D80DB17 - UX: El sitio no refleja cambios nuevos del protocolo sin reiniciar el servidor

## Narrativa

Como operador quiero que los nuevos commits aplicados al protocolo por Codex o el Arquitecto sean visibles en la consola sin necesidad de reiniciar el servidor Node (npm start), ya que actualmente el servidor carga el estado canonico al inicio y no detecta nuevos commits posteriores.

## Intencion de aceptacion

Tras un commit nuevo al repo, el servidor deberia detectar el cambio (via git poll o watcher) y actualizar el estado canonico que sirve a la UI sin requerir reinicio manual. El Ledger SEQ, backlog y artefactos deben reflejar el nuevo HEAD automaticamente.

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
