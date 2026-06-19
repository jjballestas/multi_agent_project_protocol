---
id: TASK-0117
title: Activacion gateada de la atestacion de autoria (#4) - provisioning + piloto + encendido (DECISION-0039 / SPEC-0081)
type: security
status: proposed
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0081
linked_decisions: [DECISION-0039, DECISION-0029, DECISION-0033]
created_at: 2026-06-19
---

# TASK-0117 - Activacion gateada de #4 (atestacion de autoria)

## Objective

Implementar el provisioning y la activacion gateada (off -> piloto -> on) del mecanismo #4 (prev_hash +
firma por agente + anclaje externo), ya construido off-by-default, segun SPEC-0081 y DECISION-0039.

## GATEADA - no se arranca con esta promocion

`status: proposed`. El **encendido** (poner flags en true) es un **GO POSTERIOR del operador** tras el
piloto, en su propia ventana de riesgo (sin SA.4 / authoritative-teeth / subagents / Capa C). Esta tarea
queda en backlog hasta ese GO. **#4 sigue OFF.**

## Alcance (ver SPEC-0081 para acceptance_criteria + test_plan)

- Provisioning (AC1): `event_state.signature_config.public_keys` por agente; `event_auth.keys`;
  `anchor_config.remote_url`/proof backend; claves privadas FUERA del repo; smoke de provisioning.
- Salud del instrumento (AC2): `attestation_health_cases`, tasa >=99% con denominador del event log;
  reporte declara "salud, no seguridad".
- Seguridad (AC3): prueba negativa binaria, 6 vectores (alteracion/borrado/insercion/reordenamiento/
  llave no registrada/atribucion cruzada), golden por vector.
- Rollback (AC5) + gates verdes (AC6).

## DoD

SPEC-0081 AC1-AC6 cumplidos; piloto pasado con GO del operador; #4 ON ANTES del primer handoff real del
modulo-app; SemVer MINOR + CHANGELOG; memoria actualizada.
