---
task_id: REQ-FB27AF72
title: "arrancamos con nova.budget:"
type: requirement
status: proposed
owner: Operador
phase: P2
priority: normal
project: Zeus-protocol
author: Operador
relayed_by: Arquitecto
endorsement: none
sdd_role: seed_only_architect_authors_spec
---

# REQ-FB27AF72 - arrancamos con nova.budget:

## Narrativa

Como cualquier usuario del front (no solo el operador experto), quiero una opcion Help en el menu que muestre ayuda DETALLADA de como funciona la metodologia y como usar la consola, para entender y operar sin conocimiento previo. Como cualquier usuario del front (no solo el operador experto), quiero una opcion Help en el menu que muestre ayuda DETALLADA de como funciona la metodologia y como usar la consola, para entender y operar sin conocimiento previo.

## Intencion de aceptacion

Hay un item Help en la nav; al abrirlo muestra una guia detallada y navegable: que es la consola, observar vs operar, submit_intent (escritor unico), dry_run vs execute/confirmacion, atestacion #4, las vistas, el intake, el pipeline SDD, y un glosario. Reusa el contenido de docs/MANUAL-operador.md como fuente. Honesto: refleja lo que la app HACE hoy, incluidas sus limitaciones (no documenta lo que no existe). Read-only: la vista no escribe estado. Conforme al design-system (dark-first, AC13).

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
