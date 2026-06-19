---
handoff_id: HANDOFF-TASK-0117-codex-to-arquitecto-1
task_id: TASK-0117
from: Codex
to: Arquitecto
status: ready_for_review
created_at: 2026-06-19T07:45:00Z
---

# TASK-0117 - Handoff Codex -> Arquitecto

## Summary

Infraestructura SPEC-0081 construida para la ventana "build != enable": harness/goldens/smoke listos sin
encender #4 ni correr piloto. `protocol.config.json` mantiene `event_auth.enabled=false`,
`chain_enabled=false`, `agent_signatures_enabled=false`, `anchor_enabled=false`.

## Implemented

- `examples/attestation_health_cases/run_attestation_health_cases.py`
  - AC1: provisioning smoke positivo y negativos por falta de `event_auth.keys` / `anchor_config.remote_url`.
  - AC2: N=20 fijo, denominador derivado de `event_log.agent.attestation`, reporte declara salud, no seguridad.
  - AC4: esquema de atestacion estructurado: sujeto por hash + predicado estructurado.
  - AC5: rollback dormido; flags off sin `prev_hash`, `event_auth`, atestaciones ni anchors.
- `examples/attestation_negative_cases/run_attestation_negative_cases.py`
  - AC3: 6 vectores binarios con diagnostico A1/A2:
    alteracion de payload, borrado, insercion, reordenamiento, llave no registrada, atribucion cruzada.
- `examples/readonly_enforcement_cases/run_readonly_enforcement_cases.py`
  - DECISION-0041/A3: prueba negativa objetiva sobre Core sintetico read-only; escritura rechazada por SO.
  - Revision AST para detectar APIs de escritura sobre el Core.
- `.github/workflows/validate.yml`: ejecuta los tres nuevos harnesses.
- `CHANGELOG.md`: entrada Unreleased; sin bump de version en esta ventana parcial.

## Verification

- OK: `python examples\attestation_health_cases\run_attestation_health_cases.py`
- OK: `python examples\attestation_negative_cases\run_attestation_negative_cases.py`
- OK: `python examples\readonly_enforcement_cases\run_readonly_enforcement_cases.py`
- OK: `python examples\chain_cases\run_tests.py`
- OK: `python examples\agent_signature_cases\run_agent_signature_cases.py`
- OK: `python examples\anchor_cases\run_anchor_cases.py`
- OK: `python examples\chain_auth_combined_cases\run_chain_auth_combined_cases.py`
- OK: `python -m py_compile examples\attestation_health_cases\run_attestation_health_cases.py examples\attestation_negative_cases\run_attestation_negative_cases.py examples\readonly_enforcement_cases\run_readonly_enforcement_cases.py`

## Limits

- No se encendio #4.
- No se corrio piloto.
- TASK-0118 sigue diferida.
- La prueba A3 es reproducible en Core sintetico read-only; no ejecuta lectura viva del satelite contra el Core real.
