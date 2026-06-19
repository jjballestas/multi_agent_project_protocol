---
message_id: MSG-20260619-Arquitecto-to-Operador-carril-B-DECISION-0044-promovida
type: RESPONSE
task_id: TASK-0121
from: Arquitecto
to: Operador
requires_response: false
response_owner: Operador
status: archived
one_line_summary: Confirmo scope Carril B pieza 1 y arranco el flujo - DECISION-0044 + SPEC-0083 + TASK-0121 (ready) promovidos al canonico, drift 0, #4 OFF. Falta el golden (Codex). Staging del GO a Codex pendiente de que actives a Codex para Carril B.
context_refs:
  - Area_comun/decisions/DECISION-0044-connector-readonly-deny-by-default.md
  - Area_comun/specs/SPEC-0083-connector-sqlserver-readonly.md
  - Area_comun/tasks/TASK-0121-codex-connector-sqlserver-readonly.md
  - MSG-20260619-Operador-to-Arquitecto-carril-B-GO-connector-sqlserver-ro
deadline_or_blocking_level: normal
---

# Carril B pieza 1 - scope confirmado, DECISION + SPEC + TASK promovidos

Confirmo el scope tal como lo planteaste y arranque el flujo DECISION -> SPEC -> golden.

## Scope confirmado (sin cambios respecto a tu GO)
- Connector SQL Server **read-only**, **deny-by-default**, **trust_boundary** por conector, principio
  "el connector no concede autoridad" (el dato es evidencia; el connector no escribe ledger/event log ni
  la fuente, leer no emite eventos).
- **Off-by-default**; golden con **fixtures** (sin DB viva).
- **Lectura viva = GO posterior tuyo** tras verificacion read-only REAL por Codex (s9, espejo
  DECISION-0041): deny-by-default connector-side + identidad de minimo privilegio server-side + prueba
  negativa objetiva registrada.
- **Cero dominio** en `connectors/`; las reglas fiscales van a `profiles/financiero_presupuesto/`, pieza
  aparte, NO en este connector.
- **Pista propia, independiente de #4** (sigue OFF; no se combinan ventanas de riesgo). PII nunca al
  event log (DECISION-0040); DEF-PII (TASK-0118) sigue diferida.

## Promovido al canonico (esta entrega)
- **DECISION-0044** (capacidad de connector read-only, deny-by-default, no concede autoridad, precondicion
  de uso vivo s9 con dueno Codex) - registrada en el ledger.
- **SPEC-0083** (diseno tecnico: framework `connectors/` + adaptador `sqlserver_readonly` + backend de
  fixtures + registro fuera de `protocol.config.json`; AC1-AC10 + test_plan).
- **TASK-0121** (Codex implementa el connector + golden) - estado **ready**.
- Transaccion atomica via submit_intent (claim acquire -> decision -> task_upsert -> release).
  **drift 0**, validador exit 0, encoding/neutralidad limpios. **Version sin tocar** (el bump + corte de
  CHANGELOG van con el golden al cierre, como TASK-0120 ready=1.12.0 -> done=1.13.0). #4 intacto/OFF.

## Lo que falta y la coordinacion
- El **golden** (off-by-default, fixtures) lo implementa **Codex** (maker != checker; yo reproduzco al
  cierre). El GO de implementacion para Codex esta **redactado y en staging** en mi area privada.
- Como activas a Codex/analista por proceso: dime cuando actives a **Codex para Carril B** y encolo el GO
  de TASK-0121 en el buzon. Mientras tanto no lo encolo (no asumo a Codex activo).
- No toco la DB de Budget ni su migracion. Nada de provisioning/flip de #4 aqui.
