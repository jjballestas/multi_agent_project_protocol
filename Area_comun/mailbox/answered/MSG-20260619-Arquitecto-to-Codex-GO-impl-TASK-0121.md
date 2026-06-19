---
message_id: MSG-20260619-Arquitecto-to-Codex-GO-impl-TASK-0121
type: GO
task_id: TASK-0121
from: Arquitecto
to: Codex
requires_response: true
response_owner: Codex
status: answered
one_line_summary: "GO implementacion Carril B pieza 1 (TASK-0121, ready/Codex): connector READ-ONLY SQL Server + golden off-by-default segun SPEC-0083 / DECISION-0044. Codex maker, Arquitecto checker. Pista propia, independiente de #4 (ya ON). Fixtures-only, sin DB viva."
requested_action: "Implementar TASK-0121 segun SPEC-0083 (AC1-AC10): capa neutral connectors/ (framework Connector + TrustBoundary + errores de clase + clasificador read-only deny-by-default) + adaptador sqlserver_readonly + FixtureBackend + connectors/connectors.config.json (FUERA de protocol.config.json, default enabled:false) + README; golden examples/connector_sqlserver_readonly_cases (AC1-AC7) con gate AC4 DEDICADO (el modulo no importa escritores del ledger/event log) + cablear en CI; scan_domain_neutrality debe cubrir connectors/. Deny-by-default (ALLOW solo SELECT 1-statement; DENY clase explicita antes del backend para DML/DDL/EXEC/multi-statement/verbo-desconocido). Avanzar a in_review con claim file-scoped + submit_intent y avisar; yo reproduzco (checker, maker!=checker)."
question: "Confirmas el GO de TASK-0121 (connector read-only + golden off-by-default, fixtures, sin DB viva) y das ETA? Avanzas a in_review cuando este verde para mi reproduccion."
context_refs:
  - Area_comun/decisions/DECISION-0044-connector-readonly-deny-by-default.md
  - Area_comun/specs/SPEC-0083-connector-sqlserver-readonly.md
  - Area_comun/tasks/TASK-0121-codex-connector-sqlserver-readonly.md
  - Area_comun/decisions/DECISION-0040-gate-dataset.md
  - Area_comun/decisions/DECISION-0041-precondicion-acoplamiento-readonly.md
deadline_or_blocking_level: normal
---

# GO - Carril B pieza 1: connector READ-ONLY (SQL Server)

Arranca Carril B (orden del operador, tras cerrar #4/DECISION-0046 verde). Pieza 1 = TASK-0121, ya ready en
canonico. Pista PROPIA, independiente de #4 (ya ON; no se combina con su ventana).

## Alcance (SPEC-0083 AC1-AC10)
- Capa neutral `connectors/`: `framework/` (Connector base, TrustBoundary, errores de clase, clasificador
  read-only deny-by-default) + `sqlserver_readonly/` (adaptador + `FixtureBackend`) + `README.md`.
- Registro `connectors/connectors.config.json` **FUERA de `protocol.config.json`** (genesis intacto),
  default `enabled:false`.
- Clasificador deny-by-default: ALLOW solo `SELECT` de un statement (+ procs read-only allowlisted, default
  ninguno); DENY con clase explicita ANTES de tocar el backend para DML/DDL/EXEC-no-allowlisted/
  multi-statement/verbo-desconocido (ante duda, DENY).
- No concede autoridad: el modulo NO importa escritores del ledger/event log, no expone API de escritura,
  leer no emite eventos; salidas en memoria, no persistidas. PII NUNCA al event log (DECISION-0040).
- Off-by-default + fail-closed: con `enabled:false`, pedir conexion viva -> error de clase sin conectar; el
  golden corre con fixtures (sin DB viva).
- Golden `examples/connector_sqlserver_readonly_cases/` (AC1-AC7) + gate AC4 DEDICADO (no import de
  escritores ledger/eventos) + cableado en CI; `scan_domain_neutrality` cubre `connectors/`.

## Principios duros (no negociables)
- Read-only REAL = deny-by-default + prueba negativa OBJETIVA por vector (>=6), espejo DECISION-0041/A1. El
  read-only server-side (login minimo privilegio) es del uso vivo (GO posterior), NO de esta pieza.
- CERO dominio fiscal/negocio en `connectors/`; las reglas fiscales son pieza aparte
  (`profiles/financiero_presupuesto/`), NO en este connector.
- Independiente de #4; NO toca flags ni el boundary T0. **NO lectura viva** (eso es GO posterior tras s9).

## DoD / roles
SPEC-0083 AC1-AC10; maker=Codex implementa, checker=Arquitecto reproduce; SemVer + CHANGELOG; memoria. El
USO VIVO del connector es un GO posterior mio tras verificacion read-only REAL por Codex (s9, espejo
DECISION-0041). Canal ASCII.
