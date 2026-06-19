---
id: TASK-0117
title: Activacion gateada de la atestacion de autoria (#4) - provisioning + piloto + encendido (DECISION-0039 / SPEC-0081)
type: security
status: in_review
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

## GO parcial 2026-06-19 - build harness, no enable

El operador autorizo la opcion 1: construir infraestructura SPEC-0081 sin encender #4 ni correr piloto.
TASK-0117 pasa a `in_progress` solo para el build de harness/goldens/smoke. El encendido, piloto y ON
siguen fuera de esta ventana y requieren GO posterior.

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

## Implementation Notes

- `examples/attestation_health_cases/run_attestation_health_cases.py`: AC1 provisioning smoke, AC2 N=20
  con denominador derivado del event log, AC4 esquema estructurado, AC5 rollback dormido.
- `examples/attestation_negative_cases/run_attestation_negative_cases.py`: AC3 con 6 vectores binarios
  y diagnostico A1/A2.
- `examples/readonly_enforcement_cases/run_readonly_enforcement_cases.py`: prueba negativa objetiva A3
  de DECISION-0041 contra un Core sintetico read-only, mas revision AST de rutas de escritura.
- `.github/workflows/validate.yml`: incluye los nuevos harnesses.
- `CHANGELOG.md`: registra el build de harness en Unreleased; #4 permanece OFF.

## Verification

- `python examples\attestation_health_cases\run_attestation_health_cases.py`
- `python examples\attestation_negative_cases\run_attestation_negative_cases.py`
- `python examples\readonly_enforcement_cases\run_readonly_enforcement_cases.py`
