---
id: TASK-0122
title: Replay secret-independiente - unresolved_key/missing_key no mutan estado (DECISION-0046 / SPEC-0084)
type: security
status: done
owner: Arquitecto
phase: P2
priority: high
spec_id: SPEC-0084
linked_decisions: [DECISION-0046, DECISION-0045, DECISION-0043]
created_at: 2026-06-19
---

# TASK-0122 - Replay secret-independiente

## Objective

Implementar el fix de DECISION-0046/SPEC-0084: en `runtime/eventlog.py:replay_events` (~428-440), clasificar
el resultado de `verify_event_auth` en UNVERIFIABLE_HERE (`unresolved_key`/`missing_key` = entorno sin
secreto -> aplicar el evento normal, sin rejection state-afectante, sin skip) vs TAMPER (`invalid_signature`/
`missing_signature` = rechazo real `security.unauthenticated_event` + skip, como hoy). Resultado: estado
materializado SECRET-INDEPENDIENTE -> `validate_collaboration_state --root .` exit 0 desde clon limpio SIN
secretos y desde la instancia viva CON secretos, mismo hash. Reconciliar el snapshot del head T0 a su forma
secret-independiente.

## maker != checker (orden del operador)

- **maker = Arquitecto** (implementa el fix + goldens).
- **checker = Codex** (reproduce independiente: AC1 rebuild con==sin secretos, AC2 tamper aun rechazado, AC3
  validate clon-limpio sin secretos exit 0, AC4 sin regresion #4).

## DoD

SPEC-0084 AC1-AC6; maker!=checker; SemVer + CHANGELOG; memoria; snapshot del head reconciliado. #4 sigue ON;
boundary T0 (DECISION-0045) intacto; deteccion de tamper NO debilitada.

## Verification

- `python examples\replay_secret_independent_cases\run_*.py` (AC1/AC2)
- clon del head T0 SIN secrets/ -> `validate_collaboration_state.py --root .` exit 0 (AC3/AC5)
- suites #4 verdes con secretos (AC4) + scan_encoding + scan_domain_neutrality
