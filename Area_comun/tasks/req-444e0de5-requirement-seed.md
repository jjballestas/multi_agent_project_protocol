---
task_id: REQ-444E0DE5
title: "Intake: cerrar el ciclo en la app (auto commit+push del cambio gobernado)"
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

# REQ-444E0DE5 - Intake: cerrar el ciclo en la app (auto commit+push del cambio gobernado)

## Narrativa

Como operador, tras confirmar un EXECUTE en el intake no quiero bajar a la terminal a hacer git add/commit/push; quiero que la app aterrice el cambio en canonico por mi, para operar sin salir del front.

## Intencion de aceptacion

Tras un EXECUTE exitoso la app commitea SOLO los archivos que escribio submit_intent (seed + ledger/state) con mensaje claro y pushea al remote configurado, como parte de la transaccion. Resultado atomico: "enviado + aterrizado en canonico (HEAD, seq)". Si el push falla -> error, NO verde (AC11). NO commitea cambios arbitrarios del working tree (add acotado; prueba negativa: un sucio ajeno no entra). Nueva superficie de transporte: el Arquitecto evalua si requiere DECISION.

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
