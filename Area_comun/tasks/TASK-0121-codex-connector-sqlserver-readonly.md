---
id: TASK-0121
title: Connector READ-ONLY (SQL Server) deny-by-default + trust_boundary + golden off-by-default (DECISION-0044 / SPEC-0083)
type: security
status: done
owner: Codex
phase: P2
priority: high
spec_id: SPEC-0083
linked_decisions: [DECISION-0044, DECISION-0040, DECISION-0041]
created_at: 2026-06-19
---

# TASK-0121 - Connector READ-ONLY (SQL Server), deny-by-default

## Objective

Implementar Carril B pieza 1: una capacidad de connector neutral (`connectors/`), read-only,
deny-by-default, con `trust_boundary` por conector y el principio "el connector no concede autoridad", y
su primer adaptador (SQL Server read-only) con backend de **fixtures** (sin DB viva). Ver SPEC-0083 para
acceptance_criteria + test_plan. **Pista propia, independiente de #4** (sigue OFF). **NO ejerce lectura
viva** (eso es GO posterior tras verificacion §9; DECISION-0041/DECISION-0044 sec.4).

## Alcance (SPEC-0083)

- Capa neutral `connectors/`: `framework/` (Connector base, TrustBoundary, errores de clase, clasificador
  read-only deny-by-default) + `sqlserver_readonly/` (adaptador + `FixtureBackend`) + `README.md`.
- **Registro `connectors/connectors.config.json` FUERA de `protocol.config.json`** (genesis intacto),
  default `enabled:false`.
- **Clasificador read-only deny-by-default**: ALLOW solo `SELECT` de un statement (+ procs read-only
  explicitamente allowlisted, default ninguno); DENY con clase explicita ANTES de tocar el backend para
  DML/DDL/EXEC-no-allowlisted/multi-statement/verbo-desconocido (ante duda, DENY).
- **No concede autoridad / no escribe**: el modulo no importa escritores del ledger/event log, no expone
  API de escritura, leer no emite eventos; salidas en memoria, no persistidas (PII NUNCA al event log,
  DECISION-0040).
- **Off-by-default + fail-closed**: con `enabled:false`, pedir conexion viva -> error de clase sin
  conectar; el golden corre con fixtures independientemente del flag.
- Golden `examples/connector_sqlserver_readonly_cases/`; cablear en CI. `scan_domain_neutrality` debe
  cubrir `connectors/`.
- Gate AC4 dedicado (no delegar en `scan_encoding`/`scan_domain_neutrality`): el modulo no importa
  escritores del ledger/event log.

## DoD

SPEC-0083 AC1-AC10 cumplidos; maker!=checker (Codex implementa, Arquitecto reproduce); SemVer MINOR +
CHANGELOG; memoria actualizada. **NO enciende #4. NO lectura viva.** Drift 0 (la capa no toca genesis).

## Verification

- `python examples\connector_sqlserver_readonly_cases\run_connector_sqlserver_readonly_cases.py` (AC1-AC7)
- gate AC4 (no import de escritores ledger/eventos) -> exit 1 si se viola
- `python scripts\validate_collaboration_state.py --root .` (drift 0) + `scan_encoding.py` +
  `scan_domain_neutrality.py` (cubriendo `connectors/`)

## Implementation Notes

- Read-only REAL = deny-by-default + prueba negativa OBJETIVA por vector (>=6), espejo DECISION-0041/A1;
  el read-only **server-side** (login de minimo privilegio, escritura rechazada por el servidor) es del
  uso vivo (GO posterior), no de esta pieza.
- Genesis intacto: el registro de connectors vive FUERA de `protocol.config.json`.
- Neutralidad: CERO dominio fiscal en `connectors/`; las reglas fiscales son pieza aparte
  (`profiles/financiero_presupuesto/`), NO en este connector.
